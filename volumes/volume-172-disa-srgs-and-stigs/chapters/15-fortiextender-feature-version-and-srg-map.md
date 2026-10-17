# Chapter 15: FortiExtender Feature, Version, and SRG Map

## Learning Objectives

- Find the FortiExtender OS release that introduced a given feature.
- Map each FortiExtender feature to the NDM, Router, or VPN SRG requirement
  it helps satisfy.
- Find the command that configures each feature to meet its requirement, on
  the managing FortiGate or on the FortiExtender itself.
- Use the map to scope an SRG-based assessment of FortiExtender, which has
  no STIG of its own.
- Account for the two ways a FortiExtender is run: managed by a FortiGate,
  or standalone.
- Confirm that the cellular WAN connection is approved before any of the
  rest applies.

## Theory and Architecture

FortiExtender is Fortinet's cellular (3G, 4G LTE, and 5G) WAN extender. It
has **no DISA STIG** (Chapter 10), so it is assessed against SRGs, as
described in Chapter 03. Chapter 10 assigns it the **Network Device
Management (NDM) SRG**. This chapter adds two SRGs for the functions that the
NDM SRG does not cover, explained in *Where the SRG data comes from*: the
**Router SRG** for a FortiExtender that routes and filters traffic, and the
**VPN SRG** for the IPsec tunnels it terminates. For every FortiExtender
feature the chapter gives **which FortiExtender OS release introduced it**,
**which requirement it relates to**, and **which command configures it to
meet that requirement**.

**First, confirm that the cellular connection is approved.** A FortiExtender
connects the network to a commercial cellular carrier, a path outside DoD
control. Cellular WAN use is subject to local DoD connection approval: the
authorizing official and the site's connection approval process must approve
the connection, the carrier, and the way the enclave is protected behind it
before the device is deployed. If the connection is not approved, no
FortiExtender may be connected, and the rest of this chapter does not apply.

A FortiExtender runs in one of two ways:

- **Managed by a FortiGate.** The FortiExtender discovers a FortiGate, the
  FortiGate authorizes it, and the two run a CAPWAP session. The FortiGate
  holds the FortiExtender settings under `config extension-controller`
  (units in `extender`, FortiExtender profiles in `extender-profile`, Wi-Fi
  SSIDs in `extender-vap`, and cellular data plans in `dataplan`) and pushes
  them to the unit, including its administrator password and management
  access protocols. In **WAN extension** mode the FortiExtender is a cellular
  WAN interface of the FortiGate, so the FortiGate's firewall policies filter
  everything that crosses the cellular link. In **LAN extension** mode the
  FortiExtender builds IPsec tunnels back to the FortiGate and carries a
  remote LAN over VXLAN inside them. This is the same model as a
  FortiLink-managed FortiSwitch (Chapter 11) and a FortiAP (Chapter 14).
- **Standalone.** The FortiExtender is managed locally, through its own GUI
  and CLI, and works as a cellular router in NAT mode or passes its cellular
  address to the device behind it in IP pass-through mode. It then has its
  own administrator accounts, firewall policies, routing, IPsec VPN, logging,
  and SNMP, all configured with FortiExtender OS commands.

A FortiExtender can also be managed from FortiManagement Cloud (called
FortiEdge Cloud in earlier documents), a Fortinet cloud service.
That service is outside the enclave and is not assessed here; use it only if
it is authorized for your environment.

### Where the version data comes from

Fortinet does not publish a feature matrix or a New Features Guide for
FortiExtender. The authoritative per-release list is the **"What's new"**
section (called **"New features or enhancements"** from 7.6.4 on) of each
**FortiExtender Release Notes** document. The version column was built from
all 30 FortiExtender release notes Fortinet publishes for the 7.0 to 8.0
trains: FortiExtender 7.0.0 through 7.0.5, 7.2.0 through 7.2.5, 7.4.0
through 7.4.9, 7.6.0 through 7.6.6, and 8.0.0. Twelve of them (7.0.4, 7.0.5,
7.2.1, 7.2.4, 7.2.5, 7.4.2, 7.4.5 through 7.4.9, and 7.6.6) say that the
release is a patch release with no new features. The entries were taken from
the release notes pages on docs.fortinet.com. The extra page in the 7.2.1 and
7.2.2 release notes about Verizon band certification and APN profiles
describes carrier fixes, not features, and is not included.

The table has two groups of rows:

- **Core platform features** (categories starting with *Core:*) are the
  long-standing capabilities that the requirements depend on: FortiGate
  management of the unit, local management access, administrator accounts,
  logging, time, SNMP, firmware and configuration backup, certificates,
  routing and firewall policies, IPsec VPN, and the cellular WAN itself.
  They existed before FortiExtender 7.0.0 and are not in any of these release
  notes; they were taken from the current CLI Reference and Administration
  Guides.
- **New features** are every entry in the 30 release notes. The release
  notes have no categories, so the categories were assigned for this
  chapter, and some titles were lightly edited for clarity. From 7.4.4 on,
  the release notes mark each entry as applying to standalone units, to
  FortiGate-managed units, or to both; the command column follows that, and
  some entries also name the FortiOS release they need. The one
  region and country code entry (7.6.1) is the *Regulatory* row.

| Version entry | Meaning |
| --- | --- |
| `7.0.0 or earlier` | A core feature that predates the oldest release notes used (FortiExtender 7.0.0) |
| `7.6.1 and later` | Introduced in FortiExtender OS 7.6.1 |

Four cautions apply. First, the version is the **FortiExtender OS** release.
Features of a FortiGate-managed unit also need a minimum **FortiOS** release
on the FortiGate (the release notes say so for some, for example the
LE-Always mode, which needs FortiOS 8.0.1); check the FortiOS and
FortiExtender OS compatibility matrix. Second, a feature introduced in a
patch release of an older train may reach a newer train only in a later
patch, so "and later" means later in the same train and, usually, in later
trains. Third, many features apply only to some models (for example the
Wi-Fi models, the FortiExtender Vehicle models with GPS, ignition sensing,
and digital I/O, and the G-series models with eSIM). Fourth, a core row
records a FortiExtender capability; a FortiGate setting shown in that row was
checked against the FortiOS 8.0.1 CLI Reference and may not exist on older
FortiOS releases.

### Where the SRG data comes from

The SRG column uses requirement IDs from the October 2026 DISA library:

| SRG column | SRG | Release | Applies to |
| --- | --- | --- | --- |
| **NDM** | Network Device Management SRG | V5R5, benchmark date 01 Jul 2026 | The FortiExtender management plane: administrator access, authentication, logging, time, SNMP, firmware, and backups (assigned by Chapter 10) |
| **RTR** | Router SRG | V5R2, benchmark date 28 Oct 2025 | A FortiExtender that routes and filters traffic between the enclave and the cellular network: firewall policies, routing protocols, link redundancy, and calls to Fortinet services |
| **VPN** | Virtual Private Network (VPN) SRG | V3R5, benchmark date 01 Jul 2026 | The IPsec tunnels a FortiExtender terminates: standalone site-to-site VPN and the LAN extension backhaul to a FortiGate |

The Router and VPN SRGs are added because the NDM SRG covers only the
management plane. A standalone FortiExtender in NAT mode is a router that
connects the enclave to a commercial network, which makes the cellular link
an alternate gateway in the Router SRG's terms; and a FortiExtender that
terminates IPsec tunnels is a VPN gateway for those tunnels. Only the Router
and VPN requirements that a FortiExtender feature relates to are cited; when
a FortiExtender is the site's only boundary device, assess it against the
rest of those SRGs as well. In WAN extension mode the FortiGate does the
routing and filtering, and its own FortiGate NDM and Firewall STIGs
(Chapter 10) cover them.

The requirement IDs are the **rule version IDs** from the XCCDF files, and
the severity is the rule's severity (high = CAT I, medium = CAT II, low =
CAT III). Each feature maps to one of three kinds of relationship:

- **Implements a requirement.** The feature is how FortiExtender meets a
  requirement. Remote syslog implements the requirement to off-load audit
  records (NDM `SRG-APP-000515-NDM-000325`), for example.
- **Must be configured to meet a requirement.** The feature is in scope of a
  requirement and has to be set up correctly. IPsec tunnels must use IKEv2,
  AES-256, and Diffie-Hellman group 16 or higher, for example.
- **No direct requirement.** The feature is operational, such as DNS proxy
  or speed tests. It has no requirement of its own, but if it is not needed
  it falls under the requirement to prohibit unnecessary functions, ports,
  protocols, and services (NDM `SRG-APP-000142-NDM-000245`).

The mapping is a starting point for an assessment, not a ruling. Confirm it
with your assessor, especially where a requirement is organization-defined or
depends on how the FortiExtender is deployed.

### Where the commands come from

The FortiExtender's own commands were checked against the **FortiExtender
8.0.0 CLI Reference**, the newest CLI Reference Fortinet publishes for
FortiExtender. A few `execute` and `get` commands that the CLI Reference
does not list (configuration backup, firmware upgrade, and session status)
come from the **FortiExtender (Standalone) 8.0.0 Admin Guide**. The FortiGate
commands were checked against the **FortiOS 8.0.1 CLI Reference**, the
newest FortiOS CLI Reference Fortinet publishes; the **FortiExtender
(Managed) 8.0.1 Admin Guide** describes how they are used. Every command in
the column was checked automatically against these documents: each `config`
path and nested table, each `set` and `unset` option against the syntax of
the command it is entered under, each listed option value against the
documented values, and each `execute` and `get` command. Read the column this
way:

- Commands that start with **FortiGate:** run on the FortiGate that manages
  the FortiExtender. For a managed unit this is where the configuration
  belongs: a setting made on the FortiExtender that the FortiGate also
  manages can be overwritten when the FortiGate pushes its profile.
- Commands that start with **FortiExtender CLI:** run on the FortiExtender
  itself, over SSH or the console. Most apply to standalone units; the
  discovery settings apply to a unit that is to be managed by a FortiGate.
- **GUI:** entries name the FortiExtender GUI page.
- Statements are separated by `;` to fit in a table cell; on the CLI, enter
  each one on its own line. Values in `<ANGLE_BRACKETS>` are placeholders for
  your own names, addresses, and keys.
- For **"No direct requirement"** rows, the command shown is the one that
  disables the feature when it is unused. A dash (**—**) means there is
  nothing to change: the feature is a model, a performance change, a GUI
  change, or a capability that is off unless configured.

Some requirements cannot be met exactly with FortiExtender settings. Record
them on the checklist as open findings with mitigations, or meet them another
way:

- **Password length.** From 7.6.3 a standalone FortiExtender requires
  administrator passwords of at least 12 characters with upper case, lower
  case, a number, and a symbol; the release notes document no rule before
  that, and the enforced minimum of 12 is below the required 15 (NDM
  `SRG-APP-000164-NDM-000252`). Set passwords of 15 or more characters by
  procedure, on the FortiExtender or with `login-password` from the
  FortiGate. No setting covers the rule that a new password must change at
  least eight characters (NDM `SRG-APP-000170-NDM-000329`).
