# Chapter 14: FortiAP Feature, Version, and SRG Map

## Learning Objectives

- Find the FortiAP firmware release that introduced a given feature.
- Map each FortiAP feature to the DISA Network WLAN STIG or NDM SRG
  requirement it helps satisfy.
- Find the command that configures each feature to meet its requirement, on
  the managing FortiGate or on the FortiAP itself.
- Use the map to scope a WLAN assessment of FortiAP, which has no
  product-specific STIG.
- Account for the controller model, in which the FortiAP configuration and
  most of the evidence live on the FortiGate.
- Confirm that wireless is permitted in the environment before any of the
  rest applies.

## Theory and Architecture

FortiAP has **no product-specific DISA STIG** (Chapter 10). Unlike the
products in Chapters 11 to 13, though, it does not fall back to SRGs alone:
DISA publishes **generic Network WLAN STIGs** that apply to any vendor's
wireless access points and controllers. Chapter 10 assigns FortiAP those
STIGs plus the **Network Device Management (NDM) SRG**. This chapter gives
three pieces of information for every FortiAP feature: **which FortiAP
release introduced it**, **which requirement it relates to**, and **which
command configures it to meet that requirement**.

**First, confirm that wireless is permitted at all.** A WLAN in a DoD
environment must be approved for that environment before any configuration
question arises. If the authorizing official or site policy does not permit
WLAN, no FortiAP may be deployed, the radios of any FortiWiFi unit must be
disabled, and the rest of this chapter does not apply. Where WLAN is
permitted, decide which WLAN STIG applies to each SSID (enclave access over
NIPRNet, or internet-only access), because the two carry different rules.

A FortiAP is a **thin access point**. In the usual deployment a FortiGate is
the wireless controller: the FortiAP discovers the FortiGate, the FortiGate
authorizes it, and the two run a CAPWAP tunnel whose control channel is always
encrypted with DTLS. The FortiAP's radio, SSID, security, and management
settings are held on the FortiGate under `config wireless-controller`
(FortiAP profiles in `wtp-profile`, SSIDs in `vap`, intrusion detection in
`wids-profile`, and global settings in `setting`, `global`, and `timers`), and
the FortiGate pushes them to the FortiAP. This is the same model as a
FortiLink-managed FortiSwitch (Chapter 11). A few settings exist only on the
FortiAP's own command line, where they are stored as configuration
variables.

### Where the version data comes from

Fortinet does not publish a feature matrix or a New Features Guide for
FortiAP. The authoritative per-release list is the **"New features or
enhancements"** section of each **FortiAP Release Notes** document. Each one
lists the features added in that FortiAP firmware release, in three tables:
new features, changes in CLI, and region/country code and DFS certification
updates. The version column was built from all 30 FortiAP release notes
Fortinet publishes for the 7.0 to 8.0 trains: FortiAP 7.0.0 through 7.0.7,
7.2.0 through 7.2.6, 7.4.0 through 7.4.7, 7.6.0 through 7.6.5, and 8.0.0.
Releases 7.0.5, 7.0.6, 7.0.7, 7.2.6, and 7.4.7 add no new features (only
bug fixes and region updates). The entries were taken from the release notes
pages on docs.fortinet.com (the PDF of each release was also downloaded for
reference).

The table has two groups of rows:

- **Core platform features** (categories starting with *Core:*) are the
  long-standing capabilities that the WLAN and NDM requirements depend on:
  FortiAP management, controller discovery and CAPWAP, administrator access
  on the controller, SSID security, 802.1X, wireless intrusion detection,
  radio power, and logging. They existed before FortiAP 7.0.0 and are not in
  any of these release notes.
- **New features** are every entry in the new-features and CLI-changes
  tables of the 30 release notes. The release notes have no categories, so
  the categories in the table were assigned for this chapter. An entry
  repeated in several trains (often a backport) is one row with several
  version entries, and the CLI-change entries that only document a new
  feature's variables are folded into that feature. The 170
  region/country-code and DFS-certification entries are folded into one
  *Regulatory* row.

| Version entry | Meaning |
| --- | --- |
| `7.0.0 or earlier` | A core feature that predates the oldest release notes used (FortiAP 7.0.0) |
| `7.4.1 and later` | Introduced in FortiAP 7.4.1 |
| `7.4.5+; 7.6.1+` | Introduced in several release trains at different patch levels (often backported); the first release in each train is shown |

Three cautions apply. First, the version is the **FortiAP firmware**
release. Many features also need a minimum **FortiOS** release on the
managing FortiGate (the release notes say so for some, for example the
randomized login password needs FortiOS 8.0.1); check the FortiAP and FortiOS
compatibility matrix. Second, a feature introduced in a patch release of an
older train may reach a newer train only in a later patch, so "and later"
means later in the same train and, usually, in later trains. Third, many
features apply only to some models (for example FIPS mode, which FAP-431F and
FAP-433F do not support, the TPM on Wi-Fi 6E models, and MLO on Wi-Fi 7
models). These release notes cover the FortiAP product line; FortiAP-U,
FortiAP-W2, and FortiWiFi have their own release notes and are not covered.

### Where the SRG data comes from

DISA ships the WLAN STIGs as one package in the October 2026 library,
`U_Network_WLAN_Y26M10_STIG.zip`. Its overview explains that each WLAN
component (access point for NIPRNet, access point for internet gateway only,
bridge, and controller) has two STIGs: one based on the NDM SRG (the
*Management* STIG, rule IDs `WLAN-ND-`) and one based on the Network SRG (the
*Platform* STIG, rule IDs `WLAN-NW-`), and that both are needed for the full
set of requirements. The SRG column uses these abbreviations:

| SRG column | STIG or SRG | Release | Applies to |
| --- | --- | --- | --- |
| **WLAN-AM** | Network WLAN AP-NIPR Management STIG | V7R3, benchmark date 30 Sep 2026 | The FortiAP's own management plane, for an AP that connects users to the enclave (NIPRNet) |
| **WLAN-AP** | Network WLAN AP-NIPR Platform STIG | V7R4, benchmark date 30 Sep 2026 | The FortiAP's wireless function: intrusion detection, SSIDs, WPA3, EAP-TLS, FIPS mode, placement, management traffic |
| **WLAN-IG** | Network WLAN AP-IG Management and Platform STIGs | V7R3 and V7R4, benchmark date 30 Sep 2026 | An SSID that gives internet access only (guest access); cited only for its rules that the AP-NIPR STIGs do not have |
| **WLAN-CM** | Network WLAN Controller Management STIG | V7R3, benchmark date 30 Sep 2026 | The FortiGate's management plane in its role as wireless controller |
| **WLAN-CP** | Network WLAN Controller Platform STIG | File name V7R4; the XCCDF says Release 3, benchmark date 27 Apr 2023 | The FortiGate's wireless controller function |
| **NDM** | Network Device Management SRG | V5R5 | NDM requirements that the WLAN Management STIGs do not repeat, such as audit off-loading and firmware integrity |

The requirement IDs are the **rule version IDs** exactly as the XCCDF gives
them. Because the four Management STIGs share the same `WLAN-ND-` rule IDs,
and the Platform STIGs the same `WLAN-NW-` IDs, the abbreviation tells you
which STIG the requirement is cited from: WLAN-AM `WLAN-ND-000200` is the
password-length rule as it applies to the FortiAP, and WLAN-CM
`WLAN-ND-000600` the authorization rule as it applies to the controller. The
requirement reference table gives the SRG ID that DISA assigns to each WLAN
rule. The WLAN Bridge STIGs are not used; if a FortiAP mesh link is used as a
point-to-point bridge (`MESH_ETH_BRIDGE`), assess that link against them.

The FortiGate that acts as the controller also has its own STIGs, the
FortiGate NDM and Firewall STIGs (Chapter 10). Its management plane is
assessed against the FortiGate NDM STIG, which covers the same NDM
requirements as the WLAN Controller Management STIG; record the WLAN-CM rules
against the FortiGate NDM checklist results. This chapter cites WLAN-CM only
where a wireless controller setting is involved.

Each feature maps to one of three kinds of relationship:

- **Implements a requirement.** The feature is how FortiAP meets a
  requirement. WIDS profiles implement the requirement for continuous
  wireless intrusion detection scanning (WLAN-AP `WLAN-NW-000100`), for
  example.
- **Must be configured to meet a requirement.** The feature is in scope of a
  requirement and has to be set up correctly. SSIDs must use WPA3 and
  EAP-TLS, for example.
- **No direct requirement.** The feature is operational, such as Bonjour
  gateways or Wi-Fi 7 Multi-Link Operation. It has no requirement of its
  own, but if it is not needed it falls under the WLAN Management STIG rule
  to prohibit unnecessary functions and services (WLAN-AM `WLAN-ND-001500`,
  which DISA bases on NDM `SRG-APP-000142-NDM-000245`).

The mapping is a starting point for an assessment, not a ruling. Confirm it
with your assessor, especially where a requirement is organization-defined or
a feature serves only some SSIDs.

### Where the commands come from

There is **no FortiAP CLI Reference**. The FortiAP's local commands (the
`cfg` configuration variables and the `cw_diag` diagnostics) are documented in
the appendix "FortiAP CLI configuration and diagnostics commands" of the
**FortiWiFi and FortiAP 8.0.1 Configuration Guide**. The controller commands
are in the **FortiOS 8.0.1 CLI Reference**, the newest FortiOS CLI Reference
Fortinet publishes. Every command in the column was checked automatically
against these two documents: each `config` path and nested table, each `set`
and `unset` option against the syntax of the path it is entered under, each
listed option value against the documented values, each `execute` command,
and each FortiAP variable and its value. Read the column this way:

- Commands that start with **FortiGate:** run on the FortiGate that manages
  the FortiAP. This is where almost all FortiAP configuration belongs: a
  setting made on the FortiAP that the controller also manages can be
  overwritten when the FortiGate pushes its configuration.
- Commands that start with **FortiAP CLI:** run on the FortiAP itself, over
  SSH or the console, or from the FortiGate's *Connect to CLI* option for a
  managed FortiAP. `cfg -a` sets a variable and `cfg -c` commits it to flash.
- Statements are separated by `;` to fit in a table cell; on the CLI, enter
  each one on its own line. Values in `<ANGLE_BRACKETS>` are placeholders for
  your own profile names, SSIDs, servers, and keys. A FortiAP profile has one
  `config radio-1` to `config radio-4` table per radio; the column shows
  `radio-1`, so repeat the setting for each radio.
- For **"No direct requirement"** rows, the command shown is the one that
  disables or limits the feature when it is unused. A dash (**—**) means
  there is nothing to change: the feature is a diagnostic, a model, a
  performance change, or a capability that is off unless configured.
- For the *Models* rows the requirement applies to model selection: choose
  models that are Wi-Fi Alliance WPA3 certified and FIPS 140 validated.

Some requirements cannot be met exactly with FortiAP settings. Record them on
the checklist as open findings with mitigations, or meet them another way:

- **Password length.** The FortiAP admin password must be at least 5
  characters (since 7.0.2), not 15 (WLAN-AM `WLAN-ND-000200`). Set a password
  of 15 or more characters from the controller with `login-passwd`, or use
  FortiAP 8.0.0 with FortiOS 8.0.1, which randomizes the password when the
  FortiGate authorizes the FortiAP.
- **Banner.** Neither document has a FortiAP login banner setting (WLAN-AM
  `WLAN-ND-000400`). Disable the console (`console-login disable`), limit
  `allowaccess` to HTTPS and SSH, and reach the FortiAP CLI through the
  FortiGate, whose own banner is shown at login.
- **Time synchronization.** Neither document has an NTP setting for the
  FortiAP (WLAN-AM `WLAN-ND-001600` and `WLAN-ND-001900`). Rely on the
  FortiGate's authenticated NTP for the wireless event log it records, and
  time-stamp the FortiAP syslog on the central log server.
- **Management ACL.** The FortiAP has no ingress and egress ACL for its own
  management traffic (WLAN-AM `WLAN-ND-001800`). Put the FortiAP units on a
  dedicated FortiGate interface and filter their subnet with FortiGate
  firewall policies, and limit `allowaccess` on the FortiAP profile.
- **Remote authentication and the account of last resort.** Remote
  administrator login (TACACS+) arrives in FortiAP 7.6.1 (WLAN-AM
  `WLAN-ND-001100` and `WLAN-ND-001300`). On older releases only the local
  `admin` account exists; record the finding.
- **Lockout.** The `ADMIN_LOCKOUT_THRESHOLD` and `ADMIN_LOCKOUT_DURATION`
  variables arrive in FortiAP 7.6.2 (WLAN-AM `WLAN-ND-001400`). The defaults
  are 3 attempts and 60 seconds; set the duration to 900 seconds for the
  required 15 minutes.
- **Privilege levels.** The FortiAP has a single administrator role (WLAN-AM
  `WLAN-ND-000700`). Separate duties on the FortiGate with the `wifi`
  permission of administrator profiles instead.
- **Idle timeout.** `ADMIN_TIMEOUT` applies to the FortiAP GUI (default 5
  minutes) and `cw_diag admin-timeout` to the shell; the configuration guide
  does not say whether the shell setting survives a reboot (WLAN-AM
  `WLAN-ND-000500`). Check it after each reboot or upgrade.
- **FIPS mode.** FortiAP FIPS mode (`FIPS_CC`) arrives in FortiAP 7.4.0, is
  enabled only on the FortiAP CLI, can be turned off only by a factory reset,
  and is not supported on FAP-431F and FAP-433F (WLAN-AP `WLAN-NW-000600`).
