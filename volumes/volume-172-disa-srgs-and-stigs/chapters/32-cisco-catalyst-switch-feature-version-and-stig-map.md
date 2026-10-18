# Chapter 32: Cisco Catalyst Switch Feature, Version, and STIG Map

## Learning Objectives

- Find the Cisco IOS XE release that introduced a given Catalyst 9000
  switch feature, from the Catalyst 9300 release notes.
- Map each Catalyst switch feature to the rule of the Cisco IOS XE Switch
  NDM, L2S, or RTR STIG that it satisfies.
- Find every one of the 152 IOS XE Switch STIG rules in the map, with its
  severity and the SRG requirement it implements.
- Use each STIG rule's fix text as the command to configure it, and
  recognize the fix texts that do not parse or no longer match the
  IOS XE command references.
- Decide which RTR rules apply to a switch from its role: routed access or
  distribution switch, perimeter switch, or provider edge (PE) switch.
- Record the requirements that the fix text cannot meet exactly, with
  their mitigations.

## Theory and Architecture

The Cisco Catalyst 9000 family (Catalyst 9200, 9300, 9400, 9500, and 9600)
is Cisco's current campus switching line. Every model runs **Cisco IOS XE**,
the same operating system as Cisco's enterprise routers, so a Catalyst 9000
switch can be a pure Layer 2 access switch, a routed distribution or core
switch, or, on the larger models, an MPLS provider edge. The DISA
**Cisco IOS XE Switch STIG** package covers these switches; its overview
names the Catalyst 3650 and 3850 as well as the 9000 Series (Chapter 31).
The package holds three STIGs, one for each plane that Chapter 07
describes: **NDM** for the management plane, **L2S** for switching and port
security, and **RTR** for routing and traffic filtering. This chapter is
the Cisco counterpart of the Fortinet feature maps in Chapters 11 to 30,
built the same way as the FortiGate map in Chapter 30: for every Catalyst
switch feature it gives **which IOS XE release introduced it**, **which STIG
rule it relates to**, and **which command configures it to meet that
rule**. [Chapter 11](11-fortiswitch-feature-version-and-srg-map.md) is the
FortiSwitch map, for comparison; FortiSwitch has no STIG and is mapped to
the SRGs instead.

The IOS XE command line is mode based, which matters for every command in
the map:

- **Global configuration** (`Device(config)#`) holds the device-wide
  settings: AAA, the password policy, logging, NTP, SNMP, services, the
  banner, spanning tree mode, DHCP snooping, and the routing processes.
- **Interface configuration** (`Device(config-if)#`, or
  `Device(config-if-range)#` after `interface range`) holds the per-port
  settings: access or trunk mode, VLANs, 802.1X, spanning tree guards,
  storm control, IP Source Guard, ACLs, and the ICMP options.
- **Line configuration** (`Device(config-line)#`) holds the console and
  VTY settings: the idle timeout, the transport (SSH only), the access
  class, and the login method list.
- **Submodes** hold the settings of one object: an access list
  (`config-ext-nacl`), the configuration change logger
  (`config-archive-log-cfg`), the AAA common criteria password policy
  (`config-cc-policy`), a RADIUS server (`config-radius-server`), a key
  chain key (`config-keychain-key`), a QoS policy map class
  (`config-pmap-c`), or a BGP process (`config-router`).

Most STIG rules come down to a handful of global settings, the VTY lines,
and the interface settings of host-facing ports, trunks, and external
routed interfaces.

### Where the version data comes from

Cisco publishes one set of release notes per platform and release train:
"Release Notes for Cisco Catalyst 9300 Series Switches, Cisco IOS XE
<release>", with the Catalyst 9200, 9400, 9500, and 9600 equivalents. Each
has a **What's New** section with a **Software Features** table for every
release in the train (17.12.1, 17.12.2, and so on). The version column was
built from the **Catalyst 9300 release notes as the version spine**,
because they cover every IOS XE 17 train and the trains after it: the 18
release notes for 17.1.x through 17.18.x and the release notes for 26.1.x
and 26.2.x, which follow 17.18.x, 20 in all. Their software feature tables
run from 17.1.1 to 26.2.1. Cisco still publishes 16.x release notes for
the Catalyst 9300; they are outside the 17.x scope of this map and were
not used.

cisco.com refuses scripted downloads, so the release notes were opened in
a browser and their software feature tables were read in the page: only the
rows under each "Software Features in Cisco IOS XE <release>" heading,
which gives 305 entries. A table cell that lists several features under one
heading (for example *Programmability* followed by *gNMI Dial-Out
Telemetry*, *PROTO Encoding*, and *YANG Data Models*) gives one feature per
item, named "<heading>: <item>". The rows under a table's *Serviceability*
heading (20 new or changed show and debug commands) are not features and
were left out; the rows under *New on the WebUI* are kept with the prefix
*Web UI:*. One cell has no feature name and was named from its
description (*Programmability: Candidate configuration confirmed commit*,
17.1.1). A feature listed in more than one release (usually a feature
added to an older train's later release, such as *Shutdown Fiber Ports
with no SFP Inserted* in 17.15.2 and 17.16.1) is one row, so the 305
entries make **280 features**. The release notes have no categories,
so each feature was given one of the chapter's categories by keyword,
with a few corrections by hand.

The table has two groups of rows:

- **Core platform features** (categories starting with *Core:*) are the
  long-standing capabilities that the STIG rules depend on: management
  access, AAA, the password policy, logging, time, SNMP, backups,
  certificates, services, 802.1X and the Layer 2 protections, QoS, ACLs,
  routing and its protections, BGP, MPLS and VPLS, and multicast. They
  existed before 17.1.1 and are not in any release notes' feature table.
- **Listed features** are every feature in the 20 release notes, grouped
  under the chapter's categories (*Device hardening*, *AAA and 802.1X*,
  *TrustSec*, *MACsec*, *Access lists and first-hop security*, *Layer 2 and
  VLANs*, *QoS*, *IP routing*, *IP multicast and services*, *MPLS, VPLS, and
  L2VPN*, *BGP EVPN VXLAN and fabric*, *IPsec and tunnels*, *Timing*,
  *System, stacking, and high availability*, *Monitoring and
  troubleshooting*, *Programmability*, *Application hosting*, *Licensing
  and cloud management*, and *Web UI*). Within a category the rows are
  sorted by release.