- **Lockout.** Neither the CLI Reference nor the Admin Guides has a lockout
  setting. From 7.6.5 SSH logins are locked
  for ten minutes after five failures, and the FortiExtender 8.0.0 Log
  Message Reference shows a GUI lockout whose limits are not documented as
  settings; the requirement is three attempts and 15 minutes (NDM
  `SRG-APP-000065-NDM-000214`). Authenticate administrators against a RADIUS
  or LDAP server that enforces the lockout, and limit access with trusted
  hosts.
- **Banner.** Neither the CLI Reference nor the Admin Guides have a login
  banner setting (NDM `SRG-APP-000068-NDM-000215`). Reach the FortiExtender
  only from a management host or jump server that displays the DoD banner,
  or, for a managed unit, manage it from the FortiGate, whose own banner is
  shown at login.
- **Remote authentication.** RADIUS login arrives in 7.6.0 and LDAP in
  8.0.0; there is no TACACS+ (NDM `SRG-APP-000516-NDM-000336`). On older
  releases only local accounts exist; record the finding. RADIUS uses UDP
  only, so prefer LDAPS with `server-identity-check enable`. If remote
  authentication is enabled without the wildcard option, the account's
  local password is used only when the server is unreachable, which serves
  as the account of last resort.
- **Time synchronization.** The NTP settings apply in local management mode
  and have no authentication option (NDM `SRG-APP-000395-NDM-000347`). Point
  the FortiExtender at an internal time source on a protected path, and
  record the finding.
- **Syslog.** Remote syslog has only an address and a port, with no TLS
  option, and the Admin Guide says the syslog server must be in the same
  subnet as the FortiExtender LAN port (NDM `SRG-APP-000515-NDM-000325`).
  Put the syslog server or a relay on that subnet.
- **SNMPv3.** The authentication protocols are MD5 and SHA-1 and the privacy
  protocols are AES and DES (NDM `SRG-APP-000395-NDM-000310`). Use SHA-1 with
  AES, which is the strongest combination offered, and disable SNMP v1 and
  v2c.
- **FIPS mode.** None of the documents used has a FIPS mode setting or a
  FIPS 140 validation statement for FortiExtender (NDM
  `SRG-APP-000179-NDM-000265` and `SRG-APP-000412-NDM-000331`). Check the
  NIST Cryptographic Module Validation Program for a current certificate
  before relying on the FortiExtender's cryptography.
- **IPsec hashing.** The phase 1 and phase 2 proposals stop at SHA-256, so
  the VPN SRG rules that require SHA-384 for IKE and IPsec (VPN
  `SRG-NET-000230-VPN-000780` and `SRG-NET-000063-VPN-000220`) cannot be met.
  Use `aes256-sha256` with Diffie-Hellman groups 20 or 21, and record the
  finding.
- **LAN extension tunnels.** In LAN extension mode the FortiGate generates
  the IPsec tunnel, marks it "Do NOT edit", and uses a pre-shared key; the
  example in the Managed Admin Guide offers 3DES and SHA-1 proposals and
  Diffie-Hellman group 14 alongside stronger ones (VPN
  `SRG-NET-000522-VPN-002320` and `SRG-NET-000074-VPN-000250`). Record the
  generated proposals as evidence, and record a finding where they include
  weak algorithms.
- **OSPF authentication.** OSPF has no authentication setting and runs only
  over IPsec tunnel interfaces (RTR `SRG-NET-000168-RTR-000078` and
  `SRG-NET-000230-RTR-000001`). The IPsec tunnel authenticates the peer and
  protects the routing messages; record that as the mitigation, or use
  static routes.
- **Firmware signatures.** Firmware is signed and checked before an upgrade
  only from 7.6.4, and configuration backups only from 8.0.0 (NDM
  `SRG-APP-000131-NDM-000243`). Use 7.6.4 or later.

### Prerequisites

A FortiExtender feature often meets its requirement only if something else
is already in place. A **prerequisite** is anything that must exist or be
configured *before* a row's command can meet the requirement: the FortiGate
that manages the FortiExtender and the FortiGate interfaces it uses, the LAN
extension backhaul, cellular service on the SIMs, an external server (TFTP,
syslog, NTP, SNMP manager, RADIUS, LDAP, SCEP), certificates from the PKI,
an IPsec peer, an object that the setting refers to (address objects, a
health check, a virtual WAN interface, an access profile, an API user),
Fortinet firmware, IPv6 addressing, or a minimum FortiOS release. Settings
that the row's own command already creates are not listed again. The
approval of the cellular connection (see *Theory and Architecture*) comes
before every row, so it is not repeated in the column.

The 23 prerequisites are listed once, with IDs, in *FortiExtender
prerequisites*, and the feature map names the IDs each row needs in its
**FortiExtender prerequisites** column. A dash means the feature needs
nothing beyond the FortiExtender itself. "No direct requirement" rows, and
rows whose only requirement is to disable the feature when it is unused
(NDM `SRG-APP-000142-NDM-000245`), always show a dash, and so do the
*Models* rows. Every other row whose command runs on the FortiGate lists
**P1**, the managing FortiGate, because a managed FortiExtender gets that
setting only from its controller; so do the rows that point the
FortiExtender at the FortiGate for discovery, and the LAN extension rows
whose guidance depends on the FortiGate. In *Management mode (local,
FortiGate, or FortiManagement Cloud) and controller discovery*, which gives
a standalone and a FortiGate-managed command, P1 and P2 apply to the
FortiGate-managed command only. A FortiExtender managed from
FortiManagement Cloud gets its settings from that service instead, which
this chapter does not assess.

Fortinet publishes no feature matrix or licensing guide for FortiExtender.
The FortiExtender (Managed) 8.0.1 and (Standalone) 8.0.0 Admin Guides and
the release notes name a license only for FortiManagement Cloud management
(a valid support contract and a FortiManagement Cloud license), for FortiZTP
provisioning of LAN extension units, and for the number of speed tests per
day. None of these is needed to meet a requirement in the map, so no license
is listed. No model-support entry is listed either: the features that those
documents limit to some models (SMS notification and SMS remote
diagnostics, the Wi-Fi radios, Bluetooth, eSIM, wired 802.1X, traffic
offload, and the Vehicle model functions) appear in the map only as
functions to disable when unused, which needs no prerequisite, and P8 notes
where the eSIM of the G-series models can serve as the second SIM. The
minimum FortiOS release (P6) is given only where a release note says that a
feature with a requirement needs it. Check the FortiOS & FortiExtender OS
Compatibility Matrix and the release notes for your exact model and release
before you plan on a feature.

During an assessment, check a row's prerequisites before its command: a
correctly configured setting with a missing prerequisite (a FortiExtender
that was never authorized, SIM switching with one SIM, a syslog server
outside the LAN subnet, an unreachable RADIUS server) does not meet the
requirement, and the missing prerequisite is the finding.

## Design Considerations

- **Get the cellular connection approved first.** Record the approval, the
  carrier, the SIMs and APNs it covers, and how the enclave is protected
  behind the link.
- **Prefer FortiGate management with WAN extension.** The FortiGate then
  filters all traffic on the cellular link with its own STIG-assessed
  firewall policies, and holds the FortiExtender password and access
  settings. A standalone FortiExtender in NAT mode must do that filtering
  itself (RTR `SRG-NET-000019-RTR-000008`).
- **Pick the release first, then the features.** If your design depends on a
  feature introduced in a certain release (for example RADIUS login in
  7.6.0, signed firmware in 7.6.4, or LDAP login in 8.0.0), that sets the
  minimum FortiExtender OS release, and both the FortiExtender and the
  FortiGate must run vendor-supported releases (NDM
  `SRG-APP-001035-NDM-000340`).
- **Set the management mode explicitly.** Set `discovery-type` to `local` for
  a standalone unit, which the Admin Guide says stops it from searching for
  another controller such as a FortiGate or FortiManagement Cloud, or to
  `fortigate` with static controller addresses for a managed unit. On the
  FortiGate, enable `fortiextender-discovery-lockdown` so it answers only
  units that are already authorized.
- **Keep management off the cellular interface.** Allow HTTPS and SSH only
  on the interface that faces the management network, never on the LTE
  interfaces, and set trusted hosts for every administrator.
- **Encrypt everything that crosses the carrier.** Treat the cellular network
  as untrusted: carry enclave traffic inside IPsec, either the FortiGate's
  tunnels or the FortiExtender's own.
- **Turn off what is not used.** GPS reporting, SMS notification and SMS
  remote diagnostics, Bluetooth, automatic USB image installation, and the
  Wi-Fi radios of Wi-Fi models are all functions that need a reason to stay
  on. If the Wi-Fi radios are used, the Network WLAN STIGs (Chapter 14)
  apply to them, and WLAN must be approved too.

## Implementation and Automation

### FortiExtender prerequisites

What must be in place before the FortiExtender features in the feature map
can meet their requirements (see *Prerequisites*). The commands were
verified against the FortiExtender 8.0.0 CLI Reference, the FortiExtender
(Standalone) 8.0.0 Admin Guide, and the FortiOS 8.0.1 CLI Reference with the
same checks as the feature map; GUI entries name the pane, and entries that
are not FortiExtender or FortiGate settings are described in words.

[Download the prerequisites as CSV](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/data/volume-172-disa-srgs-and-stigs/15-fortiextender-feature-version-and-srg-map-prerequisites.csv) (23 rows).