- **EAP-TLS.** The FortiGate passes 802.1X authentication to the RADIUS
  server, so EAP-TLS and certificate validation (WLAN-AP `WLAN-NW-000500` and
  `WLAN-NW-000700`) are enforced by the RADIUS server configuration, not by a
  FortiGate setting.

### Prerequisites

A FortiAP feature often meets its requirement only if something else is
already in place. A **prerequisite** is anything that must exist or be
configured *before* a row's command can meet the requirement: the FortiGate
that manages the FortiAP, a FortiGate interface or VLAN for the FortiAP units,
an external server (RADIUS, TACACS+, syslog or SIEM, FortiAnalyzer, SNMP
manager, EST or SCEP, FortiGuest or FortiAuthenticator, an external captive
portal), a PKI, an object on the FortiGate that the setting refers to (a WIDS
profile, a user group, VLAN interfaces, an access control list, an MPSK
profile, a mesh-backhaul SSID), an 802.1X switch port, firmware, a minimum
FortiOS release, or a model that supports the feature. Settings that the
row's own command already creates are not listed again.

The 23 prerequisites are listed once, with IDs, in *FortiAP
prerequisites*, and the feature map names the IDs each row needs in its
**FortiAP prerequisites** column. A dash means the feature needs nothing
beyond the FortiAP itself. "No direct requirement" rows, and rows whose only
requirement is to disable the feature when it is unused (WLAN-AM
`WLAN-ND-001500`), always show a dash, and so do the *Models* rows, where the
model choice is itself the requirement. Every other row whose command runs on
the FortiGate lists **P1**, the managing FortiGate, because the FortiAP gets
that setting only from its controller; so do the rows that point the FortiAP
at the FortiGate for static discovery. A FortiAP managed by FortiEdge Cloud
instead gets these settings from FortiEdge Cloud, which falls under the rule
against calling home to the vendor (WLAN-AP `WLAN-NW-001300`), so this
chapter assumes FortiGate management.

Fortinet publishes no feature matrix or licensing guide for FortiAP, and none
of the FortiAP 7.0.0 to 8.0.0 Release Notes or the FortiWiFi and FortiAP
8.0.1 Configuration Guide names a license or subscription for any feature in
the map, so no license is listed. **Model support** (P22, and P21 for
external antennas) is given only where those documents limit the feature to
some models; the minimum FortiOS release (P23) only where a release note
says the feature needs FortiOS 8.0.1. Check the "Supported models" and "New
features or enhancements" sections of the release notes for your exact model
and release, and the FortiAP and FortiOS compatibility, before you plan on a
feature.

During an assessment, check a row's prerequisites before its command: a
correctly configured setting with a missing prerequisite (a FortiAP that was
never authorized, an SSID on no radio, an unreachable RADIUS server, a model
without the feature) does not meet the requirement, and the missing
prerequisite is the finding.

## Design Considerations

- **Get WLAN approved first.** Record the approval, the SSIDs it covers, and
  which WLAN STIG (AP-NIPR or AP-IG) each SSID falls under.
- **Pick the release first, then the features.** If your design depends on a
  feature introduced in a certain release (for example TACACS+ login in
  7.6.1, administrator lockout in 7.6.2, or FIPS mode in 7.4.0), that sets
  the minimum FortiAP firmware, and both the FortiAP and the FortiGate must
  run vendor-supported releases (WLAN-AM `WLAN-ND-001000`).
- **Keep the configuration on the controller.** Put the FortiAP settings in
  FortiAP profiles and SSIDs on the FortiGate (or in FortiManager templates),
  so a replaced or reset FortiAP gets the same configuration.
- **Separate the WLAN from the enclave.** Give the FortiAP units their own
  FortiGate interface and VLAN, put each SSID behind firewall policies, keep
  guest SSIDs on a separate SSID and VLAN, and encrypt the CAPWAP data
  channel where it crosses networks you do not control.
- **Use WPA3-Enterprise with EAP-TLS.** Use pre-shared keys only for
  internet-only SSIDs, with passphrases of at least 15 characters.
- **Keep wireless intrusion detection running.** Assign a WIDS profile to
  every radio, and consider dedicated monitor radios where continuous
  scanning matters.
- **Turn off cloud services.** FortiPresence, FortiEdge Cloud discovery, and
  other features that send data to Fortinet's cloud fall under the rule
  against calling home to the vendor (WLAN-AP `WLAN-NW-001300`).

## Implementation and Automation

### FortiAP prerequisites

What must be in place before the FortiAP features in the feature map can meet
their requirements (see *Prerequisites*). The commands were verified against
the FortiOS 8.0.1 CLI Reference and the FortiAP command appendix of the
FortiWiFi and FortiAP 8.0.1 Configuration Guide with the same checks as the
feature map; GUI entries name the pane, and entries that are not FortiGate or
FortiAP settings are described in words.

[Download the prerequisites as CSV](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/data/volume-172-disa-srgs-and-stigs/14-fortiap-feature-version-and-srg-map-prerequisites.csv) (23 rows).

| ID | Prerequisite | What it enables | How to put it in place | Source |
| --- | --- | --- | --- | --- |
| P1 | A FortiGate wireless controller that manages the FortiAP: the FortiAP discovered and authorized, a FortiAP profile assigned to it, and the SSIDs added to the profile's radios, on a FortiOS release that the FortiAP release notes list as supported | Every setting made on the FortiGate (FortiAP profiles, SSIDs, WIDS profiles, and the global wireless controller settings), which the FortiGate pushes to the FortiAP; and static discovery of that controller | Authorize the FortiAP and assign its profile with `config wireless-controller wtp; edit <FORTIAP_SERIAL>; set admin enable; set wtp-profile <PROFILE>; end`, and add the SSIDs to each radio with `config wireless-controller wtp-profile; edit <PROFILE>; config radio-1; set vap-all manual; set vaps <SSID>; end; end` | FortiWiFi and FortiAP 8.0.1 Configuration Guide, "Discovering, authorizing, and deauthorizing FortiAP units", "Creating a FortiAP profile", and "Defining a wireless network interface (SSID)"; FortiAP 7.0.0 to 8.0.0 Release Notes, "Product integration support" (for example, FortiAP 8.0.0 needs FortiOS 8.0.0 and later); FortiOS 8.0.1 CLI Reference, `config wireless-controller wtp` and `config wireless-controller wtp-profile` |
| P2 | A FortiGate interface (or VLAN) dedicated to the FortiAP units, with an IP address, a DHCP server, and Security Fabric Connection access; for a FortiAP management VLAN, a FortiGate VLAN interface with that VLAN ID, tagged on the switch ports to the FortiAPs | CAPWAP discovery and control of the FortiAPs on their own segment, the controller address used for static discovery, and the FortiAP management VLAN | `config system interface; edit <AP_INTERFACE>; set ip <IP> <MASK>; set allowaccess fabric; set role lan; end` and `config system dhcp server; edit <ID>; set interface <AP_INTERFACE>; set default-gateway <IP>; set netmask <MASK>; end`; for a management VLAN, `config system interface; edit <AP_MGMT_VLAN>; set interface <AP_INTERFACE>; set vlanid <MGMT_VLAN_ID>; end` | FortiWiFi and FortiAP 8.0.1 Configuration Guide, "Configuring the network interface for the AP unit"; FortiOS 8.0.1 CLI Reference, `config system interface` and `config system dhcp server`; Chapter 14 row *Dedicated FortiGate interface for FortiAP units (CAPWAP access)* |
| P3 | A WIDS profile assigned to the radios of the FortiAP profile | Wireless intrusion detection and rogue AP scanning by the FortiAP radios, including monitor and dedicated scan radios | `config wireless-controller wtp-profile; edit <PROFILE>; config radio-1; set wids-profile <WIDS_PROFILE>; end; end` | FortiWiFi and FortiAP 8.0.1 Configuration Guide, "Wireless Intrusion Detection System"; Chapter 14 row *Wireless intrusion detection (WIDS profiles)* |
| P4 | A reachable organization RADIUS server with a unique shared secret, configured on the FortiGate (for EAP-TLS, see P5) | WPA2/WPA3-Enterprise 802.1X authentication, RADIUS MAC authentication and MPSK, dynamic VLAN assignment, NAS-Filter-Rule dynamic ACLs, RadSec, authentication survivability, and external MAC authentication portals | An organization RADIUS service, then `config user radius; edit <RADIUS_SERVER>; set server <RADIUS_IP>; set secret <SECRET>; end` | FortiWiFi and FortiAP 8.0.1 Configuration Guide, "Configuring WPA2-Enterprise SSID", "VLAN assignment by RADIUS" (step 1: configure access to the RADIUS server), "MAC-based authentication", "Configure NAS-Filter-Rule attribute to set up dACL", and "RADIUS authentication survivability for 802.1X SSIDs"; FortiOS 8.0.1 CLI Reference, `config user radius` |
| P5 | PKI: the DoD CA certificates and certificates issued from that PKI to the RADIUS server, the wireless clients, the FortiGate (WiFi and portal server certificates), and any FortiAP that authenticates its WAN port with EAP-TLS | EAP-TLS with certificate validation, RadSec server validation, a WiFi certificate and captive-portal server certificate that clients can trust, and EAP-TLS on the FortiAP WAN port | Import the certificates on the FortiGate in GUI: System > Certificates (Import > CA Certificate, and Import > Local Certificate with its key); load a FortiAP's WAN-port CA certificate, client certificate, and private key from a TFTP server with the FortiAP CLI `cw_diag -c wan1x` options (or enroll them with P7) | FortiWiFi and FortiAP 8.0.1 Configuration Guide, "Replacing WiFi certificate", "Configuring 802.1X supplicant on LAN", and the appendix "FortiAP CLI configuration and diagnostics commands" (`cw_diag -c wan1x` get-ca-cert, get-client-cert, get-private-key); Chapter 14 rows *WiFi controller certificate for 802.1X and captive portal* and *RADIUS over TLS (RadSec) for WPA2/WPA3-Enterprise authentication* |
| P6 | An upstream switch port with 802.1X port authentication (with MACsec where MACsec is used) and its authentication server, and the FortiAP's supplicant credentials | FortiAP WAN-port 802.1X supplicant, MACsec on the WAN port, and certificate enrollment over the 802.1X WAN port | Enable 802.1X (and MACsec) on the switch port the FortiAP connects to, with the FortiAP's identity on the authentication server; a switch setting, not a FortiAP one | FortiWiFi and FortiAP 8.0.1 Configuration Guide, "Configuring 802.1X supplicant on LAN" (the FortiAP authenticates when connected to a switch port with 802.1X authentication enabled); FortiAP 7.4.3 Release Notes, bug 951641 (MACsec in WAN-port 802.1X authentication; FortiAP works with confidentiality offset 0 or 30) |
| P7 | An EST or SCEP server reachable from the FortiAPs, issuing certificates from the organization PKI | Automatic CA certificate requests by FortiAPs connected over an 802.1X WAN port | An organization EST or SCEP service; the FortiAP profile then names it (`apcfg-auto-cert-est-server` or `apcfg-auto-cert-scep-url`) | FortiWiFi and FortiAP 8.0.1 Configuration Guide, "Configuring EST and SCEP servers for CA requests" (FortiAP firmware 7.6.4 or later) |
| P8 | A reachable TACACS+ server with the FortiAP administrator accounts, configured on the FortiGate | Console, SSH, and HTTPS login to the FortiAP with remote accounts | An organization TACACS+ service, then `config user tacacs+; edit <TACACS_SERVER>; set server <TACACS_IP>; set key <KEY>; end` | FortiWiFi and FortiAP 8.0.1 Configuration Guide, "Remote TACACS user access for FortiAP management"; FortiOS 8.0.1 CLI Reference, `config user tacacs+` |
| P9 | A central syslog server or SIEM reachable from the FortiAP units and the FortiGate | Off-loading the FortiAP log messages (syslog profile) and the wireless event log the FortiGate records | An organization syslog server or SIEM; the FortiAPs reach it through the syslog profile, and the FortiGate with `config log syslogd setting; set status enable; set server <SYSLOG_IP>; set mode reliable; set enc-algorithm high; end` | FortiWiFi and FortiAP 8.0.1 Configuration Guide, "Configuring a Syslog profile"; FortiOS 8.0.1 CLI Reference, `config log syslogd setting`; Chapter 14 rows *Wireless event logging on the FortiGate* and *FortiAP log messages sent to a syslog server* |
| P10 | A FortiAnalyzer that accepts the logs, reachable from the FortiAP units | Local-bridging UTM logs sent in syslog format to the FortiAnalyzer | An organization FortiAnalyzer (Chapter 12) | FortiAP 7.4.5 and 7.6.1 Release Notes, bug 0471150 (Wi-Fi 6E models only: local-bridging UTM logs sent in syslog format to the FortiAnalyzer as configured by the FortiGate) |
| P11 | Lightweight UTM on the bridge-mode SSID: a UTM-capable FortiAP and a UTM profile on the SSID | UTM logs from local-bridging SSIDs | `config wireless-controller vap; edit <SSID>; set utm-status enable; set utm-profile <UTM_PROFILE>; end` | FortiWiFi and FortiAP 8.0.1 Configuration Guide, "Enforcing UTM policies on a local bridge SSID" (not all FortiAPs are UTM capable); FortiAP 7.4.3 Release Notes, bug 951643 (Wi-Fi 6E models); FortiAP 7.6.4 Release Notes, bug 1210169 (FAP-23JK, 241K, 243K, 244K, 441K, and 443K) |
| P12 | An SNMPv3 manager with the FortiAP MIB and Fortinet Core MIB, configured with the same user, authentication, and privacy settings, and SNMP allowed in the FortiAP profile | SNMPv3 queries and notifications for managed FortiAP units | The organization network management system, then `config wireless-controller snmp; config user; edit <SNMP_USER>; set notify-hosts <NMS_IP>; set queries enable; end; end` and `config wireless-controller wtp-profile; edit <PROFILE>; set allowaccess https ssh snmp; end` | FortiWiFi and FortiAP 8.0.1 Configuration Guide, "Monitoring FortiAP with SNMP" (SNMP access in FortiAP profiles; the SNMP manager requires the FortiAP MIB and Fortinet Core MIB; local standalone mode does not support FortiAP direct SNMP) |
| P13 | Fortinet FortiAP firmware for the model, on a supported upgrade path, from FortiGuard or from the Fortinet Support website with its checksum checked | FortiAP firmware upgrades from the controller | Automatic provisioning downloads the latest compatible firmware from FortiGuard; for a manual upgrade, download the image from the Fortinet Support website and check it at Support > Firmware Image Checksum | FortiWiFi and FortiAP 8.0.1 Configuration Guide, "FortiAP unit firmware upgrade"; FortiAP Release Notes, "Upgrade and downgrade information" (for example, FortiAP 8.0.0 supports upgrading from 7.6.3 and later) and "Firmware image checksums" |
| P14 | An external captive portal server (for example Cisco ISE) that serves the portal over HTTPS | External and external-macauth captive portals, and client logout on external captive-portal SSIDs | An organization portal server; the SSID names it with `config wireless-controller vap; edit <SSID>; set external-web <PORTAL_URL>; end` | FortiWiFi and FortiAP 8.0.1 Configuration Guide, "Configuring an external captive portal" (including "To configure an external-macauth portal in bridge mode - CLI") |
| P15 | A firewall user group with the portal or MAC-authentication users (local, RADIUS, or guest users) | Captive-portal authentication and RADIUS MAC authentication groups on the SSID | `config user group; edit <GROUP>; set member <USERS>; end`, then `config wireless-controller vap; edit <SSID>; set selected-usergroups <GROUP>; end` (for MAC authentication, `set radius-mac-auth-usergroups <GROUP>`) | FortiWiFi and FortiAP 8.0.1 Configuration Guide, "Configuring a FortiGate captive portal" (create a user group) and "Configuring an external captive portal"; FortiOS 8.0.1 CLI Reference, `config user group` |
| P16 | The VLAN interfaces that dynamic assignment uses, with their DHCP servers and firewall policies, and for bridge-mode SSIDs the VLANs carried on the switch ports to the FortiAPs | Dynamic VLAN assignment by RADIUS attribute, by name tag, and by VLAN pool | `config system interface; edit <VLAN_INTERFACE>; set interface <SSID>; set vlanid <VLAN_ID>; end`, with a DHCP server and a firewall policy for each VLAN interface | FortiWiFi and FortiAP 8.0.1 Configuration Guide, "VLAN assignment by RADIUS" (create the VLAN interfaces and their DHCP servers, and security policies), "VLAN assignment by Name Tag", and "VLAN assignment by VLAN pool" |
| P17 | A wireless layer-3 access control list with its rules | Layer-3 access control lists on the SSID, including domain-name (FQDN or wildcard) rules | `config wireless-controller access-control-list; edit <ACL>; config layer3-ipv4-rules; edit 1; set dstaddr <ADDRESS>; set action deny; end; end` | FortiOS 8.0.1 CLI Reference, `config wireless-controller access-control-list`; FortiAP 8.0.0 Release Notes, bug 1196413 |
| P18 | An MPSK profile with its groups and keys | MPSK profiles on local-standalone WPA3-SAE SSIDs | `config wireless-controller mpsk-profile; edit <MPSK_PROFILE>; config mpsk-group; edit <GROUP>; config mpsk-key; edit <KEY_NAME>; set passphrase <PASSPHRASE_15_CHARS_MIN>; end; end; end` | FortiWiFi and FortiAP 8.0.1 Configuration Guide, "MPSK profiles"; FortiOS 8.0.1 CLI Reference, `config wireless-controller mpsk-profile` |
| P19 | A FortiGuest or FortiAuthenticator server for user MPSK management, configured on the FortiGate as a RADIUS server | User MPSK self-registration and management through FortiGuest or FortiAuthenticator | An organization FortiGuest or FortiAuthenticator, then `config user radius; edit <MPSK_SERVER>; set server <SERVER_IP>; set secret <SECRET>; end` | FortiWiFi and FortiAP 8.0.1 Configuration Guide, "User self-registration of MPSKs through FortiGuest" (configure the external FortiGuest RADIUS server); FortiAP 7.4.3 Release Notes, bug 1001339 |
| P20 | A mesh-backhaul SSID with WPA3-SAE security on the FortiGate, assigned to the mesh-root FortiAP | WPA3-SAE security over the mesh backhaul | `config wireless-controller vap; edit <MESH_SSID>; set mesh-backhaul enable; set security wpa3-sae; end`, then add it to the mesh-root FortiAP's profile | FortiAP 7.4.0 Release Notes, "Support WPA3-SAE security over the mesh backhaul" (on the FortiGate, add one mesh-backhaul VAP with security wpa3-sae and assign it to the mesh-root FortiAP); FortiWiFi and FortiAP 8.0.1 Configuration Guide, "Manually configuring a meshed WiFi network" |
| P21 | An external antenna installed on a FortiAP model that supports external antennas (Fortinet antennas on FAP-432F and FAP-433F; third-party antennas on select models) | Transmit power that accounts for the external antenna's gain | Install the antenna, and select the profile platform that supports it; a hardware choice, not a setting | FortiWiFi and FortiAP 8.0.1 Configuration Guide, "Configure Fortinet external antenna parameters" and "Configure third-party antennas"; FortiAP 7.2.3 and 7.4.0 Release Notes, bug 868839 (FAP-432F and 433F, when the external antenna is installed) |
| P22 | A FortiAP model that supports the feature, as the release notes state | Console port control (applicable models), FIPS mode (not FAP-431F or FAP-433F), the TPM (Wi-Fi 6E models), WAN-port MACsec (Wi-Fi 6E models; Wi-Fi 7 models from 7.6.2), UTM logs to FortiAnalyzer (Wi-Fi 6E models), and WPA3 beacon protection (Wi-Fi 6E and Wi-Fi 7 models) | Choose the model from the feature's entry in the FortiAP Release Notes ("New features or enhancements", and "Supported models" for the release you run) | FortiAP 7.0.1 Release Notes, bug 719445 (console port on applicable FAP models); FortiAP 7.4.0, bug 268728 (FAP-431F and FAP-433F cannot support FIPS mode); FortiAP 7.4.1, bug 903097 (Wi-Fi 6E models only: TPM); FortiAP 7.4.3, bug 951641, and 7.6.2, bug 1000375 (MACsec); FortiAP 7.4.5, bug 0471150 (Wi-Fi 6E models only: UTM logs); FortiWiFi and FortiAP 8.0.1 Configuration Guide, "Enabling Beacon Protection" (Wi-Fi 6E and Wi-Fi 7 models running FAP 7.6.1 and later) |
| P23 | FortiOS 8.0.1 on the managing FortiGate | The randomized FortiAP login password on authorization, and WPA3 transition-mode SSIDs with different behavior per radio band | Upgrade the FortiGate to FortiOS 8.0.1 or later | FortiAP 8.0.0 Release Notes, bugs 1084647 and 1294804 (this feature is only supported on FortiOS 8.0.1) |

