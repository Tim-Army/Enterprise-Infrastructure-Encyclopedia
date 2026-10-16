# Chapter 37: Cisco NX-OS Switch and FortiSwitch STIG Crosswalk

## Learning Objectives

- Explain why a FortiSwitch is assessed against SRGs and why there is no
  FortiSwitch STIG to compare with the Cisco NX-OS Switch STIGs.
- Align a Cisco NX-OS Switch STIG rule with the FortiSwitch setting that
  meets the same SRG requirement, and with the corrected Nexus 9000 NX-OS
  command that meets it on the Cisco side.
- Explain how this chapter relates to Chapter 33: the same FortiSwitch side
  for the rules the two Cisco packages share, a different Cisco platform,
  and different Cisco syntax.
- Tell the six alignment categories apart and record each one correctly on
  an SRG-based checklist.
- Recognize where Nexus data center features (vPC, FabricPath, VXLAN EVPN,
  CoPP) differ from their FortiSwitch counterparts (MCLAG and VXLAN).
- Find the FortiSwitch requirements that no NX-OS rule covers, so that the
  checklist covers both directions.

## Theory and Architecture

**DISA publishes no FortiSwitch STIG.** A FortiSwitch in a DoD network is
assessed directly against the SRGs that match its functions: the Layer 2
Switch, Network Device Management (NDM), Router, and AAA Services SRGs, as
[Chapter 11](11-fortiswitch-feature-version-and-srg-map.md) maps them.
Cisco Nexus switches running NX-OS do have STIGs: the Cisco NX-OS Switch
STIG package (N-NDM V3R6, N-L2S V3R4, and N-RTR V3R4, 142 rules in
all; [Chapter 31](31-cisco-products-stigs-and-srg-mapping.md)). Those STIGs
were written from the same SRGs: every NX-OS rule names the SRG
requirement it implements.

This chapter aligns the two platforms **through the SRG requirement each
NX-OS rule implements**. For every one of the 142 rules it gives the
corrected Nexus 9000 NX-OS command, the FortiSwitch setting and
FortiSwitchOS command that meet the same requirement, and how closely
FortiSwitch meets it. An organization that runs Nexus switches in the data
center and FortiSwitches elsewhere can use the NX-OS rules as one checklist
for both, and see where FortiSwitch differs.

### Why this is a crosswalk, not a STIG comparison

A STIG is a vendor-specific implementation of one or more SRGs (Chapter 03).
With no FortiSwitch STIG there is no FortiSwitch rule to record a finding
against: the assessor records it against the SRG requirement itself, on an
SRG-based checklist. A crosswalk keeps that distinction:

- **The NX-OS rule is a reference, not a requirement for FortiSwitch.** A
  FortiSwitch is never "compliant with `CISC-ND-000720`". It meets
  `SRG-APP-000190-NDM-000267`, the requirement that rule implements, and the
  FortiSwitch finding is recorded against that SRG ID.
- **The SRG ID is the join key.** Two settings align because they implement
  the same requirement, not because they look alike.
- **The NX-OS package covers only part of the SRGs.** The 142 rules
  cite 140 distinct SRG IDs. Chapter 11 maps FortiSwitch features to
  60 requirement IDs, of which 25 have no NX-OS rule at
  all, including all seven AAA Services SRG requirements. The second table
  in this chapter lists them.

### How this chapter relates to Chapter 33

[Chapter 33](33-fortiswitch-and-cisco-catalyst-switch-stig-crosswalk.md)
aligns the Cisco IOS XE Switch STIGs (Catalyst switches) with FortiSwitch.
The NX-OS and IOS XE switch packages were written together and share one
rule numbering scheme, so the two crosswalks have **the same FortiSwitch
side for the same requirement**, but a different Cisco platform and
different Cisco syntax:

- **127 of the 142 NX-OS rule IDs also exist in the IOS XE
  Switch STIGs.** 119 of them have the same SRG ID and the same
  title, and one more (`CISC-ND-000580`) differs only in spelling
  ("lower-case" for "lowercase"). For these 120 rules the crosswalk
  reuses Chapter 33's FortiSwitch setting, FortiSwitchOS command,
  FortiSwitchOS version, and alignment unchanged; the build script checks
  that every reused FortiSwitchOS command appears in the Chapter 33 row for
  the same rule. Two reused rows reword the setting text for NX-OS
  (`CISC-ND-000290`, which mentions the NX-OS ACL `log` keyword, and
  `CISC-L2-000160`, where NX-OS storm control levels are percentages); the
  command is unchanged.
- **Seven shared rule IDs have a different NX-OS requirement**, so the
  FortiSwitch side was aligned again: `CISC-ND-000150` asks NX-OS to
  disconnect the session after three failed logons (IOS XE: lock the
  account for 15 minutes); `CISC-ND-000210` is a non-repudiation rule (IOS
  XE: audit administrator activity); `CISC-ND-001150` asks for
  FIPS-compliant NTP authentication (IOS XE: cryptographically based), which
  turns the FortiSwitch row from Same requirement into Partial;
  `CISC-L2-000020` asks only to identify endpoints; `CISC-L2-000090` adds
  host ports to root guard; `CISC-RT-000050` asks for FIPS 198-1 routing
  authentication without the key lifetime clause, which NX-OS puts in a
  separate rule (`CISC-RT-000030`); and `CISC-RT-000470` asks BGP to check
  that a single-hop eBGP peer is directly connected (IOS XE: enable GTSM).
- **15 rules exist only in the NX-OS package**, among them
  replay-resistant authentication (`CISC-ND-000530`), control plane DoS
  protection (`CISC-ND-001220`), session capture (`CISC-L2-000060` and
  `CISC-L2-000070`), three routing authentication rules (`CISC-RT-000020`
  to `CISC-RT-000040`), the call home rule (`CISC-RT-000080`), and the ICMP
  fragment filter (`CISC-RT-000140`). Their
  FortiSwitch side was found here, in Chapter 11 and the FortiSwitchOS 8.0.0
  CLI Reference.
- **25 IOS XE rules have no NX-OS counterpart** (for example the
  password length, Rapid STP, static trunk, and IPv6 extension header
  rules), so they are not in this chapter. Where Chapter 11 maps their
  requirement, it appears in the second table, with the FortiSwitch side of
  the IOS XE rule from Chapter 33.
- **The Cisco commands are not reused.** NX-OS syntax differs from IOS XE
  throughout (for example `feature` commands, `ip access-list` without
  `standard` or `extended` and with prefix lengths, `exec-timeout` in
  minutes only, `aaa group server radius` with `server` statements, and
  `class-map type qos` with `policy-map type queuing`), so every NX-OS
  command was taken from the NX-OS fix text and checked against Cisco's
  Nexus 9000 documentation, not from Chapter 32.

### How the rules are aligned

Each NX-OS rule was aligned in four steps:

1. **Take the SRG ID the rule implements.** The rule ID, severity, SRG ID,
   title, and fix text come from the Cisco NX-OS Switch STIG XCCDF files
   (`U_Cisco_NX-OS_Switch_Y26M07_STIG.zip`).
2. **Reuse Chapter 33 where the rule is the same.** A rule with the same ID,
   SRG ID, and title as the IOS XE rule takes Chapter 33's FortiSwitch side.
3. **Otherwise look for the same SRG ID in Chapter 11.** 36 of the
   142 rules cite an SRG ID that Chapter 11 maps to a FortiSwitch
   feature. For the rest, the requirement text comes from the SRG XCCDF
   files (Layer 2 Switch V3R4, NDM V5R5, Router V5R2, and AAA Services
   V2R3) and the FortiSwitch setting from the FortiSwitchOS 8.0.0 CLI
   Reference.
4. **Judge how well the setting meets the requirement**, and assign one of
   the alignment categories below. Of the 142 rows, 120
   reuse Chapter 33 and 22 were aligned in this chapter.

Two cautions apply:

- **CCIs were not used to match requirements.** Many SRG requirements share
  the catch-all CCI-000366, so a CCI match often links unrelated
  requirements. Every alignment rests on the SRG ID or the requirement text.
- **4 NX-OS rules cite SRG IDs that are not in the current
  SRGs.** `CISC-ND-001030` (`SRG-APP-000373-NDM-000298`, redundant time
  sources) and `CISC-ND-001470` (`SRG-APP-000516-NDM-000351`, supported
  release) cite IDs that NDM SRG V5R5 no longer has; their rows, reused from
  Chapter 33, name the current requirements (`SRG-APP-000920-NDM-000320`
  and `SRG-APP-001035-NDM-000340`). `CISC-L2-000060` and `CISC-L2-000070`
  cite `SRG-NET-000331-L2S-000001` and `SRG-NET-000332-L2S-000002`, which
  Layer 2 Switch SRG V3R4 no longer has, and the current SRG has no
  requirement for session capture at all; the rows are kept, and say so.

### Where the commands come from

- **NX-OS commands start from each rule's fix text** and were checked
  against Cisco's Nexus 9000 documentation for a current release, read
  through a browser (cisco.com refuses scripted downloads) on 15 October
  2026: the **Cisco Nexus 9000 Series NX-OS Command Reference
  (Configuration Commands), Release 10.5(x)**, all 4,213 entries; the
  Release 9.3(x) reference for the three entries the 10.5(x) reference
  lacks (`aaa accounting default`, `logging ip access-list cache entries`,
  and the basic `snmp-server host` entry); the 10.5(x) Show Commands
  reference for `show version`; and the 10.5(x) Security, System
  Management, Fundamentals, Interfaces, Layer 2 Switching, Unicast Routing,
  Multicast Routing, Quality of Service, and Label Switching Configuration
  Guides. The 10.5(x) reference is generated from the CLI and shows many
  values only as placeholders (`<port_mode>`, `<algo-name>`,
  `<profile_type>`); those values (for example `switchport mode access`,
  the SSH MAC and cipher names, `copp profile strict`, and the queuing class
  names) were confirmed in the configuration guides.
- **A script checked every NX-OS statement** (149 reference
  entries in all): it must match a statement pattern that names its
  reference entry, the entry's documented command mode must be the mode the
  pattern assumes, the statement must follow the command that enters that
  mode (interface, `ip access-list`, `key chain`, `router bgp`, neighbor,
  address family, VRF, class map, policy map, route map, EEM applet, SPAN
  session, `system qos`), and every literal word must be in the entry's
  syntax or syntax description or in a configuration guide passage saved
  for that entry. Numbers are checked against documented ranges (syslog
  severity 0 to 7, NTP key 1 to 65535). The script was tested with
  deliberately wrong commands (a misspelled command, the IOS XE forms of
  `exec-timeout`, `ip access-list standard`, and the one-line BGP
  `neighbor ... password`, DISA's `switch bgp`, an undocumented guard type,
  NTP algorithm, SSH MAC, CoPP profile, key chain algorithm, and port mode,
  `feature wccp`, the fix text's `spt-threshold infinity group` form, and a
  syslog severity of 9) and caught all of them.
- **FortiSwitchOS commands come from Chapter 33** for the reused rows, and
  otherwise from Chapter 11 and the **FortiSwitchOS 8.0.0 CLI Reference**.
  The Chapter 33 script checked every FortiSwitchOS command against the CLI
  Reference: each `config` path must be a documented syntax block, each
  nested `config` a documented sub-table, each `set` option an option of
  that path, and each literal value a documented value or inside the
  documented range. Commands starting with **FortiGate:** are FortiLink
  managed-mode commands, checked the same way against the FortiOS 8.0.1 CLI
  Reference.
- Read the command cells as in Chapters 11 and 33: each pair of backticks
  is one block, statements are separated by `;` (on the CLI, enter each on
  its own line), and values in `<ANGLE_BRACKETS>` are placeholders. Names in
  capitals, such as `RADIUS_SERVERS` or `PREFIX_FILTER`, are the fix text's
  example names. NX-OS statements are entered in global configuration mode;
  a mode command (`interface`, `ip access-list`, `router bgp`, and so on)
  applies to the statements after it, up to the next mode command or
  `exit`.
- A dash (**—**) in the NX-OS column means the Nexus 9000 10.5(x)
  documentation has no command for the rule (the MPLS LDP, RSVP-TE, VPWS,
  and VPLS rules: the 10.5(x) Label Switching Configuration Guide covers
  static MPLS, MPLS L3VPN, and segment routing, and the 10.5(x) reference
  documents LDP subcommands but no command that enters LDP configuration
  mode) or that the rule is met by procedure. A dash in the FortiSwitchOS
  column means the 8.0.0 CLI Reference has no setting for the requirement.

### Fix text corrections

DISA's NX-OS fix texts contain syntax that does not parse on a Nexus 9000,
and a few examples that do not meet their own rule. The crosswalk corrects
them as follows:

- **IOS forms in NX-OS fix text.** `CISC-RT-000020`, `CISC-RT-000040`, and
  `CISC-RT-000520` write `switch bgp` for `router bgp` (a find-and-replace
  of "router"), and `CISC-RT-000040` and `CISC-RT-000520` use the IOS
  one-line `neighbor <IP> password` and `neighbor <IP> prefix-list ... out`;
  NX-OS enters the neighbor first and sets the prefix list under its
  `address-family ipv4 unicast`. `CISC-RT-000760` to `CISC-RT-000780` use
  IOS MQC (`class-map match-all`, `match ip dscp`, `priority percent`, and
  an output `service-policy` on each interface); NX-OS classifies with
  `class-map type qos` and `match dscp`, marks a QoS group, and schedules
  with a `policy-map type queuing` on the system-defined egress classes,
  attached under `system qos`. `CISC-ND-001220` and `CISC-RT-000120` use
  IOS `police <rate> <burst> conform-action ... exceed-action ...`; the
  crosswalk uses `copp profile strict`, one of the built-in CoPP policies
  (CoPP cannot be disabled on NX-OS). `CISC-RT-000680` is IOS XE syntax
  throughout (`interface Pseudowire`, `l2vpn vfi context`, `service
  instance`, `bridge-domain`), and `CISC-RT-000710` and `CISC-RT-000720`
  use `bridge-domain` commands; none is in the Nexus 9000 10.5(x)
  reference.
- **Syntax errors.** `CISC-ND-000490` repeats the prompt
  (`SW2(config)# switch(config)# username`). `CISC-ND-000530` and
  `CISC-ND-001200` list two MACs in one `ssh macs` command and
  `CISC-ND-001210` two ciphers in one `ssh ciphers` command; the reference
  takes one algorithm name per command, so each becomes two commands.
  `CISC-ND-001410` closes its EEM action with a typographic quotation mark.
  `CISC-L2-000230` writes `except 1, 999` with a space. `CISC-L2-000160`
  uses the IOS `int range e0/2 – 8`, and several L2S rules write port
  ranges with an en dash (`e1/1 – 44`); NX-OS uses `interface ethernet
  1/1-44`. `CISC-RT-000530` names its prefix list `FILTER _CORE_PREFIXES`
  with a stray space. `CISC-RT-000810` writes `deny 239.0.0.0/8` with no
  protocol or source (`deny ip any 239.0.0.0/8`). `CISC-RT-000840` and
  `CISC-RT-000860` start a route map without a sequence number.
  `CISC-RT-000890` writes `ip pim spt-threshold infinity group prefix-list`
  where NX-OS has `group-list prefix-list`. `CISC-RT-000050` writes the key
  chain algorithm as `hmac-sha-256`; the documented keyword is
  `HMAC-SHA-256`.
- **Missing prerequisites.** `CISC-L2-000020` and `CISC-L2-000080` omit
  `feature dot1x`; `CISC-L2-000240` omits `feature interface-vlan`, without
  which `interface vlan` is not available; `CISC-L2-000060` and
  `CISC-L2-000070` omit the `switchport monitor` destination port and the
  `no shut` that activates a SPAN session, which the System Management guide
  requires. `CISC-RT-000730`'s ACL has only a `deny` statement, so its
  implicit deny would drop all traffic on the interface; the crosswalk adds
  `permit ip any any`.
- **Examples that do not meet their own rule.** `CISC-ND-001150` asks for
  FIPS-compliant NTP authentication but configures `md5`; NX-OS 10.5(x) also
  offers `aes128cmac`, which the crosswalk uses. `CISC-ND-000600` relies on
  `password strength-check`, but the Security Configuration Guide defines
  a strong password as eight characters with uppercase and lowercase
  letters and numbers; special characters are allowed, not required, so
  the check does not enforce `CISC-ND-000600`. `CISC-ND-000470` disables
  `feature dhcp`, which `CISC-L2-000130` needs for DHCP snooping, and
  `feature wccp`, which the Nexus 9000 10.5(x) reference does not have; the
  crosswalk disables only Telnet and NX-API. `CISC-RT-000610` mixes LDP synchronization with RSVP refresh
  reduction, and NX-OS 10.5(x) has no RSVP configuration.
- **Port names.** Port numbers replace the fix texts' `tacacs`, `snmp`,
  `snmptrap`, `syslog`, and `ntp` port names in `CISC-RT-000260`,
  `CISC-RT-000390`, and `CISC-RT-000450` (49, 161, 162, 514, and 123),
  because the Nexus 9000 documentation shows only `www` and `bgp` as port
  names in ACL examples.

### Where the version columns come from

- **NX-OS version** is the release of the reference the command entries
  were verified in. Neither Nexus 9000 configuration command reference has
  Command History tables, so no introduction release is given: `10.5(x)`
  means every entry in the cell is in the Release 10.5(x) reference, and
  `10.5(x); 9.3(x) for ...` names the entries found only in the Release
  9.3(x) reference (14 rows, all for `aaa accounting default`,
  `logging ip access-list cache entries`, or `snmp-server host`; the first
  two are also described in the 10.5(x) Security Configuration Guide). A
  dash means the row has no NX-OS command (9 rows). Two
  configuration guide notes do date features: OSPFv2 HMAC-SHA
  authentication is supported from 7.0(3)I3(1) (Unicast Routing guide), and
  any supported SSH MAC can be configured from 10.4(2)F (Security guide).
- **FortiSwitchOS version** follows Chapter 33: the "First listed
  (FortiSwitchOS)" entry of the Chapter 11 feature that the setting uses,
  with the feature name in parentheses, or **Not in the feature matrix
  (8.0.0 CLI Reference)** for a setting the FortiSwitchOS feature matrices
  do not list. Reused rows carry Chapter 33's value. A dash means the row
  has no FortiSwitchOS command.