| ID | Prerequisite | What it enables | How to put it in place | Source |
| --- | --- | --- | --- | --- |
| P1 | A FortiGate that manages the FortiExtender: the FortiExtender controller enabled, the FortiExtender discovered and authorized, and a FortiExtender profile assigned to it, on a FortiOS release that the FortiOS and FortiExtender OS compatibility matrix lists for the FortiExtender OS release | Every setting made on the FortiGate (FortiExtender profiles, the administrator password and access protocols, firmware and modem firmware pushes, WAN and LAN extension), which the FortiGate pushes to the FortiExtender; and discovery of that controller by the FortiExtender | FortiGate: `config system global; set fortiextender enable; end`, then FortiGate: `config extension-controller extender; edit <FEX_ID>; set authorized enable; set profile <PROFILE>; next; end` | FortiExtender (Managed) 8.0.1 Admin Guide, "FortiOS and FortiExtender OS compatibility" (FortiOS & FortiExtender OS Compatibility Matrix), "Before you begin", "Enable FortiExtender Controller on FortiOS", "Authorize FortiExtender on FortiOS", and "FortiExtender Profiles"; FortiOS 8.0.1 CLI Reference, config system global and config extension-controller extender |
| P2 | A FortiGate interface that the FortiExtender connects to, with Security Fabric Connection (CAPWAP) access; for broadcast discovery, in the same subnet as the FortiExtender (with a DHCP server when the FortiExtender port4 connects to it); for static discovery, reachable at layer 3 from the FortiExtender discovery interface | CAPWAP discovery of the FortiGate by the FortiExtender, with broadcast or static controller addresses | FortiGate: `config system interface; edit <FEX_INTERFACE>; set allowaccess ping fabric; next; end` | FortiExtender (Managed) 8.0.1 Admin Guide, "Enable FortiExtender Controller on FortiOS" (step 3: enable CAPWAP access on the FortiGate interface), "Discover a FortiExtender unit" (Broadcast: the FortiGate and FortiExtender must be in the same subnet; Static), and "Authorize FortiExtender on FortiOS" (static discovery when not connected on layer 2) |
| P3 | A FortiExtender WAN interface (type fext-wan) on the FortiGate, bound to the FortiExtender's modem when it is authorized in WAN extension mode | The FortiGate interface that carries the cellular WAN traffic, which the FortiGate firewall policies filter | FortiGate: `config system interface; edit <FEXT_WAN_INTERFACE>; set type fext-wan; set mode dhcp; set role wan; next; end`, then FortiGate: `config extension-controller extender; edit <FEX_ID>; set extension-type wan-extension; config wan-extension; set modem1-extension <FEXT_WAN_INTERFACE>; end; next; end` | FortiExtender (Managed) 8.0.1 Admin Guide, "Authorize FortiExtender on FortiOS" (create a virtual WAN interface of type FEX-WAN or a VLAN sub-interface and link it to the FortiExtender during authorization) and "Configuring FortiExtender in a non-root VDOM" (CLI steps 2 and 3); FortiOS 8.0.1 CLI Reference, config system interface and config extension-controller extender |
| P4 | The LAN extension backhaul: a FortiGate backhaul interface with Security Fabric Connection access that the FortiExtender uplinks can reach, the IPsec tunnel and LAN extension profile that the controller generates for the FortiExtender, and the LAN extension interface on the FortiGate with its address and firewall policies | FortiExtender LAN extension (IPsec backhaul with VXLAN), its health checks, control channel failover, and provisioning through the FortiGate | FortiGate: `config system interface; edit <BACKHAUL_INTERFACE>; set allowaccess ping fabric; next; end`; after authorization, FortiGate: `config system interface; edit <LAN_EXTENSION_INTERFACE>; set ip <IP> <MASK>; next; end` and FortiGate: `config firewall policy; edit <POLICY_ID>; set srcintf <LAN_EXTENSION_INTERFACE>; set dstintf <WAN_INTERFACE>; set srcaddr <LAN_EXTENSION_ADDRESS>; set dstaddr <DESTINATION_ADDRESS>; set service <SERVICE>; set schedule always; set action accept; next; end` | FortiExtender (Managed) 8.0.1 Admin Guide, "FortiExtender as FortiGate LAN extension" ("Authorizing the devices", "Backhaul tunnel and VXLAN auto-deployment", and "Configuring the LAN extension and firewall policy"); FortiOS 8.0.1 CLI Reference, config system interface and config firewall policy |
| P5 | A second FortiExtender uplink that reaches the FortiGate, listed in the LAN extension profile's backhaul | Fast failover of the CAPWAP LAN extension control channel between two uplinks | Connect the second uplink, then FortiGate: `config extension-controller extender-profile; edit <PROFILE>; config lan-extension; config backhaul; edit <ID>; set port <SECOND_UPLINK_PORT>; next; end; end; next; end` | FortiExtender (Managed) 8.0.1 Admin Guide, "Fast failover of CAPWAP control channel between two uplinks" (a FortiExtender that has two uplinks to the FortiGate access controller) and "Authorizing the devices" (the backhaul entries for port1 and port2) |
| P6 | FortiOS 7.6.5 or later on the managing FortiGate | Health checks in FortiExtender LAN extension profiles | Upgrade the FortiGate to FortiOS 7.6.5 or later | FortiExtender 7.6.4 Release Notes, "New features or enhancements" (health check configurations in FortiExtender LAN-Extension profiles; Managed, requires FOS 7.6.5+) |
| P7 | Firewall address objects for the site's address space, on the FortiGate or the FortiExtender that holds the policy (IPv6 address objects for IPv6 policies) | Firewall policies that limit traffic between the cellular network and the site to the site's addresses | FortiGate: `config firewall address; edit <SITE_ADDRESS_SPACE>; set subnet <IP> <MASK>; next; end`; FortiExtender CLI: `config network address; edit <SITE_ADDRESS>; set type ipmask; set subnet <SUBNET>; next; end` and FortiExtender CLI: `config network address6; edit <ADDRESS6>; set subnet <IPV6_PREFIX>; next; end` | FortiExtender (Standalone) 8.0.0 Admin Guide, "Firewall" ("Configure address/subnet", IPv4 and IPv6); FortiExtender 8.0.0 CLI Reference, config network address and config network address6; FortiOS 8.0.1 CLI Reference, config firewall address |
| P8 | Cellular service on two SIMs: two SIM cards from approved carriers installed and activated (or, on G-series models, a SIM in slot 1 and an active eSIM profile), each with a data plan that gives its APN | SIM switching by disconnect, signal, data plan, link health, latency, and jitter | Approved carrier service for both SIMs, then a data plan for each: FortiExtender CLI: `config lte plan; edit <PLAN>; set type by-carrier; set carrier <CARRIER>; set apn <APN>; next; end`; on a managed unit, FortiGate: `config extension-controller dataplan; edit <DATAPLAN>; set type carrier; set carrier <CARRIER>; set apn <APN>; next; end` and FortiGate: `config extension-controller extender-profile; edit <PROFILE>; config cellular; set dataplan <DATAPLAN>; end; next; end` | FortiExtender (Standalone) 8.0.0 Admin Guide, "Configure SIM-switch" (SIM-switch works only when two SIM cards are installed; it switches between the active eSIM profile and the SIM in slot 1), "Activate a SIM or eSIM", "Data plans and APN", and "Supported wireless carriers"; FortiExtender (Managed) 8.0.1 Admin Guide, "Data Plans" (data plans must be applied to a FortiExtender profile to take effect) |
| P9 | A link health check (hmon hchk) that probes a target across the monitored link | SIM switching by link health, latency, and jitter, and latency-based virtual WAN member selection | FortiExtender CLI: `config hmon hchk; edit <HEALTH_CHECK>; set protocol ping; set probe-target <TARGET>; set interface <INTERFACE>; next; end` | FortiExtender (Standalone) 8.0.0 Admin Guide, "Configure SIM-switch" (By Health Monitor requires an hmon hchk instance linked to the auto-switch instance), "Configure SIM-switch based on link health", and "Check SD-WAN health" (an hmon.hchk object is required for VWAN member health checking) |
| P10 | A virtual WAN interface with its members, each member with a router target and a health check | Link redundancy across the cellular and other WAN links, with failover on link health | FortiExtender CLI: `config system interface; edit <VWAN>; set type virtual-wan; set members <MEMBERS>; next; end` and FortiExtender CLI: `config system vwan-member; edit <MEMBER>; set target <TARGET>; set health-check <HEALTH_CHECK>; next; end` | FortiExtender (Standalone) 8.0.0 Admin Guide, "SD-WAN" ("Configure an SD-WAN", "Check SD-WAN health", and "Define an SD-WAN member"); FortiExtender 8.0.0 CLI Reference, config system interface and config system vwan-member |
| P11 | Fortinet firmware for the model: the FortiExtender OS image (signed from 7.6.4) and the modem firmware package that the FortiExtender Hardware and Modem Firmware Compatibility Matrix lists for the model, from the Fortinet Support site or FortiGuard | OS firmware upgrades on the FortiExtender and from the FortiGate, and modem firmware upgrades | Download the images from the Fortinet Support site (FortiExtender, MODEM-Firmware, then the model); on a managed unit the FortiGate can instead provision the matching image from FortiGuard: FortiGate: `config system global; set fortiextender-provision-on-authorization enable; end` | FortiExtender 7.4.3 Release Notes, "What's new" (modem firmware images listed in the FortiExtender Hardware and Modem Firmware Compatibility Matrix, downloaded from the Fortinet Support site); FortiExtender (Standalone) 8.0.0 Admin Guide, "Upgrade OS firmware" and "Upgrade modem firmware"; FortiExtender (Managed) 8.0.1 Admin Guide, "Provision FortiExtender firmware upon authorization" |
| P12 | A TFTP server reachable from the FortiExtender, on the management network | OS and modem firmware upgrades, and configuration backup and restore, from the FortiExtender CLI | An organization TFTP server; the commands name it as the server address | FortiExtender (Standalone) 8.0.0 Admin Guide, "Upgrade OS firmware" (TFTP), "Upgrade modem firmware" (TFTP), and "Configuration backups and restore" |
| P13 | A central syslog server or SIEM (or a syslog relay) in the same subnet as the FortiExtender LAN port | Off-loading the FortiExtender system logs to remote syslog servers | An organization syslog server or relay on the LAN subnet; the syslog settings name it | FortiExtender (Standalone) 8.0.0 Admin Guide, "Configure the system syslog" ("Export system logs to remote syslog servers": the syslog server and the FortiExtender LAN port must be part of the same subnet) |
| P14 | An internal NTP time source reachable over a protected path | Time synchronization of a standalone FortiExtender (local management mode) | An organization NTP server; the NTP settings name it | FortiExtender 8.0.0 CLI Reference, config system ntp (NTP synchronization in local management mode; type custom with ntpserver entries); FortiExtender 7.0.1 Release Notes, "What's new in FortiExtender 7.0.1" (NTP server list configuration on GUI) |
| P15 | An SNMPv3 manager loaded with the Fortinet Core MIB and FortiExtender MIB, configured with the same user and security settings, and SNMP allowed on the management interface | SNMPv3 queries and traps, including IPv6 SNMP hosts | The organization network management system, loaded with the MIB files exported with FortiExtender CLI: `execute snmpmibs export tftp`; then FortiExtender CLI: `config snmp hosts; edit <HOST>; set host-ip <NMS_IP_PREFIX>; set host-type any; next; end` and FortiExtender CLI: `config system interface; edit <MGMT_INTERFACE>; set allowaccess https ssh snmp; next; end` | FortiExtender (Standalone) 8.0.0 Admin Guide, "SNMP (read-only) and traps" (SNMP hosts and SNMP user configuration; executable SNMP commands export FORTINET-CORE-MIB.mib and FORTINET-FORTIEXTENDER-MIB.mib) and "Access allowance"; FortiExtender 8.0.0 CLI Reference, config snmp hosts |
| P16 | An administrator access profile that grants the administrator's role | Local administrator accounts with the access level of their role | FortiExtender CLI: `config system accprofile; edit <PROFILE>; set system read; next; end` | FortiExtender 7.0.0 Release Notes, "Administration access profile"; FortiExtender 8.0.0 CLI Reference, config system accprofile; Chapter 15 row *Administrator access profiles (read-write, read-only, or no access per configuration section)* |
| P17 | A reachable organization RADIUS server with the administrator accounts and a unique shared secret, which enforces the account lockout | RADIUS authentication of FortiExtender administrators, by IP address or FQDN, with a set source address | An organization RADIUS service, then FortiExtender CLI: `config user radius; edit <RADIUS>; set server <RADIUS_SERVER>; set secret <SECRET>; next; end` | FortiExtender (Standalone) 8.0.0 Admin Guide, "RADIUS authentication" (requires configuring a RADIUS server; default port 1812); FortiExtender 7.6.0 Release Notes, "What's new" (RADIUS authentication on FortiExtender) |
| P18 | A reachable organization LDAP directory with the administrator accounts, serving LDAPS | LDAP authentication of FortiExtender administrators | An organization directory service with LDAPS enabled; the FortiExtender LDAP entry names it and its CA certificate (P19) | FortiExtender (Standalone) 8.0.0 Admin Guide, "LDAP authentication" (LDAP, STARTTLS, and LDAPS; ca-cert and server-identity-check); FortiExtender 8.0.0 Release Notes, "New features or enhancements" (remote authentication through LDAP) |
| P19 | Certificates from the DoD PKI imported on the FortiExtender: the DoD CA certificates, and a certificate issued to the FortiExtender with its private key | HTTPS management with a trusted certificate, IPsec authentication with certificates (RSA or ECDSA), and validation of the LDAPS server | FortiExtender CLI: `execute vpn certificate ca import tftp <REMOTE_FILE> <CA_NAME> <TFTP_SERVER>` and FortiExtender CLI: `execute vpn certificate local import tftp <REMOTE_FILE> <CERT_NAME> <TFTP_SERVER> <PASSWORD>`, or in the GUI at Settings > Certificate | FortiExtender (Standalone) 8.0.0 Admin Guide, "IPsec VPN support for third-party certificates" (import a third-party CA certificate and local certificate) and "Entity certificates in FortiExtender" ("Certificate for HTTPS management access"); Chapter 15 row *Local and CA certificates* |
| P20 | An SCEP server reachable from the FortiExtender over HTTP, issuing certificates from the organization PKI | Certificate enrollment through SCEP | An organization SCEP service; the certificate request names its URL | FortiExtender (Standalone) 8.0.0 Admin Guide, "Third-party certificates through an SCEP server" (FortiExtender sends the CSR to an SCEP server for signing; it supports an HTTP connection to the SCEP server) |
| P21 | An IPsec peer with matching phase 1 and phase 2 settings (a FortiGate or another FortiExtender, or a third-party gateway when certificates are used), and on the FortiExtender a route to the remote network through the tunnel and two accept firewall policies | Site-to-site IPsec VPN tunnels and redundant tunnels, the tunnel interfaces that OSPF runs over, and changes to an existing tunnel's proposals | Configure the peer with the same phase 1 and phase 2 settings; then FortiExtender CLI: `config router static; edit <ID>; set dst <REMOTE_SUBNET>; set device <TUNNEL>; next; end` and two accept firewall policies between the local and remote addresses | FortiExtender (Standalone) 8.0.0 Admin Guide, "Configure VPN" (phase 1 and phase 2 parameters on both peers, routing, and two ACCEPT firewall policies; signature mode with the default Fortinet certificates only supports FortiGate or FortiExtender peers) and "Configure dynamic routing — OSPF"; FortiExtender 7.0.0 Release Notes, "OSPF" (point-to-point network type over IPsec tunnel) |
| P22 | IPv6 addresses on the FortiExtender interfaces (a static IPv6 address on the WAN interface for an IPv6 IPsec tunnel) | Management access over IPv6, IPv6 firewall policies, IPv6 IPsec VPN, and IPv6 SNMP hosts | FortiExtender CLI: `config system interface; edit <INTERFACE>; config ipv6; set ip6-mode static; set ip6-address <IPV6_PREFIX>; end; next; end` | FortiExtender (Standalone) 8.0.0 Admin Guide, "Configuring IPv6" and "Configure VPN" (IPv6 VPN tunnels need a static IPv6 address on the WAN interface and IPv4 and IPv6 addresses on the LAN interface); FortiExtender 8.0.0 CLI Reference, config system interface |
| P23 | An API user entry on the FortiExtender | API tokens with an expiration time | FortiExtender CLI: `config system api-user; edit <API_USER>; set comment <COMMENT>; next; end` | FortiExtender 8.0.0 CLI Reference, config system api-user and execute api-user generate-key (generates an API token and token expiration time for an API user) |