### The FortiAP feature map

The SRG column uses the abbreviations defined in *Where the SRG data comes
from*. The requirement titles are listed in the next table. The command
column follows the conventions in *Where the commands come from*.
The last column lists the IDs from *FortiAP prerequisites*.

[Download the feature map as CSV](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/data/volume-172-disa-srgs-and-stigs/14-fortiap-feature-version-and-srg-map-feature-map.csv) (186 rows).

| Category | Feature | Introduced (FortiAP) | SRG requirement(s) | Command to satisfy the requirement | FortiAP prerequisites |
| --- | --- | --- | --- | --- | --- |
| Core: FortiAP management | FortiAP administrator password set from the controller | 7.0.0 or earlier | WLAN-AM `WLAN-ND-000200`; WLAN-AM `WLAN-ND-000300`; WLAN-AM `WLAN-ND-001300`; NDM `SRG-APP-000171-NDM-000258` | FortiGate: `config wireless-controller wtp-profile; edit <PROFILE>; set login-passwd-change yes; set login-passwd <PASSWORD_15_CHARS_MIN>; end` | P1 |
| Core: FortiAP management | FortiAP management access protocols (HTTPS, SSH, SNMP) set from the controller | 7.0.0 or earlier | WLAN-AM `WLAN-ND-001500`; WLAN-AM `WLAN-ND-000800`; NDM `SRG-APP-000408-NDM-000314` | FortiGate: `config wireless-controller wtp-profile; edit <PROFILE>; set allowaccess https ssh; end` | P1 |
| Core: FortiAP management | FortiAP local management access control (ALLOW_HTTPS, ALLOW_SSH) | 7.0.0 or earlier | WLAN-AM `WLAN-ND-001500`; WLAN-AM `WLAN-ND-000800` | FortiAP CLI: `cfg -a ALLOW_HTTPS=2; cfg -a ALLOW_SSH=2; cfg -c` | — |
| Core: FortiAP management | FortiAP local administrative idle timeout | 7.0.0 or earlier | WLAN-AM `WLAN-ND-000500` | FortiAP CLI: `cfg -a ADMIN_TIMEOUT=10; cfg -c`, then FortiAP CLI: `cw_diag admin-timeout <MINUTES_10_OR_LESS>` | — |
| Core: FortiAP management | FortiAP management VLAN | 7.0.0 or earlier | WLAN-AP `WLAN-NW-001200`; WLAN-CP `WLAN-NW-001200`; NDM `SRG-APP-000880-NDM-000290` | FortiAP CLI: `cfg -a AP_MGMT_VLAN_ID=<MGMT_VLAN_ID>; cfg -c` | P2 |
| Core: FortiAP management | FortiAP local configuration export | 7.0.0 or earlier | NDM `SRG-APP-000516-NDM-000340` | FortiAP CLI: `cfg -e` | — |
| Core: FortiAP management | FortiAP firmware upgrade from the controller | 7.0.0 or earlier | WLAN-AM `WLAN-ND-001000`; WLAN-CM `WLAN-ND-001000`; NDM `SRG-APP-001035-NDM-000340`; NDM `SRG-APP-000457-NDM-000352` | FortiGate: `config wireless-controller setting; set firmware-provision-on-authorization enable; end`, then FortiGate: `execute wireless-controller list-wtp-image` | P1, P13 |
| Core: Controller connectivity (CAPWAP) | Static WiFi controller discovery | 7.0.0 or earlier | WLAN-AP `WLAN-NW-001300`; NDM `SRG-APP-000516-NDM-000335` | FortiAP CLI: `cfg -a AC_DISCOVERY_TYPE=1; cfg -a AC_IPADDR_1=<FORTIGATE_IP>; cfg -c` | P1, P2 |
| Core: Controller connectivity (CAPWAP) | FortiAP discovery and authorization on the FortiGate | 7.0.0 or earlier | NDM `SRG-APP-000516-NDM-000335`; WLAN-CM `WLAN-ND-001500` | FortiGate: `config system interface; edit <AP_INTERFACE>; set ap-discover disable; set auto-auth-extension-device disable; end`, then FortiGate: `config wireless-controller wtp; edit <FORTIAP_SERIAL>; set admin enable; end` | P1, P2 |
| Core: Controller connectivity (CAPWAP) | Dedicated FortiGate interface for FortiAP units (CAPWAP access) | 7.0.0 or earlier | WLAN-AP `WLAN-NW-001100`; WLAN-AP `WLAN-NW-001200`; WLAN-CP `WLAN-NW-001200` | FortiGate: `config system interface; edit <AP_INTERFACE>; set allowaccess fabric; end` | P1 |
| Core: Controller connectivity (CAPWAP) | CAPWAP control channel encryption (always DTLS) | 7.0.0 or earlier | WLAN-AM `WLAN-ND-000800`; WLAN-CM `WLAN-ND-000800`; NDM `SRG-APP-000411-NDM-000330` | FortiGate: `config wireless-controller global; set tunnel-mode strict; end` | P1 |
| Core: Controller connectivity (CAPWAP) | CAPWAP data channel encryption (DTLS or IPsec VPN) | 7.0.0 or earlier | WLAN-AP `WLAN-NW-000600`; WLAN-CP `WLAN-NW-000600` | FortiGate: `config wireless-controller wtp-profile; edit <PROFILE>; set dtls-policy dtls-enabled; end` | P1 |
| Core: Controller administration | Administrator access to the WiFi controller (wifi permission in the administrator profile) | 7.0.0 or earlier | WLAN-CM `WLAN-ND-000700`; WLAN-CM `WLAN-ND-000600`; NDM `SRG-APP-000380-NDM-000304` | FortiGate: `config system accprofile; edit <PROFILE>; set wifi read; end` | P1 |
| Core: Controller administration | FIPS-CC mode on the FortiGate wireless controller | 7.0.0 or earlier | WLAN-CP `WLAN-NW-000600`; NDM `SRG-APP-000179-NDM-000265` | FortiGate: `config system fips-cc; set status enable; end` | P1 |
| Core: SSIDs and client access | SSID (virtual access point) security mode (WPA2/WPA3, PMF) | 7.0.0 or earlier | WLAN-AP `WLAN-NW-000400`; WLAN-IG `WLAN-NW-000900`; WLAN-AP `WLAN-NW-000500` | FortiGate: `config wireless-controller vap; edit <SSID>; set security wpa3-only-enterprise; set pmf enable; end` | P1, P4 |
| Core: SSIDs and client access | 802.1X (WPA-Enterprise) authentication with a RADIUS server | 7.0.0 or earlier | WLAN-AP `WLAN-NW-000500`; WLAN-AP `WLAN-NW-000700`; WLAN-CP `WLAN-NW-000500`; WLAN-CP `WLAN-NW-000700` | FortiGate: `config wireless-controller vap; edit <SSID>; set auth radius; set radius-server <RADIUS_SERVER>; end` (EAP-TLS and certificate validation are configured on the RADIUS server) | P1, P4, P5 |
| Core: SSIDs and client access | WiFi controller certificate for 802.1X and captive portal | 7.0.0 or earlier | WLAN-AP `WLAN-NW-000700`; NDM `SRG-APP-000516-NDM-000344` | FortiGate: `config system global; set wifi-certificate <CERT>; set wifi-ca-certificate <CA_CERT>; end` | P1, P5 |
| Core: SSIDs and client access | Pre-shared key SSIDs (WPA2-Personal, WPA3-SAE) | 7.0.0 or earlier | WLAN-IG `WLAN-ND-000100` | FortiGate: `config wireless-controller vap; edit <SSID>; set security wpa3-sae; set sae-password <PASSPHRASE_15_CHARS_MIN>; end` | P1 |
| Core: SSIDs and client access | SSID name and broadcast | 7.0.0 or earlier | WLAN-AP `WLAN-NW-000200` | FortiGate: `config wireless-controller vap; edit <SSID>; set ssid <NON_IDENTIFYING_SSID>; end` | P1 |
| Core: SSIDs and client access | Captive portal and guest SSIDs | 7.0.0 or earlier | WLAN-IG `WLAN-NW-001000` | FortiGate: `config wireless-controller vap; edit <SSID>; set captive-portal enable; set portal-type auth; end` | P1, P15 |
| Core: SSIDs and client access | Wireless client idle timeout | 7.0.0 or earlier | WLAN-AP `WLAN-NW-000300`; WLAN-CP `WLAN-NW-000300` | FortiGate: `config wireless-controller timers; set client-idle-timeout 1800; end` | P1 |
| Core: SSIDs and client access | Firewall policies between SSIDs and other networks | 7.0.0 or earlier | WLAN-AP `WLAN-NW-001100`; WLAN-IG `WLAN-NW-001000` | FortiGate: `config firewall policy; edit <ID>; set srcintf <SSID_INTERFACE>; set dstintf <DEST_INTERFACE>; set action accept; set logtraffic all; end` | P1 |
| Core: SSIDs and client access | Bridge-mode (local-bridging) SSIDs | 7.0.0 or earlier | No direct requirement; if unused, disable (WLAN-AM `WLAN-ND-001500`) | FortiGate: `config wireless-controller vap; edit <SSID>; set local-bridging disable; end` | — |
| Core: SSIDs and client access | Local-standalone SSIDs | 7.0.0 or earlier | No direct requirement; if unused, disable (WLAN-AM `WLAN-ND-001500`) | FortiGate: `config wireless-controller vap; edit <SSID>; set local-standalone disable; end` | — |
| Core: SSIDs and client access | Split tunneling | 7.0.0 or earlier | No direct requirement; if unused, disable (WLAN-AM `WLAN-ND-001500`) | FortiGate: `config wireless-controller vap; edit <SSID>; set split-tunneling disable; end` | — |
| Core: SSIDs and client access | Hotspot 2.0 (Passpoint) | 7.0.0 or earlier | No direct requirement; if unused, disable (WLAN-AM `WLAN-ND-001500`) | FortiGate: `config wireless-controller vap; edit <SSID>; unset hotspot20-profile; end` | — |
| Core: SSIDs and client access | MAC address filtering | 7.0.0 or earlier | No direct requirement; if unused, disable (WLAN-AM `WLAN-ND-001500`) | — | — |
| Core: Wireless intrusion detection | Wireless intrusion detection (WIDS profiles) | 7.0.0 or earlier | WLAN-AP `WLAN-NW-000100` | FortiGate: `config wireless-controller wids-profile; edit <WIDS_PROFILE>; set sensor-mode both; set ap-scan enable; set deauth-broadcast enable; set eapol-start-flood enable; end`, then FortiGate: `config wireless-controller wtp-profile; edit <PROFILE>; config radio-1; set wids-profile <WIDS_PROFILE>; end; end` | P1 |
| Core: Wireless intrusion detection | Rogue AP detection | 7.0.0 or earlier | WLAN-AP `WLAN-NW-000100` | FortiGate: `config wireless-controller wids-profile; edit <WIDS_PROFILE>; set ap-scan enable; end`, then FortiGate: `config wireless-controller setting; set fake-ssid-action log; end` | P1, P3 |
| Core: Wireless intrusion detection | Dedicated monitor radio | 7.0.0 or earlier | WLAN-AP `WLAN-NW-000100` | FortiGate: `config wireless-controller wtp-profile; edit <PROFILE>; config radio-1; set mode monitor; end; end` | P1, P3 |
| Core: Radio and RF | Transmit power control | 7.0.0 or earlier | WLAN-AP `WLAN-NW-000800` | FortiGate: `config wireless-controller wtp-profile; edit <PROFILE>; config radio-1; set power-mode dBm; set power-value <DBM>; end; end` | P1 |
| Core: Radio and RF | Automatic radio resource provisioning (DARRP) | 7.0.0 or earlier | No direct requirement; if unused, disable (WLAN-AM `WLAN-ND-001500`) | — | — |
| Core: Radio and RF | Wireless mesh | 7.0.0 or earlier | No direct requirement; if unused, disable (WLAN-AM `WLAN-ND-001500`) | FortiAP CLI: `cfg -a MESH_AP_TYPE=0; cfg -c` | — |
| Core: Radio and RF | Spectrum analysis and sniffer mode | 7.0.0 or earlier | No direct requirement; if unused, disable (WLAN-AM `WLAN-ND-001500`) | — | — |
| Core: Logging and monitoring | Wireless event logging on the FortiGate | 7.0.0 or earlier | NDM `SRG-APP-000516-NDM-000350`; NDM `SRG-APP-000515-NDM-000325`; WLAN-AM `WLAN-ND-000900` | FortiGate: `config wireless-controller log; set status enable; set wids-log notification; set wtp-event-log notification; end` | P1, P9 |
| Core: Logging and monitoring | SNMP for managed FortiAP units | 7.0.0 or earlier | WLAN-AM `WLAN-ND-001200` | FortiGate: `config wireless-controller snmp; config user; edit <SNMP_USER>; set security-level auth-priv; set auth-proto sha256; set priv-proto aes256; end; end` | P1, P12 |
| Core: Logging and monitoring | LLDP on FortiAP units | 7.0.0 or earlier | No direct requirement; if unused, disable (WLAN-AM `WLAN-ND-001500`) | FortiGate: `config wireless-controller wtp-profile; edit <PROFILE>; set lldp disable; end` | — |
| Core: Logging and monitoring | Bluetooth Low Energy (BLE) profiles | 7.0.0 or earlier | No direct requirement; if unused, disable (WLAN-AM `WLAN-ND-001500`) | FortiGate: `config wireless-controller wtp-profile; edit <PROFILE>; unset ble-profile; end` | — |
| Core: Logging and monitoring | FortiPresence location analytics | 7.0.0 or earlier | WLAN-AP `WLAN-NW-001300`; WLAN-CP `WLAN-NW-001300` | FortiGate: `config wireless-controller wtp-profile; edit <PROFILE>; config lbs; set fortipresence disable; end; end` | P1 |
| Wired ports | FAP-23JF LAN ports: MAC address authentication, RADIUS accounting, and dynamic VLAN assignment | 7.0.0 and later | No direct requirement; if unused, disable (WLAN-AM `WLAN-ND-001500`) | FortiGate: `config wireless-controller wtp-profile; edit <PROFILE>; config lan; set port-mode offline; end; end` | — |
| Roaming and client services | Voice-enterprise SSID enhancements: 802.11k dual-band neighbor report and 802.11v BSS transition management | 7.0.0 and later | No direct requirement; if unused, disable (WLAN-AM `WLAN-ND-001500`) | FortiGate: `config wireless-controller vap; edit <SSID>; set 80211k disable; set 80211v disable; end` | — |
| SSIDs and authentication | DHCP address enforcement (clients must complete DHCP or are disconnected) | 7.0.0 and later | WLAN-AP `WLAN-NW-001100` | FortiGate: `config wireless-controller vap; edit <SSID>; set dhcp-address-enforcement enable; end` | P1 |
| Monitoring and diagnostics | Service assurance management (SAM) radio mode: ping and iPerf tests against another AP | 7.0.0 and later | No direct requirement; if unused, disable (WLAN-AM `WLAN-ND-001500`) | — (SAM is a radio mode used only when selected) | — |
| SSIDs and authentication | MAC address delimiter options for RADIUS MAC authentication and accounting | 7.0.0 and later | No direct requirement; if unused, disable (WLAN-AM `WLAN-ND-001500`) | — | — |
| SSIDs and authentication | Bridge-mode captive portal "external-macauth" portal type for external Cisco ISE authentication | 7.0.0 and later | WLAN-IG `WLAN-NW-001000` | FortiGate: `config wireless-controller vap; edit <SSID>; set captive-portal enable; set portal-type external-macauth; end` | P1, P4, P14, P15 |
| Regulatory | Region and country code updates and DFS channel certification | 7.0.0+; 7.2.0+; 7.4.0+; 7.6.0+; 8.0.0+ | No direct requirement; if unused, disable (WLAN-AM `WLAN-ND-001500`) | — | — |
| SSIDs and authentication | Client logout URL and REST API on bridge-mode external captive-portal SSIDs | 7.0.1 and later | WLAN-IG `WLAN-NW-001000` | — | P1, P14 |
| Monitoring and diagnostics | AP operating temperature reported to the FortiGate WiFi controller | 7.0.1 and later | No direct requirement; if unused, disable (WLAN-AM `WLAN-ND-001500`) | — | — |
| Location and IoT | SES-imagotag USB dongle for Electronic Shelf Labels (ESL) | 7.0.1 and later | No direct requirement; if unused, disable (WLAN-AM `WLAN-ND-001500`) | FortiGate: `config wireless-controller wtp-profile; edit <PROFILE>; set usb-port disable; end` | — |
| SSIDs and authentication | Dynamic VLAN assignment from a text Tunnel-Private-Group-Id that matches a VAP sub-VLAN interface name | 7.0.1 and later | WLAN-AP `WLAN-NW-001100` | FortiGate: `config wireless-controller vap; edit <SSID>; set dynamic-vlan enable; end` | P1, P4, P16 |
| SSIDs and authentication | Optional DNS servers for local-standalone NAT-mode SSIDs | 7.0.1 and later | No direct requirement; if unused, disable (WLAN-AM `WLAN-ND-001500`) | FortiGate: `config wireless-controller vap; edit <SSID>; set local-standalone disable; end` | — |
| Controller connectivity | "SKIP CAPWAP Offload" flag for FortiGate models with NP7 acceleration | 7.0.1 and later | No direct requirement; if unused, disable (WLAN-AM `WLAN-ND-001500`) | — | — |
| Models | New model FAP-831F | 7.0.1 and later | WLAN-AP `WLAN-NW-000400`; WLAN-AP `WLAN-NW-000600` | — (model selection; check certification) | — |
| Management | Console port enabled or disabled from the FortiGate (console-login) | 7.0.1 and later | WLAN-AM `WLAN-ND-001500`; NDM `SRG-APP-000408-NDM-000314` | FortiGate: `config wireless-controller wtp-profile; edit <PROFILE>; set console-login disable; end` | P1, P22 |
| Controller connectivity | Hitless failover in an active-passive FortiGate HA cluster | 7.0.1 and later | No direct requirement; if unused, disable (WLAN-AM `WLAN-ND-001500`) | — | — |
| Monitoring and diagnostics | Captive-portal authentication in service assurance management (SAM) mode | 7.0.1 and later | No direct requirement; if unused, disable (WLAN-AM `WLAN-ND-001500`) | — | — |
| Radio and RF | Site survey SSID: separate transmit power for 2.4 GHz and 5 GHz (SURVEY_TX_POWER_24, SURVEY_TX_POWER_50) | 7.0.1 and later | WLAN-AP `WLAN-NW-000800` | FortiAP CLI: `cfg -a AP_MODE=0; cfg -c` | — |
| Location and IoT | Hexadecimal Eddystone namespace and instance IDs in BLE profiles | 7.0.2 and later | No direct requirement; if unused, disable (WLAN-AM `WLAN-ND-001500`) | FortiGate: `config wireless-controller wtp-profile; edit <PROFILE>; unset ble-profile; end` | — |
| Management | FortiAP admin password up to 128 characters (LOGIN_PASSWD and login-passwd) | 7.0.2 and later | WLAN-AM `WLAN-ND-000200` | FortiGate: `config wireless-controller wtp-profile; edit <PROFILE>; set login-passwd-change yes; set login-passwd <PASSWORD_15_CHARS_MIN>; end` | P1 |
| SSIDs and authentication | Hotspot 2.0 Release 3 | 7.0.2 and later | No direct requirement; if unused, disable (WLAN-AM `WLAN-ND-001500`) | FortiGate: `config wireless-controller vap; edit <SSID>; unset hotspot20-profile; end` | — |
| Location and IoT | FortiPresence push API: AP region map information | 7.0.2 and later | WLAN-AP `WLAN-NW-001300`; WLAN-CP `WLAN-NW-001300` | FortiGate: `config wireless-controller wtp-profile; edit <PROFILE>; config lbs; set fortipresence disable; end; end` | P1 |
| Management | FortiAP log messages sent to a syslog server | 7.0.2 and later | NDM `SRG-APP-000516-NDM-000350`; NDM `SRG-APP-000515-NDM-000325`; WLAN-AM `WLAN-ND-000900` | FortiGate: `config wireless-controller syslog-profile; edit <SYSLOG_PROFILE>; set server-status enable; set server <SYSLOG_SERVER>; set log-level information; end`, then FortiGate: `config wireless-controller wtp-profile; edit <PROFILE>; set syslog-profile <SYSLOG_PROFILE>; end` | P1, P9 |
| Roaming and client services | AP name, model, or serial number advertised in beacon frames | 7.0.2 and later | WLAN-AP `WLAN-NW-000200` | FortiGate: `config wireless-controller vap; edit <SSID>; unset beacon-advertising; end` | P1 |
| SSIDs and authentication | Multiple pre-shared key (MPSK) authentication with RADIUS MAC authentication | 7.0.2 and later | WLAN-IG `WLAN-ND-000100` | FortiGate: `config wireless-controller vap; edit <SSID>; set radius-mac-auth enable; set radius-mac-mpsk-auth enable; end` | P1, P4 |
| Management | FortiAP admin password requires at least 5 characters and cannot be blank | 7.0.2 and later | WLAN-AM `WLAN-ND-000200`; WLAN-AM `WLAN-ND-000300` | FortiGate: `config wireless-controller wtp-profile; edit <PROFILE>; set login-passwd-change yes; set login-passwd <PASSWORD_15_CHARS_MIN>; end` | P1 |
| Security | FortiAP WAN port 802.1X supplicant (EAP methods, user ID, and password; set from the FortiGate or the FortiAP CLI) | 7.0.2 and later | WLAN-AP `WLAN-NW-001100`; WLAN-AP `WLAN-NW-000700` | FortiGate: `config wireless-controller wtp-profile; edit <PROFILE>; set wan-port-auth 802.1x; set wan-port-auth-methods EAP-TLS; end` | P1, P5, P6 |
| Wireless intrusion detection | More rogue AP information (SGI, bandwidth, maximum rate, PHY mode) reported to the controller | 7.0.2 and later | WLAN-AP `WLAN-NW-000100` | FortiGate: `config wireless-controller wids-profile; edit <WIDS_PROFILE>; set ap-scan enable; end` | P1, P3 |
| Location and IoT | FQDN address mode for the FortiPresence server | 7.0.2 and later | WLAN-AP `WLAN-NW-001300`; WLAN-CP `WLAN-NW-001300` | FortiGate: `config wireless-controller wtp-profile; edit <PROFILE>; config lbs; set fortipresence disable; end; end` | P1 |
| Security | Stronger encryption of stored passwords (LOGIN_PASSWD, AC_DISCOVERY_FCLD_PASSWD, MESH_AP_PASSWD, WAN_1X_PASSWD) | 7.0.2 and later | NDM `SRG-APP-000171-NDM-000258` | — | — |
| Management | Firmware restore command: TFTP or FTP server type | 7.0.2 and later | WLAN-AM `WLAN-ND-001000`; NDM `SRG-APP-000457-NDM-000352` | — (FortiAP CLI restore command; not documented in the 8.0.1 configuration guide appendix) | — |
| Monitoring and diagnostics | Upload Target Assert logs to a TFTP server (cw_diag wlanfw-dump) | 7.0.2 and later | No direct requirement; if unused, disable (WLAN-AM `WLAN-ND-001500`) | — | — |
| SSIDs and authentication | Dynamic VLAN assignment by name tag (vlan-name table per SSID) | 7.0.3 and later | WLAN-AP `WLAN-NW-001100` | FortiGate: `config wireless-controller vap; edit <SSID>; set dynamic-vlan enable; end` | P1, P4, P16 |
| Radio and RF | Automatic BSS coloring | 7.0.3 and later | No direct requirement; if unused, disable (WLAN-AM `WLAN-ND-001500`) | — | — |
| Radio and RF | Custom 802.11ax MCS data rates per SSID | 7.0.3 and later | No direct requirement; if unused, disable (WLAN-AM `WLAN-ND-001500`) | — | — |
| Roaming and client services | 802.11r roaming on local-standalone SSIDs | 7.0.3 and later | No direct requirement; if unused, disable (WLAN-AM `WLAN-ND-001500`) | FortiGate: `config wireless-controller vap; edit <SSID>; set fast-bss-transition disable; end` | — |
| Security | WAN port 802.1X supplicant settings in the FortiAP web UI | 7.0.3 and later | WLAN-AP `WLAN-NW-001100`; WLAN-AP `WLAN-NW-000700` | FortiGate: `config wireless-controller wtp-profile; edit <PROFILE>; set wan-port-auth 802.1x; set wan-port-auth-methods EAP-TLS; end` | P1, P5, P6 |
| Monitoring and diagnostics | fap-tech consolidated debug command | 7.0.3 and later | No direct requirement; if unused, disable (WLAN-AM `WLAN-ND-001500`) | — | — |
| Roaming and client services | Broadcast and multicast suppression on the FortiAP | 7.0.4+; 7.2.0+ | NDM `SRG-APP-000435-NDM-000315` | FortiGate: `config wireless-controller vap; edit <SSID>; set broadcast-suppression dhcp-up arp-known; end` | P1 |
| Monitoring and diagnostics | nDPI-based client application analyzer (bridge-mode SSIDs) | 7.2.0 and later | No direct requirement; if unused, disable (WLAN-AM `WLAN-ND-001500`) | FortiGate: `config wireless-controller vap; edit <SSID>; set application-detection-engine disable; end` | — |
| SSIDs and authentication | MAC address filter by firewall address group | 7.2.0 and later | No direct requirement; if unused, disable (WLAN-AM `WLAN-ND-001500`) | — | — |
| Roaming and client services | Layer-3 roaming over tunnel-mode SSIDs | 7.2.0 and later | No direct requirement; if unused, disable (WLAN-AM `WLAN-ND-001500`) | FortiGate: `config wireless-controller vap; edit <SSID>; set l3-roaming disable; end` | — |
| Radio and RF | Redesigned 802.11ac and 802.11ax MCS rate control | 7.2.1 and later | No direct requirement; if unused, disable (WLAN-AM `WLAN-ND-001500`) | — | — |
| Radio and RF | 802.11d enable or disable | 7.2.1 and later | No direct requirement; if unused, disable (WLAN-AM `WLAN-ND-001500`) | — | — |
| SSIDs and authentication | WPA3 enhancements (Wi-Fi 6 Release 2): WPA3-SAE Public Key (SAE-PK) and Hash-to-Element (H2E) only | 7.2.1 and later | WLAN-AP `WLAN-NW-000400`; WLAN-IG `WLAN-NW-000900`; WLAN-IG `WLAN-ND-000100` | FortiGate: `config wireless-controller vap; edit <SSID>; set security wpa3-sae; set sae-h2e-only enable; end` | P1 |
| Roaming and client services | Layer-3 roaming over bridge-mode SSIDs | 7.2.1 and later | No direct requirement; if unused, disable (WLAN-AM `WLAN-ND-001500`) | FortiGate: `config wireless-controller vap; edit <SSID>; set l3-roaming disable; end` | — |
| Roaming and client services | DSCP marking by client application (nDPI, bridge-mode SSIDs; application-dscp-marking) | 7.2.1 and later | No direct requirement; if unused, disable (WLAN-AM `WLAN-ND-001500`) | FortiGate: `config wireless-controller vap; edit <SSID>; set application-dscp-marking disable; end` | — |
| Models | New models FAP-231G, FAP-233G, FAP-431G, and FAP-433G | 7.2.1 and later | WLAN-AP `WLAN-NW-000400`; WLAN-AP `WLAN-NW-000600` | — (model selection; check certification) | — |
| Models | New model FAP-432FR | 7.2.2+; 7.4.1+ | WLAN-AP `WLAN-NW-000400`; WLAN-AP `WLAN-NW-000600` | — (model selection; check certification) | — |
| Wired ports | Wired clients on a LAN port bridged to a tunnel-mode SSID reported to the controller | 7.2.2 and later | No direct requirement; if unused, disable (WLAN-AM `WLAN-ND-001500`) | FortiGate: `config wireless-controller wtp-profile; edit <PROFILE>; config lan; set port-mode offline; end; end` | — |
| Radio and RF | External antenna parameters for FAP-432F and FAP-433F in the FortiAP profile | 7.2.3+; 7.4.0+ | WLAN-AP `WLAN-NW-000800` | FortiGate: `config wireless-controller wtp-profile; edit <PROFILE>; config radio-1; set optional-antenna none; end; end` | P1, P21 |
| Controller connectivity | Data channel security option "ipsec-sn" (IPsec VPN with the FortiAP serial number) | 7.2.3+; 7.4.0+ | WLAN-AP `WLAN-NW-000600`; WLAN-CP `WLAN-NW-000600` | FortiGate: `config wireless-controller wtp-profile; edit <PROFILE>; set dtls-policy ipsec-sn-vpn; end` | P1 |
| Roaming and client services | Miracast service option in Bonjour profiles | 7.2.3+; 7.4.0+ | No direct requirement; if unused, disable (WLAN-AM `WLAN-ND-001500`) | FortiGate: `config wireless-controller wtp-profile; edit <PROFILE>; unset bonjour-profile; end` | — |
| Radio and RF | Site survey improvements: channel-bonding bandwidth and 6 GHz channels | 7.2.3+; 7.4.1+ | WLAN-AP `WLAN-NW-000800` | FortiAP CLI: `cfg -a AP_MODE=0; cfg -c` | — |
| Controller connectivity | CAPWAP auto health check (cw_diag -c acs-chan-stats) | 7.2.3+; 7.4.1+ | No direct requirement; if unused, disable (WLAN-AM `WLAN-ND-001500`) | — (FortiAP CLI: `cw_diag -c acs-chan-stats` shows the result) | — |
| Controller connectivity | CAPWAP keep-alive messages over NAT (nat-session-keep-alive) | 7.2.4+; 7.4.2+ | No direct requirement; if unused, disable (WLAN-AM `WLAN-ND-001500`) | — | — |
| Controller connectivity | 250 Mbps limit removed for encrypted CAPWAP data (dtls-enabled, ipsec-vpn, ipsec-sn-vpn) | 7.2.5+; 7.4.3+ | WLAN-AP `WLAN-NW-000600`; WLAN-CP `WLAN-NW-000600` | FortiGate: `config wireless-controller wtp-profile; edit <PROFILE>; set dtls-policy dtls-enabled; end` | P1 |
| Security | FIPS certification and FortiAP FIPS mode (FIPS_CC) | 7.4.0 and later | WLAN-AP `WLAN-NW-000600`; NDM `SRG-APP-000179-NDM-000265` | FortiAP CLI: `cfg -a FIPS_CC=1; cfg -c` | P22 |
| Radio and RF | WPA3-SAE security over the mesh backhaul (MESH_AP_SECURITY) | 7.4.0 and later | WLAN-IG `WLAN-ND-000100`; WLAN-AP `WLAN-NW-000400` | FortiAP CLI: `cfg -a MESH_AP_SECURITY=2; cfg -c` | P1, P20 |
| Models | New model FAP-234G | 7.4.0 and later | WLAN-AP `WLAN-NW-000400`; WLAN-AP `WLAN-NW-000600` | — (model selection; check certification) | — |
| Management | Patch number shown in the FortiAP firmware version and reported to the FortiGate | 7.4.1 and later | WLAN-AM `WLAN-ND-001000`; NDM `SRG-APP-001035-NDM-000340` | — (the version is reported to the FortiGate) | — |
| Wireless intrusion detection | Foreground scanning improvements: scan channels preconfigured from the FortiGate | 7.4.1 and later | WLAN-AP `WLAN-NW-000100` | FortiGate: `config wireless-controller wids-profile; edit <WIDS_PROFILE>; set ap-scan enable; set ap-scan-channel-list-2G-5G <CHANNELS>; end` | P1, P3 |
| Location and IoT | BLE raw data logged and sent to the FortiPresence server | 7.4.1 and later | WLAN-AP `WLAN-NW-001300`; WLAN-CP `WLAN-NW-001300` | FortiGate: `config wireless-controller wtp-profile; edit <PROFILE>; config lbs; set fortipresence-ble disable; end; end` | P1 |
| SSIDs and authentication | Dynamic VLAN assignment on local-bridging and external-web captive-portal SSIDs | 7.4.1 and later | WLAN-AP `WLAN-NW-001100`; WLAN-IG `WLAN-NW-001000` | FortiGate: `config wireless-controller vap; edit <SSID>; set dynamic-vlan enable; end` | P1, P4, P16 |
| Security | Trusted Platform Module (TPM) on Wi-Fi 6E models | 7.4.1 and later | NDM `SRG-APP-000171-NDM-000258` | FortiAP CLI: `cfg -a TPM=1; cfg -c` | P22 |
| Location and IoT | Polestar NAO Track integration and asset management | 7.4.1 and later | No direct requirement; if unused, disable (WLAN-AM `WLAN-ND-001500`) | FortiGate: `config wireless-controller wtp-profile; edit <PROFILE>; config lbs; set ble-rtls none; end; end` | — |
| SSIDs and authentication | VLAN pool per VLAN name tag with round-robin assignment (Tunnel-Private-Group-Id) | 7.4.1 and later | WLAN-AP `WLAN-NW-001100` | FortiGate: `config wireless-controller vap; edit <SSID>; set dynamic-vlan enable; end` | P1, P4, P16 |
| Radio and RF | MIMO mode configuration | 7.4.1 and later | No direct requirement; if unused, disable (WLAN-AM `WLAN-ND-001500`) | — | — |
| Controller connectivity | Improved DNS method for AC discovery (DHCP option 15 domain suffix) | 7.4.1 and later | WLAN-AP `WLAN-NW-001300`; NDM `SRG-APP-000516-NDM-000335` | FortiAP CLI: `cfg -a AC_DISCOVERY_TYPE=1; cfg -a AC_IPADDR_1=<FORTIGATE_IP>; cfg -c` | P1, P2 |
| Models | Wi-Fi 7 model FAP-441K | 7.4.1 and later | WLAN-AP `WLAN-NW-000400`; WLAN-AP `WLAN-NW-000600` | — (model selection; check certification) | — |
| Monitoring and diagnostics | SAM tests with OWE, WPA3-SAE, and WPA2/WPA3-Enterprise security | 7.4.2 and later | No direct requirement; if unused, disable (WLAN-AM `WLAN-ND-001500`) | — | — |
| SSIDs and authentication | WPA3-SAE "Hunting-and-Pecking (HnP) only" setting | 7.4.2 and later | WLAN-IG `WLAN-NW-000900` | FortiGate: `config wireless-controller vap; edit <SSID>; set sae-hnp-only disable; set sae-h2e-only enable; end` | P1 |
| Radio and RF | Third-party external antenna gain configured from the FortiGate | 7.4.2 and later | WLAN-AP `WLAN-NW-000800` | FortiGate: `config wireless-controller wtp-profile; edit <PROFILE>; config radio-1; set optional-antenna-gain <GAIN>; end; end` | P1, P21 |
| Controller connectivity | Automatic reboot when stuck in a discovery loop | 7.4.2 and later | No direct requirement; if unused, disable (WLAN-AM `WLAN-ND-001500`) | — | — |
| Roaming and client services | Simplified Bonjour profile provisioning and failover | 7.4.2 and later | No direct requirement; if unused, disable (WLAN-AM `WLAN-ND-001500`) | FortiGate: `config wireless-controller wtp-profile; edit <PROFILE>; unset bonjour-profile; end` | — |
| Roaming and client services | Individual control of 802.11k and 802.11v per SSID | 7.4.2 and later | No direct requirement; if unused, disable (WLAN-AM `WLAN-ND-001500`) | FortiGate: `config wireless-controller vap; edit <SSID>; set 80211k disable; set 80211v disable; end` | — |
| Models | New model FAP-432G | 7.4.2 and later | WLAN-AP `WLAN-NW-000400`; WLAN-AP `WLAN-NW-000600` | — (model selection; check certification) | — |
| Models | Wi-Fi 7 models FAP-441K and FAP-443K (FAP-441K first in 7.4.1) | 7.4.2+; 7.6.1+ | WLAN-AP `WLAN-NW-000400`; WLAN-AP `WLAN-NW-000600` | — (model selection; check certification) | — |
| SSIDs and authentication | Private key generation for WPA3-SAE SSIDs with public key authentication (cw_diag sae-pk-gen) | 7.4.2 and later | WLAN-IG `WLAN-ND-000100` | FortiGate: `execute wireless-controller create-sae-pk <SSID>` | P1 |
| Security | MACsec in WAN port 802.1X authentication (Wi-Fi 6E models; Wi-Fi 7 models from 7.6.2) | 7.4.3+; 7.6.2+ | WLAN-AP `WLAN-NW-001100` | FortiGate: `config wireless-controller wtp-profile; edit <PROFILE>; set wan-port-auth 802.1x; set wan-port-auth-macsec enable; end` | P1, P6, P22 |
| Security | Lightweight UTM on the FortiAP (application control and web filtering) | 7.4.3+; 7.6.4+ | No direct requirement; if unused, disable (WLAN-AM `WLAN-ND-001500`) | FortiGate: `config wireless-controller vap; edit <SSID>; set utm-status disable; end` | — |
| Management | USB port enabled or disabled from the FortiGate | 7.4.3 and later | WLAN-AM `WLAN-ND-001500` | FortiGate: `config wireless-controller wtp-profile; edit <PROFILE>; set usb-port disable; end` | — |
| SSIDs and authentication | User MPSK management through FortiGuest or FortiAuthenticator | 7.4.3 and later | WLAN-IG `WLAN-ND-000100` | FortiGate: `config wireless-controller mpsk-profile; edit <MPSK_PROFILE>; set mpsk-external-server-auth enable; set mpsk-external-server <SERVER>; end` | P1, P19 |
| SSIDs and authentication | RADIUS NAS-Filter-Rule attribute and dynamic access control lists for stations | 7.4.3 and later | WLAN-AP `WLAN-NW-001100` | FortiGate: `config wireless-controller vap; edit <SSID>; set nas-filter-rule enable; end` | P1, P4 |
| Monitoring and diagnostics | SAM ping test results include latency | 7.4.3 and later | No direct requirement; if unused, disable (WLAN-AM `WLAN-ND-001500`) | — | — |
| SSIDs and authentication | MPSK profiles on local-standalone WPA3-SAE SSIDs | 7.4.4+; 7.6.0+ | WLAN-IG `WLAN-ND-000100` | FortiGate: `config wireless-controller vap; edit <SSID>; set mpsk-profile <MPSK_PROFILE>; end` | P1, P18 |
| Location and IoT | BLE real-time location service (RTLS) configuration and the Evresys RTLS solution | 7.4.4+; 7.6.1+ | No direct requirement; if unused, disable (WLAN-AM `WLAN-ND-001500`) | FortiGate: `config wireless-controller wtp-profile; edit <PROFILE>; config lbs; set ble-rtls none; end; end` | — |
| Radio and RF | Channel bandwidth configuration in sniffer mode | 7.4.4+; 7.6.0+ | No direct requirement; if unused, disable (WLAN-AM `WLAN-ND-001500`) | — | — |
| SSIDs and authentication | MAC address database updated from the FortiGate WiFi controller | 7.4.4+; 7.6.1+ | No direct requirement; if unused, disable (WLAN-AM `WLAN-ND-001500`) | — | — |
| SSIDs and authentication | RADIUS-based MAC-address MPSK authentication on WPA3-SAE SSIDs | 7.4.4+; 7.6.1+ | WLAN-IG `WLAN-ND-000100` | FortiGate: `config wireless-controller vap; edit <SSID>; set radius-mac-auth enable; set radius-mac-mpsk-auth enable; end` | P1, P4 |
| SSIDs and authentication | Portal server certificate with wildcard or matching DNS names for HTTPS redirection on bridge-mode captive-portal SSIDs | 7.4.4+; 7.6.1+ | WLAN-IG `WLAN-NW-001000`; NDM `SRG-APP-000516-NDM-000344` | FortiGate: `config wireless-controller vap; edit <SSID>; set auth-cert <CERT>; end` | P1, P5 |
| Management | Local-bridging UTM logs sent in syslog format to FortiAnalyzer (Wi-Fi 6E models) | 7.4.5+; 7.6.1+ | NDM `SRG-APP-000515-NDM-000325`; NDM `SRG-APP-000516-NDM-000350` | FortiGate: `config wireless-controller vap; edit <SSID>; set utm-log enable; end` | P1, P10, P11, P22 |
| SSIDs and authentication | RADIUS over TLS (RadSec) for WPA2/WPA3-Enterprise authentication | 7.4.5+; 7.6.1+ | WLAN-AP `WLAN-NW-000500`; WLAN-CP `WLAN-NW-000500`; NDM `SRG-APP-000172-NDM-000259` | FortiGate: `config user radius; edit <RADIUS_SERVER>; set transport-protocol tls; set ca-cert <CA_CERT>; end` | P1, P4, P5 |
| SSIDs and authentication | RADIUS over TLS (RadSec) for bridge-mode captive-portal authentication | 7.4.5+; 7.6.1+ | WLAN-IG `WLAN-NW-001000`; NDM `SRG-APP-000172-NDM-000259` | FortiGate: `config user radius; edit <RADIUS_SERVER>; set transport-protocol tls; set ca-cert <CA_CERT>; end` | P1, P4, P5 |
| Controller connectivity | Improved FortiAP failover across layer-3 boundaries | 7.4.5+; 7.6.1+ | No direct requirement; if unused, disable (WLAN-AM `WLAN-ND-001500`) | — | — |
| Models | New model FAP-23JK | 7.4.5+; 7.6.2+ | WLAN-AP `WLAN-NW-000400`; WLAN-AP `WLAN-NW-000600` | — (model selection; check certification) | — |
| Models | New model FAP-231K (Secure Boot; only certified GA firmware loads) | 7.4.5+; 7.6.2+ | NDM `SRG-APP-000131-NDM-000243`; WLAN-AP `WLAN-NW-000400`; WLAN-AP `WLAN-NW-000600` | — (Secure Boot is set at the factory) | — |
| Controller connectivity | AC priority preference for HA failover and fallback (AC_PRI_PREFERENCE) | 7.4.5+; 7.6.1+ | No direct requirement; if unused, disable (WLAN-AM `WLAN-ND-001500`) | — | — |
| Management | BLE-based management by FortiExplorer Go (iOS) on Wi-Fi 6E and Wi-Fi 7 models | 7.4.6+; 7.6.2+ | WLAN-AM `WLAN-ND-001500` | — (no setting found in the 8.0.1 CLI Reference or configuration guide; BLE access is available for 30 minutes after reboot) | — |
| Monitoring and diagnostics | SNMP queries for uptime, traffic, CPU, memory, station count, and temperature | 7.4.6+; 7.6.2+ | WLAN-AM `WLAN-ND-001200` | FortiGate: `config wireless-controller snmp; config user; edit <SNMP_USER>; set security-level auth-priv; set auth-proto sha256; set priv-proto aes256; end; end` | P1, P12 |
| Controller connectivity | Improved stability of CAPWAP connections to FortiEdge Cloud | 7.4.6+; 7.6.3+ | WLAN-AP `WLAN-NW-001300` | FortiAP CLI: `cfg -a AC_DISCOVERY_TYPE=1; cfg -a AC_IPADDR_1=<FORTIGATE_IP>; cfg -c` | P1, P2 |
| Location and IoT | IEEE 802.11mc (fine timing measurement) protocol | 7.6.0 and later | No direct requirement; if unused, disable (WLAN-AM `WLAN-ND-001500`) | FortiGate: `config wireless-controller wtp-profile; edit <PROFILE>; config radio-1; set 80211mc disable; end; end` | — |
| Wired ports | Local LAN segregation (local-lan-partition) | 7.6.0 and later | WLAN-AP `WLAN-NW-001100` | FortiGate: `config wireless-controller vap; edit <SSID>; set local-lan-partition enable; end` | P1 |
| Roaming and client services | mDNS traffic restriction (micro-location) in Bonjour profiles | 7.6.0 and later | No direct requirement; if unused, disable (WLAN-AM `WLAN-ND-001500`) | FortiGate: `config wireless-controller wtp-profile; edit <PROFILE>; unset bonjour-profile; end` | — |
| SSIDs and authentication | Static RADIUS NAS-ID on local-standalone SSIDs | 7.6.0 and later | No direct requirement; if unused, disable (WLAN-AM `WLAN-ND-001500`) | FortiGate: `config wireless-controller vap; edit <SSID>; set local-standalone disable; end` | — |
| Controller connectivity | IKEv2 in the CAPWAP data tunnel with IPsec VPN encryption | 7.6.0 and later | WLAN-AP `WLAN-NW-000600`; WLAN-CP `WLAN-NW-000600` | FortiGate: `config wireless-controller wtp-profile; edit <PROFILE>; set dtls-policy ipsec-vpn; end` | P1 |
| SSIDs and authentication | WPA3 beacon protection on Wi-Fi 6E and Wi-Fi 7 models | 7.6.1 and later | WLAN-AP `WLAN-NW-000400`; WLAN-IG `WLAN-NW-000900` | FortiGate: `config wireless-controller vap; edit <SSID>; set beacon-protection enable; end` | P1, P22 |
| Management | Console, SSH, or HTTPS login with remote accounts from a TACACS+ server | 7.6.1 and later | WLAN-AM `WLAN-ND-001100`; WLAN-AM `WLAN-ND-000600`; WLAN-AM `WLAN-ND-001300` | FortiGate: `config wireless-controller wtp-profile; edit <PROFILE>; set admin-auth-tacacs+ <TACACS_SERVER>; set admin-restrict-local enable; end` | P1, P8 |
| Wireless intrusion detection | Advanced wireless intrusion detection (WIDS) options | 7.6.1 and later | WLAN-AP `WLAN-NW-000100` | FortiGate: `config wireless-controller wids-profile; edit <WIDS_PROFILE>; set sensor-mode both; set ap-spoofing enable; set chan-based-mitm enable; set spoofed-deauth enable; end` | P1, P3 |
| SSIDs and authentication | "AP Name:SSID" format for the RADIUS Called-Station-Id attribute | 7.6.1 and later | No direct requirement; if unused, disable (WLAN-AM `WLAN-ND-001500`) | — | — |
| SSIDs and authentication | RADIUS accounting with the FortiGuest server for local-standalone MPSK SSIDs | 7.6.1 and later | No direct requirement; if unused, disable (WLAN-AM `WLAN-ND-001500`) | FortiGate: `config wireless-controller vap; edit <SSID>; set local-standalone disable; end` | — |
| Roaming and client services | Zoom and Webex in nDPI application detection and DSCP marking | 7.6.1 and later | No direct requirement; if unused, disable (WLAN-AM `WLAN-ND-001500`) | FortiGate: `config wireless-controller vap; edit <SSID>; set application-dscp-marking disable; end` | — |
| Management | Local administrator lockout (ADMIN_LOCKOUT_THRESHOLD, ADMIN_LOCKOUT_DURATION) | 7.6.2 and later | WLAN-AM `WLAN-ND-001400` | FortiAP CLI: `cfg -a ADMIN_LOCKOUT_THRESHOLD=3; cfg -a ADMIN_LOCKOUT_DURATION=900; cfg -c` | — |
| Radio and RF | Zero-wait dynamic frequency selection (DFS) | 7.6.3 and later | No direct requirement; if unused, disable (WLAN-AM `WLAN-ND-001500`) | — | — |
| Radio and RF | Automated Frequency Coordination (AFC) for 6 GHz (FAP-234G, 432G, 441K, 443K; FAP-241K and FAP-243K from 7.6.5) | 7.6.3 and later | WLAN-AP `WLAN-NW-001300` | — (no AFC setting found in the 8.0.1 CLI Reference; AFC contacts an external AFC system) | — |
| Radio and RF | Multi-Link Operation (MLO) and preamble puncturing on Wi-Fi 7 models | 7.6.3 and later | No direct requirement; if unused, disable (WLAN-AM `WLAN-ND-001500`) | FortiGate: `config wireless-controller vap; edit <SSID>; set mlo disable; end` | — |
| Radio and RF | Zero-touch provisioning (ZTP) in mesh configuration | 7.6.3 and later | No direct requirement; if unused, disable (WLAN-AM `WLAN-ND-001500`) | FortiAP CLI: `cfg -a MESH_AP_TYPE=0; cfg -c` | — |
| SSIDs and authentication | Bypass of the default Captive Network Assistant (CNA) | 7.6.3 and later | WLAN-IG `WLAN-NW-001000` | FortiGate: `config wireless-controller vap; edit <SSID>; set captive-network-assistant-bypass disable; end` | P1 |
| Wireless intrusion detection | Improved foreground scan and dedicated scan radio on Wi-Fi 6E and Wi-Fi 7 models | 7.6.3 and later | WLAN-AP `WLAN-NW-000100` | FortiGate: `config wireless-controller wtp-profile; edit <PROFILE>; config radio-1; set mode monitor; end; end` | P1, P3 |
| Models | New Wi-Fi 7 model FAP-244K | 7.6.3 and later | WLAN-AP `WLAN-NW-000400`; WLAN-AP `WLAN-NW-000600` | — (model selection; check certification) | — |
| Models | New Wi-Fi 7 model FAP-221K | 7.6.3 and later | WLAN-AP `WLAN-NW-000400`; WLAN-AP `WLAN-NW-000600` | — (model selection; check certification) | — |
| Models | New Wi-Fi 7 model FAP-222KL | 7.6.3 and later | WLAN-AP `WLAN-NW-000400`; WLAN-AP `WLAN-NW-000600` | — (model selection; check certification) | — |
| Radio and RF | Factory defaults changed: MESH_AP_TYPE=2 (Ethernet with mesh backup) and MESH_AP_SECURITY=1 | 7.6.3 and later | WLAN-AM `WLAN-ND-001500` | FortiAP CLI: `cfg -a MESH_AP_TYPE=0; cfg -c` | — |
| Radio and RF | 240 MHz and 320 MHz site-survey channel bandwidth on Wi-Fi 7 models | 7.6.3 and later | WLAN-AP `WLAN-NW-000800` | FortiAP CLI: `cfg -a AP_MODE=0; cfg -c` | — |
| Radio and RF | Upgraded hostapd package for Wi-Fi 7 features | 7.6.4 and later | No direct requirement; if unused, disable (WLAN-AM `WLAN-ND-001500`) | — | — |
| Controller connectivity | IPv6 networking and IPv6 AC management (ADDR6_MODE and related variables) | 7.6.4 and later | WLAN-AP `WLAN-NW-001200`; WLAN-CP `WLAN-NW-001200` | FortiAP CLI: `cfg -a AC_IPADDR_PREFERENCE=IPv4-only; cfg -c` | — |
| Security | EST or SCEP certificate enrollment for WAN port 802.1X authentication | 7.6.4 and later | WLAN-AP `WLAN-NW-000700`; NDM `SRG-APP-000516-NDM-000344` | FortiGate: `config wireless-controller wtp-profile; edit <PROFILE>; set apcfg-auto-cert enable; set apcfg-auto-cert-enroll-protocol est; set apcfg-auto-cert-est-server <EST_SERVER>; end` | P1, P5, P6, P7 |
| SSIDs and authentication | Customizable DHCP Option 82 insertion | 7.6.4 and later | No direct requirement; if unused, disable (WLAN-AM `WLAN-ND-001500`) | FortiGate: `config wireless-controller vap; edit <SSID>; set dhcp-option82-insertion disable; end` | — |
| Controller connectivity | Up to three external AC addresses configured from FortiEdge Cloud | 7.6.4 and later | WLAN-AP `WLAN-NW-001300` | FortiAP CLI: `cfg -a AC_DISCOVERY_TYPE=1; cfg -a AC_IPADDR_1=<FORTIGATE_IP>; cfg -c` | P1, P2 |
| Controller connectivity | IPv6 local network and IPv6 AC variables (ADDR6_MODE, AP_IPADDR6, AC_IPADDR6_1) | 7.6.4 and later | WLAN-AP `WLAN-NW-001200`; WLAN-CP `WLAN-NW-001200` | FortiAP CLI: `cfg -a AC_IPADDR_PREFERENCE=IPv4-only; cfg -c` | — |
| Radio and RF | Mesh background scan enabled by default and 6 GHz mesh scan channel list | 7.6.4 and later | No direct requirement; if unused, disable (WLAN-AM `WLAN-ND-001500`) | FortiAP CLI: `cfg -a MESH_AP_TYPE=0; cfg -c` | — |
| Wired ports | FAP-23JK LAN3/PSE port 802.3af output in high power mode (POE_MODE=8) | 7.6.5 and later | No direct requirement; if unused, disable (WLAN-AM `WLAN-ND-001500`) | — | — |
| Models | FAP-231K Gen2 model | 7.6.5 and later | WLAN-AP `WLAN-NW-000400`; WLAN-AP `WLAN-NW-000600` | — (model selection; check certification) | — |
| Radio and RF | Multi-Link Operation (MLO) on local-standalone SSIDs | 7.6.5 and later | No direct requirement; if unused, disable (WLAN-AM `WLAN-ND-001500`) | FortiGate: `config wireless-controller vap; edit <SSID>; set mlo disable; end` | — |
| Radio and RF | Transmit power adaptation based on USB connectivity (FAP-241K and FAP-243K) | 7.6.5 and later | WLAN-AP `WLAN-NW-000800` | FortiGate: `config wireless-controller wtp-profile; edit <PROFILE>; config radio-1; set power-mode dBm; set power-value <DBM>; end; end` | P1 |
| Controller connectivity | IPsec offload for the data channel when the DTLS policy is IPsec VPN | 8.0.0 and later | WLAN-AP `WLAN-NW-000600`; WLAN-CP `WLAN-NW-000600` | FortiGate: `config wireless-controller wtp-profile; edit <PROFILE>; set dtls-policy ipsec-vpn; set ipsec-offload enable; end` | P1 |
| Management | Admin login password randomized by default on authorization by the FortiGate (FortiOS 8.0.1) | 8.0.0 and later | WLAN-AM `WLAN-ND-000300`; WLAN-AM `WLAN-ND-000200` | FortiGate: `config wireless-controller global; set login-passwd-on-deauth reset; end` | P1, P23 |
| Location and IoT | Location Wireless Interface (LOWI) positioning | 8.0.0 and later | No direct requirement; if unused, disable (WLAN-AM `WLAN-ND-001500`) | FortiGate: `config wireless-controller wtp-profile; edit <PROFILE>; config radio-1; set 80211mc disable; end; end` | — |
| Wireless intrusion detection | Continuous background scan (CBS) | 8.0.0 and later | WLAN-AP `WLAN-NW-000100` | FortiGate: `config wireless-controller wids-profile; edit <WIDS_PROFILE>; set ap-scan enable; end` | P1, P3 |
| Radio and RF | FortiAP and FortiWiFi local radios disabled from the FortiGate GUI | 8.0.0 and later | WLAN-AM `WLAN-ND-001500` | FortiGate: `config wireless-controller wtp-profile; edit <PROFILE>; config radio-1; set mode disabled; end; end` | — |
| SSIDs and authentication | Dynamic redirect URLs from Cisco ISE on local-bridging captive-portal SSIDs | 8.0.0 and later | WLAN-IG `WLAN-NW-001000` | FortiGate: `config wireless-controller vap; edit <SSID>; set captive-portal-dynamic-redirect-url disable; end` | P1 |
| SSIDs and authentication | Up to 16 SSIDs per radio | 8.0.0 and later | No direct requirement; if unused, disable (WLAN-AM `WLAN-ND-001500`) | FortiGate: `config wireless-controller global; set max-vap-per-radio 8; end` | — |
| SSIDs and authentication | Domain names (FQDN or wildcard) in layer-3 access control lists | 8.0.0 and later | WLAN-AP `WLAN-NW-001100` | FortiGate: `config wireless-controller vap; edit <SSID>; set access-control-list <ACL>; end` | P1, P17 |
| Radio and RF | Clear Channel Assessment (CCA) threshold tuning | 8.0.0 and later | No direct requirement; if unused, disable (WLAN-AM `WLAN-ND-001500`) | — | — |
| SSIDs and authentication | RADIUS cache for 802.1X authentication survivability | 8.0.0 and later | WLAN-AP `WLAN-NW-000500` | FortiGate: `config wireless-controller vap; edit <SSID>; set radius-auth-survivability disable; end` | P1, P4 |
| Monitoring and diagnostics | Wireless packet capture from the FortiGate GUI | 8.0.0 and later | No direct requirement; if unused, disable (WLAN-AM `WLAN-ND-001500`) | — | — |
| SSIDs and authentication | WPA3 transition-mode SSIDs with different authentication behavior per radio band (FortiOS 8.0.1) | 8.0.0 and later | WLAN-IG `WLAN-NW-000900`; WLAN-AP `WLAN-NW-000400` | FortiGate: `config wireless-controller vap; edit <SSID>; set security wpa3-only-enterprise; end` | P1, P4, P23 |

