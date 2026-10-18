# Chapter 34: Cisco ASA and FortiGate STIG Crosswalk

## Learning Objectives

- Explain why the Cisco ASA and FortiGate pair is the one crosswalk in this
  series where both products have DISA STIGs, and what that changes for an
  assessor.
- Align a Cisco ASA STIG rule with the FortiGate STIG rule, or the FortiGate
  setting, that implements the same SRG requirement.
- Use the Cisco ASA STIG rules as a working checklist for a FortiGate, and
  see where FortiGate meets, partly meets, or cannot meet each rule.
- Tell the six alignment categories apart and record each one correctly.
- Find the FortiGate STIG rules and SRG requirements that no ASA rule
  covers, so that the checklist covers both directions.
- Recognize the ASA fix texts that no longer parse on current ASA software,
  and the corrected commands.

## Theory and Architecture

**Both products in this crosswalk have STIGs.** The Cisco ASA (ASA 5500
and 5500-X, including FirePOWER Services) has a package of four STIGs: ASA
NDM V2R5 (47 rules, `CASA-ND-`), ASA Firewall V2R1 (21 rules,
`CASA-FW-`), ASA VPN V2R2 (41 rules, `CASA-VN-`), and ASA IPS V2R1
(23 rules, `CASA-IP-`; based on the ASA FirePOWER module and checked
through ASDM), 132 rules in all
([Chapter 31](31-cisco-products-stigs-and-srg-mapping.md)). FortiGate has
two: the Fortinet FortiGate Firewall NDM STIG V1R6 (`FGFW-ND-`) and Firewall
STIG V1R5 (`FNFG-FW-`), 89 rules, which
[Chapter 30](30-fortigate-feature-version-and-stig-map.md) maps to every
FortiGate feature together with the IDPS, VPN, ALG, and Router SRGs. Both
packages were written from the same SRGs, and every rule in both names the
SRG requirement it implements.

The earlier crosswalks in this volume, such as
[Chapter 33](33-fortiswitch-and-cisco-catalyst-switch-stig-crosswalk.md),
aligned a Cisco STIG with a product that has no STIG. This chapter is the
one **STIG-to-STIG pair** in the series: for every one of the 132 ASA
rules it gives the FortiGate STIG rule that implements the same SRG ID, if
there is one, and in every case the FortiGate setting and FortiOS command
that meet the requirement. 58 of the 132 ASA rules have
a FortiGate STIG rule for the same SRG requirement.

**This chapter is about ASA software, not Cisco Secure Firewall Threat
Defense (FTD).** FTD, the next-generation firewall software that runs on
Firepower and Secure Firewall appliances, has no STIG; as Chapter 31 explains,
it is assessed against the Firewall, IDPS, and VPN SRGs (and the NDM SRG with
its manager), and the ASA STIGs do not apply to it. A Firepower appliance
running the ASA image is covered by the ASA STIGs; the same appliance
running FTD is not.

### Why this is a crosswalk, and what the second STIG changes

A STIG is a vendor-specific implementation of one or more SRGs
([Chapter 03](03-the-srg-catalog-how-stigs-are-built-and-what-to-do-without-one.md)).
Its rules carry their own check and fix text, and an assessor records a
finding against the rule. A crosswalk keeps that distinction:

- **The ASA rule is a reference, not a requirement for FortiGate.** A
  FortiGate is never "compliant with `CASA-ND-000010`". Where a FortiGate
  STIG rule implements the same SRG ID (`FGFW-ND-000300` for
  `SRG-APP-000001-NDM-000200`), the FortiGate finding is recorded against
  that FortiGate rule, on the FortiGate STIG checklist. Where there is none,
  it is recorded against the SRG requirement on an SRG-based checklist.
- **The SRG ID is the join key.** Two settings align because they implement
  the same requirement, not because they look alike. ASA basic threat
  detection and a FortiGate DoS policy align because both implement
  `SRG-NET-000193-FW-000030`.
- **The two STIGs cover different ground.** The ASA package has VPN and IPS
  STIGs; FortiGate has none, so its VPN and IPS functions are assessed
  against the VPN and IDPS SRGs (Chapter 30). The FortiGate STIGs, in turn,
  have rules that no ASA rule matches, such as the administrator lockout and
  log protection rules. Chapter 30 maps FortiGate features to
  171 requirement IDs; 88 of them are cited by no ASA rule,
  including 32 of the 89 FortiGate STIG rules and every
  ALG and Router SRG requirement. The second table in this chapter lists
  them.

### How the rules are aligned

Each ASA rule was aligned in four steps:

1. **Take the SRG ID the rule implements.** The rule ID, severity, SRG ID,
   and title come from the four ASA STIG XCCDF files
   (`U_Cisco_ASA_Y26M07_STIG.zip`). The 132 rules cite 131
   distinct SRG IDs.
2. **Look for the same SRG ID in the FortiGate STIGs and in Chapter 30.** The
   FortiGate STIG rule column comes from the FortiGate XCCDF files
   (`U_FN_FortiGate_Firewall_Y26M10_STIG.zip`): 58 ASA rules
   (39 NDM and 19 Firewall) share an SRG ID with a
   FortiGate rule. Counting the SRG requirements that Chapter 30 maps
   directly (IDPS and VPN), 84 of the 132 rules cite an SRG
   ID that Chapter 30 maps to a FortiGate feature.
3. **For the rest, read the requirement and find the setting.** The
   requirement text comes from the SRG XCCDF files (NDM V5R5, Firewall V3R4,
   VPN V3R5, and IDPS V3R4). The FortiGate setting that meets it was found in
   the **FortiOS 8.0.1 CLI Reference**. Where the reference has no such
   setting, the row says so.
4. **Judge how well the setting meets the requirement**, and assign one of
   the alignment categories below.

Two cautions apply to the alignment data:

- **CCIs were not used to match requirements.** Many SRG requirements share
  the catch-all CCI-000366 ("security configuration settings"), so a CCI
  match often links unrelated requirements. Every alignment rests on the SRG
  ID or on the requirement text.
- **Six ASA rules cite SRG IDs that are not in the current SRG releases.**
  `CASA-ND-000940` cites `SRG-APP-000373-NDM-000298` (redundant time
  sources) and `CASA-ND-001420` cites `SRG-APP-000516-NDM-000351`
  (supported release); the current NDM requirements for the same topics are
  `SRG-APP-000920-NDM-000320` and `SRG-APP-001035-NDM-000340`. The FortiGate
  NDM STIG cites the same two retired IDs (`FGFW-ND-000120` and
  `FGFW-ND-000170`), so the rows still pair. `CASA-FW-000090` cites
  `SRG-NET-000089-FW-000019` (queue log records locally), which the FortiGate
  Firewall STIG also cites (`FNFG-FW-000045`); Firewall SRG V3R4 has no local
  queuing requirement, and the nearest current one is
  `SRG-NET-000333-FW-000014` (send traffic logs to a central server).
  `CASA-IP-000130` cites `SRG-NET-000089-IDPS-00010`, `CASA-VN-000080` cites
  `SRG-NET-000336-VPN-001280`, and `CASA-VN-000400` cites
  `SRG-NET-000320-VPN-001120`; the nearest current requirements are
  `SRG-NET-000334-IDPS-00191` and `SRG-NET-000334-VPN-001260` (off-load log
  records) and `SRG-NET-000015-VPN-000010` (enforce approved authorizations).

### Where the commands come from

- **Cisco ASA commands start from each rule's fix text.** There is no ASA
  feature map in this volume, so every ASA command was checked against the
  **Cisco Secure Firewall ASA Series Command Reference** (the A-H, I-R, S,
  and T-Z volumes; the table uses 101 command entries), read on
  cisco.com. A script checked every statement: it must match a command entry,
  every keyword must appear in that entry's syntax, every number must lie
  inside the documented range, a statement that belongs to a sub-mode must
  follow the statement that enters the mode (`encryption` after `crypto
  ikev2 policy`), port names must be literals from the port table of the ASA
  General Operations configuration guide for the protocol used, and a value
  that the entry's Command History marks as deprecated or removed fails. The
  script was tested with deliberately wrong commands (the fix texts'
  `dh-group14-sha`, `group 24`, `set pfs group5`, `priv aes` without a key
  size, `6/1514`, and the doubled `username-from-certificate`, an
  out-of-range timeout, an undocumented logging class, a UDP port name on a
  TCP entry, and a sub-mode statement without its parent) and caught all of
  them.
- **The ASA IPS STIG is configured in ASDM.** Its fix texts are ASDM steps
  for the ASA FirePOWER module. Each ASDM path and quoted label in the table
  was checked against the **ASA with FirePOWER Services Local Management
  Configuration Guide, Version 7.0**. Cells read "ASDM: path (what to set)".
- **FortiOS commands come from Chapter 30**, where the feature maps the same
  requirement, and otherwise from the **FortiOS 8.0.1 CLI Reference**. A
  script checked every FortiOS command against the 8.0.1 CLI Reference, as in
  Chapters 30 and 33: each `config` path must be documented, each nested
  `config` a documented sub-table, each `set` option an option of that path,
  and each literal value a documented value. It was tested with wrong
  commands (a misspelled path or option, `authmethod rsa`, `event-type
  ips-log`, an option of another table, `hop-opt block`) and caught all of
  them. GUI panes must appear in the FortiOS New Features Guides.
- Read the command cells as in Chapters 30 and 33: each pair of backticks is
  one block, statements are separated by `;` to fit in a table cell (on the
  CLI, enter each on its own line), and values in `<ANGLE_BRACKETS>` are
  placeholders. ASA sub-mode statements follow the statement that enters the
  mode; enter `exit` where you need to leave a mode.
- A dash (**—**) in a command column means the fix text or the CLI Reference
  gives no command for the requirement; the setting column says why.

**ASA fix text corrections.** DISA's ASA fix texts were written for older ASA
releases, and several do not parse on current software. The crosswalk uses
the corrected commands:

- `CASA-ND-000470`, `CASA-ND-001140`, and `CASA-ND-001150` set `ssh
  key-exchange group dh-group14-sha`, which is not a documented value; the
  values are `curve25519-sha256`, `dh-group14-sha1`, `dh-group14-sha256` (the
  default from 9.12(1)), and `ecdh-sha2-nistp256`. The crosswalk uses
  `dh-group14-sha256`. `CASA-ND-001140`, an integrity rule, sets `ssh cipher
  encryption fips`; the crosswalk uses `ssh cipher integrity fips`.
- `CASA-ND-000450` sets the local user's password and privilege in two
  `username` commands; the crosswalk uses one.
- `CASA-ND-001050` defines an SNMPv3 group with `priv` but a user without a
  privacy password, and `CASA-ND-001070` writes `priv aes` without a key
  size; the syntax is `priv aes {128 | 192 | 256}`. Both rows use `priv aes
  256`.
- `CASA-ND-001350` runs `copy` from an event manager applet without
  `/noconfirm`; the command reference says an applet command cannot accept
  input and to use the noconfirm option. Its second action (`action 2 syslog
  ...`) has no entry in the command reference and is left out.
- `CASA-FW-000010` runs the ACL name into the keyword (`INSIDE_INextended`),
  and `CASA-FW-000030` gives incomplete masks (`255.255.255.`).
- `CASA-FW-000100`, `CASA-FW-000200`, `CASA-VN-000090`, and `CASA-ND-001410`
  give the syslog transport as `6/1514` or `10.1.48.10/1514`; the syntax is
  `tcp/port` (or `udp/port`). The crosswalk uses `tcp/1514`.
- `CASA-FW-000250` says to apply the ACL inbound on the internal interface
  but writes `access-group INSIDE_IN out interface INSIDE`; the crosswalk
  uses `in`.
- `CASA-FW-000260` builds the management tunnel with IKEv1, DH group 5,
  SHA-1, and AES-192, names a transform set that it never defines, and has a
  malformed ACL line. The crosswalk keeps the rule's point (an ACL that
  selects the management traffic, bound to a crypto map) and uses an IKEv2
  proposal, so that the tunnel also meets the ASA VPN STIG.
- `CASA-FW-000280` builds an IPv6 inspection policy map but applies `inspect
  ipv6` without its name, so the map is never used; the crosswalk uses
  `inspect ipv6 <IPV6_MAP>`.
- `CASA-VN-000010`, `CASA-VN-000500` to `CASA-VN-000530`, and
  `CASA-VN-000720` use the logging classes `webvpn`, `webfo`, and `svc`,
  which are not in the command reference's list of valid classes; the
  crosswalk uses `vpn`, `vpnc`, and `vpnfo` (and `auth` for connection
  attempts). Check `logging class ?` on your release.
- `CASA-VN-000180` sets `set pfs group5`. The command reference syntax offers groups 14,
  15, 16, 19, 20, and 21, and the Command History says DH groups 1, 2, 5, and
  24 were removed in 9.15(1). The crosswalk uses `group20`.
- `CASA-VN-000210` sets `group 24` in the IKEv2 policy, and so does the ASA
  example in Chapter 31. DH group 24 was deprecated in 9.13(1) and removed in
  9.15(1); the IKEv2 policy accepts groups 14, 15, 16, 19, 20, 21, and 31.
  The crosswalk uses `group 20`, the group FortiGate uses (Chapter 30).
- `CASA-VN-000240` applies an IPsec proposal without naming it, and allows
  `sha-256` beside `sha-384` although the requirement is SHA-2 at 384 bits;
  the crosswalk names the proposal and uses `sha-384` only.
- `CASA-VN-000340` and `CASA-VN-000760` pair `integrity null` with
  `encryption aes-256`; the command reference allows null integrity only with
  AES-GCM. They also enter `protocol esp encryption` without entering
  `crypto ipsec ikev2 ipsec-proposal` first, and name a proposal (`AES-256`)
  they never define. The crosswalk uses `aes-gcm-256` in both phases.
- `CASA-VN-000450` repeats the keyword (`username-from-certificate
  username-from-certificate use-entire-name`).
- `CASA-IP-000130` points to *Devices > Platform Settings > Syslog Servers*,
  a Firepower Management Center page for FTD that is not in the ASA
  FirePOWER module guide. The crosswalk gives the ASA's own TCP syslog
  settings.
- `CASA-IP-000280` and `CASA-IP-000520` to `CASA-IP-000570` create email
  alert responses under *Policies >> Actions >> Alerts* and use an Advanced
  Malware Protection Alerts tab. The 7.0 guide names the page *ASA FirePOWER
  Configuration > Policies > Actions Alerts* and offers only syslog and SNMP
  alert responses, so the crosswalk sends the alerts to a monitored SIEM.

### Where the version columns come from

The crosswalk table has a version column for each platform:

- **ASA version** is the earliest release in the "Command History" table of
  each command's entry in the ASA command reference; where a cell uses
  several commands, it is the latest of those releases, so that every command
  in the cell is available. `or earlier` means that the history's earliest
  row records a change, not the command's introduction (the `logging enable`
  entry starts with "7.0(1) This command was changed from the logging on
  command"), so the command is at least that old. Where a rule depends on a
  keyword added later, the column gives that keyword's release with the
  keyword in parentheses, such as `9.13(1) (sha256 keyword)` for NTP
  authentication with SHA-256. `CASA-VN-000180` uses `group20`, which the
  Command History does not date. The ASDM steps of the IPS STIG have no
  command history; those cells read `ASA FirePOWER 7.0 guide (no command
  history)`, the guide in which they were verified.
- **FortiOS version** is the "Introduced (FortiOS)" entry of the Chapter 30
  feature that the FortiGate setting uses. Chapter 30 built that column from
  the FortiOS New Features Guides for 7.0 to 8.0; `7.0.0 or earlier` marks a
  core platform feature that predates them.
- **Not in the Chapter 30 feature map (8.0.1 CLI Reference)** marks a
  FortiOS setting that comes only from the 8.0.1 CLI Reference, such as VPN
  event logging or the IPv6 extension header filter, so no first release is
  given; check the CLI Reference for your release.
- A dash (**—**) means the row has no command on that platform.

### Prerequisites

A FortiGate setting often meets its requirement only if something else is
already in place. A **prerequisite** is anything that must exist or be
configured *before* a row's FortiGate setting can meet the requirement:
the FortiCare registration and support contract, a FortiGuard subscription
and a path to FortiGuard, a model capability (a log disk), an external
server (LDAP, syslog, FortiAnalyzer, SMTP, NTP, an SNMP manager),
certificates and revocation services from the DoD PKI, an operating mode
(FIPS-CC mode), or an earlier setting the row depends on (an administrator
profile, a user group, a management interface, an IPsec phase 1 interface,
a PKI peer user, a key chain, a firewall policy that applies the profile).
Settings that the row's own command creates are not listed again, and
neither are the FortiGate itself, its interfaces and routes, and the policy
table, which every row depends on. The prerequisites cover **the FortiGate
side only**.

The 25 prerequisites are Chapter 30's, with the same IDs, wording, and
commands, so that the map and the crosswalk agree; the build script checks
them against the *FortiGate prerequisites* table of Chapter 30. Only the
25 of Chapter 30's 48 that a row here needs are listed, so the IDs
are not consecutive. They are listed once in *FortiGate prerequisites*, and
the crosswalk and unmatched-requirement tables name the IDs each row needs
in their **FortiGate prerequisites** column:

- **Crosswalk rows.** A row whose FortiGate setting is a Chapter 30 feature
  takes that feature's IDs from Chapter 30 (100 rows). The other
  11 such rows use only part of the Chapter 30 command or add to it:
  the IPsec rows that set only the IKE proposal, DH group, or key lifetime
  do not list the certificate prerequisites (P15, P16, P19, and P44), which
  the certificate authentication rows carry; those of them that also set
  phase 2 list the phase 1 interface (P43); the TLS version row of the
  remote access VPN does not list the client certificate prerequisites; and
  `CASA-ND-001370` adds the FortiGate's own DoD certificate (P16), because
  its setting uses that certificate for HTTPS administration. The
  19 rows whose setting is not in the Chapter 30 feature map follow
  Chapter 30's rules.
- **Unmatched requirements.** Each row takes the IDs of the Chapter 30 row
  whose command it shows.

A dash means the setting needs nothing beyond the FortiGate, and the
2 rows with no FortiGate command always show a dash.

Fortinet publishes no FortiGate feature matrix in the documents Chapter 30
uses, so the **licenses** come from the FortiOS New Features Guides: the
FortiGuard service entitlements in *Update FortiGuard License Information
widget* (7.4.1), and the support contract and registration rules in
*Prevent FortiGates with an expired support contract from upgrading to a
major or minor firmware release* and the related 7.4 and 7.6 features. Here
they are the support contract (P1) on the firmware and update rows and the
Intrusion Prevention (P3), Advanced Malware Protection (P4), and Web
Filtering (P5) subscriptions on the IPS, antivirus, and web filter rows.
**Model support** is given only where a guide states it; the one such
prerequisite here is the log disk that local disk logging needs (P12).
Check *System > FortiGuard*, the release notes, and the hardware guides for
your exact model and release before you plan on a licensed or
model-specific feature.

During an assessment, check a row's prerequisites before its setting: a
correctly configured setting with a missing prerequisite (an IPS sensor on
a FortiGate without an IPS subscription, LDAPS with no DoD CA certificate
imported, a syslog setting with no TLS syslog server, local disk logging on
a model without a log disk) does not meet the requirement, and the missing
prerequisite is the finding.

### Alignment categories

Every row has one of six categories:

| Category | Meaning |
| --- | --- |
| Same requirement | Chapter 30 maps a FortiGate feature to the same SRG ID (directly, or through the FortiGate STIG rule that implements it), and the feature meets the requirement. |
| Equivalent setting | A FortiGate setting meets the requirement, although Chapter 30 did not map it to this SRG ID. |
| Partial | FortiGate meets part of the requirement. The setting column says what is missing. |
| Not supported | FortiGate has no such capability, so it cannot meet the rule. |
| Not applicable | The rule targets a component, role, or protocol that FortiGate does not have. |
| By procedure | The requirement is met by a process rather than a setting, on both platforms. |

**Partial**, **Not supported**, and **Not applicable** take precedence over
**Same requirement**: where Chapter 30 maps the same SRG ID but FortiGate
does not fully meet it, the row is Partial and its setting cell notes that
Chapter 30 maps the requirement.

## Design Considerations

- **Use both STIGs, and record against the right one.** In a mixed estate
  the ASA rules give one list of what to check on every firewall. For a
  FortiGate, record the finding against the FortiGate STIG rule in the
  FortiGate STIG rule column where there is one, and against the SRG
  requirement (VPN or IDPS) where there is not.
- **Take the stricter value where the two STIGs differ.** The ASA NDM STIG
  ends idle management sessions after **5 minutes**, as the SRG requires; the
  FortiGate NDM STIG allows **10**. The ASA VPN STIG allows an IKE security
  association to live **24 hours**, while the VPN SRG requirement it cites
  (`SRG-NET-000337-VPN-001300`) says eight hours, which the FortiGate
  setting in Chapter 30 meets. Set one organization-defined value for both
  platforms, at the stricter end.