### The FortiExtender feature map

The SRG column uses the abbreviations defined in *Where the SRG data comes
from*. The requirement titles are listed in the next table. The command
column follows the conventions in *Where the commands come from*.
The last column lists the IDs from *FortiExtender prerequisites*.

[Download the feature map as CSV](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/data/volume-172-disa-srgs-and-stigs/15-fortiextender-feature-version-and-srg-map-feature-map.csv) (154 rows).

| Category | Feature | Introduced (FortiExtender OS) | SRG requirement(s) | Command to satisfy the requirement | FortiExtender prerequisites |
| --- | --- | --- | --- | --- | --- |
| Core: FortiGate-managed operation | FortiExtender controller on the FortiGate | 7.0.0 or earlier | NDM `SRG-APP-000142-NDM-000245` | FortiGate: `config system global; set fortiextender disable; end` (only when the FortiGate manages no FortiExtender) | — |
| Core: FortiGate-managed operation | FortiExtender discovery and authorization on the FortiGate (CAPWAP) | 7.0.0 or earlier | NDM `SRG-APP-000516-NDM-000335`; NDM `SRG-APP-000038-NDM-000213` | FortiGate: `config system global; set fortiextender-discovery-lockdown enable; end`; FortiGate: `config extension-controller extender; edit <FEX_ID>; set authorized enable; next; end` | P1, P2 |
| Core: FortiGate-managed operation | FortiExtender profiles pushed from the FortiGate | 7.0.0 or earlier | NDM `SRG-APP-000516-NDM-000317`; NDM `SRG-APP-000380-NDM-000304` | FortiGate: `config extension-controller extender-profile; edit <PROFILE>; set model <MODEL>; set extension wan-extension; next; end` | P1 |
| Core: FortiGate-managed operation | FortiExtender administrator password set from the FortiGate | 7.0.0 or earlier | NDM `SRG-APP-000164-NDM-000252`; NDM `SRG-APP-000148-NDM-000346` | FortiGate: `config extension-controller extender-profile; edit <PROFILE>; set login-password-change yes; set login-password <PASSWORD_15_CHARS_MIN>; next; end` | P1 |
| Core: FortiGate-managed operation | FortiExtender management access protocols set from the FortiGate | 7.0.0 or earlier | NDM `SRG-APP-000142-NDM-000245`; NDM `SRG-APP-000412-NDM-000331`; NDM `SRG-APP-000408-NDM-000314` | FortiGate: `config extension-controller extender-profile; edit <PROFILE>; set allowaccess https ssh; next; end` | P1 |
| Core: FortiGate-managed operation | WAN extension mode: the FortiExtender as a cellular WAN interface of the FortiGate | 7.0.0 or earlier | RTR `SRG-NET-000019-RTR-000008`; RTR `SRG-NET-000202-RTR-000001` | FortiGate: `config firewall policy; edit <POLICY_ID>; set srcintf <FEXT_WAN_INTERFACE>; set dstintf <INTERNAL_INTERFACE>; set dstaddr <SITE_ADDRESS_SPACE>; set action accept; next; end` | P1, P3, P7 |
| Core: FortiGate-managed operation | Cellular data plans, APNs, and SIM selection from the FortiGate | 7.0.0 or earlier | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — | — |
| Core: FortiGate-managed operation | FortiExtender firmware push from the FortiGate | 7.0.0 or earlier | NDM `SRG-APP-000457-NDM-000352`; NDM `SRG-APP-001035-NDM-000340` | FortiGate: `execute extender push-fortiextender-image <VDOM> <FEX_SERIAL> <IMAGE_FILE>` | P1, P11 |
| Core: Management | Management mode (local, FortiGate, or FortiManagement Cloud) and controller discovery | 7.0.0 or earlier | NDM `SRG-APP-000038-NDM-000213`; RTR `SRG-NET-000131-RTR-000083` | FortiExtender CLI: `config system management; set discovery-type local; end` (standalone); FortiExtender CLI: `config system management; set discovery-type fortigate; config fortigate; set ac-discovery-type static; end; end` (FortiGate-managed) | P1, P2 |
| Core: Management | Management access per interface (allowaccess: HTTPS, SSH, SNMP, ping) | 7.0.0 or earlier | NDM `SRG-APP-000142-NDM-000245`; NDM `SRG-APP-000412-NDM-000331`; NDM `SRG-APP-000408-NDM-000314` | FortiExtender CLI: `config system interface; edit <INTERFACE>; set allowaccess https ssh; next; end` | — |
| Core: Management | Telnet and HTTP management access | 7.0.0 or earlier | NDM `SRG-APP-000142-NDM-000245`; NDM `SRG-APP-000172-NDM-000259` | FortiExtender CLI: `config system interface; edit <INTERFACE>; set allowaccess https ssh; next; end` (leave Telnet and HTTP out of the list) | — |
| Core: Management | Management service ports (HTTP, HTTPS, SSH, Telnet) | 7.0.0 or earlier | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — | — |
| Core: Management | Console port | 7.0.0 or earlier | NDM `SRG-APP-000408-NDM-000314` | — (physical access control; the console requires an administrator login) | — |
| Core: Administrator accounts | Local administrator accounts | 7.0.0 or earlier | NDM `SRG-APP-000148-NDM-000346`; NDM `SRG-APP-000153-NDM-000249` | FortiExtender CLI: `config system admin; edit <ADMIN>; set accprofile <PROFILE>; set password <PASSWORD_15_CHARS_MIN>; next; end` | P16 |
| Core: Administrator accounts | Administrator password storage (hashed, shown as ENC) | 7.0.0 or earlier | NDM `SRG-APP-000171-NDM-000258` | — | — |
| Core: Logging | Local event logs (System, Controller, Configuration, LTE, VPN, and other categories) | 7.0.0 or earlier | NDM `SRG-APP-000095-NDM-000225`; NDM `SRG-APP-000503-NDM-000320`; NDM `SRG-APP-000026-NDM-000208`; NDM `SRG-APP-000505-NDM-000322`; NDM `SRG-APP-000357-NDM-000293` | GUI: Logs | — |
| Core: Logging | Remote syslog servers | 7.0.0 or earlier | NDM `SRG-APP-000515-NDM-000325`; NDM `SRG-APP-000516-NDM-000350` | FortiExtender CLI: `config system syslog; config remote-servers; edit <ID>; set ip <SYSLOG_SERVER>; set port 514; next; end; end` | P13 |
| Core: Logging | System statistic reports (CPU, memory, and temperature thresholds) to syslog | 7.0.0 or earlier | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | FortiExtender CLI: `config system syslog; config statistic-report; set status disable; end; end` | — |
| Core: Time | NTP time synchronization (local management mode) | 7.0.0 or earlier | NDM `SRG-APP-000920-NDM-000320`; NDM `SRG-APP-000374-NDM-000299`; NDM `SRG-APP-000395-NDM-000347` | FortiExtender CLI: `config system ntp; set type custom; config ntpserver; edit <ID>; set server <NTP_SERVER>; next; end; end` | P14 |
| Core: SNMP | SNMP v1 and v2c communities | 7.0.0 or earlier | NDM `SRG-APP-000142-NDM-000245`; NDM `SRG-APP-000395-NDM-000310` | FortiExtender CLI: `config snmp community; edit <COMMUNITY>; set status disable; next; end` | — |
| Core: SNMP | SNMPv3 users and traps | 7.0.0 or earlier | NDM `SRG-APP-000395-NDM-000310` | FortiExtender CLI: `config snmp user; edit <SNMP_USER>; set status enable; set security-level auth-priv; set auth-proto sha1; set auth-pwd <AUTH_PASSWORD>; set priv-proto aes; set priv-pwd <PRIV_PASSWORD>; next; end` | P15 |
| Core: Firmware and configuration | OS firmware upgrade (TFTP, FTP, USB, cloud, or GUI) | 7.0.0 or earlier | NDM `SRG-APP-000457-NDM-000352`; NDM `SRG-APP-001035-NDM-000340`; NDM `SRG-APP-000516-NDM-000335` | FortiExtender CLI: `execute restore os-image tftp <IMAGE> <TFTP_SERVER>` | P11, P12 |
| Core: Firmware and configuration | Automatic image installation from USB | 7.0.0 or earlier | NDM `SRG-APP-000142-NDM-000245`; NDM `SRG-APP-000516-NDM-000335` | FortiExtender CLI: `config system global; set auto-install-image disable; end` | — |
| Core: Firmware and configuration | Modem firmware upgrade | 7.0.0 or earlier | NDM `SRG-APP-000457-NDM-000352` | FortiExtender CLI: `execute restore modem-fw tftp <PACKAGE> <TFTP_SERVER>` | P11, P12 |
| Core: Firmware and configuration | Configuration backup and restore | 7.0.0 or earlier | NDM `SRG-APP-000516-NDM-000340` | FortiExtender CLI: `execute config backup tftp <REMOTE_FILE> <TFTP_SERVER> encrypt <PASSWORD>` | P12 |
| Core: Firmware and configuration | Diagnostics package export (debug information) | 7.0.0 or earlier | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — | — |
| Core: Certificates | Local and CA certificates | 7.0.0 or earlier | NDM `SRG-APP-000516-NDM-000344`; NDM `SRG-APP-000910-NDM-000300` | GUI: Settings > Certificate | P19 |
| Core: Notifications | SMS notification of alerts | 7.0.0 or earlier | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | FortiExtender CLI: `config system sms-notification; set notification disable; end` | — |
| Core: Notifications | Remote diagnostics and commands by SMS | 7.0.0 or earlier | NDM `SRG-APP-000142-NDM-000245`; NDM `SRG-APP-000408-NDM-000314` | FortiExtender CLI: `config system sms-remote-diag; set remote-diag disable; end` | — |
| Core: Management | FortiExtender REST API and API users | 7.0.0 or earlier | NDM `SRG-APP-000408-NDM-000314` | — | — |
| Core: Networking | NAT and IP pass-through operating modes | 7.0.0 or earlier | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — | — |
| Core: Networking | Firewall policies (standalone NAT mode) | 7.0.0 or earlier | RTR `SRG-NET-000019-RTR-000008`; RTR `SRG-NET-000202-RTR-000001`; RTR `SRG-NET-000018-RTR-000001` | FortiExtender CLI: `config firewall policy; edit <POLICY_ID>; set srcintf <LTE_INTERFACE>; set dstintf <LAN_INTERFACE>; set dstaddr <SITE_ADDRESS>; set action accept; next; end` | P7 |
| Core: Networking | Static routing and policy-based routing | 7.0.0 or earlier | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — | — |
| Core: Networking | DHCP server | 7.0.0 or earlier | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | FortiExtender CLI: `config system dhcpserver; edit <ID>; set status disable; next; end` | — |
| Core: Networking | Virtual WAN (VWAN) interfaces and link health monitoring | 7.0.0 or earlier | RTR `SRG-NET-000760-RTR-000160` | FortiExtender CLI: `config hmon hchk; edit <HEALTH_CHECK>; set protocol ping; set probe-target <TARGET>; set interface <INTERFACE>; next; end` | P10 |
| Core: Networking | VRRP with a FortiGate (FortiGate backup mode) | 7.0.0 or earlier | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | FortiExtender CLI: `config system management; config fortigate-backup; set status disable; end; end` | — |
| Core: Networking | Multicast routing (PIM-SM) | 7.0.0 or earlier | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — | — |
| Core: VPN | IPsec VPN tunnels (standalone) | 7.0.0 or earlier | VPN `SRG-NET-000132-VPN-000460`; VPN `SRG-NET-000074-VPN-000250`; VPN `SRG-NET-000317-VPN-001090`; VPN `SRG-NET-000525-VPN-002330`; VPN `SRG-NET-000371-VPN-001640`; VPN `SRG-NET-000337-VPN-001300`; VPN `SRG-NET-000337-VPN-001290`; VPN `SRG-NET-000230-VPN-000780`; VPN `SRG-NET-000063-VPN-000220`; VPN `SRG-NET-000164-VPN-000560` | FortiExtender CLI: `config vpn ipsec phase1-interface; edit <TUNNEL>; set ike-version 2; set proposal aes256-sha256; set dhgrp 20 21; set keylife 28800; set authmethod signature; set certificate <LOCAL_CERT>; set peer <CA_CERT>; next; end`; FortiExtender CLI: `config vpn ipsec phase2-interface; edit <PHASE2>; set phase1name <TUNNEL>; set proposal aes256-sha256; set pfs enable; set dhgrp 20 21; set keylifeseconds 28800; next; end` | P19, P21 |
| Core: Cellular WAN | Cellular modem, SIM, carrier, and data plan (APN) configuration | 7.0.0 or earlier | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — | — |
| Core: Cellular WAN | SIM PIN lock | 7.0.0 or earlier | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — | — |
| Core: Cellular WAN | SIM switching (by disconnect, signal, or data plan) | 7.0.0 or earlier | RTR `SRG-NET-000760-RTR-000160` | FortiExtender CLI: `config lte setting; config modem1; config auto-switch; set by-disconnect enable; end; end; end` | P8 |
| Core: Cellular WAN | GPS | 7.0.0 or earlier | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | FortiExtender CLI: `config lte setting; config modem1; set gps disable; end; end`; FortiGate: `config extension-controller extender-profile; edit <PROFILE>; config cellular; config modem1; set gps disable; end; end; next; end` | — |
| Core: Cellular WAN | Controller reports of cellular status | 7.0.0 or earlier | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — | — |
| Administrator accounts | Administrator access profiles (read-write, read-only, or no access per configuration section) | 7.0.0 and later | NDM `SRG-APP-000033-NDM-000212`; NDM `SRG-APP-000231-NDM-000271` | FortiExtender CLI: `config system accprofile; edit <PROFILE>; set system read; set vpn read; next; end`; FortiExtender CLI: `config system admin; edit <ADMIN>; set accprofile <PROFILE>; next; end` | — |
| Routing | OSPF over IPsec tunnels (Area 0, point-to-point, redistribution of static and connected routes) | 7.0.0 and later | RTR `SRG-NET-000168-RTR-000078`; RTR `SRG-NET-000230-RTR-000001` | FortiExtender CLI: `config router ospf; set status disable; end` (when unused; there is no OSPF authentication setting, see *Where the commands come from*) | P21 |
| GUI | GUI pop-up warning when the IP address of the connection interface is changed | 7.0.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — | — |
| Time | NTP server list configuration in the GUI | 7.0.1 and later | NDM `SRG-APP-000920-NDM-000320` | FortiExtender CLI: `config system ntp; set type custom; config ntpserver; edit <ID>; set server <NTP_SERVER>; next; end; end` | P14 |
| GUI | Resetting configuration values to default in the GUI | 7.0.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — | — |
| Monitoring | FortiView LTE time scaling | 7.0.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — | — |
| Certificates | Download of third-party VPN certificates from the cloud | 7.0.1 and later | NDM `SRG-APP-000516-NDM-000344`; VPN `SRG-NET-000164-VPN-000560` | — | — |
| Management | Idle timeout for console, SSH, and Telnet sessions | 7.0.1 and later | NDM `SRG-APP-000190-NDM-000267` | FortiExtender CLI: `config system management; config local-access; set idle-timeout 5; end; end` | — |
| LAN extension | FortiExtender as a FortiGate LAN interface extension (IPsec backhaul with VXLAN) | 7.0.2 and later | VPN `SRG-NET-000371-VPN-001650`; VPN `SRG-NET-000132-VPN-000460`; VPN `SRG-NET-000074-VPN-000250`; VPN `SRG-NET-000230-VPN-000780`; VPN `SRG-NET-000522-VPN-002320` | FortiGate: `config extension-controller extender-profile; edit <PROFILE>; set extension lan-extension; config lan-extension; set ipsec-tunnel <TUNNEL>; set backhaul-interface <INTERFACE>; end; next; end` | P1, P4 |
| Monitoring | Bandwidth metering | 7.0.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — | — |
| Management | Multiple static access controller (FortiGate) addresses or FQDNs | 7.0.2 and later | NDM `SRG-APP-000038-NDM-000213` | FortiExtender CLI: `config system management; config fortigate; set ac-discovery-type static; config static-ac-addr; edit <ID>; set server <FORTIGATE_ADDRESS>; next; end; end; end` | P1, P2 |
| IPv6 | IPv6 support | 7.0.2 and later | RTR `SRG-NET-000512-RTR-000014` | FortiExtender CLI: `config system interface; edit <EXTERNAL_INTERFACE>; config ipv6; set ip6-send-adv disable; end; next; end` | — |
| Management | Trusted hosts for administrators | 7.0.2 and later | NDM `SRG-APP-000408-NDM-000314`; NDM `SRG-APP-000038-NDM-000213` | FortiExtender CLI: `config system admin; edit <ADMIN>; set trusthost1 <MGMT_SUBNET>; next; end` | — |
| Administrator accounts | Removal of the default admin account | 7.0.2 and later | NDM `SRG-APP-000148-NDM-000346` | — (create a named administrator account, then delete the default admin account) | — |
| Cellular WAN | Connection manager waits for the modem to attach to the network | 7.0.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — | — |
| Administrator accounts | CLI login user status and forced logout of administrator sessions | 7.0.3 and later | NDM `SRG-APP-000296-NDM-000280`; NDM `SRG-APP-000001-NDM-000200` | FortiExtender CLI: `get system admin status`; FortiExtender CLI: `execute disconnect-admin-session all <ADMIN>` | — |
| SNMP | SNMP MIB-2 interface statistics | 7.0.3 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — | — |
| DNS | DNS service (DNS proxy and DNS database with split DNS) | 7.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — | — |
| Models | New hardware models: FortiExtender 101F and 212F | 7.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — | — |
| Administrator accounts | GUI reference information, login user status, and forced logout | 7.2.0 and later | NDM `SRG-APP-000296-NDM-000280`; NDM `SRG-APP-000001-NDM-000200` | FortiExtender CLI: `get system admin status`; FortiExtender CLI: `execute disconnect-admin-session all <ADMIN>` | — |
| FortiGate-managed operation | CAPWAP tunnel performance improvement with FortiOS 7.2.0 in WAN extension deployments | 7.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — | — |
| Networking | DHCP client optimization | 7.2.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — | — |
| Management | REST API error message handling | 7.2.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — | — |
| DNS | System DNS requests forced through the DNS proxy | 7.2.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — | — |
| Logging | Multiple remote syslog servers (syslog database instead of a plain text file) | 7.2.2 and later | NDM `SRG-APP-000515-NDM-000325`; NDM `SRG-APP-000516-NDM-000350` | FortiExtender CLI: `config system syslog; config remote-servers; edit <ID>; set ip <SYSLOG_SERVER>; set port 514; next; end; end` | P13 |
| GUI | SFP DSL interface support in the GUI | 7.2.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — | — |
| Networking | DHCP relay over VPN | 7.2.3 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | FortiExtender CLI: `config system dhcprelay; set status disable; end` | — |
| Cellular WAN | Unblocking SIM cards with their PUK codes from the CLI (FEX-511F) | 7.2.3 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — | — |
| Models | New hardware model: FEX-202F | 7.2.3 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — | — |
| Networking | Multicast while the FortiExtender is the primary VRRP router | 7.4.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — | — |
| LAN extension | CAPWAP control channel backup over a second uplink | 7.4.0 and later | RTR `SRG-NET-000760-RTR-000160` | — | P1, P4, P5 |
| Management | SSH client login to other devices from the FortiExtender | 7.4.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — | — |
| Cellular WAN | SIM switching based on link health | 7.4.0 and later | RTR `SRG-NET-000760-RTR-000160` | FortiExtender CLI: `config lte setting; config modem1; config auto-switch; set by-health-monitor enable; end; end; end` | P8, P9 |
| Networking | DHCP relay to multiple DHCP servers | 7.4.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | FortiExtender CLI: `config system dhcprelay; set status disable; end` | — |
| Wi-Fi | Wi-Fi function on FEV-211F | 7.4.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | FortiExtender CLI: `config wifi; config radio-profile; edit <RADIO_PROFILE>; set status disable; next; end; end` | — |
| Cellular WAN | SIM switching based on latency and jitter | 7.4.1 and later | RTR `SRG-NET-000760-RTR-000160` | FortiExtender CLI: `config lte setting; config modem1; config auto-switch; set by-latency enable; set by-jitter enable; end; end; end` | P8, P9 |
| Networking | Network latency in the SD-WAN (virtual WAN) member selection | 7.4.1 and later | RTR `SRG-NET-000760-RTR-000160` | FortiExtender CLI: `config system vwan-member; edit <MEMBER>; set link-cost-factor latency; next; end` | P9, P10 |
| VPN | Redundant VPN tunnels between a FortiExtender and a FortiExtender or FortiGate | 7.4.1 and later | RTR `SRG-NET-000760-RTR-000160` | — | P21 |
| Firmware and configuration | Modem firmware upgrade from the FortiGate | 7.4.3 and later | NDM `SRG-APP-000457-NDM-000352` | FortiGate: `execute extender install-forticloud-mdm-package <PACKAGE> <FEX_SERIAL>` | P1, P11 |
| FortiGate-managed operation | Hitless failover in WAN extension mode with FortiGate HA | 7.4.4 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — | — |
| Wi-Fi | Wi-Fi configuration in FortiExtender profiles (managed) | 7.4.4 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | FortiGate: `config extension-controller extender-profile; edit <PROFILE>; config wifi; config radio-1; set status disable; end; end; next; end` | — |
| Wi-Fi | Wi-Fi VAPs as members of a switch interface | 7.4.4 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — | — |
| LAN extension | VLAN support in LAN extension mode | 7.4.4 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — | — |
| Management | Management access (allowaccess) on tunnel interfaces | 7.4.4 and later | NDM `SRG-APP-000142-NDM-000245` | FortiExtender CLI: `config system interface; edit <TUNNEL_INTERFACE>; unset allowaccess; next; end` | — |
| VPN | IPsec VPN with ECDSA certificates (DH groups 20, 29, and 32) | 7.4.4 and later | VPN `SRG-NET-000074-VPN-000250`; VPN `SRG-NET-000164-VPN-000560` | FortiExtender CLI: `config vpn ipsec phase1-interface; edit <TUNNEL>; set authmethod signature; set certificate <ECDSA_CERT>; set peer <CA_CERT>; set dhgrp 20; next; end` | P19, P21 |
| Authentication | RADIUS authentication of administrators | 7.6.0 and later | NDM `SRG-APP-000516-NDM-000336`; NDM `SRG-APP-000153-NDM-000249` | FortiExtender CLI: `config user radius; edit <RADIUS>; set server <RADIUS_SERVER>; set secret <SECRET>; set auth-type ms_chap_v2; next; end`; FortiExtender CLI: `config user group; edit <GROUP>; set member <RADIUS>; next; end`; FortiExtender CLI: `config system admin; edit <ADMIN>; set remote-auth enable; set remote-group <GROUP>; next; end` | P17 |
| LAN extension | Multiple VLANs in LAN extension mode | 7.6.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — | — |
| Cellular WAN | Multiple simultaneous packet data networks (APNs) on FEX-511G and FEX-511G-WiFi in WAN extension mode | 7.6.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | FortiGate: `config extension-controller extender-profile; edit <PROFILE>; config cellular; config modem1; set multiple-PDN disable; end; end; next; end` | — |
| Certificates | Custom certificate for HTTPS management access | 7.6.1 and later | NDM `SRG-APP-000516-NDM-000344`; NDM `SRG-APP-000412-NDM-000331` | FortiExtender CLI: `config system global; set admin-server-cert <CERT_NAME>; end` | P19 |
| Management | SSH strong cryptography with configurable key exchange, cipher, host key, and MAC algorithms | 7.6.1 and later | NDM `SRG-APP-000412-NDM-000331`; NDM `SRG-APP-000411-NDM-000330` | FortiExtender CLI: `config system ssh-crypto; set strong-crypto enable; set ssh-enc-algo aes256-ctr aes256-gcm@openssh.com; set ssh-mac-algo hmac-sha2-256 hmac-sha2-512; end` | — |
| FortiGate-managed operation | FortiCare registration of the FortiExtender through FortiOS | 7.6.1 and later | RTR `SRG-NET-000131-RTR-000083` | — | — |
| LAN extension | Split tunneling in LAN extension mode (traffic that bypasses the SASE overlay) | 7.6.1 and later | RTR `SRG-NET-000018-RTR-000001` | — (configure no traffic split services in the LAN extension profile) | — |
| Wi-Fi | DFS channels on FEV-21xF and FBS-10F in permitted regions | 7.6.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — | — |
| Regulatory | Wi-Fi country code and SKU mapping aligned with other Fortinet F and G series Wi-Fi products | 7.6.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — | — |
| Automation | Automation stitches for digital I/O on FortiExtender Vehicle models | 7.6.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — | — |
| Authentication | Wired 802.1X authentication on LAN ports (select models) | 7.6.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — | — |
| Authentication | RADIUS servers specified by FQDN | 7.6.2 and later | NDM `SRG-APP-000516-NDM-000336` | FortiExtender CLI: `config user radius; edit <RADIUS>; set server <RADIUS_FQDN>; next; end` | P17 |
| Certificates | Third-party certificates through an SCEP server | 7.6.2 and later | NDM `SRG-APP-000516-NDM-000344` | FortiExtender CLI: `config vpn certificate local; edit <CERT>; set enroll-protocol scep; next; end`; FortiExtender CLI: `execute vpn certificate local generate rsa <CERT> <KEY_SIZE_2048_OR_4096> <SUBJECT> <SCEP_URL>` | P20 |
| Management | Out-of-band management (OBM) tunnel to FortiManagement Cloud in FortiGate mode | 7.6.2 and later | RTR `SRG-NET-000131-RTR-000083`; NDM `SRG-APP-000142-NDM-000245` | — (do not provision the FortiExtender as the OBM type in the FortiManagement Cloud portal) | — |
| Vehicle | Ignition sensing on FEV-211F and FEV-212F | 7.6.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — | — |
| Vehicle | Bluetooth button control on BLE-capable models | 7.6.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | FortiExtender CLI: `config system bluetooth; set status disable; end` | — |
| Administrator accounts | Stronger administrator password requirements (12 characters with upper case, lower case, number, and symbol) | 7.6.3 and later | NDM `SRG-APP-000164-NDM-000252`; NDM `SRG-APP-000166-NDM-000254`; NDM `SRG-APP-000167-NDM-000255`; NDM `SRG-APP-000168-NDM-000256`; NDM `SRG-APP-000169-NDM-000257` | FortiExtender CLI: `config system admin; edit <ADMIN>; set password <PASSWORD_15_CHARS_MIN>; next; end` | — |
| Models | New hardware models: FEV-511G, FEX-101G, and FEX-211G | 7.6.4 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — | — |
| Cellular WAN | eSIM on G-series models | 7.6.4 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | FortiExtender CLI: `config lte setting; config modem1; set esim disable; end; end` | — |
| LAN extension | LAN extension member VLAN ID (select models, FortiOS 7.6.4 or later) | 7.6.4 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — | — |
| LAN extension | Power reset of LE-switch member ports when the LAN extension connection changes | 7.6.4 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — | — |
| IPv6 | API and GUI access over IPv6 | 7.6.4 and later | NDM `SRG-APP-000142-NDM-000245`; NDM `SRG-APP-000408-NDM-000314` | FortiExtender CLI: `config system interface; edit <INTERFACE>; config ipv6; set ip6-allowaccess https ssh; end; next; end` | P22 |
| IPv6 | IPv6 stateless address autoconfiguration (SLAAC) | 7.6.4 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — | — |
| IPv6 | IPv4 and IPv6 dual stack | 7.6.4 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — | — |
| IPv6 | IPv6 addresses in firewall policies | 7.6.4 and later | RTR `SRG-NET-000202-RTR-000001`; RTR `SRG-NET-000018-RTR-000001` | FortiExtender CLI: `config firewall policy; edit <POLICY_ID>; set srcaddr6 <ADDRESS6>; set dstaddr6 <ADDRESS6>; set action accept; next; end` | P7, P22 |
| IPv6 | IPv6 DNS for the DNS proxy | 7.6.4 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — | — |
| IPv6 | IPv6 addressing | 7.6.4 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — | — |
| IPv6 | Static IPv6 addresses and routing | 7.6.4 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — | — |
| Authentication | Source IP address for RADIUS server communication | 7.6.4 and later | NDM `SRG-APP-000516-NDM-000336` | FortiExtender CLI: `config user radius; edit <RADIUS>; set source-ip <SOURCE_IP>; next; end` | P17 |
| DNS | DNS category filtering with DNS filter profiles | 7.6.4 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — | — |
| Wi-Fi | Captive portals and captive portal redirection on Wi-Fi models in LAN extension mode | 7.6.4 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — | — |
| Logging | VWAN log category | 7.6.4 and later | NDM `SRG-APP-000095-NDM-000225` | GUI: Logs | — |
| Firmware and configuration | Firmware signed with a SHA-256 signature | 7.6.4 and later | NDM `SRG-APP-000131-NDM-000243` | — (the signature is checked automatically before an upgrade) | — |
| Administrator accounts | Encryption of all password and key settings | 7.6.4 and later | NDM `SRG-APP-000171-NDM-000258` | — | — |
| Firmware and configuration | Encrypted configuration backup and restore | 7.6.4 and later | NDM `SRG-APP-000516-NDM-000340` | FortiExtender CLI: `execute config backup tftp <REMOTE_FILE> <TFTP_SERVER> encrypt <PASSWORD>` | P12 |
| LAN extension | Health checks in LAN extension profiles (FortiOS 7.6.5 or later) | 7.6.4 and later | RTR `SRG-NET-000760-RTR-000160` | FortiGate: `config extension-controller extender-profile; edit <PROFILE>; config lan-extension; config backhaul; edit <ID>; set port <PORT>; set health-check-interval <SECONDS>; next; end; end; next; end` | P1, P4, P6 |
| LAN extension | FortiZTP provisioning of FortiExtenders in LAN extension mode | 7.6.5 and later | RTR `SRG-NET-000362-RTR-000109` | — (provision through the FortiGate instead of FortiZTP) | P1, P4 |
| VPN | Null encryption (null-sha1 and null-sha256) in IPsec phase 2 | 7.6.5 and later | VPN `SRG-NET-000371-VPN-001650`; VPN `SRG-NET-000525-VPN-002330` | FortiExtender CLI: `config vpn ipsec phase2-interface; edit <PHASE2>; set proposal aes256-sha256; next; end` | P21 |
| IPv6 | IPv6 prefix delegation with SLAAC | 7.6.5 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — | — |
| GUI | Redesigned GUI layout | 7.6.5 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — | — |
| VPN | IPv6 IPsec VPN (IPv6 transport, phase 2 selectors, dual stack) | 7.6.5 and later | VPN `SRG-NET-000132-VPN-000460`; VPN `SRG-NET-000525-VPN-002330` | FortiExtender CLI: `config vpn ipsec phase1-interface; edit <TUNNEL>; set ip-version 6; set ike-version 2; set remote-gw6 <PEER_IPV6>; next; end` | P21, P22 |
| IPv6 | DHCPv6 servers on physical, switch, and Wi-Fi LAN interfaces | 7.6.5 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | FortiExtender CLI: `config system dhcp6server; edit <ID>; set status disable; next; end` | — |
| IPv6 | IPv6 on Wi-Fi LAN and Wi-Fi WAN interfaces | 7.6.5 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — | — |
| SNMP | IPv6 SNMP hosts | 7.6.5 and later | NDM `SRG-APP-000395-NDM-000310` | FortiExtender CLI: `config snmp hosts; edit <HOST>; set host-ip <IPV6_PREFIX>; set host-type any; next; end` | P15, P22 |
| SNMP | SNMP OID and MIB data type updates | 7.6.5 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — | — |
| IPv6 | IPv6 redirect portal address for DNS filtering | 7.6.5 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — | — |
| Wi-Fi | IPv6 RADIUS server and source address for WPA2 and WPA3 Enterprise in Wi-Fi LAN mode | 7.6.5 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — | — |
| Wi-Fi | IPv6 captive portal servers and IPv6 security exempt lists | 7.6.5 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — | — |
| Management | SSH login lockout: ten minutes after five failed attempts | 7.6.5 and later | NDM `SRG-APP-000065-NDM-000214` | — (fixed behavior; not configurable) | — |
| Cellular WAN | LTE and 5G traffic offload to a coprocessor in local NAT mode (FER-511G and FEV-511G) | 7.6.5 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | FortiExtender CLI: `config system management; config local; set modem-offload disable; end; end` | — |
| Cellular WAN | Assisted GPS (A-GPS) on G-series models | 7.6.5 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | FortiExtender CLI: `config lte setting; config modem1; set gps disable; end; end` | — |
| Logging | OBM console log output saved to USB, FTP, SFTP, SMB, or NFS | 7.6.5 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — | — |
| Cellular WAN | CHAP authentication and APN order for multiple packet data networks (managed) | 7.6.5 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — | — |
| IPv6 | IPv6 addresses in health monitoring health checks | 8.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — | — |
| Wi-Fi | Wi-Fi password complexity enforcement (AT&T FirstNet certification) | 8.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — | — |
| Wi-Fi | 802.1X EAP-TLS certificate authentication in Wi-Fi client mode | 8.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — | — |
| Monitoring | On-demand interface speed tests | 8.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — | — |
| Management | API token expiration and encrypted API tokens | 8.0.0 and later | NDM `SRG-APP-000408-NDM-000314` | FortiExtender CLI: `execute api-user generate-key <API_USER> <EXPIRE_SECONDS>` | P23 |
| Administrator accounts | Per-administrator setting to allow or deny SSH login | 8.0.0 and later | NDM `SRG-APP-000142-NDM-000245`; NDM `SRG-APP-000408-NDM-000314` | FortiExtender CLI: `config system admin; edit <ADMIN>; set allow-ssh disable; next; end` | — |
| Management | SSH access disabled by default on FEX-511G-WiFi | 8.0.0 and later | NDM `SRG-APP-000142-NDM-000245` | — | — |
| Firmware and configuration | Digitally signed configuration backup files, validated on restore | 8.0.0 and later | NDM `SRG-APP-000516-NDM-000340`; NDM `SRG-APP-000516-NDM-000335` | — (the signature is checked automatically on restore) | — |
| LAN extension | Persistent LAN extension (LE-Always) mode (FortiOS 8.0.1 or later) | 8.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | FortiGate: `config extension-controller extender-profile; edit <PROFILE>; set lanext-always-mode disable; next; end` | — |
| LAN extension | Wi-Fi WAN interfaces as LAN extension uplink and discovery interfaces in Wi-Fi station mode (FortiOS 8.0.1 or later) | 8.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — | — |
| Networking | MAC filter based traffic control on Branch platform models | 8.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — | — |
| Authentication | LDAP authentication of administrators | 8.0.0 and later | NDM `SRG-APP-000516-NDM-000336` | FortiExtender CLI: `config user ldap; edit <LDAP>; set server <LDAP_SERVER>; set secure ldaps; set port 636; set ca-cert <CA_CERT>; set server-identity-check enable; next; end`; FortiExtender CLI: `config user group; edit <GROUP>; set ldap-member <LDAP>; next; end` | P18, P19 |
| Vehicle | GPS and GNSS data forwarding in NMEA format over UDP on FortiExtender Vehicle models | 8.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | FortiExtender CLI: `config lte setting; config modem1; set gps-reporting disable; end; end` | — |