### Requirement reference

The requirements used in the map, with their severity in the current STIG
and SRG releases. For WLAN rules the SRG ID that DISA assigns to the rule is
shown in parentheses:

[Download the requirement reference as CSV](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/data/volume-172-disa-srgs-and-stigs/14-fortiap-feature-version-and-srg-map-requirements.csv) (56 rows).

| SRG | Requirement | Severity | Requirement title |
| --- | --- | --- | --- |
| WLAN-AM | `WLAN-ND-000200` (`SRG-APP-000164-NDM-000252`) | CAT II | The network device must enforce a minimum 15-character password length. |
| WLAN-AM | `WLAN-ND-000300` (`SRG-APP-000080-NDM-000345`) | CAT II | The network device must not have any default manufacturer passwords when deployed. |
| WLAN-AM | `WLAN-ND-000500` (`SRG-APP-000190-NDM-000267`) | CAT I | The network device must terminate all network connections associated with a device management session at the end of the session, or the session must be terminated after 10 minutes of inactivity except to fulfill documented and validated mission requirements. |
| WLAN-AM | `WLAN-ND-000600` (`SRG-APP-000153-NDM-000249`) | CAT II | The network device must be configured to authenticate each administrator prior to authorizing privileges based on assignment of group or role. |
| WLAN-AM | `WLAN-ND-000800` (`SRG-APP-000412-NDM-000331`) | CAT I | The network device must be configured to implement cryptographic mechanisms using a FIPS 140-2 approved algorithm to protect the confidentiality of remote maintenance sessions. |
| WLAN-AM | `WLAN-ND-000900` (`SRG-APP-000503-NDM-000320`) | CAT II | The network device must generate audit records when successful/unsuccessful logon attempts occur. |
| WLAN-AM | `WLAN-ND-001000` (`SRG-APP-000516-NDM-000351`) | CAT I | The network device must be running an operating system release that is currently supported by the vendor. |
| WLAN-AM | `WLAN-ND-001100` (`SRG-APP-000516-NDM-000336`) | CAT I | The network device must be configured to use an authentication server to authenticate users prior to granting administrative access. |
| WLAN-AM | `WLAN-ND-001200` (`SRG-APP-000395-NDM-000310`) | CAT II | The network device must be configured to authenticate SNMP messages using a FIPS-validated Keyed-Hash Message Authentication Code (HMAC). |
| WLAN-AM | `WLAN-ND-001300` (`SRG-APP-000148-NDM-000346`) | CAT II | The network device must be configured with only one local account to be used as the account of last resort in the event the authentication server is unavailable. |
| WLAN-AM | `WLAN-ND-001400` (`SRG-APP-000065-NDM-000214`) | CAT II | The network device must be configured to enforce the limit of three consecutive invalid logon attempts, after which time it must block any login attempt for 15 minutes. |
| WLAN-AM | `WLAN-ND-001500` (`SRG-APP-000142-NDM-000245`) | CAT I | The network device must be configured to prohibit the use of all unnecessary and/or nonsecure functions, ports, protocols, and/or services. |
| WLAN-AM | `WLAN-ND-001600` (`SRG-APP-000395-NDM-000347`) | CAT II | The network device must authenticate Network Time Protocol (NTP) sources using authentication that is cryptographically based. |
| WLAN-AM | `WLAN-ND-001800` (`SRG-APP-000516-NDM-000335`) | CAT II | The network device must be configured with both an ingress and egress ACL. |
| WLAN-AP | `WLAN-NW-000100` (`SRG-NET-000383`) | CAT II | The site must conduct continuous wireless Intrusion Detection System (IDS) scanning. |
| WLAN-AP | `WLAN-NW-000200` (`SRG-NET-000512`) | CAT III | WLAN SSIDs must be changed from the manufacturer's default to a pseudo random word that does not identify the unit, base, organization, etc. |
| WLAN-AP | `WLAN-NW-000300` (`SRG-NET-000514`) | CAT II | The WLAN inactive/idle session timeout must be set for 30 minutes or less. |
| WLAN-AP | `WLAN-NW-000400` (`SRG-NET-000063`) | CAT II | WLAN components must be Wi-Fi Alliance certified with WPA3. |
| WLAN-AP | `WLAN-NW-000500` (`SRG-NET-000070`) | CAT II | WLAN must use EAP-TLS. |
| WLAN-AP | `WLAN-NW-000600` (`SRG-NET-000151`) | CAT II | WLAN components must be FIPS 140-2 or FIPS 140-3 certified and configured to operate in FIPS mode. |
| WLAN-AP | `WLAN-NW-000700` (`SRG-NET-000070`) | CAT II | WLAN EAP-TLS implementation must use certificate-based PKI authentication to connect to DoW networks. |
| WLAN-AP | `WLAN-NW-000800` (`SRG-NET-000384`) | CAT III | WLAN signals must not be intercepted outside areas authorized for WLAN access. |
| WLAN-AP | `WLAN-NW-001100` (`SRG-NET-000512`) | CAT II | Wireless access points and bridges must be placed in dedicated subnets outside the enclave's perimeter. |
| WLAN-AP | `WLAN-NW-001200` (`SRG-NET-000205`) | CAT II | The network device must be configured to only permit management traffic that ingresses and egresses the out-of-band management (OOBM) interface. |
| WLAN-AP | `WLAN-NW-001300` (`SRG-NET-000131`) | CAT II | The network device must not be configured to have any feature enabled that calls home to the vendor. |
| WLAN-IG | `WLAN-ND-000100` (`SRG-APP-000164-NDM-000252`) | CAT II | The password configured on the WLAN access point for key generation and client access must be set to a 15-character or longer complex password as required by USCYBERCOM CTO 07-15 Rev1. |
| WLAN-IG | `WLAN-NW-000900` (`SRG-NET-000063`) | CAT II | The WLAN access point must be configured for Wi-Fi Alliance WPA3 security. |
| WLAN-IG | `WLAN-NW-001000` (`SRG-NET-000512`) | CAT II | DoW Components providing guest WLAN access (internet access only) must use separate WLAN or logical segmentation of the enterprise WLAN (e.g., separate service set identifier [SSID] and virtual LAN) or DoW network. |
| WLAN-CM | `WLAN-ND-000600` (`SRG-APP-000153-NDM-000249`) | CAT II | The network device must be configured to authenticate each administrator prior to authorizing privileges based on assignment of group or role. |
| WLAN-CM | `WLAN-ND-000700` (`SRG-APP-000033-NDM-000212`) | CAT I | The network device must enforce the assigned privilege level for each administrator and authorizations for access to all commands relative to the privilege level in accordance with applicable policy for the device. |
| WLAN-CM | `WLAN-ND-000800` (`SRG-APP-000412-NDM-000331`) | CAT I | The network device must be configured to implement cryptographic mechanisms using a FIPS 140-2 approved algorithm to protect the confidentiality of remote maintenance sessions. |
| WLAN-CM | `WLAN-ND-001000` (`SRG-APP-000516-NDM-000351`) | CAT I | The network device must be running an operating system release that is currently supported by the vendor. |
| WLAN-CM | `WLAN-ND-001500` (`SRG-APP-000142-NDM-000245`) | CAT I | The network device must be configured to prohibit the use of all unnecessary and/or nonsecure functions, ports, protocols, and/or services. |
| WLAN-CP | `WLAN-NW-000300` (`SRG-NET-000514`) | CAT II | The WLAN inactive/idle session timeout must be set for 30 minutes or less. |
| WLAN-CP | `WLAN-NW-000500` (`SRG-NET-000070`) | CAT II | WLAN must use EAP-TLS. |
| WLAN-CP | `WLAN-NW-000600` (`SRG-NET-000151`) | CAT II | WLAN components must be FIPS 140-2 or FIPS 140-3 certified and configured to operate in FIPS mode. |
| WLAN-CP | `WLAN-NW-000700` (`SRG-NET-000070`) | CAT II | WLAN EAP-TLS implementation must use certificate-based PKI authentication to connect to DoD networks. |
| WLAN-CP | `WLAN-NW-001200` (`SRG-NET-000205`) | CAT II | The network device must be configured to only permit management traffic that ingresses and egresses the out-of-band management (OOBM) interface. |
| WLAN-CP | `WLAN-NW-001300` (`SRG-NET-000131`) | CAT II | The network device must not be configured to have any feature enabled that calls home to the vendor. |
| NDM | `SRG-APP-000131-NDM-000243` | CAT II | The network device must prevent the installation of patches, service packs, or application components without verification the software component has been digitally signed using a certificate that is recognized and approved by the organization. |
| NDM | `SRG-APP-000142-NDM-000245` | CAT I | The network device must be configured to prohibit the use of all unnecessary and/or nonsecure functions, ports, protocols, and/or services |
| NDM | `SRG-APP-000171-NDM-000258` | CAT I | The network device must be configured to store passwords using an approved salted key derivation function, preferably using a keyed hash for password-based authentication. |
| NDM | `SRG-APP-000172-NDM-000259` | CAT I | The network device must transmit only encrypted representations of passwords. |
| NDM | `SRG-APP-000179-NDM-000265` | CAT I | The network device must use FIPS 140-2 approved algorithms for authentication to a cryptographic module. |
| NDM | `SRG-APP-000380-NDM-000304` | CAT II | The network device must enforce access restrictions associated with changes to device configuration. |
| NDM | `SRG-APP-000408-NDM-000314` | CAT II | Network devices performing maintenance functions must restrict use of these functions to authorized personnel only. |
| NDM | `SRG-APP-000411-NDM-000330` | CAT I | The network devices must use FIPS-validated Keyed-Hash Message Authentication Code (HMAC) to protect the integrity of nonlocal maintenance and diagnostic communications. |
| NDM | `SRG-APP-000435-NDM-000315` | CAT II | The network device must be configured to protect against known types of denial-of-service (DoS) attacks by employing organization-defined security safeguards. |
| NDM | `SRG-APP-000457-NDM-000352` | CAT II | The network device must install security-relevant firmware updates within 30 days unless the time period is directed by an authoritative source (e.g., IAVM, CTOs, DTMs, STIGs). |
| NDM | `SRG-APP-000515-NDM-000325` | CAT II | The network device must off-load audit records onto a different system or media than the system being audited. |
| NDM | `SRG-APP-000516-NDM-000335` | CAT II | The network device must enforce access restrictions associated with changes to the system components. |
| NDM | `SRG-APP-000516-NDM-000340` | CAT II | The network device must be configured to conduct backups of system level information contained in the information system when changes occur. |
| NDM | `SRG-APP-000516-NDM-000344` | CAT II | The network device must obtain its public key certificates from an appropriate certificate policy through an approved service provider. |
| NDM | `SRG-APP-000516-NDM-000350` | CAT I | The network device must be configured to send log data to at least one central log server for the purpose of forwarding alerts to the administrators and the information system security officer (ISSO). For boundary devices, two log servers are required. |
| NDM | `SRG-APP-000880-NDM-000290` | CAT II | The network device must be configured to protect nonlocal maintenance sessions by separating the maintenance session from other network sessions with the system by logically separated communications paths. |
| NDM | `SRG-APP-001035-NDM-000340` | CAT I | The network device hardware and software must be a version supported by the vendor. |