### Prerequisites

A FortiSwitch setting often meets its requirement only if something else
is already in place. A **prerequisite** is anything that must exist or be
configured *before* a row's FortiSwitch setting can meet the requirement:
an external server (RADIUS, syslog, NTP, SNMP manager, SFTP), a certificate,
an object on the switch that the setting refers to (a user group, a VLAN, a
management interface, binding entries, routing neighbors), a license, a
model that supports the feature, or a managing FortiGate. Settings that the
row's own command already creates (a loopback interface, a prefix list) are
not listed again. The prerequisites cover **the FortiSwitch side only**;
the NX-OS column has its own needs (for example `feature` commands, the
management VRF, and the AAA server group), which the NX-OS command cells
include where a rule needs them.

The 15 prerequisites are Chapter 33's, with the same IDs, wording,
and commands, so that the two crosswalks agree; no Chapter 37 row needs one
that Chapter 33 lacks. They are listed once in *FortiSwitch prerequisites*,
and the crosswalk and unmatched-requirement tables name the IDs each row
needs in their **FortiSwitch prerequisites** column. The 120
rows that reuse Chapter 33's FortiSwitch side also reuse its prerequisite
IDs (the build script checks that they match Chapter 33), and so do the
unmatched requirements, which come from Chapter 33. The other rows follow
Chapter 33's rules. A dash means the setting needs nothing beyond the
switch itself, and Not supported and Not applicable rows always show a
dash. Two prerequisites depend on the exact switch: **licensing** (P8)
comes from the "Layer 3: Requires Advanced Features License" section of the
*Feature Matrix for FortiSwitchOS 8.0.0*, and **model support** (P9) from
its model-series columns. Check the matrix for your release and model
before you plan on a feature. A row carries P9 when a feature it uses shows
"--" (not supported) in at least one model-series column of the 8.0.0
feature matrix PDF; the matrix's first column is the GUI column, and a "--"
there only means the feature has no GUI, so it does not count. During an
assessment, check a row's prerequisites before its
setting: a correctly configured setting with a missing prerequisite (an
unreachable RADIUS server, an unlicensed routing protocol) does not meet
the requirement, and the missing prerequisite is the finding.

### Alignment categories

Every row has one of six categories:

| Category | Meaning |
| --- | --- |
| Same requirement | Chapter 11 maps a FortiSwitch feature to the same SRG ID, and the feature meets the requirement. |
| Equivalent setting | A FortiSwitch setting meets the requirement, although Chapter 11 did not map it to this SRG ID. |
| Partial | FortiSwitch meets part of the requirement. The setting column says what is missing. |
| Not supported | FortiSwitch has no such capability (for example MPLS, VPLS, or UDLD), so it cannot meet the rule or take the role the rule secures. |
| Not applicable | The rule targets a component, role, or protocol that FortiSwitch does not have or take (a PIM rendezvous point, MSDP, VTP), so there is nothing to secure. |
| By procedure | The requirement is met by a process rather than a setting, on both platforms (running a supported release, address planning). |

**Partial**, **Not supported**, and **Not applicable** take precedence over
**Same requirement**: where Chapter 11 maps the same SRG ID but the
FortiSwitch feature does not fully meet it, the row is Partial and its
setting cell notes that Chapter 11 maps the requirement.

### Nexus data center features and their FortiSwitch counterparts

Nexus switches are usually data center switches, and several of their
features have no direct FortiSwitch counterpart. None of them has an
NX-OS STIG rule of its own, but each changes how the rules are applied:

- **vPC and MCLAG.** A Nexus vPC pair presents two switches as one to
  downstream devices, with a peer link and a peer-keepalive link. FortiSwitch
  does the same with an **MCLAG** pair (`config switch trunk; edit <TRUNK>;
  set mclag enable; end`), which Chapter 11 maps to the Layer 2 Switch
  SRG's alternate path requirement. Apply the port guards, storm control,
  and VLAN rules to both members of a vPC or MCLAG pair, and keep the peer
  links on dedicated, trusted ports.
- **FabricPath.** FabricPath, the older Cisco layer 2 multipath fabric
  (the 10.5(x) reference still lists `switchport mode fabricpath`), has no
  FortiSwitch equivalent; FortiSwitch uses MSTP and MCLAG.
- **VXLAN EVPN.** NX-OS VXLAN EVPN fabrics use an NVE interface and BGP
  EVPN. FortiSwitch has hardware VXLAN (7.4.2 and later) and BGP EVPN
  (7.4.0 and later, Advanced Features license), which Chapter 11 maps to
  the Layer 2 Switch SRG's traffic separation requirement
  (`SRG-NET-000715-L2S-000120`, in the second table because no NX-OS rule
  cites it). DHCP snooping, ARP suppression, and IGMP snooping work over
  FortiSwitch VXLAN from the releases Chapter 11 lists. The BGP rules
  (`CISC-RT-000470` to `CISC-RT-000580`) apply to the EVPN peerings on both
  platforms.
- **CoPP and DoS protection.** Every Nexus 9000 runs a CoPP policy, chosen
  at setup and changed with `copp profile`; it cannot be disabled.
  FortiSwitchOS has no configurable control plane policing; its hardware
  DoS checks (`switch security-feature`) and storm control are the nearest
  settings, so `CISC-ND-001220` and `CISC-RT-000120` are Partial.
- **The `feature` model and the management VRF.** NX-OS enables protocols
  with `feature` commands, so disabling a feature (`no feature telnet`)
  removes the whole service, and `mgmt0` sits in the management VRF:
  syslog and NTP servers reached through `mgmt0` need the `use-vrf` option
  of `logging server` and `ntp server`. FortiSwitchOS has no feature switches; a
  service is limited by `allowaccess` on each interface, and management can
  use a dedicated `mgmt` port or an SVI.

## Design Considerations

- **Use the NX-OS rules as the checklist, but record against the SRG.** In
  a mixed estate the NX-OS rules give one list of what to check on every
  switch. For a FortiSwitch, the finding goes on the SRG-based checklist
  under the SRG ID in the table, with the alignment category and the
  FortiSwitch evidence.
- **Use one checklist for Catalyst, Nexus, and FortiSwitch where you can.**
  The FortiSwitch side of the shared rules is identical in Chapters 33 and
  37, so one FortiSwitch result can be recorded against either Cisco
  package. Keep the rules that only one Cisco package has, and the second
  table of each chapter, on the FortiSwitch checklist.
- **Decide each switch's role first.** The N-RTR rules depend on the role:
  perimeter rules apply only at the enclave boundary, PE and P rules only to
  an MPLS provider switch, and multicast rules only where the switch routes
  multicast. A FortiSwitch cannot be an MPLS PE or P switch, and should
  rarely be the perimeter device (Chapter 30 covers FortiGate).
- **Use the same organization-defined values on both platforms**: session
  limits, idle timeout, lockout values, log servers, time sources, and
  password policy.
- **Plan for FortiLink-managed mode.** Most FortiSwitches are managed by a
  FortiGate; the FortiSwitch side of each row is then configured under the
  FortiGate's `config switch-controller` tree.
- **Check the licenses.** FortiSwitch OSPF, BGP, IS-IS, VRF, BGP EVPN, and
  multicast routing need the Advanced Features license (Chapter 11).
- **Accept the gaps deliberately.** Record each Partial and Not supported
  row as an open finding with its mitigation, or keep the function on a
  platform that meets the requirement.

## Implementation and Automation

### FortiSwitch prerequisites

What must be in place before the FortiSwitch settings in the crosswalk can
meet their requirements (see *Prerequisites*). The table is Chapter 33's,
unchanged. The commands were verified with the same script as the
crosswalk; entries that are not switch settings are described in words.

[Download the prerequisites as CSV](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/data/volume-172-disa-srgs-and-stigs/37-cisco-nx-os-switch-and-fortiswitch-stig-crosswalk-prerequisites.csv) (15 rows).

| ID | Prerequisite | What it enables | How to put it in place | Source |
| --- | --- | --- | --- | --- |
| P1 | Reachable RADIUS or TACACS+ servers, each with a unique shared secret | Remote administrator authentication, 802.1X and MAB, and RADIUS accounting | An organization RADIUS or TACACS+ service, then `config user radius; edit <RADIUS_1>; set server <RADIUS_1_IP>; set secret <KEY_1>; end` or `config user tacacs+; edit <TACACS_1>; set server <TACACS_1_IP>; set key <KEY_1>; end` | FortiSwitchOS 8.0.0 CLI Reference, `config user radius` and `config user tacacs+`; Chapter 11 rows *RADIUS for administrative authentication* and *TACACS+ for administrative authentication* |
| P2 | User group that lists the authentication servers | The administrator remote group (`remote-group`) and the 802.1X security group (`security-groups`) | `config user group; edit <GROUP>; set member <RADIUS_1> <RADIUS_2>; end` | FortiSwitchOS 8.0.0 CLI Reference, `config user group`, `config system admin`, and `config switch interface` (`port-security`); Chapter 11 rows *802.1X port mode* and *802.1X MAC-based mode* |
| P3 | PKI: the DoD CA certificate on the switch, and a reachable CA enrollment (SCEP) service | Certificate enrollment from the DoD CA and RadSec server certificate validation | `config system certificate ca; edit <DOD_CA>; set ca <CA_CERTIFICATE>; end` | FortiSwitchOS 8.0.0 CLI Reference, `config system certificate ca`, `config system certificate local` (`scep-url`), and `config user radius` (`radsec-server-ca-cert`, `radsec-cert-validate`); Chapter 11 row *802.1X: RadSec (IPv4)* |
| P4 | Central syslog servers that accept reliable (TCP) syslog with TLS | Off-loading logs to two central servers with reliable, encrypted delivery | Two organization log servers, then `config log syslogd setting; set status enable; set server <SYSLOG_SERVER_1>; end` | FortiSwitchOS 8.0.0 CLI Reference, `config log {syslogd, syslogd2, syslogd3} setting` (`mode`, `enc-algorithm`); Chapter 11 row *Reliable syslog* |
| P5 | Authoritative NTP servers and their authentication keys | Synchronized, authenticated time for log time stamps, and key lifetimes for routing protocol keys | Organization NTP servers, then `config system ntp; config ntpserver; edit 1; set server <NTP_SERVER_1>; set authentication enable; set key-id <ID>; set key <KEY>; end; end` | FortiSwitchOS 8.0.0 CLI Reference, `config system ntp`; Chapter 11 row *NTP server (IPv4/IPv6)* |
| P6 | SNMPv3 manager configured with the same user, authentication, and privacy settings | SNMPv3 queries and notifications with SHA-2 authentication and AES privacy | The organization network management system, then `config system snmp user; edit <USER>; set notify-hosts <NMS_IP>; end` | FortiSwitchOS 8.0.0 CLI Reference, `config system snmp user` |
| P7 | A FortiGate managing the switch over FortiLink | The "FortiGate:" commands and the Security Fabric features (NAC, quarantine, centralized syslog collection) | FortiGate: `config system interface; edit <FORTILINK>; set fortilink enable; end` | *Feature Matrix for FortiSwitchOS 8.0.0* (Security Fabric features are available only in managed mode); FortiOS 8.0.1 CLI Reference, `config system interface` |
| P8 | FortiSwitch Advanced Features license | Policy-based routing, VRF, OSPF, RIP, VRRP, BGP, IS-IS, PIM-SSM, and VXLAN BGP EVPN, and router event logs | `execute license add <LICENSE_KEY>`, then check with `execute license status` | *Feature Matrix for FortiSwitchOS 8.0.0*, section "Layer 3: Requires Advanced Features License" and note 19; FortiSwitchOS 8.0.0 CLI Reference notes under `config router ospf`, `config router rip`, `config router route-map`, and `get log eventfilter` |
| P9 | A switch model series that supports the feature | Features the feature matrix marks as not supported on some model series (for example uRPF, IP source guard, dynamic ARP inspection, FIPS-CC mode, and the licensed Layer 3 features) | Check the model series column of the feature matrix for your release; `get system status` shows the model | *Feature Matrix for FortiSwitchOS 8.0.0* (PDF), model-series columns; the first (GUI) column is not a model series |
| P10 | A management interface with an address: the management port or a management SVI on a dedicated VLAN | Restricting management protocols to the management network, and keeping management off the default VLAN | `config system interface; edit <MGMT_SVI>; set interface internal; set vlanid <MGMT_VLAN>; set ip <IP_ADDRESS> <MASK>; end` | FortiSwitchOS 8.0.0 CLI Reference, `config system interface`; Chapter 11 row *SVI* |
| P11 | Routing protocol configured with its neighbors, and matching keys on every peer | Neighbor authentication, TTL security, prefix and AS path filters, and maximum prefixes | `config router bgp; set as <ASN>; set router-id <ROUTER_ID>; config neighbor; edit <PEER_IP>; set remote-as <PEER_ASN>; end; end`, with the same key or key chain configured on each peer | FortiSwitchOS 8.0.0 CLI Reference, `config router bgp`, `config router ospf`, and `config router key-chain` |
| P12 | DHCP snooping enabled on the VLAN | Dynamic ARP inspection, which can be enabled only on a VLAN with DHCP snooping enabled | `config switch vlan; edit <VLAN>; set dhcp-snooping enable; end` | FortiSwitchOS 8.0.0 CLI Reference, `config switch vlan` (note under `arp-inspection`) |
| P13 | The user, native, management, and unused VLANs created on the switch | Per-VLAN settings (DHCP snooping, ARP inspection, IGMP and MLD snooping) and native VLAN assignments | `config switch vlan; edit <VLAN_ID>; set description <VLAN_NAME>; end` | FortiSwitchOS 8.0.0 CLI Reference, `config switch vlan` and `config switch interface` (`native-vlan`, `allowed-vlans`) |
| P14 | IP-to-MAC binding entries for statically addressed hosts | IP source guard on ports with hosts that do not use DHCP | `config switch ip-source-guard; edit <PORT>; config binding-entry; edit 1; set ip <IP_ADDRESS>; set mac <MAC_ADDRESS>; end; end` | FortiSwitchOS 8.0.0 CLI Reference, `config switch ip-source-guard` |
| P15 | An SFTP server and account for configuration backups | The automation stitch that copies the configuration off the switch when it changes | An organization SFTP server; the backup runs `execute backup config sftp <FILE> <SFTP_SERVER> <USER> <PASSWORD>` | FortiSwitchOS 8.0.0 CLI Reference, `execute backup config` and `config system automation-action` |

### The crosswalk table

One row per Cisco NX-OS Switch STIG rule: 42 N-NDM rules, then
22 N-L2S rules, then 78 N-RTR rules. Severity is the Cisco
rule's category. The Requirement column summarizes what the rule requires;
the SRG ID links it to the requirement text. The command columns follow
*Where the commands come from*, the version columns *Where the version
columns come from*, and the prerequisites column *Prerequisites*.

[Download the crosswalk as CSV](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/data/volume-172-disa-srgs-and-stigs/37-cisco-nx-os-switch-and-fortiswitch-stig-crosswalk-crosswalk.csv) (142 rows).