### Requirement reference

The requirements used in the map and in this chapter's text, with their
severity in the current SRG releases:

[Download the requirement reference as CSV](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/data/volume-172-disa-srgs-and-stigs/15-fortiextender-feature-version-and-srg-map-requirements.csv) (65 rows).

| SRG | Requirement | Severity | Requirement title |
| --- | --- | --- | --- |
| NDM | `SRG-APP-000001-NDM-000200` | CAT II | The network device must limit the number of concurrent sessions to an organization-defined number for each administrator account and/or administrator account type. |
| NDM | `SRG-APP-000026-NDM-000208` | CAT II | The network device must automatically audit account creation. |
| NDM | `SRG-APP-000033-NDM-000212` | CAT I | The network device must be configured to assign appropriate user roles or access levels to authenticated users. |
| NDM | `SRG-APP-000038-NDM-000213` | CAT II | The network device must enforce approved authorizations for controlling the flow of management information within the network device based on information flow control policies. |
| NDM | `SRG-APP-000065-NDM-000214` | CAT II | The network device must be configured to enforce the limit of three consecutive invalid logon attempts, after which time it must block any login attempt for 15 minutes. |
| NDM | `SRG-APP-000068-NDM-000215` | CAT II | The network device must display the Standard Mandatory DoD Notice and Consent Banner before granting access to the device. |
| NDM | `SRG-APP-000095-NDM-000225` | CAT II | The network device must produce audit log records containing sufficient information to establish what type of event occurred. |
| NDM | `SRG-APP-000131-NDM-000243` | CAT II | The network device must prevent the installation of patches, service packs, or application components without verification the software component has been digitally signed using a certificate that is recognized and approved by the organization. |
| NDM | `SRG-APP-000142-NDM-000245` | CAT I | The network device must be configured to prohibit the use of all unnecessary and/or nonsecure functions, ports, protocols, and/or services |
| NDM | `SRG-APP-000148-NDM-000346` | CAT II | The network device must be configured with only one local account to be used as the account of last resort in the event the authentication server is unavailable. |
| NDM | `SRG-APP-000153-NDM-000249` | CAT II | The network device must be configured to authenticate each administrator prior to authorizing privileges based on assignment of group or role. |
| NDM | `SRG-APP-000164-NDM-000252` | CAT II | The network device must enforce a minimum 15-character password length. |
| NDM | `SRG-APP-000166-NDM-000254` | CAT II | The network device must enforce password complexity by requiring that at least one uppercase character be used. |
| NDM | `SRG-APP-000167-NDM-000255` | CAT II | The network device must enforce password complexity by requiring that at least one lowercase character be used. |
| NDM | `SRG-APP-000168-NDM-000256` | CAT II | The network device must enforce password complexity by requiring that at least one numeric character be used. |
| NDM | `SRG-APP-000169-NDM-000257` | CAT II | The network device must enforce password complexity by requiring that at least one special character be used. |
| NDM | `SRG-APP-000170-NDM-000329` | CAT II | The network device must require that when a password is changed, the characters are changed in at least eight of the positions within the password. |
| NDM | `SRG-APP-000171-NDM-000258` | CAT I | The network device must be configured to store passwords using an approved salted key derivation function, preferably using a keyed hash for password-based authentication. |
| NDM | `SRG-APP-000172-NDM-000259` | CAT I | The network device must transmit only encrypted representations of passwords. |
| NDM | `SRG-APP-000179-NDM-000265` | CAT I | The network device must use FIPS 140-2 approved algorithms for authentication to a cryptographic module. |
| NDM | `SRG-APP-000190-NDM-000267` | CAT I | The network device must terminate all network connections associated with a device management session at the end of the session, or the session must be terminated after five minutes of inactivity except to fulfill documented and validated mission requirements. |
| NDM | `SRG-APP-000231-NDM-000271` | CAT I | The network device must only allow authorized administrators to view or change the device configuration, system files, and other files stored either in the device or on removable media (such as a flash drive). |
| NDM | `SRG-APP-000296-NDM-000280` | CAT II | The network device must be configured to provide a logout mechanism for administrator-initiated communication sessions. |
| NDM | `SRG-APP-000357-NDM-000293` | CAT II | The network device must allocate audit record storage capacity in accordance with organization-defined audit record storage requirements. |
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
| NDM | `SRG-APP-000516-NDM-000317` | CAT II | The network device must be configured in accordance with the security configuration settings based on DoD security configuration or implementation guidance, including STIGs, NSA configuration guides, CTOs, and DTMs. |
| NDM | `SRG-APP-000516-NDM-000335` | CAT II | The network device must enforce access restrictions associated with changes to the system components. |
| NDM | `SRG-APP-000516-NDM-000336` | CAT I | The network device must be configured to use at least one authentication server for the purpose of authenticating users prior to granting administrative access. For boundary devices, two authentication servers are required. |
| NDM | `SRG-APP-000516-NDM-000340` | CAT II | The network device must be configured to conduct backups of system level information contained in the information system when changes occur. |
| NDM | `SRG-APP-000516-NDM-000344` | CAT II | The network device must obtain its public key certificates from an appropriate certificate policy through an approved service provider. |
| NDM | `SRG-APP-000516-NDM-000350` | CAT I | The network device must be configured to send log data to at least one central log server for the purpose of forwarding alerts to the administrators and the information system security officer (ISSO). For boundary devices, two log servers are required. |
| NDM | `SRG-APP-000910-NDM-000300` | CAT II | The network device must be configured to include only approved trust anchors in trust stores or certificate stores managed by the organization. |
| NDM | `SRG-APP-000920-NDM-000320` | CAT II | The network device must be configured to synchronize system clocks within and between systems or system components. |
| NDM | `SRG-APP-001035-NDM-000340` | CAT I | The network device hardware and software must be a version supported by the vendor. |
| RTR | `SRG-NET-000018-RTR-000001` | CAT II | The router must be configured to enforce approved authorizations for controlling the flow of information within the network based on organization-defined information flow control policies. |
| RTR | `SRG-NET-000019-RTR-000008` | CAT I | The perimeter router must be configured to protect an enclave connected to an alternate gateway by using an inbound filter that only permits packets with destination addresses within the site's address space. |
| RTR | `SRG-NET-000131-RTR-000083` | CAT II | The router must not be configured to have any feature enabled that calls home to the vendor. |
| RTR | `SRG-NET-000168-RTR-000078` | CAT II | The router must be configured to authenticate all routing protocol messages using NIST-validated FIPS 198-1 message authentication code algorithm. |
| RTR | `SRG-NET-000202-RTR-000001` | CAT I | The perimeter router must be configured to deny network traffic by default and allow network traffic by exception. |
| RTR | `SRG-NET-000230-RTR-000001` | CAT II | The router must be configured to implement message authentication for all control plane protocols. |
| RTR | `SRG-NET-000362-RTR-000109` | CAT II | The router must not be configured to have any zero-touch deployment feature enabled when connected to an operational network. |
| RTR | `SRG-NET-000512-RTR-000014` | CAT II | The perimeter router must be configured to suppress Router Advertisements on all external IPv6-enabled interfaces. |
| RTR | `SRG-NET-000760-RTR-000160` | CAT II | The router must establish organization-defined alternate communications paths for system operations organizational command and control. |
| VPN | `SRG-NET-000063-VPN-000220` | CAT II | The VPN Gateway must be configured to use IPsec with SHA-2 at 384 bits or greater for hashing to protect the integrity of remote access sessions. |
| VPN | `SRG-NET-000074-VPN-000250` | CAT I | The IPSec VPN must be configured to use a Diffie-Hellman (DH) Group of 16 or greater for Internet Key Exchange (IKE) Phase 1. |
| VPN | `SRG-NET-000132-VPN-000460` | CAT II | The IPsec VPN Gateway must use IKEv2 for IPsec VPN security associations. |
| VPN | `SRG-NET-000164-VPN-000560` | CAT II | The VPN Gateway, when utilizing PKI-based authentication, must validate certificates by constructing a certification path (which includes status information) to an accepted trust anchor. |
| VPN | `SRG-NET-000230-VPN-000780` | CAT I | The IPSec VPN must be configured to use FIPS-validated SHA-2 at 384 bits or higher for Internet Key Exchange (IKE). |
| VPN | `SRG-NET-000317-VPN-001090` | CAT I | The IPsec VPN Gateway must use AES encryption for the Internet Key Exchange (IKE) proposal to protect confidentiality of remote access sessions. |
| VPN | `SRG-NET-000337-VPN-001290` | CAT II | The VPN Gateway must renegotiate the IPsec security association (SA) after eight hours or less. |
| VPN | `SRG-NET-000337-VPN-001300` | CAT II | The VPN Gateway must renegotiate the IKE security association (SA) after eight hours or less. |
| VPN | `SRG-NET-000371-VPN-001640` | CAT I | The IPsec VPN Gateway must specify Perfect Forward Secrecy (PFS) during Internet Key Exchange (IKE) negotiation. |
| VPN | `SRG-NET-000371-VPN-001650` | CAT I | The VPN Gateway and Client must be configured to protect the confidentiality and integrity of transmitted information. |
| VPN | `SRG-NET-000522-VPN-002320` | CAT II | For site-to-site, VPN Gateway must be configured to store only cryptographic representations of pre-shared Keys (PSKs). |
| VPN | `SRG-NET-000525-VPN-002330` | CAT I | The IPsec VPN must use AES256 or greater encryption for the IPsec proposal to protect the confidentiality of remote access sessions. |