### Collecting evidence

Most of the evidence lives on the FortiGate. Collect the
`config wireless-controller` sections of `show full-configuration` (FortiAP
profiles, SSIDs, WIDS profiles, settings, timers, syslog profile, and SNMP),
the managed FortiAP list with each unit's firmware version, the FortiAP
images held on the FortiGate (`execute wireless-controller list-wtp-image`), the wireless event log, and the rogue AP list. From each FortiAP
model, collect `cfg -s` (the variables that differ from the defaults) to show
FIPS mode, lockout, and discovery settings. Attach both, with the WLAN
approval, to the WLAN checklists.

## Validation and Troubleshooting

- **A feature in the map is missing on your FortiAP.** Check the version
  column against the FortiAP firmware, check the FortiOS release on the
  FortiGate against the compatibility matrix, and check whether the feature
  applies to your model.
- **A setting made on the FortiAP disappears.** The FortiGate may have pushed
  its own configuration. Make the change in the FortiAP profile or SSID on the
  FortiGate instead.
- **A FortiAP will not join after hardening.** Check that the FortiGate
  interface allows Security Fabric (CAPWAP) access, that the FortiAP is
  authorized, that static discovery points to the right address, and that
  the data channel setting matches on both sides.
- **FIPS mode cannot be enabled.** The model may not support it (FAP-431F
  and FAP-433F), or the firmware may be older than 7.4.0.