| Version entry | Meaning |
| --- | --- |
| `17.1.1 or earlier` | A core platform feature, present in 17.1.1 and earlier releases |
| `17.10.1 and later` | First listed in 17.10.1 (listed in one release only) |
| `17.15.2+; 17.16.1+` | Listed in several releases: first listed in each train at the release shown (often a feature added to an older train's later release); the first release in each train is shown |
| `17.11.99SW+` | A release that the 17.11.x release notes list under its own heading, with Cisco's name for it (17.11.99SW) |

Three cautions apply. First, the column says when a feature first appeared
in the **Catalyst 9300** release notes. Features differ by model, and the
Catalyst 9200, 9400, 9500, and 9600 have their own release notes, which
can list a feature in a different release or not at all. Check the release
notes for your model, or Cisco Feature Navigator, before relying on a
release. Second, "and
later" means later releases in the same train and, usually, later trains;
a feature first listed in a train's later release may reach a newer train
only in that train's later releases. Third, many features depend on the
license level (Network Essentials or Network Advantage in most entries,
and the Cisco Switching Licensing levels from 26.2.1) shown in each
release notes entry.

### Where the STIG and SRG data comes from

The requirement column uses the October 2026 DISA library. The three STIGs
come in one package, `U_Cisco_IOS-XE_Switch_Y26M04_STIG.zip`, and are the
only requirements in the map:

| Column | STIG | Release | Applies to |
| --- | --- | --- | --- |
| **C-NDM** | Cisco IOS XE Switch NDM STIG | V3R6, benchmark date 01 Apr 2026; 42 rules (8 CAT I, 34 CAT II) | The management plane: session limits and timeouts, management ACLs, lockout, the banner, AAA and two authentication servers, the account of last resort, the password policy and password storage, the configuration change logger, logging and two syslog servers, NTP, SNMPv3, SSH, backups, certificates, services, and supported software |
| **C-L2S** | Cisco IOS XE Switch L2S STIG | V3R2, benchmark date 02 Jul 2025; 22 rules (1 CAT I, 17 CAT II, 4 CAT III) | Switching: 802.1X and MAB, VTP authentication, QoS, root guard, BPDU guard, loop guard, unknown unicast flood blocking, DHCP snooping, IP Source Guard, dynamic ARP inspection, storm control, IGMP snooping, Rapid STP, UDLD, trunks, and VLAN assignment |
| **C-RTR** | Cisco IOS XE Switch RTR STIG | V3R4, benchmark date 01 Apr 2026; 88 rules (8 CAT I, 52 CAT II, 28 CAT III) | Routing and filtering: ACLs, routing protocol authentication, control plane policing, ICMP and ARP options, perimeter filtering, BGP, MPLS, L3VPN, VPWS, VPLS, multicast, MSDP, and IPv6 |

The STIG rules have IDs of the form `CISC-ND-nnnnnn`, `CISC-L2-nnnnnn`,
and `CISC-RT-nnnnnn`, and the map cites them by that rule version, as the
XCCDF gives it. The NDM rule numbers are shared with the other Cisco NDM
STIGs (Chapter 31), so one set of management procedures can serve a mixed
Cisco estate. The Requirement reference table adds each rule's
severity (high = CAT I, medium = CAT II, low = CAT III) and the SRG
requirement it implements (the XCCDF group title), so C-NDM
`CISC-ND-000150` shows that it implements NDM SRG requirement
`SRG-APP-000065-NDM-000214`. **All 152 rules appear in the map**, each
attached to the core or listed feature that satisfies it; the build script
fails if one is missing. No SRG is needed for functions outside the three
STIGs, because the RTR STIG already covers routing, MPLS, and multicast;
functions the STIGs do not name (TrustSec, MACsec, IPsec, application
hosting) fall under the NDM rule on unnecessary functions when unused.

The RTR STIG applies its rules by the switch's role, as Chapter 31
explains for routers:

- **Every routed switch**: ACLs between subnets, routing protocol
  authentication, control plane policing, inactive interfaces, ICMP and
  ARP options, CEF, and the IPv6 rules that are not perimeter rules.
- **Perimeter switch** (21 rules, titled "The Cisco perimeter
  switch"): only a switch that connects an enclave to an external network,
  such as NIPRNet or SIPRNet. These rules deny traffic by default, block
  bogons and IP options, filter egress and spoofed traffic, suppress LLDP,
  CDP, proxy ARP, and router advertisements on external interfaces, block
  outbound management traffic, and filter IPv6 extension headers. On an
  internal campus switch they are Not Applicable.
- **PE switch** (14 rules, titled "The Cisco PE switch"): only a
  switch that gives customers MPLS L3VPN, VPWS, or VPLS services on a
  backbone. These rules bind VRFs, route targets, and route
  distinguishers, set VC and VPN IDs, and protect the core.
- **Function rules**: the BGP, MPLS, RSVP-TE, multicast (PIM, RP, DR), and
  MSDP rules apply only when the switch runs that protocol.

Record the role of each switch on its checklist before assessing, so the
role-specific rules are marked Not Applicable consistently.

Each feature maps to one of three kinds of relationship:

- **Implements a rule.** The feature is how the switch meets a rule. The
  configuration change logger records every configuration command
  (C-NDM `CISC-ND-000330`), for example.
- **Must be configured to meet a rule.** The feature is in scope of a rule
  and has to be set up correctly. The AAA common criteria policy must
  require 15 characters (C-NDM `CISC-ND-000550`), for example.
- **No direct rule.** The feature is operational or belongs to a function
  the STIGs do not name, such as a programmability interface, a fabric
  option, or a licensing change. It has no rule of its own, but if it is
  not needed it falls under the NDM rule that implements the NDM
  requirement to prohibit unnecessary and nonsecure functions and services:
  C-NDM `CISC-ND-000470`, a CAT I rule that implements
  `SRG-APP-000142-NDM-000245`. Those rows read "No direct requirement; if
  unused, disable (C-NDM `CISC-ND-000470`)".

The mapping is a starting point for an assessment, not a ruling. Confirm it
with your assessor, especially the placements of listed features.

### Where the commands come from

Each STIG rule has a vendor-specific check and fix, so the **fix text of
the rule is the authority for the command** wherever it gives one: the
command cell repeats the fix text's commands, with its example names kept
and its addresses and secrets replaced by placeholders in angle brackets.
Every command was then checked by a script against the newest Cisco
documentation for the Catalyst 9300: the **Command Reference, Cisco IOS XE
26.x.x (Catalyst 9300 Switches)**, the fifteen **Catalyst 9300 26.x.x
configuration guides** (Security, System Management, Layer 2, VLAN, IP
Routing, IP Addressing Services, IP Multicast Routing, MPLS, QoS, Network
Management, Interface and Hardware, Stacking and High Availability, Cisco
TrustSec, Bonjour, and BGP EVPN VXLAN), and the platform-independent Cisco
IOS XE command references that the 9300 command reference leaves out
(Security A to Z, Configuration Fundamentals, Embedded Syslog Manager,
Basic System Management, SNMP, HTTP Services, IP Addressing and
Application Services, IPv6, BGP, OSPF, Protocol-Independent Routing, MPLS,
LAN Switching, QoS, Embedded Event Manager, Interface and Hardware, IP
Switching, and Carrier Ethernet). The script follows the IOS XE modes: each
block starts in global configuration (or in privileged EXEC for `show` and
`install`), and `interface`, `line`, `router`, `ip access-list`,
`archive`, `log config`, `radius server`, `key chain`, `policy-map`, and
the other mode commands move into their submode until `exit`. A statement
passes when it is a documented command line in the same mode (an example
with a `Device(config-if)#` prompt, for instance), when a documented
command in a compatible mode has all of its keywords, when its keywords are
in the command's own article (or, for a submode option such as `min-length`,
in the article of the command that opened the submode), when a
configuration guide procedure gives it, or when it appears word for word in
the documentation (a running configuration that shows `no service pad`, for
example). The final run checked 94 command blocks and
386 statements with no failures: 279 matched a documented
example in the same mode, 64 matched a command's syntax,
23 a command's article, 3 a configuration guide
procedure, and 15 the documentation text; 2 are the
documented exceptions below. Read the column this way:

- Commands are entered in global configuration mode (`configure
  terminal`) unless the block starts with `show` or `install`. Each pair
  of backticks is one block; statements are separated by `;` to fit in a
  table cell, and on the CLI each one goes on its own line. A mode command
  (`interface range <HOST_PORTS>`, `line vty 0 31`) applies to the
  statements after it, up to the next mode command or `exit`. Values in
  `<ANGLE_BRACKETS>` are placeholders.
- For **"No direct requirement"** rows, a dash (**—**) means there is
  nothing to configure for the rule: turn the feature off, or do not
  configure it, if it is not used.
- A dash in a mapped row means the feature meets the rule by default (the
  Resilient Infrastructure changes, for example), or, where the cell says
  so, that the 26.x documentation has no CLI for it.

The STIG fix text is an example, and many examples need correcting. These
are the corrections in the map, and the rules that cannot be met exactly
with the documented commands. Record them on the checklist, with the
mitigation:

- **`iip ssh`.** The fix text for C-NDM `CISC-ND-001200` and C-NDM
  `CISC-ND-001210` begins `iip ssh server algorithm`, a typing error; the
  command is `ip ssh server algorithm mac` and `ip ssh server algorithm
  encryption`.
- **`char-changes`.** The fix text for C-NDM `CISC-ND-000610` sets
  `char-changes 8` in the common criteria policy. The 26.x command
  reference lists the option as `char-change` (the number of characters
  that must change between the old and new password, 1 to 64). The map
  uses `char-change 8`.
- **VTY line ranges.** The fix texts for C-NDM `CISC-ND-000010`, C-NDM
  `CISC-ND-000140`, C-NDM `CISC-ND-000720`, and C-NDM `CISC-ND-001370`
  configure `line vty 0 1` and `line vty 2 4`. From 17.1.1 the default
  number of VTY lines is 32 (the 17.1.x release notes), so lines 5 to 31
  would be left with no access class, timeout, or method list. The map
  uses `line vty 0 31` and `line vty 2 31`. The fix text for
  C-NDM `CISC-ND-000010` also shows `transport input` at the global
  configuration prompt; it is a line configuration command.
- **RADIUS group prompts and `aaa new-model`.** The fix text for
  C-NDM `CISC-ND-001370` shows `server name` at the global configuration
  prompt; it is entered under `aaa group server radius` (the
  `config-sg-radius` submode). AAA method lists also need `aaa new-model`
  first, which the fix text leaves out; the map adds it. Unlike the fix
  text that Chapter 31 describes, this one writes `aaa authentication login
  CONSOLE` with the `login` keyword.
- **`authorization bypass`.** The fix text for C-NDM `CISC-ND-001410`
  enters `authorization bypass` as an applet command. In the 26.x command
  reference it is a keyword of `event manager applet <name>`
  (`event manager applet BACKUP_CONFIG authorization bypass`), which the map
  uses.
- **Trustpoint mode.** The fix text for C-NDM `CISC-ND-001440` gives only
  `enrollment url`, a trustpoint submode command; the map adds `crypto pki
  trustpoint <TRUSTPOINT>` before it.
- **Services that are not documented.** Of the services in the fix text
  for C-NDM `CISC-ND-000470`, `no ip boot server` is in none of the
  downloaded references and is left out. `no ip identd`, `no service
  finger`, `no service pad`, and `no service call-home` are documented only
  in running configurations and the `show auto secure config` output, not
  as commands with syntax. The CNS commands in the fix text for
  C-RTR `CISC-RT-000090` (`no cns config initial`, `no cns exec`, and the
  others) are in none of the downloaded references; the map keeps the
  documented `no boot network` and `no service config`. Check that `show
  running-config` has no `cns` lines.
- **Account of last resort.** The fix text for C-NDM `CISC-ND-000490`
  creates the account with `password`. The map uses `secret`, so that the
  account is stored as a hash (C-NDM `CISC-ND-000620`). The command
  reference documents `common-criteria-policy` and `secret` as options of
  `username` but prints no example that combines them; if the switch
  rejects the combination, keep `secret` and enforce the policy on the
  account by procedure.
- **Enable password and the password policy.** From 17.8.1 the
  common criteria policy can apply to the enable password
  (`enable common-criteria-policy PASSWORD_POLICY password <PASSWORD>`),
  but the command reference says that the option is not supported for
  `enable secret`, and `enable password` is not stored as a hash. Keep
  `enable secret` (C-NDM `CISC-ND-000620`), which takes precedence, and
  meet C-NDM `CISC-ND-000550` for it by procedure.
- **Login failure logging.** C-NDM `CISC-ND-001260` uses `login on-failure
  log` and `login on-success log`. The 26.x documentation shows `login
  on-success log` in running configurations and names `login on-failure`
  in the `show login` description, but gives no syntax or example for
  `login on-failure log`; it is kept from the fix text as an exception.
- **802.1X without MAB.** The fix text for C-L2S `CISC-L2-000020` says MAC
  Authentication Bypass must be configured for devices that cannot do
  802.1X, but its example has no MAB command; the map adds `mab` to the
  host-facing ports.
- **Storm control keyword.** The fix text for C-L2S `CISC-L2-000160` writes
  `storm-control unicast bps 62000000`; the syntax is `storm-control
  unicast level bps <rate>`, as its own broadcast line has it. The fix
  text for C-RTR `CISC-RT-000700` sets `storm-control broadcast cir` under
  a service instance, which none of the references documents; the map
  sets interface storm control on the CE-facing port instead.
- **BGP and key chain authentication.** The fix text for C-RTR
  `CISC-RT-000050` gives a BGP example with TCP-AO (`neighbor <ip> ao
  <key-chain>`), which none of the downloaded references documents, and
  the OSPF key chain example. The map gives the OSPF key chain. The BGP
  example also writes `cryptographic-algorithm hmac-sha256`; the
  documented value is `hmac-sha-256`. Both examples set the key lifetime
  with `duration 180`, but `duration` is in seconds, so a 180-day key is
  `duration 15552000`. For BGP, `neighbor <ip> password` (C-RTR
  `CISC-RT-000480`) is documented but uses MD5, which is not a FIPS 198-1
  algorithm; record BGP as a finding unless TCP-AO is confirmed on your
  release.
- **BGP prefix filter examples.** The fix text for C-RTR `CISC-RT-000500`
  enters `switch bgp xx` (the command is `router bgp`), the fix text for
  C-RTR `CISC-RT-000510` defines `PREFIX_FILTER_CUST1` but applies
  `FILTER_PREFIXES_CUST1`, the fix text for C-RTR `CISC-RT-000530` puts a
  space in `FILTER _CORE_PREFIXES`, and the fix text for C-RTR
  `CISC-RT-000490` lists `240.0.0.0/4` twice. The map uses one prefix list
  name throughout.
- **MSDP outbound filter.** The fix text for C-RTR `CISC-RT-000930` builds
  an outbound SA filter but applies it with `ip msdp sa-filter in`; the map
  uses `ip msdp sa-filter out`.
- **RSVP rate limit.** The fix text for C-RTR `CISC-RT-000610` adds `limit
  50` to `ip rsvp signalling rate-limit`, but the documented syntax has
  only `burst`, `maxsize`, and `period`; the map leaves it out.
- **Core ACL with no permit.** The fix text for C-RTR `CISC-RT-000730`
  builds `BLOCK_TO_CORE` with a single `deny` entry, so the implicit deny
  would drop all traffic from the customer; the map adds `permit ip any
  any` after it.
- **IPv6 extension header filters.** The fix texts for C-RTR
  `CISC-RT-000394` to C-RTR `CISC-RT-000398` write `deny hbh any any
  dest-option log` and `deny 60 any any dest-option log`. In the IPv6
  access list syntax `hbh` and `dest-option-type` are matching keywords
  after the addresses, not a protocol and a `dest-option` keyword; the map
  uses `deny ipv6 any any hbh log` and `deny ipv6 any any dest-option-type
  log`. The fix texts for C-RTR `CISC-RT-000393` to C-RTR `CISC-RT-000398`
  also apply `ipv6 traffic-filter FILTER_IPV6` with no direction; the
  syntax requires `in` or `out`, and the map uses `in`.
- **Management ACL port.** In the management ACL for C-RTR
  `CISC-RT-000450` the map writes the SNMP port as `161`, because the
  `permit` article does not list the `snmp` port name; the outbound ACL
  for C-RTR `CISC-RT-000390` keeps the fix text's port names, which the
  `deny` article lists.
- **Commands not found in the downloaded references.** `ip pim
  neighbor-filter` (C-RTR `CISC-RT-000800`) is kept from the fix text as
  an exception: the Cisco IOS IP Multicast Command Reference returned HTTP
  404, and the 9300 references document only the IPv6 form. `ip igmp
  snooping` and `ipv6 mld snooping` under `bridge-domain` (C-RTR
  `CISC-RT-000710`) are documented as global commands; the bridge-domain
  form comes from the fix text and was not confirmed in that mode.
- **No CLI for some listed features.** The release notes list the RADIUS
  Message Authenticator attribute (17.18.1), TLS for TACACS+ (17.18.1), and
  Strict-KEX for SSH (17.17.1), but the 26.x configuration guides give no
  command for them; check the release's configuration guide before relying
  on them as evidence.
- **Supported software.** C-NDM `CISC-ND-001470` is met by procedure: run a
  release inside Cisco's support lifecycle, check it with `show version`,
  and upgrade with `install add file <IMAGE> activate commit`.
- **No SCAP benchmark.** The IOS XE Switch STIGs are manual, so every rule
  is checked by hand or by a script against the running configuration.

### Prerequisites

A Catalyst switch setting often meets its rule only if something else is
already in place. A **prerequisite** is anything that must exist or be
configured *before* a row's command can meet the rule: a license level
(Network Advantage), an external server (RADIUS, TACACS+, syslog, NTP, an
SNMP manager, an SCP server, a file server for software images, a DHCP
server), certificates from the DoD PKI, a management network, the devices
at the other end of a link (a VTP domain, a UDLD neighbor, routing peers
with matching keys), or an earlier setting the row depends on (AAA, the
password policy, the RADIUS server group, the VLANs, DHCP snooping before
IP Source Guard and dynamic ARP inspection, IP routing, Cisco Express
Forwarding, an MPLS core, IP multicast routing). Settings that the row's
own command creates are not listed again, and neither are the switch
itself, its interfaces, and its base license, which every row depends on.

The 30 prerequisites are listed once, with IDs, in *Cisco Catalyst
switch prerequisites*, and the feature map names the IDs each row needs in
its **Cisco Catalyst switch prerequisites** column. The list is written for
the product, not for this chapter's rows, so the Catalyst crosswalks can
use the same IDs. A dash means the feature needs nothing beyond the switch.
"No direct requirement" rows always show a dash, because their entry turns
the feature off or leaves it unconfigured, and so do the six rows whose
only rule is the disable rule (C-NDM `CISC-ND-000470`, the rule to prohibit
all unnecessary and nonsecure functions and services). The rules that turn
off one named function (zero-touch deployment, C-RTR `CISC-RT-000090`;
gratuitous ARP, directed broadcast, and ICMP messages; the auxiliary port;
LLDP, CDP, and proxy ARP on external interfaces; TTL propagation; PIM on
interfaces that do not need it) are specific settings and are not treated
as disable rules, and neither are the rules on inactive Layer 3 interfaces
(C-RTR `CISC-RT-000060`) and disabled ports in an unused VLAN (C-L2S
`CISC-L2-000210`). Four conventions keep the column readable:

- **License.** Network Advantage (P1) is listed on the rows of the
  features that the Catalyst 9300 documents name as Network Advantage only:
  the OSPF and BGP rows, MSDP, Management Traffic Control, reflexive access
  lists, and IGMP and MLD snooping over VPLS.
- **Servers and peers.** Each external server is listed on the rows that
  connect to it, and the devices at the other end of a link on the rows
  whose setting must match theirs: the VTP domain (P15), the UDLD neighbor
  (P21), and the routing peers with the same keys (P26).
- **Management and AAA.** The SSH keys (P2) are listed on every row that
  uses the SSH server or Secure Copy, the management network (P3) on the
  rows that name the management interface, subnet, or VRF, AAA (P4) on the
  rows whose AAA commands do not enable it themselves, and the RADIUS
  servers (P5) on every row that uses RADIUS.
- **Earlier settings.** IP Source Guard and dynamic ARP inspection list the
  DHCP server and trusted ports (P17), DHCP snooping on the VLANs (P18),
  the binding database agent (P19), and the static bindings (P20); the
  routed rows list IP routing (P22); uRPF lists Cisco Express Forwarding
  (P24); and the MPLS, PE, and multicast rows list the MPLS core (P28) and
  IP multicast routing (P30) they build on.

The **license** entries come from the Catalyst 9300 documents this chapter
uses: the license level in each release notes entry (*Management Traffic
Control*, *Reflexive Access Lists (IPv4)*, *IGMP (IPv4) : VPLS Layer 2
Snooping*, and *MLD Snooping over VPLS* are marked Network Advantage), the
IP Routing Configuration Guide (with Network Essentials only default
routing, static routing, and RIP run, and MSDP needs the Network Advantage
feature set), and the Stacking and High Availability Configuration Guide
(every stack member runs the active switch's license level). Features that
the release notes mark "Network Essentials and Network Advantage" need no
prerequisite beyond the base license. **Model support** is not in the
list: the documents behind this chapter are the Catalyst 9300 release
notes, configuration guides, and command reference, which do not compare
the Catalyst 9200, 9400, 9500, and 9600. Check the release notes for your
model and release, and Cisco Feature Navigator, before you plan on a
licensed or model-specific feature.

During an assessment, check a row's prerequisites before its command: a
correctly configured setting with a missing prerequisite (OSPF
authentication on a switch with only Network Essentials, an 802.1X port
with no reachable RADIUS server, IP Source Guard with no DHCP snooping
database agent, an NTP key that the servers do not share, certificate
enrollment with the system clock not set) does not meet the rule, and the
missing prerequisite is the finding.

## Design Considerations

- **Pick the release first, then the features.** A design that needs a
  feature first listed in a certain release (the enable password policy in
  17.8.1, password combination rules in 17.10.1, management traffic control
  in 17.13.1, or HTTPS disabled by default in 26.2.1) sets the minimum IOS
  XE release, and it must be a supported release (C-NDM `CISC-ND-001470`,
  CAT I).
- **Assign the role before the RTR STIG.** An access switch with no routed
  interfaces needs the NDM and L2S STIGs only; a routed switch adds the
  general RTR rules; only a perimeter or PE switch takes the role rules.
  Record the role on the checklist.
- **Treat the STIGs as the floor, not the scope.** Every function you
  enable brings rules with it, and every function you leave off shrinks
  the assessment; the NDM rule on unnecessary functions (C-NDM
  `CISC-ND-000470`, CAT I) requires it anyway.
- **Separate management from data.** Use the dedicated management port in
  the management VRF where the model has one, restrict the VTY lines with
  an access class, allow only SSH, and keep management traffic off the
  default VLAN (C-L2S `CISC-L2-000240`).
- **Authenticate administrators centrally.** Use two RADIUS or TACACS+
  servers (C-NDM `CISC-ND-001370`, CAT I) with one local account of last
  resort (C-NDM `CISC-ND-000490`), and the same servers for 802.1X on the
  access ports (C-L2S `CISC-L2-000020`, CAT I).
- **Log twice.** Two syslog servers are a CAT I rule (C-NDM
  `CISC-ND-001450`); keep a local buffer as well (C-NDM `CISC-ND-000980`).
- **Template the access ports.** The L2S rules are mostly per-port
  settings: an interface template or a configuration management tool keeps
  802.1X, BPDU guard, storm control, IP Source Guard, and the VLAN settings
  the same on every host-facing port.

## Implementation and Automation

### Cisco Catalyst switch prerequisites

What must be in place before the Catalyst switch features in the feature
map can meet their rules (see *Prerequisites*). The commands were verified
against the Catalyst 9300 26.x.x command reference and configuration
guides and the Cisco IOS XE command references with the same checks as the
feature map; entries that are not switch settings are described in words.

[Download the prerequisites as CSV](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/data/volume-172-disa-srgs-and-stigs/32-cisco-catalyst-switch-feature-version-and-stig-map-prerequisites.csv) (30 rows).

| ID | Prerequisite | What it enables | How to put it in place | Source |
| --- | --- | --- | --- | --- |
| P1 | Network Advantage license on the switch (on a stack, the active switch, with every member at the same license level) | OSPF and BGP (with Network Essentials only default routing, static routing, and RIP run), MSDP, Management Traffic Control, reflexive access lists, and IGMP and MLD snooping over VPLS | `license boot level network-advantage`, save the configuration and reload, then check with `show license summary` | IP Routing Configuration Guide, *Configuring IP Unicast Routing* (supported protocols by license level) and *Configuring MSDP* (Network Advantage feature set); Stacking and High Availability Configuration Guide, *Prerequisites for Switch Stacks*; RN entries marked Network Advantage: *Management Traffic Control* (17.13.1), *Reflexive Access Lists (IPv4)* (17.10.1), *IGMP (IPv4) : VPLS Layer 2 Snooping* (17.1.1), and *MLD Snooping over VPLS* (17.6.1); CR, *license boot level* |
| P2 | SSH server keys: a hostname, an IP domain name, and an RSA key pair of at least 2048 bits | The SSH server (SSH-only VTY lines, the SSH algorithms, NETCONF over SSH) and Secure Copy, which relies on SSH | `hostname <HOSTNAME>; ip domain name <DOMAIN_NAME>; crypto key generate rsa modulus 2048`, then check with `show ip ssh` | Security Configuration Guide, *Prerequisites for Configuring Secure Shell* (RSA key pair, hostname and host domain, encryption image); System Management Configuration Guide, *Prerequisites for Secure Copy*; RN, *Deprecation of Weak Ciphers* (17.11.1: minimum RSA key pair size 2048 bits) |
| P3 | A management network: the Ethernet management port (GigabitEthernet0/0, a port in the Mgmt-vrf VRF) or a management SVI, with an address and the management subnet defined | Management access lists, VTY access classes, Management Traffic Control, and RADIUS testing in a non-default VRF | `interface GigabitEthernet0/0; vrf forwarding Mgmt-vrf; ip address <MGMT_IP_ADDRESS> <MASK>` | Interface and Hardware Components Configuration Guide, *Configuring Ethernet Management Port* (prerequisite: assign an IP address; the port is a VRF interface); Cisco TrustSec Configuration Guide, *Cisco TrustSec Overview* (VRF-aware automated tester needs a source interface in the VRF); feature map rows *Management access list on the VTY lines* and *Out-of-band management interface and management ACLs* |
| P4 | AAA enabled (the AAA new model), with an exec authorization method for Secure Copy | AAA common criteria password policies, the enable password policy, AAA login method lists, and the Secure Copy server | `aaa new-model; aaa authorization exec default group RADIUS_GROUP local` | CR, *enable password* (aaa new-model and aaa common-criteria policy must be configured before the common-criteria-policy option) and *aaa common-criteria policy* (example); System Management Configuration Guide, *Prerequisites for Secure Copy* (configure SSH, authentication, and authorization) |
| P5 | Two reachable RADIUS servers (for example Cisco ISE), each with its own shared secret, defined on the switch in a RADIUS server group | Administrator authentication with the local account as fallback, 802.1X and MAB, the RADIUS automated tester, and the RADIUS Message Authenticator attribute | An organization RADIUS service, then `aaa new-model; radius server RADIUS1; address ipv4 <RADIUS_1_IP> auth-port 1812 acct-port 1813; key <KEY>; exit; radius server RADIUS2; address ipv4 <RADIUS_2_IP> auth-port 1812 acct-port 1813; key <KEY>; exit; aaa group server radius RADIUS_GROUP; server name RADIUS1; server name RADIUS2` | Security Configuration Guide, *Prerequisites for Configuring RADIUS* (RADIUS and AAA must be enabled) and *Configuring IEEE 802.1x Port-Based Authentication* (Cisco ISE as the authentication server); RN, *Message authenticator attribute in RADIUS* (17.18.1); feature map row *AAA with two RADIUS servers and the local account as fallback* |
| P6 | A TACACS+ server that supports TACACS+ over TLS, and the certificates for the TLS connection | TLS for TACACS+ | An organization TACACS+ service with TLS; the 26.x guides give no switch command for it (see *Where the commands come from*) | Security Configuration Guide, *Configuring TACACS+* (prerequisites; feature history: TACACS+ over TLS, 17.18.1, certificate-based AAA services); RN, *TLS for TACACS+* (17.18.1) |
| P7 | The AAA common criteria password policy PASSWORD_POLICY | The local account and the enable password created under the policy, and the added combination rules | `aaa new-model; aaa common-criteria policy PASSWORD_POLICY; min-length 15; upper-case 1; lower-case 1; numeric-count 1; special-case 1; char-change 8` | CR, *enable password* and *username*; feature map row *Password policy (AAA common criteria policy)* |
| P8 | 802.1X authentication on the switch (the dot1x method list and system authentication control), and endpoints with 802.1X client software or MAC addresses known to the RADIUS server for MAB | 802.1X and MAC Authentication Bypass on the host-facing ports | `aaa authentication dot1x default group RADIUS_GROUP; dot1x system-auth-control`, with an 802.1X supplicant on each endpoint that supports one | Security Configuration Guide, *Configuring IEEE 802.1x Port-Based Authentication* (method list; clients with 802.1x-compliant client software; MAC authentication bypass); feature map row *IEEE 802.1X port-based authentication with MAC Authentication Bypass* |
| P9 | Two central syslog servers | Off-loading log records and alerts to two servers | Two organization log servers, then `logging host <SYSLOG_SERVER_1>; logging host <SYSLOG_SERVER_2>` | System Management Configuration Guide, *Configuring System Message Logs*; feature map row *Syslog to two central log servers* |
| P10 | Authoritative NTP servers that share the authentication key (the same key number and value) with the switch | Authenticated time synchronization, and a set system clock for certificate enrollment and validation | Organization NTP servers with the key, then `ntp authenticate; ntp authentication-key 1 hmac-sha2-256 <KEY>; ntp trusted-key 1` | System Management Configuration Guide, *Administering the Device* (NTP authentication: the switch synchronizes only to a source that has one of its keys); IP Routing Configuration Guide, *Configuring Multi-VRF CE* (the key number and value must be the same on the client and the server); Security Configuration Guide, *Configuring Secure Socket Layer HTTP* (set the system clock before you configure a CA trustpoint) |
| P11 | An SNMPv3 manager configured with the same user, authentication, and privacy settings | SNMPv3 queries and notifications with SHA authentication and AES privacy | The organization network management system, then `snmp-server host <NMS_IP_ADDRESS> version 3 priv V3USER` | Network Management Configuration Guide, *Configuring Simple Network Management Protocol*; feature map row *SNMPv3 with SHA authentication and AES-256 privacy* |
| P12 | An SCP server and account for configuration backups | The EEM applet that copies the running configuration off the switch when it changes | An organization SCP server; the applet copies to it with a copy running-config command to an scp:// address | System Management Configuration Guide, *Secure Copy*; feature map row *Configuration backup on change (EEM applet and SCP)* |
| P13 | PKI: a reachable DoD CA enrollment (SCEP) service, the CA certificate authenticated on the trustpoint, and the switch certificate enrolled | Certificates from the DoD CA for the switch | `crypto pki trustpoint <TRUSTPOINT>; enrollment url <DOD_CA_ENROLLMENT_URL>; exit; crypto pki authenticate <TRUSTPOINT>; crypto pki enroll <TRUSTPOINT>` | Security Configuration Guide, *Configuring Secure Socket Layer HTTP* (Configuring a CA Trustpoint) and *X.509v3 Certificates for SSH Authentication*; Cisco IOS Security Command Reference, *crypto pki authenticate* and *crypto pki enroll* |
| P14 | The software image for the platform, on flash or on a TFTP, FTP, HTTP, or HTTPS server the switch can reach | Installing a supported release | Copy the image from Cisco to the file server; the install command copies it from the remote location to the switch | System Management Configuration Guide, *Performing Device Setup Configuration* (Software Install: install add file copies the package from a remote location via FTP, HTTP, HTTPS, or TFTP) |
| P15 | A VTP domain with the same domain name and VTP password on every switch in it | VTP authentication (devices without the password, or with the wrong one, reject VTP advertisements) | `vtp domain <DOMAIN_NAME>` on each switch, with the same password | VLAN Configuration Guide, *Configuring VTP* (Passwords for the VTP Domain) |
| P16 | The user, unused, native, and management VLANs created on the switch | Per-VLAN settings (DHCP snooping, dynamic ARP inspection), VLAN assignments, trunk native and allowed VLAN lists, and the SVIs | `vlan <VLAN_ID>`, then check with `show vlan brief` | VLAN Configuration Guide, *Configuring VLANs* and *Configuring VLAN Trunks* |
| P17 | A DHCP server or DHCP relay agent configured and enabled, and the ports toward it trusted for DHCP snooping | DHCP snooping, and the bindings that IP Source Guard and dynamic ARP inspection use | `interface <UPLINK_PORT>; ip dhcp snooping trust` | IP Addressing Services Configuration Guide, *Prerequisites for Configuring DHCP* (DHCP server and relay agent configured and enabled before DHCP snooping; ports connected to a DHCP server trusted) |
| P18 | DHCP snooping enabled globally and on the user VLANs | IP Source Guard (DHCP snooping must be enabled on the access VLAN) and dynamic ARP inspection (which depends on the DHCP snooping binding database) | `ip dhcp snooping; ip dhcp snooping vlan <USER_VLANS>` | Security Configuration Guide, *Configuring IP Source Guard* and *Configuring Dynamic ARP Inspection*; feature map row *DHCP snooping* |
| P19 | The DHCP snooping binding database agent, with a location for the binding file | Keeping the DHCP snooping bindings across a reload (without it, a switch with IP Source Guard or dynamic ARP inspection loses connectivity after a reload) | `ip dhcp snooping database <URL>` | IP Addressing Services Configuration Guide, *Configuring DHCP* (DHCP Snooping Binding Database; Enabling the DHCP Snooping Binding Database Agent) |
| P20 | Static bindings for hosts that do not use DHCP: static IP source bindings for IP Source Guard and ARP access lists for dynamic ARP inspection | IP Source Guard and dynamic ARP inspection on ports and VLANs with statically addressed hosts | `ip source binding <MAC_ADDRESS> vlan <VLAN_ID> <IP_ADDRESS> interface <PORT>`, and an ARP access list for each VLAN with static hosts | Security Configuration Guide, *Configuring IP Source Guard* (static IP source bindings) and *Configuring Dynamic ARP Inspection* (ARP ACLs in non-DHCP environments); CR, *ip source binding* |
| P21 | UDLD enabled, in the same mode, on the neighbor device's port | Detection of unidirectional links (a UDLD-capable port cannot detect one when the far end is not UDLD-capable) | On the neighbor switch, enable UDLD in the same mode (normal or aggressive) as this switch | Layer 2 Configuration Guide, *Restrictions for Configuring UniDirectional Link Detection* |
| P22 | IP routing enabled | Routing between VLANs and routed ports, so that ACLs between subnets, perimeter filters, uRPF, routing protocols, VRFs, and multicast routing take effect | `ip routing` | IP Routing Configuration Guide, *Configuring IP Unicast Routing* (IP routing is disabled by default and must be enabled before routing can take place) |
| P23 | IPv6 unicast routing enabled | Forwarding of IPv6 traffic, router advertisements, and the IPv6 perimeter filters | `ipv6 unicast-routing` | IP Routing Configuration Guide, *Configuring IPv6 Unicast Routing*; IP Addressing Services Configuration Guide, *Configuring HSRP* (ipv6 unicast-routing enables the forwarding of IPv6 unicast datagrams) |
| P24 | Cisco Express Forwarding enabled | Unicast RPF (strict and loose mode) | `ip cef` | IP Routing Configuration Guide, *Prerequisites for Unicast Reverse Path Forwarding*; feature map row *Cisco Express Forwarding* |
| P25 | The egress filter ACL that permits only the enclave's valid source addresses | The egress filter and uRPF on internal interfaces | `ip access-list extended EGRESS_FILTER; permit ip <INTERNAL_SUBNET> <WILDCARD> any; deny ip any any log-input` | IP Routing Configuration Guide, *Prerequisites for Unicast Reverse Path Forwarding* (configure the egress filtering ACLs before Unicast RPF) |
| P26 | The routing protocol configured with its neighbors, and the same key, key chain, or password configured on each peer | OSPF authentication, BGP peer protection and filters, LDP neighbor authentication, and MSDP peer authentication | `router ospf <PROCESS_ID>; network <NETWORK> <WILDCARD> area <AREA_ID>` or `router bgp <ASN>; neighbor <EBGP_PEER> remote-as <PEER_ASN>`, with the matching key on each peer | IP Routing Configuration Guide, *Configuring OSPF* (all neighboring routers on a network must have the same password) and *Configuring BGP*; IP Multicast Routing Configuration Guide, *Configuring MSDP* (the same password on both MSDP peers) |
| P27 | A Loopback0 interface with an address that the peers can reach | Loopback sources for iBGP, the LDP router ID, and MSDP peering | `interface Loopback0; ip address <LOOPBACK_IP> 255.255.255.255` | Feature map rows *BGP peer protection*, *MPLS LDP*, and *MSDP peers* (their commands name Loopback0) |
| P28 | An MPLS core: MPLS forwarding and LDP on the core-facing interfaces, Cisco Express Forwarding, and the IGP (and MP-BGP for VPN routes) between the PE and P devices | LDP settings, TTL propagation, L3VPN VRFs, VPWS, VPLS, and the PE edge protections | `mpls label protocol ldp; interface <CORE_INTERFACE>; mpls ip` | Multiprotocol Label Switching Configuration Guide, *Prerequisites for MPLS Virtual Private Networks* (MPLS, LDP, and Cisco Express Forwarding in the network) and *Configuring MPLS Layer 3 VPN over GRE* (LDP and MP-BGP) |
| P29 | MPLS traffic engineering with RSVP on the core links, over IS-IS or OSPF | RSVP-TE message pacing | `mpls traffic-eng tunnels; interface <CORE_INTERFACE>; mpls traffic-eng tunnels; ip rsvp bandwidth` | Multiprotocol Label Switching Configuration Guide, *Prerequisites for MPLS Traffic Engineering and Enhancements* (MPLS, Cisco Express Forwarding, IS-IS or OSPF) |
| P30 | IP multicast routing enabled, with PIM sparse mode and a rendezvous point | PIM neighbor filters and boundaries, rendezvous point protection, IGMP join filters on the designated router, and MSDP | `ip multicast-routing; interface <PIM_INTERFACE>; ip pim sparse-mode; exit; ip pim rp-address <RP_ADDRESS>` | IP Multicast Routing Configuration Guide, *Configuring PIM* (prerequisites) and *Configuring SSM* (enable IP multicast routing and PIM sparse mode) |

### The Cisco Catalyst switch feature map

The requirement column uses the abbreviations defined in *Where the STIG
and SRG data comes from*. The rule titles, severities, and SRG IDs are
listed in the next table. The command column follows the conventions in
*Where the commands come from*.
The last column lists the IDs from *Cisco Catalyst switch prerequisites*.

[Download the feature map as CSV](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/data/volume-172-disa-srgs-and-stigs/32-cisco-catalyst-switch-feature-version-and-stig-map-feature-map.csv) (352 rows).

| Category | Feature | First listed / Introduced (IOS XE) | STIG rule(s) | Command to satisfy the requirement | Cisco Catalyst switch prerequisites |
| --- | --- | --- | --- | --- | --- |
| Core: Management access | Management session limit (VTY lines and HTTP connections) | 17.1.1 or earlier | C-NDM `CISC-ND-000010` | `ip http max-connections 2; line vty 0 1; transport input ssh; line vty 2 31; transport input none` | P2 |
| Core: Management access | Management access list on the VTY lines | 17.1.1 or earlier | C-NDM `CISC-ND-000140` | `ip access-list standard MANAGEMENT_NET; permit <MGMT_SUBNET> <WILDCARD>; exit; line vty 0 31; transport input ssh; access-class MANAGEMENT_NET in` | P2, P3 |
| Core: Management access | Idle session timeout (console, VTY, and HTTP) | 17.1.1 or earlier | C-NDM `CISC-ND-000720` | `line console 0; exec-timeout 5 0; line vty 0 31; exec-timeout 5 0; exit; ip http timeout-policy idle 300 life <SECONDS> requests <NUMBER>` | — |
| Core: Management access | SSH version 2 server with FIPS-approved MACs and ciphers | 17.1.1 or earlier | C-NDM `CISC-ND-001200`; C-NDM `CISC-ND-001210` | `ip ssh version 2; ip ssh server algorithm mac hmac-sha2-512 hmac-sha2-256; ip ssh server algorithm encryption aes256-ctr aes192-ctr aes128-ctr` | P2 |
| Core: Management access | DoD Notice and Consent Banner (login banner) | 17.1.1 or earlier | C-NDM `CISC-ND-000160` | `banner login # <DOD_NOTICE_AND_CONSENT_BANNER_TEXT> #` | — |
| Core: Management access | Out-of-band management interface and management ACLs | 17.1.1 or earlier | C-RTR `CISC-RT-000450` | `ip access-list extended INGRESS_MANAGEMENT_ACL; permit tcp any host <MGMT_IP_ADDRESS> eq 22; permit udp any host <MGMT_IP_ADDRESS> eq 161; permit icmp any host <MGMT_IP_ADDRESS>; deny ip any any log-input; exit; ip access-list extended EGRESS_MANAGEMENT_ACL; deny ip any any log-input; exit; interface <MGMT_INTERFACE>; ip access-group INGRESS_MANAGEMENT_ACL in; ip access-group EGRESS_MANAGEMENT_ACL out` | P3 |
| Core: Management access | Auxiliary port | 17.1.1 or earlier | C-RTR `CISC-RT-000230` | `line aux 0; no exec; transport input none` | — |
| Core: Administrators and authentication | AAA with two RADIUS servers and the local account as fallback | 17.1.1 or earlier | C-NDM `CISC-ND-001370` | `aaa new-model; radius server RADIUS1; address ipv4 <RADIUS_1_IP> auth-port 1812 acct-port 1813; key <KEY>; exit; radius server RADIUS2; address ipv4 <RADIUS_2_IP> auth-port 1812 acct-port 1813; key <KEY>; exit; aaa group server radius RADIUS_GROUP; server name RADIUS1; server name RADIUS2; exit; aaa authentication login CONSOLE group RADIUS_GROUP local; aaa authentication login LOGIN_AUTHENTICATION group RADIUS_GROUP local; line vty 0 31; login authentication LOGIN_AUTHENTICATION; line console 0; login authentication CONSOLE; exit; ip http authentication aaa login-authentication LOGIN_AUTHENTICATION` | P5 |
| Core: Administrators and authentication | Local account of last resort | 17.1.1 or earlier | C-NDM `CISC-ND-000490` | `username <USERNAME> privilege <PRIVILEGE_LEVEL> common-criteria-policy PASSWORD_POLICY secret <PASSWORD>; aaa authentication login default group RADIUS_GROUP local` | P4, P5, P7 |
| Core: Administrators and authentication | Password policy (AAA common criteria policy) | 17.1.1 or earlier | C-NDM `CISC-ND-000550`; C-NDM `CISC-ND-000570`; C-NDM `CISC-ND-000580`; C-NDM `CISC-ND-000590`; C-NDM `CISC-ND-000600`; C-NDM `CISC-ND-000610` | `aaa new-model; aaa common-criteria policy PASSWORD_POLICY; min-length 15; upper-case 1; lower-case 1; numeric-count 1; special-case 1; char-change 8` | — |
| Core: Administrators and authentication | Password encryption and enable secret | 17.1.1 or earlier | C-NDM `CISC-ND-000620` | `service password-encryption; enable secret <PASSWORD>` | — |
| Core: Administrators and authentication | Login lockout (login block-for) | 17.1.1 or earlier | C-NDM `CISC-ND-000150` | `login block-for 900 attempts 3 within 120` | — |
| Core: Logging and auditing | Configuration change logger (archive log config) | 17.1.1 or earlier | C-NDM `CISC-ND-000090`; C-NDM `CISC-ND-000100`; C-NDM `CISC-ND-000110`; C-NDM `CISC-ND-000120`; C-NDM `CISC-ND-000210`; C-NDM `CISC-ND-000330`; C-NDM `CISC-ND-000880`; C-NDM `CISC-ND-001250`; C-NDM `CISC-ND-001270` | `logging userinfo; archive; log config; logging enable; logging size 1000; notify syslog contenttype plaintext; hidekeys` | — |
| Core: Logging and auditing | Login success and failure logging | 17.1.1 or earlier | C-NDM `CISC-ND-001260` | `login on-success log; login on-failure log` | — |
| Core: Logging and auditing | Log timestamps | 17.1.1 or earlier | C-NDM `CISC-ND-000280` | `service timestamps log datetime localtime` | — |
| Core: Logging and auditing | ACL logging of denied packets (log-input) | 17.1.1 or earlier | C-NDM `CISC-ND-000290`; C-RTR `CISC-RT-000200`; C-RTR `CISC-RT-000210`; C-RTR `CISC-RT-000220` | `ip access-list extended <ACL_NAME>; deny ip any any log-input` | — |
| Core: Logging and auditing | Local log buffer | 17.1.1 or earlier | C-NDM `CISC-ND-000980` | `logging buffered <BUFFER_SIZE> informational` | — |
| Core: Logging and auditing | Syslog to two central log servers | 17.1.1 or earlier | C-NDM `CISC-ND-001000`; C-NDM `CISC-ND-001450` | `logging host <SYSLOG_SERVER_1>; logging host <SYSLOG_SERVER_2>; logging trap critical` | P9 |
| Core: Logging and auditing | File system privilege (file privilege) | 17.1.1 or earlier | C-NDM `CISC-ND-000380`; C-NDM `CISC-ND-000390`; C-NDM `CISC-ND-000460` | `file privilege 15` | — |
| Core: System | Authenticated NTP from two servers | 17.1.1 or earlier | C-NDM `CISC-ND-001030`; C-NDM `CISC-ND-001150` | `ntp authenticate; ntp authentication-key 1 hmac-sha2-256 <KEY>; ntp trusted-key 1; ntp server <NTP_SERVER_1> key 1; ntp server <NTP_SERVER_2> key 1` | P10 |
| Core: System | SNMPv3 with SHA authentication and AES-256 privacy | 17.1.1 or earlier | C-NDM `CISC-ND-001130`; C-NDM `CISC-ND-001140` | `snmp-server group V3GROUP v3 priv read V3READ write V3WRITE; snmp-server user V3USER V3GROUP v3 auth sha <AUTH_PASSWORD> priv aes 256 <PRIV_PASSWORD>; snmp-server host <NMS_IP_ADDRESS> version 3 priv V3USER` | P11 |
| Core: System | Configuration backup on change (EEM applet and SCP) | 17.1.1 or earlier | C-NDM `CISC-ND-001410` | `ip scp server enable; file prompt quiet; event manager applet BACKUP_CONFIG authorization bypass; event syslog pattern "%SYS-5-CONFIG_I"; action 1 cli command "enable"; action 2 info type routername; action 3 cli command "copy running-config scp://<USER>@<SCP_SERVER>/<PATH>/$_info_routername-running-config"; action 4 syslog priority informational msg "Configuration backup executed for $_info_routername"` | P2, P4, P12 |
| Core: System | PKI trustpoints and certificate enrollment | 17.1.1 or earlier | C-NDM `CISC-ND-001440` | `crypto pki trustpoint <TRUSTPOINT>; enrollment url <DOD_CA_ENROLLMENT_URL>` | P10, P13 |
| Core: System | Software installation and supported releases | 17.1.1 or earlier | C-NDM `CISC-ND-001470` | `show version` `install add file <IMAGE> activate commit` | P14 |
| Core: System | Unnecessary and nonsecure services | 17.1.1 or earlier | C-NDM `CISC-ND-000470` | `no boot network; no ip bootp server; no ip dns server; no ip identd; no ip finger; no ip http server; no ip rcmd rcp-enable; no ip rcmd rsh-enable; no service config; no service finger; no service tcp-small-servers; no service udp-small-servers; no service pad; no service call-home` | — |
| Core: System | Configuration auto-loading (boot network and service config) | 17.1.1 or earlier | C-RTR `CISC-RT-000090` | `no boot network; no service config` | — |
| Core: Layer 2 security | IEEE 802.1X port-based authentication with MAC Authentication Bypass | 17.1.1 or earlier | C-L2S `CISC-L2-000020` | `aaa new-model; radius server RADIUS_1; address ipv4 <RADIUS_1_IP>; key <KEY>; exit; radius server RADIUS_2; address ipv4 <RADIUS_2_IP>; key <KEY>; exit; aaa group server radius RADIUS_SERVERS; server name RADIUS_1; server name RADIUS_2; exit; aaa authentication dot1x default group RADIUS_SERVERS; dot1x system-auth-control; interface range <HOST_PORTS>; switchport mode access; authentication host-mode single-host; dot1x pae authenticator; authentication port-control auto; mab` | P5, P8 |
| Core: Layer 2 security | VTP authentication | 17.1.1 or earlier | C-L2S `CISC-L2-000030` | `vtp password <PASSWORD>` | P15 |
| Core: Layer 2 security | Root guard | 17.1.1 or earlier | C-L2S `CISC-L2-000090` | `interface range <ACCESS_SWITCH_PORTS>; spanning-tree guard root` | — |
| Core: Layer 2 security | BPDU guard | 17.1.1 or earlier | C-L2S `CISC-L2-000100` | `interface range <HOST_PORTS>; spanning-tree bpduguard enable` | — |
| Core: Layer 2 security | STP loop guard | 17.1.1 or earlier | C-L2S `CISC-L2-000110` | `spanning-tree loopguard default` | — |
| Core: Layer 2 security | Unknown unicast flood blocking | 17.1.1 or earlier | C-L2S `CISC-L2-000120` | `interface range <HOST_PORTS>; switchport block unicast` | — |
| Core: Layer 2 security | DHCP snooping | 17.1.1 or earlier | C-L2S `CISC-L2-000130` | `ip dhcp snooping; ip dhcp snooping vlan <USER_VLANS>` | P16, P17 |
| Core: Layer 2 security | IP Source Guard | 17.1.1 or earlier | C-L2S `CISC-L2-000140` | `interface range <HOST_PORTS>; ip verify source` | P17, P18, P19, P20 |
| Core: Layer 2 security | Dynamic ARP inspection | 17.1.1 or earlier | C-L2S `CISC-L2-000150` | `ip arp inspection vlan <USER_VLANS>` | P16, P17, P18, P19, P20 |
| Core: Layer 2 security | Storm control | 17.1.1 or earlier | C-L2S `CISC-L2-000160` | `interface range <HOST_PORTS>; storm-control unicast level bps 62000000; storm-control broadcast level bps 20000000` | — |
| Core: Layer 2 security | IGMP snooping | 17.1.1 or earlier | C-L2S `CISC-L2-000170` | `ip igmp snooping` | — |
| Core: Layer 2 switching | Rapid PVST+ and MST spanning tree | 17.1.1 or earlier | C-L2S `CISC-L2-000180` | `spanning-tree mode rapid-pvst` | — |
| Core: Layer 2 switching | Unidirectional Link Detection (UDLD) | 17.1.1 or earlier | C-L2S `CISC-L2-000190` | `udld enable` | P21 |
| Core: Layer 2 switching | Static 802.1Q trunks | 17.1.1 or earlier | C-L2S `CISC-L2-000200` | `interface <TRUNK_PORT>; switchport trunk encapsulation dot1q; switchport mode trunk; switchport nonegotiate` | — |
| Core: Layer 2 switching | Access ports and VLAN assignment | 17.1.1 or earlier | C-L2S `CISC-L2-000210`; C-L2S `CISC-L2-000220`; C-L2S `CISC-L2-000250`; C-L2S `CISC-L2-000270` | `interface range <UNUSED_PORTS>; switchport access vlan <UNUSED_VLAN>; shutdown; interface range <HOST_PORTS>; switchport mode access; switchport access vlan <USER_VLAN>` | P16 |
| Core: Layer 2 switching | Trunk native VLAN and allowed VLAN list | 17.1.1 or earlier | C-L2S `CISC-L2-000230`; C-L2S `CISC-L2-000260` | `interface <TRUNK_PORT>; switchport trunk native vlan <NATIVE_VLAN>; switchport trunk allowed vlan except 1,<UNUSED_VLAN>` | P16 |
| Core: Layer 2 switching | Management VLAN interface (SVI) | 17.1.1 or earlier | C-L2S `CISC-L2-000240` | `interface vlan <MGMT_VLAN>; ip address <IP_ADDRESS> <MASK>; no shutdown` | P16 |
| Core: QoS | Modular QoS (class maps, policy maps, and service policies) | 17.1.1 or earlier | C-L2S `CISC-L2-000040`; C-RTR `CISC-RT-000760`; C-RTR `CISC-RT-000770`; C-RTR `CISC-RT-000780` | `class-map match-all VOICE; match ip dscp ef; exit; class-map match-all SCAVENGER; match ip dscp cs1; exit; policy-map QOS_POLICY; class VOICE; priority level 1; class SCAVENGER; bandwidth percent 5; class class-default; bandwidth percent 25; exit; exit; interface <UPLINK_PORT>; service-policy output QOS_POLICY` | — |
| Core: Layer 3 and routing | IP access lists on routed ports and SVIs | 17.1.1 or earlier | C-RTR `CISC-RT-000010` | `ip access-list extended <ACL_NAME>; permit tcp any <DEST_SUBNET> <WILDCARD> eq <PORT>; deny ip any any log-input; exit; interface vlan <VLAN_ID>; ip access-group <ACL_NAME> out` | P16, P22 |
| Core: Layer 3 and routing | Inactive Layer 3 interfaces | 17.1.1 or earlier | C-RTR `CISC-RT-000060` | `interface <UNUSED_L3_INTERFACE>; shutdown` | — |
| Core: Layer 3 and routing | Control plane policing (CoPP) | 17.1.1 or earlier | C-RTR `CISC-RT-000120` | `cpp system-default` `show policy-map control-plane` | — |
| Core: Layer 3 and routing | Gratuitous ARP | 17.1.1 or earlier | C-RTR `CISC-RT-000150` | `no ip gratuitous-arps` | — |
| Core: Layer 3 and routing | IP directed broadcast | 17.1.1 or earlier | C-RTR `CISC-RT-000160` | `interface <L3_INTERFACE>; no ip directed-broadcast` | — |
| Core: Layer 3 and routing | ICMP unreachable, mask reply, and redirect messages | 17.1.1 or earlier | C-RTR `CISC-RT-000170`; C-RTR `CISC-RT-000180`; C-RTR `CISC-RT-000190` | `interface <EXTERNAL_INTERFACE>; no ip unreachables; no ip mask-reply; no ip redirects` | — |
| Core: Layer 3 and routing | Cisco Express Forwarding | 17.1.1 or earlier | C-RTR `CISC-RT-000235` | `ip cef; ipv6 cef` | — |
| Core: Layer 3 and routing | Routing protocol authentication with key chains (OSPF) | 17.1.1 or earlier | C-RTR `CISC-RT-000050` | `key chain OSPF_KEY_CHAIN; key 1; key-string <KEY>; cryptographic-algorithm hmac-sha-256; send-lifetime <START_TIME> duration 15552000; accept-lifetime <START_TIME> duration 15552000; exit; exit; interface <L3_INTERFACE>; ip ospf authentication key-chain OSPF_KEY_CHAIN` | P1, P22, P26 |
| Core: Perimeter router role | Inbound ACL on external interfaces (deny by default, bogons, IP options) | 17.1.1 or earlier | C-RTR `CISC-RT-000240`; C-RTR `CISC-RT-000250`; C-RTR `CISC-RT-000260`; C-RTR `CISC-RT-000270`; C-RTR `CISC-RT-000320`; C-RTR `CISC-RT-000330`; C-RTR `CISC-RT-000350` | `ip access-list extended EXTERNAL_ACL_INBOUND; deny ip any any option any-options; deny ip <BOGON_PREFIX> <WILDCARD> any log-input; permit tcp any any established; permit tcp host <PEER_IP> host <LOCAL_IP> eq bgp; deny ip any any log-input; exit; interface <EXTERNAL_INTERFACE>; ip access-group EXTERNAL_ACL_INBOUND in` | P22 |
| Core: Perimeter router role | Egress filter and uRPF on internal interfaces | 17.1.1 or earlier | C-RTR `CISC-RT-000310`; C-RTR `CISC-RT-000340` | `interface <INTERNAL_INTERFACE>; ip verify unicast source reachable-via rx; ip access-group EGRESS_FILTER in` | P22, P24, P25 |
| Core: Perimeter router role | LLDP and CDP on external interfaces | 17.1.1 or earlier | C-RTR `CISC-RT-000360`; C-RTR `CISC-RT-000370` | `interface <EXTERNAL_INTERFACE>; no lldp transmit; no cdp enable` | — |
| Core: Perimeter router role | Proxy ARP on external interfaces | 17.1.1 or earlier | C-RTR `CISC-RT-000380` | `interface <EXTERNAL_INTERFACE>; no ip proxy-arp` | — |
| Core: Perimeter router role | Outbound management traffic block | 17.1.1 or earlier | C-RTR `CISC-RT-000390` | `ip access-list extended EXTERNAL_ACL_OUTBOUND; deny tcp any any eq tacacs log-input; deny tcp any any eq 22 log-input; deny udp any any eq snmp log-input; deny udp any any eq snmptrap log-input; deny udp any any eq syslog log-input; permit tcp any any eq www; deny ip any any log-input; exit; interface <EXTERNAL_INTERFACE>; ip access-group EXTERNAL_ACL_OUTBOUND out` | P22 |
| Core: Perimeter router role | IPv6 perimeter filtering and Router Advertisement suppression | 17.1.1 or earlier | C-RTR `CISC-RT-000391`; C-RTR `CISC-RT-000392`; C-RTR `CISC-RT-000393`; C-RTR `CISC-RT-000394`; C-RTR `CISC-RT-000395`; C-RTR `CISC-RT-000396`; C-RTR `CISC-RT-000397`; C-RTR `CISC-RT-000398` | `ipv6 access-list FILTER_IPV6; deny ipv6 any any undetermined-transport log; permit ipv6 any host <HOME_AGENT_IPV6> routing-type 2; deny ipv6 any any routing log; deny ipv6 any any hbh log; deny ipv6 any any dest-option-type log; deny ipv6 any any log; exit; interface <EXTERNAL_INTERFACE>; ipv6 nd ra suppress; ipv6 traffic-filter FILTER_IPV6 in` | P23 |
| Core: Layer 3 and routing | IPv6 router advertisement hop limit | 17.1.1 or earlier | C-RTR `CISC-RT-000236` | `ipv6 hop-limit 128` | P23 |
| Core: Layer 3 and routing | IPv6 addressing (no site-local unicast addresses) | 17.1.1 or earlier | C-RTR `CISC-RT-000237` | — | — |
| Core: BGP | BGP peer protection (GTSM, unique keys, maximum prefixes, first-AS check, loopback source) | 17.1.1 or earlier | C-RTR `CISC-RT-000470`; C-RTR `CISC-RT-000480`; C-RTR `CISC-RT-000540`; C-RTR `CISC-RT-000560`; C-RTR `CISC-RT-000580` | `router bgp <ASN>; bgp enforce-first-as; neighbor <EBGP_PEER> ttl-security hops 1; neighbor <EBGP_PEER> password <UNIQUE_KEY>; neighbor <EBGP_PEER> maximum-prefix <MAXIMUM>; neighbor <IBGP_PEER> update-source Loopback0` | P1, P22, P26, P27 |
| Core: BGP | BGP prefix and AS-path filtering | 17.1.1 or earlier | C-RTR `CISC-RT-000490`; C-RTR `CISC-RT-000500`; C-RTR `CISC-RT-000510`; C-RTR `CISC-RT-000520`; C-RTR `CISC-RT-000530`; C-RTR `CISC-RT-000550`; C-RTR `CISC-RT-000570` | `ip prefix-list PREFIX_FILTER deny <BOGON_PREFIX> le 32; ip prefix-list PREFIX_FILTER deny <LOCAL_AS_PREFIX> le 32; ip prefix-list PREFIX_FILTER permit 0.0.0.0/0 ge 8 le 24; ip prefix-list CE_PREFIX_ADVERTISEMENTS permit <CUSTOMER_PREFIX> le 32; ip as-path access-list 10 permit ^<CUSTOMER_ASN>$; router bgp <ASN>; neighbor <EBGP_PEER> prefix-list PREFIX_FILTER in; neighbor <CE_PEER> prefix-list <CUSTOMER_PREFIX_LIST> in; neighbor <CE_PEER> prefix-list CE_PREFIX_ADVERTISEMENTS out; neighbor <CE_PEER> filter-list 10 in` | P1, P22, P26 |
| Core: MPLS and PE router role | MPLS LDP (router ID, IGP synchronization, neighbor authentication) and TTL propagation | 17.1.1 or earlier | C-RTR `CISC-RT-000590`; C-RTR `CISC-RT-000600`; C-RTR `CISC-RT-000620`; C-RTR `CISC-RT-000660` | `mpls ldp router-id Loopback0 force; no mpls ip propagate-ttl; mpls ldp neighbor <PEER_IP> password <PASSWORD>; router ospf <PROCESS_ID>; mpls ldp sync` | P1, P22, P26, P27, P28 |
| Core: MPLS and PE router role | RSVP-TE message pacing | 17.1.1 or earlier | C-RTR `CISC-RT-000610` | `ip rsvp signalling rate-limit burst 9 maxsize 2100 period 30` | P28, P29 |
| Core: MPLS and PE router role | MPLS Layer 3 VPN VRFs (RD, route targets, interface binding) | 17.1.1 or earlier | C-RTR `CISC-RT-000630`; C-RTR `CISC-RT-000640`; C-RTR `CISC-RT-000650` | `ip vrf <VRF_NAME>; rd <RD>; route-target import <RT>; route-target export <RT>; exit; interface <CE_INTERFACE>; ip vrf forwarding <VRF_NAME>` | P22, P28 |
| Core: MPLS and PE router role | VPWS pseudowires (xconnect VC IDs) | 17.1.1 or earlier | C-RTR `CISC-RT-000670` | `interface <CE_INTERFACE>; xconnect <PEER_IP> <VC_ID> encapsulation mpls` | P28 |
| Core: MPLS and PE router role | VPLS (VFI, VPN ID, split horizon, storm control, IGMP snooping, MAC limits) | 17.1.1 or earlier | C-RTR `CISC-RT-000680`; C-RTR `CISC-RT-000690`; C-RTR `CISC-RT-000700`; C-RTR `CISC-RT-000710`; C-RTR `CISC-RT-000720` | `l2 vfi <VFI_NAME> manual; vpn id <VPN_ID>; neighbor <PE_IP> encapsulation mpls; bridge-domain <BD_ID>; exit; interface <CE_INTERFACE>; storm-control broadcast level bps <RATE>; service instance <ID> ethernet; encapsulation untagged; bridge-domain <BD_ID>; exit; exit; bridge-domain <BD_ID>; ip igmp snooping; mac limit maximum addresses <MAXIMUM>` | P1, P28 |
| Core: MPLS and PE router role | PE edge protection (core ACL, uRPF loose mode, IP options) | 17.1.1 or earlier | C-RTR `CISC-RT-000730`; C-RTR `CISC-RT-000740`; C-RTR `CISC-RT-000750` | `ip access-list extended BLOCK_TO_CORE; deny ip any <CORE_PREFIX> <WILDCARD> log-input; permit ip any any; exit; interface <CE_INTERFACE>; ip access-group BLOCK_TO_CORE in; ip verify unicast source reachable-via any; exit; ip options drop` | P22, P24, P28 |
| Core: IP multicast | PIM interfaces, neighbor filters, and multicast boundaries | 17.1.1 or earlier | C-RTR `CISC-RT-000790`; C-RTR `CISC-RT-000800`; C-RTR `CISC-RT-000810` | `ip access-list standard PIM_NEIGHBORS; permit <PIM_NEIGHBOR_IP>; exit; ip access-list standard MULTICAST_SCOPE; deny 239.0.0.0 0.255.255.255; permit any; exit; interface <NON_MULTICAST_INTERFACE>; no ip pim sparse-mode; interface <PIM_INTERFACE>; ip pim neighbor-filter PIM_NEIGHBORS; ip multicast boundary MULTICAST_SCOPE` | P22, P30 |
| Core: IP multicast | Rendezvous point protection (register and join filters, register rate limit, SPT threshold) | 17.1.1 or earlier | C-RTR `CISC-RT-000820`; C-RTR `CISC-RT-000830`; C-RTR `CISC-RT-000840`; C-RTR `CISC-RT-000850`; C-RTR `CISC-RT-000890` | `ip access-list extended PIM_REGISTER_FILTER; deny ip any <GROUP> <WILDCARD>; permit ip host <SOURCE> any; deny ip any any; exit; ip pim accept-register list PIM_REGISTER_FILTER; ip pim register-rate-limit <RATE>; ip access-list standard PIM_JOIN_FILTER; deny <GROUP> <WILDCARD>; permit any; exit; ip pim accept-rp <RP_ADDRESS> PIM_JOIN_FILTER; ip pim spt-threshold infinity` | P22, P30 |
| Core: IP multicast | IGMP join filters and limits on the designated router | 17.1.1 or earlier | C-RTR `CISC-RT-000860`; C-RTR `CISC-RT-000870`; C-RTR `CISC-RT-000880` | `ip access-list standard IGMP_JOIN_FILTER; deny <GROUP> <WILDCARD>; permit any; exit; interface vlan <USER_VLAN>; ip igmp access-group IGMP_JOIN_FILTER; ip igmp limit <NUMBER>` | P16, P22, P30 |
| Core: IP multicast | MSDP peers (authentication, SA filters, SA limits, loopback source) | 17.1.1 or earlier | C-RTR `CISC-RT-000900`; C-RTR `CISC-RT-000910`; C-RTR `CISC-RT-000920`; C-RTR `CISC-RT-000930`; C-RTR `CISC-RT-000940`; C-RTR `CISC-RT-000950` | `ip msdp peer <PEER_IP> connect-source Loopback0 remote-as <ASN>; ip msdp password peer <PEER_IP> <PASSWORD>; ip msdp sa-filter in <PEER_IP> list INBOUND_MSDP_SA_FILTER; ip msdp sa-filter out <PEER_IP> list OUTBOUND_MSDP_SA_FILTER; ip msdp sa-limit <PEER_IP> <NUMBER>; ip access-list extended EXTERNAL_ACL_INBOUND; permit tcp host <PEER_IP> host <LOCAL_IP> eq 639; deny tcp any host <LOCAL_IP> eq 639` | P1, P22, P26, P27, P30 |
| Device hardening | BIOS Protection for Golden SPI | 17.1.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Device hardening | Cisco Umbrella Integration | 17.1.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Device hardening | Opening or Closing SNMP UDP Ports | 17.1.1 and later | C-NDM `CISC-ND-000470` | — | — |
| Device hardening | Factory Reset with 3-pass Overwrite | 17.2.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Device hardening | Active Directory Integration for Umbrella Connector | 17.3.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Device hardening | Disabling USB Ports | 17.5.1 and later | C-NDM `CISC-ND-000470` | `platform usb disable` | — |
| Device hardening | Network Detection and Response | 17.5.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Device hardening | Mandatory enable secret password in the initial configuration | 17.7.1 and later | C-NDM `CISC-ND-000620` | — | — |
| Device hardening | Enforce minimum length for Enable password | 17.8.1 and later | C-NDM `CISC-ND-000550` | `enable common-criteria-policy PASSWORD_POLICY password <PASSWORD>` | P4, P7 |
| Device hardening | Support for PI SSH | 17.9.1 and later | C-NDM `CISC-ND-001210` | `ip ssh server algorithm encryption aes256-gcm aes128-gcm aes256-ctr aes192-ctr aes128-ctr` | P2 |
| Device hardening | Enhanced Password Security Through Updated Combination Rule | 17.10.1 and later | C-NDM `CISC-ND-000550` | `aaa common-criteria policy PASSWORD_POLICY; character-repetition 3; restrict-consecutive-letters` | P4, P7 |
| Device hardening | Secure Data Wipe | 17.10.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Device hardening | SHA256 based Password-masking support | 17.10.1 and later | C-NDM `CISC-ND-000620` | `enable algorithm-type sha256 secret <PASSWORD>` | — |
| Device hardening | Deprecation of Weak Ciphers | 17.11.1 and later | C-NDM `CISC-ND-001210` | — | P2 |
| Device hardening | Modified Trustpoints for Secure Unique Device Identity (SUDI) Certificates | 17.12.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Device hardening | Strict-KEX | 17.17.1 and later | C-NDM `CISC-ND-001210` | — (no CLI setting in the 26.x Security Configuration Guide; applies to SSH sessions) | P2 |
| Device hardening | Audit commands | 17.18.2 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Device hardening | Syslog warning for high-risk configuration changes | 17.18.2 and later | C-NDM `CISC-ND-001270` | — | — |
| Device hardening | Warnings for planned default and deprecation changes | 17.18.2 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Device hardening | Resilient Infrastructure | 26.1.1 and later | C-NDM `CISC-ND-000470` | — | — |
| Device hardening | Disable HTTPS servers by default (exceptions allowed) | 26.2.1 and later | C-NDM `CISC-ND-000470` | `no ip http server; no ip http secure-server` | — |
| Device hardening | Resilient Infrastructure changes | 26.2.1 and later | C-NDM `CISC-ND-000470` | — | — |
| AAA and 802.1X | Session Limit - To prevent MAC address flooding DOS attack | 17.2.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| AAA and 802.1X | Device Classifier Profiles | 17.4.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| AAA and 802.1X | VRF-Aware RADIUS Automated Tester | 17.4.1 and later | C-NDM `CISC-ND-001370` | `radius server RADIUS1; automate-tester username <PROBE_USER> probe-on vrf <VRF_NAME>` | P3, P5 |
| AAA and 802.1X | DSCP marking on RADIUS Servers | 17.5.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| AAA and 802.1X | Session Timer Enhancement | 17.5.1 and later | C-L2S `CISC-L2-000020` | `dot1x system-auth-control; interface range <HOST_PORTS>; authentication port-control auto; dot1x pae authenticator; mab` | P5, P8 |
| AAA and 802.1X | RadSec CoA over same tunnel | 17.6.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| AAA and 802.1X | AAA Authentication Cache for 802.1x | 17.7.1 and later | C-L2S `CISC-L2-000020` | `dot1x system-auth-control; interface range <HOST_PORTS>; authentication port-control auto; dot1x pae authenticator; mab` | P5, P8 |
| AAA and 802.1X | Custom EAPoL | 17.10.1 and later | C-L2S `CISC-L2-000020` | `dot1x system-auth-control; interface range <HOST_PORTS>; authentication port-control auto; dot1x pae authenticator; mab` | P5, P8 |
| AAA and 802.1X | RADIUS Automated Testing Probe-on | 17.10.1 and later | C-NDM `CISC-ND-001370` | `radius server RADIUS1; automate-tester username <PROBE_USER> probe-on` | P5 |
| AAA and 802.1X | show aaa dead-criteria radius enhancement command | 17.11.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| AAA and 802.1X | show access-session command | 17.11.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| AAA and 802.1X | Silent Host Handling | 17.11.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| AAA and 802.1X | DSCP marking for RADIUS packets for administrative sessions | 17.12.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| AAA and 802.1X | VLAN RADIUS Attributes in Access Requests | 17.13.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| AAA and 802.1X | Message authenticator attribute in RADIUS | 17.18.1 and later | C-NDM `CISC-ND-001370` | — (no CLI example in the 26.x Security Configuration Guide or command references) | P5 |
| AAA and 802.1X | TLS for TACACS+ | 17.18.1 and later | C-NDM `CISC-ND-001370` | — (no CLI example in the 26.x Security Configuration Guide or command references) | P6 |
| TrustSec | IPv6: HTTP SGACL enforcement with IPv6 Policy Server | 17.2.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| TrustSec | Enhanced SGACL Logging | 17.3.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| TrustSec | Cisco TrustSec support with IEEE 802.1X | 17.7.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| TrustSec | SXP Version 5 | 17.9.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| TrustSec | Flexible Netflow Record for SGACL Permit and Deny Actions | 17.13.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| TrustSec | AAA PAC-less Authentication | 17.15.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| TrustSec | Interface-Level VLAN-SGT Mapping | 17.16.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| TrustSec | CTS Role-Based Enforcement | 17.17.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| TrustSec | Retain last known good policy | 17.18.2 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| TrustSec | CTS policy server list enablement over RADIUS for IPv6 | 26.1.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| TrustSec | Dynamic protocol switching for communication between network devices and policy servers | 26.1.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| TrustSec | High Availability for Security Exchange Protocol | 26.1.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| TrustSec | PAC download over IPv6 | 26.1.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| TrustSec | Security Service Insertion | 26.1.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| TrustSec | SGT Exchange Protocol over IPv6 | 26.1.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| MACsec | MACsec over Ethernet over MPLS (EoMPLS) | 17.1.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| MACsec | MACsec Fallback Key Support | 17.8.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| MACsec | MACsec Fallback Key Support with High Availability | 17.10.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| MACsec | LAN MACsec over MPLS | 17.11.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| MACsec | MACsec PQC | 26.2.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Access lists and first-hop security | Neighbor Discovery (ND) Inspection Feature Deprecation | 17.1.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Access lists and first-hop security | Switch Integrated Security Features (SISF) - Throttling of ARP Packets | 17.3.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Access lists and first-hop security | ACL Template for IPv4 and IPv6 | 17.5.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Access lists and first-hop security | Fully Qualified Domain Name (FQDN) ACL | 17.5.1 and later | C-RTR `CISC-RT-000010` | `ip access-list extended <ACL_NAME>; permit tcp any <DEST_SUBNET> <WILDCARD> eq <PORT>; deny ip any any log-input; exit; interface vlan <VLAN_ID>; ip access-group <ACL_NAME> out` | P16, P22 |
| Access lists and first-hop security | Switch Integrated Security Features (SISF): ARP Protection | 17.7.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Access lists and first-hop security | DHCP Snooping with Egress SPAN on the same interface | 17.9.1 and later | C-L2S `CISC-L2-000130` | `ip dhcp snooping; ip dhcp snooping vlan <USER_VLANS>` | P16, P17 |
| Access lists and first-hop security | DHCP Gleaning | 17.10.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Access lists and first-hop security | Reflexive Access Lists (IPv4) | 17.10.1 and later | C-RTR `CISC-RT-000010` | `ip access-list extended <ACL_NAME>; permit tcp any <DEST_SUBNET> <WILDCARD> eq <PORT>; deny ip any any log-input; exit; interface vlan <VLAN_ID>; ip access-group <ACL_NAME> out` | P1, P16, P22 |
| Access lists and first-hop security | Interface ID Option in DHCPv6 Relay Message | 17.12.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Access lists and first-hop security | Interface Template Support for IPv6 DHCP Guard | 17.12.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Access lists and first-hop security | IP DHCP Server Changes to Limit IP Assignment to Next Hop only | 17.12.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Access lists and first-hop security | IPv6 Neighbor Discovery Proxy | 17.13.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Access lists and first-hop security | Management Traffic Control | 17.13.1 and later | C-NDM `CISC-ND-000140`; C-RTR `CISC-RT-000450` | `mgmt-traffic control ipv4; interface <MGMT_INTERFACE>; protocol ssh https snmp; address <MGMT_IP_ADDRESS>` | P1, P3 |
| Access lists and first-hop security | device tracking export oper data command | 17.14.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Layer 2 and VLANs | Per-Port MTU Configuration | 17.1.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Layer 2 and VLANs | Loop Detection Guard | 17.2.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Layer 2 and VLANs | Multiple Administrative VLANS in Resilient Ethernet Protocol (REP) | 17.2.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Layer 2 and VLANs | VLAN Load Balancing for FlexLink+ | 17.2.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Layer 2 and VLANs | Link Aggregation Control Protocol (LACP) 1:1 Redundancy and Dampening | 17.3.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Layer 2 and VLANs | Private VLAN (PVLAN) on Trunk Ports and Portchannels | 17.3.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Layer 2 and VLANs | Selective Q-in-Q | 17.5.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Layer 2 and VLANs | Wired Dynamic PVLAN | 17.5.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Layer 2 and VLANs | Standalone Mode on Layer 3 EtherChannels | 17.10.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Layer 2 and VLANs | TCN Flood | 17.11.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Layer 2 and VLANs | spanning-tree bpdu sender-conflict command | 17.14.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Layer 2 and VLANs | Port Settings Configuration for Interfaces | 17.15.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Layer 2 and VLANs | STP Bridge Assurance per Interface Support | 17.16.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Layer 2 and VLANs | Maximum number of allowed MAC address moves | 17.18.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Layer 2 and VLANs | MAC Move Permit Redundancy Protocol | 26.1.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| QoS | Low priority control packet mapping to Non-Low Latency Queueing (LLQ) | 17.7.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| QoS | Split ARP and ForUS Packets to 2 Separate Queues | 17.16.1 and later | C-RTR `CISC-RT-000120` | `cpp system-default` `show policy-map control-plane` | — |
| IP routing | VRF Aware NAT | 17.2.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| IP routing | VRF Support for TCL Socket | 17.2.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| IP routing | Forwarding Scale Enhancements | 17.3.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| IP routing | BGP Large Community | 17.4.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| IP routing | WCCP - VRF support | 17.6.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| IP routing | SSO Support for VRRPv3 | 17.6.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| IP routing | NAT support on L3 Port Channel | 17.10.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| IP routing | Default Limits for redistributed routes and LSA in OSPF | 17.11.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| IP routing | show ip eigrp topology and show ip eigrp accounting command output | 17.13.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| IP routing | NAT SSO support with StackWise Virtual | 17.14.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| IP routing | OSPF Local RIB Path Limit Enhancement | 17.14.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| IP routing | Unique BGP Identifier for BGP-4 | 17.15.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| IP routing | BGP neighbors monitoring with SNMP | 17.18.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| IP routing | Default Recursive next-hop support | 26.1.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| IP routing | BGP IPv4 prefix with IPv6 next-hop | 26.2.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| IP multicast and services | Multicast VPN Extranet Support | 17.1.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| IP multicast and services | Bonjour Apple AirDrop Service | 17.13.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| IP multicast and services | Removal of Service Types from the Default Service List | 17.13.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| IP multicast and services | mDNS Protocol Options | 17.14.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| IP multicast and services | Multicast Flow-aware SG Timer | 17.15.2+; 17.16.1+ | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| MPLS, VPLS, and L2VPN | IGMP (IPv4) : VPLS Layer 2 Snooping | 17.1.1 and later | C-RTR `CISC-RT-000710` | `bridge-domain <BD_ID>; ip igmp snooping` | P1, P28 |
| MPLS, VPLS, and L2VPN | Ingress and Egress Flexible Netflow on MPLS | 17.1.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| MPLS, VPLS, and L2VPN | MPLS VPN InterAS Option A | 17.1.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| MPLS, VPLS, and L2VPN | VPLS Flow-Aware Transport Pseudowire Support | 17.1.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| MPLS, VPLS, and L2VPN | VPLS Protocol-Mode CLI Support | 17.1.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| MPLS, VPLS, and L2VPN | MPLS QoS - WRED | 17.3.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| MPLS, VPLS, and L2VPN | MPLS VPN InterAS Option AB | 17.3.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| MPLS, VPLS, and L2VPN | VPLS: Routed Pseudowire IRB for IPv6 Unicast | 17.3.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| MPLS, VPLS, and L2VPN | MLDP-Based MVPN | 17.3.3 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| MPLS, VPLS, and L2VPN | IPv6 Explicit Null Label | 17.6.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| MPLS, VPLS, and L2VPN | LACP and PAGP over EoMPLS | 17.6.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| MPLS, VPLS, and L2VPN | MLD Snooping over VPLS | 17.6.1 and later | C-RTR `CISC-RT-000710` | `bridge-domain <BD_ID>; ipv6 mld snooping` | P1, P28 |
| MPLS, VPLS, and L2VPN | MPLS Traffic Engineering: IP Explicit Address Exclusion | 17.6.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| MPLS, VPLS, and L2VPN | MPLS Traffic Engineering: LSP Attributes | 17.6.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| MPLS, VPLS, and L2VPN | MPLS Traffic Engineering: Bundled Interface | 17.6.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| MPLS, VPLS, and L2VPN | MPLS Traffic Engineering: Configurable Path Calculation Metric for Tunnels | 17.6.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| MPLS, VPLS, and L2VPN | MPLS Traffic Engineering: Any Transport over MPLS Tunnel Selection | 17.7.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| MPLS, VPLS, and L2VPN | MPLS Traffic Engineering: Forwarding Adjacency | 17.7.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| MPLS, VPLS, and L2VPN | MPLS Traffic Engineering: Interarea Tunnels | 17.7.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| MPLS, VPLS, and L2VPN | MPLS Traffic Engineering: Inter-AS TE | 17.7.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| MPLS, VPLS, and L2VPN | MPLS Traffic Engineering: RSVP Graceful Restart | 17.7.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| MPLS, VPLS, and L2VPN | MPLS Traffic Engineering: RSVP Refresh Reduction and Reliable Messaging | 17.7.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| MPLS, VPLS, and L2VPN | MPLS Traffic Engineering: Verbatim Path Support | 17.7.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| MPLS, VPLS, and L2VPN | show mvpn vrfri command | 17.13.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| BGP EVPN VXLAN and fabric | BGP EVPN VXLAN: Broadcast, Unknown Unicast, and Multicast (BUM) Traffic Rate Limiting | 17.3.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| BGP EVPN VXLAN and fabric | BGP EVPN VXLAN: Enhanced rendezvous point (RP) Functionality for Layer 3 TRM for IPv4 and IPv6 traffic | 17.3.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| BGP EVPN VXLAN and fabric | BGP EVPN VXLAN: Interworking of Layer 3 TRM with MVPN Networks for IPv4 Traffic | 17.3.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| BGP EVPN VXLAN and fabric | BGP EVPN VXLAN: Layer 3 Tenant Routed Multicast (TRM) for IPv6 Traffic | 17.3.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| BGP EVPN VXLAN and fabric | Data MDT Support for L3 TRM | 17.6.2 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| BGP EVPN VXLAN and fabric | Optimized Layer 2 Multicast in BGP EVPN VXLAN Fabric | 17.8.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| BGP EVPN VXLAN and fabric | BGP EVPN VXLAN: TCP MSS Adjustment | 17.9.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| BGP EVPN VXLAN and fabric | IPsec: BGP EVPN VXLAN over IPSec | 17.9.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| BGP EVPN VXLAN and fabric | LISP VXLAN Fabric for a Wired Network | 17.9.3 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| BGP EVPN VXLAN and fabric | Support for Wireless in a LISP VXLAN Fabric | 17.9.4 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| BGP EVPN VXLAN and fabric | BGP EVPN VXLAN with IPv6 in the Underlay (VXLANv6) | 17.10.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| BGP EVPN VXLAN and fabric | BGP EVPN VXLAN: Dynamic BGP Peering for EVPN | 17.11.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| BGP EVPN VXLAN and fabric | BGP EVPN VXLAN: EVPN Microsegmentation | 17.11.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| BGP EVPN VXLAN and fabric | BGP EVPN VXLAN: EVPN Route Map Support | 17.11.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| BGP EVPN VXLAN and fabric | BGP EVPN VXLAN: Multi-Homing in a BGP EVPN VXLAN Fabric | 17.11.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| BGP EVPN VXLAN and fabric | BGP EVPN VXLAN: Tenant Routed Multicast over BGP EVPN VXLANv6 | 17.11.99SW+; 17.13.1+ | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| BGP EVPN VXLAN and fabric | BGP EVPN VXLAN: ARP inspection and DHCP Rogue Server Protection in VXLAN Environment (L2 VNIs) | 17.12.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| BGP EVPN VXLAN and fabric | BGP EVPN VXLAN: BGP EVPN VRF Auto RD and Auto RT | 17.12.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| BGP EVPN VXLAN and fabric | BGP EVPN VXLAN: fast-detection command | 17.14.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| BGP EVPN VXLAN and fabric | BGP EVPN VXLAN: show lisp instance {ipv4, ipv6, ethernet} command | 17.14.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| BGP EVPN VXLAN and fabric | Multi-Cluster Fabric – Router MAC Rewrite with Nexthop-Self BGP Attribute | 17.15.2 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| BGP EVPN VXLAN and fabric | IPv6 Solution: Multisite Across SDA Transit (w. HER) Multicast | 17.16.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| BGP EVPN VXLAN and fabric | Multi-cluster BGP EVPN VXLAN Fabric | 17.16.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| BGP EVPN VXLAN and fabric | BGP EVPN VXLAN: BGP EVPN IPv6 Originator ID | 17.18.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| BGP EVPN VXLAN and fabric | BGP EVPN VXLAN: Next-hop recursive support with EVPN PBR | 17.18.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| BGP EVPN VXLAN and fabric | EVPN Multihoming: Fabric Networks | 17.18.2 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| BGP EVPN VXLAN and fabric | EVPN Multihoming: Non-Fabric Networks | 17.18.2 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| BGP EVPN VXLAN and fabric | BGP EVPN VXLAN IRB in the global routing table or non-EVPN VRF | 26.2.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| IPsec and tunnels | IPsec: IPsec Virtual Tunnel Interfaces | 17.6.2 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| IPsec and tunnels | IPsec: IPsec Dead Peer Detection Periodic Message Option | 17.6.2 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| IPsec and tunnels | IPsec: IPsec Anti-Replay Window | 17.6.2 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| IPsec and tunnels | IPsec: Encrypted Preshared Key | 17.6.2 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| IPsec and tunnels | IPsec: IKE for IPsec VPNs | 17.6.2 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| IPsec and tunnels | IPsec: Transform Sets for IKEv2 Proposals | 17.6.2 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| IPsec and tunnels | PBR Support for IPsec SVTI | 17.7.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| IPsec and tunnels | Multicast traffic support for IPsec SVTI | 17.8.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| IPsec and tunnels | IPsec: IPsec NAT Transparency | 17.9.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| IPsec and tunnels | IPsec: VRF Aware IPsec | 17.9.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| IPsec and tunnels | GRE over IPsec | 17.11.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| IPsec and tunnels | IPsec Scale Enhancement for supported SVTIs | 17.13.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| IPsec and tunnels | VRF-aware GRE over IPsec | 17.13.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| IPsec and tunnels | Distributed Processing for IPsec | 17.14.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Timing | IEEE802.1AS (gPTP) and IEEE 1588v2 PTP on EtherChannel Interfaces | 17.2.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Timing | Generalized PTP over Layer 3 Unicast | 17.5.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Timing | IEEE 1588v2 Precision Time Protocol (PTP) on SDA Fabric | 17.6.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Timing | IEEE 1588v2 PTP interoperability with MACsec and EtherChannel | 17.6.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Timing | AES67 Compliance | 17.7.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Timing | G8275.x Timing Profile | 17.8.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| System, stacking, and high availability | Default Number of VTY Lines | 17.1.1 and later | C-NDM `CISC-ND-000010` | `ip http max-connections 2; line vty 0 1; transport input ssh; line vty 2 31; transport input none` | P2 |
| System, stacking, and high availability | Flash MIB instance retrieval count limit increase | 17.1.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| System, stacking, and high availability | SCP Performance Improvements | 17.2.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| System, stacking, and high availability | Extended Fast Software Upgrade | 17.3.2a+; 17.7.1+ | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| System, stacking, and high availability | Line Configuration for Disabling Auto-Consolidation | 17.4.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| System, stacking, and high availability | High Speed Stacking | 17.5.1+; 17.6.2+ | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| System, stacking, and high availability | SCP improvement in large RTT scenario | 17.6.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| System, stacking, and high availability | View System Power Consumption | 17.8.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| System, stacking, and high availability | SMU Installation disabled in bundle mode | 17.9.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| System, stacking, and high availability | hw-module ecomode serdes-disable command | 17.14.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| System, stacking, and high availability | show reload history command | 17.14.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| System, stacking, and high availability | Energy Consumption Visibility | 17.15.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| System, stacking, and high availability | Shutdown Fiber Ports with no SFP Inserted | 17.15.2+; 17.16.1+ | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| System, stacking, and high availability | Shutdown Power Supplies in C9300 Stack Power during Low Load | 17.15.2+; 17.16.1+ | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| System, stacking, and high availability | Extended Fast Software Upgrade reduced traffic downtime | 17.15.2 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| System, stacking, and high availability | Smart LEDs | 17.16.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| System, stacking, and high availability | LLDP Support on Management Port | 17.17.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Monitoring and troubleshooting | ERSPAN IPv6 | 17.1.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Monitoring and troubleshooting | VPN ID in NetFlow | 17.2.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Monitoring and troubleshooting | ERSPAN over MPLS VPN | 17.5.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Monitoring and troubleshooting | request tech-support command | 17.12.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Monitoring and troubleshooting | show idprom tan command | 17.12.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Monitoring and troubleshooting | IP SLA Probe Configuration Modification Capability | 17.14.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Monitoring and troubleshooting | IP SLA Probe Config Modification Capability via Config Replace | 17.16.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Monitoring and troubleshooting | Resource Manager System (RMS) and Resource Manager Controller (RMC) commands | 17.18.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Monitoring and troubleshooting | Embedded Packet Capture (EPC) support on EtherChannel sub-interfaces | 17.18.2 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Monitoring and troubleshooting | Radio-active tracing for MAC learning | 17.18.2 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Programmability | Programmability: Candidate configuration confirmed commit | 17.1.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Programmability | Programmability: YANG Data Models | 17.2.1+; 17.3.1+; 17.4.1+; 17.5.1+; 17.6.1+; 17.8.1+; 17.9.1+; 17.10.1+; 17.11.1+; 17.12.1+; 17.13.1+; 17.14.1+; 17.15.1+; 17.16.1+; 17.17.1+; 17.18.1+; 26.1.1+; 26.2.1+ | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Programmability | Programmability: Native Docker Container: Application Auto-Restart | 17.2.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Programmability | Programmability: TLDP On-Change Notifications | 17.2.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Programmability | Programmability: gNMI Configuration Persistence | 17.3.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Programmability | Programmability: gNOI Certificate Management | 17.3.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Programmability | Programmability: gNOI Bootstrapping with Certificate Service | 17.3.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Programmability | Programmability: ThousandEyes Enterprise Agent | 17.3.3+; 17.6.1+ | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Programmability | Programmability: OpenFlow Rewrite Fields | 17.4.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Programmability | Programmability: Application Hosting on Internal Flash for Cisco Signed Applications | 17.4.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Programmability | Programmability: Front-Panel Application Hosting | 17.6.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Programmability | Programmability: ThousandEyes BrowserBot | 17.6.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Programmability | Programmability: NETCONF Access from Guest Shell | 17.6.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Programmability | Programmability: YANG Model Version 1.1 | 17.7.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Programmability | Programmability: Converting IOS Commands to XML | 17.7.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Programmability | Programmability: gNOI Factory Reset Services | 17.7.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Programmability | Programmability: Leaf-Level Filtering for Telemetry | 17.7.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Programmability | Programmability: ZTP Configuration through YANG | 17.7.1 and later | C-RTR `CISC-RT-000090` | — | — |
| Programmability | Programmability: Pubd Restartability | 17.9.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Programmability | Programmability: Upgrade YANG Models to YANG 1.1 | 17.10.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Programmability | Programmability: App-Hosting: ERSPAN Capabilities on AppGigabitEthernet Port | 17.10.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Programmability | NETCONF support for PTPv2 | 17.11.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Programmability | Programmability: gNMI Dial-Out Telemetry | 17.11.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Programmability | Programmability: Multicast Routing Support on the AppGigabitEthernet Port | 17.11.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Programmability | Programmability: PROTO Encoding | 17.11.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Programmability | Programmability: Secure Zero-Touch Provisioning | 17.11.1 and later | C-RTR `CISC-RT-000090` | — | — |
| Programmability | Programmability: NETCONF-SSH Algorithms | 17.12.1 and later | C-NDM `CISC-ND-001200`; C-NDM `CISC-ND-001210` | `ip ssh version 2; ip ssh server algorithm mac hmac-sha2-512 hmac-sha2-256; ip ssh server algorithm encryption aes256-ctr aes192-ctr aes128-ctr` | P2 |
| Programmability | Programmability: gNMI: Stream Subscriptions with on-Change Mode | 17.14.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Programmability | Programmability: gNMI: SubscribeResponse with sync_response | 17.14.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Programmability | Programmability: YANG Support for Multiple Next-Hops | 17.14.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Programmability | Programmability: On-change Support for Location-Aware Models | 17.17.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Programmability | Programmability: gNXI gRPC server reach by user-configured VRFs | 17.18.2 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Programmability | Programmability: Service-level ACL support for gNXI services | 26.1.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Programmability | Programmability: MAC address table mapping | 26.2.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Application hosting | EPC support of AppGigabitEthernet | 17.12.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Application hosting | ASAc Firewall-Application Hosting | 17.12.2 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Application hosting | ThousandEyes 5.0 Support | 17.16.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Licensing and cloud management | Smart Licensing Using Policy | 17.3.2a and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Licensing and cloud management | Cisco DNA Center Support for Smart Licensing Using Policy | 17.3.2a and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Licensing and cloud management | Smart Software Manager On-Prem (SSM On-Prem) Support for Smart Licensing Using Policy | 17.3.3 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Licensing and cloud management | Export Control Key for High Security (HSECK9) | 17.6.2+; 17.7.1+ | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Licensing and cloud management | Smart Licensing Using Policy: Factory-installed trust code | 17.7.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Licensing and cloud management | Smart Licensing Using Policy: Support for trust code in additional topologies | 17.7.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Licensing and cloud management | Smart Licensing Using Policy: Ability to save authorization code request and return in a file and simpler upload in the CSSM Web UI | 17.7.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Licensing and cloud management | Smart Licensing Using Policy: RUM Report optimization and availability of statistics | 17.7.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Licensing and cloud management | Smart Licensing Using Policy: Support to collect software version in a RUM report | 17.7.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Licensing and cloud management | Smart Licensing Using Policy: Account information included in the ACK and show command outputs | 17.7.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Licensing and cloud management | Smart Licensing Using Policy: CSLU support for Linux | 17.7.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Licensing and cloud management | Smart Licensing Using Policy: New mechanism to send data privacy related information | 17.9.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Licensing and cloud management | Smart Licensing Using Policy: Hostname support | 17.9.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Licensing and cloud management | Support for Migrating to Meraki Dashboard-Managed Mode | 17.10.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Licensing and cloud management | Device Telemetry | 17.11.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Licensing and cloud management | Modified License Level for Unicast mDNS | 17.13.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Licensing and cloud management | AWS S3 and CloudWatch Support | 17.15.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Licensing and cloud management | Support sensitive CLIs with CRUD on Meraki | 17.17.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Licensing and cloud management | Product Analytics | 17.18.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Licensing and cloud management | Cisco Cloud Redirection for device onboarding | 26.2.1 and later | C-RTR `CISC-RT-000090` | — | — |
| Licensing and cloud management | PUSH ID (HTTPS) | 26.2.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Licensing and cloud management | Cisco Switching Licensing | 26.2.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Web UI | Web UI: Cisco Umbrella Integration | 17.1.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Web UI | Web UI: New default credentials for WebUI | 17.1.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Web UI | Web UI: Power Over Ethernet (POE) | 17.1.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Web UI | Web UI: Intermediate System- Intermediate System(IS-IS) | 17.1.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Web UI | Web UI: Routing Information Protocol (RIP) | 17.1.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Web UI | Web UI: Virtual Terminal Lines (VTY) | 17.1.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Web UI | Web UI: HSRP | 17.2.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Web UI | Web UI: Passwordless Login | 17.2.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Web UI | Web UI: Smart Licensing Using Policy | 17.4.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Web UI | Web UI: Stealthwatch Cloud support for NetFlow monitoring | 17.4.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Web UI | Web UI: BFD Echo Mode for OSPFv3 | 17.6.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Web UI | Web UI: SDM Templates | 17.6.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |
| Web UI | Web UI: Enhanced Day 0 Web UI Account Settings | 26.2.1 and later | No direct requirement; if unused, disable (C-NDM `CISC-ND-000470`) | — | — |

### Requirement reference

The STIG rules used in the map and in this chapter's text, with their
severity in the current releases. The SRG ID column gives the SRG
requirement each rule implements (the XCCDF group title).

[Download the requirement reference as CSV](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/data/volume-172-disa-srgs-and-stigs/32-cisco-catalyst-switch-feature-version-and-stig-map-requirements.csv) (152 rows).

| STIG | Rule | Severity | SRG ID | Rule title |
| --- | --- | --- | --- | --- |
| C-NDM | `CISC-ND-000010` | CAT II | `SRG-APP-000001-NDM-000200` | The Cisco switch must be configured to limit the number of concurrent management sessions to an organization-defined number. |
| C-NDM | `CISC-ND-000090` | CAT II | `SRG-APP-000026-NDM-000208` | The Cisco switch must be configured to automatically audit account creation. |
| C-NDM | `CISC-ND-000100` | CAT II | `SRG-APP-000027-NDM-000209` | The Cisco switch must be configured to automatically audit account modification. |
| C-NDM | `CISC-ND-000110` | CAT II | `SRG-APP-000028-NDM-000210` | The Cisco switch must be configured to automatically audit account disabling actions. |
| C-NDM | `CISC-ND-000120` | CAT II | `SRG-APP-000029-NDM-000211` | The Cisco switch must be configured to automatically audit account removal actions. |
| C-NDM | `CISC-ND-000140` | CAT II | `SRG-APP-000038-NDM-000213` | The Cisco switch must be configured to enforce approved authorizations for controlling the flow of management information within the device based on control policies. |
| C-NDM | `CISC-ND-000150` | CAT II | `SRG-APP-000065-NDM-000214` | The Cisco switch must be configured to enforce the limit of three consecutive invalid logon attempts, after which time it must lock out the user account from accessing the device for 15 minutes. |
| C-NDM | `CISC-ND-000160` | CAT II | `SRG-APP-000068-NDM-000215` | The Cisco switch must be configured to display the Standard Mandatory DoD Notice and Consent Banner before granting access to the device. |
| C-NDM | `CISC-ND-000210` | CAT II | `SRG-APP-000080-NDM-000220` | The Cisco device must be configured to audit all administrator activity. |
| C-NDM | `CISC-ND-000280` | CAT II | `SRG-APP-000096-NDM-000226` | The Cisco switch must produce audit records containing information to establish when (date and time) the events occurred. |
| C-NDM | `CISC-ND-000290` | CAT II | `SRG-APP-000097-NDM-000227` | The Cisco switch must produce audit records containing information to establish where the events occurred. |
| C-NDM | `CISC-ND-000330` | CAT II | `SRG-APP-000101-NDM-000231` | The Cisco switch must be configured to generate audit records containing the full-text recording of privileged commands. |
| C-NDM | `CISC-ND-000380` | CAT II | `SRG-APP-000119-NDM-000236` | The Cisco switch must be configured to protect audit information from unauthorized modification. |
| C-NDM | `CISC-ND-000390` | CAT II | `SRG-APP-000120-NDM-000237` | The Cisco switch must be configured to protect audit information from unauthorized deletion. |
| C-NDM | `CISC-ND-000460` | CAT II | `SRG-APP-000133-NDM-000244` | The Cisco switch must be configured to limit privileges to change the software resident within software libraries. |
| C-NDM | `CISC-ND-000470` | CAT I | `SRG-APP-000142-NDM-000245` | The Cisco switch must be configured to prohibit the use of all unnecessary and nonsecure functions and services. |
| C-NDM | `CISC-ND-000490` | CAT II | `SRG-APP-000148-NDM-000346` | The Cisco switch must be configured with only one local account to be used as the account of last resort in the event the authentication server is unavailable. |
| C-NDM | `CISC-ND-000550` | CAT II | `SRG-APP-000164-NDM-000252` | The Cisco switch must be configured to enforce a minimum 15-character password length. |
| C-NDM | `CISC-ND-000570` | CAT II | `SRG-APP-000166-NDM-000254` | The Cisco switch must be configured to enforce password complexity by requiring that at least one uppercase character be used. |
| C-NDM | `CISC-ND-000580` | CAT II | `SRG-APP-000167-NDM-000255` | The Cisco switch must be configured to enforce password complexity by requiring that at least one lowercase character be used. |
| C-NDM | `CISC-ND-000590` | CAT II | `SRG-APP-000168-NDM-000256` | The Cisco switch must be configured to enforce password complexity by requiring that at least one numeric character be used. |
| C-NDM | `CISC-ND-000600` | CAT II | `SRG-APP-000169-NDM-000257` | The Cisco switch must be configured to enforce password complexity by requiring that at least one special character be used. |
| C-NDM | `CISC-ND-000610` | CAT II | `SRG-APP-000170-NDM-000329` | The Cisco switch must be configured to require that when a password is changed, the characters are changed in at least eight of the positions within the password. |
| C-NDM | `CISC-ND-000620` | CAT I | `SRG-APP-000171-NDM-000258` | The Cisco switch must only store cryptographic representations of passwords. |
| C-NDM | `CISC-ND-000720` | CAT I | `SRG-APP-000190-NDM-000267` | The Cisco switch must be configured to terminate all network connections associated with device management after five minutes of inactivity. |
| C-NDM | `CISC-ND-000880` | CAT II | `SRG-APP-000319-NDM-000283` | The Cisco switch must be configured to automatically audit account enabling actions. |
| C-NDM | `CISC-ND-000980` | CAT II | `SRG-APP-000357-NDM-000293` | The Cisco switch must be configured to allocate audit record storage capacity in accordance with organization-defined audit record storage requirements. |
| C-NDM | `CISC-ND-001000` | CAT II | `SRG-APP-000360-NDM-000295` | The Cisco switch must be configured to generate an alert for all audit failure events. |
| C-NDM | `CISC-ND-001030` | CAT II | `SRG-APP-000373-NDM-000298` | The Cisco switch must be configured to synchronize its clock with the primary and secondary time sources using redundant authoritative time sources. |
| C-NDM | `CISC-ND-001130` | CAT II | `SRG-APP-000395-NDM-000310` | The Cisco switch must be configured to authenticate SNMP messages using a FIPS-validated Keyed-Hash Message Authentication Code (HMAC). |
| C-NDM | `CISC-ND-001140` | CAT II | `SRG-APP-000395-NDM-000310` | The Cisco switch must be configured to encrypt SNMP messages using a FIPS 140-2 approved algorithm. |
| C-NDM | `CISC-ND-001150` | CAT II | `SRG-APP-000395-NDM-000347` | The Cisco switch must be configured to authenticate Network Time Protocol (NTP) sources using authentication that is cryptographically based. |
| C-NDM | `CISC-ND-001200` | CAT I | `SRG-APP-000411-NDM-000330` | The Cisco switch must be configured to use FIPS-validated Keyed-Hash Message Authentication Code (HMAC) to protect the integrity of remote maintenance sessions. |
| C-NDM | `CISC-ND-001210` | CAT I | `SRG-APP-000412-NDM-000331` | The Cisco switch must be configured to implement cryptographic mechanisms to protect the confidentiality of remote maintenance sessions. |
| C-NDM | `CISC-ND-001250` | CAT II | `SRG-APP-000499-NDM-000319` | The Cisco switch must be configured to generate log records when administrator privileges are deleted. |
| C-NDM | `CISC-ND-001260` | CAT II | `SRG-APP-000503-NDM-000320` | The Cisco switch must be configured to generate audit records when successful/unsuccessful logon attempts occur. |
| C-NDM | `CISC-ND-001270` | CAT II | `SRG-APP-000504-NDM-000321` | The Cisco switch must be configured to generate log records for privileged activities. |
| C-NDM | `CISC-ND-001370` | CAT I | `SRG-APP-000516-NDM-000336` | The Cisco switch must be configured to use at least two authentication servers for the purpose of authenticating users prior to granting administrative access. |
| C-NDM | `CISC-ND-001410` | CAT II | `SRG-APP-000516-NDM-000340` | The Cisco switch must be configured to support organizational requirements to conduct backups of the configuration when changes occur. |
| C-NDM | `CISC-ND-001440` | CAT II | `SRG-APP-000516-NDM-000344` | The Cisco switch must be configured to obtain its public key certificates from an appropriate certificate policy through an approved service provider. |
| C-NDM | `CISC-ND-001450` | CAT I | `SRG-APP-000516-NDM-000350` | The Cisco switch must be configured to send log data to at least two central log servers for the purpose of forwarding alerts to the administrators and the information system security officer (ISSO). |
| C-NDM | `CISC-ND-001470` | CAT I | `SRG-APP-000516-NDM-000351` | The Cisco switch must be running an IOS release that is currently supported by Cisco Systems. |
| C-L2S | `CISC-L2-000020` | CAT I | `SRG-NET-000148-L2S-000015` | The Cisco switch must uniquely identify and authenticate all network-connected endpoint devices before establishing any connection. |
| C-L2S | `CISC-L2-000030` | CAT II | `SRG-NET-000168-L2S-000019` | The Cisco switch must authenticate all VLAN Trunk Protocol (VTP) messages with a hash function using the most secured cryptographic algorithm available. |
| C-L2S | `CISC-L2-000040` | CAT II | `SRG-NET-000193-L2S-000020` | The Cisco switch must manage excess bandwidth to limit the effects of packet flooding types of denial-of-service (DoS) attacks. |
| C-L2S | `CISC-L2-000090` | CAT III | `SRG-NET-000362-L2S-000021` | The Cisco switch must have Root Guard enabled on all switch ports connecting to access layer switches. |
| C-L2S | `CISC-L2-000100` | CAT II | `SRG-NET-000362-L2S-000022` | The Cisco switch must have BPDU Guard enabled on all user-facing or untrusted access switch ports. |
| C-L2S | `CISC-L2-000110` | CAT II | `SRG-NET-000362-L2S-000023` | The Cisco switch must have STP Loop Guard enabled. |
| C-L2S | `CISC-L2-000120` | CAT II | `SRG-NET-000362-L2S-000024` | The Cisco switch must have Unknown Unicast Flood Blocking (UUFB) enabled. |
| C-L2S | `CISC-L2-000130` | CAT II | `SRG-NET-000362-L2S-000025` | The Cisco switch must have DHCP snooping for all user VLANs to validate DHCP messages from untrusted sources. |
| C-L2S | `CISC-L2-000140` | CAT II | `SRG-NET-000362-L2S-000026` | The Cisco switch must have IP Source Guard enabled on all user-facing or untrusted access switch ports. |
| C-L2S | `CISC-L2-000150` | CAT II | `SRG-NET-000362-L2S-000027` | The Cisco switch must have Dynamic Address Resolution Protocol (ARP) Inspection (DAI) enabled on all user VLANs. |
| C-L2S | `CISC-L2-000160` | CAT III | `SRG-NET-000512-L2S-000001` | The Cisco switch must have Storm Control configured on all host-facing switchports. |
| C-L2S | `CISC-L2-000170` | CAT III | `SRG-NET-000512-L2S-000002` | The Cisco switch must have IGMP or MLD Snooping configured on all VLANs. |
| C-L2S | `CISC-L2-000180` | CAT II | `SRG-NET-000512-L2S-000003` | The Cisco switch must implement Rapid STP where VLANs span multiple switches with redundant links. |
| C-L2S | `CISC-L2-000190` | CAT II | `SRG-NET-000512-L2S-000004` | The Cisco switch must enable Unidirectional Link Detection (UDLD) to protect against one-way connections. |
| C-L2S | `CISC-L2-000200` | CAT II | `SRG-NET-000512-L2S-000005` | The Cisco switch must have all trunk links enabled statically. |
| C-L2S | `CISC-L2-000210` | CAT II | `SRG-NET-000512-L2S-000007` | The Cisco switch must have all disabled switch ports assigned to an unused VLAN. |
| C-L2S | `CISC-L2-000220` | CAT II | `SRG-NET-000512-L2S-000008` | The Cisco switch must not have the default VLAN assigned to any host-facing switch ports. |
| C-L2S | `CISC-L2-000230` | CAT II | `SRG-NET-000512-L2S-000009` | The Cisco switch must have the default VLAN pruned from all trunk ports that do not require it. |
| C-L2S | `CISC-L2-000240` | CAT II | `SRG-NET-000512-L2S-000010` | The Cisco switch must not use the default VLAN for management traffic. |
| C-L2S | `CISC-L2-000250` | CAT II | `SRG-NET-000512-L2S-000011` | The Cisco switch must have all user-facing or untrusted ports configured as access switch ports. |
| C-L2S | `CISC-L2-000260` | CAT II | `SRG-NET-000512-L2S-000012` | The Cisco switch must have the native VLAN assigned to an ID other than the default VLAN for all 802.1q trunk links. |
| C-L2S | `CISC-L2-000270` | CAT III | `SRG-NET-000512-L2S-000013` | The Cisco switch must not have any switchports assigned to the native VLAN. |
| C-RTR | `CISC-RT-000010` | CAT II | `SRG-NET-000018-RTR-000001` | The Cisco switch must be configured to enforce approved authorizations for controlling the flow of information within the network based on organization-defined information flow control policies. |
| C-RTR | `CISC-RT-000050` | CAT II | `SRG-NET-000168-RTR-000078` | The Cisco switch must be configured to enable routing protocol authentication using FIPS 198-1 algorithms with keys not exceeding 180 days of lifetime. |
| C-RTR | `CISC-RT-000060` | CAT III | `SRG-NET-000019-RTR-000007` | The Cisco switch must be configured to have all inactive layer 3 interfaces disabled. |
| C-RTR | `CISC-RT-000090` | CAT II | `SRG-NET-000362-RTR-000109` | The Cisco switch must not be configured to have any zero-touch deployment feature enabled when connected to an operational network. |
| C-RTR | `CISC-RT-000120` | CAT I | `SRG-NET-000362-RTR-000110` | The Cisco switch must be configured to protect against or limit the effects of denial-of-service (DoS) attacks by employing control plane protection. |
| C-RTR | `CISC-RT-000150` | CAT II | `SRG-NET-000362-RTR-000111` | The Cisco switch must be configured to have Gratuitous ARP disabled on all external interfaces. |
| C-RTR | `CISC-RT-000160` | CAT III | `SRG-NET-000362-RTR-000112` | The Cisco switch must be configured to have IP directed broadcast disabled on all interfaces. |
| C-RTR | `CISC-RT-000170` | CAT II | `SRG-NET-000362-RTR-000113` | The Cisco switch must be configured to have Internet Control Message Protocol (ICMP) unreachable messages disabled on all external interfaces. |
| C-RTR | `CISC-RT-000180` | CAT II | `SRG-NET-000362-RTR-000114` | The Cisco switch must be configured to have Internet Control Message Protocol (ICMP) mask reply messages disabled on all external interfaces. |
| C-RTR | `CISC-RT-000190` | CAT II | `SRG-NET-000362-RTR-000115` | The Cisco switch must be configured to have Internet Control Message Protocol (ICMP) redirect messages disabled on all external interfaces. |
| C-RTR | `CISC-RT-000200` | CAT III | `SRG-NET-000078-RTR-000001` | The Cisco switch must be configured to log all packets that have been dropped at interfaces via an ACL. |
| C-RTR | `CISC-RT-000210` | CAT II | `SRG-NET-000076-RTR-000001` | The Cisco switch must be configured to produce audit records containing information to establish where the events occurred. |
| C-RTR | `CISC-RT-000220` | CAT II | `SRG-NET-000077-RTR-000001` | The Cisco switch must be configured to produce audit records containing information to establish the source of the events. |
| C-RTR | `CISC-RT-000230` | CAT III | `SRG-NET-000019-RTR-000001` | The Cisco switch must be configured to disable the auxiliary port unless it is connected to a secured modem providing encryption and authentication. |
| C-RTR | `CISC-RT-000235` | CAT II | `SRG-NET-000512-RTR-000100` | The Cisco switch must be configured to have Cisco Express Forwarding enabled. |
| C-RTR | `CISC-RT-000236` | CAT III | `SRG-NET-000512-RTR-000012` | The Cisco switch must be configured to advertise a hop limit of at least 32 in Switch Advertisement messages for IPv6 stateless auto-configuration deployments. |
| C-RTR | `CISC-RT-000237` | CAT II | `SRG-NET-000512-RTR-000013` | The Cisco switch must not be configured to use IPv6 Site Local Unicast addresses. |
| C-RTR | `CISC-RT-000240` | CAT I | `SRG-NET-000202-RTR-000001` | The Cisco perimeter switch must be configured to deny network traffic by default and allow network traffic by exception. |
| C-RTR | `CISC-RT-000250` | CAT II | `SRG-NET-000019-RTR-000002` | The Cisco perimeter switch must be configured to enforce approved authorizations for controlling the flow of information between interconnected networks in accordance with applicable policy. |
| C-RTR | `CISC-RT-000260` | CAT II | `SRG-NET-000364-RTR-000109` | The Cisco perimeter switch must be configured to only allow incoming communications from authorized sources to be routed to authorized destinations. |
| C-RTR | `CISC-RT-000270` | CAT II | `SRG-NET-000364-RTR-000110` | The Cisco perimeter switch must be configured to block inbound packets with source Bogon IP address prefixes. |
| C-RTR | `CISC-RT-000310` | CAT I | `SRG-NET-000205-RTR-000014` | The Cisco perimeter switch must be configured to restrict it from accepting outbound IP packets that contain an illegitimate address in the source address field via egress filter or by enabling Unicast Reverse Path Forwarding (uRPF). |
| C-RTR | `CISC-RT-000320` | CAT II | `SRG-NET-000205-RTR-000003` | The Cisco perimeter switch must be configured to filter traffic destined to the enclave in accordance with the guidelines contained in DoD Instruction 8551.1. |
| C-RTR | `CISC-RT-000330` | CAT II | `SRG-NET-000205-RTR-000004` | The Cisco perimeter switch must be configured to filter ingress traffic at the external interface on an inbound direction. |
| C-RTR | `CISC-RT-000340` | CAT II | `SRG-NET-000205-RTR-000005` | The Cisco perimeter switch must be configured to filter egress traffic at the internal interface on an inbound direction. |
| C-RTR | `CISC-RT-000350` | CAT II | `SRG-NET-000205-RTR-000015` | The Cisco perimeter switch must be configured to block all packets with any IP options. |
| C-RTR | `CISC-RT-000360` | CAT III | `SRG-NET-000364-RTR-000111` | The Cisco perimeter switch must be configured to have Link Layer Discovery Protocol (LLDP) disabled on all external interfaces. |
| C-RTR | `CISC-RT-000370` | CAT III | `SRG-NET-000364-RTR-000111` | The Cisco perimeter switch must be configured to have Cisco Discovery Protocol (CDP) disabled on all external interfaces. |
| C-RTR | `CISC-RT-000380` | CAT II | `SRG-NET-000364-RTR-000112` | The Cisco perimeter switch must be configured to have Proxy ARP disabled on all external interfaces. |
| C-RTR | `CISC-RT-000390` | CAT II | `SRG-NET-000364-RTR-000113` | The Cisco perimeter switch must be configured to block all outbound management traffic. |
| C-RTR | `CISC-RT-000391` | CAT II | `SRG-NET-000512-RTR-000014` | The Cisco perimeter switch must be configured to suppress Router Advertisements on all external IPv6-enabled interfaces. |
| C-RTR | `CISC-RT-000392` | CAT II | `SRG-NET-000364-RTR-000200` | The Cisco perimeter switch must be configured to drop IPv6 undetermined transport packets. |
| C-RTR | `CISC-RT-000393` | CAT II | `SRG-NET-000364-RTR-000201` | The Cisco perimeter switch must be configured drop IPv6 packets with a Routing Header type 0, 1, or 3-255. |
| C-RTR | `CISC-RT-000394` | CAT II | `SRG-NET-000364-RTR-000202` | The Cisco perimeter switch must be configured to drop IPv6 packets containing a Hop-by-Hop header with invalid option type values. |
| C-RTR | `CISC-RT-000395` | CAT II | `SRG-NET-000364-RTR-000203` | The Cisco perimeter switch must be configured to drop IPv6 packets containing a Destination Option header with invalid option type values. |
| C-RTR | `CISC-RT-000396` | CAT II | `SRG-NET-000364-RTR-000204` | The Cisco perimeter switch must be configured to drop IPv6 packets containing an extension header with the Endpoint Identification option. |
| C-RTR | `CISC-RT-000397` | CAT II | `SRG-NET-000364-RTR-000205` | The Cisco perimeter switch must be configured to drop IPv6 packets containing the NSAP address option within Destination Option header. |
| C-RTR | `CISC-RT-000398` | CAT II | `SRG-NET-000364-RTR-000206` | The Cisco perimeter switch must be configured to drop IPv6 packets containing a Hop-by-Hop or Destination Option extension header with an undefined option type. |
| C-RTR | `CISC-RT-000450` | CAT II | `SRG-NET-000205-RTR-000012` | The Cisco switch must be configured to only permit management traffic that ingresses and egresses the out-of-band management (OOBM) interface. |
| C-RTR | `CISC-RT-000470` | CAT III | `SRG-NET-000362-RTR-000124` | The Cisco BGP switch must be configured to enable the Generalized TTL Security Mechanism (GTSM). |
| C-RTR | `CISC-RT-000480` | CAT II | `SRG-NET-000230-RTR-000002` | The Cisco BGP switch must be configured to use a unique key for each autonomous system (AS) that it peers with. |
| C-RTR | `CISC-RT-000490` | CAT II | `SRG-NET-000018-RTR-000002` | The Cisco BGP switch must be configured to reject inbound route advertisements for any Bogon prefixes. |
| C-RTR | `CISC-RT-000500` | CAT II | `SRG-NET-000018-RTR-000003` | The Cisco BGP switch must be configured to reject inbound route advertisements for any prefixes belonging to the local autonomous system (AS). |
| C-RTR | `CISC-RT-000510` | CAT II | `SRG-NET-000018-RTR-000004` | The Cisco BGP switch must be configured to reject inbound route advertisements from a customer edge (CE) switch for prefixes that are not allocated to that customer. |
| C-RTR | `CISC-RT-000520` | CAT II | `SRG-NET-000018-RTR-000005` | The Cisco BGP switch must be configured to reject outbound route advertisements for any prefixes that do not belong to any customers or the local autonomous system (AS). |
| C-RTR | `CISC-RT-000530` | CAT II | `SRG-NET-000205-RTR-000006` | The Cisco BGP switch must be configured to reject outbound route advertisements for any prefixes belonging to the IP core. |
| C-RTR | `CISC-RT-000540` | CAT III | `SRG-NET-000018-RTR-000006` | The Cisco BGP switch must be configured to reject route advertisements from BGP peers that do not list their autonomous system (AS) number as the first AS in the AS_PATH attribute. |
| C-RTR | `CISC-RT-000550` | CAT III | `SRG-NET-000018-RTR-000010` | The Cisco BGP switch must be configured to reject route advertisements from CE switches with an originating AS in the AS_PATH attribute that does not belong to that customer. |
| C-RTR | `CISC-RT-000560` | CAT II | `SRG-NET-000362-RTR-000117` | The Cisco BGP switch must be configured to use the maximum prefixes feature to protect against route table flooding and prefix de-aggregation attacks. |
| C-RTR | `CISC-RT-000570` | CAT III | `SRG-NET-000362-RTR-000118` | The Cisco BGP switch must be configured to limit the prefix size on any inbound route advertisement to /24, or the least significant prefixes issued to the customer. |
| C-RTR | `CISC-RT-000580` | CAT III | `SRG-NET-000512-RTR-000001` | The Cisco BGP switch must be configured to use its loopback address as the source address for iBGP peering sessions. |
| C-RTR | `CISC-RT-000590` | CAT III | `SRG-NET-000512-RTR-000002` | The Cisco MPLS switch must be configured to use its loopback address as the source address for LDP peering sessions. |
| C-RTR | `CISC-RT-000600` | CAT III | `SRG-NET-000512-RTR-000003` | The Cisco MPLS switch must be configured to synchronize Interior Gateway Protocol (IGP) and LDP to minimize packet loss when an IGP adjacency is established prior to LDP peers completing label exchange. |
| C-RTR | `CISC-RT-000610` | CAT III | `SRG-NET-000193-RTR-000001` | The MPLS switch with RSVP-TE enabled must be configured with message pacing to adjust maximum burst and maximum number of RSVP messages to an output queue based on the link speed and input queue size of adjacent core switches. |
| C-RTR | `CISC-RT-000620` | CAT II | `SRG-NET-000512-RTR-000004` | The Cisco MPLS switch must be configured to have TTL Propagation disabled. |
| C-RTR | `CISC-RT-000630` | CAT I | `SRG-NET-000512-RTR-000005` | The Cisco PE switch must be configured to have each Virtual Routing and Forwarding (VRF) instance bound to the appropriate physical or logical interfaces to maintain traffic separation between all MPLS L3VPNs. |
| C-RTR | `CISC-RT-000640` | CAT I | `SRG-NET-000512-RTR-000006` | The Cisco PE switch must be configured to have each Virtual Routing and Forwarding (VRF) instance with the appropriate Route Target (RT). |
| C-RTR | `CISC-RT-000650` | CAT II | `SRG-NET-000512-RTR-000007` | The Cisco PE switch must be configured to have each VRF with the appropriate Route Distinguisher (RD). |
| C-RTR | `CISC-RT-000660` | CAT II | `SRG-NET-000343-RTR-000001` | The Cisco PE switch providing MPLS Layer 2 Virtual Private Network (L2VPN) services must be configured to authenticate targeted Label Distribution Protocol (LDP) sessions used to exchange virtual circuit (VC) information using a FIPS-approved message authentication code algorithm. |
| C-RTR | `CISC-RT-000670` | CAT I | `SRG-NET-000512-RTR-000008` | The Cisco PE switch providing MPLS Virtual Private Wire Service (VPWS) must be configured to have the appropriate virtual circuit identification (VC ID) for each attachment circuit. |
| C-RTR | `CISC-RT-000680` | CAT I | `SRG-NET-000512-RTR-000009` | The Cisco PE switch providing Virtual Private LAN Services (VPLS) must be configured to have all attachment circuits defined to the virtual forwarding instance (VFI) with the globally unique VPN ID assigned for each customer VLAN. |
| C-RTR | `CISC-RT-000690` | CAT III | `SRG-NET-000512-RTR-000010` | The Cisco PE switch must be configured to enforce the split-horizon rule for all pseudowires within a Virtual Private LAN Services (VPLS) bridge domain. |
| C-RTR | `CISC-RT-000700` | CAT II | `SRG-NET-000193-RTR-000002` | The Cisco PE switch providing Virtual Private LAN Services (VPLS) must be configured to have traffic storm control thresholds on CE-facing interfaces. |
| C-RTR | `CISC-RT-000710` | CAT III | `SRG-NET-000362-RTR-000119` | The Cisco PE switch must be configured to implement Internet Group Management Protocol (IGMP) or Multicast Listener Discovery (MLD) snooping for each Virtual Private LAN Services (VPLS) bridge domain. |
| C-RTR | `CISC-RT-000720` | CAT II | `SRG-NET-000192-RTR-000002` | The Cisco PE switch must be configured to limit the number of MAC addresses it can learn for each Virtual Private LAN Services (VPLS) bridge domain. |
| C-RTR | `CISC-RT-000730` | CAT I | `SRG-NET-000205-RTR-000007` | The Cisco PE switch must be configured to block any traffic that is destined to the IP core infrastructure. |
| C-RTR | `CISC-RT-000740` | CAT II | `SRG-NET-000205-RTR-000008` | The Cisco PE switch must be configured with Unicast Reverse Path Forwarding (uRPF) loose mode enabled on all CE-facing interfaces. |
| C-RTR | `CISC-RT-000750` | CAT II | `SRG-NET-000205-RTR-000016` | The Cisco PE switch must be configured to ignore or drop all packets with any IP options. |
| C-RTR | `CISC-RT-000760` | CAT III | `SRG-NET-000193-RTR-000113` | The Cisco PE switch must be configured to enforce a Quality-of-Service (QoS) policy to provide preferred treatment for mission-critical applications. |
| C-RTR | `CISC-RT-000770` | CAT III | `SRG-NET-000193-RTR-000114` | The Cisco P switch must be configured to enforce a Quality-of-Service (QoS) policy to provide preferred treatment for mission-critical applications. |
| C-RTR | `CISC-RT-000780` | CAT II | `SRG-NET-000193-RTR-000112` | The Cisco switch must be configured to enforce a Quality-of-Service (QoS) policy to limit the effects of packet flooding denial-of-service (DoS) attacks. |
| C-RTR | `CISC-RT-000790` | CAT II | `SRG-NET-000019-RTR-000003` | The Cisco multicast switch must be configured to disable Protocol Independent Multicast (PIM) on all interfaces that are not required to support multicast routing. |
| C-RTR | `CISC-RT-000800` | CAT II | `SRG-NET-000019-RTR-000004` | The Cisco multicast switch must be configured to bind a Protocol Independent Multicast (PIM) neighbor filter to interfaces that have PIM enabled. |
| C-RTR | `CISC-RT-000810` | CAT III | `SRG-NET-000019-RTR-000005` | The Cisco multicast edge switch must be configured to establish boundaries for administratively scoped multicast traffic. |
| C-RTR | `CISC-RT-000820` | CAT III | `SRG-NET-000362-RTR-000120` | The Cisco multicast Rendezvous Point (RP) switch must be configured to limit the multicast forwarding cache so that its resources are not saturated by managing an overwhelming number of Protocol Independent Multicast (PIM) and Multicast Source Discovery Protocol (MSDP) source-active entries. |
| C-RTR | `CISC-RT-000830` | CAT III | `SRG-NET-000019-RTR-000013` | The Cisco multicast Rendezvous Point (RP) switch must be configured to filter Protocol Independent Multicast (PIM) Register messages received from the Designated switch (DR) for any undesirable multicast groups and sources. |
| C-RTR | `CISC-RT-000840` | CAT III | `SRG-NET-000019-RTR-000014` | The Cisco multicast Rendezvous Point (RP) switch must be configured to filter Protocol Independent Multicast (PIM) Join messages received from the Designated Cisco switch (DR) for any undesirable multicast groups. |
| C-RTR | `CISC-RT-000850` | CAT II | `SRG-NET-000362-RTR-000121` | The Cisco multicast Rendezvous Point (RP) must be configured to rate limit the number of Protocol Independent Multicast (PIM) Register messages. |
| C-RTR | `CISC-RT-000860` | CAT III | `SRG-NET-000364-RTR-000114` | The Cisco multicast Designated switch (DR) must be configured to filter the Internet Group Management Protocol (IGMP) and Multicast Listener Discovery (MLD) Report messages to allow hosts to join only multicast groups that have been approved by the organization. |
| C-RTR | `CISC-RT-000870` | CAT II | `SRG-NET-000364-RTR-000115` | The Cisco multicast Designated switch (DR) must be configured to filter the Internet Group Management Protocol (IGMP) and Multicast Listener Discovery (MLD) Report messages to allow hosts to join a multicast group only from sources that have been approved by the organization. |
| C-RTR | `CISC-RT-000880` | CAT II | `SRG-NET-000362-RTR-000122` | The Cisco multicast Designated switch (DR) must be configured to limit the number of mroute states resulting from Internet Group Management Protocol (IGMP) and Multicast Listener Discovery (MLD) Host Membership Reports. |
| C-RTR | `CISC-RT-000890` | CAT II | `SRG-NET-000362-RTR-000123` | The Cisco multicast Designated switch (DR) must be configured to set the shortest-path tree (SPT) threshold to infinity to minimalize source-group (S, G) state within the multicast topology where Any Source Multicast (ASM) is deployed. |
| C-RTR | `CISC-RT-000900` | CAT II | `SRG-NET-000364-RTR-000116` | The Cisco Multicast Source Discovery Protocol (MSDP) switch must be configured to only accept MSDP packets from known MSDP peers. |
| C-RTR | `CISC-RT-000910` | CAT II | `SRG-NET-000343-RTR-000002` | The Cisco Multicast Source Discovery Protocol (MSDP) switch must be configured to authenticate all received MSDP packets. |
| C-RTR | `CISC-RT-000920` | CAT III | `SRG-NET-000018-RTR-000007` | The Cisco Multicast Source Discovery Protocol (MSDP) switch must be configured to filter received source-active multicast advertisements for any undesirable multicast groups and sources. |
| C-RTR | `CISC-RT-000930` | CAT III | `SRG-NET-000018-RTR-000008` | The Cisco Multicast Source Discovery Protocol (MSDP) switch must be configured to filter source-active multicast advertisements to external MSDP peers to avoid global visibility of local-only multicast sources and groups. |
| C-RTR | `CISC-RT-000940` | CAT III | `SRG-NET-000018-RTR-000009` | The Cisco Multicast Source Discovery Protocol (MSDP) switch must be configured to limit the amount of source-active messages it accepts on a per-peer basis. |
| C-RTR | `CISC-RT-000950` | CAT III | `SRG-NET-000512-RTR-000011` | The Cisco Multicast Source Discovery Protocol (MSDP) switch must be configured to use a loopback address as the source address when originating MSDP traffic. |

### Collecting evidence

Run `show version` and keep the output with the checklist, together with a
full configuration backup (the backup applet's copy on the SCP server, or
`show running-config`). Keep the output of `show running-config | section
line`, `show running-config | section aaa`, `show aaa common-criteria
policy all`, `show archive log config all`, `show logging`, `show ntp
associations`, `show snmp user`, `show ip ssh`, `show login`, `show
spanning-tree summary`, `show interfaces trunk`, `show interfaces
status`, `show ip dhcp snooping`, `show ip arp inspection`, `show
authentication sessions`, `show storm-control`, `show policy-map
control-plane`, and `show ip access-lists`. For routed switches add `show
ip interface`, `show ip bgp neighbors`, `show ip prefix-list`, `show mpls
ldp neighbor`, `show ip pim interface`, and `show ip msdp peer`, as the
role requires. Export a sample of the syslog server's records showing the
configuration change logger entries, login failures, and denied packets
with `log-input`, and keep the upgrade history.

## Validation and Troubleshooting

- **A feature in the map is missing on your switch.** Check the version
  column against your release and model: the column comes from the
  Catalyst 9300 release notes, and the 9200, 9400, 9500, and 9600 have
  their own. Check the license level as well.
- **A STIG fix command is rejected.** Many fix texts have errors (`iip
  ssh`, `char-changes`, `switch bgp`, `ipv6 traffic-filter` with no
  direction). Use the command in the map, which was checked against the
  26.x documentation, and `?` on the CLI to list the options of your
  release.
- **Administrators are locked out after hardening.** Check the VTY access
  class, `transport input ssh`, the method lists on the console and VTY
  lines, the RADIUS servers and keys, and `login block-for`. Keep console
  access and the local account of last resort while you test.
- **Hosts lose connectivity after the L2S settings.** Check that DHCP
  snooping trusts the uplinks to the DHCP server, that dynamic ARP
  inspection and IP Source Guard have bindings for static hosts, that MAB
  is enabled for devices without 802.1X, and that the native VLAN matches
  on both ends of each trunk.
- **Routing adjacencies drop after the RTR settings.** Check the key
  chain lifetimes (in seconds), the time on both peers (NTP), the ACLs on
  the routed interfaces, and the control plane policer rates.
- **A rule has no matching feature on this switch.** Role rules are Not
  Applicable outside their role; some rules are met by procedure
  (supported software, backups, CNS absence). Record how each rule is met,
  not only which feature covers it.

## Security and Best Practices

- Keep IOS XE on a supported release and verify each image before
  installing it.
- Allow only SSH version 2 with SHA-2 MACs and AES counter mode on 32 VTY
  lines restricted by an access class, a five-minute idle timeout on every
  line and on HTTP, lockout after three failures for 15 minutes, and the
  DoD banner.
- Disable the HTTP server and every service in the fix text for C-NDM
  `CISC-ND-000470`, and leave off the functions you do not use.
- Use two RADIUS or TACACS+ servers for administrators and 802.1X, one
  local account of last resort stored as a secret, and a 15-character
  common criteria password policy.
- Log configuration changes, logins, and denied packets to two syslog
  servers with timestamps, and keep a local buffer.
- Use authenticated NTP from two servers and SNMPv3 with SHA and AES-256.
- On every host-facing port use 802.1X with MAB, BPDU guard, storm
  control, IP Source Guard, and a non-default access VLAN; use DHCP
  snooping and dynamic ARP inspection on user VLANs, static trunks with a
  non-default native VLAN, and VLAN 1 pruned.
- On routed switches apply ACLs between subnets, authenticate routing
  protocols, keep the control plane policer at its defaults or stricter,
  and apply the perimeter, PE, BGP, MPLS, and multicast rules for the roles
  the switch has.
- Review this map each time Cisco publishes an IOS XE release or DISA
  updates the IOS XE Switch STIGs.

## References and Knowledge Checks

**References:**

- Cisco, *Release Notes for Cisco Catalyst 9300 Series Switches*, Cisco IOS
  XE 17.1.x through 17.18.x, 26.1.x, and 26.2.x ("What's New" software
  feature tables).
- Cisco, *Command Reference, Cisco IOS XE 26.x.x (Catalyst 9300
  Switches)*, and the Catalyst 9300 26.x.x configuration guides (Security,
  System Management, Layer 2, VLAN, IP Routing, IP Addressing Services, IP
  Multicast Routing, Multiprotocol Label Switching, Quality of Service,
  Network Management, Interface and Hardware Components, Stacking and High
  Availability, Cisco TrustSec, Cisco DNA Service for Bonjour, and BGP EVPN
  VXLAN).
- Cisco, the Cisco IOS XE command references for access and edge routers:
  *Security Command Reference* (Commands A to C, D to L, M to R, and S to
  Z), *Configuration Fundamentals*, *Embedded Syslog Manager*, *Basic
  System Management*, *SNMP Support*, *HTTP Services*, *IP Addressing
  Services*, *IP Application Services*, *IPv6*, *IP Routing: BGP*, *IP
  Routing: OSPF*, *IP Routing: Protocol-Independent*, *Multiprotocol Label
  Switching*, *LAN Switching*, *Quality of Service Solutions*, *Embedded
  Event Manager*, *Interface and Hardware Component*, *IP Switching*, and
  *Carrier Ethernet*.
- DISA Cisco IOS XE Switch NDM STIG V3R6, L2S STIG V3R2, and RTR STIG V3R4
  (`U_Cisco_IOS-XE_Switch_Y26M04_STIG.zip`), from the October 2026 STIG
  Library Compilation.
- [Chapter 03](03-the-srg-catalog-how-stigs-are-built-and-what-to-do-without-one.md)
  (how STIGs are built from SRGs),
  [Chapter 07](07-network-device-stigs-management-routing-and-filtering.md)
  (network device STIGs by plane),
  [Chapter 11](11-fortiswitch-feature-version-and-srg-map.md) (the
  FortiSwitch map, for comparison),
  [Chapter 30](30-fortigate-feature-version-and-stig-map.md) (the
  FortiGate map, the model for this chapter), and
  [Chapter 31](31-cisco-products-stigs-and-srg-mapping.md) (the Cisco STIG
  packages and router roles).

**Knowledge checks:**

1. Which three STIGs apply to a Catalyst 9300 that routes between VLANs,
   and which RTR rules can you mark Not Applicable if it is not a
   perimeter or PE switch?
2. Why does this chapter use the Catalyst 9300 release notes for the
   version column, and what should you check for a Catalyst 9200?
3. Which rule do the "No direct requirement" rows point to, and why?
4. Name three fix texts that do not parse on IOS XE and what the map uses
   instead.
5. Why does the map configure `line vty 0 31` when the fix text configures
   `line vty 0 1` and `line vty 2 4`?
6. A key chain key has `send-lifetime 00:00:00 Jan 1 2026 duration 180`.
   How long is the key valid, and what should the value be?

## Summary and Completion Checklist

Catalyst 9000 switches running IOS XE are assessed against the three
Cisco IOS XE Switch STIGs: NDM for management, L2S for switching, and RTR
for routing, with the RTR perimeter and PE rules applied only to switches
in those roles. This chapter maps 352 features to the IOS XE release
that introduced them, to all 152 STIG rules (42 C-NDM,
22 C-L2S, and 88 C-RTR), and to the command that
configures them: 72 core platform features and 280 features
from the Catalyst 9300 release notes for 17.1.x through 26.2.x, of which
32 map to a rule and 248 fall under the rule to disable
unnecessary functions when unused. Every command was checked against the
IOS XE 26.x documentation, and the fix texts that needed correcting are
listed with their corrections.

- [ ] Can find the release that introduced a Catalyst switch feature, and
  check it for the model.
- [ ] Can find each IOS XE Switch STIG rule in the map, with its severity
  and SRG requirement.
- [ ] Can configure each rule with its fix text and correct the fix texts
  that do not parse.
- [ ] Can decide which RTR rules apply from the switch's role.
- [ ] Can collect a Catalyst switch's evidence and record the rules it
  cannot meet exactly.