### Collecting evidence

For a FortiGate-managed FortiExtender, collect from the FortiGate the
`config extension-controller` sections of the configuration (units,
profiles, VAPs, and data plans), the `fortiextender` settings of
`config system global`, the firewall policies of the FortiExtender
interface, and, for LAN extension, the generated IPsec tunnel. For a
standalone FortiExtender, enter `show` in each configuration section that
the map cites (`config system admin`, `config system interface`,
`config system management`, `config system syslog`, `config system ntp`,
`config snmp user`, and `config vpn ipsec`), and run `get extender status`
and `get system admin status`. Export the GUI logs or the diagnostics package
(`execute debuginfo export tftp`), and attach the cellular connection
approval to the checklist.

## Validation and Troubleshooting

- **A feature in the map is missing on your FortiExtender.** Check the
  version column against the FortiExtender OS release, check the FortiOS
  release on the FortiGate against the compatibility matrix, and check
  whether the feature applies to your model.
- **A setting made on the FortiExtender disappears.** The FortiGate may have
  pushed its profile. Make the change in the FortiExtender profile on the
  FortiGate instead.
- **The FortiExtender will not join the FortiGate after hardening.** Check
  that the FortiGate interface allows Security Fabric (CAPWAP) access, that
  the unit is authorized (or pre-authorized when discovery lockdown is on),
  and that the static controller addresses and discovery interfaces are
  right. `get extender status` on the FortiExtender shows the management
  state.