- **A requirement has no matching feature.** Some WLAN requirements are met
  by site procedure (signal containment surveys, placement, approval) or by
  another system (the RADIUS server for EAP-TLS, the central log server, the
  FortiGate NDM STIG). Record how the requirement is met, not just which
  feature covers it.

## Security and Best Practices

- Keep FortiAP and FortiOS on vendor-supported releases and track the version
  column when planning upgrades.
- Set a strong FortiAP administrator password from the controller, restrict
  FortiAP management to HTTPS and SSH, disable the console port, and use
  TACACS+ with local login restricted where the release supports it.
- Enable FIPS mode on supported FortiAP models and FIPS-CC mode on the
  FortiGate where DoD requires it.
- Send FortiAP and wireless controller logs to a central log server.
- Review this map each time Fortinet publishes a FortiAP release or DISA
  updates the WLAN STIGs or the NDM SRG.

## References and Knowledge Checks

**References:**

- Fortinet, *FortiAP Release Notes*, releases 7.0.0 to 8.0.0, section "New
  features or enhancements" (docs.fortinet.com, FortiAP documentation).
- Fortinet, *FortiWiFi and FortiAP 8.0.1 Configuration Guide*, including the
  appendix "FortiAP CLI configuration and diagnostics commands".
- Fortinet, *FortiOS 8.0.1 CLI Reference* (docs.fortinet.com).
- DISA Network WLAN STIG package (AP-NIPR, AP-IG, and Controller Management
  and Platform STIGs) and Network Device Management SRG V5R5, from the
  October 2026 STIG Library Compilation.