| Cisco rule | Severity | SRG ID | Requirement | Cisco NX-OS command | NX-OS version | FortiSwitch setting | FortiSwitchOS command | FortiSwitchOS version | FortiSwitch prerequisites | Alignment |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| N-NDM `CISC-ND-000010` | CAT II | `SRG-APP-000001-NDM-000200` | Limit concurrent management sessions to an organization-defined number | `line vty; session-limit <MAX_SESSIONS>` | 10.5(x) | Concurrent administrator login control: stops one administrator name from logging in from two IP addresses at once; FortiSwitchOS has no setting for a maximum number of management sessions | `config system global; set admin-concurrent enable; end` | Not in the feature matrix (8.0.0 CLI Reference) | — | Partial |
| N-NDM `CISC-ND-000090` | CAT II | `SRG-APP-000026-NDM-000208` | Audit the creation of accounts | `radius-server host <RADIUS_1_IP> key <KEY>; radius-server host <RADIUS_2_IP> key <KEY>; aaa group server radius RADIUS_SERVERS; server <RADIUS_1_IP>; server <RADIUS_2_IP>; exit; aaa accounting default group RADIUS_SERVERS` | 10.5(x); 9.3(x) for `aaa accounting default` | System event logging, which records configuration changes such as new administrator accounts; send the logs off the switch (`CISC-ND-001450`) | `config log eventfilter; set event enable; set system enable; end` | Not in the feature matrix (8.0.0 CLI Reference) | — | Equivalent setting |
| N-NDM `CISC-ND-000100` | CAT II | `SRG-APP-000027-NDM-000209` | Audit the modification of accounts | `radius-server host <RADIUS_1_IP> key <KEY>; radius-server host <RADIUS_2_IP> key <KEY>; aaa group server radius RADIUS_SERVERS; server <RADIUS_1_IP>; server <RADIUS_2_IP>; exit; aaa accounting default group RADIUS_SERVERS` | 10.5(x); 9.3(x) for `aaa accounting default` | System event logging of configuration changes to administrator accounts | `config log eventfilter; set event enable; set system enable; end` | Not in the feature matrix (8.0.0 CLI Reference) | — | Equivalent setting |
| N-NDM `CISC-ND-000110` | CAT II | `SRG-APP-000028-NDM-000210` | Audit the disabling of accounts | `radius-server host <RADIUS_1_IP> key <KEY>; radius-server host <RADIUS_2_IP> key <KEY>; aaa group server radius RADIUS_SERVERS; server <RADIUS_1_IP>; server <RADIUS_2_IP>; exit; aaa accounting default group RADIUS_SERVERS` | 10.5(x); 9.3(x) for `aaa accounting default` | System event logging of configuration changes to administrator accounts | `config log eventfilter; set event enable; set system enable; end` | Not in the feature matrix (8.0.0 CLI Reference) | — | Equivalent setting |
| N-NDM `CISC-ND-000120` | CAT II | `SRG-APP-000029-NDM-000211` | Audit the removal of accounts | `radius-server host <RADIUS_1_IP> key <KEY>; radius-server host <RADIUS_2_IP> key <KEY>; aaa group server radius RADIUS_SERVERS; server <RADIUS_1_IP>; server <RADIUS_2_IP>; exit; aaa accounting default group RADIUS_SERVERS` | 10.5(x); 9.3(x) for `aaa accounting default` | System event logging of configuration changes to administrator accounts | `config log eventfilter; set event enable; set system enable; end` | Not in the feature matrix (8.0.0 CLI Reference) | — | Equivalent setting |
| N-NDM `CISC-ND-000140` | CAT II | `SRG-APP-000038-NDM-000213` | Allow management access only from authorized networks and over approved protocols | `ip access-list MGMT_NET; permit ip <MGMT_PREFIX> any; deny ip any any log; exit; line vty; access-class MGMT_NET in` `interface mgmt0; ip access-group MGMT_NET in` | 10.5(x) | Trusted hosts on each administrator account, and management protocols allowed only on a dedicated management interface | `config system admin; edit <ADMIN>; set trusthost1 <MGMT_SUBNET> <MASK>; end` `config system interface; edit <MGMT_SVI>; set allowaccess https ssh; end` | 7.6.4 and later (SVI) | P10 | Same requirement |
| N-NDM `CISC-ND-000150` | CAT II | `SRG-APP-000065-NDM-000214` | Disconnect the session after three consecutive failed logons | `ssh login-attempts 3` | 10.5(x) | Administrator lockout after three failed attempts (the FortiSwitchOS default threshold); the account is then locked for the lockout duration, which is stricter than the disconnect the NX-OS rule asks for (the IOS XE rule in Chapter 33 asks for a 15-minute lockout) | `config system global; set admin-lockout-threshold 3; set admin-lockout-duration 900; end` | Not in the feature matrix (8.0.0 CLI Reference) | — | Equivalent setting |
| N-NDM `CISC-ND-000160` | CAT II | `SRG-APP-000068-NDM-000215` | Show the DoD Notice and Consent Banner before logon | `banner motd #<DOD_NOTICE_AND_CONSENT_BANNER_TEXT>#` | 10.5(x) | Pre-login banner | `config system global; set pre-login-banner "<DOD_NOTICE_AND_CONSENT_BANNER_TEXT>"; end` | Not in the feature matrix (8.0.0 CLI Reference) | — | Equivalent setting |
| N-NDM `CISC-ND-000210` | CAT II | `SRG-APP-000080-NDM-000220` | Protect against an administrator falsely denying actions (non-repudiation) | `radius-server host <RADIUS_1_IP> key <KEY>; radius-server host <RADIUS_2_IP> key <KEY>; aaa group server radius RADIUS_SERVERS; server <RADIUS_1_IP>; server <RADIUS_2_IP>; exit; aaa accounting default group RADIUS_SERVERS` | 10.5(x); 9.3(x) for `aaa accounting default` | System and user event logging, which records each configuration change and logon with the administrator account that made it | `config log eventfilter; set event enable; set system enable; set user enable; end` | Not in the feature matrix (8.0.0 CLI Reference) | — | Equivalent setting |
| N-NDM `CISC-ND-000290` | CAT II | `SRG-APP-000097-NDM-000227` | Record where each audited event occurred | `logging ip access-list cache entries <ENTRIES>` `ip access-list <ACL_NAME>; deny ip any any log` | 10.5(x); 9.3(x) for `logging ip access-list cache entries` | Event logs identify the switch by its host name; ACL matches can be counted but not logged, so there is no equivalent of the NX-OS ACL `log` keyword and ACL log cache | `config system global; set hostname <HOSTNAME>; end` `config switch acl ingress; edit <ID>; config action; set count enable; end; end` | Not in the feature matrix (8.0.0 CLI Reference) | — | Partial |
| N-NDM `CISC-ND-000330` | CAT II | `SRG-APP-000101-NDM-000231` | Log the full text of privileged commands | `radius-server host <RADIUS_1_IP> key <KEY>; radius-server host <RADIUS_2_IP> key <KEY>; aaa group server radius RADIUS_SERVERS; server <RADIUS_1_IP>; server <RADIUS_2_IP>; exit; aaa accounting default group RADIUS_SERVERS` | 10.5(x); 9.3(x) for `aaa accounting default` | System event logging records configuration changes; the 8.0.0 CLI Reference documents no setting that logs the full text of every command entered | `config log eventfilter; set event enable; set system enable; end` | Not in the feature matrix (8.0.0 CLI Reference) | — | Partial |
| N-NDM `CISC-ND-000470` | CAT I | `SRG-APP-000142-NDM-000245` | Disable unnecessary and nonsecure functions and services | `no feature telnet; no feature nxapi` | 10.5(x) | Allow only HTTPS and SSH for management (no HTTP or Telnet), and keep SSH version 1 compatibility off | `config system interface; edit <MGMT>; set allowaccess https ssh; end` `config system global; set admin-ssh-v1 disable; end` | 7.0.0 or earlier (HTTP REST APIs for configuration and monitoring) | P10 | Same requirement |
| N-NDM `CISC-ND-000490` | CAT II | `SRG-APP-000148-NDM-000346` | Keep only one local account, as the account of last resort | `username <LOCAL_ADMIN> password <PASSWORD> role <ROLE>; aaa authentication login default group RADIUS_SERVERS; aaa authentication login default fallback error local` | 10.5(x) | One local administrator account, with all others authenticated remotely; local logons can be refused while the authentication server is reachable | `config system global; set admin-restrict-local enable; end` | Not in the feature matrix (8.0.0 CLI Reference) | P1 | Equivalent setting |
| N-NDM `CISC-ND-000530` | CAT II | `SRG-APP-000156-NDM-000250` | Use replay-resistant authentication for privileged network access | `ssh macs hmac-sha2-256; ssh macs hmac-sha2-512` | 10.5(x) | Management only over SSH and HTTPS, whose per-session keys and message authentication resist replay, with strong cryptography enforced | `config system interface; edit <MGMT>; set allowaccess https ssh; end` `config system global; set strong-crypto enable; end` | 7.0.0 or earlier (HTTP REST APIs for configuration and monitoring) | P10 | Equivalent setting |
| N-NDM `CISC-ND-000570` | CAT II | `SRG-APP-000166-NDM-000254` | Require at least one uppercase character in passwords | `password strength-check` | 10.5(x) | Password policy | `config system password-policy; set status enable; set min-upper-case-letter 1; end` | Not in the feature matrix (8.0.0 CLI Reference) | — | Equivalent setting |
| N-NDM `CISC-ND-000580` | CAT II | `SRG-APP-000167-NDM-000255` | Require at least one lowercase character in passwords | `password strength-check` | 10.5(x) | Password policy | `config system password-policy; set status enable; set min-lower-case-letter 1; end` | Not in the feature matrix (8.0.0 CLI Reference) | — | Equivalent setting |
| N-NDM `CISC-ND-000590` | CAT II | `SRG-APP-000168-NDM-000256` | Require at least one numeric character in passwords | `password strength-check` | 10.5(x) | Password policy | `config system password-policy; set status enable; set min-number 1; end` | Not in the feature matrix (8.0.0 CLI Reference) | — | Equivalent setting |
| N-NDM `CISC-ND-000600` | CAT II | `SRG-APP-000169-NDM-000257` | Require at least one special character in passwords | `password strength-check` | 10.5(x) | Password policy | `config system password-policy; set status enable; set min-non-alphanumeric 1; end` | Not in the feature matrix (8.0.0 CLI Reference) | — | Equivalent setting |
| N-NDM `CISC-ND-000720` | CAT I | `SRG-APP-000190-NDM-000267` | End management sessions after five minutes of inactivity | `line console; exec-timeout 5; exit; line vty; exec-timeout 5` | 10.5(x) | Administrator idle timeout; the FortiSwitchOS default is already 5 minutes | `config system global; set admintimeout 5; end` | Not in the feature matrix (8.0.0 CLI Reference) | — | Equivalent setting |
| N-NDM `CISC-ND-000880` | CAT II | `SRG-APP-000319-NDM-000283` | Audit the enabling of accounts | `radius-server host <RADIUS_1_IP> key <KEY>; radius-server host <RADIUS_2_IP> key <KEY>; aaa group server radius RADIUS_SERVERS; server <RADIUS_1_IP>; server <RADIUS_2_IP>; exit; aaa accounting default group RADIUS_SERVERS` | 10.5(x); 9.3(x) for `aaa accounting default` | System event logging of configuration changes to administrator accounts | `config log eventfilter; set event enable; set system enable; end` | Not in the feature matrix (8.0.0 CLI Reference) | — | Equivalent setting |
| N-NDM `CISC-ND-000940` | CAT II | `SRG-APP-000343-NDM-000289` | Audit the execution of privileged functions | `radius-server host <RADIUS_1_IP> key <KEY>; radius-server host <RADIUS_2_IP> key <KEY>; aaa group server radius RADIUS_SERVERS; server <RADIUS_1_IP>; server <RADIUS_2_IP>; exit; aaa accounting default group RADIUS_SERVERS` | 10.5(x); 9.3(x) for `aaa accounting default` | System event logging of the configuration changes administrators make | `config log eventfilter; set event enable; set system enable; end` | Not in the feature matrix (8.0.0 CLI Reference) | — | Equivalent setting |
| N-NDM `CISC-ND-000980` | CAT II | `SRG-APP-000357-NDM-000293` | Allocate local audit record storage as the organization requires | `logging logfile <LOGFILE_NAME> 6 size <BYTES>` | 10.5(x) | Local event log on flash, overwriting the oldest records, with fill-level warnings | `config log disk setting; set status enable; set diskfull overwrite; set full-first-warning-threshold 75; end` | 7.2.0 and later (Save event log in flash memory) | P9 | Same requirement |
| N-NDM `CISC-ND-001000` | CAT II | `SRG-APP-000360-NDM-000295` | Alert on audit failures | `logging server <SYSLOG_SERVER_1> 2` | 10.5(x) | The log disk raises warnings at three fill levels; there is no dedicated alert when syslog delivery fails | `config log disk setting; set full-first-warning-threshold <PERCENT>; set full-second-warning-threshold <PERCENT>; set full-final-warning-threshold <PERCENT>; end` | 7.2.0 and later (Save event log in flash memory) | P9 | Partial |
| N-NDM `CISC-ND-001030` | CAT II | `SRG-APP-000373-NDM-000298` | Synchronize the clock with two redundant authoritative time sources | `feature ntp; ntp server <NTP_SERVER_1>; ntp server <NTP_SERVER_2>` | 10.5(x) | Two NTP servers (the rule's SRG ID is not in NDM SRG V5R5; Chapter 11 maps NTP to the current requirement `SRG-APP-000920-NDM-000320`) | `config system ntp; set ntpsync enable; config ntpserver; edit 1; set server <NTP_SERVER_1>; next; edit 2; set server <NTP_SERVER_2>; end; end` | 7.6.2 and later (NTP server (IPv4/IPv6)) | P5 | Equivalent setting |
| N-NDM `CISC-ND-001050` | CAT II | `SRG-APP-000374-NDM-000299` | Record time stamps that map to UTC or GMT | `clock timezone <ZONE> <HOURS> <MINUTES>` | 10.5(x) | Time zone, with the clock synchronized by NTP (Chapter 11 maps PTP and NTP clock synchronization to this requirement) | `config system global; set timezone <TIMEZONE_NUMBER>; end` `config system ntp; set ntpsync enable; end` | Not in the feature matrix (8.0.0 CLI Reference) | P5 | Same requirement |
| N-NDM `CISC-ND-001130` | CAT II | `SRG-APP-000395-NDM-000310` | Authenticate SNMP messages with a FIPS-validated HMAC | `snmp-server user NETOPS auth sha <AUTH_PASSWORD> priv aes-128 <PRIV_PASSWORD>; snmp-server host <NMS_IP> traps version 3 priv NETOPS` | 10.5(x); 9.3(x) for `snmp-server host` | SNMPv3 user with authentication and privacy, SHA-256 authentication | `config system snmp user; edit <USER>; set security-level auth-priv; set auth-proto sha256; set auth-pwd <AUTH_PASSWORD>; end` | 7.0.0 or earlier (Support for switch SNMP OID) | P6 | Same requirement |
| N-NDM `CISC-ND-001140` | CAT II | `SRG-APP-000395-NDM-000310` | Encrypt SNMP messages with a FIPS-approved algorithm | `snmp-server user NETOPS auth sha <AUTH_PASSWORD> priv aes-128 <PRIV_PASSWORD>; snmp-server host <NMS_IP> traps version 3 priv NETOPS` | 10.5(x); 9.3(x) for `snmp-server host` | SNMPv3 user with authentication and privacy, AES-256 privacy | `config system snmp user; edit <USER>; set security-level auth-priv; set priv-proto aes256; set priv-pwd <PRIV_PASSWORD>; end` | 7.0.0 or earlier (Support for switch SNMP OID) | P6 | Same requirement |
| N-NDM `CISC-ND-001150` | CAT II | `SRG-APP-000395-NDM-000347` | Authenticate NTP sources with FIPS-compliant algorithms | `feature ntp; ntp authentication-key 1 aes128cmac <KEY>; ntp trusted-key 1; ntp authenticate; ntp server <NTP_SERVER> key 1` | 10.5(x) | NTP authentication; FortiSwitchOS NTPv4 uses a SHA-1 keyed digest (MD5 with NTPv3), not a FIPS-approved MAC such as the AES-128-CMAC that NX-OS offers (Chapter 11 maps NTP to this requirement) | `config system ntp; set ntpsync enable; set authentication enable; config ntpserver; edit 1; set server <NTP_IP>; set authentication enable; set key-id <ID>; set key <KEY>; end; end` | 7.6.2 and later (NTP server (IPv4/IPv6)) | P5 | Partial |
| N-NDM `CISC-ND-001200` | CAT I | `SRG-APP-000411-NDM-000330` | Protect remote maintenance sessions with a FIPS-validated HMAC | `ssh macs hmac-sha2-256; ssh macs hmac-sha2-512` | 10.5(x) | FIPS-CC mode and strong cryptography for SSH and HTTPS; FortiSwitchOS has no per-algorithm SSH MAC or cipher list | `config system security; set mode fips-cc; end` `config system global; set strong-crypto enable; end` | 7.6.4 and later (FIPS 140-3 (Level 1) and CC support) | P9 | Same requirement |
| N-NDM `CISC-ND-001210` | CAT I | `SRG-APP-000412-NDM-000331` | Encrypt remote maintenance sessions | `ssh ciphers aes128-ctr; ssh ciphers aes256-ctr` | 10.5(x) | FIPS-CC mode, strong cryptography, and TLS 1.2 for HTTPS (TLS 1.3 is not supported in FIPS-CC mode) | `config system security; set mode fips-cc; end` `config system global; set strong-crypto enable; end` `config system web; set https-ssl-versions tlsv1-2; end` | 7.6.4 and later (FIPS 140-3 (Level 1) and CC support) | P9 | Same requirement |
| N-NDM `CISC-ND-001220` | CAT II | `SRG-APP-000435-NDM-000315` | Protect against known denial-of-service attacks with organization-defined safeguards | `copp profile strict` | 10.5(x) | Hardware DoS checks (`switch security-feature`; the available checks depend on the model) and storm control; FortiSwitchOS has no configurable control plane policing like NX-OS CoPP | `config switch security-feature; set sip-eq-dip enable; set ip-pod enable; set icmp-frag enable; end` `config switch physical-port; edit <PORT>; set storm-control-mode override; config storm-control; set broadcast enable; set rate <PPS>; end; end` | Not in the feature matrix (8.0.0 CLI Reference) | — | Partial |
| N-NDM `CISC-ND-001240` | CAT II | `SRG-APP-000495-NDM-000318` | Log the modification of administrator privileges | `radius-server host <RADIUS_1_IP> key <KEY>; radius-server host <RADIUS_2_IP> key <KEY>; aaa group server radius RADIUS_SERVERS; server <RADIUS_1_IP>; server <RADIUS_2_IP>; exit; aaa accounting default group RADIUS_SERVERS` | 10.5(x); 9.3(x) for `aaa accounting default` | System event logging of configuration changes to administrator accounts and access profiles | `config log eventfilter; set event enable; set system enable; end` | Not in the feature matrix (8.0.0 CLI Reference) | — | Equivalent setting |
| N-NDM `CISC-ND-001250` | CAT II | `SRG-APP-000499-NDM-000319` | Log the deletion of administrator privileges | `radius-server host <RADIUS_1_IP> key <KEY>; radius-server host <RADIUS_2_IP> key <KEY>; aaa group server radius RADIUS_SERVERS; server <RADIUS_1_IP>; server <RADIUS_2_IP>; exit; aaa accounting default group RADIUS_SERVERS` | 10.5(x); 9.3(x) for `aaa accounting default` | System event logging of configuration changes to administrator accounts and access profiles | `config log eventfilter; set event enable; set system enable; end` | Not in the feature matrix (8.0.0 CLI Reference) | — | Equivalent setting |
| N-NDM `CISC-ND-001260` | CAT II | `SRG-APP-000503-NDM-000320` | Log successful and unsuccessful logons | `logging level authpriv 6; logging logfile <LOGFILE_NAME> 6` | 10.5(x) | System and user event logging, which records administrator logons | `config log eventfilter; set event enable; set system enable; set user enable; end` | Not in the feature matrix (8.0.0 CLI Reference) | — | Equivalent setting |
| N-NDM `CISC-ND-001270` | CAT II | `SRG-APP-000504-NDM-000321` | Log privileged activities | `radius-server host <RADIUS_1_IP> key <KEY>; radius-server host <RADIUS_2_IP> key <KEY>; aaa group server radius RADIUS_SERVERS; server <RADIUS_1_IP>; server <RADIUS_2_IP>; exit; aaa accounting default group RADIUS_SERVERS` | 10.5(x); 9.3(x) for `aaa accounting default` | System event logging of configuration changes | `config log eventfilter; set event enable; set system enable; end` | Not in the feature matrix (8.0.0 CLI Reference) | — | Equivalent setting |
| N-NDM `CISC-ND-001280` | CAT II | `SRG-APP-000505-NDM-000322` | Record the start and end time of each administrator session | `logging level authpriv 6` | 10.5(x) | System and user event logging, which records administrator logins and logouts with time stamps | `config log eventfilter; set event enable; set system enable; set user enable; end` | Not in the feature matrix (8.0.0 CLI Reference) | — | Equivalent setting |
| N-NDM `CISC-ND-001310` | CAT II | `SRG-APP-000515-NDM-000325` | Off-load log records to a system other than the switch | `logging server <SYSLOG_SERVER> 6` | 10.5(x) | Reliable (TCP), encrypted syslog to a central server | `config log syslogd setting; set status enable; set server <SYSLOG_SERVER>; set mode reliable; set enc-algorithm high; end` | 7.0.0 or earlier (Reliable syslog) | P4 | Same requirement |
| N-NDM `CISC-ND-001370` | CAT I | `SRG-APP-000516-NDM-000336` | Use at least two authentication servers for administrator logons | `radius-server host <RADIUS_1_IP> key <KEY>; radius-server host <RADIUS_2_IP> key <KEY>; aaa group server radius RADIUS_SERVERS; server <RADIUS_1_IP>; server <RADIUS_2_IP>; exit; aaa authentication login default group RADIUS_SERVERS; aaa authentication login console group RADIUS_SERVERS` | 10.5(x) | Two RADIUS (or TACACS+) server entries in the group that administrator accounts authenticate against; a FortiSwitchOS RADIUS entry holds one server, so define two | `config user radius; edit <RADIUS_1>; set server <RADIUS_1_IP>; set secret <KEY_1>; next; edit <RADIUS_2>; set server <RADIUS_2_IP>; set secret <KEY_2>; end` `config user group; edit <ADMIN_GROUP>; set member <RADIUS_1> <RADIUS_2>; end` `config system admin; edit <ADMIN>; set remote-auth enable; set remote-group <ADMIN_GROUP>; set wildcard enable; end` | 7.2.0 and later (RADIUS for administrative authentication) | P1, P2 | Same requirement |
| N-NDM `CISC-ND-001410` | CAT II | `SRG-APP-000516-NDM-000340` | Back up the configuration whenever it changes | `event manager applet BACKUP_CONFIG; event syslog pattern "SYSLOG_CONFIG_I"; action 1.0 cli copy startup-config scp://<USER>@<SCP_SERVER>/<FILE_NAME>; action 2.0 syslog priority informational msg "Configuration backup was executed"` | 10.5(x) | Automation stitch: a configuration-change trigger runs a CLI script that copies the configuration to an SFTP server (the script holds the SFTP credential); local revisions are also kept at logout | `config system automation-trigger; edit <TRIGGER>; set trigger-type event-based; set event-type config-change; end` `config system automation-action; edit <ACTION>; set action-type cli-script; set script "execute backup config sftp <FILE> <SFTP_SERVER> <USER> <PASSWORD>"; end` `config system automation-stitch; edit <STITCH>; set trigger <TRIGGER>; set action <ACTION>; end` `config system global; set revision-backup-on-logout enable; end` | 7.2.0 and later (Automation stitches) | P15 | Same requirement |
| N-NDM `CISC-ND-001440` | CAT II | `SRG-APP-000516-NDM-000344` | Obtain public key certificates from an approved (DoD) certificate authority | `crypto ca trustpoint <DOD_TRUSTPOINT>; crypto ca authenticate <DOD_TRUSTPOINT>; crypto ca enroll <DOD_TRUSTPOINT>` | 10.5(x) | SCEP enrollment of the switch certificate from the DoD CA | `config system certificate local; edit <CERT_NAME>; set scep-url <DOD_CA_SCEP_URL>; end` | Not in the feature matrix (8.0.0 CLI Reference) | P3 | Equivalent setting |
| N-NDM `CISC-ND-001450` | CAT I | `SRG-APP-000516-NDM-000350` | Send logs to at least two central log servers | `logging server <SYSLOG_SERVER_1> 6; logging server <SYSLOG_SERVER_2> 6` | 10.5(x) | Reliable (TCP), encrypted syslog to two of the three syslog destinations | `config log syslogd setting; set status enable; set server <SYSLOG_SERVER_1>; set mode reliable; set enc-algorithm high; end` `config log syslogd2 setting; set status enable; set server <SYSLOG_SERVER_2>; set mode reliable; set enc-algorithm high; end` | 7.0.0 or earlier (Reliable syslog) | P4 | Same requirement |
| N-NDM `CISC-ND-001470` | CAT I | `SRG-APP-000516-NDM-000351` | Run a software release the vendor still supports | `show version` | 10.5(x) | Run a FortiSwitchOS release Fortinet supports and check the running version (the rule's SRG ID is not in NDM SRG V5R5; Chapter 11 maps the current requirement `SRG-APP-001035-NDM-000340`) | `get system status` | Not in the feature matrix (8.0.0 CLI Reference) | — | By procedure |
| N-L2S `CISC-L2-000020` | CAT I | `SRG-NET-000148-L2S-000015` | Identify every endpoint before it connects | `feature dot1x; radius-server host <RADIUS_1_IP> key <KEY>; radius-server host <RADIUS_2_IP> key <KEY>; aaa group server radius RADIUS_GROUP; server <RADIUS_1_IP>; server <RADIUS_2_IP>; exit; aaa authentication dot1x default group RADIUS_GROUP; interface ethernet <HOST_PORTS>; dot1x port-control auto; dot1x host-mode single-host; dot1x mac-auth-bypass` | 10.5(x) | 802.1X with MAC authentication bypass on host ports, against a RADIUS server group | `config switch interface; edit <HOST_PORT>; config port-security; set port-security-mode 802.1X-mac-based; set mac-auth-bypass enable; end; set security-groups <GROUP>; end` `config user group; edit <GROUP>; set member <RADIUS_1> <RADIUS_2>; end` | 7.0.0 or earlier (802.1X MAC-based mode) | P1, P2 | Same requirement |
| N-L2S `CISC-L2-000030` | CAT II | `SRG-NET-000168-L2S-000019` | Authenticate VTP messages with the strongest available hash | `feature vtp; vtp password <PASSWORD>` | 10.5(x) | FortiSwitch does not run VTP; it only floods Cisco VTP frames when `flood-vtp` is enabled (disabled by default) | `config switch global; set flood-vtp disable; end` | — | — | Not applicable |
| N-L2S `CISC-L2-000060` | CAT II | `SRG-NET-000331-L2S-000001` | Let authorized users select a user session to capture | `interface ethernet <DEST_PORT>; switchport; switchport monitor; exit; monitor session 1; source interface ethernet <SOURCE_PORT> both; destination interface ethernet <DEST_PORT>; exit; no monitor session 1 shut` | 10.5(x) | Port mirroring (SPAN) of the user's port to a monitoring port (the rule's SRG ID is not in Layer 2 Switch SRG V3R4, which has no current requirement for session capture) | `config switch mirror; edit <SESSION>; set mode SPAN; set dst <MONITOR_PORT>; set src-ingress <USER_PORT>; set src-egress <USER_PORT>; set status active; end` | 7.0.0 or earlier (SPAN) | — | Equivalent setting |
| N-L2S `CISC-L2-000070` | CAT II | `SRG-NET-000332-L2S-000002` | Let authorized users view a user session in real time from a separate component | `interface ethernet <DEST_PORT>; switchport; switchport monitor; exit; monitor session 1; source interface ethernet <SOURCE_PORT> both; destination interface ethernet <DEST_PORT>; exit; no monitor session 1 shut` | 10.5(x) | Port mirroring to a monitoring port (SPAN) or, with RSPAN or ERSPAN, to a remote collector (the rule's SRG ID is not in Layer 2 Switch SRG V3R4) | `config switch mirror; edit <SESSION>; set mode SPAN; set dst <MONITOR_PORT>; set src-ingress <USER_PORT>; set src-egress <USER_PORT>; set status active; end` | 7.0.0 or earlier (SPAN) | — | Equivalent setting |
| N-L2S `CISC-L2-000080` | CAT II | `SRG-NET-000343-L2S-000016` | Authenticate every endpoint before it connects | `feature dot1x; radius-server host <RADIUS_1_IP> key <KEY>; radius-server host <RADIUS_2_IP> key <KEY>; aaa group server radius RADIUS_GROUP; server <RADIUS_1_IP>; server <RADIUS_2_IP>; exit; aaa authentication dot1x default group RADIUS_GROUP; interface ethernet <HOST_PORTS>; dot1x port-control auto; dot1x host-mode single-host; dot1x mac-auth-bypass` | 10.5(x) | 802.1X port authentication against a RADIUS server group | `config switch interface; edit <HOST_PORT>; config port-security; set port-security-mode 802.1X; end; set security-groups <GROUP>; end` | 7.0.0 or earlier (802.1X port mode) | P1, P2 | Same requirement |
| N-L2S `CISC-L2-000090` | CAT III | `SRG-NET-000362-L2S-000021` | Enable Root Guard on ports facing access switches and hosts | `interface ethernet <ACCESS_PORTS>; spanning-tree guard root` | 10.5(x) | STP root guard | `config switch interface; edit <ACCESS_PORT>; set stp-root-guard enabled; end` | 7.0.0 or earlier (STP root guard) | — | Same requirement |
| N-L2S `CISC-L2-000100` | CAT II | `SRG-NET-000362-L2S-000022` | Enable BPDU Guard on user-facing and untrusted ports | `interface ethernet <HOST_PORTS>; spanning-tree bpduguard enable` | 10.5(x) | STP BPDU guard | `config switch interface; edit <HOST_PORT>; set stp-bpdu-guard enabled; end` | 7.0.0 or earlier (STP BPDU guard) | — | Same requirement |
| N-L2S `CISC-L2-000110` | CAT II | `SRG-NET-000362-L2S-000023` | Enable STP Loop Guard | `spanning-tree loopguard default` | 10.5(x) | STP loop protection, the counterpart of Cisco loop guard; FortiSwitch loop guard (`loop-guard`, the feature Chapter 11 maps) detects loops with its own probe frames and can be added | `config switch interface; edit <PORT>; set stp-loop-protection enabled; set loop-guard enabled; end` | 7.0.0 or earlier (Loop guard) | — | Same requirement |
| N-L2S `CISC-L2-000120` | CAT II | `SRG-NET-000362-L2S-000024` | Enable Unknown Unicast Flood Blocking on host ports | `interface ethernet <HOST_PORTS>; switchport block unicast` | 10.5(x) | Per-port storm control with only unknown unicast enabled and a rate of 0 drops all unknown unicast; the port has one rate for all enabled traffic types, so it cannot also rate-limit broadcast (`CISC-L2-000160`) | `config switch physical-port; edit <HOST_PORT>; set storm-control-mode override; config storm-control; set unknown-unicast enable; set broadcast disable; set unknown-multicast disable; set rate 0; end; end` | 7.0.0 or earlier (Per-port storm control) | — | Partial |
| N-L2S `CISC-L2-000130` | CAT II | `SRG-NET-000362-L2S-000025` | Enable DHCP snooping on all user VLANs | `feature dhcp; ip dhcp snooping; ip dhcp snooping vlan <USER_VLANS>` `interface ethernet <UPLINK>; ip dhcp snooping trust` | 10.5(x) | DHCP snooping per VLAN, with the uplink trusted | `config switch vlan; edit <VLAN>; set dhcp-snooping enable; end` `config switch interface; edit <UPLINK>; set dhcp-snooping trusted; end` | 7.0.0 or earlier (DHCP snooping) | P13 | Same requirement |
| N-L2S `CISC-L2-000140` | CAT II | `SRG-NET-000362-L2S-000026` | Enable IP Source Guard on user-facing and untrusted ports | `interface ethernet <HOST_PORTS>; ip verify source dhcp-snooping-vlan` | 10.5(x) | IP source guard | `config switch interface; edit <HOST_PORT>; set ip-source-guard enable; end` | 7.0.0 or earlier (IP source guard (IPv4)) | P9, P14 | Same requirement |
| N-L2S `CISC-L2-000150` | CAT II | `SRG-NET-000362-L2S-000027` | Enable Dynamic ARP Inspection on all user VLANs | `ip arp inspection vlan <USER_VLANS>` | 10.5(x) | Dynamic ARP inspection per VLAN, with the uplink trusted | `config switch vlan; edit <VLAN>; set arp-inspection enable; end` `config switch interface; edit <UPLINK>; set arp-inspection-trust trusted; end` | 7.0.0 or earlier (Dynamic ARP inspection (IPv4)) | P9, P12, P13 | Same requirement |
| N-L2S `CISC-L2-000160` | CAT III | `SRG-NET-000512-L2S-000001` | Configure storm control on all host-facing ports | `interface ethernet <HOST_PORTS>; storm-control unicast level <PERCENT>; storm-control broadcast level <PERCENT>` | 10.5(x) | Per-port storm control; FortiSwitchOS rates are in packets per second, NX-OS levels in percent of the port bandwidth (or packets per second) | `config switch physical-port; edit <HOST_PORT>; set storm-control-mode override; config storm-control; set broadcast enable; set unknown-unicast enable; set rate <PPS>; end; end` | 7.0.0 or earlier (Per-port storm control) | — | Same requirement |
| N-L2S `CISC-L2-000170` | CAT III | `SRG-NET-000512-L2S-000002` | Enable IGMP or MLD snooping on all VLANs | `ip igmp snooping` | 10.5(x) | IGMP and MLD snooping per VLAN | `config switch vlan; edit <VLAN>; set igmp-snooping enable; set mld-snooping enable; end` | 7.0.0 or earlier (IGMP snooping) | P9, P13 | Same requirement |
| N-L2S `CISC-L2-000190` | CAT II | `SRG-NET-000512-L2S-000004` | Enable UDLD to protect against one-way links | `feature udld` | 10.5(x) | FortiSwitchOS has no UDLD; STP loop protection reduces the effect of a one-way link on a blocking port | `config switch interface; edit <PORT>; set stp-loop-protection enabled; end` | — | — | Not supported |
| N-L2S `CISC-L2-000210` | CAT II | `SRG-NET-000512-L2S-000007` | Put disabled ports in an unused VLAN | `interface ethernet <UNUSED_PORTS>; switchport access vlan <UNUSED_VLAN>; shutdown` `interface ethernet <TRUNK_PORT>; switchport trunk allowed vlan except <UNUSED_VLAN>` | 10.5(x) | Native VLAN set to an unused VLAN, and the port shut down | `config switch interface; edit <UNUSED_PORT>; set native-vlan <UNUSED_VLAN>; end` `config switch physical-port; edit <UNUSED_PORT>; set status down; end` | 7.0.0 or earlier (forced-untagged or force-tagged setting on switch interfaces) | P13 | Equivalent setting |
| N-L2S `CISC-L2-000220` | CAT II | `SRG-NET-000512-L2S-000008` | Keep the default VLAN off host-facing ports | `interface ethernet <HOST_PORTS>; switchport mode access; switchport access vlan <USER_VLAN>` | 10.5(x) | Native VLAN on host ports set to a user VLAN (the FortiSwitchOS default native VLAN is 1) | `config switch interface; edit <HOST_PORT>; set native-vlan <USER_VLAN>; end` | 7.0.0 or earlier (forced-untagged or force-tagged setting on switch interfaces) | P13 | Equivalent setting |
| N-L2S `CISC-L2-000230` | CAT II | `SRG-NET-000512-L2S-000009` | Prune the default VLAN from trunks that do not need it | `interface ethernet <TRUNK_PORT>; switchport trunk allowed vlan except 1,<UNUSED_VLAN>` | 10.5(x) | Allowed VLAN list on tagged ports that leaves out VLAN 1, with a native VLAN other than 1 | `config switch interface; edit <TRUNK_PORT>; set native-vlan <NATIVE_VLAN>; set allowed-vlans <VLANS>; end` | 7.0.0 or earlier (forced-untagged or force-tagged setting on switch interfaces) | P13 | Same requirement |
| N-L2S `CISC-L2-000240` | CAT II | `SRG-NET-000512-L2S-000010` | Keep management traffic off the default VLAN | `feature interface-vlan; interface vlan <MGMT_VLAN>; ip address <IP_PREFIX>` | 10.5(x) | Management switch virtual interface (SVI) on a dedicated management VLAN | `config system interface; edit <MGMT_SVI>; set interface internal; set vlanid <MGMT_VLAN>; set ip <IP_ADDRESS> <MASK>; set allowaccess https ssh; end` | 7.6.4 and later (SVI) | P10, P13 | Equivalent setting |
| N-L2S `CISC-L2-000250` | CAT II | `SRG-NET-000512-L2S-000011` | Configure user-facing and untrusted ports as access ports | `interface ethernet <HOST_PORTS>; switchport mode access` | 10.5(x) | Native VLAN only, with tagged frames discarded | `config switch interface; edit <HOST_PORT>; set native-vlan <USER_VLAN>; set discard-mode all-tagged; end` | 7.0.0 or earlier (forced-untagged or force-tagged setting on switch interfaces) | P13 | Same requirement |
| N-L2S `CISC-L2-000260` | CAT II | `SRG-NET-000512-L2S-000012` | Use a native VLAN other than the default VLAN on 802.1Q trunks | `interface ethernet <TRUNK_PORT>; switchport trunk native vlan <NATIVE_VLAN>` | 10.5(x) | Native VLAN on tagged ports set to a dedicated VLAN other than 1 | `config switch interface; edit <TRUNK_PORT>; set native-vlan <NATIVE_VLAN>; end` | 7.0.0 or earlier (forced-untagged or force-tagged setting on switch interfaces) | P13 | Same requirement |
| N-L2S `CISC-L2-000270` | CAT III | `SRG-NET-000512-L2S-000013` | Assign no access ports to the native VLAN | `interface ethernet <HOST_PORTS>; switchport mode access; switchport access vlan <USER_VLAN>` | 10.5(x) | Host ports use user VLANs, never the native VLAN of the tagged ports | `config switch interface; edit <HOST_PORT>; set native-vlan <USER_VLAN>; end` | 7.0.0 or earlier (forced-untagged or force-tagged setting on switch interfaces) | P13 | Equivalent setting |
| N-RTR `CISC-RT-000010` | CAT II | `SRG-NET-000018-RTR-000001` | Enforce approved information flow control on routed traffic | `ip access-list FILTER_SERVER_TRAFFIC; permit tcp any <PRINT_SERVER_PREFIX> eq 631; permit tcp any <SQL_SERVER_PREFIX> eq 1433; permit icmp any any; deny ip any any; exit; interface ethernet <L3_PORT>; ip access-group FILTER_SERVER_TRAFFIC in` | 10.5(x) | Ingress ACLs on ports and routed interfaces | `config switch acl ingress; edit <ID>; set ingress-interface <PORT>; config classifier; set src-ip-prefix <IP> <MASK>; end; config action; set drop enable; end; end` | 7.0.0 or earlier (ACL (IPv4 ingress)) | — | Same requirement |
| N-RTR `CISC-RT-000020` | CAT II | `SRG-NET-000230-RTR-000001` | Authenticate all control plane (routing) protocol messages | `key chain OSPF_KEY; key 1; key-string <KEY>; exit; exit; interface ethernet <L3_PORT>; ip ospf authentication key-chain OSPF_KEY` `router bgp <ASN>; neighbor <PEER_IP> remote-as <PEER_ASN>; password <KEY>` | 10.5(x) | OSPF MD5 authentication and a TCP MD5 password on BGP neighbors; FortiSwitchOS has no VRRP authentication (Chapter 11 maps VRRP to this requirement and records the gap) | `config router ospf; config interface; edit <INTERFACE>; set authentication md5; config md5-keys; edit 1; set key <KEY>; end; end; end` `config router bgp; config neighbor; edit <PEER_IP>; set password <KEY>; end; end` | 7.0.0 or earlier (OSPF (IPv4/IPv6)) | P8, P9, P11 | Partial |
| N-RTR `CISC-RT-000030` | CAT II | `SRG-NET-000230-RTR-000003` | Use routing protocol keys with lifetimes of no more than 180 days | `key chain OSPF_KEY; key 1; key-string <KEY>; send-lifetime <START_TIME> duration 15552000; accept-lifetime <START_TIME> duration 15552000` | 10.5(x) | Key chains with send and accept lifetimes, used by RIP and IS-IS; OSPF MD5 keys and BGP passwords have no lifetime, so they must be rotated by procedure | `config router key-chain; edit <KEYCHAIN>; config key; edit 1; set key-string <KEY>; set accept-lifetime <START> <END>; set send-lifetime <START> <END>; end; end` | 7.0.0 or earlier (RIP (IPv4/IPv6)) | P5, P8, P9, P11 | Partial |
| N-RTR `CISC-RT-000040` | CAT II | `SRG-NET-000168-RTR-000077` | Use hashed (MD5) rather than plain-text routing protocol authentication | `interface ethernet <L3_PORT>; ip ospf authentication message-digest; ip ospf message-digest-key 1 md5 <KEY>` `router bgp <ASN>; neighbor <PEER_IP> remote-as <PEER_ASN>; password <KEY>` | 10.5(x) | MD5 authentication on OSPF interfaces and a TCP MD5 password on BGP neighbors | `config router ospf; config interface; edit <INTERFACE>; set authentication md5; config md5-keys; edit 1; set key <KEY>; end; end; end` `config router bgp; config neighbor; edit <PEER_IP>; set password <KEY>; end; end` | 7.0.0 or earlier (OSPF (IPv4/IPv6)) | P8, P9, P11 | Equivalent setting |
| N-RTR `CISC-RT-000050` | CAT II | `SRG-NET-000168-RTR-000078` | Authenticate routing protocol messages with a NIST-validated FIPS 198-1 MAC | `key chain OSPF_KEY; key 1; key-string <KEY>; cryptographic-algorithm HMAC-SHA-256; exit; exit; interface ethernet <L3_PORT>; ip ospf authentication key-chain OSPF_KEY` | 10.5(x) | OSPF, RIP, and IS-IS authenticate with MD5 or plain text only, and BGP with a TCP MD5 password; none is a FIPS 198-1 algorithm (Chapter 11 maps these protocols to this requirement and records the MD5 gap) | `config router ospf; config interface; edit <INTERFACE>; set authentication md5; config md5-keys; edit 1; set key <KEY>; end; end; end` | 7.0.0 or earlier (OSPF (IPv4/IPv6)) | P8, P9, P11 | Partial |
| N-RTR `CISC-RT-000060` | CAT III | `SRG-NET-000019-RTR-000007` | Disable inactive Layer 3 interfaces | `interface ethernet <UNUSED_L3_PORTS>; shutdown` | 10.5(x) | Interface administrative status | `config system interface; edit <UNUSED_L3_INTERFACE>; set status down; end` | Not in the feature matrix (8.0.0 CLI Reference) | — | Equivalent setting |
| N-RTR `CISC-RT-000080` | CAT II | `SRG-NET-000131-RTR-000083` | Disable any feature that calls home to the vendor | `callhome; no enable` | 10.5(x) | FortiEdge Cloud (FortiLAN Cloud) connection disabled on a standalone switch | `config system flan-cloud; set status disable; end` | 7.0.0 or earlier (FortiEdge Cloud configuration) | — | Equivalent setting |
| N-RTR `CISC-RT-000120` | CAT II | `SRG-NET-000362-RTR-000110` | Protect the control plane against denial-of-service attacks | `copp profile strict` | 10.5(x) | FortiSwitchOS has no configurable control plane policing; OSPF database overflow protection (the setting Chapter 11 maps) and storm control limit some control-plane load | `config router ospf; set database-overflow enable; set database-overflow-max-external-lsa <LSAS>; end` | 7.0.0 or earlier (OSPF database overflow protection (IPv4)) | P8, P9 | Partial |
| N-RTR `CISC-RT-000140` | CAT II | `SRG-NET-000205-RTR-000002` | Drop fragmented ICMP packets destined to the switch | `ip access-list EXTERNAL_ACL; 35 deny icmp any host <LOCAL_IP> fragments log` | 10.5(x) | The `icmp-frag` hardware check drops fragmented ICMP packets on models that support it; it drops all ICMP fragments, not only those addressed to the switch | `config switch security-feature; set icmp-frag enable; end` | Not in the feature matrix (8.0.0 CLI Reference) | — | Equivalent setting |
| N-RTR `CISC-RT-000150` | CAT II | `SRG-NET-000362-RTR-000111` | Disable gratuitous ARP on external interfaces | `interface ethernet <EXTERNAL_PORT>; no ip arp gratuitous request` | 10.5(x) | No setting stops FortiSwitch interfaces from sending gratuitous ARP; the `gratuitous-arp` security check on some models drops received gratuitous ARP packets instead | — | — | — | Not supported |
| N-RTR `CISC-RT-000160` | CAT III | `SRG-NET-000362-RTR-000112` | Disable IP directed broadcast on all interfaces | `interface ethernet <L3_PORT>; no ip directed-broadcast` | 10.5(x) | No directed-broadcast setting; an ingress ACL can drop packets sent to a subnet broadcast address | `config switch acl ingress; edit <ID>; set ingress-interface <PORT>; config classifier; set dst-ip-prefix <SUBNET_BROADCAST_IP> <HOST_MASK>; end; config action; set drop enable; end; end` | 7.0.0 or earlier (ACL (IPv4 ingress)) | — | Partial |
| N-RTR `CISC-RT-000170` | CAT II | `SRG-NET-000362-RTR-000113` | Disable ICMP unreachable messages on external interfaces | `interface ethernet <EXTERNAL_PORT>; no ip unreachables` | 10.5(x) | No setting to stop the switch from sending ICMP unreachable messages | — | — | — | Not supported |
| N-RTR `CISC-RT-000190` | CAT II | `SRG-NET-000362-RTR-000115` | Disable ICMP redirect messages on external interfaces | `interface ethernet <EXTERNAL_PORT>; no ip redirects` | 10.5(x) | ICMP redirect setting per interface | `config system interface; edit <EXTERNAL_INTERFACE>; set icmp-redirect disable; end` | Not in the feature matrix (8.0.0 CLI Reference) | — | Equivalent setting |
| N-RTR `CISC-RT-000200` | CAT III | `SRG-NET-000078-RTR-000001` | Log all packets dropped by interface ACLs | `ip access-list EXTERNAL_ACL; 90 deny ip any any log` | 10.5(x) | ACL counters show how many packets each policy dropped; FortiSwitchOS ACLs cannot log individual packets | `config switch acl ingress; edit <ID>; config action; set drop enable; set count enable; end; end` `get switch acl counters ingress` | 7.0.0 or earlier (ACL (IPv4 ingress)) | — | Partial |
| N-RTR `CISC-RT-000236` | CAT III | `SRG-NET-000512-RTR-000012` | Advertise a hop limit of at least 32 in IPv6 router advertisements | `interface ethernet <L3_PORTS>; ipv6 nd hop-limit 32` | 10.5(x) | IPv6 router advertisement hop limit per interface | `config system interface; edit <INTERFACE>; config ipv6; set ip6-hop-limit 64; end; end` | Not in the feature matrix (8.0.0 CLI Reference) | — | Equivalent setting |
| N-RTR `CISC-RT-000237` | CAT II | `SRG-NET-000512-RTR-000013` | Do not use IPv6 site-local unicast addresses | — | — | Address planning: assign no FEC0::/10 addresses | — | — | — | By procedure |
| N-RTR `CISC-RT-000240` | CAT I | `SRG-NET-000202-RTR-000001` | Perimeter: deny traffic by default and allow by exception | `ip access-list EXTERNAL_ACL; permit tcp host <PEER_IP> eq bgp host <LOCAL_IP>; permit tcp host <PEER_IP> host <LOCAL_IP> eq bgp; permit icmp host <PEER_IP> host <LOCAL_IP>; permit tcp any <WEB_SERVER_IP>/32 eq www; deny ip any any log; exit; interface ethernet <EXTERNAL_PORT>; ip access-group EXTERNAL_ACL in` | 10.5(x) | Ingress ACLs can permit approved traffic and drop the rest, but FortiSwitchOS ACLs have no implicit deny and no established-session match, so an explicit drop policy must cover everything not permitted | `config switch acl ingress; edit <ID>; set ingress-interface <EXTERNAL_PORT>; config action; set drop enable; end; end` | 7.0.0 or earlier (ACL (IPv4 ingress)) | — | Partial |
| N-RTR `CISC-RT-000250` | CAT II | `SRG-NET-000019-RTR-000002` | Perimeter: control traffic between interconnected networks by policy | `ip access-list EXTERNAL_ACL; permit tcp any any established; permit tcp host <PEER_IP> host <LOCAL_IP> eq bgp; permit tcp any <WEB_SERVER_IP>/32 eq www; deny ip any any log; exit; interface ethernet <EXTERNAL_PORT>; ip access-group EXTERNAL_ACL in` | 10.5(x) | Ingress ACLs on the external ports | `config switch acl ingress; edit <ID>; set ingress-interface <EXTERNAL_PORT>; config classifier; set src-ip-prefix <SOURCE> <MASK>; set dst-ip-prefix <DESTINATION> <MASK>; end; config action; set drop enable; end; end` | 7.0.0 or earlier (ACL (IPv4 ingress)) | — | Equivalent setting |
| N-RTR `CISC-RT-000260` | CAT II | `SRG-NET-000364-RTR-000109` | Perimeter: route inbound traffic only from authorized sources to authorized destinations | `ip access-list EXTERNAL_ACL; permit tcp any any established; permit udp host <NTP_SOURCE> host <NTP_DESTINATION> eq 123; deny ip any any log; exit; interface ethernet <EXTERNAL_PORT>; ip access-group EXTERNAL_ACL in` | 10.5(x) | Ingress ACLs matching source, destination, and service | `config switch acl ingress; edit <ID>; set ingress-interface <EXTERNAL_PORT>; config classifier; set src-ip-prefix <SOURCE> <MASK>; set dst-ip-prefix <DESTINATION> <MASK>; set service <SERVICE>; end; end` | 7.0.0 or earlier (ACL (IPv4 ingress)) | — | Equivalent setting |
| N-RTR `CISC-RT-000270` | CAT II | `SRG-NET-000364-RTR-000110` | Perimeter: block inbound packets with bogon source addresses | `ip access-list EXTERNAL_ACL; deny ip <BOGON_PREFIX> any log; permit tcp any any established; deny ip any any log; exit; interface ethernet <EXTERNAL_PORT>; ip access-group EXTERNAL_ACL in` | 10.5(x) | Ingress ACL dropping bogon source prefixes | `config switch acl ingress; edit <ID>; set ingress-interface <EXTERNAL_PORT>; config classifier; set src-ip-prefix <BOGON_PREFIX> <MASK>; end; config action; set drop enable; end; end` | 7.0.0 or earlier (ACL (IPv4 ingress)) | — | Equivalent setting |
| N-RTR `CISC-RT-000310` | CAT I | `SRG-NET-000205-RTR-000014` | Perimeter: drop outbound packets with illegitimate source addresses (egress filter or uRPF) | `interface ethernet <INTERNAL_PORT>; ip verify unicast source reachable-via rx` | 10.5(x) | Unicast reverse path forwarding (source check) on internal interfaces | `config system interface; edit <INTERNAL_INTERFACE>; set src-check strict; end` | 7.0.0 or earlier (uRPF) | P9 | Same requirement |
| N-RTR `CISC-RT-000320` | CAT II | `SRG-NET-000205-RTR-000003` | Perimeter: filter traffic into the enclave as DoD Instruction 8551.01 requires | `ip access-list EXTERNAL_ACL; permit tcp any any established; permit tcp host <PEER_IP> host <LOCAL_IP> eq bgp; permit tcp any <WEB_SERVER_IP>/32 eq www; deny ip any any log; exit; interface ethernet <EXTERNAL_PORT>; ip access-group EXTERNAL_ACL in` | 10.5(x) | Ingress ACLs built from the PPSM ports, protocols, and services list, using custom ACL services | `config switch acl service custom; edit <SERVICE>; set protocol TCP/UDP/SCTP; set tcp-portrange <PORT>; end` `config switch acl ingress; edit <ID>; set ingress-interface <EXTERNAL_PORT>; config classifier; set service <SERVICE>; end; end` | 7.4.3 and later (ACL service (IPv4)) | — | Equivalent setting |
| N-RTR `CISC-RT-000330` | CAT II | `SRG-NET-000205-RTR-000004` | Perimeter: filter ingress traffic inbound on the external interface | `interface ethernet <EXTERNAL_PORT>; ip access-group EXTERNAL_ACL in` | 10.5(x) | Ingress ACLs on the external ports | `config switch acl ingress; edit <ID>; set ingress-interface <EXTERNAL_PORT>; config classifier; set src-ip-prefix <SOURCE> <MASK>; end; config action; set drop enable; end; end` | 7.0.0 or earlier (ACL (IPv4 ingress)) | — | Equivalent setting |
| N-RTR `CISC-RT-000340` | CAT II | `SRG-NET-000205-RTR-000005` | Perimeter: filter egress traffic inbound on the internal interface | `interface ethernet <INTERNAL_PORT>; ip access-group EGRESS_FILTER in` | 10.5(x) | Strict unicast reverse path forwarding on the internal interfaces, or an ingress ACL on the internal ports | `config system interface; edit <INTERNAL_INTERFACE>; set src-check strict; end` | 7.0.0 or earlier (uRPF) | P9 | Equivalent setting |
| N-RTR `CISC-RT-000350` | CAT II | `SRG-NET-000205-RTR-000015` | Perimeter: block all packets with IP options | `no ip source-route` | 10.5(x) | FortiSwitchOS ACL classifiers cannot match IP options | — | — | — | Not supported |
| N-RTR `CISC-RT-000360` | CAT III | `SRG-NET-000364-RTR-000111` | Perimeter: disable LLDP on external interfaces | `interface ethernet <EXTERNAL_PORT>; no lldp transmit` | 10.5(x) | LLDP status per physical port | `config switch physical-port; edit <EXTERNAL_PORT>; set lldp-status disable; end` | 7.0.0 or earlier (LLDP transmit) | — | Equivalent setting |
| N-RTR `CISC-RT-000370` | CAT III | `SRG-NET-000364-RTR-000111` | Perimeter: disable CDP on external interfaces | `interface ethernet <EXTERNAL_PORT>; no cdp enable` | 10.5(x) | CDP status per physical port | `config switch physical-port; edit <EXTERNAL_PORT>; set cdp-status disable; end` | Not in the feature matrix (8.0.0 CLI Reference) | — | Equivalent setting |
| N-RTR `CISC-RT-000380` | CAT II | `SRG-NET-000364-RTR-000112` | Perimeter: disable proxy ARP on external interfaces | `interface ethernet <EXTERNAL_PORT>; no ip proxy-arp` | 10.5(x) | The 8.0.0 CLI Reference documents no proxy ARP function, so there is nothing to disable; confirm by test | — | — | — | Not applicable |
| N-RTR `CISC-RT-000390` | CAT II | `SRG-NET-000364-RTR-000113` | Perimeter: block all outbound management traffic | `ip access-list EXTERNAL_ACL_OUTBOUND; deny tcp any any eq 49 log; deny tcp any any eq 22 log; deny udp any any eq 161 log; deny udp any any eq 162 log; deny udp any any eq 514 log; permit tcp any any eq www; deny ip any any log; exit; interface ethernet <EXTERNAL_PORT>; ip access-group EXTERNAL_ACL_OUTBOUND out` | 10.5(x) | Egress ACL on the external ports that drops management protocols (SSH, TACACS+, SNMP, syslog) defined as custom ACL services | `config switch acl service custom; edit <MGMT_SERVICE>; set protocol TCP/UDP/SCTP; set tcp-portrange <MGMT_TCP_PORTS>; set udp-portrange <MGMT_UDP_PORTS>; end` `config switch acl egress; edit <ID>; set interface <EXTERNAL_PORT>; config classifier; set service <MGMT_SERVICE>; end; config action; set drop enable; end; end` | 7.4.3 and later (ACL (IPv4 egress)) | P9 | Equivalent setting |
| N-RTR `CISC-RT-000391` | CAT II | `SRG-NET-000512-RTR-000014` | Perimeter: suppress IPv6 router advertisements on external interfaces | `interface ethernet <EXTERNAL_PORT>; ipv6 nd suppress-ra` | 10.5(x) | Stop sending router advertisements on the interface, and RA guard on the external ports | `config system interface; edit <EXTERNAL_INTERFACE>; config ipv6; set ip6-send-adv disable; end; end` `config switch raguard-policy; edit <POLICY>; set device-role host; end` `config switch interface; edit <EXTERNAL_PORT>; config raguard; edit 1; set raguard-policy <POLICY>; set vlan-list <VLANS>; end; end` | 7.0.0 or earlier (IPv6 RA guard) | P9 | Same requirement |
| N-RTR `CISC-RT-000450` | CAT II | `SRG-NET-000205-RTR-000012` | Permit management traffic only through the out-of-band management interface | `ip access-list INGRESS_MANAGEMENT_ACL; permit tcp any host <MGMT_IP> eq 49; permit tcp any host <MGMT_IP> eq 22; permit udp any host <MGMT_IP> eq 161; permit udp any host <MGMT_IP> eq 162; permit udp any host <MGMT_IP> eq 123; permit icmp any host <MGMT_IP>; deny ip any any log; exit; ip access-list EGRESS_MANAGEMENT_ACL; deny ip any any log; exit; interface ethernet <MGMT_PORT>; ip access-group INGRESS_MANAGEMENT_ACL in; ip access-group EGRESS_MANAGEMENT_ACL out` | 10.5(x) | Management protocols allowed only on the dedicated management port, with no management access on in-band interfaces | `config system interface; edit mgmt; set allowaccess https ssh snmp; end` | Not in the feature matrix (8.0.0 CLI Reference) | P10 | Equivalent setting |
| N-RTR `CISC-RT-000470` | CAT III | `SRG-NET-000362-RTR-000124` | BGP: check that a single-hop eBGP peer is directly connected | `router bgp <ASN>; neighbor <EBGP_PEER> remote-as <PEER_ASN>; no disable-connected-check` | 10.5(x) | eBGP neighbors must be directly connected unless multihop is allowed; keep `ebgp-enforce-multihop` disabled (the default) for single-hop peers | `config router bgp; config neighbor; edit <EBGP_PEER>; set ebgp-enforce-multihop disable; end; end` | 7.0.0 or earlier (BGP (IPv4/IPv6)) | P8, P9, P11 | Equivalent setting |
| N-RTR `CISC-RT-000480` | CAT II | `SRG-NET-000230-RTR-000002` | BGP: use a unique key for each autonomous system peered with | `router bgp <ASN>; neighbor <EBGP_PEER_1> remote-as <PEER_ASN_1>; password <UNIQUE_KEY_1>; exit; neighbor <EBGP_PEER_2> remote-as <PEER_ASN_2>; password <UNIQUE_KEY_2>` | 10.5(x) | Per-neighbor BGP password (TCP MD5, as on the Cisco side) | `config router bgp; config neighbor; edit <EBGP_PEER>; set password <UNIQUE_KEY>; end; end` | 7.0.0 or earlier (BGP (IPv4/IPv6)) | P8, P9, P11 | Equivalent setting |
| N-RTR `CISC-RT-000490` | CAT II | `SRG-NET-000018-RTR-000002` | BGP: reject inbound advertisements of bogon prefixes | `ip prefix-list PREFIX_FILTER seq 5 deny <BOGON_PREFIX> le 32; ip prefix-list PREFIX_FILTER seq 75 permit 0.0.0.0/0 ge 8; router bgp <ASN>; neighbor <EBGP_PEER> remote-as <PEER_ASN>; address-family ipv4 unicast; prefix-list PREFIX_FILTER in` | 10.5(x) | Inbound prefix list on each eBGP neighbor | `config router prefix-list; edit PREFIX_FILTER; config rule; edit 1; set action deny; set prefix <BOGON_PREFIX> <MASK>; set le 32; end; end` `config router bgp; config neighbor; edit <EBGP_PEER>; set prefix-list-in PREFIX_FILTER; end; end` | 7.0.0 or earlier (BGP (IPv4/IPv6)) | P8, P9, P11 | Same requirement |
| N-RTR `CISC-RT-000500` | CAT II | `SRG-NET-000018-RTR-000003` | BGP: reject inbound advertisements of the local AS's own prefixes | `ip prefix-list PREFIX_FILTER seq 74 deny <LOCAL_AS_PREFIX> le 32; router bgp <ASN>; neighbor <EBGP_PEER> remote-as <PEER_ASN>; address-family ipv4 unicast; prefix-list PREFIX_FILTER in` | 10.5(x) | Inbound prefix list on each eBGP neighbor | `config router prefix-list; edit PREFIX_FILTER; config rule; edit 2; set action deny; set prefix <LOCAL_AS_PREFIX> <MASK>; set le 32; end; end` `config router bgp; config neighbor; edit <EBGP_PEER>; set prefix-list-in PREFIX_FILTER; end; end` | 7.0.0 or earlier (BGP (IPv4/IPv6)) | P8, P9, P11 | Equivalent setting |
| N-RTR `CISC-RT-000510` | CAT II | `SRG-NET-000018-RTR-000004` | BGP: reject advertisements from a CE for prefixes not allocated to that customer | `ip prefix-list PREFIX_FILTER_CUST1 permit <CUSTOMER_PREFIX> le 32; ip prefix-list PREFIX_FILTER_CUST1 deny 0.0.0.0/0 ge 8; router bgp <ASN>; neighbor <CE_PEER> remote-as <CE_ASN>; address-family ipv4 unicast; prefix-list PREFIX_FILTER_CUST1 in` | 10.5(x) | Inbound prefix list per customer neighbor | `config router bgp; config neighbor; edit <CE_PEER>; set prefix-list-in <CUSTOMER_PREFIX_LIST>; end; end` | 7.0.0 or earlier (BGP (IPv4/IPv6)) | P8, P9, P11 | Equivalent setting |
| N-RTR `CISC-RT-000520` | CAT II | `SRG-NET-000018-RTR-000005` | BGP: advertise only customer and local AS prefixes | `ip prefix-list CE_PREFIX_ADVERTISEMENTS permit <CUSTOMER_PREFIX> le 32; ip prefix-list CE_PREFIX_ADVERTISEMENTS deny 0.0.0.0/0 ge 8; router bgp <ASN>; neighbor <CE_PEER> remote-as <CE_ASN>; address-family ipv4 unicast; prefix-list CE_PREFIX_ADVERTISEMENTS out` | 10.5(x) | Outbound prefix list per neighbor | `config router prefix-list; edit CE_PREFIX_ADVERTISEMENTS; config rule; edit 1; set action permit; set prefix <CUSTOMER_PREFIX> <MASK>; set le 32; end; end` `config router bgp; config neighbor; edit <CE_PEER>; set prefix-list-out CE_PREFIX_ADVERTISEMENTS; end; end` | 7.0.0 or earlier (BGP (IPv4/IPv6)) | P8, P9, P11 | Equivalent setting |
| N-RTR `CISC-RT-000530` | CAT II | `SRG-NET-000205-RTR-000006` | BGP: do not advertise IP core prefixes | `ip prefix-list FILTER_CORE_PREFIXES deny <CORE_PREFIX> le 32; ip prefix-list FILTER_CORE_PREFIXES permit 0.0.0.0/0 ge 8; router bgp <ASN>; neighbor <EBGP_PEER> remote-as <PEER_ASN>; address-family ipv4 unicast; prefix-list FILTER_CORE_PREFIXES out` | 10.5(x) | Outbound prefix list that denies the core prefixes | `config router prefix-list; edit CE_PREFIX_ADVERTISEMENTS; config rule; edit 2; set action deny; set prefix <CORE_PREFIX> <MASK>; set le 32; end; end` `config router bgp; config neighbor; edit <CE_PEER>; set prefix-list-out CE_PREFIX_ADVERTISEMENTS; end; end` | 7.0.0 or earlier (BGP (IPv4/IPv6)) | P8, P9, P11 | Equivalent setting |
| N-RTR `CISC-RT-000540` | CAT III | `SRG-NET-000018-RTR-000006` | BGP: reject routes whose AS_PATH does not start with the peer's AS | `router bgp <ASN>; enforce-first-as` | 10.5(x) | First-AS enforcement per neighbor | `config router bgp; config neighbor; edit <EBGP_PEER>; set enforce-first-as enable; end; end` | 7.0.0 or earlier (BGP (IPv4/IPv6)) | P8, P9, P11 | Equivalent setting |
| N-RTR `CISC-RT-000550` | CAT III | `SRG-NET-000018-RTR-000010` | BGP: reject CE routes whose originating AS does not belong to that customer | `ip as-path access-list AS_PATH permit ^<CUSTOMER_ASN>$; ip as-path access-list AS_PATH deny .*; router bgp <ASN>; neighbor <CE_PEER> remote-as <CE_ASN>; address-family ipv4 unicast; filter-list AS_PATH in` | 10.5(x) | AS path list applied inbound to the customer neighbor | `config router aspath-list; edit <ASPATH_LIST>; config rule; edit 1; set action permit; set regexp <CUSTOMER_ASN_REGEX>; end; end` `config router bgp; config neighbor; edit <CE_PEER>; set filter-list-in <ASPATH_LIST>; end; end` | 7.0.0 or earlier (BGP (IPv4/IPv6)) | P8, P9, P11 | Equivalent setting |
| N-RTR `CISC-RT-000560` | CAT II | `SRG-NET-000362-RTR-000117` | BGP: limit the number of prefixes accepted from each peer | `router bgp <ASN>; neighbor <EBGP_PEER> remote-as <PEER_ASN>; address-family ipv4 unicast; maximum-prefix <MAXIMUM>` | 10.5(x) | Maximum prefixes per neighbor | `config router bgp; config neighbor; edit <EBGP_PEER>; set maximum-prefix <MAXIMUM>; end; end` | 7.0.0 or earlier (BGP (IPv4/IPv6)) | P8, P9, P11 | Equivalent setting |
| N-RTR `CISC-RT-000570` | CAT III | `SRG-NET-000362-RTR-000118` | BGP: accept no inbound prefixes longer than /24 | `ip prefix-list FILTER_PREFIX_LENGTH permit 0.0.0.0/0 ge 8 le 24; ip prefix-list FILTER_PREFIX_LENGTH deny 0.0.0.0/0 le 32; router bgp <ASN>; neighbor <EBGP_PEER> remote-as <PEER_ASN>; address-family ipv4 unicast; prefix-list FILTER_PREFIX_LENGTH in` | 10.5(x) | Inbound prefix list rule that permits only prefixes of /8 to /24 | `config router prefix-list; edit PREFIX_FILTER; config rule; edit 3; set action permit; set prefix any; set ge 8; set le 24; end; end` | 7.0.0 or earlier (BGP (IPv4/IPv6)) | P8, P9, P11 | Equivalent setting |
| N-RTR `CISC-RT-000580` | CAT III | `SRG-NET-000512-RTR-000001` | BGP: source iBGP sessions from a loopback address | `router bgp <ASN>; neighbor <IBGP_PEER> remote-as <ASN>; update-source loopback0` | 10.5(x) | Loopback interface used as the update source for iBGP neighbors | `config system interface; edit <LOOPBACK>; set type loopback; set ip <LOOPBACK_IP> <HOST_MASK>; end` `config router bgp; config neighbor; edit <IBGP_PEER>; set update-source <LOOPBACK>; end; end` | 7.0.0 or earlier (BGP (IPv4/IPv6)) | P8, P9, P11 | Equivalent setting |
| N-RTR `CISC-RT-000590` | CAT III | `SRG-NET-000512-RTR-000002` | MPLS: source LDP sessions from a loopback address | — | — | FortiSwitchOS has no MPLS or LDP | — | — | — | Not supported |
| N-RTR `CISC-RT-000600` | CAT III | `SRG-NET-000512-RTR-000003` | MPLS: synchronize the IGP with LDP | — | — | FortiSwitchOS has no MPLS or LDP | — | — | — | Not supported |
| N-RTR `CISC-RT-000610` | CAT III | `SRG-NET-000193-RTR-000001` | MPLS: pace RSVP-TE messages | — | — | FortiSwitchOS has no MPLS traffic engineering or RSVP-TE | — | — | — | Not supported |
| N-RTR `CISC-RT-000620` | CAT II | `SRG-NET-000512-RTR-000004` | MPLS: disable TTL propagation | `no mpls ip propagate-ttl` | 10.5(x) | FortiSwitchOS has no MPLS | — | — | — | Not supported |
| N-RTR `CISC-RT-000630` | CAT I | `SRG-NET-000512-RTR-000005` | PE: bind each VRF to the right interfaces to keep L3VPNs separate | `vrf context <VRF_NAME>; exit; interface ethernet <CE_PORT>; vrf member <VRF_NAME>` | 10.5(x) | VRF-lite: interfaces can be bound to VRFs (the setting Chapter 11 maps), but FortiSwitchOS has no MPLS L3VPN, so it cannot act as a PE | `config router vrf; edit <VRF>; set vrfid <ID>; end` `config system interface; edit <INTERFACE>; set vrf <VRF>; end` | 7.0.0 or earlier (VRF (IPv4/IPv6)) | P8, P9 | Partial |
| N-RTR `CISC-RT-000640` | CAT I | `SRG-NET-000512-RTR-000006` | PE: give each VRF the right route targets | `vrf context <VRF_NAME>; address-family ipv4 unicast; route-target import <RT>; route-target export <RT>` | 10.5(x) | No MPLS L3VPN; FortiSwitchOS route targets exist only for BGP EVPN VXLAN | — | — | — | Not supported |
| N-RTR `CISC-RT-000650` | CAT II | `SRG-NET-000512-RTR-000007` | PE: give each VRF the right route distinguisher | `vrf context <VRF_NAME>; rd <RD>` | 10.5(x) | No MPLS L3VPN; FortiSwitchOS route distinguishers exist only for BGP EVPN VXLAN | — | — | — | Not supported |
| N-RTR `CISC-RT-000660` | CAT II | `SRG-NET-000343-RTR-000001` | PE: authenticate targeted LDP sessions for L2VPN with a FIPS-approved MAC | — | — | FortiSwitchOS has no MPLS L2VPN or LDP | — | — | — | Not supported |
| N-RTR `CISC-RT-000670` | CAT I | `SRG-NET-000512-RTR-000008` | PE: set the right VC ID for each VPWS attachment circuit | — | — | FortiSwitchOS has no VPWS pseudowires | — | — | — | Not supported |
| N-RTR `CISC-RT-000680` | CAT I | `SRG-NET-000512-RTR-000009` | PE: define VPLS attachment circuits with a unique VPN ID per customer VLAN | — | — | FortiSwitchOS has no VPLS | — | — | — | Not supported |
| N-RTR `CISC-RT-000700` | CAT II | `SRG-NET-000193-RTR-000002` | PE: set storm control thresholds on VPLS CE-facing interfaces | `interface ethernet <CE_PORT>; storm-control broadcast level <PERCENT>` | 10.5(x) | FortiSwitchOS has no VPLS; storm control itself is covered by `CISC-L2-000160` | — | — | — | Not supported |
| N-RTR `CISC-RT-000710` | CAT III | `SRG-NET-000362-RTR-000119` | PE: run IGMP or MLD snooping in each VPLS bridge domain | — | — | FortiSwitchOS has no VPLS; VLAN snooping is covered by `CISC-L2-000170` | — | — | — | Not supported |
| N-RTR `CISC-RT-000720` | CAT II | `SRG-NET-000192-RTR-000002` | PE: limit the MAC addresses learned in each VPLS bridge domain | — | — | FortiSwitchOS has no VPLS; per-port and per-VLAN MAC learning limits exist outside VPLS | — | — | — | Not supported |
| N-RTR `CISC-RT-000730` | CAT I | `SRG-NET-000205-RTR-000007` | PE: block traffic destined to the IP core infrastructure | `ip access-list BLOCK_TO_CORE; deny ip any <CORE_PREFIX> log; permit ip any any; exit; interface ethernet <CE_PORT>; ip access-group BLOCK_TO_CORE in` | 10.5(x) | The rule is for an MPLS PE, a role FortiSwitch cannot take; an ingress ACL can drop traffic to core prefixes at another edge | `config switch acl ingress; edit <ID>; set ingress-interface <EDGE_PORT>; config classifier; set dst-ip-prefix <CORE_PREFIX> <MASK>; end; config action; set drop enable; end; end` | — | — | Not applicable |
| N-RTR `CISC-RT-000740` | CAT II | `SRG-NET-000205-RTR-000008` | PE: enable loose uRPF on CE-facing interfaces | `interface ethernet <CE_PORT>; ip verify unicast source reachable-via any` | 10.5(x) | The rule is for an MPLS PE, a role FortiSwitch cannot take; loose source checking exists for other edges | `config system interface; edit <EDGE_INTERFACE>; set src-check loose; end` | — | — | Not applicable |
| N-RTR `CISC-RT-000750` | CAT II | `SRG-NET-000205-RTR-000016` | PE: drop or ignore all packets with IP options | `no ip source-route` | 10.5(x) | The rule is for an MPLS PE, a role FortiSwitch cannot take; FortiSwitchOS ACLs cannot match IP options in any role (`CISC-RT-000350`) | — | — | — | Not applicable |
| N-RTR `CISC-RT-000760` | CAT III | `SRG-NET-000193-RTR-000113` | PE: enforce a QoS policy that favors mission-critical traffic | `class-map type qos match-all VOICE; match dscp 46; exit; policy-map type qos QOS_CLASSIFY; class VOICE; set qos-group 7; exit; exit; interface ethernet <INGRESS_PORT>; service-policy type qos input QOS_CLASSIFY` `policy-map type queuing QOS_QUEUING; class type queuing c-out-8q-q7; priority level 1; exit; class type queuing c-out-8q-q-default; bandwidth remaining percent 25; exit; exit; system qos; service-policy type queuing output QOS_QUEUING` | 10.5(x) | The rule is for an MPLS PE, a role FortiSwitch cannot take; QoS policies exist for other roles (`CISC-RT-000780`) | — | — | — | Not applicable |
| N-RTR `CISC-RT-000770` | CAT III | `SRG-NET-000193-RTR-000114` | P (MPLS core): enforce a QoS policy that favors mission-critical traffic | `class-map type qos match-all VOICE; match dscp 46; exit; policy-map type qos QOS_CLASSIFY; class VOICE; set qos-group 7; exit; exit; interface ethernet <INGRESS_PORT>; service-policy type qos input QOS_CLASSIFY` `policy-map type queuing QOS_QUEUING; class type queuing c-out-8q-q7; priority level 1; exit; class type queuing c-out-8q-q-default; bandwidth remaining percent 25; exit; exit; system qos; service-policy type queuing output QOS_QUEUING` | 10.5(x) | The rule is for an MPLS provider core switch, a role FortiSwitch cannot take | — | — | — | Not applicable |
| N-RTR `CISC-RT-000780` | CAT II | `SRG-NET-000193-RTR-000112` | Enforce a QoS policy that limits packet-flooding denial-of-service attacks | `class-map type qos match-all SCAVENGER; match dscp 8; exit; policy-map type qos QOS_CLASSIFY; class SCAVENGER; set qos-group 1; exit; exit; interface ethernet <INGRESS_PORT>; service-policy type qos input QOS_CLASSIFY` `policy-map type queuing QOS_QUEUING; class type queuing c-out-8q-q1; bandwidth remaining percent 5; exit; class type queuing c-out-8q-q-default; bandwidth remaining percent 10; exit; exit; system qos; service-policy type queuing output QOS_QUEUING` | 10.5(x) | Egress QoS policy on uplinks, with ACL policers for flood-prone traffic | `config switch qos qos-policy; edit <POLICY>; set schedule weighted; end` `config switch interface; edit <UPLINK_PORT>; set qos-policy <POLICY>; end` | 7.0.0 or earlier (802.1p support, including priority queuing trunk and WRED) | P9 | Equivalent setting |
| N-RTR `CISC-RT-000790` | CAT II | `SRG-NET-000019-RTR-000003` | Multicast: disable PIM on interfaces that do not need multicast routing | `interface ethernet <NON_MULTICAST_PORT>; no ip pim sparse-mode` | 10.5(x) | PIM-SSM configured only on the interfaces that route multicast | `config router multicast; config interface; edit <INTERFACE>; set pim-mode ssm-mode; end; end` | 7.2.8 and later (PIM-SSM (IPv4)) | P8, P9 | Same requirement |
| N-RTR `CISC-RT-000800` | CAT II | `SRG-NET-000019-RTR-000004` | Multicast: bind a PIM neighbor filter to PIM interfaces | `ip prefix-list PIM_NEIGHBOR seq 5 permit <PIM_NEIGHBOR_IP>/32; interface ethernet <PIM_PORT>; ip pim neighbor-policy prefix-list PIM_NEIGHBOR` | 10.5(x) | PIM runs only where configured (the setting Chapter 11 maps), but FortiSwitchOS has no PIM neighbor filter | `config router multicast; config interface; edit <INTERFACE>; set pim-mode ssm-mode; end; end` | 7.2.8 and later (PIM-SSM (IPv4)) | P8, P9 | Partial |
| N-RTR `CISC-RT-000810` | CAT III | `SRG-NET-000019-RTR-000005` | Multicast edge: set boundaries for administratively scoped multicast | `ip access-list FILTER_TRAFFIC_IN; deny ip any 239.0.0.0/8; permit tcp any any established; deny ip any any log; exit; ip access-list FILTER_TRAFFIC_OUT; deny ip any 239.0.0.0/8; permit ip any any; exit; interface ethernet <BOUNDARY_PORT>; ip access-group FILTER_TRAFFIC_IN in; ip access-group FILTER_TRAFFIC_OUT out` | 10.5(x) | No multicast boundary setting; an ingress ACL on the boundary ports can drop 239.0.0.0/8 traffic, but it does not filter PIM or IGMP control messages for those groups | `config switch acl ingress; edit <ID>; set ingress-interface <BOUNDARY_PORT>; config classifier; set dst-ip-prefix <ADMIN_SCOPED_PREFIX> <MASK>; end; config action; set drop enable; end; end` | 7.0.0 or earlier (ACL (IPv4 ingress)) | — | Partial |
| N-RTR `CISC-RT-000820` | CAT III | `SRG-NET-000362-RTR-000120` | RP: limit the multicast forwarding cache (PIM and MSDP source-active state) | `route-map PIM_REGISTER_FILTER deny 10; match ip multicast group <UNWANTED_GROUP_PREFIX>; route-map PIM_REGISTER_FILTER permit 20; match ip multicast source <APPROVED_SOURCE>/32; exit; ip pim register-policy PIM_REGISTER_FILTER; ip pim register-rate-limit <RATE>` | 10.5(x) | FortiSwitchOS supports PIM-SSM only, which has no rendezvous point | — | — | — | Not applicable |
| N-RTR `CISC-RT-000830` | CAT III | `SRG-NET-000019-RTR-000013` | RP: filter PIM Register messages for unwanted groups and sources | `route-map PIM_REGISTER_FILTER deny 10; match ip multicast group <UNWANTED_GROUP_PREFIX>; route-map PIM_REGISTER_FILTER permit 20; match ip multicast source <APPROVED_SOURCE>/32; exit; ip pim register-policy PIM_REGISTER_FILTER` | 10.5(x) | FortiSwitchOS supports PIM-SSM only, which has no rendezvous point or Register messages | — | — | — | Not applicable |
| N-RTR `CISC-RT-000840` | CAT III | `SRG-NET-000019-RTR-000014` | RP: filter PIM Join messages for unwanted groups | `route-map PIM_JOIN_FILTER deny 10; match ip multicast group <UNWANTED_GROUP_PREFIX>; route-map PIM_JOIN_FILTER permit 20; match ip multicast group 224.0.0.0/4; exit; interface ethernet <PIM_PORT>; ip pim jp-policy PIM_JOIN_FILTER in` | 10.5(x) | FortiSwitchOS supports PIM-SSM only, which has no rendezvous point | — | — | — | Not applicable |
| N-RTR `CISC-RT-000860` | CAT III | `SRG-NET-000364-RTR-000114` | DR: let hosts join only approved multicast groups (IGMP and MLD report filter) | `route-map ALLOWED_GROUPS permit 10; match ip multicast group <APPROVED_GROUP_PREFIX>; route-map ALLOWED_GROUPS deny 40; match ip multicast group 224.0.0.0/4; exit; interface ethernet <HOST_FACING_PORT>; ip igmp report-policy ALLOWED_GROUPS` | 10.5(x) | FortiSwitchOS has no IGMP or MLD join filter on routed interfaces | — | — | — | Not supported |
| N-RTR `CISC-RT-000870` | CAT II | `SRG-NET-000364-RTR-000115` | DR: let hosts join groups only from approved sources | `route-map ALLOWED_SOURCES permit 10; match ip multicast source <APPROVED_SOURCE>/32; route-map ALLOWED_SOURCES deny 30; match ip multicast source 0.0.0.0/0; exit; interface ethernet <HOST_FACING_PORT>; ip igmp report-policy ALLOWED_SOURCES` | 10.5(x) | FortiSwitchOS has no IGMP or MLD source filter on routed interfaces | — | — | — | Not supported |
| N-RTR `CISC-RT-000880` | CAT II | `SRG-NET-000362-RTR-000122` | DR: limit the multicast route states created by IGMP and MLD reports | `interface ethernet <HOST_FACING_PORT>; ip igmp state-limit <MAX_STATES>` | 10.5(x) | FortiSwitchOS has no limit on IGMP or MLD groups per interface | — | — | — | Not supported |
| N-RTR `CISC-RT-000890` | CAT II | `SRG-NET-000362-RTR-000123` | DR: set the SPT threshold to infinity where Any Source Multicast is used | `ip prefix-list SPT_GROUPS permit <ASM_GROUP_PREFIX>; ip pim spt-threshold infinity group-list prefix-list SPT_GROUPS` | 10.5(x) | FortiSwitchOS supports PIM-SSM only, so there is no shared tree or SPT switchover | — | — | — | Not applicable |
| N-RTR `CISC-RT-000900` | CAT II | `SRG-NET-000364-RTR-000116` | MSDP: accept MSDP packets only from known peers | `ip access-list EXTERNAL_ACL_INBOUND; permit tcp any any established; permit tcp host <MSDP_PEER> host <LOCAL_IP> eq 639; deny tcp any host <LOCAL_IP> eq 639; deny ip any any; exit; interface ethernet <EXTERNAL_PORT>; ip access-group EXTERNAL_ACL_INBOUND in` | 10.5(x) | FortiSwitchOS does not run MSDP | — | — | — | Not applicable |
| N-RTR `CISC-RT-000910` | CAT II | `SRG-NET-000343-RTR-000002` | MSDP: authenticate all received MSDP packets | `feature msdp; ip msdp password <PEER_IP> <PASSWORD>` | 10.5(x) | FortiSwitchOS does not run MSDP | — | — | — | Not applicable |
| N-RTR `CISC-RT-000920` | CAT III | `SRG-NET-000018-RTR-000007` | MSDP: filter received source-active messages for unwanted groups and sources | `ip prefix-list INBOUND_MSDP_SA_FILTER seq 10 deny <UNWANTED_GROUP>/32; ip prefix-list INBOUND_MSDP_SA_FILTER seq 75 permit 0.0.0.0/0 ge 8; ip msdp sa-policy <PEER_IP> prefix-list INBOUND_MSDP_SA_FILTER in` | 10.5(x) | FortiSwitchOS does not run MSDP | — | — | — | Not applicable |
| N-RTR `CISC-RT-000930` | CAT III | `SRG-NET-000018-RTR-000008` | MSDP: filter source-active messages sent to external peers | `ip prefix-list OUTBOUND_MSDP_SA_FILTER seq 10 deny <LOCAL_ONLY_SOURCE_PREFIX> le 32; ip prefix-list OUTBOUND_MSDP_SA_FILTER seq 20 permit 0.0.0.0/0 ge 8; ip msdp sa-policy <PEER_IP> prefix-list OUTBOUND_MSDP_SA_FILTER out` | 10.5(x) | FortiSwitchOS does not run MSDP | — | — | — | Not applicable |
| N-RTR `CISC-RT-000940` | CAT III | `SRG-NET-000018-RTR-000009` | MSDP: limit source-active messages accepted from each peer | `ip msdp sa-limit <PEER_IP> <NUMBER>` | 10.5(x) | FortiSwitchOS does not run MSDP | — | — | — | Not applicable |
| N-RTR `CISC-RT-000950` | CAT III | `SRG-NET-000512-RTR-000011` | MSDP: source MSDP traffic from a loopback address | `ip msdp peer <PEER_IP> connect-source loopback0 remote-as <ASN>` | 10.5(x) | FortiSwitchOS does not run MSDP | — | — | — | Not applicable |

### FortiSwitch requirements with no Cisco NX-OS rule

The 25 SRG requirements below are mapped to FortiSwitch features
in Chapter 11 but are cited by no NX-OS Switch STIG rule, so an NX-OS rule
checklist misses them. They are the AAA Services SRG requirements (802.1X
and RADIUS behavior), the Layer 2 Switch SRG's general requirements
(traffic separation, alternate paths, excess bandwidth, Rapid STP, static
trunks), the VRRP authentication requirement, and NDM requirements such as
FIPS mode and signed firmware; two NDM requirements (clock synchronization
and vendor-supported versions) are the current versions of the older SRG
IDs that `CISC-ND-001030` and `CISC-ND-001470` cite. The FortiSwitch side
of each comes from Chapter 33: from its second table, or, for the
3 requirements that an IOS XE rule cites but no NX-OS rule
does, from the Chapter 33 row of that IOS XE rule. Add them to the
FortiSwitch checklist, with the prerequisites in the last column.

[Download the unmatched requirements as CSV](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/data/volume-172-disa-srgs-and-stigs/37-cisco-nx-os-switch-and-fortiswitch-stig-crosswalk-unmatched.csv) (25 rows).

| SRG | Requirement ID | Requirement | FortiSwitch setting | FortiSwitchOS command | FortiSwitchOS version | FortiSwitch prerequisites |
| --- | --- | --- | --- | --- | --- | --- |
| NDM | `SRG-APP-000033-NDM-000212` | The network device must be configured to assign appropriate user roles or access levels to authenticated users. | Access profiles assigned to administrator accounts (Chapter 11 also maps centralized, cloud, and REST API management to this requirement) | `config system accprofile; edit <PROFILE>; set sysgrp read; end` `config system admin; edit <ADMIN>; set accprofile <PROFILE>; end` | Not in the feature matrix (8.0.0 CLI Reference) | — |
| NDM | `SRG-APP-000131-NDM-000243` | The network device must prevent the installation of patches, service packs, or application components without verification the software component has been digitally signed using a certificate that is recognized and approved by the organization. | OS image signature verification; Configuration file verification; CLI reports if BIOS and firmware signatures are valid | `diagnose sys firmware info` | 7.4.0 and later (OS image signature verification) | P9 |
| NDM | `SRG-APP-000179-NDM-000265` | The network device must use FIPS 140-2 approved algorithms for authentication to a cryptographic module. | LINCE support; FIPS 140-3 (Level 1) and CC support; FedRAMP support | `config system security; set mode fips-cc; end` | 7.6.4 and later (FIPS 140-3 (Level 1) and CC support) | P9 |
| NDM | `SRG-APP-000457-NDM-000352` | The network device must install security-relevant firmware updates within 30 days unless the time period is directed by an authoritative source (e.g., IAVM, CTOs, DTMs, STIGs). | Centralized firmware management; CPLD software upgrade support for OS; Firmware image rotation (dual-firmware image support) | `config system global; set image-rotation enable; end` | 7.0.0 or earlier (Firmware image rotation (dual-firmware image support)) | — |
| NDM | `SRG-APP-000920-NDM-000320` | The network device must be configured to synchronize system clocks within and between systems or system components. | PTP version-2 transparent clock; PTP layer-2 boundary clock; Layer-3 PTP; Use PTP to synchronize system clock; and 2 more | `config system ntp; set ntpsync enable; set authentication enable; config ntpserver; edit 1; set server <NTP_IP>; set authentication enable; set key-id <ID>; set key <KEY>; end; end` | 7.6.2 and later (NTP server (IPv4/IPv6)) | P5 |
| NDM | `SRG-APP-000925-NDM-000330` | The network device must be configured to compare the internal system clocks on an organization-defined frequency with organization-defined authoritative time source. | NTP synchronization interval (Chapter 11 maps automatic clock source selection) | `config system ntp; set ntpsync enable; set syncinterval <MINUTES>; end` | Not in the feature matrix (8.0.0 CLI Reference) | P5 |
| NDM | `SRG-APP-001035-NDM-000340` | The network device hardware and software must be a version supported by the vendor. | A FortiSwitchOS release Fortinet supports; check the running version (Chapter 11 maps centralized firmware management) | `get system status` | Not in the feature matrix (8.0.0 CLI Reference) | — |
| L2S | `SRG-NET-000057-L2S-000005` | The layer 2 switch must dynamically associate security attributes with organization-defined subjects in accordance with organization-defined security policies as information is created and combined. | Host quarantine; Integrated FortiGate network access control (NAC) function; NAC LAN segments; Matching FortiClient EMS tags in NAC policies; and 12 more | FortiGate: `config switch-controller quarantine; set quarantine enable; config targets; edit <MAC>; end` | 7.0.0 or earlier (Host quarantine) | P7 |
| L2S | `SRG-NET-000131-L2S-000014` | The layer 2 switch must be configured to disable non-essential capabilities. | Disable unused ports and features (Chapter 11 marks every operational feature that falls under this requirement when unused) | `config switch physical-port; edit <PORT>; set status down; end` | Not in the feature matrix (8.0.0 CLI Reference) | — |
| L2S | `SRG-NET-000193-L2S-000020` | The layer 2 switch must manage excess bandwidth to limit the effects of packet flooding types of denial of service (DoS) attacks. | Egress QoS policy with weighted queues on uplinks (ACL policers and MAC learning limits also apply) (the FortiSwitch side of IOS XE rule `CISC-L2-000040` in Chapter 33) | `config switch qos qos-policy; edit <POLICY>; set schedule weighted; end` `config switch interface; edit <UPLINK_PORT>; set qos-policy <POLICY>; end` | 7.0.0 or earlier (802.1p support, including priority queuing trunk and WRED) | P9 |
| L2S | `SRG-NET-000235-L2S-000031` | The layer 2 switch must be configured to fail securely in the event of an operational failure. | Firmware image rotation (dual-firmware image support); Tagged VLAN support for authserver-timeout | `config system global; set image-rotation enable; end` | 7.0.0 or earlier (Firmware image rotation (dual-firmware image support)) | — |
| L2S | `SRG-NET-000325-L2S-000041` | The layer 2 switch must uniquely identify and authenticate source by organization, system, application, and/or individual for information transfer. | FortiLink Secure Fabric authentication; MACsec: PSK mode; MACsec: Dynamic-CAK mode | `config switch macsec profile; edit <PROFILE>; set macsec-mode static-cak; set cipher_suite GCM-AES-256; config mka-psk; edit <KEY>; set mka-cak <CAK>; set mka-ckn <CKN>; end; end` `config switch physical-port; edit <PORT>; set security-mode macsec; set macsec-profile <PROFILE>; end` | 7.0.0 or earlier (MACsec: PSK mode) | P9 |
| L2S | `SRG-NET-000512-L2S-000003` | The layer 2 switch must implement Rapid STP where VLANs span multiple switches with redundant links. | FortiSwitchOS runs MSTP, which uses rapid convergence; enable it on every port, with Rapid PVST+ interoperation on ports that face Cisco switches (the FortiSwitch side of IOS XE rule `CISC-L2-000180` in Chapter 33) | `config switch stp settings; set status enable; end` `config switch interface; edit <PORT>; set stp-state enabled; set rpvst-port enabled; end` | 7.0.0 or earlier (MSTP instances) | — |
| L2S | `SRG-NET-000512-L2S-000005` | The layer 2 switch must have all trunk links enabled statically. | FortiSwitchOS has no trunk negotiation (no DTP), so tagged VLANs are always set statically per port; set link aggregation groups (FortiSwitchOS "trunks") to static or LACP explicitly (the FortiSwitch side of IOS XE rule `CISC-L2-000200` in Chapter 33) | `config switch interface; edit <TRUNK_PORT>; set native-vlan <NATIVE_VLAN>; set allowed-vlans <VLANS>; end` `config switch trunk; edit <TRUNK>; set mode static; end` | 7.0.0 or earlier (forced-untagged or force-tagged setting on switch interfaces) | P13 |
| L2S | `SRG-NET-000512-L2S-000100` | The layer 2 switch must be configured in accordance with the security configuration settings based on DoD security configuration or implementation guidance, including STIGs, NSA configuration guides, CTOs, and DTMs. | Automated detection and recommendations; Automation stitches (zero-touch provisioning automation); IP conflict detection and notification; ACL (IPv4 ingress); and 3 more | `config switch acl ingress; edit <ID>; set ingress-interface <PORT>; config classifier; set src-ip-prefix <IP> <MASK>; end; config action; set drop enable; end; end` | 7.0.0 or earlier (ACL (IPv4 ingress)) | — |
| L2S | `SRG-NET-000520-L2S-000105` | The layer 2 switch must dynamically associate security attributes with organization-defined objects in accordance with organization-defined security policies as information is created and combined. | Matching FortiClient EMS tags in NAC policies; Matching IoT/OT vulnerabilities in NAC policies; Matching FortiVoice tags in NAC policies; Dynamic port policies (DPP) | FortiGate: `config user nac-policy; edit <POLICY>; set category ems-tag; set ems-tag <TAG>; end` | 7.0.0 or earlier (Matching FortiClient EMS tags in NAC policies) | P7 |
| L2S | `SRG-NET-000715-L2S-000120` | The layer 2 switch must implement physically or logically separate subnetworks to isolate organization-defined critical system components and functions. | Block intra-VLAN traffic; Host quarantine; NAC LAN segments; FortiSwitch VLANs over VXLAN; and 7 more | FortiGate: `config system interface; edit <VLAN_INTERFACE>; set switch-controller-access-vlan enable; end` | 7.0.0 or earlier (Block intra-VLAN traffic) | P7 |
| L2S | `SRG-NET-000760-L2S-000160` | The layer 2 switch must establish organization-defined alternate communications paths for system operations organizational command and control. | Link aggregation group size; LAG min-max bundle; Multi-stage load balancing; VXLAN: ECMP; and 12 more | `config switch trunk; edit <TRUNK>; set mode lacp-active; set members <PORTS>; end` | 7.0.0 or earlier (Link aggregation group size) | — |
| AAA | `SRG-APP-000023-AAA-000030` | AAA Services must be configured to provide automated account management functions. | RADIUS accounting server support | `config user radius; edit <RADIUS>; config acct-server; edit 1; set status enable; set server <IP>; set secret <SECRET>; end; end` | 7.0.0 or earlier (RADIUS accounting server support) | P1 |
| AAA | `SRG-APP-000142-AAA-000020` | AAA Services must be configured to use protocols that encrypt credentials when authenticating clients, as defined in the PPSM CAL and vulnerability assessments. | 802.1X: RadSec (IPv4) | `config user radius; edit <RADIUS>; set transport-type TLS; set radsec-tls-min-ver TLSv1-2; set radsec-cert-validate enable; end` | 7.6.4 and later (802.1X: RadSec (IPv4)) | P1, P3 |
| AAA | `SRG-APP-000158-AAA-000420` | AAA Services used for 802.1x must be configured to uniquely identify network endpoints (supplicants) before the authenticator establishes any connection. | 802.1X MAC-based mode | `config switch interface; edit <PORT>; config port-security; set port-security-mode 802.1X-mac-based; end; set security-groups <GROUP>; end` | 7.0.0 or earlier (802.1X MAC-based mode) | P1, P2 |
| AAA | `SRG-APP-000172-AAA-000520` | AAA Services must be configured to encrypt transmitted credentials using a FIPS-validated cryptographic module. | RADIUS for administrative authentication; 802.1X: RadSec (IPv4) | `config user radius; edit <RADIUS>; set transport-type TLS; set radsec-tls-min-ver TLSv1-2; set radsec-cert-validate enable; end` | 7.6.4 and later (802.1X: RadSec (IPv4)) | P1, P3 |
| AAA | `SRG-APP-000394-AAA-000430` | AAA Services used for 802.1x must be configured to authenticate network endpoint devices (supplicants) before the authenticator establishes any connection. | 802.1X port mode | `config switch interface; edit <PORT>; config port-security; set port-security-mode 802.1X; end; set security-groups <GROUP>; end` | 7.0.0 or earlier (802.1X port mode) | P1, P2 |
| AAA | `SRG-APP-000516-AAA-000440` | AAA Services used for 802.1x must be configured to use secure Extensible Authentication Protocol (EAP), such as EAP-TLS, EAP-TTLS, and PEAP. | EAP pass-through | `config switch interface; edit <PORT>; config port-security; set eap-passthru enable; end; end` | 7.0.0 or earlier (EAP pass-through) | P1 |
| AAA | `SRG-APP-000516-AAA-000640` | AAA Services must be configured to use a unique shared secret for communication (i.e. RADIUS, TACACS+) with clients requesting authentication services. | RADIUS for administrative authentication; TACACS+ for administrative authentication; RADIUS CoA and disconnect messages | `config user radius; edit <RADIUS>; set server <IP>; set secret <SECRET>; end` `config system admin; edit <ADMIN>; set remote-auth enable; set remote-group <GROUP>; end` | 7.2.0 and later (RADIUS for administrative authentication) | P1, P2 |

### Alignment summary

| STIG | Same requirement | Equivalent setting | Partial | Not supported | Not applicable | By procedure | Total |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| N-NDM (V3R6) | 12 | 23 | 6 | 0 | 0 | 1 | 42 |
| N-L2S (V3R4) | 13 | 6 | 1 | 1 | 1 | 0 | 22 |
| N-RTR (V3R4) | 5 | 28 | 10 | 18 | 16 | 1 | 78 |
| **Total** | **30** | **57** | **17** | **19** | **17** | **2** | **142** |

FortiSwitch meets 87 of the 142 NX-OS rules' requirements
with a setting (30 through the feature Chapter 11 maps and 57
through another setting), and 2 more by procedure. 17 are met
only in part, 19 describe capabilities FortiSwitch does not have, and
17 do not apply. As in Chapter 33, most gaps are in the router STIG;
the N-NDM and N-L2S rules, which apply to every switch, are almost all met.
The main differences:

- **Management defaults.** The FortiSwitchOS administrator idle timeout
  defaults to 5 minutes, which already meets `CISC-ND-000720`; NX-OS needs
  `exec-timeout 5` on the console and VTY lines. NX-OS limits concurrent
  VTY sessions with `session-limit`; FortiSwitchOS has no session limit
  (`CISC-ND-000010` is Partial). For `CISC-ND-000150`, FortiSwitchOS locks
  the account after three failures, which is stricter than the NX-OS
  disconnect after `ssh login-attempts 3`.
- **Audit records.** The NX-OS fix texts meet eleven audit rules with RADIUS
  accounting (`aaa accounting default group`), which sends a record of
  each session and command to the server; FortiSwitchOS logs configuration
  changes and logons in its event log, which must be sent off the switch
  (`CISC-ND-001310` and `CISC-ND-001450`). Neither the FortiSwitchOS event
  log nor ACL counters give the full text of each command or a log entry
  per dropped packet (`CISC-ND-000330`, `CISC-ND-000290`, and
  `CISC-RT-000200` are Partial).
- **Where FortiSwitch is weaker.** FortiSwitchOS NTP authentication uses a
  SHA-1 or MD5 keyed digest, where NX-OS 10.5(x) offers AES-128-CMAC
  (`CISC-ND-001150` is Partial). FortiSwitchOS OSPF, RIP, and IS-IS
  authenticate with MD5 only and BGP with a TCP MD5 password, where NX-OS
  key chains offer HMAC-SHA-256 for OSPFv2 (`CISC-RT-000050`), and only
  key-chain protocols carry key lifetimes (`CISC-RT-000030`); there is no
  VRRP authentication (`CISC-RT-000020`). FortiSwitchOS has no control plane
  policing (`CISC-ND-001220`, `CISC-RT-000120`) and no per-algorithm SSH
  list; FIPS-CC mode and `strong-crypto` stand in for `ssh macs` and
  `ssh ciphers`.
- **Where FortiSwitch is stronger or simpler.** FortiSwitchOS syslog can
  use reliable, encrypted transport, its password policy can require
  special characters (which `password strength-check` does not), and it has
  no Telnet or NX-API service to disable. Its `icmp-frag` hardware check
  drops all fragmented ICMP, more than `CISC-RT-000140` asks.
- **MPLS and multicast roles.** As in Chapter 33, the MPLS, LDP, RSVP-TE,
  L3VPN, VPWS, and VPLS rules are Not supported on FortiSwitch, and the PIM
  rendezvous point, SPT, and MSDP rules are Not applicable, because
  FortiSwitchOS multicast routing is PIM-SSM only. On the Nexus side, the
  10.5(x) documentation has no LDP, RSVP-TE, VPWS, or VPLS configuration
  either, so those rows have no NX-OS command.

**FortiLink-managed mode.** When a FortiGate manages the switch, make the
FortiSwitch side of each row under the FortiGate's `config
switch-controller` tree, as in Chapter 33. For example, the port guards
(`CISC-L2-000090`, `CISC-L2-000100`, `CISC-L2-000140`):

FortiGate: `config switch-controller managed-switch; edit <SWITCH_SN>; config ports; edit <PORT>; set stp-bpdu-guard enabled; set stp-root-guard enabled; set ip-source-guard enable; end; end`

The switch's syslog destination (`CISC-ND-001310` and `CISC-ND-001450`):

FortiGate: `config switch-controller remote-log; edit <NAME>; set status enable; set server <SYSLOG_IP>; end`

Settings with no `switch-controller` equivalent, such as the lockout
duration or the DoS checks, can be pushed as a custom command:

FortiGate: `config switch-controller custom-command; edit <CMD_NAME>; set command <SWITCH_CLI_TEXT>; end`

### Collecting evidence

In a mixed estate, keep one checklist row per NX-OS rule for each switch,
with the SRG ID and alignment category from the table, and attach each
platform's evidence:

- **Nexus switches:** `show version` for the release, `show
  running-config` for the settings in the NX-OS column, and `show copp
  status` for the CoPP policy.
- **Standalone FortiSwitches:** `get system status` for the release, and
  `show full-configuration` for the settings in the FortiSwitchOS column,
  with the outputs Chapter 33 lists for the rows they cover.
- **FortiLink-managed FortiSwitches:** the FortiGate's `switch-controller`
  configuration as well as `get system status` from the switch.
- **For every row with prerequisites:** evidence that each prerequisite is
  in place (the server reachable, the license installed, the model listed as
  supported).
- **For every Partial and Not supported row:** the open finding, its
  mitigation, and its approval, recorded against the SRG ID.

Keep the AAA Services and other Chapter 11-only requirements (the second
table) on the FortiSwitch checklist as well (Chapter 03 describes
SRG-based checklists).

## Validation and Troubleshooting

- **A rule seems to have no row.** Every one of the 142 rules has a
  row; the build script fails if one is missing. Search for the rule ID,
  not the title.
- **A Chapter 33 row and a Chapter 37 row for the same rule ID differ.**
  Seven shared rule IDs have a different NX-OS requirement (see *How this
  chapter relates to Chapter 33*); for all the others the FortiSwitch side
  is identical.
- **An NX-OS command is rejected.** Check the release, the platform, and
  whether the `feature` is enabled (`feature dot1x`, `feature interface-vlan`,
  `feature msdp`, and so on). The commands were checked against the 10.5(x)
  documentation; some depend on the line card or the queuing mode (the
  `c-out-8q` classes are the 8-queue egress classes).
- **SPAN sends nothing.** NX-OS creates SPAN sessions shut down; the
  session needs `no monitor session <N> shut`, and the destination port
  needs `switchport monitor`.
- **Syslog or NTP through `mgmt0` fails.** `mgmt0` is in the management
  VRF; add the `use-vrf` option to the server command.
- **An assessor asks for the FortiSwitch STIG rule.** There is none. Show
  the SRG-based checklist, the SRG ID in the table, and the NX-OS rule only
  as the reference that implements the same requirement.
- **Routing adjacencies fail between a Nexus and a FortiSwitch.** A Nexus
  key chain with `HMAC-SHA-256` cannot authenticate to FortiSwitchOS OSPF,
  which supports MD5 only; a mixed adjacency must fall back to MD5, and both
  ends then carry the Partial finding for `CISC-RT-000050`.

## Security and Best Practices

- Treat the NX-OS Switch STIG rules as the minimum checklist for every
  switch, and add the Chapter 11-only requirements for FortiSwitch.
- On Nexus switches, use `aes128cmac` for NTP authentication, HMAC-SHA-256
  key chains for OSPFv2, `ssh macs` and `ssh ciphers` limited to the SHA-2
  MACs and CTR ciphers, and keep the strict CoPP profile.
- On FortiSwitch, set the lockout duration to 900 seconds, keep the
  5-minute idle timeout, set the DoD pre-login banner, use a 15-character
  password policy with all four character classes, and allow only HTTPS
  and SSH from trusted hosts.
- Use two authentication servers, two reliable encrypted syslog servers,
  two authenticated NTP servers, and SNMPv3 with authentication and
  privacy on both platforms.
- On host ports, use 802.1X with MAB, BPDU guard, root guard where switches
  may connect, IP source guard, and storm control; use DHCP snooping and
  dynamic ARP inspection on user VLANs.
- Keep FortiSwitches out of perimeter, MPLS, and multicast rendezvous point
  roles, and record every Partial and Not supported row as an open finding.
- Review the crosswalk whenever DISA updates the NX-OS Switch STIGs or an
  SRG, Cisco releases a new NX-OS train, or Fortinet a new FortiSwitchOS
  version.

## References and Knowledge Checks

**References:**

- DISA Cisco NX-OS Switch NDM STIG V3R6, L2S STIG V3R4, and RTR STIG V3R4
  (`U_Cisco_NX-OS_Switch_Y26M07_STIG.zip`), and the Layer 2 Switch SRG
  V3R4, Network Device Management SRG V5R5, Router SRG V5R2, and AAA
  Services SRG V2R3, from the October 2026 STIG Library Compilation.
- Cisco, *Cisco Nexus 9000 Series NX-OS Command Reference (Configuration
  Commands)*, Releases 10.5(x) and 9.3(x); *Command Reference (Show
  Commands)*, Release 10.5(x); and the Release 10.5(x) Security, System
  Management, Fundamentals, Interfaces, Layer 2 Switching, Unicast Routing,
  Multicast Routing, Quality of Service, and Label Switching Configuration
  Guides.
- Fortinet, *FortiSwitchOS 8.0.0 CLI Reference*, and *FortiOS 8.0.1 CLI
  Reference* (FortiLink managed-mode commands).
- [Chapter 03](03-the-srg-catalog-how-stigs-are-built-and-what-to-do-without-one.md)
  (how STIGs are built from SRGs, and SRG-based assessment),
  [Chapter 07](07-network-device-stigs-management-routing-and-filtering.md)
  (network device STIGs by plane),
  [Chapter 11](11-fortiswitch-feature-version-and-srg-map.md) (the
  FortiSwitch feature and SRG map),
  [Chapter 31](31-cisco-products-stigs-and-srg-mapping.md) (the Cisco STIG
  packages and router roles),
  [Chapter 32](32-cisco-catalyst-switch-feature-version-and-stig-map.md)
  (the IOS XE switch commands, which this chapter does not reuse), and
  [Chapter 33](33-fortiswitch-and-cisco-catalyst-switch-stig-crosswalk.md)
  (the IOS XE switch crosswalk, source of the reused FortiSwitch side).

**Knowledge checks:**

1. Why is it wrong to say a FortiSwitch is compliant with an NX-OS STIG
   rule, and what is the finding recorded against instead?
2. When does this chapter reuse Chapter 33's FortiSwitch side, and why are
   the Cisco commands never reused?
3. Why is `CISC-ND-001150` Same requirement in Chapter 33 but Partial
   here, for the same FortiSwitch setting?
4. Which NX-OS fix text does not meet its own rule because
   `password strength-check` does not require special characters?
5. What must be added to the DISA SPAN example before an NX-OS session
   copies any traffic?
6. How do vPC and MCLAG differ in name and configuration, and which rules
   apply to both members of the pair?
7. Why do the MPLS LDP and VPLS rules have no NX-OS command in this
   chapter?

## Summary and Completion Checklist

There is no FortiSwitch STIG, so a FortiSwitch is assessed against the
SRGs, and the Cisco NX-OS Switch STIGs implement those same SRGs. This
chapter aligns all 142 NX-OS rules (42 N-NDM, 22
N-L2S, and 78 N-RTR) with a corrected Nexus 9000 command and with
the FortiSwitch setting and FortiSwitchOS command that meet the same SRG
requirement: 30 through the feature Chapter 11 maps, 57 through
another setting, 2 by procedure, 17 only in part, 19 not
supported, and 17 not applicable. 120 rows reuse Chapter
33's FortiSwitch side, and 22 were aligned here. It also lists the
25 FortiSwitch requirements that no NX-OS rule covers. Every
NX-OS and FortiSwitchOS command was checked by script against the
vendor's documentation.

- [ ] Can explain why FortiSwitch is assessed against SRGs and the NX-OS
  rules are only a reference.
- [ ] Can explain which rows Chapters 33 and 37 share and why the Cisco
  commands differ.
- [ ] Can find an NX-OS rule in the crosswalk and configure both the NX-OS
  command and the FortiSwitch setting.
- [ ] Can assign and record the alignment category for each rule, and
  check a row's FortiSwitch prerequisites before its setting.
- [ ] Can apply the rules to vPC and MCLAG pairs and VXLAN fabrics.
- [ ] Can add the Chapter 11-only requirements to a FortiSwitch checklist.