- **Syslog messages do not arrive.** Check that the syslog server is on the
  same subnet as the FortiExtender LAN port.
- **A requirement has no matching feature.** Some requirements are met by
  procedure (connection approval, password length), by another system (the
  RADIUS or LDAP server, the central log server, the FortiGate STIGs), or not
  at all (banner, NTP authentication, SHA-384). Record how each requirement
  is met, not just which feature covers it.

## Security and Best Practices

- Keep FortiExtender OS and FortiOS on vendor-supported releases, and use
  7.6.4 or later for signed firmware.
- Set administrator passwords of at least 15 characters, remove the default
  `admin` account (7.0.2 and later), and use RADIUS or LDAPS for administrator
  login where the release supports it.
- Allow only HTTPS and SSH, only on the management-facing interface, with
  strong SSH cryptography and trusted hosts.
- Send logs to a central log server, and use SNMPv3 with authentication and
  privacy only.
- Review this map each time Fortinet publishes a FortiExtender release or
  DISA updates the NDM, Router, or VPN SRG.

## References and Knowledge Checks

**References:**

- Fortinet, *FortiExtender Release Notes*, releases 7.0.0 to 8.0.0, section
  "What's new" or "New features or enhancements" (docs.fortinet.com,
  FortiExtender documentation).
- Fortinet, *FortiExtender 8.0.0 CLI Reference*, *FortiExtender
  (Standalone) 8.0.0 Admin Guide*, *FortiExtender (Managed) 8.0.1 Admin
  Guide*, and *FortiExtender 8.0.0 Log Message Reference*.