- **Decide each firewall's role first.** The VPN and IPS rules apply only
  where the firewall terminates VPNs or inspects traffic with an IPS, and
  `CASA-FW-000250` only to a premise firewall behind the premise router.
- **Plan the cryptography together.** IKEv2 with AES-256 (or AES-256-GCM),
  SHA-384, and DH group 20 works on both platforms and meets both the ASA VPN
  STIG and the VPN SRG; use it for site-to-site tunnels between an ASA and a
  FortiGate.
- **Plan FIPS mode early on both.** ASA `fips enable` and FortiGate FIPS-CC
  mode both need a reload and change the available algorithms; enable them on
  a new device or in a maintenance window, and test VPN peers and management
  tools.
- **Check what the ASA software release supports.** Several fix texts use
  values that current ASA releases removed (DH groups 5 and 24, `3des`,
  `md5`); see *ASA fix text corrections*.

## Implementation and Automation

### FortiGate prerequisites

What must be in place before the FortiGate settings in the crosswalk can
meet their requirements (see *Prerequisites*). The rows are Chapter 30's,
unchanged, limited to the IDs this chapter's rows use. The commands were
verified with the same script as the crosswalk; entries that are not
FortiGate settings are described in words.

[Download the prerequisites as CSV](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/data/volume-172-disa-srgs-and-stigs/34-cisco-asa-and-fortigate-stig-crosswalk-prerequisites.csv) (25 rows).

| ID | Prerequisite | What it enables | How to put it in place | Source |
| --- | --- | --- | --- | --- |
| P1 | The FortiGate registered to FortiCare in a FortiCloud account, with a valid FortiCare support contract that includes Firmware & General Updates (FMWR) | Access to the GUI and the full CLI on models that enforce registration, upgrades to a new major or minor FortiOS release and firmware downloads from FortiGuard, and the FMWR definitions: application control signatures (including the generative AI database), virtual patch signatures for local-in policies, inline CASB application definitions, the Internet Service Database, and PSIRT vulnerability definitions | Register the FortiGate and its contracts on the FortiCloud support portal (in an air-gapped network, upload the license file in the setup wizard), then check the entitlements and expiry dates in GUI: System > FortiGuard | FortiOS 7.4.0 NFG, "Update FortiGuard License Information widget" (License Information widget: Firmware & General Updates and FortiCare Support entitlements), "Prevent FortiGates with an expired support contract from upgrading to a major or minor firmware release", "Prevent firmware upgrade depending on the current firmware license's expiration date", "Required firmware upgrades for FortiGate appliances with invalid support contracts or that have reached EOES", and "Add inline CASB security profile"; FortiOS 7.6.0 NFG, "Enforce FortiCare registration after new GUI login", "Enforce FortiCare registration with read-only CLI", and "Application control support for generative AI" (database updates require an FMWR contract) |
| P2 | A path from the FortiGate to the FortiGuard Distribution Network: DNS and a route to the FortiGuard servers with the traffic allowed outbound, or an upstream proxy or custom override servers (such as FortiManager), and FortiGuard anycast where a feature needs it | Signature, engine, and package updates, web filter and DNS filter rating queries, URL risk scores, virtual patching queries to the FortiGuard API, zero-day malware stream scanning, automatic firmware upgrade checks, the end-of-support and time zone packages, and reports of unauthorized firmware modification | Allow the FortiGuard traffic outbound, or set a proxy with `config system fortiguard; set proxy-server-ip <PROXY_IP>; set proxy-server-port <PORT>; end`; turn on anycast with `config system fortiguard; set fortiguard-anycast enable; end`; server preference in GUI: System > FortiGuard | FortiOS 8.0.0 NFG, "Enhanced FortiGuard server selection and load balancing" and "Configurable FQDN Host header for FortiGate proxy communication"; FortiOS 7.6.0 NFG, "Zero-day malware stream scanning" (FortiGuard Anycast must be enabled), "Introduce URL risk-scores in determining policy action", and "Streamline timezone updates with a downloadable database"; FortiOS 7.2.0 NFG, "Virtual patching on the local-in management interface" and "Support checking for firmware updates daily when auto firmware upgrade is enabled"; FortiOS 7.4.0 NFG, "Display warnings for supported Fabric devices passing their hardware EOS date" and "Unauthorized firmware modification attempt reporting" |
| P3 | A FortiGuard Intrusion Prevention (IPS) subscription | IPS definitions and engine updates, malicious URL and botnet IP and domain lists, the AI/Machine Learning IPS Definitions package (AI and ML-based IPS detection and DNS tunneling detection), and, on 7.2.4 and 7.2.5, virtual patching on the local-in interface | Purchase the subscription, register it to the FortiGate (P1), and check it in GUI: System > FortiGuard | FortiOS 7.4.0 NFG, "Update FortiGuard License Information widget" (Intrusion Prevention entitlement); FortiOS 7.6.0 NFG, "AI and ML-based IPS detection" (devices with an active IPS subscription); FortiOS 8.0.0 NFG, "Enhanced DNS security with AI and ML driven threat detection" (an active IPS subscription is required); FortiOS 7.2.0 NFG, "Virtual patching on the local-in management interface" (valid IPS license, changed in 7.2.6 and 7.4.1) |
| P4 | A FortiGuard Advanced Malware Protection (antivirus) subscription | Antivirus definitions and engine updates, the AI malware detection model, mobile malware definitions, and outbreak prevention hash queries for antivirus profiles | Purchase the subscription, register it to the FortiGate (P1), and check it in GUI: System > FortiGuard | FortiOS 7.4.0 NFG, "Update FortiGuard License Information widget" (Advanced Malware Protection entitlement); FortiOS 7.0.0 NFG, "AI-based malware detection" (devices with an active AV subscription) |
| P5 | A FortiGuard Web Filtering (Web Security) subscription | FortiGuard categories in web filter, DNS filter, and video filter profiles, URL risk scores, and the malicious certificate database (blocked certificates in SSL/SSH inspection and the client certificate blocklist of the secure explicit proxy) | Purchase the subscription, register it to the FortiGate (P1), and check it in GUI: System > FortiGuard | FortiOS 7.4.0 NFG, "Update FortiGuard License Information widget" (Web Filtering entitlement: the Web Security service); FortiOS 7.6.0 NFG, "Introduce URL risk-scores in determining policy action" (FortiGuard URL rating service); FortiOS 8.0.0 NFG, "Secure explicit proxy with client certificate blocklist enforcement" (an active FortiGuard subscription is required to use the Malicious Certificate Database) |
| P12 | A FortiGate model with a log disk (local disk storage) | Local disk logging, the policy change audit trail, log upload from disk, and quarantined files (which also work with FortiAnalyzer logging) | Check that `get system status` reports the log hard disk as available | FortiOS 7.2.0 NFG, "Add Policy change summary and Policy expiration to Workflow Management" (the Audit Trail is only supported by FortiGate models with disk logging); FortiOS 7.4.0 NFG, "Download quarantined files in archive format" (disk logging capacity or FortiAnalyzer); FortiOS 8.0.0 NFG, "Secure log upload enhancements with SFTP and LZ4 support"; get system status output in the NFGs (Log hard disk: Available or Not available) |
| P14 | Preparation for FIPS-CC mode: a maintenance window, because enabling the mode reboots the FortiGate and leaving FIPS cipher mode needs a factory reset; on cloud FortiGate VMs, all VPN configurations removed before the mode is enabled | FIPS-CC mode on appliances, and FIPS cipher mode on FortiGate VMs in public clouds | Schedule the change, back up the configuration, and on a cloud VM remove the VPN configuration first and re-create it after the mode is enabled | FortiOS 7.0.0 NFG, "FIPS cipher mode for OCI and GCP FortiGate VMs" (all VPN configurations must be removed; a factory reset is required to disable it); FortiOS 7.4.0 NFG, "Add built-in entropy source" (enabling FIPS-CC mode causes the FortiGate to reboot); FortiOS 7.2.0 NFG, "AWS silent fips-cipher enablement" |
| P15 | The DoD PKI root and intermediate CA certificates (and those of any other approved CA) imported into the FortiGate | Validation of administrator, user, and VPN peer certificates, and of the certificates of servers and Fabric devices the FortiGate connects to (LDAPS, certificate-authorized Fabric members) | GUI: System > Certificates (Import, CA Certificate) | Chapter row "CA certificates (DoD-approved CAs)"; FortiOS 8.0.1 CLI Reference, "config user peer" (ca) and "config user ldap" (ca-cert); FortiOS 8.0.0 NFG, "Enhancement to certificate authorization for Security Fabric devices" (the issuer must be a trusted CA) |
| P16 | A certificate issued to the FortiGate by the DoD PKI (from a certificate signing request) and imported as a local certificate | The HTTPS administration server certificate, IPsec signature authentication, the secure explicit proxy, and the client certificate for LDAPS servers that require one | Generate a certificate signing request, have the DoD PKI sign it, and import the signed certificate in GUI: System > Certificates | Chapter rows "Local certificate wizard" and "New default certificate for HTTPS administrative access"; FortiOS 8.0.1 CLI Reference, "config vpn ipsec phase1-interface" (certificate) and "config user ldap" (client-cert); FortiOS 7.2.0 NFG, "Configuring client certificate authentication on the LDAP server" |
| P18 | A DoD-issued subordinate CA certificate and key for SSL deep inspection, imported into the FortiGate, with its issuing CA in the trusted certificate store of every client | SSL deep inspection without certificate warnings, and the features that need deep inspection: HTTP/2 and HTTP/3 inspection, DNS over TLS and HTTPS inspection, Encrypted Client Hello control, video filtering, and inline CASB | Deploy the issuing CA to the client trust stores, import the certificate in GUI: System > Certificates (Import, Local Certificate), and select it with `config firewall ssl-ssh-profile; edit <PROFILE>; set caname <CA_CERT>; next; end` | FortiOS 8.0.1 CLI Reference, "config firewall ssl-ssh-profile" (caname); FortiOS 7.0.0 NFG, "Video filtering" (requires SSL deep inspection); FortiOS 7.4.0 NFG, "Add inline CASB security profile" (proxy-based inspection with a deep inspection SSL profile) |
| P19 | DoD CRL distribution points or OCSP responders reachable from the FortiGate, with CRL updates or OCSP checks configured | Revocation checks of administrator, user, VPN peer, and server certificates | `config vpn certificate crl; edit <CRL>; set http-url <CRL_URL>; set update-interval <SECONDS>; next; end`; or `config vpn certificate setting; set ocsp-status enable; set ocsp-default-server <OCSP_SERVER>; end` | FortiOS 8.0.1 CLI Reference, "config vpn certificate crl" (http-url, update-interval) and "config vpn certificate setting" (ocsp-status, ocsp-default-server) |
| P20 | DoD PKI certificates (such as the CAC) issued to the users and endpoints, with the middleware that presents them | Client certificate authentication for SSL VPN, dial-up IPsec VPN, the access proxy, and the secure explicit proxy, and LDAP- or RADIUS-integrated certificate authentication | Issued by the DoD PKI; not a FortiGate setting | FortiOS 7.0.0 NFG, "mTLS client certificate authentication" (clients are issued certificates by the CA); FortiOS 7.4.0 NFG, "IPsec IKEv2 VPN 2FA with EAP and certificate authentication" and "RADIUS integrated certificate authentication for SSL VPN"; FortiOS 7.2.0 NFG, "Specify the SAN field to use for LDAP-integrated certificate authentication" |
| P21 | An LDAP directory server reachable over LDAPS, with a bind account and the user and group objects | Remote administrator authentication with LDAP (and the restriction of local administrator logins while the server is reachable), user groups with remote members, and LDAP-integrated certificate authentication | Create the bind account on the directory, then test with `diagnose test authserver ldap <LDAP_SERVER> <USER> <PASSWORD>` | FortiOS 8.0.1 CLI Reference, "config user ldap"; FortiOS 7.2.0 NFG, "Improve admin-restrict-local handling of multiple authentication servers"; FortiOS 7.6.0 NFG, "Restrict local administrator logins through the console" |
| P28 | A syslog server that accepts reliable syslog over TLS | Remote syslog of FortiGate logs, and the health check that alerts when the syslog server stops responding | Configure the server for TLS on the reliable syslog port; not a FortiGate setting | FortiOS 8.0.1 CLI Reference, "config log syslogd setting" (mode reliable, enc-algorithm); chapter row "Logging to syslog servers over reliable TLS" |
| P29 | A FortiAnalyzer that has authorized the FortiGate (7.0.1 or later for authorization from the Fabric connector); for an alternate FortiAnalyzer, FortiAnalyzers in geo-redundant HA mode | Encrypted, reliable, real-time logging to FortiAnalyzer, its log caching, and switching to an alternate FortiAnalyzer | Authorize the device on the FortiAnalyzer, then check with `execute log fortianalyzer test-connectivity` | FortiOS 7.0.0 NFG, "Simplify Fabric approval workflow for FortiAnalyzer" (FortiAnalyzer 7.0.1 is required); FortiOS 7.4.0 NFG, "Support switching to an alternate FortiAnalyzer if the main FortiAnalyzer is unavailable" (geo-redundant HA mode) |
| P30 | An SMTP server that accepts mail from the FortiGate, and the mailbox of the ISSO and SA | Email actions of automation stitches (alerts on audit and log failure events) | `config system email-server; set server <SMTP_SERVER>; set port <PORT>; set security smtps; end` | FortiOS 8.0.1 CLI Reference, "config system email-server" and "config system automation-action" (action-type email) |
| P31 | Authoritative NTP servers (two or more) with authentication keys shared with the FortiGate | Authenticated, redundant time synchronization | Agree on the key ID and key with the NTP server administrator; check with `diagnose sys ntp status` | FortiOS 8.0.1 CLI Reference, "config system ntp" (ntpserver: authentication, key, key-id); chapter row "NTP with authenticated, redundant servers" |
| P32 | An SNMPv3 manager with the matching user, authentication, and privacy settings | SNMPv3 queries and traps, including queries from non-management VDOMs | Configure the user on the manager, and list it as a notify host with `config system snmp user; edit <NAME>; set notify-hosts <MANAGER_IP>; next; end` | FortiOS 8.0.1 CLI Reference, "config system snmp user"; FortiOS 7.2.0 NFG, "Access control for SNMP based on the MIB-view and VDOM"; FortiOS 7.6.0 NFG, "Non-management VDOMs perform queries using SNMP v3" |
| P40 | The administrator profile that an account will use | Least-privilege local, remote, and REST API administrator accounts | `config system accprofile; edit <PROFILE>; set sysgrp read; next; end`; or GUI: System > Admin Profiles | Chapter row "Administrator profiles: System access permission"; FortiOS 8.0.1 CLI Reference, "config system accprofile" |
| P41 | A user group whose members are the remote authentication server (or its groups) | Remote administrators matched on a server group, and user authentication groups for dial-up VPN | `config user group; edit <GROUP>; set member <LDAP_SERVER>; next; end`; or GUI: User & Authentication > User Groups | Chapter row "User groups with remote (LDAP) servers"; FortiOS 8.0.1 CLI Reference, "config user group" |
| P42 | A dedicated management interface on a separate management network, with address objects for the management hosts | Administrative access, local-in policies, DoS policies, and trusted hosts limited to the management network, and policies that keep management traffic off other networks | `config firewall address; edit <MGMT_HOSTS>; set subnet <IP> <MASK>; next; end`; interface settings in GUI: Network > Interfaces | Chapter rows "Administrative access protocols on each interface" and "Local-in policies (traffic to the FortiGate itself)"; FortiOS 8.0.1 CLI Reference, "config firewall address" |
| P43 | An IPsec VPN tunnel (phase 1 interface) to the peer | Phase 2 selectors, policies for traffic from VPN interfaces, and the tunnel features (serial number exchange, cross-validation, post-quantum and QKD key exchange) | `config vpn ipsec phase1-interface; edit <TUNNEL>; set interface <PORT>; set remote-gw <PEER_IP>; next; end`; or GUI: VPN > IPsec Tunnels | Chapter row "IPsec VPN phase 1 (IKEv2, AES-256, SHA-384, DH group 20, certificates)"; FortiOS 8.0.1 CLI Reference, "config vpn ipsec phase1-interface" |
| P44 | A PKI peer user that names the trusted CA and the expected certificate subject | IPsec certificate authentication that accepts only the intended peer | `config user peer; edit <PEER_USER>; set ca <CA_CERT>; set subject <SUBJECT>; next; end` | Chapter row "PKI peer users for certificate authentication"; FortiOS 8.0.1 CLI Reference, "config user peer" |
| P45 | The neighboring routers configured with the same authentication keys and key lifetimes, and the key chain defined on the FortiGate | Authenticated OSPF and BGP adjacencies | Agree on the keys with the neighbors' administrators; key chain: `config router key-chain; edit <KEYCHAIN>; config key; edit 1; set key-string <KEY>; set algorithm hmac-sha256; next; end; next; end` | Chapter rows "Key chains for routing protocol authentication" and "BGP neighbors (passwords, maximum prefixes, inbound prefix lists)"; FortiOS 8.0.1 CLI Reference, "config router key-chain" |
| P46 | A firewall policy (or proxy policy) that matches the traffic and applies the security profile, with proxy-based inspection for proxy-mode features | Security profile settings, which take effect only on the traffic of a policy that uses them | `config firewall policy; edit <POLICY_ID>; set inspection-mode proxy; set utm-status enable; next; end` (proxy mode only where the feature needs it); or GUI: Policy & Objects > Firewall Policy | FortiOS 8.0.1 CLI Reference, "config firewall policy" (inspection-mode, utm-status); FortiOS 7.4.0 NFG, "Add inline CASB security profile" (a firewall policy must use proxy-based inspection) |

### The crosswalk table

One row per Cisco ASA STIG rule: 47 ASA-NDM rules, then 21
ASA-FW rules, 41 ASA-VPN rules, and 23 ASA-IPS rules. Severity
is the ASA rule's category. The FortiGate STIG rule column gives the
FortiGate rule that implements the same SRG ID, or a dash where there is
none. The Requirement column summarizes what the ASA rule requires in plain
language; the SRG ID links it to the requirement text. The command columns
follow the conventions in *Where the commands come from*, the version
columns those in *Where the version columns come from*, and the
prerequisite IDs refer to *FortiGate prerequisites*.

[Download the crosswalk as CSV](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/data/volume-172-disa-srgs-and-stigs/34-cisco-asa-and-fortigate-stig-crosswalk-crosswalk.csv) (132 rows).