- [Chapter 03](03-the-srg-catalog-how-stigs-are-built-and-what-to-do-without-one.md)
  (SRG-based assessment),
  [Chapter 10](10-fortinet-products-stigs-and-srg-mapping.md) (Fortinet
  products),
  [Chapter 11](11-fortiswitch-feature-version-and-srg-map.md) (the
  FortiSwitch map, the same controller model),
  [Chapter 12](12-fortianalyzer-feature-version-and-srg-map.md) (the
  FortiAnalyzer map), and
  [Chapter 13](13-fortimanager-feature-version-and-srg-map.md) (the
  FortiManager map).

**Knowledge checks:**

1. What must be true before any WLAN STIG requirement applies to a FortiAP?
2. Why does a FortiAP assessment use the Network WLAN STIGs, and how do the
   Management and Platform STIGs divide the requirements?
3. Where does the version data come from, given that FortiAP has no feature
   matrix or New Features Guide?
4. Why should FortiAP settings be made on the FortiGate rather than on the
   FortiAP, and which settings exist only on the FortiAP CLI?
5. Which WLAN requirements can FortiAP not meet exactly, and how do you
   handle them?
6. What applies to a feature marked "No direct requirement"?

## Summary and Completion Checklist

FortiAP has no product-specific STIG, so it is assessed against DISA's
generic Network WLAN STIGs, for the access point and for the FortiGate
acting as its controller, plus the NDM SRG, and only after wireless has been
approved for the environment. This chapter maps 186 features to the
FortiAP release that introduced them, to 56 WLAN STIG and NDM SRG
requirements, and to the command that configures them on the FortiGate or
the FortiAP: 39 core platform features, and 147 features from the
FortiAP release notes for 7.0.0 through 8.0.0. Operational features with no
direct requirement fall under the rule to prohibit unnecessary functions when
unused.

- [ ] Can confirm that WLAN is approved and pick the WLAN STIG for each SSID.
- [ ] Can find the release that introduced a FortiAP feature.
- [ ] Can map a FortiAP feature to its WLAN STIG or NDM requirement.
- [ ] Can find the FortiGate or FortiAP command that meets the requirement.
- [ ] Can collect FortiAP evidence from the managing FortiGate and the
  FortiAP CLI, and record the requirements FortiAP cannot meet exactly.