- Fortinet, *FortiOS 8.0.1 CLI Reference* (docs.fortinet.com).
- DISA Network Device Management SRG V5R5, Router SRG V5R2, and VPN SRG
  V3R5, from the October 2026 STIG Library Compilation.
- [Chapter 03](03-the-srg-catalog-how-stigs-are-built-and-what-to-do-without-one.md)
  (SRG-based assessment),
  [Chapter 10](10-fortinet-products-stigs-and-srg-mapping.md) (Fortinet
  products),
  [Chapter 11](11-fortiswitch-feature-version-and-srg-map.md) (the
  FortiSwitch map, the same FortiGate-managed model),
  [Chapter 12](12-fortianalyzer-feature-version-and-srg-map.md) (the
  FortiAnalyzer map), and
  [Chapter 14](14-fortiap-feature-version-and-srg-map.md) (the FortiAP map
  and the Network WLAN STIGs).

**Knowledge checks:**

1. What must be approved before any of this chapter applies to a
   FortiExtender?
2. Why does this chapter add the Router and VPN SRGs to the NDM SRG that
   Chapter 10 assigns?
3. Where does the version data come from, given that FortiExtender has no
   feature matrix or New Features Guide?
4. How does the place where you configure a FortiExtender change between
   FortiGate-managed and standalone operation?
5. Which requirements can FortiExtender not meet exactly, and how do you
   handle them?
6. What applies to a feature marked "No direct requirement"?

## Summary and Completion Checklist

FortiExtender has no STIG, so it is assessed against the NDM SRG, with the
Router SRG for its routing and filtering and the VPN SRG for its IPsec
tunnels, and only after its cellular connection has been approved. This
chapter maps 154 features to the FortiExtender OS release that
introduced them, to 65 SRG requirements, and to the command that
configures them on the FortiGate or the FortiExtender: 43 core
platform features, and 111 features from the FortiExtender release
notes for 7.0.0 through 8.0.0. Operational features with no direct
requirement fall under the requirement to prohibit unnecessary functions
when unused.

- [ ] Can confirm that the cellular connection is approved.
- [ ] Can find the release that introduced a FortiExtender feature.
- [ ] Can map a FortiExtender feature to its NDM, Router, or VPN SRG
  requirement.
- [ ] Can find the FortiGate or FortiExtender command that meets the
  requirement.
- [ ] Can collect FortiExtender evidence and record the requirements
  FortiExtender cannot meet exactly.