| ASA rule | Severity | SRG ID | FortiGate STIG rule | Requirement | ASA command | ASA version | FortiGate setting | FortiOS command | FortiOS version | FortiGate prerequisites | Alignment |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ASA-NDM `CASA-ND-000010` | CAT II | `SRG-APP-000001-NDM-000200` | FGT-NDM `FGFW-ND-000300` | Limit concurrent management sessions to an organization-defined number | `quota management-session <NUMBER>` | 9.1(2) | Maximum number of administrator logins, with concurrent logins of one account disabled | `config system global; set admin-concurrent disable; set admin-login-max <NUMBER>; end` | 7.0.0 or earlier | — | Same requirement |
| ASA-NDM `CASA-ND-000090` | CAT II | `SRG-APP-000026-NDM-000208` | FGT-NDM `FGFW-ND-000005` | Audit the creation of accounts | `logging enable; logging buffered informational` | 7.0(1) or earlier | System and user event logging | `config log eventfilter; set event enable; set system enable; set endpoint enable; set user enable; end` | 7.0.0 or earlier | — | Same requirement |
| ASA-NDM `CASA-ND-000100` | CAT II | `SRG-APP-000027-NDM-000209` | FGT-NDM `FGFW-ND-000010` | Audit the modification of accounts | `logging enable; logging buffered informational` | 7.0(1) or earlier | System and user event logging | `config log eventfilter; set event enable; set system enable; set endpoint enable; set user enable; end` | 7.0.0 or earlier | — | Same requirement |
| ASA-NDM `CASA-ND-000110` | CAT II | `SRG-APP-000028-NDM-000210` | — | Audit the disabling of accounts | `logging enable; logging buffered informational` | 7.0(1) or earlier | System and user event logging, which records changes to administrator accounts (the FortiGate NDM STIG has no rule for this SRG requirement) | `config log eventfilter; set event enable; set system enable; set endpoint enable; set user enable; end` | 7.0.0 or earlier | — | Equivalent setting |
| ASA-NDM `CASA-ND-000120` | CAT II | `SRG-APP-000029-NDM-000211` | FGT-NDM `FGFW-ND-000020` | Audit the removal of accounts | `logging enable; logging buffered informational` | 7.0(1) or earlier | System and user event logging | `config log eventfilter; set event enable; set system enable; set endpoint enable; set user enable; end` | 7.0.0 or earlier | — | Same requirement |
| ASA-NDM `CASA-ND-000140` | CAT II | `SRG-APP-000038-NDM-000213` | FGT-NDM `FGFW-ND-000035` | Allow management access only from authorized addresses | `ssh <MGMT_SUBNET> <MASK> <MGMT_INTERFACE>` | 7.0(1) | Trusted hosts on each administrator account (local-in policies can restrict management traffic further) | `config system admin; edit <ADMIN>; set trusthost1 <IP> <MASK>; next; end` | 7.0.0 or earlier | P42 | Same requirement |
| ASA-NDM `CASA-ND-000160` | CAT II | `SRG-APP-000068-NDM-000215` | FGT-NDM `FGFW-ND-000050` | Show the DoD Notice and Consent Banner before logon | `banner login <DOD_BANNER_LINE>` | 7.2(4) or earlier | Pre-login disclaimer banner | `config system global; set pre-login-banner enable; end` `config system replacemsg admin; edit pre_admin-disclaimer-text; set buffer "<DOD_BANNER_TEXT>"; next; end` | 7.0.0 or earlier | — | Same requirement |
| ASA-NDM `CASA-ND-000210` | CAT II | `SRG-APP-000080-NDM-000220` | FGT-NDM `FGFW-ND-000060` | Log administrator activity for non-repudiation | `logging enable; logging buffered informational` | 7.0(1) or earlier | System and user event logging | `config log eventfilter; set event enable; set system enable; set endpoint enable; set user enable; end` | 7.0.0 or earlier | — | Same requirement |
| ASA-NDM `CASA-ND-000240` | CAT II | `SRG-APP-000091-NDM-000223` | — | Log successful and unsuccessful attempts to access privileges | `logging enable; logging buffered informational` | 7.0(1) or earlier | System and user event logging (logons, privilege use, and configuration changes) | `config log eventfilter; set event enable; set system enable; set endpoint enable; set user enable; end` | 7.0.0 or earlier | — | Equivalent setting |
| ASA-NDM `CASA-ND-000260` | CAT II | `SRG-APP-000095-NDM-000225` | — | Record what type of event occurred | `logging enable; logging buffered informational` | 7.0(1) or earlier | System and user event logging; each log record carries its log ID, type, and subtype | `config log eventfilter; set event enable; set system enable; set endpoint enable; set user enable; end` | 7.0.0 or earlier | — | Equivalent setting |
| ASA-NDM `CASA-ND-000270` | CAT II | `SRG-APP-000096-NDM-000226` | — | Record the date and time of each event | `logging timestamp` | 7.0(1) | Log records take their date and time from the system clock; set the time zone and synchronize the clock (`CASA-ND-000940`) | `config system global; set timezone <TIMEZONE>; end` | 7.0.0 or earlier | — | Equivalent setting |
| ASA-NDM `CASA-ND-000280` | CAT II | `SRG-APP-000097-NDM-000227` | — | Record where each event occurred | `logging enable; logging buffered informational` | 7.0(1) or earlier | System and user event logging; each record identifies the FortiGate, the VDOM, and the interface or source involved | `config log eventfilter; set event enable; set system enable; set endpoint enable; set user enable; end` | 7.0.0 or earlier | — | Equivalent setting |
| ASA-NDM `CASA-ND-000290` | CAT II | `SRG-APP-000098-NDM-000228` | — | Record the source of each event | `logging enable; logging buffered informational` | 7.0(1) or earlier | System and user event logging, with user names left in the logs | `config log setting; set user-anonymize disable; end` | 7.0.0 or earlier | — | Equivalent setting |
| ASA-NDM `CASA-ND-000300` | CAT II | `SRG-APP-000099-NDM-000229` | — | Record the outcome of each event | `logging enable; logging buffered informational` | 7.0(1) or earlier | System and user event logging; records carry the action and status of the event | `config log eventfilter; set event enable; set system enable; set endpoint enable; set user enable; end` | 7.0.0 or earlier | — | Equivalent setting |
| ASA-NDM `CASA-ND-000320` | CAT II | `SRG-APP-000101-NDM-000231` | FGT-NDM `FGFW-ND-000100` | Record the full text of privileged commands | `logging enable; logging buffered informational` | 7.0(1) or earlier | CLI audit log, which records each command entered | `config system global; set cli-audit-log enable; end` | 7.0.0 or earlier | — | Same requirement |
| ASA-NDM `CASA-ND-000430` | CAT I | `SRG-APP-000142-NDM-000245` | FGT-NDM `FGFW-ND-000200` | Disable unnecessary and nonsecure functions, ports, protocols, and services | `no http server enable; no telnet <IP> <MASK> <INTERFACE>` | 7.0(1) | Allow only HTTPS and SSH for management, on the management interface (no HTTP or Telnet) | `config system interface; edit <MGMT_PORT>; set allowaccess ping https ssh; next; end` | 7.0.0 or earlier | P42 | Same requirement |
| ASA-NDM `CASA-ND-000450` | CAT II | `SRG-APP-000148-NDM-000346` | FGT-NDM `FGFW-ND-000030` | Keep only one local account, as the account of last resort | `username <LAST_RESORT> password <PASSWORD> privilege 15; aaa-server <AAA_GROUP> protocol radius; aaa-server <AAA_GROUP> (<MGMT_INTERFACE>) host <SERVER_IP>; key <KEY>; aaa authentication serial console <AAA_GROUP> LOCAL; aaa authentication ssh console <AAA_GROUP> LOCAL` | 7.2(1) or earlier | One local administrator; all others matched on a remote server group | `config system admin; edit <ADMIN>; set remote-auth enable; set accprofile <PROFILE>; set remote-group <GROUP>; next; end` | 7.0.0 or earlier | P21, P40, P41 | Same requirement |
| ASA-NDM `CASA-ND-000470` | CAT II | `SRG-APP-000156-NDM-000250` | FGT-NDM `FGFW-ND-000205` | Use replay-resistant authentication for privileged network access | `fips enable; ssh cipher encryption fips; ssh key-exchange group dh-group14-sha256` | 9.12(1) (dh-group14-sha256) | TLS 1.2 or later for HTTPS administration and no SSH version 1 | `config system global; set admin-https-ssl-versions tlsv1-2 tlsv1-3; set admin-ssh-v1 disable; end` | 7.0.0 or earlier | — | Same requirement |
| ASA-NDM `CASA-ND-000490` | CAT II | `SRG-APP-000164-NDM-000252` | FGT-NDM `FGFW-ND-000220` | Require passwords of at least 15 characters | `password-policy minimum-length 15` | 9.1(2) | Administrator password policy | `config system password-policy; set status enable; set apply-to admin-password; set minimum-length 15; end` | 7.0.0 or earlier | — | Same requirement |
| ASA-NDM `CASA-ND-000520` | CAT II | `SRG-APP-000166-NDM-000254` | FGT-NDM `FGFW-ND-000225` | Require at least one uppercase character | `password-policy minimum-uppercase 1` | 9.1(2) | Administrator password policy | `config system password-policy; set status enable; set min-upper-case-letter 1; end` | 7.0.0 or earlier | — | Same requirement |
| ASA-NDM `CASA-ND-000530` | CAT II | `SRG-APP-000167-NDM-000255` | FGT-NDM `FGFW-ND-000230` | Require at least one lowercase character | `password-policy minimum-lowercase 1` | 9.1(2) | Administrator password policy | `config system password-policy; set status enable; set min-lower-case-letter 1; end` | 7.0.0 or earlier | — | Same requirement |
| ASA-NDM `CASA-ND-000550` | CAT II | `SRG-APP-000168-NDM-000256` | FGT-NDM `FGFW-ND-000235` | Require at least one numeric character | `password-policy minimum-numeric 1` | 9.1(2) | Administrator password policy | `config system password-policy; set status enable; set min-number 1; end` | 7.0.0 or earlier | — | Same requirement |
| ASA-NDM `CASA-ND-000570` | CAT II | `SRG-APP-000169-NDM-000257` | FGT-NDM `FGFW-ND-000240` | Require at least one special character | `password-policy minimum-special 1` | 9.1(2) | Administrator password policy | `config system password-policy; set status enable; set min-non-alphanumeric 1; end` | 7.0.0 or earlier | — | Same requirement |
| ASA-NDM `CASA-ND-000580` | CAT II | `SRG-APP-000170-NDM-000329` | FGT-NDM `FGFW-ND-000311` | Change at least eight character positions when a password changes | `password-policy minimum-changes 8` | 9.1(2) | Chapter 30 maps this requirement (FGFW-ND-000311), but the 8.0.1 CLI Reference has no changed-characters option for administrator passwords (7.0 to 7.6 have `min-change-characters`); give administrators remote accounts whose directory enforces it | — | — | — | Partial |
| ASA-NDM `CASA-ND-000690` | CAT I | `SRG-APP-000190-NDM-000267` | FGT-NDM `FGFW-ND-000275` | End management sessions after five minutes of inactivity | `ssh timeout 5; console timeout 5; http server idle-timeout 5` | 8.2(1) | Administrator idle timeout set to 5 minutes; the FortiGate STIG rule allows 10, the SRG requirement five | `config system global; set admintimeout 5; end` | 7.0.0 or earlier | — | Same requirement |
| ASA-NDM `CASA-ND-000910` | CAT II | `SRG-APP-000343-NDM-000289` | FGT-NDM `FGFW-ND-000040` | Audit the execution of privileged functions | `logging enable; logging buffered informational` | 7.0(1) or earlier | System and user event logging | `config log eventfilter; set event enable; set system enable; set endpoint enable; set user enable; end` | 7.0.0 or earlier | — | Same requirement |
| ASA-NDM `CASA-ND-000920` | CAT II | `SRG-APP-000357-NDM-000293` | FGT-NDM `FGFW-ND-000105` | Allocate audit record storage capacity | `logging flash-maximum-allocation <KBYTES>; logging flash-minimum-free <KBYTES>` | 7.0(1) | Local disk logging with a maximum log file size and full-disk behavior | `config log disk setting; set status enable; set max-log-file-size <MB>; set diskfull overwrite; end` | 7.0.0 or earlier | P12 | Same requirement |
| ASA-NDM `CASA-ND-000930` | CAT II | `SRG-APP-000360-NDM-000295` | FGT-NDM `FGFW-ND-000115` | Alert in real time on audit failure events | `logging host <MGMT_INTERFACE> <SYSLOG_IP>; logging trap critical` | 7.0(1) | Automation stitch that emails an alert on each log failure event | `config system automation-trigger; edit <TRIGGER>; set event-type event-log; set logid <LOG_ID>; next; end` `config system automation-action; edit <ACTION>; set action-type email; set email-to <ADDRESS>; set email-subject <SUBJECT>; next; end` | 7.0.0 or earlier | P30 | Same requirement |
| ASA-NDM `CASA-ND-000940` | CAT II | `SRG-APP-000373-NDM-000298` | FGT-NDM `FGFW-ND-000120` | Synchronize the clock with redundant authoritative time sources | `ntp server <NTP_IP_1> prefer; ntp server <NTP_IP_2>` | 7.0(1) or earlier | Two authenticated NTP servers | `config system ntp; set ntpsync enable; set type custom; config ntpserver; edit 1; set server <NTP_SERVER_1>; next; edit 2; set server <NTP_SERVER_2>; next; end; end` | 7.0.0 or earlier | P31 | Same requirement |
| ASA-NDM `CASA-ND-000970` | CAT II | `SRG-APP-000375-NDM-000300` | — | Time-stamp audit records to one second | `logging timestamp` | 7.0(1) | Log records carry the date and the time to the second from the system clock; keep the clock synchronized | `config system global; set timezone <TIMEZONE>; end` | 7.0.0 or earlier | — | Equivalent setting |
| ASA-NDM `CASA-ND-001050` | CAT II | `SRG-APP-000395-NDM-000310` | FGT-NDM `FGFW-ND-000210` | Authenticate SNMP messages with a FIPS-validated HMAC | `snmp-server group <GROUP> v3 priv; snmp-server user <USER> <GROUP> v3 auth sha <AUTH_PASSWORD> priv aes 256 <PRIV_PASSWORD>; snmp-server host <MGMT_INTERFACE> <NMS_IP> version 3 <USER>` | 8.2(1) | SNMPv3 user with SHA-256 authentication and AES-256 privacy | `config system snmp user; edit <NAME>; set status enable; set security-level auth-priv; set auth-proto sha256; set auth-pwd <PASSWORD>; set priv-proto aes256; set priv-pwd <PASSWORD>; next; end` | 7.0.0 or earlier | P32 | Same requirement |
| ASA-NDM `CASA-ND-001070` | CAT II | `SRG-APP-000395-NDM-000310` | FGT-NDM `FGFW-ND-000210` | Encrypt SNMP messages with a FIPS-approved algorithm | `snmp-server group <GROUP> v3 priv; snmp-server user <USER> <GROUP> v3 auth sha <AUTH_PASSWORD> priv aes 256 <PRIV_PASSWORD>; snmp-server host <MGMT_INTERFACE> <NMS_IP> version 3 <USER>` | 8.2(1) | SNMPv3 user with AES-256 privacy | `config system snmp user; edit <NAME>; set status enable; set security-level auth-priv; set auth-proto sha256; set auth-pwd <PASSWORD>; set priv-proto aes256; set priv-pwd <PASSWORD>; next; end` | 7.0.0 or earlier | P32 | Same requirement |
| ASA-NDM `CASA-ND-001080` | CAT II | `SRG-APP-000395-NDM-000347` | FGT-NDM `FGFW-ND-000215` | Authenticate NTP sources with FIPS-compliant algorithms | `ntp authenticate; ntp trusted-key 1; ntp authentication-key 1 sha256 <KEY>; ntp server <NTP_IP_1> key 1 prefer; ntp server <NTP_IP_2> key 1` | 9.13(1) (sha256 keyword) | NTP server authentication; the 8.0.1 CLI Reference also offers `set key-type SHA256` for each server | `config system ntp; set ntpsync enable; set type custom; config ntpserver; edit 1; set server <NTP_SERVER_1>; set authentication enable; set key <KEY>; set key-id <KEY_ID>; next; end; end` | 7.0.0 or earlier | P31 | Same requirement |
| ASA-NDM `CASA-ND-001140` | CAT I | `SRG-APP-000411-NDM-000330` | FGT-NDM `FGFW-ND-000260` | Protect the integrity of remote maintenance with a FIPS-validated HMAC | `fips enable; ssh cipher integrity fips; ssh key-exchange group dh-group14-sha256` | 9.12(1) (dh-group14-sha256) | Strong cryptography for HTTPS and SSH administration | `config system global; set strong-crypto enable; end` | 7.0.0 or earlier | — | Same requirement |
| ASA-NDM `CASA-ND-001150` | CAT I | `SRG-APP-000412-NDM-000331` | FGT-NDM `FGFW-ND-000265` | Protect the confidentiality of remote maintenance with FIPS-approved cryptography | `fips enable; ssh cipher encryption fips; ssh key-exchange group dh-group14-sha256` | 9.12(1) (dh-group14-sha256) | Strong cryptography for HTTPS and SSH administration | `config system global; set strong-crypto enable; end` | 7.0.0 or earlier | — | Same requirement |
| ASA-NDM `CASA-ND-001180` | CAT II | `SRG-APP-000435-NDM-000315` | FGT-NDM `FGFW-ND-000290` | Protect against known denial-of-service attacks | `threat-detection basic-threat` | 8.0(2) | DoS policy on the management interface with L3 and L4 anomaly thresholds | `config firewall DoS-policy; edit <ID>; set interface <INTERFACE>; set srcaddr <SRC_ADDRESS>; set dstaddr <DST_ADDRESS>; set service <SERVICE>; config anomaly; edit <ANOMALY>; set status enable; set log enable; set action block; set threshold <THRESHOLD>; next; end; next; end` | 7.0.0 or earlier | P42 | Same requirement |
| ASA-NDM `CASA-ND-001200` | CAT II | `SRG-APP-000495-NDM-000318` | FGT-NDM `FGFW-ND-000065` | Log attempts to modify administrator privileges | `logging enable; logging buffered informational` | 7.0(1) or earlier | System and user event logging | `config log eventfilter; set event enable; set system enable; set endpoint enable; set user enable; end` | 7.0.0 or earlier | — | Same requirement |
| ASA-NDM `CASA-ND-001210` | CAT II | `SRG-APP-000499-NDM-000319` | FGT-NDM `FGFW-ND-000070` | Log attempts to delete administrator privileges | `logging enable; logging buffered informational` | 7.0(1) or earlier | System and user event logging | `config log eventfilter; set event enable; set system enable; set endpoint enable; set user enable; end` | 7.0.0 or earlier | — | Same requirement |
| ASA-NDM `CASA-ND-001220` | CAT II | `SRG-APP-000503-NDM-000320` | FGT-NDM `FGFW-ND-000075` | Log successful and unsuccessful logons | `logging enable; logging buffered informational` | 7.0(1) or earlier | System and user event logging | `config log eventfilter; set event enable; set system enable; set endpoint enable; set user enable; end` | 7.0.0 or earlier | — | Same requirement |
| ASA-NDM `CASA-ND-001230` | CAT II | `SRG-APP-000504-NDM-000321` | FGT-NDM `FGFW-ND-000080` | Log privileged activities and system-level access | `logging enable; logging buffered informational` | 7.0(1) or earlier | System and user event logging | `config log eventfilter; set event enable; set system enable; set endpoint enable; set user enable; end` | 7.0.0 or earlier | — | Same requirement |
| ASA-NDM `CASA-ND-001240` | CAT II | `SRG-APP-000505-NDM-000322` | FGT-NDM `FGFW-ND-000085` | Log the start and end time of administrator sessions | `logging enable; logging timestamp; logging buffered informational` | 7.0(1) or earlier | System and user event logging | `config log eventfilter; set event enable; set system enable; set endpoint enable; set user enable; end` | 7.0.0 or earlier | — | Same requirement |
| ASA-NDM `CASA-ND-001250` | CAT II | `SRG-APP-000506-NDM-000323` | FGT-NDM `FGFW-ND-000090` | Log concurrent logons from different workstations | `logging enable; logging buffered informational` | 7.0(1) or earlier | System and user event logging | `config log eventfilter; set event enable; set system enable; set endpoint enable; set user enable; end` | 7.0.0 or earlier | — | Same requirement |
| ASA-NDM `CASA-ND-001310` | CAT I | `SRG-APP-000516-NDM-000336` | FGT-NDM `FGFW-ND-000165` | Use at least two authentication servers for administrator access | `aaa-server <AAA_GROUP> protocol radius; aaa-server <AAA_GROUP> (<MGMT_INTERFACE>) host <SERVER_IP_1>; key <KEY_1>; aaa-server <AAA_GROUP> (<MGMT_INTERFACE>) host <SERVER_IP_2>; key <KEY_2>; aaa authentication serial console <AAA_GROUP> LOCAL; aaa authentication ssh console <AAA_GROUP> LOCAL` | 7.2(1) or earlier | LDAP server over LDAPS with a secondary server (the FortiGate STIG rule requires LDAP; the SRG requires two servers on boundary devices) | `config user ldap; edit <LDAP_SERVER>; set server <SERVER_IP_1>; set secondary-server <SERVER_IP_2>; set secure ldaps; set ca-cert <CA_CERT>; next; end` | 7.0.0 or earlier | P15, P21 | Same requirement |
| ASA-NDM `CASA-ND-001350` | CAT II | `SRG-APP-000516-NDM-000340` | FGT-NDM `FGFW-ND-000180` | Back up the configuration when it changes | `event manager applet <APPLET>; event syslog id 111010; action 1 cli command "copy /noconfirm startup-config scp://<USER>:<PASSWORD>@<SCP_SERVER>/<PATH>"` | 9.2(1) | Configuration revision backup on administrator logout (or FortiManager revision history) | `config system global; set revision-backup-on-logout enable; end` | 7.0.0 or earlier | — | Same requirement |
| ASA-NDM `CASA-ND-001370` | CAT II | `SRG-APP-000516-NDM-000344` | FGT-NDM `FGFW-ND-000195` | Obtain certificates from a DoD-approved certificate authority | — | — | Import DoD-approved CA certificates, and use a certificate they issued for HTTPS administration | GUI: System > Certificates | 7.0.0 or earlier | P15, P16 | Same requirement |
| ASA-NDM `CASA-ND-001410` | CAT I | `SRG-APP-000516-NDM-000350` | FGT-NDM `FGFW-ND-000295` | Send log data to at least two central log servers | `logging host <MGMT_INTERFACE> <SYSLOG_IP_1> tcp/1514; logging host <MGMT_INTERFACE> <SYSLOG_IP_2> tcp/1514; logging trap notifications` | 7.0(1) | Two syslog servers over reliable TLS (or FortiAnalyzer and syslog); the FortiGate STIG rule asks for one server, the SRG for two on boundary devices | `config log syslogd setting; set status enable; set server <SYSLOG_IP_1>; set mode reliable; set enc-algorithm high; end` `config log syslogd2 setting; set status enable; set server <SYSLOG_IP_2>; set mode reliable; set enc-algorithm high; end` | 7.0.0 or earlier | P28 | Same requirement |
| ASA-NDM `CASA-ND-001420` | CAT I | `SRG-APP-000516-NDM-000351` | FGT-NDM `FGFW-ND-000170` | Run a release the vendor supports | `show version` | 7.2(1) or earlier | Run a FortiOS release Fortinet supports; check the running release | `get system status` | 7.0.0 or earlier | P1, P2 | Same requirement |
| ASA-FW `CASA-FW-000010` | CAT I | `SRG-NET-000019-FW-000003` | FGT-FW `FNFG-FW-000005` | Filter outbound traffic, allowing only authorized ports and services | `access-list <INSIDE_ACL> extended permit tcp any any eq https; access-list <INSIDE_ACL> extended deny ip any any log; access-group <INSIDE_ACL> in interface <INSIDE>` | 7.0(1) | Firewall policies on interfaces, addresses, services, and schedules; anything not allowed is denied | `config firewall policy; edit <POLICY_ID>; set srcintf <IN_INTERFACE>; set dstintf <OUT_INTERFACE>; set srcaddr <SRC_ADDRESS>; set dstaddr <DST_ADDRESS>; set schedule <SCHEDULE>; set service <SERVICE>; set action accept; set logtraffic all; next; end` | 7.0.0 or earlier | — | Same requirement |
| ASA-FW `CASA-FW-000020` | CAT II | `SRG-NET-000019-FW-000004` | — | Use updates to the rule base immediately | `no asp rule-engine transactional-commit access-group` | 9.1(5) | No setting needed: a firewall policy change takes effect when it is saved; FortiOS has no transactional-commit option for policies to turn off | — | — | — | Equivalent setting |
| ASA-FW `CASA-FW-000030` | CAT II | `SRG-NET-000061-FW-000001` | FGT-FW `FNFG-FW-000015` | Filter remote access VPN traffic with organization-defined rules | `access-list <VPN_ACL> extended permit tcp <VPN_POOL> <MASK> host <SERVER_IP> eq https; access-list <VPN_ACL> extended deny ip any any log; group-policy <GROUP_POLICY> attributes; vpn-filter value <VPN_ACL>` | 7.0(1) | Firewall policies for traffic from the VPN interface | `config firewall policy; edit <POLICY_ID>; set srcintf <VPN_INTERFACE>; set dstintf <INTERFACE>; set srcaddr <SRC_ADDRESS>; set dstaddr <DST_ADDRESS>; set schedule <SCHEDULE>; set service <SERVICE>; set action accept; set logtraffic all; next; end` | 7.0.0 or earlier | P43 | Same requirement |
| ASA-FW `CASA-FW-000040` | CAT II | `SRG-NET-000074-FW-000009` | FGT-FW `FNFG-FW-000020` | Record what type of traffic event occurred | `logging enable; access-list <ACL> extended deny ip any any log` | 7.0(1) or earlier | Traffic logging on every policy | `config firewall policy; edit <POLICY_ID>; set logtraffic all; next; end` | 7.0.0 or earlier | — | Same requirement |
| ASA-FW `CASA-FW-000050` | CAT II | `SRG-NET-000075-FW-000010` | FGT-FW `FNFG-FW-000025` | Record the date and time of traffic events | `logging timestamp` | 7.0(1) | Traffic logging; records carry the date and time | `config firewall policy; edit <POLICY_ID>; set logtraffic all; next; end` | 7.0.0 or earlier | — | Same requirement |
| ASA-FW `CASA-FW-000090` | CAT II | `SRG-NET-000089-FW-000019` | FGT-FW `FNFG-FW-000045` | Queue log records locally when the central server is unreachable | `logging buffered informational; logging queue 8192` | 7.0(1) | Local disk logging alongside the central server | `config log disk setting; set status enable; set max-log-file-size <MB>; set diskfull overwrite; end` | 7.0.0 or earlier | P12 | Same requirement |
| ASA-FW `CASA-FW-000100` | CAT II | `SRG-NET-000098-FW-000021` | FGT-FW `FNFG-FW-000050` | Use TCP to send log records to the central server | `logging host <MGMT_INTERFACE> <SYSLOG_IP> tcp/1514; logging permit-hostdown` | 7.0(1) | Syslog over reliable (TCP) transport with TLS | `config log syslogd setting; set status enable; set server <SYSLOG_IP>; set mode reliable; set enc-algorithm high; end` | 7.0.0 or earlier | P28 | Same requirement |
| ASA-FW `CASA-FW-000130` | CAT II | `SRG-NET-000131-FW-000025` | FGT-FW `FNFG-FW-000065` | Disable unnecessary network services and functions | `no http server enable; no telnet <IP> <MASK> <INTERFACE>` | 7.0(1) | Disable interface services that are not needed | `config system interface; edit <INTERFACE>; set dhcp-relay-service disable; set pptp-client disable; set arpforward disable; set broadcast-forward disable; set l2forward disable; set icmp-send-redirect disable; set vlanforward disable; set stpforward disable; set lldp-transmission disable; next; end` | 7.0.0 or earlier | — | Same requirement |
| ASA-FW `CASA-FW-000150` | CAT II | `SRG-NET-000193-FW-000030` | FGT-FW `FNFG-FW-000075` | Limit the effects of packet flooding attacks | `threat-detection basic-threat` | 8.0(2) | IPv4 and IPv6 DoS policies with flood thresholds | `config firewall DoS-policy; edit <ID>; set interface <INTERFACE>; set srcaddr <SRC_ADDRESS>; set dstaddr <DST_ADDRESS>; set service <SERVICE>; config anomaly; edit <ANOMALY>; set status enable; set log enable; set action block; set threshold <THRESHOLD>; next; end; next; end` | 7.0.0 or earlier | — | Same requirement |
| ASA-FW `CASA-FW-000170` | CAT II | `SRG-NET-000205-FW-000040` | FGT-FW `FNFG-FW-000085` | Filter traffic into the enclave as the PPSM CAL and vulnerability assessments allow | `access-list <OUTSIDE_ACL> extended permit tcp any host <SERVER_IP> eq https; access-list <OUTSIDE_ACL> extended deny ip any any log; access-group <OUTSIDE_ACL> in interface <OUTSIDE>` | 7.0(1) | Firewall policies that allow only the registered traffic; the rest meets the implicit deny | `config firewall policy; edit <POLICY_ID>; set srcintf <IN_INTERFACE>; set dstintf <OUT_INTERFACE>; set srcaddr <SRC_ADDRESS>; set dstaddr <DST_ADDRESS>; set schedule <SCHEDULE>; set service <SERVICE>; set action accept; set logtraffic all; next; end` | 7.0.0 or earlier | — | Same requirement |
| ASA-FW `CASA-FW-000200` | CAT II | `SRG-NET-000333-FW-000014` | FGT-FW `FNFG-FW-000100` | Send traffic logs to a central audit server | `logging host <MGMT_INTERFACE> <SYSLOG_IP> tcp/1514; logging trap notifications` | 7.0(1) | Logging to FortiAnalyzer (or syslog) | `config log fortianalyzer setting; set status enable; set server <FAZ_IP>; set upload-option realtime; end` | 7.0.0 or earlier | P29 | Same requirement |
| ASA-FW `CASA-FW-000210` | CAT II | `SRG-NET-000335-FW-000017` | FGT-FW `FNFG-FW-000105` | Alert the administrator and ISSO when the central audit server is lost | `logging mail errors; logging recipient-address <ADMIN_EMAIL>; logging recipient-address <ISSO_EMAIL>; logging from-address <ASA_EMAIL>; smtp-server <SMTP_IP>` | 7.0(1) | Automation stitch that emails an alert on the log failure event | `config system automation-trigger; edit <TRIGGER>; set event-type event-log; set logid <LOG_ID>; next; end` `config system automation-action; edit <ACTION>; set action-type email; set email-to <ADDRESS>; set email-subject <SUBJECT>; next; end` | 7.0.0 or earlier | P30 | Same requirement |
| ASA-FW `CASA-FW-000220` | CAT I | `SRG-NET-000362-FW-000028` | FGT-FW `FNFG-FW-000110` | Detect and limit scanning and other common denial-of-service attacks | `threat-detection scanning-threat shun` | 8.0(2) | IPv4 and IPv6 DoS policies (port scan and sweep anomalies) | `config firewall DoS-policy; edit <ID>; set interface <INTERFACE>; set srcaddr <SRC_ADDRESS>; set dstaddr <DST_ADDRESS>; set service <SERVICE>; config anomaly; edit <ANOMALY>; set status enable; set log enable; set action block; set threshold <THRESHOLD>; next; end; next; end` | 7.0.0 or earlier | — | Same requirement |
| ASA-FW `CASA-FW-000230` | CAT II | `SRG-NET-000364-FW-000031` | FGT-FW `FNFG-FW-000115` | Filter inbound traffic on every external interface | `access-list <OUTSIDE_ACL> extended permit tcp any host <SERVER_IP> eq https; access-list <OUTSIDE_ACL> extended deny ip any any log; access-group <OUTSIDE_ACL> in interface <OUTSIDE>` | 7.0(1) | Firewall policies from each external interface; the rest meets the implicit deny | `config firewall policy; edit <POLICY_ID>; set srcintf <IN_INTERFACE>; set dstintf <OUT_INTERFACE>; set srcaddr <SRC_ADDRESS>; set dstaddr <DST_ADDRESS>; set schedule <SCHEDULE>; set service <SERVICE>; set action accept; set logtraffic all; next; end` | 7.0.0 or earlier | — | Same requirement |
| ASA-FW `CASA-FW-000240` | CAT II | `SRG-NET-000364-FW-000032` | FGT-FW `FNFG-FW-000120` | Filter outbound traffic on every internal interface | `access-list <INSIDE_ACL> extended permit tcp any any eq https; access-list <INSIDE_ACL> extended deny ip any any log; access-group <INSIDE_ACL> in interface <INSIDE>` | 7.0(1) | Firewall policies from each internal interface; the rest meets the implicit deny | `config firewall policy; edit <POLICY_ID>; set srcintf <IN_INTERFACE>; set dstintf <OUT_INTERFACE>; set srcaddr <SRC_ADDRESS>; set dstaddr <DST_ADDRESS>; set schedule <SCHEDULE>; set service <SERVICE>; set action accept; set logtraffic all; next; end` | 7.0.0 or earlier | — | Same requirement |
| ASA-FW `CASA-FW-000250` | CAT II | `SRG-NET-000364-FW-000035` | FGT-FW `FNFG-FW-000125` | Perimeter firewall: block all outbound management traffic | `access-list <INSIDE_ACL> extended deny udp any any eq snmp; access-list <INSIDE_ACL> extended deny udp any any eq snmptrap; access-list <INSIDE_ACL> extended deny udp any any eq ntp; access-list <INSIDE_ACL> extended deny udp any any eq syslog; access-list <INSIDE_ACL> extended deny tcp any any eq ssh; access-list <INSIDE_ACL> extended deny tcp any any eq tacacs; access-list <INSIDE_ACL> extended permit ip any any; access-group <INSIDE_ACL> in interface <INSIDE>` | 7.0(1) | Deny policy for management traffic leaving the enclave | `config firewall policy; edit <POLICY_ID>; set srcintf <MGMT_INTERFACE>; set dstintf <EGRESS_INTERFACE>; set srcaddr <MGMT_NETWORK>; set dstaddr <ALL_ADDRESS>; set schedule <SCHEDULE>; set service <ALL_SERVICE>; set action deny; set logtraffic all; next; end` | 7.0.0 or earlier | P42 | Same requirement |
| ASA-FW `CASA-FW-000260` | CAT II | `SRG-NET-000364-FW-000036` | FGT-FW `FNFG-FW-000130` | Send management traffic to the NOC only through an IPsec tunnel | `access-list <MGMT_TRAFFIC> extended permit udp host <ASA_MGMT_IP> <NOC_NET> <MASK> eq snmptrap; access-list <MGMT_TRAFFIC> extended permit udp host <ASA_MGMT_IP> <NOC_NET> <MASK> eq syslog; crypto map <MAP> 1 match address <MGMT_TRAFFIC>; crypto map <MAP> 1 set peer <NOC_PEER_IP>; crypto map <MAP> 1 set ikev2 ipsec-proposal <PROPOSAL>; crypto map <MAP> interface <OUTSIDE>` | 8.4(1) | Policies that allow only the authorized management hosts and services through the tunnel to the management network | `config firewall policy; edit <POLICY_ID>; set srcintf <VPN_INTERFACE>; set dstintf <MGMT_INTERFACE>; set srcaddr <MGMT_HOSTS>; set dstaddr <MGMT_ASSETS>; set schedule <SCHEDULE>; set service <MGMT_SERVICES>; set action accept; next; end` | 7.0.0 or earlier | P42, P43 | Same requirement |
| ASA-FW `CASA-FW-000270` | CAT II | `SRG-NET-000364-FW-000040` | FGT-FW `FNFG-FW-000135` | Inspect inbound and outbound traffic at the application layer | `service-policy global_policy global` | 7.0(1) | Session helpers for application-layer inspection | `config system session-helper; edit <ID>; set name <PROTOCOL_NAME>; set protocol <PROTOCOL_NUMBER>; set port <PORT>; next; end` | 7.0.0 or earlier | — | Same requirement |
| ASA-FW `CASA-FW-000280` | CAT II | `SRG-NET-000364-FW-000041` | — | Inspect IPv6 traffic for unknown or out-of-order extension headers | `policy-map type inspect ipv6 <IPV6_MAP>; parameters; verify-header type; verify-header order; match header hop-by-hop; drop log; match header routing-type eq 0; drop log; match header routing-type eq 1; drop log; match header routing-type range 3 255; drop log; policy-map global_policy; class inspection_default; inspect ipv6 <IPV6_MAP>` | 8.2(1) | IPv6 extension header filter: blocks Hop-by-Hop, Routing, and other chosen headers, but has no check for unknown headers or header order | `config firewall ipv6-eh-filter; set hop-opt enable; set routing enable; end` | Not in the Chapter 30 feature map (8.0.1 CLI Reference) | — | Partial |
| ASA-FW `CASA-FW-000290` | CAT II | `SRG-NET-000364-FW-000042` | FGT-FW `FNFG-FW-000145` | Drop outbound packets with illegitimate source addresses (egress filter or uRPF) | `ip verify reverse-path interface <INSIDE>` | 7.0(1) | Reverse path check of source addresses (asymmetric routing disabled) | `config system settings; set asymroute disable; set asymroute-icmp disable; set asymroute6 disable; set asymroute6-icmp disable; end` | 7.0.0 or earlier | — | Same requirement |
| ASA-FW `CASA-FW-000300` | CAT II | `SRG-NET-000392-FW-000042` | FGT-FW `FNFG-FW-000150` | Alert the ISSO and ISSM when denial-of-service incidents are detected | `threat-detection basic-threat; threat-detection scanning-threat; logging mail warnings; logging recipient-address <ISSO_EMAIL>; logging from-address <ASA_EMAIL>; smtp-server <SMTP_IP>` | 8.0(2) | DoS policy anomaly logging, with an automation stitch on anomaly logs that emails the ISSO and ISSM | `config firewall DoS-policy; edit <ID>; set interface <INTERFACE>; set srcaddr <SRC_ADDRESS>; set dstaddr <DST_ADDRESS>; set service <SERVICE>; config anomaly; edit <ANOMALY>; set status enable; set log enable; set action block; set threshold <THRESHOLD>; next; end; next; end` `config system automation-trigger; edit <TRIGGER>; set event-type anomaly-logs; next; end` | 7.0.0 or earlier | — | Same requirement |
| ASA-VPN `CASA-VN-000010` | CAT III | `SRG-NET-000077-VPN-000280` | — | Record what type of VPN event occurred | `logging class vpn trap notifications; logging class vpnc trap notifications; logging class vpnfo trap notifications` | 7.2(1) | VPN event logging | `config log eventfilter; set event enable; set vpn enable; end` | Not in the Chapter 30 feature map (8.0.1 CLI Reference) | — | Equivalent setting |
| ASA-VPN `CASA-VN-000020` | CAT III | `SRG-NET-000078-VPN-000290` | — | Record the date and time of VPN events | `logging timestamp` | 7.0(1) | VPN event logging; records carry the date and time from the system clock | `config log eventfilter; set event enable; set vpn enable; end` | Not in the Chapter 30 feature map (8.0.1 CLI Reference) | — | Equivalent setting |
| ASA-VPN `CASA-VN-000080` | CAT II | `SRG-NET-000336-VPN-001280` | — | Queue log records locally when the central server is unreachable | `logging permit-hostdown; logging queue 8192` | 7.0(1) | Local disk logging alongside the central server | `config log disk setting; set status enable; set max-log-file-size <MB>; set diskfull overwrite; end` | 7.0.0 or earlier | P12 | Equivalent setting |
| ASA-VPN `CASA-VN-000090` | CAT II | `SRG-NET-000335-VPN-001270` | — | Alert on log failure events | `logging host <MGMT_INTERFACE> <SYSLOG_IP> tcp/1514; logging trap critical` | 7.0(1) | Automation stitch that emails an alert on each log failure event | `config system automation-trigger; edit <TRIGGER>; set event-type event-log; set logid <LOG_ID>; next; end` `config system automation-action; edit <ACTION>; set action-type email; set email-to <ADDRESS>; set email-subject <SUBJECT>; next; end` | 7.0.0 or earlier | P30 | Equivalent setting |
| ASA-VPN `CASA-VN-000120` | CAT II | `SRG-NET-000164-VPN-000560` | — | Validate certificates against a DoD or DoD-approved trust anchor | — | — | PKI peer users that name the DoD CA certificate | `config user peer; edit <PEER_USER>; set ca <CA_CERT>; set subject <SUBJECT>; next; end` | 7.0.0 or earlier | P15, P19 | Same requirement |
| ASA-VPN `CASA-VN-000130` | CAT I | `SRG-NET-000345-VPN-002430` | — | Refuse revoked certificates | `crypto ca trustpoint <CA_TRUSTPOINT>; revocation-check crl` | 9.0(1) | Locally cached CRLs updated on an interval, with OCSP checking | `config vpn certificate crl; edit <CRL>; set http-url <CRL_URL>; set update-interval <SECONDS>; next; end` `config vpn certificate setting; set ocsp-status enable; set strict-ocsp-check enable; end` | Not in the Chapter 30 feature map (8.0.1 CLI Reference) | P19 | Equivalent setting |
| ASA-VPN `CASA-VN-000150` | CAT I | `SRG-NET-000512-VPN-002220` | — | Use IKE for all IPsec security associations | `crypto ikev2 policy 1; encryption aes-256; crypto ikev2 enable <OUTSIDE>; crypto ipsec ikev2 ipsec-proposal <PROPOSAL>` | 8.4(1) | IPsec phase 1 with IKE version 2 | `config vpn ipsec phase1-interface; edit <TUNNEL>; set ike-version 2; set proposal aes256-sha384; set dhgrp 20; set keylife 28800; set authmethod signature; set certificate <CERT>; set peer <PEER_USER>; next; end` | 7.0.0 or earlier | P15, P16, P19, P44 | Same requirement |
| ASA-VPN `CASA-VN-000160` | CAT II | `SRG-NET-000132-VPN-000460` | — | Use IKEv2 for all IPsec security associations | `crypto ikev2 policy 1; encryption aes-256; crypto ikev2 enable <OUTSIDE>; crypto ipsec ikev2 ipsec-proposal <PROPOSAL>` | 8.4(1) | IPsec phase 1 with IKE version 2 | `config vpn ipsec phase1-interface; edit <TUNNEL>; set ike-version 2; set proposal aes256-sha384; set dhgrp 20; set keylife 28800; set authmethod signature; set certificate <CERT>; set peer <PEER_USER>; next; end` | 7.0.0 or earlier | P15, P16, P19, P44 | Same requirement |
| ASA-VPN `CASA-VN-000170` | CAT II | `SRG-NET-000510-VPN-002180` | — | Use FIPS-validated cryptography for IKE phase 1 | `crypto ikev2 policy 1; encryption aes-256` | 8.4(1) | IPsec phase 1 proposal of AES-256 with SHA-384 (Chapter 30 maps this requirement to the SM3 and SM4 option, which must not be used) | `config vpn ipsec phase1-interface; edit <TUNNEL>; set ike-version 2; set proposal aes256-sha384; set dhgrp 20; next; end` | 7.0.0 or earlier | — | Same requirement |
| ASA-VPN `CASA-VN-000180` | CAT II | `SRG-NET-000371-VPN-001640` | — | Use Perfect Forward Secrecy in IKE phase 2 | `crypto map <MAP> 1 set pfs group20` | 7.0(1) or earlier (the Command History does not date group20) | IPsec phase 2 with PFS and DH group 20 | `config vpn ipsec phase2-interface; edit <PHASE2>; set phase1name <TUNNEL>; set proposal aes256-sha384; set pfs enable; set dhgrp 20; set replay enable; set keylifeseconds 28800; next; end` | 7.0.0 or earlier | P43 | Same requirement |
| ASA-VPN `CASA-VN-000190` | CAT II | `SRG-NET-000510-VPN-002160` | — | Generate hashes with a FIPS-validated module | `crypto ikev2 policy 1; integrity sha384; crypto ipsec ikev2 ipsec-proposal <PROPOSAL>; protocol esp integrity sha-384` | 9.0(1) (protocol esp integrity) | SHA-384 in the phase 1 and phase 2 proposals | `config vpn ipsec phase1-interface; edit <TUNNEL>; set proposal aes256-sha384; next; end` `config vpn ipsec phase2-interface; edit <PHASE2>; set proposal aes256-sha384; next; end` | 7.0.0 or earlier | P43 | Equivalent setting |
| ASA-VPN `CASA-VN-000200` | CAT II | `SRG-NET-000510-VPN-002170` | — | Encrypt IPsec traffic with a FIPS-validated module | `crypto ipsec ikev2 ipsec-proposal <PROPOSAL>; protocol esp encryption aes-256` | 8.4(1) | AES-256 in the phase 2 proposal | `config vpn ipsec phase2-interface; edit <PHASE2>; set phase1name <TUNNEL>; set proposal aes256-sha384; next; end` | 7.0.0 or earlier | P43 | Equivalent setting |
| ASA-VPN `CASA-VN-000210` | CAT I | `SRG-NET-000074-VPN-000250` | — | Use Diffie-Hellman group 16 or higher for IKE phase 1 | `crypto ikev2 policy 1; group 20` | 9.0(1) (ECDH groups) | IPsec phase 1 with DH group 20 | `config vpn ipsec phase1-interface; edit <TUNNEL>; set ike-version 2; set proposal aes256-sha384; set dhgrp 20; next; end` | 7.0.0 or earlier | — | Same requirement |
| ASA-VPN `CASA-VN-000230` | CAT II | `SRG-NET-000168-VPN-000600` | — | Use SHA-384 or stronger for IKE phase 1 | `crypto ikev2 policy 1; integrity sha384` | 8.4(2) (sha384 keyword) | SHA-384 in the phase 1 proposal | `config vpn ipsec phase1-interface; edit <TUNNEL>; set ike-version 2; set proposal aes256-sha384; next; end` | 7.0.0 or earlier | — | Equivalent setting |
| ASA-VPN `CASA-VN-000240` | CAT I | `SRG-NET-000230-VPN-000780` | — | Use SHA-2 at 384 bits or more for IKE phase 2 | `crypto ipsec ikev2 ipsec-proposal <PROPOSAL>; protocol esp integrity sha-384; crypto map <MAP> 10 set ikev2 ipsec-proposal <PROPOSAL>` | 9.0(1) (protocol esp integrity) | SHA-384 in the phase 2 proposal | `config vpn ipsec phase2-interface; edit <PHASE2>; set phase1name <TUNNEL>; set proposal aes256-sha384; next; end` | 7.0.0 or earlier | P43 | Same requirement |
| ASA-VPN `CASA-VN-000300` | CAT II | `SRG-NET-000019-VPN-000040` | — | Restrict which traffic the IPsec tunnel carries | `access-list <TUNNEL_ACL> extended permit ip <LOCAL_NET> <MASK> <REMOTE_NET> <MASK>; crypto map <MAP> 10 match address <TUNNEL_ACL>` | 7.0(1) | Phase 2 selectors for the protected networks, with firewall policies on the tunnel interface (Chapter 30 maps this requirement to the SSL VPN web portal) | `config vpn ipsec phase2-interface; edit <PHASE2>; set phase1name <TUNNEL>; set src-subnet <LOCAL_NET> <MASK>; set dst-subnet <REMOTE_NET> <MASK>; next; end` | 7.0.0 or earlier | P43 | Same requirement |
| ASA-VPN `CASA-VN-000310` | CAT II | `SRG-NET-000148-VPN-000540` | — | Identify and authenticate every peer before connecting | `tunnel-group <PEER_IP> type ipsec-l2l; tunnel-group <PEER_IP> ipsec-attributes; ikev2 remote-authentication pre-shared-key <KEY>; ikev2 local-authentication pre-shared-key <KEY>` | 8.4(1) | Phase 1 certificate authentication of a named peer | `config vpn ipsec phase1-interface; edit <TUNNEL>; set ike-version 2; set authmethod signature; set certificate <CERT>; set peer <PEER_USER>; next; end` | 7.0.0 or earlier | P15, P16, P19, P44 | Same requirement |
| ASA-VPN `CASA-VN-000340` | CAT I | `SRG-NET-000565-VPN-002400` | — | Use NSA-approved algorithms for classified traffic over an unclassified network | `crypto ikev2 policy 2; encryption aes-gcm-256; integrity null; group 20; prf sha384; crypto ipsec ikev2 ipsec-proposal <PROPOSAL>; protocol esp encryption aes-gcm-256; protocol esp integrity null; crypto map <MAP> 10 set ikev2 ipsec-proposal <PROPOSAL>` | 9.0(1) (AES-GCM) | AES-256-GCM with PRF SHA-384 and DH group 20 in phase 1, AES-256-GCM in phase 2 | `config vpn ipsec phase1-interface; edit <TUNNEL>; set ike-version 2; set proposal aes256gcm-prfsha384; set dhgrp 20; next; end` `config vpn ipsec phase2-interface; edit <PHASE2>; set phase1name <TUNNEL>; set proposal aes256gcm; set pfs enable; set dhgrp 20; next; end` | 7.0.0 or earlier | P43 | Equivalent setting |
| ASA-VPN `CASA-VN-000350` | CAT II | `SRG-NET-000337-VPN-001290` | — | Renegotiate the IPsec security association after eight hours or less | `crypto map <MAP> 10 set security-association lifetime seconds 28800` | 7.0(1) | Phase 2 key lifetime of 28,800 seconds | `config vpn ipsec phase2-interface; edit <PHASE2>; set phase1name <TUNNEL>; set keylifeseconds 28800; next; end` | 7.0.0 or earlier | P43 | Same requirement |
| ASA-VPN `CASA-VN-000360` | CAT II | `SRG-NET-000337-VPN-001300` | — | Renegotiate the IKE security association after 24 hours or less | `crypto ikev2 policy 1; lifetime seconds 86400` | 8.4(1) | Phase 1 key lifetime of 28,800 seconds, which meets the SRG's eight hours (the ASA rule allows 24) | `config vpn ipsec phase1-interface; edit <TUNNEL>; set keylife 28800; next; end` | 7.0.0 or earlier | — | Same requirement |
| ASA-VPN `CASA-VN-000390` | CAT II | `SRG-NET-000166-VPN-000580` | — | Remote access: authenticate users on a separate authentication server | `aaa-server <LDAP_GROUP> protocol ldap; aaa-server <LDAP_GROUP> (<INSIDE>) host <LDAP_IP>` | 7.2(1) or earlier | Dial-up IPsec VPN that authenticates users through a user group on a remote server | `config vpn ipsec phase1-interface; edit <TUNNEL>; set type dynamic; set mode-cfg enable; set authusrgrp <GROUP>; next; end` | 7.0.0 or earlier | P41 | Same requirement |
| ASA-VPN `CASA-VN-000400` | CAT II | `SRG-NET-000320-VPN-001120` | — | Remote access: use LDAP over SSL for authorization | `aaa-server <LDAP_GROUP> protocol ldap; aaa-server <LDAP_GROUP> (<INSIDE>) host <LDAP_IP>; ldap-over-ssl enable; tunnel-group <RA_GROUP> general-attributes; authorization-required; authorization-server-group <LDAP_GROUP>` | 7.2(1) or earlier | LDAP server over LDAPS for the VPN user group | `config user ldap; edit <LDAP_SERVER>; set server <SERVER_IP>; set secure ldaps; set ca-cert <CA_CERT>; next; end` | 7.0.0 or earlier | P15, P21 | Equivalent setting |
| ASA-VPN `CASA-VN-000410` | CAT II | `SRG-NET-000138-VPN-000490` | — | Remote access: identify and authenticate users before granting access | `tunnel-group <RA_GROUP> webvpn-attributes; authentication certificate` | 7.1(1) | Dial-up IPsec VPN that authenticates each user | `config vpn ipsec phase1-interface; edit <TUNNEL>; set type dynamic; set mode-cfg enable; set authusrgrp <GROUP>; next; end` | 7.0.0 or earlier | P41 | Same requirement |
| ASA-VPN `CASA-VN-000440` | CAT I | `SRG-NET-000140-VPN-000500` | — | Remote access: require certificate-based (multifactor) authentication | `tunnel-group <RA_GROUP> webvpn-attributes; authentication certificate` | 7.1(1) | Client certificates required for VPN logins | `config vpn ssl settings; set reqclientcert enable; end` | 7.0.0 or earlier | P15, P19, P20 | Same requirement |
| ASA-VPN `CASA-VN-000450` | CAT II | `SRG-NET-000166-VPN-000590` | — | Remote access: map the certificate's identity to the user account | `tunnel-group <RA_GROUP> general-attributes; authorization-required; authorization-server-group <LDAP_GROUP>; username-from-certificate use-entire-name` | 8.0(4) | PKI peer users matched on the certificate subject | `config user peer; edit <PEER_USER>; set ca <CA_CERT>; set subject <SUBJECT>; next; end` | 7.0.0 or earlier | P15, P19 | Same requirement |
| ASA-VPN `CASA-VN-000460` | CAT II | `SRG-NET-000041-VPN-000110` | — | Remote access: show the DoD Notice and Consent Banner before granting access | `group-policy <GROUP_POLICY> attributes; banner value <DOD_BANNER_TEXT>` | 7.0(1) | Banner that the dial-up client shows after it connects, like the ASA group-policy banner (a post-login banner), so neither shows it before access is granted | `config vpn ipsec phase1-interface; edit <TUNNEL>; set banner "<DOD_BANNER_TEXT>"; next; end` | Not in the Chapter 30 feature map (8.0.1 CLI Reference) | — | Partial |
| ASA-VPN `CASA-VN-000500` | CAT II | `SRG-NET-000079-VPN-000300` | — | Record the identity of the user or process in VPN logs | `logging class vpn trap notifications; logging class vpnc trap notifications; logging class vpnfo trap notifications` | 7.2(1) | VPN event logging, which records the user name | `config log eventfilter; set event enable; set vpn enable; end` | Not in the Chapter 30 feature map (8.0.1 CLI Reference) | — | Equivalent setting |
| ASA-VPN `CASA-VN-000510` | CAT II | `SRG-NET-000088-VPN-000310` | — | Record where VPN events occurred | `logging class vpn trap notifications; logging class vpnc trap notifications; logging class vpnfo trap notifications` | 7.2(1) | VPN event logging | `config log eventfilter; set event enable; set vpn enable; end` | Not in the Chapter 30 feature map (8.0.1 CLI Reference) | — | Equivalent setting |
| ASA-VPN `CASA-VN-000520` | CAT III | `SRG-NET-000089-VPN-000330` | — | Record the source of VPN events | `logging class vpn trap notifications; logging class vpnc trap notifications; logging class vpnfo trap notifications` | 7.2(1) | VPN event logging, which records the remote address | `config log eventfilter; set event enable; set vpn enable; end` | Not in the Chapter 30 feature map (8.0.1 CLI Reference) | — | Equivalent setting |
| ASA-VPN `CASA-VN-000530` | CAT II | `SRG-NET-000091-VPN-000350` | — | Record the outcome of VPN events | `logging class vpn trap notifications; logging class vpnc trap notifications; logging class vpnfo trap notifications` | 7.2(1) | VPN event logging | `config log eventfilter; set event enable; set vpn enable; end` | Not in the Chapter 30 feature map (8.0.1 CLI Reference) | — | Equivalent setting |
| ASA-VPN `CASA-VN-000550` | CAT I | `SRG-NET-000062-VPN-000200` | — | Remote access: use TLS 1.2 or later | `ssl server-version tlsv1.2 dtlsv1.2` | 9.10(1) (dtlsv1.2) | Minimum TLS 1.2 for the TLS VPN (from 7.6.3 the Agentless VPN; tunnel mode is replaced by IPsec) | `config vpn ssl settings; set ssl-min-proto-ver tls1-2; end` | 7.0.0 or earlier | — | Same requirement |
| ASA-VPN `CASA-VN-000560` | CAT II | `SRG-NET-000063-VPN-000210` | — | Remote access: protect TLS integrity with FIPS-validated algorithms | `ssl cipher tlsv1.2 fips` | 9.3(2) | High-strength algorithms only for the TLS VPN | `config vpn ssl settings; set algorithm high; end` | Not in the Chapter 30 feature map (8.0.1 CLI Reference) | — | Equivalent setting |
| ASA-VPN `CASA-VN-000610` | CAT II | `SRG-NET-000234-VPN-000810` | — | Generate session identifiers with a FIPS-validated DRBG | `fips enable` | 7.0(4) | FIPS-CC mode | `config system fips-cc; set status enable; end` | 7.0.0 or earlier | P14 | Equivalent setting |
| ASA-VPN `CASA-VN-000630` | CAT II | `SRG-NET-000063-VPN-000220` | — | Remote access: use SHA-384 or stronger for IPsec integrity | `crypto ikev2 policy 1; integrity sha384; crypto ipsec ikev2 ipsec-proposal <PROPOSAL>; protocol esp integrity sha-384` | 9.0(1) (protocol esp integrity) | SHA-384 in the phase 1 and phase 2 proposals | `config vpn ipsec phase1-interface; edit <TUNNEL>; set ike-version 2; set proposal aes256-sha384; next; end` | 7.0.0 or earlier | — | Same requirement |
| ASA-VPN `CASA-VN-000640` | CAT I | `SRG-NET-000317-VPN-001090` | — | Remote access: use AES-256 for IKE phase 1 | `crypto ikev2 policy 1; encryption aes-256` | 8.4(1) | AES-256 in the phase 1 proposal | `config vpn ipsec phase1-interface; edit <TUNNEL>; set ike-version 2; set proposal aes256-sha384; next; end` | 7.0.0 or earlier | — | Same requirement |
| ASA-VPN `CASA-VN-000650` | CAT I | `SRG-NET-000525-VPN-002330` | — | Remote access: use AES-256 for the IPsec security association | `crypto ipsec ikev2 ipsec-proposal <PROPOSAL>; protocol esp encryption aes-256` | 8.4(1) | AES-256 in the phase 2 proposal | `config vpn ipsec phase2-interface; edit <PHASE2>; set phase1name <TUNNEL>; set proposal aes256-sha384; next; end` | 7.0.0 or earlier | P43 | Same requirement |
| ASA-VPN `CASA-VN-000660` | CAT II | `SRG-NET-000341-VPN-001350` | — | Remote access: accept the Common Access Card | `tunnel-group <RA_GROUP> webvpn-attributes; authentication certificate` | 7.1(1) | PKI peer users that accept certificates issued by the DoD CA | `config user peer; edit <PEER_USER>; set ca <DOD_CA_CERT>; set subject <SUBJECT>; next; end` | 7.0.0 or earlier | P15, P19 | Equivalent setting |
| ASA-VPN `CASA-VN-000700` | CAT II | `SRG-NET-000369-VPN-001620` | — | Remote access: disable split tunneling | `group-policy <GROUP_POLICY> attributes; split-tunnel-policy tunnelall` | 7.0(1) | Dial-up IPsec VPN with no split-include addresses, so that all client traffic uses the tunnel | `config vpn ipsec phase1-interface; edit <TUNNEL>; set type dynamic; set mode-cfg enable; set authusrgrp <GROUP>; next; end` | 7.0.0 or earlier | P41 | Same requirement |
| ASA-VPN `CASA-VN-000720` | CAT II | `SRG-NET-000492-VPN-001980` | — | Log successful and unsuccessful VPN connection attempts | `logging class vpn trap notifications; logging class auth trap notifications` | 7.2(1) | VPN event logging (Chapter 30 maps this requirement to the VPN monitor and tunnel-down logging features) | `config log eventfilter; set event enable; set vpn enable; end` | Not in the Chapter 30 feature map (8.0.1 CLI Reference) | — | Same requirement |
| ASA-VPN `CASA-VN-000730` | CAT II | `SRG-NET-000580-VPN-002410` | — | Validate TLS certificates by RFC 5280 path validation | `crypto ca trustpoint <CA_TRUSTPOINT>; validation-usage ssl-client; validation-usage ipsec-client` | 9.0(1) | Certificate chain and CA checks for all certificate validation | `config vpn certificate setting; set check-ca-cert enable; set check-ca-chain enable; end` | Not in the Chapter 30 feature map (8.0.1 CLI Reference) | P15 | Equivalent setting |
| ASA-VPN `CASA-VN-000760` | CAT I | `SRG-NET-000565-VPN-002390` | — | Remote access to a classified network: use NSA-approved (CSfC) algorithms | `crypto ikev2 policy 2; encryption aes-gcm-256; integrity null; group 20; prf sha384; crypto ipsec ikev2 ipsec-proposal <PROPOSAL>; protocol esp encryption aes-gcm-256; protocol esp integrity null; crypto map <MAP> 10 set ikev2 ipsec-proposal <PROPOSAL>` | 9.0(1) (AES-GCM) | AES-256-GCM with PRF SHA-384 and DH group 20 in phase 1, AES-256-GCM in phase 2; CSfC also needs a listed product and layered design | `config vpn ipsec phase1-interface; edit <TUNNEL>; set ike-version 2; set proposal aes256gcm-prfsha384; set dhgrp 20; next; end` `config vpn ipsec phase2-interface; edit <PHASE2>; set phase1name <TUNNEL>; set proposal aes256gcm; set pfs enable; set dhgrp 20; next; end` | 7.0.0 or earlier | P43 | Equivalent setting |
| ASA-IPS `CASA-IP-000040` | CAT II | `SRG-NET-000074-IDPS-00059` | — | IPS events: record what type of event occurred | ASDM: Configuration > ASA FirePOWER Configuration > Policies > Access Control Policy (each rule's Logging tab: "Log at End of Connection", to syslog); ASDM: Configuration > ASA FirePOWER Configuration > Policies > Intrusion Policy ("Advanced Settings", "Syslog Alerting under External Responses", "Logging Hosts") | ASA FirePOWER 7.0 guide (no command history) | IPS sensor logging, applied to the firewall policies | `config ips sensor; edit <SENSOR>; config entries; edit 1; set severity <SEVERITIES>; set status enable; set action block; set log enable; set log-packet enable; next; end; next; end` | 7.0.0 or earlier | P3 | Equivalent setting |
| ASA-IPS `CASA-IP-000050` | CAT II | `SRG-NET-000075-IDPS-00060` | — | IPS events: record the date and time | ASDM: Configuration > ASA FirePOWER Configuration > Policies > Access Control Policy (each rule's Logging tab: "Log at End of Connection", to syslog); ASDM: Configuration > ASA FirePOWER Configuration > Policies > Intrusion Policy ("Advanced Settings", "Syslog Alerting under External Responses", "Logging Hosts") | ASA FirePOWER 7.0 guide (no command history) | IPS sensor logging; records carry the date and time | `config ips sensor; edit <SENSOR>; config entries; edit 1; set status enable; set log enable; next; end; next; end` | 7.0.0 or earlier | P3 | Equivalent setting |
| ASA-IPS `CASA-IP-000060` | CAT II | `SRG-NET-000076-IDPS-00061` | — | IPS events: record where the event was detected | ASDM: Configuration > ASA FirePOWER Configuration > Policies > Access Control Policy (each rule's Logging tab: "Log at End of Connection", to syslog); ASDM: Configuration > ASA FirePOWER Configuration > Policies > Intrusion Policy ("Advanced Settings", "Syslog Alerting under External Responses", "Logging Hosts") | ASA FirePOWER 7.0 guide (no command history) | IPS sensor logging; records carry the interfaces, destination, and policy | `config ips sensor; edit <SENSOR>; config entries; edit 1; set status enable; set log enable; next; end; next; end` | 7.0.0 or earlier | P3 | Equivalent setting |
| ASA-IPS `CASA-IP-000070` | CAT II | `SRG-NET-000077-IDPS-00062` | — | IPS events: record the source of the event | ASDM: Configuration > ASA FirePOWER Configuration > Policies > Access Control Policy (each rule's Logging tab: "Log at End of Connection", to syslog); ASDM: Configuration > ASA FirePOWER Configuration > Policies > Intrusion Policy ("Advanced Settings", "Syslog Alerting under External Responses", "Logging Hosts") | ASA FirePOWER 7.0 guide (no command history) | IPS sensor logging; records carry the source address | `config ips sensor; edit <SENSOR>; config entries; edit 1; set status enable; set log enable; next; end; next; end` | 7.0.0 or earlier | P3 | Equivalent setting |
| ASA-IPS `CASA-IP-000080` | CAT II | `SRG-NET-000078-IDPS-00063` | — | IPS events: record the outcome, including the associated traffic | ASDM: Configuration > ASA FirePOWER Configuration > Policies > Access Control Policy (each rule's Logging tab: "Log at End of Connection", to syslog); ASDM: Configuration > ASA FirePOWER Configuration > Policies > Intrusion Policy ("Advanced Settings", "Syslog Alerting under External Responses", "Logging Hosts") | ASA FirePOWER 7.0 guide (no command history) | IPS sensor logging with packet logging, which keeps the packets of each event | `config ips sensor; edit <SENSOR>; config entries; edit 1; set status enable; set log enable; set log-packet enable; next; end; next; end` | 7.0.0 or earlier | P3 | Equivalent setting |
| ASA-IPS `CASA-IP-000090` | CAT II | `SRG-NET-000113-IDPS-00013` | — | Log detection events from policies, signatures, and anomaly analysis | ASDM: Configuration > ASA FirePOWER Configuration > Policies > Access Control Policy ("Network Analysis and Intrusion Policies": "Balanced Security and Connectivity"; each rule's Logging tab: "Log at End of Connection") | ASA FirePOWER 7.0 guide (no command history) | IPS sensors with logging, applied to the firewall policies | `config ips sensor; edit <SENSOR>; config entries; edit 1; set severity <SEVERITIES>; set status enable; set action block; set log enable; set log-packet enable; next; end; next; end` `config firewall policy; edit <POLICY_ID>; set utm-status enable; set ips-sensor <SENSOR>; next; end` | 7.0.0 or earlier | P3 | Same requirement |
| ASA-IPS `CASA-IP-000110` | CAT II | `SRG-NET-000334-IDPS-00191` | — | Off-load IPS log records to a central log server | ASDM: ASA FirePOWER Configuration > Policies > Actions Alerts ("Create Syslog Alert") | ASA FirePOWER 7.0 guide (no command history) | Logging to FortiAnalyzer (or syslog) | `config log fortianalyzer setting; set status enable; set server <FAZ_IP>; set upload-option realtime; end` | 7.0.0 or earlier | P29 | Equivalent setting |
| ASA-IPS `CASA-IP-000120` | CAT II | `SRG-NET-000113-IDPS-00189` | — | Send IPS logs with a configurable facility and severity | ASDM: ASA FirePOWER Configuration > Policies > Actions Alerts ("Create Syslog Alert"; Facility and Severity) | ASA FirePOWER 7.0 guide (no command history) | Syslog facility and the lowest severity sent | `config log syslogd setting; set status enable; set server <SYSLOG_IP>; set facility local7; end` `config log syslogd filter; set severity information; end` | Not in the Chapter 30 feature map (8.0.1 CLI Reference) | P28 | Equivalent setting |
| ASA-IPS `CASA-IP-000130` | CAT II | `SRG-NET-000089-IDPS-00010` | — | Queue IPS log records locally when the central server is unreachable | `logging host <MGMT_INTERFACE> <SYSLOG_IP> tcp/1514; logging permit-hostdown` | 7.0(1) | Local disk logging alongside the central server | `config log disk setting; set status enable; set max-log-file-size <MB>; set diskfull overwrite; end` | 7.0.0 or earlier | P12 | Equivalent setting |
| ASA-IPS `CASA-IP-000180` | CAT II | `SRG-NET-000192-IDPS-00140` | — | Block outbound denial-of-service traffic with an intrusion policy | `access-list <SFR_REDIRECT> extended permit ip any any; class-map <SFR_CLASS>; match access-list <SFR_REDIRECT>; policy-map global_policy; class <SFR_CLASS>; sfr fail-open` ASDM: Configuration > ASA FirePOWER Configuration > Policies > Access Control Policy (rule action "Interactive Block"; "Inspection tab": intrusion policy) | 9.2(1); ASA FirePOWER 7.0 guide (no command history) | IPS sensor that blocks, applied to the outbound firewall policies | `config firewall policy; edit <POLICY_ID>; set utm-status enable; set ips-sensor <SENSOR>; next; end` | 7.0.0 or earlier | P3 | Equivalent setting |
| ASA-IPS `CASA-IP-000190` | CAT II | `SRG-NET-000228-IDPS-00196` | — | Detect and block malware with Advanced Malware Protection | ASDM: Configuration > ASA FirePOWER Configuration > Policies > Files (file rule action "Block Malware"); ASDM: Configuration > ASA FirePOWER Configuration > Policies > Access Control Policy ("Inspection tab": file policy) | ASA FirePOWER 7.0 guide (no command history) | Antivirus profile that blocks infected files, applied to the firewall policies | `config antivirus profile; edit <PROFILE>; config http; set av-scan block; end; next; end` | 7.0.0 or earlier | P4, P46 | Equivalent setting |
| ASA-IPS `CASA-IP-000200` | CAT II | `SRG-NET-000229-IDPS-00163` | — | Block prohibited mobile code at the enclave boundary | ASDM: Configuration > ASA FirePOWER Configuration > Policies > Files (file rule action "Block Malware"); ASDM: Configuration > ASA FirePOWER Configuration > Policies > Access Control Policy ("Inspection tab": file policy) | ASA FirePOWER 7.0 guide (no command history) | Antivirus profile that blocks infected files, applied to the firewall policies | `config antivirus profile; edit <PROFILE>; config http; set av-scan block; end; next; end` | 7.0.0 or earlier | P4, P46 | Equivalent setting |
| ASA-IPS `CASA-IP-000240` | CAT II | `SRG-NET-000246-IDPS-00205` | — | Install signature and rule updates | ASDM: Configuration > ASA FirePOWER Configuration > Updates ("Enable Recurring Rule Update Imports"; "Import Frequency") | ASA FirePOWER 7.0 guide (no command history) | Automatic FortiGuard IPS and antivirus updates | `config system autoupdate schedule; set status enable; set frequency automatic; end` | 7.0.0 or earlier | P1, P2, P3, P4 | Same requirement |
| ASA-IPS `CASA-IP-000260` | CAT II | `SRG-NET-000249-IDPS-00176` | — | Block malicious code | ASDM: Configuration > ASA FirePOWER Configuration > Policies > Files (file rule action "Block Malware"); ASDM: Configuration > ASA FirePOWER Configuration > Policies > Access Control Policy ("Inspection tab": file policy) | ASA FirePOWER 7.0 guide (no command history) | Antivirus profile that blocks infected files | `config antivirus profile; edit <PROFILE>; config http; set av-scan block; end; next; end` | 7.0.0 or earlier | P4, P46 | Same requirement |
| ASA-IPS `CASA-IP-000270` | CAT II | `SRG-NET-000249-IDPS-00221` | — | Block traffic from addresses with a bad reputation | ASDM: Configuration > ASA FirePOWER Configuration > Object Management ("Security Intelligence": "Intelligence Feed", "Update Frequency") | ASA FirePOWER 7.0 guide (no command history) | IPS sensor that blocks connections to botnet command-and-control addresses from the FortiGuard feed | `config ips sensor; edit <SENSOR>; set scan-botnet-connections block; next; end` | Not in the Chapter 30 feature map (8.0.1 CLI Reference) | P3 | Equivalent setting |
| ASA-IPS `CASA-IP-000280` | CAT II | `SRG-NET-000249-IDPS-00222` | — | Alert when malicious code is detected | ASDM: ASA FirePOWER Configuration > Policies > Actions Alerts ("Create Syslog Alert" or "Create SNMP Alert" to a monitored SIEM; the 7.0 guide has no email alert response) | ASA FirePOWER 7.0 guide (no command history) | Automation stitch on antivirus logs that emails the administrator | `config system automation-trigger; edit <TRIGGER>; set event-type virus-logs; next; end` `config system automation-action; edit <ACTION>; set action-type email; set email-to <ADDRESS>; next; end` | Not in the Chapter 30 feature map (8.0.1 CLI Reference) | P4, P30 | Equivalent setting |
| ASA-IPS `CASA-IP-000290` | CAT II | `SRG-NET-000251-IDPS-00178` | — | Install signature and rule updates automatically | ASDM: Configuration > ASA FirePOWER Configuration > Updates ("Enable Recurring Rule Update Imports"; "Import Frequency") | ASA FirePOWER 7.0 guide (no command history) | Automatic FortiGuard IPS and antivirus updates | `config system autoupdate schedule; set status enable; set frequency automatic; end` | 7.0.0 or earlier | P1, P2, P3, P4 | Equivalent setting |
| ASA-IPS `CASA-IP-000500` | CAT II | `SRG-NET-000390-IDPS-00212` | — | Monitor and block unauthorized inbound activity | `access-list <SFR_REDIRECT> extended permit ip any any; class-map <SFR_CLASS>; match access-list <SFR_REDIRECT>; policy-map global_policy; class <SFR_CLASS>; sfr fail-open` ASDM: Configuration > ASA FirePOWER Configuration > Policies > Access Control Policy (rule action "Interactive Block"; "Inspection tab": intrusion policy) | 9.2(1); ASA FirePOWER 7.0 guide (no command history) | IPS sensors applied to the inbound firewall policies | `config ips sensor; edit <SENSOR>; config entries; edit 1; set severity <SEVERITIES>; set status enable; set action block; set log enable; set log-packet enable; next; end; next; end` `config firewall policy; edit <POLICY_ID>; set utm-status enable; set ips-sensor <SENSOR>; next; end` | 7.0.0 or earlier | P3 | Same requirement |
| ASA-IPS `CASA-IP-000510` | CAT II | `SRG-NET-000391-IDPS-00213` | — | Monitor and block unauthorized outbound activity | `access-list <SFR_REDIRECT> extended permit ip any any; class-map <SFR_CLASS>; match access-list <SFR_REDIRECT>; policy-map global_policy; class <SFR_CLASS>; sfr fail-open` ASDM: Configuration > ASA FirePOWER Configuration > Policies > Access Control Policy (rule action "Interactive Block"; "Inspection tab": intrusion policy) | 9.2(1); ASA FirePOWER 7.0 guide (no command history) | IPS sensors applied to the outbound firewall policies | `config ips sensor; edit <SENSOR>; config entries; edit 1; set severity <SEVERITIES>; set status enable; set action block; set log enable; set log-packet enable; next; end; next; end` `config firewall policy; edit <POLICY_ID>; set utm-status enable; set ips-sensor <SENSOR>; next; end` | 7.0.0 or earlier | P3 | Same requirement |
| ASA-IPS `CASA-IP-000520` | CAT II | `SRG-NET-000392-IDPS-00214` | — | Alert the ISSM and ISSO on intrusion events | ASDM: ASA FirePOWER Configuration > Policies > Actions Alerts ("Create Syslog Alert" or "Create SNMP Alert" to a monitored SIEM; the 7.0 guide has no email alert response) | ASA FirePOWER 7.0 guide (no command history) | Automation stitch on IPS logs that emails the ISSM and ISSO | `config system automation-trigger; edit <TRIGGER>; set event-type ips-logs; next; end` `config system automation-action; edit <ACTION>; set action-type email; set email-to <ADDRESS>; next; end` | Not in the Chapter 30 feature map (8.0.1 CLI Reference) | P3, P30 | Equivalent setting |
| ASA-IPS `CASA-IP-000530` | CAT II | `SRG-NET-000392-IDPS-00215` | — | Alert the ISSM and ISSO on threats from authoritative sources | ASDM: ASA FirePOWER Configuration > Policies > Actions Alerts ("Create Syslog Alert" or "Create SNMP Alert" to a monitored SIEM; the 7.0 guide has no email alert response) | ASA FirePOWER 7.0 guide (no command history) | Automation stitch on IPS logs that emails the ISSM and ISSO | `config system automation-trigger; edit <TRIGGER>; set event-type ips-logs; next; end` `config system automation-action; edit <ACTION>; set action-type email; set email-to <ADDRESS>; next; end` | Not in the Chapter 30 feature map (8.0.1 CLI Reference) | P3, P30 | Equivalent setting |
| ASA-IPS `CASA-IP-000560` | CAT II | `SRG-NET-000392-IDPS-00218` | — | Alert the ISSM and ISSO on denial-of-service incidents | ASDM: ASA FirePOWER Configuration > Policies > Actions Alerts ("Create Syslog Alert" or "Create SNMP Alert" to a monitored SIEM; the 7.0 guide has no email alert response) | ASA FirePOWER 7.0 guide (no command history) | Automation stitch on anomaly (DoS policy) logs that emails the ISSM and ISSO | `config system automation-trigger; edit <TRIGGER>; set event-type anomaly-logs; next; end` `config system automation-action; edit <ACTION>; set action-type email; set email-to <ADDRESS>; next; end` | Not in the Chapter 30 feature map (8.0.1 CLI Reference) | P30 | Equivalent setting |
| ASA-IPS `CASA-IP-000570` | CAT II | `SRG-NET-000392-IDPS-00219` | — | Alert the ISSM and ISSO on active malware propagation | ASDM: ASA FirePOWER Configuration > Policies > Actions Alerts ("Create Syslog Alert" or "Create SNMP Alert" to a monitored SIEM; the 7.0 guide has no email alert response) | ASA FirePOWER 7.0 guide (no command history) | Automation stitch on antivirus logs that emails the ISSM and ISSO | `config system automation-trigger; edit <TRIGGER>; set event-type virus-logs; next; end` `config system automation-action; edit <ACTION>; set action-type email; set email-to <ADDRESS>; next; end` | Not in the Chapter 30 feature map (8.0.1 CLI Reference) | P4, P30 | Equivalent setting |

### FortiGate requirements with no Cisco ASA rule

The 88 requirements below are mapped to FortiGate features in Chapter
30 but are cited by no Cisco ASA STIG rule, so an ASA rule checklist misses
them: 22 FortiGate NDM STIG rules, 10 FortiGate Firewall
STIG rules, 9 IDPS, 9 VPN, 22 ALG, and 16
Router SRG requirements. They include the administrator lockout
(`FGFW-ND-000045`), log protection, FIPS-CC mode, and the default
administrator password among the STIG rules, and the web filtering,
application control, SSL inspection, proxy, and routing requirements that the
ASA STIGs do not address. Add them to the FortiGate checklist. The
requirement text is the FortiGate rule title or the SRG title; the setting
column lists the Chapter 30 features mapped to the requirement, the
version column gives the release of the feature whose command is shown,
and the prerequisite IDs are those of the Chapter 30 row whose command is
shown (see *FortiGate prerequisites*).

[Download the unmatched requirements as CSV](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/data/volume-172-disa-srgs-and-stigs/34-cisco-asa-and-fortigate-stig-crosswalk-unmatched.csv) (88 rows).

| Source | FortiGate STIG rule | SRG ID | Requirement | FortiGate setting | FortiOS command | FortiOS version | FortiGate prerequisites |
| --- | --- | --- | --- | --- | --- | --- | --- |
| FGT-NDM | `FGFW-ND-000045` | `SRG-APP-000065-NDM-000214` | The FortiGate device must enforce the limit of three consecutive invalid logon attempts, after which time it must lock out the user account from accessing the device for 15 minutes. | Administrator lockout after failed logins | `config system global; set admin-lockout-threshold 3; set admin-lockout-duration 900; end` | 7.0.0 or earlier | — |
| FGT-NDM | `FGFW-ND-000055` | `SRG-APP-000069-NDM-000216` | The FortiGate device must retain the Standard Mandatory DoW Notice and Consent Banner on the screen until the administrator acknowledges the usage conditions and takes explicit actions to log on for further access. | Pre-login disclaimer banner (Standard Mandatory DoD Notice and Consent Banner) | `config system global; set pre-login-banner enable; end` `config system replacemsg admin; edit pre_admin-disclaimer-text; set buffer "<DOD_BANNER_TEXT>"; next; end` | 7.0.0 or earlier | — |
| FGT-NDM | `FGFW-ND-000095` | `SRG-APP-000100-NDM-000230` | The FortiGate device must generate audit records containing information that establishes the identity of any individual or process associated with the event. | User identity in logs (no anonymization); Generate unique user name for anonymized logs; Add dstuser field to UTM logs | `config log setting; set user-anonymize disable; end` | 7.0.0 or earlier | — |
| FGT-NDM | `FGFW-ND-000110` | `SRG-APP-000515-NDM-000325` | The FortiGate device must off-load audit records on to a different system or media than the system being audited. | Logging to FortiAnalyzer; Logging to syslog servers over reliable TLS; Simplify Fabric approval workflow for FortiAnalyzer; and 3 more | `config log fortianalyzer setting; set status enable; set server <FAZ_IP>; set upload-option realtime; end` | 7.0.0 or earlier | P29 |
| FGT-NDM | `FGFW-ND-000125` | `SRG-APP-000374-NDM-000299` | The FortiGate device must record time stamps for audit records that can be mapped to Coordinated Universal Time (UTC) or Greenwich Mean Time (GMT). | Time zone; Streamline timezone updates with a downloadable database | `config system global; set timezone <TIMEZONE>; end` | 7.0.0 or earlier | — |
| FGT-NDM | `FGFW-ND-000130` | `SRG-APP-000120-NDM-000237` | The FortiGate device must protect audit information from unauthorized deletion. | Administrator profiles: Log and Report access permission | `config system accprofile; edit <PROFILE>; set loggrp none; next; end` | 7.0.0 or earlier | — |
| FGT-NDM | `FGFW-ND-000135` | `SRG-APP-000121-NDM-000238` | The FortiGate device must protect audit tools from unauthorized access. | Administrator profiles: Log and Report access permission | `config system accprofile; edit <PROFILE>; set loggrp none; next; end` | 7.0.0 or earlier | — |
| FGT-NDM | `FGFW-ND-000140` | `SRG-APP-000122-NDM-000239` | The FortiGate device must protect audit tools from unauthorized modification. | Administrator profiles: Log and Report access permission | `config system accprofile; edit <PROFILE>; set loggrp none; next; end` | 7.0.0 or earlier | — |
| FGT-NDM | `FGFW-ND-000145` | `SRG-APP-000378-NDM-000302` | The FortiGate device must prohibit installation of software without explicit privileged status. | Administrator profiles: System access permission | `config system accprofile; edit <PROFILE>; set sysgrp read; next; end` `config system admin; edit <ADMIN>; set accprofile <PROFILE>; next; end` | 7.0.0 or earlier | — |
| FGT-NDM | `FGFW-ND-000150` | `SRG-APP-000380-NDM-000304` | The FortiGate device must enforce access restrictions associated with changes to device configuration. | Administrator profiles: System access permission; Add Policy change summary and Policy expiration to Workflow Management | `config system accprofile; edit <PROFILE>; set sysgrp read; next; end` `config system admin; edit <ADMIN>; set accprofile <PROFILE>; next; end` | 7.0.0 or earlier | — |
| FGT-NDM | `FGFW-ND-000155` | `SRG-APP-000133-NDM-000244` | The FortiGate device must limit privileges to change the software resident within software libraries. | Administrator profiles: System access permission | `config system accprofile; edit <PROFILE>; set sysgrp read; next; end` `config system admin; edit <ADMIN>; set accprofile <PROFILE>; next; end` | 7.0.0 or earlier | — |
| FGT-NDM | `FGFW-ND-000160` | `SRG-APP-000516-NDM-000335` | The FortiGate device must enforce access restrictions associated with changes to the system components. | Trusted hosts for each administrator; Administrator profiles: System access permission | `config system admin; edit <ADMIN>; set trusthost1 <IP> <MASK>; next; end` | 7.0.0 or earlier | P42 |
| FGT-NDM | `FGFW-ND-000175` | `SRG-APP-000516-NDM-000334` | The FortiGate device must generate log records for a locally developed list of auditable events. | Event and log settings for the locally defined list of auditable events | `config log setting; set fwpolicy-implicit-log enable; set local-in-allow enable; set local-in-deny-unicast enable; end` `config log eventfilter; set event enable; set system enable; set endpoint enable; set user enable; end` | 7.0.0 or earlier | — |
| FGT-NDM | `FGFW-ND-000185` | `SRG-APP-000516-NDM-000341` | The FortiGate device must support organizational requirements to conduct backups of information system documentation, including security-related documentation, when changes occur or weekly, whichever is sooner. | Configuration revision backup on administrator logout; Central management by FortiManager (configuration backups and revision history); SFTP configuration backup; and 1 more | `config system global; set revision-backup-on-logout enable; end` | 7.0.0 or earlier | — |
| FGT-NDM | `FGFW-ND-000190` | `SRG-APP-000408-NDM-000314` | FortiGate devices performing maintenance functions must restrict use of these functions to authorized personnel only. | Trusted hosts for each administrator; Administrator profiles: System access permission; REST API administrators | `config system admin; edit <ADMIN>; set trusthost1 <IP> <MASK>; next; end` | 7.0.0 or earlier | P42 |
| FGT-NDM | `FGFW-ND-000245` | `SRG-APP-000172-NDM-000259` | The FortiGate device must use LDAPS for the LDAP connection. | LDAP servers over LDAPS; Configuring client certificate authentication on the LDAP server; Enable secure LDAP connection by default in the GUI | `config user ldap; edit <LDAP_SERVER>; set server <SERVER_IP>; set cnid <CN>; set dn <BASE_DN>; set type regular; set username <BIND_DN>; set password <BIND_PASSWORD>; set secure ldaps; set ca-cert <CA_CERT>; next; end` | 7.0.0 or earlier | P15, P21 |
| FGT-NDM | `FGFW-ND-000250` | `SRG-APP-000080-NDM-000345` | The FortiGate device must not have any default manufacturer passwords when deployed. | Default admin account password; Remove maintainer account | `config system admin; edit admin; set password <PASSWORD>; next; end` | 7.0.0 or earlier | — |
| FGT-NDM | `FGFW-ND-000255` | `SRG-APP-000179-NDM-000265` | The FortiGate device must use FIPS 140-2 approved algorithms for authentication to a cryptographic module. | FIPS-CC mode; OpenSSL FIPS provider installed globally at startup; FIPS cipher mode for OCI and GCP FortiGate VMs; and 1 more | `config system fips-cc; set status enable; end` | 7.0.0 or earlier | P14 |
| FGT-NDM | `FGFW-ND-000270` | `SRG-APP-000186-NDM-000266` | The FortiGate device must terminate idle sessions after 10 minutes of inactivity. | Administrator idle timeout | `config system global; set admintimeout 10; end` | 7.0.0 or earlier | — |
| FGT-NDM | `FGFW-ND-000280` | `SRG-APP-000224-NDM-000270` | The FortiGate device must generate unique session identifiers using a FIPS 140-2-approved random number generator. | FIPS-CC mode; Add built-in entropy source | `config system fips-cc; set status enable; end` | 7.0.0 or earlier | P14 |
| FGT-NDM | `FGFW-ND-000285` | `SRG-APP-000231-NDM-000271` | The FortiGate device must only allow authorized administrators to view or change the device configuration, system files, and other files stored either in the device or on removable media (such as a flash drive). | Administrator profiles: System access permission; CLI system permissions | `config system accprofile; edit <PROFILE>; set sysgrp read; next; end` `config system admin; edit <ADMIN>; set accprofile <PROFILE>; next; end` | 7.0.0 or earlier | — |
| FGT-NDM | `FGFW-ND-000305` | `SRG-APP-000131-NDM-000243` | The FortiGate device must only install patches or updates that are validated by the vendor via digital signature or hash. | Firmware and update packages validated by signature or checksum; Warnings for unsigned firmware; Enhance BIOS-level signature and file integrity checking; and 7 more | — | — | — |
| FGT-FW | `FNFG-FW-000030` | `SRG-NET-000076-FW-000011` | The FortiGate firewall must generate traffic log entries containing information to establish the network location where the events occurred. | Traffic logging in firewall policies; Policy and address UUIDs in traffic logs | `config log eventfilter; set event enable; set system enable; set endpoint enable; set user enable; set security-rating enable; end` `config firewall policy; edit <POLICY_ID>; set logtraffic all; next; end` | 7.0.0 or earlier | — |
| FGT-FW | `FNFG-FW-000035` | `SRG-NET-000077-FW-000012` | The FortiGate firewall must generate traffic log entries containing information to establish the source of the events, such as the source IP address at a minimum. | Traffic logging in firewall policies; Policy and address UUIDs in traffic logs | `config log eventfilter; set event enable; set system enable; set endpoint enable; set user enable; set security-rating enable; end` `config firewall policy; edit <POLICY_ID>; set logtraffic all; next; end` | 7.0.0 or earlier | — |
| FGT-FW | `FNFG-FW-000040` | `SRG-NET-000078-FW-000013` | The FortiGate firewall must generate traffic log entries containing information to establish the outcome of the events, such as, at a minimum, the success or failure of the application of the firewall rule. | Traffic logging in firewall policies; Policy and address UUIDs in traffic logs | `config log eventfilter; set event enable; set system enable; set endpoint enable; set user enable; set security-rating enable; end` `config firewall policy; edit <POLICY_ID>; set logtraffic all; next; end` | 7.0.0 or earlier | — |
| FGT-FW | `FNFG-FW-000055` | `SRG-NET-000099-FW-000161` | The FortiGate firewall must protect the traffic log from unauthorized modification of local log records. | Administrator profiles: Log and Report access permission | `config system accprofile; edit <PROFILE>; set loggrp none; next; end` | 7.0.0 or earlier | — |
| FGT-FW | `FNFG-FW-000060` | `SRG-NET-000100-FW-000023` | The FortiGate firewall must protect the traffic log from unauthorized deletion of local log files and log records. | Administrator profiles: Log and Report access permission | `config system accprofile; edit <PROFILE>; set loggrp none; next; end` | 7.0.0 or earlier | — |
| FGT-FW | `FNFG-FW-000070` | `SRG-NET-000192-FW-000029` | The FortiGate firewall must block outbound traffic containing denial-of-service (DoS) attacks to protect against the use of internal information systems to launch any DoS attacks against other networks or endpoints. | IPv4 and IPv6 DoS policies (L3 and L4 anomaly thresholds) | `config firewall DoS-policy; edit <ID>; set interface <INTERFACE>; set srcaddr <SRC_ADDRESS>; set dstaddr <DST_ADDRESS>; set service <SERVICE>; config anomaly; edit <ANOMALY>; set status enable; set log enable; set action block; set threshold <THRESHOLD>; next; end; next; end` | 7.0.0 or earlier | — |
| FGT-FW | `FNFG-FW-000090` | `SRG-NET-000235-FW-000133` | The FortiGate firewall must fail to a secure state if the firewall filtering functions fail unexpectedly. | Fail-closed behavior in conserve mode (IPS and antivirus fail-open disabled) | `config ips global; set fail-open disable; end` `config system global; set av-failopen off; set av-failopen-session disable; end` | 7.0.0 or earlier | — |
| FGT-FW | `FNFG-FW-000155` | `SRG-NET-000399-FW-000008` | The FortiGate firewall must allow authorized users to record a packet-capture-based IP, traffic type (TCP, UDP, or ICMP), or protocol. | Packet capture with host, port, VLAN, and protocol filters; Logs generated when starting and stopping packet capture and TCP dump operations | `config firewall on-demand-sniffer; edit <NAME>; set interface <PORT>; set max-packet-count <NUMBER>; set hosts <IP>; set ports <PORT_NUMBER>; set protocols <PROTOCOL_NUMBER>; next; end` GUI: Network > Packet Capture | 7.0.0 or earlier | — |
| FGT-FW | `FNFG-FW-000160` | `SRG-NET-000492-FW-000006` | The FortiGate firewall must generate traffic log records when traffic is denied, restricted, or discarded. | Traffic logging in firewall policies; Logging of traffic denied by the implicit deny policy | `config log eventfilter; set event enable; set system enable; set endpoint enable; set user enable; set security-rating enable; end` `config firewall policy; edit <POLICY_ID>; set logtraffic all; next; end` | 7.0.0 or earlier | — |
| FGT-FW | `FNFG-FW-000165` | `SRG-NET-000493-FW-000007` | The FortiGate firewall must generate traffic log records when attempts are made to send packets between security zones that are not authorized to communicate. | Logging of traffic denied by the implicit deny policy; Logging local traffic per local-in policy | `config log setting; set fwpolicy-implicit-log enable; set fwpolicy6-implicit-log enable; end` | 7.0.0 or earlier | — |
| IDPS | — | `SRG-NET-000018-IDPS-00018` | The IPS must enforce approved authorizations by restricting or blocking the flow of harmful or suspicious communications traffic within the network. | IPS sensors applied to firewall policies | `config ips sensor; edit <SENSOR>; config entries; edit 1; set severity <SEVERITIES>; set status enable; set action block; set log enable; set log-packet enable; next; end; next; end` `config firewall policy; edit <POLICY_ID>; set utm-status enable; set ips-sensor <SENSOR>; next; end` | 7.0.0 or earlier | P3 |
| IDPS | — | `SRG-NET-000019-IDPS-00019` | The IPS must restrict or block harmful or suspicious communications traffic between interconnected networks based on attribute- and content-based inspection of the source, destination, headers, and/or content of the communications traffic. | IPS sensors applied to firewall policies; Virtual patching on the local-in management interface; IPS sensor entry filters; and 5 more | `config ips sensor; edit <SENSOR>; config entries; edit 1; set severity <SEVERITIES>; set status enable; set action block; set log enable; set log-packet enable; next; end; next; end` `config firewall policy; edit <POLICY_ID>; set utm-status enable; set ips-sensor <SENSOR>; next; end` | 7.0.0 or earlier | P3 |
| IDPS | — | `SRG-NET-000019-IDPS-00187` | The IDPS must immediately use updates made to policy filters, rules, signatures, and anomaly analysis algorithms for traffic detection and prevention functions. | FortiGuard IPS and antivirus signature updates; Highlight on hold IPS signatures; Immediate download update option; and 2 more | `config system autoupdate schedule; set status enable; set frequency automatic; end` | 7.0.0 or earlier | P1, P2, P3, P4 |
| IDPS | — | `SRG-NET-000113-IDPS-00082` | The IDPS must provide audit record generation capability for events where communication traffic is blocked or restricted based on policy filters, rules, signatures, and anomaly analysis. | IPS sensors applied to firewall policies | `config ips sensor; edit <SENSOR>; config entries; edit 1; set severity <SEVERITIES>; set status enable; set action block; set log enable; set log-packet enable; next; end; next; end` `config firewall policy; edit <POLICY_ID>; set utm-status enable; set ips-sensor <SENSOR>; next; end` | 7.0.0 or earlier | P3 |
| IDPS | — | `SRG-NET-000235-IDPS-00169` | The IDPS must fail to a secure state which maintains access control mechanisms when the IDPS hardware, software, or firmware fails on initialization/shutdown or experiences a sudden abort during normal operation. | Fail-closed behavior in conserve mode (IPS and antivirus fail-open disabled) | `config ips global; set fail-open disable; end` `config system global; set av-failopen off; set av-failopen-session disable; end` | 7.0.0 or earlier | — |
| IDPS | — | `SRG-NET-000318-IDPS-00182` | To protect against unauthorized data mining, the IPS must prevent code injection attacks launched against application objects including, at a minimum, application URLs and application code. | IPS sensors applied to firewall policies | `config ips sensor; edit <SENSOR>; config entries; edit 1; set severity <SEVERITIES>; set status enable; set action block; set log enable; set log-packet enable; next; end; next; end` `config firewall policy; edit <POLICY_ID>; set utm-status enable; set ips-sensor <SENSOR>; next; end` | 7.0.0 or earlier | P3 |
| IDPS | — | `SRG-NET-000318-IDPS-00183` | To protect against unauthorized data mining, the IPS must prevent SQL injection attacks launched against data storage objects, including, at a minimum, databases, database records, and database fields. | IPS sensors applied to firewall policies | `config ips sensor; edit <SENSOR>; config entries; edit 1; set severity <SEVERITIES>; set status enable; set action block; set log enable; set log-packet enable; next; end; next; end` `config firewall policy; edit <POLICY_ID>; set utm-status enable; set ips-sensor <SENSOR>; next; end` | 7.0.0 or earlier | P3 |
| IDPS | — | `SRG-NET-000362-IDPS-00197` | The IPS must protect against or limit the effects of known and unknown types of denial-of-service (DoS) attacks by employing anomaly-based attack detection. | IPv4 and IPv6 DoS policies (L3 and L4 anomaly thresholds) | `config firewall DoS-policy; edit <ID>; set interface <INTERFACE>; set srcaddr <SRC_ADDRESS>; set dstaddr <DST_ADDRESS>; set service <SERVICE>; config anomaly; edit <ANOMALY>; set status enable; set log enable; set action block; set threshold <THRESHOLD>; next; end; next; end` | 7.0.0 or earlier | — |
| IDPS | — | `SRG-NET-000362-IDPS-00198` | The IPS must protect against or limit the effects of known types of denial-of-service (DoS) attacks by employing signatures. | IPS sensors applied to firewall policies; Support full extended IPS database for CP9 models and slim extended database for other physical models; Support full extended IPS database for FortiGate VMs with eight cores or more | `config ips sensor; edit <SENSOR>; config entries; edit 1; set severity <SEVERITIES>; set status enable; set action block; set log enable; set log-packet enable; next; end; next; end` `config firewall policy; edit <POLICY_ID>; set utm-status enable; set ips-sensor <SENSOR>; next; end` | 7.0.0 or earlier | P3 |
| VPN | — | `SRG-NET-000053-VPN-000170` | The VPN Gateway must limit the number of concurrent sessions for user accounts to 1 or to an organization-defined number. | SSL VPN settings (TLS version, idle timeout, login limits, client certificates); SSL VPN web portals (tunnel mode is replaced by IPsec VPN from 7.6.3) | `config vpn ssl settings; set ssl-min-proto-ver tls1-2; set idle-timeout <SECONDS>; set login-attempt-limit 3; set login-block-time 900; set reqclientcert enable; end` | 7.0.0 or earlier | P15, P19, P20 |
| VPN | — | `SRG-NET-000132-VPN-000450` | The VPN Gateway must be configured to prohibit the use of all unnecessary and/or nonsecure functions, ports, protocols, and/or services, as defined in the PPSM CAL and vulnerability assessments. | Update SSL VPN default behavior and visibility in the GUI | — | — | — |
| VPN | — | `SRG-NET-000147-VPN-000530` | The IPsec VPN Gateway must use anti-replay mechanisms for security associations. | IPsec VPN phase 2 (AES-256, SHA-384, PFS, replay protection, SA lifetime) | `config vpn ipsec phase2-interface; edit <PHASE2>; set phase1name <TUNNEL>; set proposal aes256-sha384; set pfs enable; set dhgrp 20; set replay enable; set keylifeseconds 28800; next; end` | 7.0.0 or earlier | P43 |
| VPN | — | `SRG-NET-000213-VPN-000721` | The Remote Access VPN Gateway must terminate remote access network connections after an organization-defined time period. | SSL VPN settings (TLS version, idle timeout, login limits, client certificates) | `config vpn ssl settings; set ssl-min-proto-ver tls1-2; set idle-timeout <SECONDS>; set login-attempt-limit 3; set login-block-time 900; set reqclientcert enable; end` | 7.0.0 or earlier | P15, P19, P20 |
| VPN | — | `SRG-NET-000230-VPN-002436` | The VPN Gateway must use Always On VPN connections for remote computing. | Support for autoconnect to IPsec VPN using Microsoft Entra ID | — | — | — |
| VPN | — | `SRG-NET-000343-VPN-001370` | The VPN Gateway must authenticate all network-connected endpoint devices before establishing a connection. | Enhancing IPsec security using EMS SN verification; Cross-validation for IPsec VPN; Security posture tag match enforced before dial-up IPsec VPN connection; and 1 more | — | — | — |
| VPN | — | `SRG-NET-000355-VPN-002433` | The VPN Gateway providing authentication intermediary services must only accept end entity certificates (user or machine) issued by DOD PKI or DOD-approved PKI Certification Authorities (CAs) for the establishment of VPN sessions. | PKI peer users for certificate authentication | `config user peer; edit <PEER_USER>; set ca <CA_CERT>; set subject <SUBJECT>; next; end` | 7.0.0 or earlier | P15, P19 |
| VPN | — | `SRG-NET-000371-VPN-001650` | The VPN Gateway and Client must be configured to protect the confidentiality and integrity of transmitted information. | IPsec VPN phase 2 (AES-256, SHA-384, PFS, replay protection, SA lifetime); Enhancing security with Post-Quantum Cryptography for IPsec key exchange; Support Quantum Key Distribution and Post-Quantum Cryptography; and 1 more | `config vpn ipsec phase2-interface; edit <PHASE2>; set phase1name <TUNNEL>; set proposal aes256-sha384; set pfs enable; set dhgrp 20; set replay enable; set keylifeseconds 28800; next; end` | 7.0.0 or earlier | P43 |
| VPN | — | `SRG-NET-000530-VPN-002340` | The TLS VPN Gateway that supports Government-only services must prohibit client negotiation to TLS 1.1, TLS 1.0, SSL 2.0, or SSL 3.0. | SSL VPN settings (TLS version, idle timeout, login limits, client certificates) | `config vpn ssl settings; set ssl-min-proto-ver tls1-2; set idle-timeout <SECONDS>; set login-attempt-limit 3; set login-block-time 900; set reqclientcert enable; end` | 7.0.0 or earlier | P15, P19, P20 |
| ALG | — | `SRG-NET-000018-ALG-000017` | The ALG must enforce approved authorizations for controlling the flow of information within the network based on attribute- and content-based inspection of the source, destination, headers, and/or content of the communications traffic. | Web filter profiles (FortiGuard categories, URL filters); Application control sensors; DNS filter profiles; and 4 more | `config webfilter profile; edit <PROFILE>; config ftgd-wf; config filters; edit 1; set category <CATEGORY_ID>; set action block; next; end; end; next; end` | 7.0.0 or earlier | P2, P5, P46 |
| ALG | — | `SRG-NET-000019-ALG-000018` | The ALG must restrict or block harmful or suspicious communications traffic by controlling the flow of information between interconnected networks based on attribute- and content-based inspection of the source, destination, headers, and/or content of the communications traffic. | Web filter profiles (FortiGuard categories, URL filters); Application control sensors; DNS filter profiles; and 13 more | `config webfilter profile; edit <PROFILE>; config ftgd-wf; config filters; edit 1; set category <CATEGORY_ID>; set action block; next; end; end; next; end` | 7.0.0 or earlier | P2, P5, P46 |
| ALG | — | `SRG-NET-000019-ALG-000019` | The ALG must immediately use updates made to policy enforcement mechanisms such as policy filters, rules, signatures, and analysis algorithms for gateway and/or intermediary functions. | FortiGuard IPS and antivirus signature updates; Immediate download update option | `config system autoupdate schedule; set status enable; set frequency automatic; end` | 7.0.0 or earlier | P1, P2, P3, P4 |
| ALG | — | `SRG-NET-000062-ALG-000150` | The ALG that provides intermediary services for TLS must be configured to comply with the required TLS settings in NIST SP 800-52. | SSL/SSH inspection profiles (deep inspection and server certificate checks); Configuring a secure explicit proxy; HTTP/2 support in proxy mode SSL inspection; and 7 more | `config firewall ssl-ssh-profile; edit <PROFILE>; config https; set status deep-inspection; set untrusted-server-cert block; set expired-server-cert block; set revoked-server-cert block; end; next; end` | 7.0.0 or earlier | P18, P19, P46 |
| ALG | — | `SRG-NET-000074-ALG-000043` | The ALG must produce audit records containing information to establish what type of events occurred. | Explicit proxy logging enhancements; ZTNA logging enhancements; ZTNA FortiView and log enhancements; and 1 more | — | — | — |
| ALG | — | `SRG-NET-000131-ALG-000085` | The ALG must not have unnecessary services and functions enabled. | Explicit web proxy | `config web-proxy explicit; set status disable; end` | 7.0.0 or earlier | — |
| ALG | — | `SRG-NET-000131-ALG-000086` | The ALG must be configured to remove or disable unrelated or unneeded application proxy services. | Explicit web proxy; SOCKS proxy supports UTM scanning, authentication, and forward server | `config web-proxy explicit; set status disable; end` | 7.0.0 or earlier | — |
| ALG | — | `SRG-NET-000132-ALG-000087` | The ALG must be configured to prohibit or restrict the use of functions, ports, protocols, and/or services, as defined in the PPSM CAL and vulnerability assessments. | Application control sensors; Add option to set application default port as a service port | `config application list; edit <LIST>; config entries; edit 1; set category <CATEGORY_ID>; set action block; next; end; next; end` | 7.0.0 or earlier | P1, P46 |
| ALG | — | `SRG-NET-000138-ALG-000063` | The ALG providing user authentication intermediary services must uniquely identify and authenticate organizational users (or processes acting on behalf of organizational users). | Explicit web proxy; Explicit proxy authentication over HTTPS; Basic ZTNA configuration; and 2 more | `config web-proxy explicit; set status disable; end` | 7.0.0 or earlier | — |
| ALG | — | `SRG-NET-000140-ALG-000094` | The ALG providing user authentication intermediary services must use multifactor authentication for network access to non-privileged accounts. | Improve FortiToken Cloud visibility | — | — | — |
| ALG | — | `SRG-NET-000164-ALG-000100` | The ALG that provides intermediary services for TLS must validate certificates used for TLS functions by performing RFC 5280-compliant certification path validation. | SSL/SSH inspection profiles (deep inspection and server certificate checks); mTLS client certificate authentication; Secure explicit proxy with client certificate blocklist enforcement; and 1 more | `config firewall ssl-ssh-profile; edit <PROFILE>; config https; set status deep-inspection; set untrusted-server-cert block; set expired-server-cert block; set revoked-server-cert block; end; next; end` | 7.0.0 or earlier | P18, P19, P46 |
| ALG | — | `SRG-NET-000246-ALG-000132` | The ALG providing content filtering must update malicious code protection mechanisms and signature definitions whenever new releases are available in accordance with organizational configuration management policy. | FortiGuard IPS and antivirus signature updates | `config system autoupdate schedule; set status enable; set frequency automatic; end` | 7.0.0 or earlier | P1, P2, P3, P4 |
| ALG | — | `SRG-NET-000248-ALG-000133` | The ALG providing content filtering must be configured to perform real-time scans of files from external sources at network entry/exit points as they are downloaded and prior to being opened or executed. | Antivirus profiles; Stream-based antivirus scan in proxy mode for FTP, SFTP, and SCP; AI-based malware detection; and 5 more | `config antivirus profile; edit <PROFILE>; config http; set av-scan block; end; next; end` | 7.0.0 or earlier | P4, P46 |
| ALG | — | `SRG-NET-000249-ALG-000134` | The ALG providing content filtering must block malicious code upon detection. | Antivirus profiles; Configure threat feed and outbreak prevention without AV engine scan; Malware threat feed from EMS; and 6 more | `config antivirus profile; edit <PROFILE>; config http; set av-scan block; end; next; end` | 7.0.0 or earlier | P4, P46 |
| ALG | — | `SRG-NET-000249-ALG-000145` | The ALG providing content filtering must delete or quarantine malicious code in response to malicious code detection. | Antivirus profiles; Download quarantined files in archive format | `config antivirus profile; edit <PROFILE>; config http; set av-scan block; end; next; end` | 7.0.0 or earlier | P4, P46 |
| ALG | — | `SRG-NET-000288-ALG-000109` | The ALG providing content filtering must block or restrict detected prohibited mobile code. | Web filter profiles (FortiGuard categories, URL filters) | `config webfilter profile; edit <PROFILE>; config ftgd-wf; config filters; edit 1; set category <CATEGORY_ID>; set action block; next; end; end; next; end` | 7.0.0 or earlier | P2, P5, P46 |
| ALG | — | `SRG-NET-000384-ALG-000136` | The ALG providing content filtering must detect use of network services that have not been authorized or approved by the ISSM and ISSO, at a minimum. | Application control sensors | `config application list; edit <LIST>; config entries; edit 1; set category <CATEGORY_ID>; set action block; next; end; next; end` | 7.0.0 or earlier | P1, P46 |
| ALG | — | `SRG-NET-000390-ALG-000139` | The ALG providing content filtering must continuously monitor inbound communications traffic crossing internal security boundaries for unusual or unauthorized activities or conditions. | SSL/SSH inspection profiles (deep inspection and server certificate checks); Inspecting HTTP3 traffic; Remove option to block QUIC by default in application control | `config firewall ssl-ssh-profile; edit <PROFILE>; config https; set status deep-inspection; set untrusted-server-cert block; set expired-server-cert block; set revoked-server-cert block; end; next; end` | 7.0.0 or earlier | P18, P19, P46 |
| ALG | — | `SRG-NET-000391-ALG-000140` | The ALG providing content filtering must continuously monitor outbound communications traffic crossing internal security boundaries for unusual/unauthorized activities or conditions. | SSL/SSH inspection profiles (deep inspection and server certificate checks); DNS inspection with DoT and DoH; Control TLS connections that utilize Encrypted Client Hello | `config firewall ssl-ssh-profile; edit <PROFILE>; config https; set status deep-inspection; set untrusted-server-cert block; set expired-server-cert block; set revoked-server-cert block; end; next; end` | 7.0.0 or earlier | P18, P19, P46 |
| ALG | — | `SRG-NET-000400-ALG-000097` | The ALG providing user authentication intermediary services must transmit only encrypted representations of passwords. | Explicit proxy authentication over HTTPS; Configuring a secure explicit proxy | — | — | — |
| ALG | — | `SRG-NET-000512-ALG-000066` | The ALG that provides intermediary services for HTTP must inspect inbound and outbound HTTP traffic for protocol compliance and protocol anomalies. | Restriction and validation of HTTP messages | — | — | — |
| ALG | — | `SRG-NET-000750-ALG-000140` | The ALG must include only approved trust anchors in trust stores or certificate stores managed by the organization. | SSL/SSH inspection profiles (deep inspection and server certificate checks) | `config firewall ssl-ssh-profile; edit <PROFILE>; config https; set status deep-inspection; set untrusted-server-cert block; set expired-server-cert block; set revoked-server-cert block; end; next; end` | 7.0.0 or earlier | P18, P19, P46 |
| RTR | — | `SRG-NET-000018-RTR-000001` | The router must be configured to enforce approved authorizations for controlling the flow of information within the network based on organization-defined information flow control policies. | Static routes and policy routes; BGP RPKI route origin validation | — | — | — |
| RTR | — | `SRG-NET-000018-RTR-000002` | The BGP router must be configured to reject inbound route advertisements for any Bogon prefixes. | BGP neighbors (passwords, maximum prefixes, inbound prefix lists) | `config router bgp; config neighbor; edit <NEIGHBOR_IP>; set password <PASSWORD>; set maximum-prefix <NUMBER>; set prefix-list-in <PREFIX_LIST>; next; end; end` | 7.0.0 or earlier | P45 |
| RTR | — | `SRG-NET-000018-RTR-000003` | The BGP router must be configured to reject inbound route advertisements for any prefixes belonging to the local autonomous system (AS). | BGP neighbors (passwords, maximum prefixes, inbound prefix lists) | `config router bgp; config neighbor; edit <NEIGHBOR_IP>; set password <PASSWORD>; set maximum-prefix <NUMBER>; set prefix-list-in <PREFIX_LIST>; next; end; end` | 7.0.0 or earlier | P45 |
| RTR | — | `SRG-NET-000131-RTR-000035` | The router must be configured to have all non-essential capabilities disabled. | Static routes and policy routes | — | — | — |
| RTR | — | `SRG-NET-000168-RTR-000078` | The router must be configured to authenticate all routing protocol messages using NIST-validated FIPS 198-1 message authentication code algorithm. | OSPF with message-digest authentication; Key chains for routing protocol authentication (HMAC-SHA algorithms, key lifetimes); OSPF HMAC-SHA authentication; and 1 more | `config router ospf; config ospf-interface; edit <NAME>; set interface <PORT>; set authentication message-digest; set keychain <KEYCHAIN>; next; end; end` | 7.0.0 or earlier | P45 |
| RTR | — | `SRG-NET-000202-RTR-000001` | The perimeter router must be configured to deny network traffic by default and allow network traffic by exception. | Implicit deny (traffic not allowed by a policy is denied) | — | — | — |
| RTR | — | `SRG-NET-000205-RTR-000001` | The router must be configured to restrict traffic destined to itself. | Enhanced security with default local-in policy | — | — | — |
| RTR | — | `SRG-NET-000205-RTR-000014` | The perimeter router must be configured to restrict it from accepting outbound IP packets that contain an illegitimate address in the source address field via egress filter or by enabling Unicast Reverse Path Forwarding (uRPF). | Asymmetric routing disabled (reverse path check of source addresses) | `config system settings; set asymroute disable; set asymroute-icmp disable; set asymroute6 disable; set asymroute6-icmp disable; end` | 7.0.0 or earlier | — |
| RTR | — | `SRG-NET-000230-RTR-000001` | The router must be configured to implement message authentication for all control plane protocols. | OSPF with message-digest authentication; OSPF HMAC-SHA authentication | `config router ospf; config ospf-interface; edit <NAME>; set interface <PORT>; set authentication message-digest; set keychain <KEYCHAIN>; next; end; end` | 7.0.0 or earlier | P45 |
| RTR | — | `SRG-NET-000230-RTR-000002` | The BGP router must be configured to use a unique key for each autonomous system (AS) that it peers with. | BGP neighbors (passwords, maximum prefixes, inbound prefix lists); Add static route tag and BGP neighbor password; BGP incorporates the advanced security measures of TCP Authentication Option (TCP-AO) | `config router bgp; config neighbor; edit <NEIGHBOR_IP>; set password <PASSWORD>; set maximum-prefix <NUMBER>; set prefix-list-in <PREFIX_LIST>; next; end; end` | 7.0.0 or earlier | P45 |
| RTR | — | `SRG-NET-000230-RTR-000003` | The router must be configured to use keys with a duration not exceeding 180 days for authenticating routing protocol messages. | Key chains for routing protocol authentication (HMAC-SHA algorithms, key lifetimes) | `config router key-chain; edit <KEYCHAIN>; config key; edit 1; set key-string <KEY>; set algorithm hmac-sha256; set accept-lifetime <LIFETIME>; set send-lifetime <LIFETIME>; next; end; next; end` | 7.0.0 or earlier | P45 |
| RTR | — | `SRG-NET-000362-RTR-000112` | The router must be configured to have IP directed broadcast disabled on all interfaces. | Interface services that are not needed (DHCP relay, PPTP client, ARP, broadcast, layer 2, VLAN, and STP forwarding, ICMP redirects, LLDP transmission) | `config system interface; edit <INTERFACE>; set dhcp-relay-service disable; set pptp-client disable; set arpforward disable; set broadcast-forward disable; set l2forward disable; set icmp-send-redirect disable; set vlanforward disable; set stpforward disable; set lldp-transmission disable; next; end` | 7.0.0 or earlier | — |
| RTR | — | `SRG-NET-000362-RTR-000115` | The router must be configured to have Internet Control Message Protocol (ICMP) redirects disabled on all external interfaces. | Interface services that are not needed (DHCP relay, PPTP client, ARP, broadcast, layer 2, VLAN, and STP forwarding, ICMP redirects, LLDP transmission) | `config system interface; edit <INTERFACE>; set dhcp-relay-service disable; set pptp-client disable; set arpforward disable; set broadcast-forward disable; set l2forward disable; set icmp-send-redirect disable; set vlanforward disable; set stpforward disable; set lldp-transmission disable; next; end` | 7.0.0 or earlier | — |
| RTR | — | `SRG-NET-000362-RTR-000117` | The BGP router must be configured to use the maximum prefixes feature to protect against route table flooding and prefix de-aggregation attacks. | BGP neighbors (passwords, maximum prefixes, inbound prefix lists) | `config router bgp; config neighbor; edit <NEIGHBOR_IP>; set password <PASSWORD>; set maximum-prefix <NUMBER>; set prefix-list-in <PREFIX_LIST>; next; end; end` | 7.0.0 or earlier | P45 |
| RTR | — | `SRG-NET-000364-RTR-000111` | The perimeter router must be configured to have Link Layer Discovery Protocols (LLDPs) disabled on all external interfaces. | Interface services that are not needed (DHCP relay, PPTP client, ARP, broadcast, layer 2, VLAN, and STP forwarding, ICMP redirects, LLDP transmission) | `config system interface; edit <INTERFACE>; set dhcp-relay-service disable; set pptp-client disable; set arpforward disable; set broadcast-forward disable; set l2forward disable; set icmp-send-redirect disable; set vlanforward disable; set stpforward disable; set lldp-transmission disable; next; end` | 7.0.0 or earlier | — |
| RTR | — | `SRG-NET-000364-RTR-000113` | The perimeter router must be configured to block all outbound management traffic. | Deny policy for outbound management traffic (premise firewall) | `config firewall policy; edit <POLICY_ID>; set srcintf <MGMT_INTERFACE>; set dstintf <EGRESS_INTERFACE>; set srcaddr <MGMT_NETWORK>; set dstaddr <ALL_ADDRESS>; set schedule <SCHEDULE>; set service <ALL_SERVICE>; set action deny; set logtraffic all; next; end` | 7.0.0 or earlier | P42 |

### Alignment summary

| STIG | Same requirement | Equivalent setting | Partial | Not supported | Not applicable | By procedure | Total | FortiGate STIG rule for the same SRG ID |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| ASA-NDM (V2R5) | 38 | 8 | 1 | 0 | 0 | 0 | 47 | 39 |
| ASA-FW (V2R1) | 19 | 1 | 1 | 0 | 0 | 0 | 21 | 19 |
| ASA-VPN (V2R2) | 21 | 19 | 1 | 0 | 0 | 0 | 41 | 0 |
| ASA-IPS (V2R1) | 5 | 18 | 0 | 0 | 0 | 0 | 23 | 0 |
| **Total** | **83** | **46** | **3** | **0** | **0** | **0** | **132** | **58** |

FortiGate meets 129 of the 132 ASA rules' requirements with
a setting (83 through the feature Chapter 30 maps and 46 through
another setting), and 3 only in part; no rule describes a capability
FortiGate lacks or a component it does not have. **58 of the
132 ASA rules have a FortiGate STIG rule for the same SRG
requirement** (39 of the 47 NDM rules and 19 of
the 21 Firewall rules, matching 57 distinct FortiGate
rules); the ASA VPN and IPS rules have none, because FortiGate has no VPN or
IPS STIG. The main differences:

- **Where the ASA STIG is stricter.** The ASA rules require a 5-minute idle
  timeout (`CASA-ND-000690`), two authentication servers (`CASA-ND-001310`),
  and two log servers (`CASA-ND-001410`); the FortiGate STIG rules for the
  same SRG IDs ask for 10 minutes, LDAP, and one log server, while the SRG
  asks for two servers on boundary devices. Meet the ASA value on FortiGate:
  `admintimeout 5`, an LDAP server with `secondary-server`, and two syslog
  destinations (`syslogd` and `syslogd2`).
- **Where FortiGate is stricter.** The FortiGate phase 1 key lifetime of
  28,800 seconds meets the eight hours of `SRG-NET-000337-VPN-001300`, where
  the ASA rule allows 24 hours. FortiGate syslog can use reliable TCP
  transport with TLS (`set mode reliable` and `set enc-algorithm high`), where
  the ASA rule asks only for TCP. The FortiGate STIG has an administrator
  lockout rule (`FGFW-ND-000045`, three attempts and 15 minutes) that the ASA
  NDM STIG lacks. The ASA has a lockout setting, but from 9.17(1) it unlocks
  users after 10 minutes:

  ASA: `aaa local authentication attempts max-fail 3`

- **The three Partial rows.** FortiOS 8.0.1 has no option for changed
  characters in administrator passwords (`CASA-ND-000580`; Chapter 30 records
  the same gap for `FGFW-ND-000311`). The FortiOS IPv6 extension header filter
  blocks chosen headers but does not check header order or unknown headers
  (`CASA-FW-000280`):

  FortiOS: `config firewall ipv6-eh-filter; set hop-opt enable; set routing enable; end`

  The remote access banner (`CASA-VN-000460`) is shown by the client after
  it connects on both platforms; the ASA group-policy banner is a post-login
  banner, so neither meets "before granting access" by itself.
- **IPS through the FirePOWER module.** The ASA IPS STIG configures the ASA
  FirePOWER module in ASDM, and the ASA redirects traffic to it with a service
  policy (`sfr`). On FortiGate the same requirements are met by IPS sensors,
  antivirus profiles, and FortiGuard updates on the firewall policies
  themselves, assessed against the IDPS SRG (Chapter 30). FortiGate alerts by
  email directly from automation stitches on IPS, antivirus, and anomaly
  logs; the ASA FirePOWER module alerts through syslog or SNMP to a SIEM.
- **VPN on 7.6.3 and later.** From FortiOS 7.6.3, SSL VPN tunnel mode is
  replaced by IPsec VPN (Chapter 30). The ASA remote access rules that rely
  on AnyConnect TLS settings map to the FortiGate dial-up IPsec VPN, and to
  the Agentless VPN settings for TLS.

### Collecting evidence

In a mixed estate, keep one checklist row per ASA rule for each firewall,
with the SRG ID, the FortiGate STIG rule, and the alignment category from the
table, and attach each platform's evidence:

- **Cisco ASA:** `show version` for the release, and `show running-config
  all` for the settings that do not appear in the default output (Chapter
  31). For the IPS STIG, ASDM screenshots or exports of the ASA FirePOWER
  access control, intrusion, file, and alert configuration.
- **FortiGate:** `get system status` for the release, and `show
  full-configuration` for the settings in the FortiOS column, with the
  FortiGate STIG checklist (Chapter 30) for the rules in the FortiGate STIG
  rule column.
- **For every Partial row:** the open finding, its mitigation, and its
  approval, recorded against the FortiGate STIG rule or the SRG ID.

Keep the FortiGate-only requirements (the second table) on the FortiGate
checklist as well (Chapter 03 describes SRG-based checklists).

## Validation and Troubleshooting

- **An ASA rule seems to have no row.** Every one of the 132 rules
  has a row; the build script fails if one is missing. Search for the rule
  ID, not the title.
- **An ASA command from a fix text is rejected.** Check *ASA fix text
  corrections* and the release: `group 24`, `set pfs group5`, and `3des` were
  removed in 9.15(1), and `dh-group14-sha` is not a documented value. Use `?` on
  the CLI.
- **An IKEv2 tunnel between an ASA and a FortiGate does not come up.** Both
  ends must offer the same proposal: AES-256 with SHA-384 (or AES-256-GCM
  with PRF SHA-384) and DH group 20, and the same PFS group in phase 2.
- **An assessor asks for the FortiGate rule for an ASA VPN or IPS rule.**
  There is none; show the VPN or IDPS SRG requirement in the SRG ID column,
  as Chapter 30 maps it.
- **The ASA keeps sending traffic when the FirePOWER module is down.** The
  fix text uses `sfr fail-open`; use `sfr fail-close` where the policy
  requires the firewall to fail secure, and record the choice.

## Security and Best Practices

- Treat the ASA STIG rules as the checklist for every firewall, add the
  FortiGate-only requirements, and record each FortiGate finding against the
  FortiGate STIG rule where one exists.
- On both platforms, end idle management sessions after 5 minutes, lock
  accounts after three failed logons, show the DoD banner, require
  15-character passwords, and allow management only over SSH and HTTPS from
  trusted hosts.
- Use two authentication servers, two log servers over TCP (with TLS where
  available), and two authenticated NTP servers.
- Use IKEv2 with AES-256, SHA-384, DH group 20, and PFS, with lifetimes of
  eight hours or less, and certificate authentication for peers and remote
  users.
- Enable FIPS mode where DoD policy requires FIPS-validated cryptography.
- Record every Partial row as an open finding with its mitigation, and
  review the crosswalk whenever DISA updates either STIG package or an SRG,
  or a new ASA or FortiOS release changes the commands.

## References and Knowledge Checks

**References:**

- DISA Cisco ASA NDM STIG V2R5, Firewall STIG V2R1, VPN STIG V2R2, and IPS
  STIG V2R1 (`U_Cisco_ASA_Y26M07_STIG.zip`); Fortinet FortiGate Firewall NDM
  STIG V1R6 and Firewall STIG V1R5 (`U_FN_FortiGate_Firewall_Y26M10_STIG.zip`);
  and the Network Device Management SRG V5R5, Firewall SRG V3R4, VPN SRG
  V3R5, and IDPS SRG V3R4, from the October 2026 STIG Library Compilation.
- Cisco, *Cisco Secure Firewall ASA Series Command Reference* (A-H, I-R, S,
  and T-Z), *Cisco Secure Firewall ASA Series General Operations CLI
  Configuration Guide, 9.24* (port literals), and *Cisco ASA with FirePOWER
  Services Local Management Configuration Guide, Version 7.0*.
- Fortinet, *FortiOS 8.0.1 CLI Reference*.
- [Chapter 03](03-the-srg-catalog-how-stigs-are-built-and-what-to-do-without-one.md)
  (how STIGs are built from SRGs, and SRG-based assessment),
  [Chapter 07](07-network-device-stigs-management-routing-and-filtering.md)
  (network device STIGs by plane),
  [Chapter 30](30-fortigate-feature-version-and-stig-map.md) (the FortiGate
  feature and STIG map, source of the FortiOS commands and versions),
  [Chapter 31](31-cisco-products-stigs-and-srg-mapping.md) (the Cisco STIG
  packages, the ASA STIGs, and FTD), and
  [Chapter 33](33-fortiswitch-and-cisco-catalyst-switch-stig-crosswalk.md)
  (the FortiSwitch and Cisco Catalyst switch crosswalk).

**Knowledge checks:**

1. Why is this crosswalk a STIG-to-STIG pair, and against which checklist is
   a FortiGate finding for an ASA NDM rule recorded?
2. Why do the ASA VPN and IPS rules have no FortiGate STIG rule, and what
   does a FortiGate get assessed against instead?
3. Which idle timeout should a mixed estate use, and why does the FortiGate
   STIG's value not settle the question?
4. Why does `group 24` from the ASA VPN STIG fail on ASA 9.15(1) and later,
   and what replaces it?
5. Does the ASA STIG apply to a Firepower appliance running FTD?
6. Name two FortiGate STIG rules that an ASA rule checklist would miss.
7. How does the ASA IPS STIG's alerting differ from FortiGate's?

## Summary and Completion Checklist

Cisco ASA and FortiGate both have STIGs, built from the same SRGs. This
chapter aligns all 132 ASA rules (47 NDM, 21 Firewall,
41 VPN, and 23 IPS) with the FortiGate STIG rule and the
FortiGate setting and FortiOS command that meet the same SRG requirement:
83 through the feature Chapter 30 maps, 46 through another setting,
and 3 only in part. 58 ASA rules have a FortiGate STIG rule
for the same SRG ID. It also lists the 88 FortiGate requirements that no
ASA rule covers. Every ASA command was checked by script against the ASA
command reference (with the fix text errors corrected), every ASDM path
against the ASA FirePOWER guide, and every FortiOS command against the
FortiOS 8.0.1 CLI Reference.

- [ ] Can explain why this pair is STIG to STIG, and record a FortiGate
  finding against the right rule or SRG requirement.
- [ ] Can find an ASA rule in the crosswalk and configure the FortiGate
  setting that meets the same requirement.
- [ ] Can correct the ASA fix texts that current ASA releases reject.
- [ ] Can add the FortiGate-only requirements to a FortiGate checklist.
- [ ] Can tell ASA software from FTD when deciding which STIG applies.
