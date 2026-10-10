# Chapter 30: FortiGate Feature, Version, and STIG Map

## Learning Objectives

- Find the FortiOS release that introduced a given FortiGate feature.
- Map each FortiGate feature to the rule of the Fortinet FortiGate Firewall
  NDM STIG or the Fortinet FortiGate Firewall STIG that it satisfies, or,
  for functions the two STIGs do not cover, to the IDPS, VPN, ALG, or Router
  SRG requirement.
- Find every one of the 89 FortiGate STIG rules in the map, with its
  severity and the SRG requirement it implements.
- Use each STIG rule's own fix text as the command to configure it, and
  recognize where that fix text no longer matches the current FortiOS CLI.
- Explain what the Cloud Computing SRG adds when FortiGate runs as a VM in a
  public cloud.
- Record the requirements that FortiGate cannot meet exactly with the fix
  text, with their mitigations.

## Theory and Architecture

FortiGate is Fortinet's next-generation firewall, sold as hardware
appliances and as FortiGate VM for private hypervisors and public clouds.
Every model runs **FortiOS**, which combines stateful firewall policies with
security profiles (IPS, antivirus, web filtering, application control, DNS
filtering, and SSL/SSH inspection), IPsec and SSL VPN, an explicit web
proxy, dynamic routing, SD-WAN, high availability, and the controller
functions for FortiSwitch and FortiAP. FortiGate is the only Fortinet product
with DISA STIGs (Chapter 10): the **Fortinet FortiGate Firewall NDM STIG**
for the management plane and the **Fortinet FortiGate Firewall STIG** for
traffic filtering. For every FortiGate feature this chapter gives **which
FortiOS release introduced it**, **which STIG rule or SRG requirement it
relates to**, and **which command configures it to meet that
requirement**. It is the last and largest map of the series.

The FortiOS CLI uses `config`, `edit`, `set`, `next`, and `end`
statements, and the same settings are in the GUI. A few ideas run through
the configuration and through the STIGs:

- **Administrators and profiles.** Each administrator in `config system
  admin` has an administrator profile (`config system accprofile`) that
  gives None, Read, or Read/Write access to each area (System, Log and
  Report, Firewall, and others), trusted hosts that limit where the
  administrator can log in from, and either a local password or a match on
  a remote server group (LDAP, RADIUS, or TACACS+). Most NDM STIG rules
  about access control come down to the profiles and the trusted hosts.
- **Global settings.** `config system global` holds the idle timeout,
  lockout, pre-login banner, administrative TLS versions, strong
  cryptography, the CLI audit log, and revision backups; `config system
  password-policy`, `config system ntp`, `config system snmp user`, and
  `config system fips-cc` hold the rest of the management settings.
- **Policies and profiles.** Traffic is denied unless a firewall policy
  (`config firewall policy`, one table for IPv4 and IPv6) allows it. The
  policy names the interfaces, addresses, services, and schedule, sets the
  traffic logging, and applies the security profiles. DoS policies
  (`config firewall DoS-policy`) apply anomaly thresholds before the
  firewall policy.
- **Logging.** The event log filter (`config log eventfilter`) selects
  the event logs, each policy sets its traffic logging, and logs go to the
  local disk, FortiAnalyzer, and syslog servers. Automation stitches
  (*Security Fabric > Automation*) turn log events into email alerts.
- **VDOMs.** A FortiGate can be split into virtual domains, each with its
  own policies and profiles. Global settings (administrators, the password
  policy, FIPS-CC mode) apply to the whole device; check the per-VDOM
  settings in every VDOM.

### Where the version data comes from

Fortinet does not publish a feature matrix for FortiOS. Instead, each
release train has a **FortiOS New Features Guide** that lists the features
added in that train under the guide's own top-level categories and tags
each one with the patch release that introduced it (an untagged feature
arrived in the train's first release). The version column was built from
all five guides Fortinet publishes for FortiOS 7.0, 7.2, 7.4, 7.6, and 8.0
(981, 731, 1,028, 1,015, and 1,060 pages); their tags run up to 7.0.16,
7.2.12, 7.4.12, 7.6.7, and 8.0.1. These are the same kind of guide as the
FortiAnalyzer and FortiManager guides used in Chapters 12 and 13, and the
same pipeline was used.

The feature titles come from each guide's table of contents on
docs.fortinet.com, which gives the full titles. The PDF bookmarks were read
as a cross-check: every one of the 1,408 second-level entries matches a
bookmark, but 106 long titles are cut short in the bookmarks and were taken
from the online table of contents instead. A second-level entry is one
feature; nine third-level entries (the ZTNA examples in 7.0 and one ZTNA
connector topic in 8.0) are sub-topics and are folded into their parent.
That gives 1,415 entries: 324 in 7.0, 261 in 7.2, 317 in 7.4, 287 in 7.6,
and 226 in 8.0. A feature that is listed in more than one guide (usually a
feature backported to an older train) is one row, so the 1,415 entries
make **1291 features**. The full list is kept: nothing was collapsed or
left out, because a script maps the rows that have no direct requirement in
one step.

The table has two groups of rows:

- **Core platform features** (categories starting with *Core:*) are the
  long-standing capabilities that the STIG rules depend on: management
  access, administrators and profiles, authentication, the password policy,
  logging, time, SNMP, backups, firmware, certificates, FIPS-CC mode,
  firewall and DoS policies, security profiles, VPN, routing, HA, and
  central management. They existed before 7.0.0 and are not in any New
  Features Guide.
- **New features** are every feature in the five guides, grouped under the
  guide's own categories in the order of the 8.0 guide (*GUI*, *Network*,
  *SD-WAN*, *Policy and objects*, *Zero Trust Network Access*, *Security
  profiles*, *VPN*, *User and authentication*, *LAN Edge*, *System*,
  *Security Fabric*, *Log and report*, *Cloud*, *FortiOS Carrier*,
  *FortiASIC*, and *Operational Technology*). The 7.0 and 7.2 guides use a
  *Secure access* category for what later guides split into *LAN Edge* and
  *Zero Trust Network Access*; those rows keep *Secure access* and are listed
  after *LAN Edge*. Within a category the rows are sorted by release.

| Version entry | Meaning |
| --- | --- |
| `7.0.0 or earlier` | A core platform feature, present in 7.0.0 and earlier releases |
| `7.4.1 and later` | Introduced in 7.4.1 (listed in one guide only) |
| `7.0.12+; 7.2.5+; 7.4.0+` | Listed in several guides: introduced in each train at the release shown (often a backport); the first release in each train is shown |

Two cautions apply. First, "and later" means later releases in the same
train and, usually, later trains, but a feature introduced in a patch of an
older train may reach a newer train only in that train's later patches;
check the release notes for your exact release. Second, many features
depend on the model, the license, or the platform: NP7 and SOC
acceleration, 2 GB RAM models (which lose the proxy features from 7.4.4),
FortiGate Rugged models, the cloud marketplaces, and FortiGuard
subscriptions. Some features were also removed: SSL VPN tunnel mode is
replaced by IPsec VPN from 7.6.3.

### Where the STIG and SRG data comes from

The requirement column uses the October 2026 DISA library. The two
FortiGate STIGs come in one package,
`U_FN_FortiGate_Firewall_Y26M10_STIG.zip`, and are the primary
requirements; the SRGs cover the functions the STIGs leave out:

| Column | STIG or SRG | Release | Applies to |
| --- | --- | --- | --- |
| **FGT-NDM** | Fortinet FortiGate Firewall NDM STIG | V1R6, benchmark date 30 Sep 2026; 60 rules (9 CAT I, 51 CAT II) | The management plane: administrators and profiles, authentication, the password policy, sessions and the banner, event logging and its protection and off-loading, time, SNMP, backups, certificates, FIPS-CC mode, and supported, signed firmware |
| **FGT-FW** | Fortinet FortiGate Firewall STIG | V1R5, benchmark date 30 Sep 2026; 29 rules (3 CAT I, 24 CAT II, 2 CAT III) | The firewall function: policy filtering, PPSM and VPN filtering, DoS protection, traffic logging, log protection and transport, application-layer inspection, anti-spoofing, fail-secure behavior, and packet capture |
| **IDPS** | Intrusion Detection and Prevention Systems SRG | V3R4, benchmark date 28 Oct 2025 | IPS sensors, IPS signatures and their updates, and virtual patching |
| **VPN** | Virtual Private Network SRG | V3R5, benchmark date 01 Jul 2026 | IPsec VPN (site-to-site and dial-up), SSL VPN, and Agentless VPN |
| **ALG** | Application Layer Gateway SRG | V2R4, benchmark date 01 Jul 2026 | Web filtering, application control, SSL/SSH inspection, the explicit web proxy and ZTNA access proxy, and the content-filtering profiles (antivirus and DNS filter) |
| **RTR** | Router SRG | V5R2, benchmark date 28 Oct 2025 | Static and policy routes, OSPF, BGP, routing protocol authentication, and the router-like interface settings |
| **CC** | Cloud Computing Mission Owner Operating System SRG V1R3 (benchmark date 13 Aug 2025) and Network SRG V1R2 (benchmark date 30 Jan 2025) | See the columns | Cited only in *FortiGate VM in public cloud*, for the hosting environment |

The two STIGs are the authority wherever they have a rule. Their rules
have STIG IDs of the form `FGFW-ND-nnnnnn` (NDM) and `FNFG-FW-nnnnnn`
(Firewall), and the map cites them by that rule version, as the XCCDF
gives it. The Requirement reference table adds each rule's severity and the
SRG requirement it implements (the XCCDF group title), so
FGT-NDM `FGFW-ND-000045` shows that it implements NDM SRG requirement
`SRG-APP-000065-NDM-000214`. **All 89 rules appear in the map**, each
attached to the core or listed feature that satisfies it; the build script
fails if one is missing.

For FortiGate functions that the two STIGs do not cover, the map uses the
SRGs that Chapter 10 assigns: IDPS for IPS sensors, VPN for SSL VPN and
IPsec VPN, ALG for web filtering, application control, SSL/SSH inspection,
and the explicit proxy, and Router for routing. Two placements go a little
further than Chapter 10's table, and are this chapter's choice: the ZTNA
access proxy is mapped to ALG, because it is an authenticating application
proxy like the explicit proxy; and the antivirus and DNS filter profiles are
mapped to ALG, because the ALG SRG's content-filtering requirements (real-time
scans of files at the boundary, blocking malicious code, and blocking
prohibited content) describe exactly what those profiles do. The SRG
requirement IDs are the rule versions from each SRG's XCCDF, and the
severity is the rule's severity (high = CAT I, medium = CAT II, low =
CAT III).

Each feature maps to one of three kinds of relationship:

- **Implements a requirement.** The feature is how FortiGate meets a rule.
  The CLI audit log implements the full-text recording of privileged
  commands (FGT-NDM `FGFW-ND-000100`), for example.
- **Must be configured to meet a requirement.** The feature is in scope of
  a rule and has to be set up correctly. The administrator password policy
  must require 15 characters (FGT-NDM `FGFW-ND-000220`), for example.
- **No direct requirement.** The feature is operational or cosmetic, such
  as an SD-WAN steering option, a GUI page, or a cloud connector. It has no
  rule of its own, but if it is not needed it falls under the NDM STIG rule
  that implements the NDM requirement to prohibit unnecessary functions:
  FGT-NDM `FGFW-ND-000200`, a CAT I rule that implements
  `SRG-APP-000142-NDM-000245`. Those rows read "No direct requirement; if
  unused, disable (FGT-NDM `FGFW-ND-000200`)". When the feature is part of a
  function that is enabled, the function's own SRG applies as well, as
  Chapter 10 explains.

The mapping is a starting point for an assessment, not a ruling. Confirm it
with your assessor, especially the SRG placements for functions outside the
STIGs.

### Where the commands come from

Each STIG rule has a vendor-specific check and fix, so the **fix text of
the rule is the authority for the command** wherever it gives one: the
command cell repeats the fix text's CLI, with its placeholders in angle
brackets. Every command was then checked against the newest CLI reference,
the **FortiOS 8.0.1 CLI Reference** (the same extraction and verifier code
Chapter 14 used): every `config` path must be documented, every nested
`config` must be a documented sub-table, every `set` option must be in the
syntax of its path, and every literal value must be one of the documented
values. Each GUI pane named in the column must appear in the text of the
New Features Guides, and each `execute` or `get` command must appear in the
CLI Reference or in a New Features Guide (`get system status` is printed in
the guides, not in the CLI Reference). The final run checked 93 CLI blocks
and 8 GUI panes with no failures. Read the column this way:

- Commands run on the FortiOS CLI, over SSH or in the GUI's CLI console.
  Each pair of backticks is one block; statements are separated by `;` to
  fit in a table cell, and on the CLI each one goes on its own line. Values
  in `<ANGLE_BRACKETS>` are placeholders.
- **GUI:** entries name the FortiOS GUI pane; the text in parentheses says
  what to set.
- For **"No direct requirement"** rows, a dash (**—**) means there is
  nothing to configure for the requirement: turn the feature off, or do not
  configure it, if it is not used.

Some fix texts no longer match the FortiOS CLI, and some rules cannot be
met exactly. Record these on the checklist as findings with mitigations, or
meet them another way:

- **`config firewall policy6`.** The Firewall STIG fix text for
  FGT-FW `FNFG-FW-000005` and FGT-FW `FNFG-FW-000030` configures IPv6
  policies under `config firewall policy6`, which the 8.0.1 CLI Reference
  does not have: IPv4 and IPv6 share `config firewall policy`, with
  `srcaddr6` and `dstaddr6` for IPv6 addresses. The map uses the shared
  table.
- **Changed characters in a new password.** The fix text for
  FGT-NDM `FGFW-ND-000311` sets `change-8-characters`, which neither the
  7.6.0 nor the 8.0.1 CLI Reference documents. FortiOS 7.0.0 replaced it
  with a minimum number of new characters (the 7.0 New Features Guide), and
  the 7.6.0 CLI Reference documents `set min-change-characters` under
  `config system password-policy`; on 7.0 through 7.6, set it to 8. The
  8.0.1 CLI Reference lists that option only for `config user
  password-policy` (local users), not for administrator passwords. On 8.0,
  give administrators remote LDAP accounts, whose passwords the directory
  controls, and record the finding for the local account of last resort.
- **SNMPv3 security level.** The fix text for FGT-NDM `FGFW-ND-000210` sets
  `security-level auth`, which is not a documented value; the 8.0.1 values
  are `no-auth-no-priv`, `auth-no-priv`, and `auth-priv`. The map uses
  `auth-priv` with SHA-256 authentication, as the fix text requires, and
  AES-256 privacy.
- **Banner message name.** The fix text for FGT-NDM `FGFW-ND-000050` and
  FGT-NDM `FGFW-ND-000055` writes `config system replacemsg admin
  pre_admin-disclaimer-text`; the 8.0.1 syntax is `config system
  replacemsg admin` followed by `edit <msg-type>`. The message name comes
  from the fix text.
- **Local audit list options.** The fix text for FGT-NDM `FGFW-ND-000175`
  lists every option of `config log setting` and `config log eventfilter`
  as a menu. Three of them (`log-invalid-packet`, `log-policy-name`, and
  `compliance-check`) are not in the 8.0.1 CLI Reference; the map uses the
  documented options.
- **Alerts when the syslog server is lost.** FortiOS has an event for a lost
  FortiAnalyzer connection but not for a lost syslog server, so the fix text
  for FGT-FW `FNFG-FW-000105` builds one: a load-balancing virtual server
  with a TCP health check on the syslog port, and an automation stitch on
  the "VIP real server down" event. The GUI pane the fix text names
  (*Policy & Objects > Health Check*) is not in the New Features Guides, so
  the map gives the CLI (`config firewall ldb-monitor` and `config firewall
  vip`). Alerting from FortiAnalyzer or the syslog server itself is simpler
  where it is available.
- **Two-factor authentication.** The NDM STIG has no multifactor rule for
  administrators. FortiToken is mapped to the replay-resistant
  authentication rule (FGT-NDM `FGFW-ND-000205`), and DoD PKI for
  administrators is not required by the STIG; follow the organization's
  policy.
- **Signed firmware.** FGT-NDM `FGFW-ND-000305` is met by procedure: install
  updates from FortiGuard or FortiManager, or compare the published hash of
  an image downloaded from the support site. The BIOS-level signature and
  file integrity checks of 7.0.12, 7.2.5, and 7.4.0 and later add a
  technical control.
- **SSL VPN tunnel mode.** From 7.6.3, SSL VPN tunnel mode is replaced by
  IPsec VPN, and tunnel-mode settings such as split tunneling are not in
  the 8.0.1 CLI Reference. Apply the VPN SRG to the dial-up IPsec VPN that
  replaces it (no split-include addresses, so that all client traffic uses
  the tunnel) and to the Agentless VPN web portal.
- **No SCAP benchmark.** The FortiGate STIGs are manual, so every rule is
  checked by hand or by a script against the configuration (Chapter 10).

### FortiGate VM in public cloud

FortiGate VM runs on AWS, Azure, Google Cloud, Oracle Cloud, AliCloud, and
other clouds (the *Cloud* category of the map has the cloud features of
each release). The FortiGate STIGs apply to the VM exactly as to an
appliance. The **Cloud Computing SRG** adds the obligations of the hosting
environment, which fall on the Mission Owner, not on FortiOS (see Chapter 29
for how that SRG is built: a Cloud Service Provider document without
requirement IDs, and Mission Owner requirements in XCCDF). A FortiGate VM
deployed by the Mission Owner in infrastructure as a service (IaaS) is
usually the very control those requirements ask for, so record it as the
evidence:

- **The cloud offering.** Obtain AO authorization for the cloud service
  offering (CC `SRG-OS-000480-CLD-000025`), choose one listed in the DoD
  Cloud Service Catalog at the impact level of the data (CC
  `SRG-OS-000480-CLD-000031` for Impact Level 4/5), register the
  connection in SNAP (CC `SRG-OS-000368-CLD-000040`), and keep the cloud
  portal credentials least privilege (CC `SRG-OS-000001-CLD-000010`), since
  the portal can change the FortiGate VM's network and disks.
- **The security stack.** The IaaS must have a security stack that
  restricts traffic between the IaaS and the boundary or internal cloud
  access point (CC `SRG-NET-000205-CLD-000085`), internet-facing
  applications must traverse the cloud access point and virtual datacenter
  security stack (CC `SRG-NET-000205-CLD-000090`), management and
  production traffic must be kept separate (CC
  `SRG-NET-000205-CLD-000100`), and the Mission Owner must restrict ports
  and protocols (CC `SRG-OS-000096-CLD-000060`). FortiGate VM firewall
  policies, with a dedicated management interface and subnet, meet these.
- **Inspection and monitoring.** An IDPS must protect the VMs and services
  (CC `SRG-NET-000383-CLD-000105`), and inbound and outbound traffic must be
  monitored (CC `SRG-NET-000390-CLD-000110`, CC
  `SRG-NET-000391-CLD-000115`): IPS sensors on the FortiGate VM policies,
  assessed against the IDPS SRG.
- **Logging and hygiene.** The IaaS must log centrally
  (CC `SRG-OS-000342-CLD-000020`), which the FortiGate VM's FortiAnalyzer or
  syslog logging supports, and orphaned or unused VM instances must be
  removed (CC `SRG-OS-000368-CLD-000045`), including old FortiGate VM
  instances left behind after an upgrade or a failed autoscaling event.

The cloud provider's own access, HA, and SDN connector settings (IAM roles
for the SDN connector, for example) are outside FortiOS; review them with
the cloud environment's own STIG or SRG guidance.

## Design Considerations

- **Pick the release first, then the features.** A design that needs a
  feature introduced in a certain release (BIOS-level signature and
  file integrity checks, console-only local logins in 7.6.0,
  disallowed login methods for each administrator in 8.0.0, or IPsec
  instead of SSL VPN tunnel mode from 7.6.3) sets the minimum FortiOS
  release, and it must be a vendor-supported release (FGT-NDM
  `FGFW-ND-000170`, CAT I).
- **Treat the STIGs as the floor, not the scope.** The two STIGs cover
  management and filtering. Every security profile or VPN you enable brings
  its SRG with it; leaving a function off is the cheapest way to shrink the
  assessment, and the NDM rule on unnecessary functions
  (FGT-NDM `FGFW-ND-000200`) requires it anyway.
- **Separate management from data.** Put HTTPS and SSH only on a dedicated
  management interface, restrict them with trusted hosts and local-in
  policies, and block outbound management traffic at a premise firewall
  (FGT-FW `FNFG-FW-000125`). In a cloud, give the management interface its
  own subnet.
- **Authenticate administrators centrally.** Use LDAP over LDAPS
  (FGT-NDM `FGFW-ND-000165`, FGT-NDM `FGFW-ND-000245`) with one local
  account of last resort (FGT-NDM `FGFW-ND-000030`), and administrator
  profiles that separate system, log, and firewall duties.
- **Log twice.** The Firewall STIG wants logs queued locally when the
  central server is lost (FGT-FW `FNFG-FW-000045`) and protected in transit
  (FGT-FW `FNFG-FW-000050`): log to the local disk and to FortiAnalyzer, or
  to two central servers, over reliable, encrypted transport, and alert on
  lost connections.
- **Plan FIPS-CC mode early.** FIPS-CC mode (FGT-NDM `FGFW-ND-000255`,
  CAT I) is a global setting for the whole device. Enable it on a new device or in a maintenance window,
  and test VPN peers and management tools against it.
- **Use central management.** FortiManager keeps the configuration
  revisions the backup rules require (FGT-NDM `FGFW-ND-000180`, FGT-NDM
  `FGFW-ND-000185`) and pushes the same STIG settings to every FortiGate;
  Chapter 13 maps FortiManager itself.

## Implementation and Automation

### The FortiGate feature map

The requirement column uses the abbreviations defined in *Where the STIG
and SRG data comes from*. The requirement titles, severities, and SRG IDs
are listed in the next table. The command column follows the conventions in
*Where the commands come from*.

[Download the feature map as CSV](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/data/volume-172-disa-srgs-and-stigs/30-fortigate-feature-version-and-stig-map-feature-map.csv) (1363 rows).

| Category | Feature | Introduced (FortiOS) | STIG or SRG requirement(s) | Command to satisfy the requirement |
| --- | --- | --- | --- | --- |
| Core: Management access | Administrative access protocols on each interface (HTTPS, SSH, PING, SNMP, HTTP, Telnet, FMG-Access, and others) | 7.0.0 or earlier | FGT-NDM `FGFW-ND-000260`; FGT-NDM `FGFW-ND-000265`; FGT-NDM `FGFW-ND-000200` | `config system interface; edit <MGMT_PORT>; set allowaccess ping https ssh; next; end` (HTTPS and SSH only, on the management interface; no HTTP or Telnet) |
| Core: Management access | HTTPS administrative access TLS versions and SSH version 1 | 7.0.0 or earlier | FGT-NDM `FGFW-ND-000205`; FGT-NDM `FGFW-ND-000265` | `config system global; set admin-https-ssl-versions tlsv1-2 tlsv1-3; set admin-ssh-v1 disable; end` |
| Core: Management access | Strong cryptography for HTTPS and SSH administrative access | 7.0.0 or earlier | FGT-NDM `FGFW-ND-000265`; FGT-NDM `FGFW-ND-000260` | `config system global; set strong-crypto enable; end` |
| Core: Management access | Administrator idle timeout | 7.0.0 or earlier | FGT-NDM `FGFW-ND-000270`; FGT-NDM `FGFW-ND-000275` | `config system global; set admintimeout 10; end` |
| Core: Management access | Administrator lockout after failed logins | 7.0.0 or earlier | FGT-NDM `FGFW-ND-000045` | `config system global; set admin-lockout-threshold 3; set admin-lockout-duration 900; end` |
| Core: Management access | Pre-login disclaimer banner (Standard Mandatory DoD Notice and Consent Banner) | 7.0.0 or earlier | FGT-NDM `FGFW-ND-000050`; FGT-NDM `FGFW-ND-000055` | `config system global; set pre-login-banner enable; end`; `config system replacemsg admin; edit pre_admin-disclaimer-text; set buffer "<DOD_BANNER_TEXT>"; next; end` |
| Core: Management access | Concurrent administrator sessions | 7.0.0 or earlier | FGT-NDM `FGFW-ND-000300` | `config system global; set admin-concurrent disable; set admin-login-max <NUMBER>; end` |
| Core: Management access | Trusted hosts for each administrator | 7.0.0 or earlier | FGT-NDM `FGFW-ND-000035`; FGT-NDM `FGFW-ND-000160`; FGT-NDM `FGFW-ND-000190` | `config system admin; edit <ADMIN>; set trusthost1 <IP> <MASK>; next; end` |
| Core: Management access | Local-in policies (traffic to the FortiGate itself) | 7.0.0 or earlier | FGT-NDM `FGFW-ND-000200`; FGT-NDM `FGFW-ND-000035` | `config firewall local-in-policy; edit <ID>; set intf <MGMT_PORT>; set srcaddr <MGMT_HOSTS>; set dstaddr <FGT_ADDRESS>; set service <SERVICES>; set schedule <SCHEDULE>; set action accept; next; end` (plus a final deny entry) |
| Core: Management access | Interface services that are not needed (DHCP relay, PPTP client, ARP, broadcast, layer 2, VLAN, and STP forwarding, ICMP redirects, LLDP transmission) | 7.0.0 or earlier | FGT-NDM `FGFW-ND-000200`; FGT-FW `FNFG-FW-000065`; RTR `SRG-NET-000362-RTR-000115`; RTR `SRG-NET-000362-RTR-000112`; RTR `SRG-NET-000364-RTR-000111` | `config system interface; edit <INTERFACE>; set dhcp-relay-service disable; set pptp-client disable; set arpforward disable; set broadcast-forward disable; set l2forward disable; set icmp-send-redirect disable; set vlanforward disable; set stpforward disable; set lldp-transmission disable; next; end` |
| Core: Management access | DoS policy protecting the management interface | 7.0.0 or earlier | FGT-NDM `FGFW-ND-000290` | `config firewall DoS-policy; edit <ID>; set interface <INTERFACE>; set srcaddr <SRC_ADDRESS>; set dstaddr <DST_ADDRESS>; set service <SERVICE>; config anomaly; edit <ANOMALY>; set status enable; set log enable; set action block; set threshold <THRESHOLD>; next; end; next; end` (incoming interface: the management interface; L3 and L4 anomalies set to the organization's thresholds) |
| Core: Administrator accounts | Administrator profiles: System access permission | 7.0.0 or earlier | FGT-NDM `FGFW-ND-000035`; FGT-NDM `FGFW-ND-000145`; FGT-NDM `FGFW-ND-000150`; FGT-NDM `FGFW-ND-000155`; FGT-NDM `FGFW-ND-000160`; FGT-NDM `FGFW-ND-000190`; FGT-NDM `FGFW-ND-000285` | `config system accprofile; edit <PROFILE>; set sysgrp read; next; end`; `config system admin; edit <ADMIN>; set accprofile <PROFILE>; next; end` (sysgrp read-write only in the profile of administrators authorized to change the system) |
| Core: Administrator accounts | Administrator profiles: Log and Report access permission | 7.0.0 or earlier | FGT-NDM `FGFW-ND-000130`; FGT-NDM `FGFW-ND-000135`; FGT-NDM `FGFW-ND-000140`; FGT-FW `FNFG-FW-000055`; FGT-FW `FNFG-FW-000060` | `config system accprofile; edit <PROFILE>; set loggrp none; next; end` (none or read for administrators without a need to manage logs) |
| Core: Administrator accounts | Default admin account password | 7.0.0 or earlier | FGT-NDM `FGFW-ND-000250` | `config system admin; edit admin; set password <PASSWORD>; next; end` |
| Core: Administrator accounts | One local account of last resort; other administrators matched on a remote server group | 7.0.0 or earlier | FGT-NDM `FGFW-ND-000030`; FGT-NDM `FGFW-ND-000165` | `config system admin; edit <ADMIN>; set remote-auth enable; set accprofile <PROFILE>; set remote-group <GROUP>; next; end` |
| Core: Administrator accounts | REST API administrators | 7.0.0 or earlier | FGT-NDM `FGFW-ND-000035`; FGT-NDM `FGFW-ND-000190` | `config system api-user; edit <API_USER>; set accprofile <PROFILE>; config trusthost; edit 1; set ipv4-trusthost <IP> <MASK>; next; end; next; end` |
| Core: Authentication | LDAP servers over LDAPS | 7.0.0 or earlier | FGT-NDM `FGFW-ND-000165`; FGT-NDM `FGFW-ND-000245` | `config user ldap; edit <LDAP_SERVER>; set server <SERVER_IP>; set cnid <CN>; set dn <BASE_DN>; set type regular; set username <BIND_DN>; set password <BIND_PASSWORD>; set secure ldaps; set ca-cert <CA_CERT>; next; end` |
| Core: Authentication | User groups with remote (LDAP) servers | 7.0.0 or earlier | FGT-NDM `FGFW-ND-000165` | `config user group; edit <GROUP>; set member <LDAP_SERVER>; next; end` |
| Core: Authentication | RADIUS and TACACS+ servers for administrator authentication | 7.0.0 or earlier | FGT-NDM `FGFW-ND-000030`; FGT-NDM `FGFW-ND-000165` | GUI: User & Authentication > RADIUS Servers (the NDM STIG requires LDAP over LDAPS; use RADIUS or TACACS+ only where the organization approves it) |
| Core: Authentication | FortiToken two-factor authentication for administrators | 7.0.0 or earlier | FGT-NDM `FGFW-ND-000205` | `config system admin; edit <ADMIN>; set two-factor fortitoken; set fortitoken <SERIAL_NUMBER>; next; end` |
| Core: Password policy | Administrator password policy (length and character classes) | 7.0.0 or earlier | FGT-NDM `FGFW-ND-000220`; FGT-NDM `FGFW-ND-000225`; FGT-NDM `FGFW-ND-000230`; FGT-NDM `FGFW-ND-000235`; FGT-NDM `FGFW-ND-000240` | `config system password-policy; set status enable; set apply-to admin-password; set minimum-length 15; set min-upper-case-letter 1; set min-lower-case-letter 1; set min-number 1; set min-non-alphanumeric 1; end` |
| Core: Password policy | Minimum number of changed characters in a new administrator password | 7.0.0 or earlier | FGT-NDM `FGFW-ND-000311` | — (no `change-8-characters` or `min-change-characters` option for administrator passwords in the 8.0.1 CLI Reference; see *Where the commands come from*) |
| Core: Logging and auditing | Event logging of system and user activity (account, privilege, logon, and session events) | 7.0.0 or earlier | FGT-NDM `FGFW-ND-000005`; FGT-NDM `FGFW-ND-000010`; FGT-NDM `FGFW-ND-000020`; FGT-NDM `FGFW-ND-000040`; FGT-NDM `FGFW-ND-000060`; FGT-NDM `FGFW-ND-000065`; FGT-NDM `FGFW-ND-000070`; FGT-NDM `FGFW-ND-000075`; FGT-NDM `FGFW-ND-000080`; FGT-NDM `FGFW-ND-000085`; FGT-NDM `FGFW-ND-000090` | `config log eventfilter; set event enable; set system enable; set endpoint enable; set user enable; end` |
| Core: Logging and auditing | Event and log settings for the locally defined list of auditable events | 7.0.0 or earlier | FGT-NDM `FGFW-ND-000175` | `config log setting; set fwpolicy-implicit-log enable; set local-in-allow enable; set local-in-deny-unicast enable; end`; `config log eventfilter; set event enable; set system enable; set endpoint enable; set user enable; end` (enable the events on the local audit list) |
| Core: Logging and auditing | Full-text CLI command audit log | 7.0.0 or earlier | FGT-NDM `FGFW-ND-000100` | `config system global; set cli-audit-log enable; end` |
| Core: Logging and auditing | User identity in logs (no anonymization) | 7.0.0 or earlier | FGT-NDM `FGFW-ND-000095` | `config log setting; set user-anonymize disable; end` |
| Core: Logging and auditing | Local disk logging, log file size, and full-disk behavior | 7.0.0 or earlier | FGT-NDM `FGFW-ND-000105`; FGT-FW `FNFG-FW-000045` | `config log disk setting; set status enable; set max-log-file-size <MB>; set diskfull overwrite; end` |
| Core: Logging and auditing | Logging to FortiAnalyzer | 7.0.0 or earlier | FGT-NDM `FGFW-ND-000110`; FGT-NDM `FGFW-ND-000295`; FGT-FW `FNFG-FW-000100` | `config log fortianalyzer setting; set status enable; set server <FAZ_IP>; set upload-option realtime; end` |
| Core: Logging and auditing | Logging to syslog servers over reliable TLS | 7.0.0 or earlier | FGT-NDM `FGFW-ND-000110`; FGT-NDM `FGFW-ND-000295`; FGT-FW `FNFG-FW-000045`; FGT-FW `FNFG-FW-000050`; FGT-FW `FNFG-FW-000100`; FGT-FW `FNFG-FW-000150` | `config log syslogd setting; set status enable; set server <SYSLOG_IP>; set mode reliable; set enc-algorithm high; end` |
| Core: Logging and auditing | Traffic logging in firewall policies | 7.0.0 or earlier | FGT-FW `FNFG-FW-000020`; FGT-FW `FNFG-FW-000025`; FGT-FW `FNFG-FW-000030`; FGT-FW `FNFG-FW-000035`; FGT-FW `FNFG-FW-000040`; FGT-FW `FNFG-FW-000160` | `config log eventfilter; set event enable; set system enable; set endpoint enable; set user enable; set security-rating enable; end`; `config firewall policy; edit <POLICY_ID>; set logtraffic all; next; end` |
| Core: Logging and auditing | Logging of traffic denied by the implicit deny policy | 7.0.0 or earlier | FGT-FW `FNFG-FW-000160`; FGT-FW `FNFG-FW-000165` | `config log setting; set fwpolicy-implicit-log enable; set fwpolicy6-implicit-log enable; end` |
| Core: Logging and auditing | Policy and address UUIDs in traffic logs | 7.0.0 or earlier | FGT-FW `FNFG-FW-000030`; FGT-FW `FNFG-FW-000035`; FGT-FW `FNFG-FW-000040` | `config system global; set log-uuid-address enable; end` |
| Core: Logging and auditing | Automation stitches that email an alert on log failure events | 7.0.0 or earlier | FGT-NDM `FGFW-ND-000115`; FGT-FW `FNFG-FW-000105` | `config system automation-trigger; edit <TRIGGER>; set event-type event-log; set logid <LOG_ID>; next; end`; `config system automation-action; edit <ACTION>; set action-type email; set email-to <ADDRESS>; set email-subject <SUBJECT>; next; end`; GUI: Security Fabric > Automation (one stitch for each log failure event the STIG lists) |
| Core: Logging and auditing | Load balancing health check on a virtual server for the syslog server (to alert when it stops responding) | 7.0.0 or earlier | FGT-FW `FNFG-FW-000105` | `config firewall ldb-monitor; edit <MONITOR>; set type tcp; set interval 5; set timeout 1; set retry 1; set port 514; next; end`; `config firewall vip; edit <VIP>; set type server-load-balance; set server-type tcp; set extintf <UNUSED_INTERFACE>; set extip <UNUSED_IP>; set extport 514; set monitor <MONITOR>; config realservers; edit 1; set ip <SYSLOG_IP>; set port 514; next; end; next; end` (automation trigger on the "VIP real server down" event) |
| Core: Time and SNMP | NTP with authenticated, redundant servers | 7.0.0 or earlier | FGT-NDM `FGFW-ND-000120`; FGT-NDM `FGFW-ND-000215` | `config system ntp; set ntpsync enable; set type custom; set syncinterval <MINUTES>; config ntpserver; edit 1; set server <NTP_SERVER_1>; set authentication enable; set key <KEY>; set key-id <KEY_ID>; next; edit 2; set server <NTP_SERVER_2>; set authentication enable; set key <KEY>; set key-id <KEY_ID>; next; end; end` |
| Core: Time and SNMP | Time zone | 7.0.0 or earlier | FGT-NDM `FGFW-ND-000125` | `config system global; set timezone <TIMEZONE>; end` |
| Core: Time and SNMP | SNMPv3 users with SHA-256 authentication | 7.0.0 or earlier | FGT-NDM `FGFW-ND-000210` | `config system snmp user; edit <NAME>; set status enable; set security-level auth-priv; set auth-proto sha256; set auth-pwd <PASSWORD>; set priv-proto aes256; set priv-pwd <PASSWORD>; next; end` |
| Core: Backup and firmware | Configuration revision backup on administrator logout | 7.0.0 or earlier | FGT-NDM `FGFW-ND-000180`; FGT-NDM `FGFW-ND-000185` | `config system global; set revision-backup-on-logout enable; end` |
| Core: Backup and firmware | Vendor-supported FortiOS release and firmware upgrades | 7.0.0 or earlier | FGT-NDM `FGFW-ND-000170` | `get system status`; GUI: System > Firmware & Registration |
| Core: Backup and firmware | Firmware and update packages validated by signature or checksum | 7.0.0 or earlier | FGT-NDM `FGFW-ND-000305` | — (download images from FortiGuard, FortiManager, or the Fortinet support site, and compare the published hash before each upgrade) |
| Core: Certificates and cryptography | CA certificates (DoD-approved CAs) | 7.0.0 or earlier | FGT-NDM `FGFW-ND-000195` | GUI: System > Certificates (Import, CA Certificate) |
| Core: Certificates and cryptography | FIPS-CC mode | 7.0.0 or earlier | FGT-NDM `FGFW-ND-000255`; FGT-NDM `FGFW-ND-000280` | `config system fips-cc; set status enable; end` |
| Core: Firewall policy | Firewall policies filtering on interfaces, addresses, services, and schedules (IPv4 and IPv6 in one policy table) | 7.0.0 or earlier | FGT-FW `FNFG-FW-000005`; FGT-FW `FNFG-FW-000085`; FGT-FW `FNFG-FW-000115`; FGT-FW `FNFG-FW-000120` | `config firewall policy; edit <POLICY_ID>; set srcintf <IN_INTERFACE>; set dstintf <OUT_INTERFACE>; set srcaddr <SRC_ADDRESS>; set dstaddr <DST_ADDRESS>; set schedule <SCHEDULE>; set service <SERVICE>; set action accept; set logtraffic all; next; end` |
| Core: Firewall policy | Implicit deny (traffic not allowed by a policy is denied) | 7.0.0 or earlier | FGT-FW `FNFG-FW-000085`; FGT-FW `FNFG-FW-000115`; FGT-FW `FNFG-FW-000120`; FGT-NDM `FGFW-ND-000200`; RTR `SRG-NET-000202-RTR-000001` | — (implicit; permit only the traffic in the PPSM CAL and VA guidance) |
| Core: Firewall policy | Policies for traffic from VPN interfaces | 7.0.0 or earlier | FGT-FW `FNFG-FW-000015` | `config firewall policy; edit <POLICY_ID>; set srcintf <VPN_INTERFACE>; set dstintf <INTERFACE>; set srcaddr <SRC_ADDRESS>; set dstaddr <DST_ADDRESS>; set schedule <SCHEDULE>; set service <SERVICE>; set action accept; set logtraffic all; next; end` |
| Core: Firewall policy | Deny policy for outbound management traffic (premise firewall) | 7.0.0 or earlier | FGT-FW `FNFG-FW-000125`; RTR `SRG-NET-000364-RTR-000113` | `config firewall policy; edit <POLICY_ID>; set srcintf <MGMT_INTERFACE>; set dstintf <EGRESS_INTERFACE>; set srcaddr <MGMT_NETWORK>; set dstaddr <ALL_ADDRESS>; set schedule <SCHEDULE>; set service <ALL_SERVICE>; set action deny; set logtraffic all; next; end` |
| Core: Firewall policy | Policies limiting VPN traffic to the management network to authorized management hosts and services | 7.0.0 or earlier | FGT-FW `FNFG-FW-000130` | `config firewall policy; edit <POLICY_ID>; set srcintf <VPN_INTERFACE>; set dstintf <MGMT_INTERFACE>; set srcaddr <MGMT_HOSTS>; set dstaddr <MGMT_ASSETS>; set schedule <SCHEDULE>; set service <MGMT_SERVICES>; set action accept; next; end` |
| Core: Firewall policy | Session helpers (application-layer inspection of FTP, SIP, and other protocols) | 7.0.0 or earlier | FGT-FW `FNFG-FW-000135` | `config system session-helper; edit <ID>; set name <PROTOCOL_NAME>; set protocol <PROTOCOL_NUMBER>; set port <PORT>; next; end` |
| Core: Firewall policy | Asymmetric routing disabled (reverse path check of source addresses) | 7.0.0 or earlier | FGT-FW `FNFG-FW-000145`; RTR `SRG-NET-000205-RTR-000014` | `config system settings; set asymroute disable; set asymroute-icmp disable; set asymroute6 disable; set asymroute6-icmp disable; end` |
| Core: Firewall policy | Fail-closed behavior in conserve mode (IPS and antivirus fail-open disabled) | 7.0.0 or earlier | FGT-FW `FNFG-FW-000090`; IDPS `SRG-NET-000235-IDPS-00169` | `config ips global; set fail-open disable; end`; `config system global; set av-failopen off; set av-failopen-session disable; end` |
| Core: Firewall policy | Packet capture with host, port, VLAN, and protocol filters | 7.0.0 or earlier | FGT-FW `FNFG-FW-000155` | `config firewall on-demand-sniffer; edit <NAME>; set interface <PORT>; set max-packet-count <NUMBER>; set hosts <IP>; set ports <PORT_NUMBER>; set protocols <PROTOCOL_NUMBER>; next; end`; GUI: Network > Packet Capture |
| Core: DoS protection | IPv4 and IPv6 DoS policies (L3 and L4 anomaly thresholds) | 7.0.0 or earlier | FGT-FW `FNFG-FW-000070`; FGT-FW `FNFG-FW-000075`; FGT-FW `FNFG-FW-000110`; FGT-FW `FNFG-FW-000150`; FGT-NDM `FGFW-ND-000290`; IDPS `SRG-NET-000362-IDPS-00197` | `config firewall DoS-policy; edit <ID>; set interface <INTERFACE>; set srcaddr <SRC_ADDRESS>; set dstaddr <DST_ADDRESS>; set service <SERVICE>; config anomaly; edit <ANOMALY>; set status enable; set log enable; set action block; set threshold <THRESHOLD>; next; end; next; end` |
| Core: Security profiles | IPS sensors applied to firewall policies | 7.0.0 or earlier | IDPS `SRG-NET-000019-IDPS-00019`; IDPS `SRG-NET-000018-IDPS-00018`; IDPS `SRG-NET-000362-IDPS-00198`; IDPS `SRG-NET-000318-IDPS-00182`; IDPS `SRG-NET-000318-IDPS-00183`; IDPS `SRG-NET-000390-IDPS-00212`; IDPS `SRG-NET-000391-IDPS-00213`; IDPS `SRG-NET-000113-IDPS-00013`; IDPS `SRG-NET-000113-IDPS-00082` | `config ips sensor; edit <SENSOR>; config entries; edit 1; set severity <SEVERITIES>; set status enable; set action block; set log enable; set log-packet enable; next; end; next; end`; `config firewall policy; edit <POLICY_ID>; set utm-status enable; set ips-sensor <SENSOR>; next; end` |
| Core: Security profiles | FortiGuard IPS and antivirus signature updates | 7.0.0 or earlier | IDPS `SRG-NET-000019-IDPS-00187`; IDPS `SRG-NET-000246-IDPS-00205`; ALG `SRG-NET-000246-ALG-000132`; ALG `SRG-NET-000019-ALG-000019` | `config system autoupdate schedule; set status enable; set frequency automatic; end` |
| Core: Security profiles | Antivirus profiles | 7.0.0 or earlier | ALG `SRG-NET-000248-ALG-000133`; ALG `SRG-NET-000249-ALG-000134`; ALG `SRG-NET-000249-ALG-000145`; IDPS `SRG-NET-000249-IDPS-00176` | `config antivirus profile; edit <PROFILE>; config http; set av-scan block; end; next; end` |
| Core: Security profiles | Web filter profiles (FortiGuard categories, URL filters) | 7.0.0 or earlier | ALG `SRG-NET-000018-ALG-000017`; ALG `SRG-NET-000019-ALG-000018`; ALG `SRG-NET-000288-ALG-000109` | `config webfilter profile; edit <PROFILE>; config ftgd-wf; config filters; edit 1; set category <CATEGORY_ID>; set action block; next; end; end; next; end` |
| Core: Security profiles | Application control sensors | 7.0.0 or earlier | ALG `SRG-NET-000018-ALG-000017`; ALG `SRG-NET-000019-ALG-000018`; ALG `SRG-NET-000132-ALG-000087`; ALG `SRG-NET-000384-ALG-000136` | `config application list; edit <LIST>; config entries; edit 1; set category <CATEGORY_ID>; set action block; next; end; next; end` |
| Core: Security profiles | SSL/SSH inspection profiles (deep inspection and server certificate checks) | 7.0.0 or earlier | ALG `SRG-NET-000062-ALG-000150`; ALG `SRG-NET-000164-ALG-000100`; ALG `SRG-NET-000750-ALG-000140`; ALG `SRG-NET-000390-ALG-000139`; ALG `SRG-NET-000391-ALG-000140` | `config firewall ssl-ssh-profile; edit <PROFILE>; config https; set status deep-inspection; set untrusted-server-cert block; set expired-server-cert block; set revoked-server-cert block; end; next; end` |
| Core: Security profiles | Explicit web proxy | 7.0.0 or earlier | ALG `SRG-NET-000131-ALG-000086`; ALG `SRG-NET-000138-ALG-000063`; ALG `SRG-NET-000131-ALG-000085` | `config web-proxy explicit; set status disable; end` (unless the explicit proxy is used; then require authentication in proxy policies) |
| Core: Security profiles | DNS filter profiles | 7.0.0 or earlier | ALG `SRG-NET-000019-ALG-000018`; ALG `SRG-NET-000018-ALG-000017` | `config dnsfilter profile; edit <PROFILE>; config ftgd-dns; config filters; edit 1; set category <CATEGORY_ID>; set action block; next; end; end; next; end` |
| Core: IPsec VPN | IPsec VPN phase 1 (IKEv2, AES-256, SHA-384, DH group 20, certificates) | 7.0.0 or earlier | VPN `SRG-NET-000512-VPN-002220`; VPN `SRG-NET-000132-VPN-000460`; VPN `SRG-NET-000317-VPN-001090`; VPN `SRG-NET-000230-VPN-000780`; VPN `SRG-NET-000074-VPN-000250`; VPN `SRG-NET-000337-VPN-001300`; VPN `SRG-NET-000164-VPN-000560`; VPN `SRG-NET-000063-VPN-000220` | `config vpn ipsec phase1-interface; edit <TUNNEL>; set ike-version 2; set proposal aes256-sha384; set dhgrp 20; set keylife 28800; set authmethod signature; set certificate <CERT>; set peer <PEER_USER>; next; end` |
| Core: IPsec VPN | IPsec VPN phase 2 (AES-256, SHA-384, PFS, replay protection, SA lifetime) | 7.0.0 or earlier | VPN `SRG-NET-000525-VPN-002330`; VPN `SRG-NET-000371-VPN-001640`; VPN `SRG-NET-000147-VPN-000530`; VPN `SRG-NET-000337-VPN-001290`; VPN `SRG-NET-000371-VPN-001650` | `config vpn ipsec phase2-interface; edit <PHASE2>; set phase1name <TUNNEL>; set proposal aes256-sha384; set pfs enable; set dhgrp 20; set replay enable; set keylifeseconds 28800; next; end` |
| Core: IPsec VPN | PKI peer users for certificate authentication | 7.0.0 or earlier | VPN `SRG-NET-000164-VPN-000560`; VPN `SRG-NET-000166-VPN-000590`; VPN `SRG-NET-000355-VPN-002433` | `config user peer; edit <PEER_USER>; set ca <CA_CERT>; set subject <SUBJECT>; next; end` |
| Core: SSL VPN | SSL VPN settings (TLS version, idle timeout, login limits, client certificates) | 7.0.0 or earlier | VPN `SRG-NET-000062-VPN-000200`; VPN `SRG-NET-000530-VPN-002340`; VPN `SRG-NET-000213-VPN-000721`; VPN `SRG-NET-000140-VPN-000500`; VPN `SRG-NET-000053-VPN-000170` | `config vpn ssl settings; set ssl-min-proto-ver tls1-2; set idle-timeout <SECONDS>; set login-attempt-limit 3; set login-block-time 900; set reqclientcert enable; end` |
| Core: SSL VPN | SSL VPN web portals (tunnel mode is replaced by IPsec VPN from 7.6.3) | 7.0.0 or earlier | VPN `SRG-NET-000019-VPN-000040`; VPN `SRG-NET-000053-VPN-000170` | `config vpn ssl web portal; edit <PORTAL>; set limit-user-logins enable; next; end` |
| Core: IPsec VPN | Dial-up IPsec VPN for remote access (mode configuration, user groups, no split tunnel) | 7.0.0 or earlier | VPN `SRG-NET-000369-VPN-001620`; VPN `SRG-NET-000138-VPN-000490`; VPN `SRG-NET-000166-VPN-000580` | `config vpn ipsec phase1-interface; edit <TUNNEL>; set type dynamic; set mode-cfg enable; set authusrgrp <GROUP>; next; end` (no `ipv4-split-include`, so that all client traffic uses the tunnel) |
| Core: Routing | Static routes and policy routes | 7.0.0 or earlier | RTR `SRG-NET-000018-RTR-000001`; RTR `SRG-NET-000131-RTR-000035` | — |
| Core: Routing | OSPF with message-digest authentication | 7.0.0 or earlier | RTR `SRG-NET-000168-RTR-000078`; RTR `SRG-NET-000230-RTR-000001` | `config router ospf; config ospf-interface; edit <NAME>; set interface <PORT>; set authentication message-digest; set keychain <KEYCHAIN>; next; end; end` |
| Core: Routing | Key chains for routing protocol authentication (HMAC-SHA algorithms, key lifetimes) | 7.0.0 or earlier | RTR `SRG-NET-000168-RTR-000078`; RTR `SRG-NET-000230-RTR-000003` | `config router key-chain; edit <KEYCHAIN>; config key; edit 1; set key-string <KEY>; set algorithm hmac-sha256; set accept-lifetime <LIFETIME>; set send-lifetime <LIFETIME>; next; end; next; end` |
| Core: Routing | BGP neighbors (passwords, maximum prefixes, inbound prefix lists) | 7.0.0 or earlier | RTR `SRG-NET-000230-RTR-000002`; RTR `SRG-NET-000362-RTR-000117`; RTR `SRG-NET-000018-RTR-000002`; RTR `SRG-NET-000018-RTR-000003` | `config router bgp; config neighbor; edit <NEIGHBOR_IP>; set password <PASSWORD>; set maximum-prefix <NUMBER>; set prefix-list-in <PREFIX_LIST>; next; end; end` |
| Core: High availability | FGCP high availability clusters (heartbeat authentication and encryption) | 7.0.0 or earlier | FGT-NDM `FGFW-ND-000200` | `config system ha; set authentication enable; set encryption enable; end` |
| Core: Central management | Central management by FortiManager (configuration backups and revision history) | 7.0.0 or earlier | FGT-NDM `FGFW-ND-000180`; FGT-NDM `FGFW-ND-000185` | `config system central-management; set type fortimanager; set fmg <FMG_IP>; end` |
| GUI | FortiView application bandwidth widget | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| GUI | SSL-VPN and IPsec monitor improvements | 7.0.0 and later | VPN `SRG-NET-000492-VPN-001980` | — |
| GUI | New themes and CLI console enhancements | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| GUI | Add options for API Preview, Edit in CLI, and References | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| GUI | GUI usability enhancements | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| GUI | Seven-day rolling counter for policy hit counters | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| GUI | FortiGate administrator log in using FortiCloud single sign-on | 7.0.0 and later | FGT-NDM `FGFW-ND-000030`; FGT-NDM `FGFW-ND-000165` | `config system global; set admin-forticloud-sso-login disable; end` (unless FortiCloud SSO is approved for administrators) |
| GUI | Navigation menu updates | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| GUI | UX improvements for objects | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| GUI | Interface migration wizard | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| GUI | GUI-based global search | 7.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| GUI | DNS status widget | 7.0.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| GUI | Export firewall policy list to CSV and JSON formats | 7.0.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| GUI | GUI support for configuration save mode | 7.0.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| GUI | Add real-time FortiView monitors for proxy traffic | 7.0.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| GUI | GUI support for DSL settings | 7.0.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| GUI | Automatically enable FortiCloud single sign-on after product registration | 7.0.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| GUI | Process monitor | 7.0.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| GUI | Loading artifacts from a CDN for improved GUI performance | 7.0.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| GUI | Look up IP address information from the Internet Service Database page | 7.2.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| GUI | Embed real-time packet capture and analysis tool on Diagnostics page | 7.2.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| GUI | Embed real-time debug flow tool on Diagnostics page | 7.2.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| GUI | Display detailed FortiSandbox analysis and downloadable PDF report | 7.2.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| GUI | Display LTE modem configuration on GUI of FG-40F-3G4G model | 7.2.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| GUI | Update naming of FortiCare support levels | 7.2.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| GUI | Enforce FortiCare registration after new GUI login | 7.2.11+; 7.4.8+; 7.6.5+ | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| GUI | Updated Dashboard and FortiView | 7.4.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| GUI | Accessing additional support resources | 7.4.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| GUI | Run simultaneous packet captures and use the command palette | 7.4.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| GUI | Update FortiSandbox Files FortiView monitor | 7.4.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| GUI | Combine the Device Inventory widget and Asset Identity Center page | 7.4.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| GUI | GUI enhancements for FortiGuard DLP service | 7.4.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| GUI | FortiConverter usability improvements | 7.4.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| GUI | Update FortiGuard License Information widget | 7.4.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| GUI | Optimize policy and objects pages and dialogs | 7.4.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| GUI | Indicate Special Technical Support builds | 7.4.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| GUI | Support filtering on policy list statistics | 7.4.8+; 7.6.4+ | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| GUI | Enforce FortiCare registration with read-only CLI | 7.4.9+; 7.6.5+ | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| GUI | Enhanced setup wizard for networking connectivity support | 7.4.10+; 7.6.5+ | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| GUI | Seven-day setup period for GUI and CLI configuration | 7.4.10+; 7.6.7+; 8.0.0+ | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| GUI | GUI support for local-in policies | 7.6.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| GUI | GUI support for internet service groups | 7.6.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| GUI | GUI displays logic between firewall policy objects | 7.6.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| GUI | GUI support to create policies in FortiView Sources and traffic logs | 7.6.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| GUI | GUI improvements to device upgrade | 7.6.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| GUI | GUI support for enhanced logging for threat feeds | 7.6.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| GUI | Expanded support for Advanced Threat Protection Statistics widget | 7.6.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| GUI | GUI improvements to the IPsec VPN Wizard | 7.6.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| GUI | GUI improvements to Security Rating | 7.6.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| GUI | GUI support for web proxy forward server over IPv6 | 7.6.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| GUI | GUI support for security posture tags in dial-up IPsec VPN tunnels | 7.6.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| GUI | CLI diagnostic shortcuts in the GUI | 7.6.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| GUI | Asset Details pane | 7.6.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| GUI | GUI access for global search | 7.6.3 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| GUI | GUI warnings for IKE-TCP port conflicts | 7.6.3 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| GUI | GUI improvements of PIM support for VRFs | 7.6.3 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| GUI | Enhanced security rating tooltip controls | 7.6.5 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| GUI | Summary panel in Log Details | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| GUI | GUI support for preferred outbound route map options | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| GUI | VDOM selection for Central Management in the GUI | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| GUI | GUI support for configuring proxy ARP on VLAN interface | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| GUI | Improve switch management | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| GUI | Display Known Exploited Vulnerabilities from FortiClient | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| GUI | Custom GUI themes and admin‑level personalization | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| GUI | Enhanced GUI support for Inline-CASB SaaS Application | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| GUI | Enhance Security Fabric topology performance with lazy loading | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| GUI | Dashboard and monitor unification | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| GUI | Graphical display for application performance monitoring analytics | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| GUI | Feature Visibility page redesign | 8.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| GUI | GUI notification center for hardware and operational alerts | 8.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| GUI | Interactive FortiView Applications and AI Applications dashboards | 8.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Usability enhancements to SD-WAN Network Monitor service | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Hold down time to support SD-WAN service strategies | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Passive WAN health measurement | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Summarize source IP usage on the Local Out Routing page | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Add option to select source interface and address for Telnet and SSH | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | ECMP routes for recursive BGP next hop resolution | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | BGP next hop recursive resolution using other BGP routes | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Add SNMP OIDs for shaping-related statistics | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | PRP handling in NAT mode with virtual wire pair | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | NetFlow on FortiExtender and tunnel interfaces | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Integration with carrier CPE management tools | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Use file filter rules in sniffer policy | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Explicit mode with DoT and DoH | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | GUI advanced routing options for BGP | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | GUI page for OSPF settings | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | GUI routing monitor for BGP and OSPF | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Multicast and broadcast packet counters | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Configuring IPv6 multicast policies in the GUI | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | GUI support for configuring IPv6 | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | FortiGate as an IPv6 DDNS client for generic DDNS | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | FortiGate as an IPv6 DDNS client for FortiGuard DDNS | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Allow backup and restore commands to use IPv6 addresses | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Explicit proxy authentication over HTTPS | 7.0.0 and later | ALG `SRG-NET-000400-ALG-000097`; ALG `SRG-NET-000138-ALG-000063` | — |
| Network | Selectively forward web requests to a transparent web proxy | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | SD-WAN passive health check configurable on GUI | 7.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | ECMP support for the longest match in SD-WAN rule matching | 7.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Override quality comparisons in SD-WAN longest match rule matching | 7.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Specify an SD-WAN zone in static routes and SD-WAN rules | 7.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Display ADVPN shortcut information in the GUI | 7.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Speed tests run from the hub to the spokes in dial-up IPsec tunnels | 7.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Interface based QoS on individual child tunnels based on speed test results | 7.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | OSPF HMAC-SHA authentication | 7.0.1 and later | RTR `SRG-NET-000168-RTR-000078`; RTR `SRG-NET-000230-RTR-000001` | `config router ospf; config ospf-interface; edit <NAME>; set interface <PORT>; set authentication message-digest; set keychain <KEYCHAIN>; next; end; end`; `config router key-chain; edit <KEYCHAIN>; config key; edit 1; set key-string <KEY>; set algorithm hmac-sha256; set accept-lifetime <LIFETIME>; set send-lifetime <LIFETIME>; next; end; next; end` |
| Network | BGP conditional advertisement for IPv6 | 7.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Enable or disable updating policy routes when link health monitor fails | 7.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Add weight setting on each link health monitor server | 7.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Enhanced hashing for LAG member selection | 7.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | VRF support for IPv6 | 7.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | mTLS client certificate authentication | 7.0.1 and later | ALG `SRG-NET-000164-ALG-000100` | — |
| Network | WAN optimization SSL proxy chaining | 7.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Passive health-check measurement by internet service and application | 7.0.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Adaptive Forward Error Correction | 7.0.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Add GPS coordinates to REST API monitor output for FortiExtender and LTE modems | 7.0.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | BGP error handling per RFC 7606 | 7.0.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Configure IPAM locally on the FortiGate | 7.0.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | IPv6 tunnel inherits MTU based on physical interface | 7.0.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Use DNS over TLS for default FortiGuard DNS servers | 7.0.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Accept multiple conditions in BGP conditional advertisements | 7.0.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Enhanced BGP next hop updates and ADVPN shortcut override | 7.0.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Allow per-prefix network import checking in BGP | 7.0.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Support QinQ 802.1Q in 802.1Q for FortiGate VMs | 7.0.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Allow only supported FEC implementations on 10G, 25G, 40G, and 100G interfaces | 7.0.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Support 802.1X on virtual switch for certain NP6 platforms | 7.0.6+; 7.2.0+ | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | SNMP OIDs for port block allocations IP pool statistics | 7.0.6+; 7.2.0+ | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Support cross-VRF local-in and local-out traffic for local services | 7.0.6+; 7.2.1+ | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | BFD for multihop path for BGP | 7.0.6+; 7.2.0+ | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Support CORS protocol in explicit web proxy when using session-based, cookie-enabled, and captive portal-enabled SAML authentication | 7.0.6+; 7.2.1+ | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Allow application category as an option for SD-WAN rule destination | 7.2.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Add mean opinion score calculation and logging in performance SLA health checks | 7.2.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Multiple members per SD-WAN neighbor configuration | 7.2.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Duplication on-demand when SLAs in the configured service are matched | 7.2.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | SD-WAN in large scale deployments | 7.2.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | SD-WAN segmentation over a single overlay | 7.2.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Add NetFlow fields to identify class of service | 7.2.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | OSPF graceful restart on topology change | 7.2.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | OSPFv3 graceful restart for OSPF6 | 7.2.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Configuring a FortiGate interface to act as an 802.1X supplicant | 7.2.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Increase the number of VRFs per VDOM | 7.2.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Configuring IPv4 over IPv6 DS-Lite service | 7.2.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | NAT46 and NAT64 for SIP ALG | 7.2.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Embedded SD-WAN SLA information in ICMP probes | 7.2.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Exchange underlay link cost property with remote peer in IPsec VPN phase 1 negotiation | 7.2.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Copying the DSCP value from the session original direction to its reply direction | 7.2.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | GUI support for advanced BGP options | 7.2.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Support BGP AS number input in asdot and asdot+ format | 7.2.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | SNMP OIDs with details about authenticated users | 7.2.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Add new IPAM GUI page | 7.2.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Assign multiple IP pools and subnets using IPAM Rules | 7.2.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Add VCI pattern matching as a condition for IP or DHCP option assignment | 7.2.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | FortiGate as FortiGate LAN extension | 7.2.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Send Netflow traffic to collector in IPv6 | 7.2.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | IPv6 feature parity with IPv4 static and policy routes | 7.2.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | HTTPS download of PAC files for explicit proxy | 7.2.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Matching BGP extended community route targets in route maps | 7.2.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | SD-WAN application monitor using FortiMonitor | 7.2.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Add Fabric Overlay Orchestrator for SD-WAN overlay configurations | 7.2.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Allow VLAN sub-interfaces to be used in virtual wire pairs | 7.2.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Add static route tag and BGP neighbor password | 7.2.4 and later | RTR `SRG-NET-000230-RTR-000002` | `config router bgp; config neighbor; edit <NEIGHBOR_IP>; set password <PASSWORD>; set maximum-prefix <NUMBER>; set prefix-list-in <PREFIX_LIST>; next; end; end` |
| Network | DHCP enhancements | 7.2.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Improve DVLAN QinQ performance for NP7 platforms over virtual wire pairs | 7.2.5+; 7.4.0+ | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Improve client-side settings for SD-WAN network monitor | 7.2.6+; 7.4.1+ | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Support BGP graceful restart helper-only mode | 7.2.8+; 7.4.2+ | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Allow multiple Netflow collectors | 7.2.8+; 7.4.2+ | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Handling IPv4 SCTP packets with zero checksum on the NP7 platform | 7.2.8+; 7.4.4+ | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Using MP-BGP EVPN with VXLAN | 7.4.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Add route tag address objects | 7.4.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Configuring a DHCP shared subnet | 7.4.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Configuring DHCP smart relay on interfaces with a secondary IP | 7.4.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Active SIM card switching available on FortiGates with cellular modem and dual SIM card support | 7.4.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | LAG interface status signaled to peer when available links fall below min-link | 7.4.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Configuring multiple DDNS entries in the GUI | 7.4.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | BGP conditional advertisements for IPv6 prefix when IPv4 prefix conditions are met and vice-versa | 7.4.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Changing the FTP mode from active to passive for explicit proxy | 7.4.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Configuring a secure explicit proxy | 7.4.0 and later | ALG `SRG-NET-000062-ALG-000150`; ALG `SRG-NET-000400-ALG-000097` | — |
| Network | Explicit proxy logging enhancements | 7.4.0 and later | ALG `SRG-NET-000074-ALG-000043` | — |
| Network | Support DHCP client mode for inter-VDOM links | 7.4.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Configuring FortiGate LAN extension the GUI | 7.4.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Transparent conditional DNS forwarder | 7.4.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | IPAM enhancements | 7.4.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | DNS over QUIC and DNS over HTTP3 for transparent and local-in DNS modes | 7.4.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Enhancement to QUIC and HTTP3 inspection | 7.4.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Interfaces in non-management VDOMs as the source IP address of the DNS conditional forwarding server | 7.4.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | FortiGate 3G4G: improved dual SIM card switching capabilities | 7.4.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Cellular interface of FortiGate-40F-3G4G supports IPv6 | 7.4.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Connectivity Fault Management supported for network troubleshooting | 7.4.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Support LTE / BLE airplane mode for FGR-70F-3G4G | 7.4.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Support the Happy Eyeballs algorithm for explicit proxy | 7.4.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Support webpages to properly display CORS content in an explicit proxy environment | 7.4.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Forward HTTPS requests to a web server without the need for an HTTP CONNECT message | 7.4.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Support web proxy forward server over IPv6 | 7.4.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | BGP incorporates the advanced security measures of TCP Authentication Option (TCP-AO) | 7.4.2 and later | RTR `SRG-NET-000230-RTR-000002`; RTR `SRG-NET-000168-RTR-000078` | — |
| Network | Allow multiple sFlow collectors | 7.4.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Enhance persistent packet capture | 7.4.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Support for LAN extension VDOM simplifications | 7.4.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Enhance port-level control for STP and 802.1x authentication | 7.4.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Allow backup customization for DHCP leases during power cycles | 7.4.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Assign multiple remote Autonomous Systems to a single BGP neighbor group | 7.4.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Upgrade LTE modem firmware directly from FortiGuard | 7.4.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Support RADIUS Vendor-Specific Attributes for captive portal redirects | 7.4.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | GUI support for DNS over QUIC and DNS over HTTP3 for transparent and local-in DNS modes | 7.4.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Store packet capture criteria | 7.4.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Support for inspection of 802.1ah packet headers in virtual wire pairs | 7.4.5 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Including denied multicast sessions in the session table | 7.4.5+; 7.6.1+ | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Add support for 802.1X on a virtual switch when added to a software switch | 7.4.10+; 7.6.5+ | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Configure the VRRP hello timer in milliseconds | 7.6.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | FortiGate as a recursive DNS resolver | 7.6.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | BGP network prefixes utilize firewall addresses and groups | 7.6.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Support UDP-Lite traffic | 7.6.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Custom LSA refresh rates and fast link-down detection on VLAN interfaces for OSPF | 7.6.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Filter NetFlow sampling | 7.6.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | SOCKS proxy supports UTM scanning, authentication, and forward server | 7.6.0 and later | ALG `SRG-NET-000131-ALG-000086` | — |
| Network | Implement the interface name as the source IP address in RADIUS, LDAP, and DNS configurations | 7.6.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Include groups in PIM join/prune messages | 7.6.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Automatic LTE connection establishment | 7.6.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Netflow sampling | 7.6.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Support source-IP interface for system DNS database | 7.6.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Fortinet Support Tool for capturing incidents | 7.6.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | DHCPv6 enhancements | 7.6.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Recursive resolution of BGP routes using IPv6 prefix with on-link flag from route aggregation | 7.6.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Extended VRF ID range for enhanced network scalability | 7.6.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Enhanced PIM support for VRFs | 7.6.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Support specific VRF ID for local-out traffic | 7.6.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Support source IP interface for system DNS | 7.6.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Improvements to IPsec monitoring | 7.6.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Enhancing SIP reliability in 464XLAT environments | 7.6.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Specifying outgoing interface and VRF for a web proxy forward server or isolator server | 7.6.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Isolator servers in proxy policies | 7.6.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Connectivity Fault Management (CFM) now available for FG-80F-POE and FG-20xF models | 7.6.3 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Application and network performance monitoring with FortiTelemetry | 7.6.3 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Support configuring users and groups in policy routes | 7.6.3 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | GUI support of isolator servers for proxy policies | 7.6.3 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Support additional NIC interface diagnostics | 7.6.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Auto speed negotiation for 10G Base-T on FortiGate 100xF devices | 7.6.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | GUI support for 5G modem management | 7.6.7+; 8.0.1+ | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | IPv6 Multicast Routing Enhancement with BSR Support Added | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | BGP neighbor naming support | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Increased AS path item for BGP route maps | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | IPv6 PCP support for DNAT46 in NAT64 deployments | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Customizable CoS marking for locally generated ARP packets | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Firewall address support for IPAM rules | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Graceful BGP shutdown | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | TCP congestion control enhancement with BBR | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Session helper statistics | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Enhanced EVPN support for VXLAN Anycast gateway and type-5 routing | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Enhanced PIM support for IPv6 across all VRFs | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | GPON support for FortiGates with SFP/SFP+ ports | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | 802.1X, MAB, dynamic VLAN, and address object support for software switch | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Dynamic BGP learning of ISDB reputation IPs | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | IPAM DHCP templates | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Enhanced multicast session key for virtual wire pair | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Next hop self-support for VPNv4 and VPNv6 route reflectors | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | External GNSS antenna support for improved GPS accuracy on FWF-50G-5G | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | DHCP IP assignment based on MAC vendor OUI | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Support CoS marking for FortiGate DHCP client requests | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | IPv6 Link-local configuration enhancement | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | IPv6 proxy address and address group object support | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Secure explicit proxy with client certificate blocklist enforcement | 8.0.0 and later | ALG `SRG-NET-000164-ALG-000100` | — |
| Network | Add VRF name support | 8.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Support link sync group (bidirectional fail detection) | 8.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Support manual MAC address config for VLAN and software switch interfaces | 8.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Support BGP large communities | 8.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | BGP RPKI route origin validation | 8.0.1 and later | RTR `SRG-NET-000018-RTR-000001` | — |
| Network | OBM USB serial console support for FGR-70F/70G series | 8.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Source MAC address retrieval via DHCP Lease Query | 8.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Captive Portal API support | 8.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Network | Monitor device status using monitoring profile | 8.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| SD-WAN | Using a single IKE selector in ADVPN to match all SD-WAN control plane traffic | 7.4.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| SD-WAN | Add option to keep sessions in established ADVPN shortcuts while they remain in SLA | 7.4.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| SD-WAN | Allow better control over the source IP used by each egress interface for local out traffic | 7.4.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| SD-WAN | Logging FortiMonitor-detected performance metrics | 7.4.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| SD-WAN | Classifying SLA probes for traffic prioritization | 7.4.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| SD-WAN | VRF-aware SD-WAN IPv6 health checks | 7.4.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| SD-WAN | Support maximize bandwidth (SLA) to load balance spoke-to-spoke traffic between multiple ADVPN shortcuts | 7.4.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| SD-WAN | Support IPv6 application based steering in SD-WAN | 7.4.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| SD-WAN | Allow SD-WAN to steer multicast traffic | 7.4.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| SD-WAN | Support the new SD-WAN Overlay-as-a-Service | 7.4.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| SD-WAN | SD-WAN multi-PoP multi-hub large scale design and failover | 7.4.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| SD-WAN | Active dynamic BGP neighbor triggered by ADVPN shortcut | 7.4.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| SD-WAN | Support HTTPS performance SLA health checks | 7.4.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| SD-WAN | Using load balancing in a manual SD-WAN rule without configuring an SLA target | 7.4.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| SD-WAN | IPv6 support for SD-WAN segmentation over a single overlay | 7.4.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| SD-WAN | SD-WAN hub and spoke speed test improvements | 7.4.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| SD-WAN | ADVPN 2.0 edge discovery and path management | 7.4.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| SD-WAN | Support an OaaS agent for uninterrupted spoke traffic | 7.4.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| SD-WAN | Fabric Overlay Orchestrator SPA easy configuration key for FortiSASE | 7.4.5 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| SD-WAN | Create default configuration of SD-WAN on FortiGate models with two WAN ports | 7.4.9+; 7.6.5+ | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| SD-WAN | ADVPN 2.0 enhancements | 7.6.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| SD-WAN | Embed SLA priorities in ICMP probes | 7.6.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| SD-WAN | Embed SLA status in ICMP probes | 7.6.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| SD-WAN | Allow SD-WAN rules to steer IPv6 multicast traffic | 7.6.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| SD-WAN | ADVPN 2.0 overlay placeholders for shortcuts between spokes | 7.6.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| SD-WAN | SD-WAN Setup wizard for guided configuration | 7.6.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| SD-WAN | Map SD-WAN member priorities to BGP MED attribute when spoke advertises routes using iBGP to hub | 7.6.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| SD-WAN | FortiGuard SLA database for SD-WAN performance SLA | 7.6.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| SD-WAN | Passive monitoring of TCP metrics | 7.6.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| SD-WAN | Specify SD-WAN zones in some policies | 7.6.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| SD-WAN | Fabric Overlay Orchestrator Topology dashboard widget for hub FortiGates | 7.6.3 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| SD-WAN | Application performance monitoring | 7.6.3 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| SD-WAN | Hub-to-spoke traffic shaping by IKE bandwidth negotiation | 7.6.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| SD-WAN | ADVPN 2.0 enhancement: trigger just one shortcut for each distinct underlay path | 7.6.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| SD-WAN | ADVPN spoke-to-spoke traffic shaping by IKE bandwidth negotiation | 7.6.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| SD-WAN | Hybrid strategy for service rules | 7.6.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| SD-WAN | Allow SD-WAN hubs to suppress BGP routes when all links to a spoke are down | 7.6.5 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| SD-WAN | SD-WAN speed test enhancements 1 | 7.6.5 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| SD-WAN | SD-WAN speed test enhancements 2 | 7.6.5 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| SD-WAN | IPv6 probe-response through interface configuration | 7.6.5 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| SD-WAN | Support for PIM using unaddressed IPsec interfaces | 7.6.7+; 8.0.1+ | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| SD-WAN | SD-WAN underlay bandwidth steers traffic | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| SD-WAN | ToS-based SD-WAN duplication matching | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| SD-WAN | Stop packet duplication upon reaching bandwidth utilization threshold | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| SD-WAN | Selective SD-WAN duplication | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| SD-WAN | Use secondary tunnel for FEC redundant parity packets | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| SD-WAN | ToS matching and negate options on adaptive FEC profiles | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| SD-WAN | Control SD-WAN interface usage based on monthly traffic volume (quota) | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| SD-WAN | Confine packet duplication across multiple overlays to the same spoke | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| SD-WAN | On-demand duplication at the Hub using remote health-check | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| SD-WAN | Fabric Overlay Orchestrator IPAM integration | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| SD-WAN | SD-WAN speed test scheduling improvements | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| SD-WAN | Support for IKE phase 1 priority option on static gateways | 8.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| SD-WAN | SD-WAN health-check MTU awareness | 8.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| SD-WAN | SD-WAN performance SLA HTTPS support for IPv6 | 8.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| SD-WAN | Weight-based-spillover load-balancing algorithm support | 8.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| SD-WAN | Spillover load-balancing algorithm support | 8.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| SD-WAN | FortiExtender integration with SD-WAN | 8.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Policy and objects | Zero Trust Network Access introduction | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Policy and objects | Basic ZTNA configuration | 7.0.0 and later | ALG `SRG-NET-000138-ALG-000063`; ALG `SRG-NET-000018-ALG-000017` | — |
| Policy and objects | Establish device identity and trust context with FortiClient EMS | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Policy and objects | SSL certificate based authentication | 7.0.0 and later | ALG `SRG-NET-000164-ALG-000100`; ALG `SRG-NET-000138-ALG-000063` | — |
| Policy and objects | ZTNA configuration examples | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Policy and objects | Migrating from SSL VPN to ZTNA HTTPS access proxy | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Policy and objects | ZTNA troubleshooting and debugging | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Policy and objects | Filters for application control groups in NGFW mode | 7.0.0 and later | ALG `SRG-NET-000018-ALG-000017` | — |
| Policy and objects | DNS health check monitor for server load balancing | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Policy and objects | Carrier-grade NAT | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Policy and objects | Allow multiple virtual wire pairs in a virtual wire pair policy | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Policy and objects | Record central NAT and DNAT hit count | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Policy and objects | MAC address wildcard in firewall address | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Policy and objects | ZTNA logging enhancements | 7.0.1 and later | ALG `SRG-NET-000074-ALG-000043` | — |
| Policy and objects | Simplify NAT46 and NAT64 policy and routing configurations | 7.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Policy and objects | Cisco Security Group Tag as policy matching criteria | 7.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Policy and objects | Allow VIPs to be enabled or disabled in central NAT mode | 7.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Policy and objects | Logical AND for ZTNA tag matching | 7.0.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Policy and objects | Implicitly generate a firewall policy for a ZTNA rule | 7.0.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Policy and objects | Posture check verification for active ZTNA proxy session | 7.0.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Policy and objects | GUI support for multiple ZTNA features | 7.0.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Policy and objects | Increase ZTNA and EMS tag limits | 7.0.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Policy and objects | Use FQDN with ZTNA TCP forwarding access proxy | 7.0.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Policy and objects | UTM scanning on TCP forwarding access proxy traffic | 7.0.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Policy and objects | Connect a ZTNA access proxy to an SSL VPN web portal | 7.0.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Policy and objects | ZTNA FortiView and log enhancements | 7.0.4 and later | ALG `SRG-NET-000074-ALG-000043` | — |
| Policy and objects | ZTNA session-based form authentication | 7.0.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Policy and objects | Using the IP pool or client IP address in a ZTNA connection to backend servers | 7.0.6+; 7.2.0+ | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Policy and objects | ZTNA scalability support for up to 50 thousand concurrent endpoints | 7.2.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Policy and objects | Allow web filter category groups to be selected in NGFW policies | 7.2.0 and later | ALG `SRG-NET-000019-ALG-000018` | — |
| Policy and objects | Add option to set application default port as a service port | 7.2.0 and later | ALG `SRG-NET-000132-ALG-000087` | — |
| Policy and objects | Introduce learn mode in security policies in NGFW mode | 7.2.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Policy and objects | Adding traffic shapers to multicast policies | 7.2.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Policy and objects | Add Policy change summary and Policy expiration to Workflow Management | 7.2.0 and later | FGT-NDM `FGFW-ND-000150` | — |
| Policy and objects | Allow empty address groups | 7.2.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Policy and objects | Remove overlap check for VIPs | 7.2.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Policy and objects | ZTNA device certificate verification from EMS for SSL VPN connections | 7.2.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Policy and objects | Publishing ZTNA services through the ZTNA portal | 7.2.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Policy and objects | ZTNA inline CASB for SaaS application access control | 7.2.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Policy and objects | ZTNA policy access control of unmanaged devices | 7.2.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Policy and objects | HTTP2 connection coalescing and concurrent multiplexing for ZTNA, virtual server load balancing, and explicit proxy | 7.2.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Policy and objects | ZTNA policy access control of unmanageable and unknown devices with dynamic address local tags | 7.2.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Policy and objects | Virtual patching on the local-in management interface | 7.2.4 and later | FGT-NDM `FGFW-ND-000290`; IDPS `SRG-NET-000019-IDPS-00019` | — |
| Policy and objects | Using IPv6 addresses in the ISDB | 7.2.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Policy and objects | Add ISDB on-demand mode to reduce the size stored on the flash drive | 7.2.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Policy and objects | Enabling the ISDB cache in the FortiOS kernel | 7.2.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Policy and objects | Add the Any and All options back for ZTNA tags in the GUI | 7.2.6 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Policy and objects | Support destination port matching of central SNAT rules | 7.2.8+; 7.4.0+ | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Policy and objects | Add scanunit support for learning mode | 7.4.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Policy and objects | Support the Port Control Protocol | 7.4.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Policy and objects | Improve the performance of the GUI policy list | 7.4.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Policy and objects | Process Ethernet frames with Cisco Security Group Tag and VLAN tag | 7.4.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Policy and objects | Support port block allocation for NAT64 | 7.4.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Policy and objects | Increase the number of supported dynamic FSSO IP addresses | 7.4.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Policy and objects | Traffic shaping extensions | 7.4.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Policy and objects | Support dynamic Fabric address in security policies | 7.4.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Policy and objects | Support refreshing active sessions for specific protocols and port ranges per VDOM in a specified direction | 7.4.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Policy and objects | Update policy lookup tool with policy match tool | 7.4.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Policy and objects | Policy list enhancements | 7.4.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Policy and objects | Unified Policy name and ID column | 7.4.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Policy and objects | Support IPS inspection for multicast UDP traffic | 7.4.2 and later | IDPS `SRG-NET-000390-IDPS-00212` | — |
| Policy and objects | Optimize virtual patching on the local-in interface | 7.4.2 and later | FGT-NDM `FGFW-ND-000290` | — |
| Policy and objects | Stripping the X-Forwarded-For value in the HTTP header | 7.4.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Policy and objects | Enhanced logging for NAT persistent sessions utilizing PBA | 7.4.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Policy and objects | Fine-tuning source port behavior for SNAT | 7.4.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Policy and objects | Internet service as source addresses in the local-in policy | 7.4.4 and later | FGT-NDM `FGFW-ND-000200` | — |
| Policy and objects | DSCP marking for self-generated traffic | 7.4.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Policy and objects | Seven-day policy hit counter | 7.6.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Policy and objects | NPTv6 protocol for IPv6 address translation | 7.6.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Policy and objects | MAP-E supports multiple VNE interfaces in the same VDOM | 7.6.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Policy and objects | Full cone NAT for fixed port range IP pools | 7.6.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Policy and objects | Custom port ranges for PBA and FPR IP pools | 7.6.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Policy and objects | HTTP transaction logging | 7.6.0 and later | ALG `SRG-NET-000074-ALG-000043` | — |
| Policy and objects | Support for NAT64 in FPR IP pools | 7.6.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Policy and objects | Support for randomized port selection in IP pool mechanisms | 7.6.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Policy and objects | Enhanced security with default local-in policy | 7.6.1 and later | FGT-NDM `FGFW-ND-000200`; RTR `SRG-NET-000205-RTR-000001` | — |
| Policy and objects | DHCP-PD support for MAP-E | 7.6.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Policy and objects | RSSO dynamic address subtype | 7.6.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Policy and objects | New ISDB record for SOCaaS | 7.6.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Policy and objects | Apply FQDN address groups within the ISDB | 7.6.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Policy and objects | GUI support for FQDN address groups within the ISDB | 7.6.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Policy and objects | Dynamic telemetry firewall address type | 7.6.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Policy and objects | IPv6 wildcard addresses | 7.6.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Policy and objects | NGFW policy support for FQDN address groups in the ISDB | 7.6.5 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Policy and objects | Upstream SSL/TLS support for virtual load-balancing servers | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Policy and objects | Custom tags for addresses, policies, and dynamic tag address groups | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Policy and objects | Improved virtual IP ordering and Security Rating insights | 8.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Policy and objects | Initial Firewall Policy Setup wizard | 8.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Zero Trust Network Access | Support logical AND for tag matching between primary and secondary EMS tags in a firewall policy | 7.4.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Zero Trust Network Access | Support sending the FortiGate interface subnet list to EMS | 7.4.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Zero Trust Network Access | Introduce simplified ZTNA rules within firewall policies | 7.4.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Zero Trust Network Access | Introduce new ZTNA replacement message types | 7.4.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Zero Trust Network Access | Condense ZTNA server mapping configurations | 7.4.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Zero Trust Network Access | Introduce Fabric integration with FortiGSLB | 7.4.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Zero Trust Network Access | Add the Any and All options back for security posture tags in the GUI | 7.4.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Zero Trust Network Access | Rename ZTNA Tag to Security Posture Tag in the GUI | 7.4.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Zero Trust Network Access | Share ZTNA application configurations with FortiClient EMS | 7.4.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Zero Trust Network Access | Dynamic interface IP addresses for access proxy VIPs | 7.4.5 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Zero Trust Network Access | Share ZTNA information through the EMS connector | 7.6.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Zero Trust Network Access | ZTNA support for UDP traffic | 7.6.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Zero Trust Network Access | ZTNA support for SaaS application access control in the GUI | 7.6.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Zero Trust Network Access | Include EMS tag information in traffic logs | 7.6.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Zero Trust Network Access | ZTNA agentless web-based application access | 7.6.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Zero Trust Network Access | ZTNA single sign-on with Entra ID | 7.6.3 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Zero Trust Network Access | ZTNA tags on 2 GB entry-level platforms in IP/MAC-based access control | 7.6.3 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Zero Trust Network Access | Extend ZTNA error codes and replacement messages | 7.6.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Zero Trust Network Access | Share used security posture tags with EMS | 7.6.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Zero Trust Network Access | ZTNA configuration simplification | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Zero Trust Network Access | ZTNA service connector | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Zero Trust Network Access | Support tags in dual stack IPv4/IPv6 ZTNA policies | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security profiles | Stream-based antivirus scan in proxy mode for FTP, SFTP, and SCP | 7.0.0 and later | ALG `SRG-NET-000248-ALG-000133` | — |
| Security profiles | Configure threat feed and outbreak prevention without AV engine scan | 7.0.0 and later | ALG `SRG-NET-000249-ALG-000134` | — |
| Security profiles | AI-based malware detection | 7.0.0 and later | ALG `SRG-NET-000248-ALG-000133` | — |
| Security profiles | Malware threat feed from EMS | 7.0.0 and later | ALG `SRG-NET-000249-ALG-000134` | — |
| Security profiles | Application signature dissector for DNP3 | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security profiles | FortiGuard web filter categories to block child sexual abuse and terrorism | 7.0.0 and later | ALG `SRG-NET-000019-ALG-000018` | — |
| Security profiles | Enhance web filter antiphishing profile | 7.0.0 and later | ALG `SRG-NET-000019-ALG-000018` | — |
| Security profiles | Highlight on hold IPS signatures | 7.0.0 and later | IDPS `SRG-NET-000019-IDPS-00187` | — |
| Security profiles | HTTP/2 support in proxy mode SSL inspection | 7.0.0 and later | ALG `SRG-NET-000062-ALG-000150` | — |
| Security profiles | Define multiple certificates in an SSL profile in replace mode | 7.0.0 and later | ALG `SRG-NET-000062-ALG-000150` | — |
| Security profiles | Support secure ICAP clients | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security profiles | Add TCP connection pool for connections to ICAP server | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security profiles | Improve WAD traffic dispatcher | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security profiles | Video filtering | 7.0.0 and later | ALG `SRG-NET-000019-ALG-000018` | — |
| Security profiles | DNS filter handled by IPS engine in flow mode | 7.0.0 and later | ALG `SRG-NET-000019-ALG-000018` | — |
| Security profiles | DNS inspection with DoT and DoH | 7.0.0 and later | ALG `SRG-NET-000391-ALG-000140` | — |
| Security profiles | Flow-based SIP inspection | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security profiles | FortiAI inline blocking and integration with an AV profile | 7.0.1 and later | ALG `SRG-NET-000249-ALG-000134` | — |
| Security profiles | Extend SCTP filtering capabilities | 7.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security profiles | Add categories for URL shortening, crypto mining, and potentially unwanted programs | 7.0.2 and later | ALG `SRG-NET-000019-ALG-000018` | — |
| Security profiles | Scanning MSRP traffic | 7.0.2 and later | ALG `SRG-NET-000248-ALG-000133` | — |
| Security profiles | Support full extended IPS database for CP9 models and slim extended database for other physical models | 7.0.6+; 7.2.0+ | IDPS `SRG-NET-000362-IDPS-00198` | — |
| Security profiles | Allow the YouTube channel override action to take precedence | 7.0.6+; 7.2.1+ | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security profiles | Support full extended IPS database for FortiGate VMs with eight cores or more | 7.0.11+; 7.2.5+; 7.4.0+ | IDPS `SRG-NET-000362-IDPS-00198` | — |
| Security profiles | FortiSandbox inline scanning | 7.2.0 and later | ALG `SRG-NET-000249-ALG-000134` | — |
| Security profiles | Using the Websense Integrated Services Protocol in flow mode | 7.2.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security profiles | Inspecting HTTP3 traffic | 7.2.0 and later | ALG `SRG-NET-000390-ALG-000139` | — |
| Security profiles | IPS sensor entry filters | 7.2.0 and later | IDPS `SRG-NET-000019-IDPS-00019` | — |
| Security profiles | Add email filters for block allow lists | 7.2.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security profiles | Enhance the DLP backend and configurations | 7.2.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security profiles | Add option to disable the FortiGuard IP address rating | 7.2.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security profiles | ICAP scanning with SCP and FTP | 7.2.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security profiles | Inline scanning with FortiGuard AI-Based Sandbox Service | 7.2.1 and later | ALG `SRG-NET-000249-ALG-000134` | — |
| Security profiles | Add persistency for banned IP list | 7.2.1 and later | IDPS `SRG-NET-000019-IDPS-00019` | — |
| Security profiles | Reduce memory usage on FortiGate models with 2 GB RAM or less by not running WAD processes for unused proxy features | 7.2.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security profiles | Antivirus exempt list for files based on individual hash | 7.2.4 and later | ALG `SRG-NET-000248-ALG-000133` | — |
| Security profiles | Add REST API for IPS session monitoring | 7.2.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security profiles | Hide proxy features in the GUI by default for models with 2 GB RAM or less | 7.2.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security profiles | Re-introduce DLP profiles in the GUI | 7.2.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security profiles | Remove option to block QUIC by default in application control | 7.2.4 and later | ALG `SRG-NET-000390-ALG-000139` | — |
| Security profiles | Improve replacement message displayed in blocked videos | 7.2.5+; 7.4.0+ | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security profiles | Introduce SIP IPS profile as a complement to SIP ALG | 7.2.5+; 7.4.0+ | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security profiles | Support the Zstandard compression algorithm for web content | 7.2.9+; 7.4.5+; 7.6.0+ | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security profiles | Support OT and IoT virtual patching on NAC policies | 7.4.0 and later | IDPS `SRG-NET-000019-IDPS-00019` | — |
| Security profiles | Download quarantined files in archive format | 7.4.1 and later | ALG `SRG-NET-000249-ALG-000145` | — |
| Security profiles | Add FortiGuard web filter categories for AI and cryptocurrency | 7.4.1 and later | ALG `SRG-NET-000019-ALG-000018` | — |
| Security profiles | Virtual patching profile | 7.4.1 and later | IDPS `SRG-NET-000019-IDPS-00019` | — |
| Security profiles | Add inline CASB security profile | 7.4.1 and later | ALG `SRG-NET-000018-ALG-000017` | — |
| Security profiles | Support domain name in XFF with ICAP | 7.4.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security profiles | Support Punycode encoding for the url and hostname fields in flow inspection logs | 7.4.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security profiles | Support Diameter protocol inspection on the FortiGate | 7.4.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security profiles | Improve visibility of OT vulnerabilities and virtual patching signatures | 7.4.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security profiles | Enhance the video filter profile with a new level of customization and control | 7.4.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security profiles | Enhancements to data loss prevention (DLP) | 7.4.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security profiles | Support XLSB, OpenOffice, and RTF files for CDR in antivirus profiles | 7.4.4 and later | ALG `SRG-NET-000249-ALG-000134` | — |
| Security profiles | Search engine support extended to flow-based web filter profiles | 7.4.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security profiles | GUI support for exact data match (EDM) for data loss prevention | 7.4.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security profiles | Control TLS connections that utilize Encrypted Client Hello | 7.4.4+; 7.6.0+ | ALG `SRG-NET-000062-ALG-000150`; ALG `SRG-NET-000391-ALG-000140` | `config firewall ssl-ssh-profile; edit <PROFILE>; config https; set encrypted-client-hello block; end; next; end` |
| Security profiles | Proxy-related features no longer supported on FortiGate 2 GB RAM models | 7.4.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security profiles | Sanitize Microsoft OneNote files through content disarm and reconstruction | 7.6.0 and later | ALG `SRG-NET-000249-ALG-000134` | — |
| Security profiles | Stream-based antivirus scanning for HTML and Javascript files | 7.6.0 and later | ALG `SRG-NET-000248-ALG-000133` | — |
| Security profiles | FortiGuard managed DLP dictionaries | 7.6.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security profiles | Introducing domain fronting protection | 7.6.0 and later | ALG `SRG-NET-000019-ALG-000018` | — |
| Security profiles | DNS filtering in proxy policies | 7.6.0 and later | ALG `SRG-NET-000019-ALG-000018` | — |
| Security profiles | DNS translation support for Service records over the DNS Filter profile | 7.6.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security profiles | Introduce URL risk-scores in determining policy action | 7.6.1 and later | ALG `SRG-NET-000019-ALG-000018` | — |
| Security profiles | Streamline IoT/OT device detection | 7.6.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security profiles | Unified OT virtual patching and IPS signatures | 7.6.1 and later | IDPS `SRG-NET-000019-IDPS-00019` | — |
| Security profiles | Selective forwarding to ICAP server | 7.6.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security profiles | Zero-day malware stream scanning | 7.6.3 and later | ALG `SRG-NET-000248-ALG-000133` | — |
| Security profiles | AI and ML-based IPS detection | 7.6.3 and later | IDPS `SRG-NET-000019-IDPS-00019` | — |
| Security profiles | Control TLS connections that utilize Encrypted Client Hello in flow mode | 7.6.3 and later | ALG `SRG-NET-000062-ALG-000150` | — |
| Security profiles | Support FortiSandbox inline scanning in flow mode | 7.6.4 and later | ALG `SRG-NET-000249-ALG-000134` | — |
| Security profiles | Integration with FortiData | 7.6.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security profiles | Use MPIP labels directly with DLP profiles | 7.6.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security profiles | Application control support for generative AI | 7.6.4+; 8.0.0+ | ALG `SRG-NET-000018-ALG-000017` | — |
| Security profiles | Hybrid post-quantum cryptography in SSL deep inspection in flow mode | 7.6.5 and later | ALG `SRG-NET-000062-ALG-000150` | — |
| Security profiles | Support proxy-based inspection for email protocols on models with 2 GB RAM | 7.6.5 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security profiles | Enhanced UTM protection with WebSocket traffic inspection | 7.6.7+; 8.0.0+ | ALG `SRG-NET-000248-ALG-000133` | — |
| Security profiles | File filter warning action for HTTP downloads | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security profiles | Local URL filtering with custom FortiGuard categories | 8.0.0 and later | ALG `SRG-NET-000019-ALG-000018` | — |
| Security profiles | New classification framework for application signatures and FortiView support | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security profiles | Support for hybrid PQC SSL deep inspection in proxy mode | 8.0.0 and later | ALG `SRG-NET-000062-ALG-000150` | — |
| Security profiles | FortiGuard-free rating for local and external categories | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security profiles | Expanded CASB SaaS application database | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security profiles | Enhanced DNS security with AI and ML driven threat detection | 8.0.0 and later | ALG `SRG-NET-000019-ALG-000018` | — |
| Security profiles | Agentic AI protocol support in FortiOS | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security profiles | Enhanced DLP with OCR-based content analysis | 8.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security profiles | Custom telemetry application support | 8.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security profiles | EDM support for hashed data through GO tool | 8.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security profiles | Support PQC-Classical TLS key exchange translation in proxy mode SSL deep inspection | 8.0.1 and later | ALG `SRG-NET-000062-ALG-000150` | — |
| Security profiles | SIP ALG supports one-to-one NAT mapping to each voice server in VIP range | 8.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security profiles | Post-Quantum TLS authentication support for deep inspection in flow mode | 8.0.1 and later | ALG `SRG-NET-000062-ALG-000150` | — |
| Security profiles | SaaS application risk visibility | 8.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security profiles | Custom application classifications for application signatures | 8.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security profiles | Application control signature package hold timer | 8.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security profiles | Add web filter image classification | 8.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| VPN | Configurable IKE port | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| VPN | Packet distribution for aggregate dial-up IPsec tunnels | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| VPN | IPsec global IKE embryonic limit | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| VPN | FortiGate as SSL VPN Client | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| VPN | Dual stack IPv4 and IPv6 support for SSL VPN | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| VPN | Disable the clipboard in SSL VPN web mode RDP connections | 7.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| VPN | Use SSL VPN interfaces in zones | 7.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| VPN | SSL VPN and IPsec VPN IP address assignments | 7.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| VPN | Dedicated tunnel ID for IPsec tunnels | 7.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| VPN | Allow customization of RDP display size for SSL VPN web mode | 7.0.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| VPN | IPsec support for round robin and RPS distribution | 7.0.8 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| VPN | Restriction and validation of HTTP messages | 7.0.15+; 7.2.9+; 7.4.4+ | ALG `SRG-NET-000512-ALG-000066` | — |
| VPN | Add log field to identify ADVPN shortcuts in VPN logs | 7.2.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| VPN | Show the SSL VPN portal login page in the browser's language | 7.2.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| VPN | SLA link monitoring for dynamic IPsec and SSL VPN tunnels | 7.2.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| VPN | SAML-based authentication for FortiClient remote access dialup IPsec VPN clients | 7.2.0+; 7.4.0+ | VPN `SRG-NET-000138-VPN-000490`; VPN `SRG-NET-000166-VPN-000580` | — |
| VPN | IPsec IKE load balancing based on FortiSASE account information | 7.2.5+; 7.4.0+ | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| VPN | Securely exchange serial numbers between FortiGates connected with IPsec VPN | 7.2.6+; 7.4.1+ | VPN `SRG-NET-000148-VPN-000540` | — |
| VPN | Matching IPsec tunnel gateway based on address parameters | 7.2.8+; 7.4.4+ | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| VPN | Enhancing IPsec security and performance | 7.2.8 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| VPN | Support for autoconnect to IPsec VPN using Microsoft Entra ID | 7.2.8+; 7.4.2+ | VPN `SRG-NET-000230-VPN-002436` | — |
| VPN | Update the SSL VPN web portal layout using Neutrino | 7.4.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| VPN | Improve the styling of the SSL VPN landing page | 7.4.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| VPN | Allow SSL VPN login to be redirected to a custom landing page | 7.4.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| VPN | IPsec SA key retrieval from a KMS server using KMIP | 7.4.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| VPN | Add user group information to the SSL-VPN monitor | 7.4.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| VPN | Adjust DTLS heartbeat parameter for SSL VPN | 7.4.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| VPN | Multiple interface monitoring for IPsec | 7.4.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| VPN | Update SSL VPN default behavior and visibility in the GUI | 7.4.1 and later | VPN `SRG-NET-000132-VPN-000450` | — |
| VPN | IPsec split DNS | 7.4.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| VPN | Support IPsec tunnel to change names | 7.4.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| VPN | Encapsulate ESP packets within TCP headers | 7.4.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| VPN | IPsec key retrieval with a QKD system using the ETSI standardized API | 7.4.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| VPN | IPsec IKEv2 VPN 2FA with EAP and certificate authentication | 7.4.2 and later | VPN `SRG-NET-000140-VPN-000500`; VPN `SRG-NET-000164-VPN-000560` | — |
| VPN | TCP encapsulation of IKE and IPsec packets across multiple vendors | 7.4.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| VPN | Enhancing IPsec security using EMS SN verification | 7.4.4 and later | VPN `SRG-NET-000343-VPN-001370` | — |
| VPN | Cross-validation for IPsec VPN | 7.4.4 and later | VPN `SRG-NET-000343-VPN-001370` | — |
| VPN | Resuming sessions for IPsec tunnel IKE version 2 | 7.4.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| VPN | Automatic selection of IPsec tunneling protocol | 7.6.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| VPN | Security posture tag match enforced before dial-up IPsec VPN connection | 7.6.0 and later | VPN `SRG-NET-000343-VPN-001370` | — |
| VPN | Enhancing security with Post-Quantum Cryptography for IPsec key exchange | 7.6.1 and later | VPN `SRG-NET-000371-VPN-001650` | — |
| VPN | Migration from SSL VPN tunnel mode to IPsec VPN | 7.6.3 and later | VPN `SRG-NET-000132-VPN-000460` | — |
| VPN | Agentless VPN | 7.6.3 and later | VPN `SRG-NET-000062-VPN-000200` | — |
| VPN | Configure FortiClient SIA for IPsec VPN tunnels | 7.6.3 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| VPN | Support Quantum Key Distribution and Post-Quantum Cryptography | 7.6.3 and later | VPN `SRG-NET-000371-VPN-001650` | — |
| VPN | Post-Quantum Cryptography for Agentless VPN | 7.6.5 and later | VPN `SRG-NET-000371-VPN-001650` | — |
| VPN | Allow UDP port 443 for dialup IPsec VPN | 7.6.5 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| VPN | Multipath IPsec VPN | 7.6.7 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| VPN | New Cloud SDN Orchestration VPN wizard for AWS | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| VPN | Support matching firewall policies and policy routes based on source IP geography of dial-up IPsec remote users | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| VPN | Send security posture tags from FortiClient to FortiOS directly as JWT | 8.0.0 and later | VPN `SRG-NET-000343-VPN-001370` | — |
| VPN | TLS 1.3 based VPN over TCP | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| VPN | Native VPN remote access support in VPN wizard | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| VPN | Default to IPAM addressing for remote access VPNs in VPN Wizard | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| VPN | Display interface and tunnel alias in various diagnose and get commands | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| VPN | Support SM3/SM4 cryptographic algorithms for IKEv1/ IKEv2 | 8.0.0 and later | VPN `SRG-NET-000510-VPN-002180` | — (SM3 and SM4 are not FIPS-approved; do not use them) |
| VPN | Show only recommended IKE proposals by default | 8.0.0 and later | VPN `SRG-NET-000317-VPN-001090` | — |
| VPN | DNS suffix for IKEv2 VPN | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| VPN | Signature authentication for VPNs using Post Quantum Cryptography | 8.0.0 and later | VPN `SRG-NET-000164-VPN-000560` | — |
| VPN | VPN with FortiClient Standalone and FortiIdentity Cloud | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| VPN | IPv6 addressing for remote access VPNs with IPAM | 8.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| VPN | FGSP tunnel roles in VPN widget | 8.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| VPN | Logging enhancements for tunnel down | 8.0.1 and later | VPN `SRG-NET-000492-VPN-001980` | — |
| VPN | IPsec synchronization during FGSP member join and failover | 8.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| VPN | IPsec VPN Wizard top-level template update | 8.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| User and authentication | Integrate user information from EMS connector and Exchange connector in the user store | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| User and authentication | SAML authentication in a proxy policy | 7.0.0 and later | ALG `SRG-NET-000138-ALG-000063` | — |
| User and authentication | Improve FortiToken Cloud visibility | 7.0.1 and later | FGT-NDM `FGFW-ND-000205`; ALG `SRG-NET-000140-ALG-000094` | — |
| User and authentication | Use a browser as an external user-agent for SAML authentication in an SSL VPN connection | 7.0.1 and later | VPN `SRG-NET-000138-VPN-000490` | — |
| User and authentication | Add configurable FSSO timeout when connection to collector agent fails | 7.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| User and authentication | Track users in each Active Directory LDAP group | 7.0.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| User and authentication | Configuring SAML SSO in the GUI | 7.0.2 and later | FGT-NDM `FGFW-ND-000030` | — |
| User and authentication | Migrating FortiToken Mobile users from FortiOS to FortiToken Cloud | 7.0.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| User and authentication | Synchronizing LDAP Active Directory users to FortiToken Cloud using the group filter | 7.0.6 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| User and authentication | RADIUS Termination-Action AVP in wired and wireless scenarios | 7.2.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| User and authentication | Improve response time for direct FSSO login REST API | 7.2.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| User and authentication | Configuring client certificate authentication on the LDAP server | 7.2.0 and later | FGT-NDM `FGFW-ND-000245` | — |
| User and authentication | Tracking rolling historical records of LDAP user logins | 7.2.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| User and authentication | Using a comma as a group delimiter in RADIUS accounting messages | 7.2.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| User and authentication | Vendor-Specific Attributes for TACACS | 7.2.1 and later | FGT-NDM `FGFW-ND-000030` | — |
| User and authentication | Synchronizing LDAP Active Directory users to FortiToken Cloud using the two-factor filter | 7.2.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| User and authentication | Specify the SAN field to use for LDAP-integrated certificate authentication | 7.2.4 and later | VPN `SRG-NET-000166-VPN-000590` | — |
| User and authentication | Add RADSEC client support | 7.4.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| User and authentication | Enable the FortiToken Cloud free trial directly from the FortiGate | 7.4.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| User and authentication | Enhance complexity options for local user password policy | 7.4.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| User and authentication | RADIUS integrated certificate authentication for SSL VPN | 7.4.1 and later | VPN `SRG-NET-000164-VPN-000560` | — |
| User and authentication | New options for certificate validation and FortiClient EMS tag matching | 7.4.4 and later | VPN `SRG-NET-000164-VPN-000560` | — |
| User and authentication | Customizable password reuse thresholds | 7.6.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| User and authentication | Trigger RADIUS authentication with DNS and ICMP queries | 7.6.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| User and authentication | Authentication sessions preserved after a reboot | 7.6.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| User and authentication | SCIM server support | 7.6.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| User and authentication | GUI support for SCIM clients | 7.6.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| User and authentication | Bearer token authentication for SCIM | 7.6.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| User and authentication | Support SAML authentication in a proxy policy using SCIM | 7.6.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| User and authentication | Support SAML users when configuring local users | 7.6.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| User and authentication | Configure FTM push with dynamic IP handling in the GUI | 7.6.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| User and authentication | Per-Session SAML authentication logging and logout support for ZTNA and explicit proxy users | 7.6.5 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| User and authentication | Direct SCIM group integration and SCIM authorization based on the ZTNA peer certificate | 7.6.7 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| User and authentication | Enable secure LDAP connection by default in the GUI | 8.0.0 and later | FGT-NDM `FGFW-ND-000245` | — |
| User and authentication | SCIM group integration and SCIM authorization based on the ZTNA peer certificate | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| User and authentication | SSO integration with FortiIdentity Cloud | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| User and authentication | Post-authentication redirection using continue form item | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Add profile support for UNII-4 5GHz band on FortiAP G-series models | 7.4.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Add support for WPA3-SAE security mode on mesh backhaul SSIDs | 7.4.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Implement multi-processing for the wpad daemon for large-scale FortiAP management | 7.4.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Add support for an IPsec VPN tunnel that carries the FortiAP SN | 7.4.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Support for WPA3 security modes on FortiWiFi units operating in Client Mode | 7.4.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Specify FortiSwitch names to use in switch-controller CLI commands | 7.4.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Support user-configurable ACL | 7.4.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Support configuring DHCP-snooping option-82 settings | 7.4.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Display DHCP-snooping option-82 data | 7.4.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Fast failover of CAPWAP control channel between two uplinks | 7.4.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Support Dynamic VLAN assignment with multiple VLAN IDs per Name Tag | 7.4.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Support for EAP/TLS on FortiWiFi models operating in Client Mode | 7.4.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Enable AP and Client mode on FortiWiFi 80F series models | 7.4.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Integration with Pole Star's NAO Cloud service for BLE asset tag tracking | 7.4.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Wireless Foreground Scan improvements | 7.4.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Support for MIMO mode configuration | 7.4.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Add GUI support for configuring WPA3-SAE security mode on mesh backhaul SSIDs | 7.4.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Support automatically allowing and blocking intra-VLAN traffic based on FortiLink connectivity | 7.4.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Support the FortiOS one-arm sniffer on a mirrored VLAN interface | 7.4.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Support new commands for Precision Time Protocol configuration | 7.4.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Support inter-VLAN routing by managed FortiSwitch units | 7.4.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Support security rating recommendations for tier-2 and tier-3 MCLAGs | 7.4.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Support for the authentication and encryption of fabric links | 7.4.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Synchronize the FortiOS interface description with the FortiSwitch VLAN description | 7.4.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Add support for SAE-PK generation | 7.4.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Support RADIUS accounting interim update on roaming for WPA Enterprise security | 7.4.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Improve Bonjour profile provisioning and redundancy | 7.4.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | GUI support for WPA3 security mode on Client mode FortiWiFi units | 7.4.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Support WPA3 options when the FortiAP radio mode is set to SAM | 7.4.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Add automated reboot functionality for FortiAPs | 7.4.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Support individual control of 802.11k and 802.11v protocols | 7.4.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Support external antennas in select FortiAP models | 7.4.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Support Hitless Rolling AP upgrade | 7.4.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Support third-party antennas in select FortiAP models | 7.4.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Improve CAPWAP stability over NAT | 7.4.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Support FortiSwitch management using HTTPS | 7.4.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Set the priority for dynamic or egress VLAN assignment | 7.4.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Specify how RADIUS request attributes are formatted | 7.4.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Enhance memory optimization in FortiGate-managed FortiAPs | 7.4.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Support for Beacon Protection | 7.4.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Add support for managing the FortiAP USB port status | 7.4.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Support more Captive Portal security modes | 7.4.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Add profile support for Wi-Fi 7 on FortiAP K-series models | 7.4.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Support receiving the NAS-Filter-Rule during Wi-Fi authentication | 7.4.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Support MACsec on FortiAP G-series | 7.4.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Support LACP fallback mode | 7.4.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Support dynamic access control lists for managed switches | 7.4.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Use FortiSwitch event log IDs as triggers for automation stitches | 7.4.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Enhanced device-matching logic based on policy priority | 7.4.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Support internet connectivity for WiFi clients through FortiExtender in LAN-extension mode | 7.4.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Support fast failover for FortiExtender | 7.4.4+; 7.6.0+ | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Improve packet detection on the FortiAP sniffer | 7.4.5+; 7.6.0+ | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Support RADIUS MAC Authentication for MPSK on WPA3 SAE SSID | 7.4.5 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Add BLE integration and support for Evresys RTLS solution | 7.4.5 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Support uploading a captive portal's certificate authority to the FortiAP | 7.4.5 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | New GUI for FortiWiFi configurations | 7.4.10 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Support the 802.11mc protocol in FortiAP | 7.6.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Support OpenRoaming Standards on FortiAP | 7.6.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Support segregating WLAN traffic on FortiAPs operating in WAN-LAN mode | 7.6.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Support isolating mDNS traffic on the Bonjour profile | 7.6.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Support RADIUS NAS-ID on FortiAPs in standalone mode | 7.6.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Support RADSEC on WPA2/WPA3-Enterprise SSID | 7.6.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Add GUI support for configuring wireless data rates and sticky client thresholds | 7.6.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Support self-registration of MPSKs through FortiGuest | 7.6.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Support IKEv2 for FortiAP IPsec data channel management | 7.6.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Support WPA3-SAE and WPA3-SAE Transition security modes in MPSK profiles | 7.6.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Change the priority of MAB and EAP 802.1X authentication | 7.6.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Send SNMP traps for MAC address changes | 7.6.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Add Advanced WIDS Options | 7.6.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Support RADSEC on Local Bridge mode captive portals | 7.6.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Add a RADIUS Called Station ID setting | 7.6.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Support remote TACACS access to FortiAP | 7.6.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Support RADIUS Accounting messages over FortiGuest MPSK Authentication | 7.6.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Support QinQ with the switch controller | 7.6.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Enhance network performance with VLAN pruning | 7.6.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Support VLAN over FortiExtender LAN-extension mode | 7.6.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Support split tunneling in LAN extension mode | 7.6.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Support multiple APNs in WAN extension mode | 7.6.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Support FortiCare registration for FortiExtender | 7.6.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Provide an enhanced GUI for NAC policies | 7.6.3 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Support IPv6 addresses for managed FortiSwitch units | 7.6.3 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Prevent automatically created VLANs | 7.6.3 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Add GUI support for split tunneling in LAN extension mode | 7.6.3 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Add GUI support for multiple APNs in WAN extension mode | 7.6.3 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Add GUI support for FortiCare registration for FortiExtender | 7.6.3 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Add profile support for Zero-Wait DFS on select FortiAP models | 7.6.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Support Zero-Touch Provisioning for Mesh Leaf FortiAPs | 7.6.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Support manual captive portal trigger for bridge mode SSIDs | 7.6.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Add event logging for IPv4 source guard | 7.6.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Layer-3 switch configuration | 7.6.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Support maximum burst size for storm control | 7.6.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Increase length of managed FortiSwitch names | 7.6.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Integrate FortiSwitch NAC and 802.1X authentication | 7.6.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Support VLAN ID lists on LAN-extension FortiExtenders | 7.6.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Support FortiAP management through IPv6 | 7.6.5+; 8.0.0+ | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Enhance DARRP with FortiAIOps | 7.6.5+; 8.0.0+ | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Support Wi-Fi 7 MLO on FortiAP K-series models | 7.6.5+; 8.0.0+ | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Enhance GUI support for configuring mesh leaf FortiAPs | 7.6.5 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Support CA requests through EST and SCEP servers | 7.6.5 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Support Filter-ID for RADIUS authentication in WPA2-Enterprise | 7.6.5 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Improve security during FortiWiFi setup | 7.6.5 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | New default configurations on FortiWiFi platforms | 7.6.5 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Add support for LoRaWAN profiles on FAP-222KL | 7.6.5 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Add health check settings in the LAN-extension profile | 7.6.5 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Support customizable DHCP Option 82 configurations | 7.6.7+; 8.0.0+ | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Support MLO on standalone VAPs | 7.6.7+; 8.0.0+ | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Improve CAPWAP stability | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Support dynamic redirect URLs from Cisco ISE | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Support IPsec traffic offloading from the FortiAP | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Support up to 16 VAPs on FortiAP G and K-series models | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Support FQDN in Layer 3 ACLs | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Add GUI support for 6 GHz Channel Utilization | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Optimize and update default DARRP parameters | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Support 802.3af PoE output on FAP-23JK | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Add GUI support for capturing wireless packets | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Support tuning Clear Channel Assessment threshold values | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Allow FortiAP radio and FortiWiFi local radio to be disabled | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Support DVLAN assignments from RADIUS and VLAN pooling together | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Support multiple FortiAP groups per VLAN entry for VLAN pooling | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Add RADIUS authentication survivability for 802.1X SSIDs | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Automated FortiAP location positioning system | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Support FortiGuest assignments of RADIUS attributes to MPSK groups | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Add maximum power control for PoE ports | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Increase number of supported switches | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Advertise and control EEE using LLDP in the switch controller | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Support trusted host settings for managed switches | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Control when custom commands are pushed | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Provide private data encryption for managed switches | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Support MAC move for managed switches | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Enable advanced switching features in the GUI | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Control the number of 802.1X-authenticated clients per port | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Support IGMP-snooping static group configuration | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Dynamic MAB session handling | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Enhance NAC/DPP port control and QoS/PoE support | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Add global port‑selection criteria for some switch models | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Using NAC with 802.1X authentication in the FortiOS GUI | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Configure captive portals on LAN-extension FortiExtender | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Support static IP clients in VLAN pools | 8.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Support WPA3 transition mode SSIDs on 6 GHz radios | 8.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Automatic FortiAP password change after authorization | 8.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Support upgrading FortiAP firmware from external servers | 8.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Automatic one-time DARRP optimization | 8.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Support GCMP-256 on OWE security profiles | 8.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Apply RSPAN or ERSPAN per FortiLink interface | 8.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | FortiVoice management through FortiGate Voice Controller | 8.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Support WiFi-WAN as LAN Extension uplink | 8.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| LAN Edge | Support LAN Extension Always mode | 8.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Configure Agile Multiband Operation | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Captive portal authentication when bridged via software switch | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | DHCP address enforcement | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Increase maximum number of supported VLANs | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Add RADIUS MAC delimiter options | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Radio transmit power range in dBm | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Station mode on FortiAP radios to initiate tests against other APs | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Forward error correction settings on switch ports | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Cancel pending or downloading FortiSwitch upgrades | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Automatic provisioning of FortiSwitch firmware upon authorization | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Additional FortiSwitch recommendations in Security Rating | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | PoE pre-standard detection disabled by default | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Cloud icon indicates that the FortiSwitch unit is managed over layer 3 | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | GUI support for viewing and configuring shared FortiSwitch ports | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | FortiSwitch NAC VLANs widget | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Use wildcards in a MAC address in a NAC policy | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | FortiGate NAC engine optimization | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Wireless NAC support | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Dynamic port profiles for FortiSwitch ports | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | GUI updates for the switch controller | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | AP operating temperature | 7.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Allow indoor and outdoor flags to be overridden | 7.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | DNS configuration for local standalone NAT VAPs | 7.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Backward compatibility with FortiAP models that uses weaker ciphers | 7.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Disable console access on managed FortiAP devices | 7.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Captive portal authentication in service assurance management (SAM) mode | 7.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Support CAPWAP hitless failover using FGCP | 7.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Ability to re-order FortiSwitch units in the Topology view | 7.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Support of the DHCP server access list | 7.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | SNMP OIDs added for switch statistics and port status | 7.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Display port properties of managed FortiSwitch units | 7.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Support dynamic firewall addresses in NAC policies | 7.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | NAC LAN segments | 7.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Provide LBS station information with REST API | 7.0.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Allow users to select individual security profiles in bridged SSID | 7.0.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Wireless client MAC authentication and MPSK returned through RADIUS | 7.0.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | FQDN for FortiPresence server IP address in FortiAP profiles | 7.0.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Wi-Fi Alliance Hotspot 2.0 Release 3 support | 7.0.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Automatic BSS coloring | 7.0.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Configure 802.11ax MCS rates | 7.0.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | IGMP-snooping querier and per-VLAN IGMP-snooping proxy configuration | 7.0.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Managing DSL transceivers (FN-TRAN-DSL) | 7.0.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Specify FortiSwitch groups in NAC policies | 7.0.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Introduce LAN extension mode for FortiExtender | 7.0.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Using the backhaul IP when the FortiGate access controller is behind NAT | 7.0.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Bandwidth limits on the FortiExtender Thin Edge | 7.0.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Syslog profile to send logs to the syslog server | 7.0.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Support Dynamic VLAN assignment by Name Tag | 7.0.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | DARRP to consider full channel bandwidth in channel selection | 7.0.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Support multiple DARRP profiles and per profile optimize schedule | 7.0.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Support WPA3 on FortiWiFi F-series models | 7.0.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Support advertising vendor specific element in beacon frames | 7.0.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Support 802.1X supplicant on LAN | 7.0.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | GUI support for Wireless client MAC authentication and MPSK returned through RADIUS | 7.0.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | GUI enhancements to distinguish UTM capable FortiAP models | 7.0.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Upgrade FortiAP firmware on authorization | 7.0.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Optimize memory usage in 802.11r Fast BSS transition deployments | 7.0.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Optimize Broadcast/Multicast packets across the FortiAP network | 7.0.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | One-time automatic upgrade to the latest FortiSwitch firmware | 7.0.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Support hardware vendor matching in dynamic port policies | 7.0.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | IPAM in FortiExtender LAN extension mode | 7.0.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | FortiExtender LAN extension in public cloud FGT-VM | 7.0.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Wireless Authentication using SAML Credentials | 7.0.5 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Add profile support for FortiAP G-series models supporting WiFi 6E Tri-band and Dual 5 GHz modes | 7.0.8+; 7.2.1+ | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Configure the frequency of IGMP queries | 7.0.8+; 7.2.1+ | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Allow pre-authorization of a FortiAP by specifying a Wildcard Serial Number | 7.2.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Disable dedicated scanning on FortiAP F-Series profiles | 7.2.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Improve WiFi channel selection GUI | 7.2.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Support Layer 3 roaming for tunnel mode | 7.2.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Report wireless client app usage for clients connected to bridge mode SSIDs | 7.2.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Automatic updating of the port list when switch split ports are changed | 7.2.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Use wildcard serial numbers to pre-authorize FortiSwitch units | 7.2.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Allow multiple managed FortiSwitch VLANs to be used in a software switch | 7.2.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Allow a LAG on a FortiLink-enabled software switch | 7.2.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Configure MAB reauthentication globally or locally | 7.2.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Enhanced FortiSwitch Topology view | 7.2.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Support dynamic discovery in FortiLink mode over a layer-3 network | 7.2.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Configure flap guard through the switch controller | 7.2.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Allow FortiSwitch console port login to be disabled | 7.2.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Configure multiple flow-export collectors | 7.2.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Enhanced FortiSwitch Ports page and Diagnostics and Tools pane | 7.2.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Manage FortiSwitch units on VXLAN interfaces | 7.2.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Add new FortiSwitch Clients page | 7.2.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Allow the configuration of NAC LAN segments in the GUI | 7.2.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Allow FortiExtender to be managed and used in a non-root VDOM | 7.2.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Support enabling or disabling 802.11d | 7.2.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Improve MAC address filtering | 7.2.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Support Layer 3 roaming for bridge mode | 7.2.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Redesign rate control CLI | 7.2.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Add GUI visibility for Advanced Wireless Features | 7.2.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | WPA3 enhancements to support H2E only and SAE-PK | 7.2.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Automatic revision backup upon FortiSwitch logout or firmware upgrade | 7.2.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | FortiExtender monitoring enhancement | 7.2.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Provision FortiExtender firmware upon authorization | 7.2.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Implement multi-processing for wireless daemon for large-scale FortiAP management | 7.2.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Allow custom RADIUS NAS-ID | 7.2.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Support wireless client mode on FortiWiFi 80F series models | 7.2.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Support displaying details about wired clients connected to the FortiAP LAN port | 7.2.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Add FortiView Internal Hubs monitor | 7.2.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Configure DHCP-snooping static entries | 7.2.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Track device traffic statistics when NAC is enabled | 7.2.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Enhance switch PoE port settings | 7.2.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Increase the number of NAC devices supported | 7.2.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | De-authorize FortiExtender devices | 7.2.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Simplify BLE iBeacon provisioning for RTLS deployments | 7.2.5 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Dynamically assign the NAS-IP-Address attribute | 7.2.9+; 7.4.2+ | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Secure access | Specify a tagged VLAN for when the authentication server is unavailable | 7.2.9+; 7.4.4+ | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | Allow administrators to define password policy with minimum character change | 7.0.0 and later | FGT-NDM `FGFW-ND-000311` | — (`min-change-characters` is documented for administrator passwords through the 7.6.0 CLI Reference; see *Where the commands come from*) |
| System | Enhance host protection engine | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | ACME certificate support | 7.0.0 and later | FGT-NDM `FGFW-ND-000195` | — (only with an ACME server of a DoD-approved CA) |
| System | Optimizing FGSP session synchronization and redundancy | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | Layer 3 unicast standalone configuration synchronization between peers | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | Improved link monitoring and HA failover time | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | HA monitor shows tables that are out of synchronization | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | HA failover due to memory utilization | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | IKE monitor for FGSP | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | Immediate download update option | 7.0.0 and later | IDPS `SRG-NET-000019-IDPS-00187`; ALG `SRG-NET-000019-ALG-000019` | — |
| System | Add option to automatically update schedule frequency | 7.0.0 and later | IDPS `SRG-NET-000019-IDPS-00187`; IDPS `SRG-NET-000246-IDPS-00205` | `config system autoupdate schedule; set status enable; set frequency automatic; end` |
| System | Update OUI files from FortiGuard | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | SFTP configuration backup | 7.0.1 and later | FGT-NDM `FGFW-ND-000180`; FGT-NDM `FGFW-ND-000185` | `execute backup config sftp <FILE> <SERVER> <USER> <PASSWORD>` |
| System | Promote FortiCare registration | 7.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | Add monitoring API to retrieve LTE modem statistics from 3G and 4G FortiGates | 7.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | Add USB support for FortiExplorer Android | 7.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | Resume IPS scanning of ICCP traffic after HA failover | 7.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | Warnings for unsigned firmware | 7.0.2 and later | FGT-NDM `FGFW-ND-000305` | — |
| System | Enabling individual ciphers in the SSH administrative access protocol | 7.0.2 and later | FGT-NDM `FGFW-ND-000260`; FGT-NDM `FGFW-ND-000265` | `config system ssh-config; set ssh-enc-algo <ENCRYPTION_ALGORITHMS>; set ssh-kex-algo <KEX_ALGORITHMS>; set ssh-mac-algo <MAC_ALGORITHMS>; end` (FIPS-approved algorithms only) |
| System | ECDSA in SSH administrative access | 7.0.2 and later | FGT-NDM `FGFW-ND-000260` | — |
| System | Clear multiple sessions with REST API | 7.0.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | Disable weak ciphers in the HTTPS protocol | 7.0.2 and later | FGT-NDM `FGFW-ND-000265`; FGT-NDM `FGFW-ND-000205` | `config system global; set admin-https-ssl-banned-ciphers <CIPHERS>; end` |
| System | Extend dedicated management CPU feature to 1U and desktop models | 7.0.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | Local certificate wizard | 7.0.2 and later | FGT-NDM `FGFW-ND-000195` | GUI: System > Certificates |
| System | Extended HA VMAC address range | 7.0.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | Use only EU servers for FortiGuard updates | 7.0.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | FDS-only ISDB package in firmware images | 7.0.4+; 7.2.0+ | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | Introduce maturity firmware levels | 7.0.6+; 7.2.0+ | FGT-NDM `FGFW-ND-000170` | — |
| System | Central management configuration preservation for factory reset on FortiGate | 7.0.6+; 7.2.4+ | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | Applying the session synchronization filter only between FGSP peers in an FGCP over FGSP topology | 7.0.6+; 7.2.1+ | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | Optimized FGSP peer communication | 7.0.6+; 7.2.0+ | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | Improve admin-restrict-local handling of multiple authentication servers | 7.0.8+; 7.2.0+ | FGT-NDM `FGFW-ND-000030` | `config system global; set admin-restrict-local all; end` |
| System | FGSP per-tunnel failover for IPsec | 7.0.8+; 7.2.1+ | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | FGCP over FGSP per-tunnel failover for IPsec | 7.0.8+; 7.2.1+ | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | Allow IPsec DPD in FGSP members to support failovers | 7.0.8+; 7.2.1+ | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | Enhance BIOS-level signature and file integrity checking | 7.0.12+; 7.2.5+; 7.4.0+ | FGT-NDM `FGFW-ND-000305` | — |
| System | Real-time file system integrity checking | 7.0.12+; 7.2.5+; 7.4.0+ | FGT-NDM `FGFW-ND-000305` | — |
| System | Command to compute file hashes | 7.0.13+; 7.2.6+; 7.4.0+ | FGT-NDM `FGFW-ND-000305` | — |
| System | Enhance file integrity check to perform verification during system bootup | 7.0.15+; 7.2.9+; 7.4.4+ | FGT-NDM `FGFW-ND-000305` | — |
| System | Enhance real-time file system integrity checking | 7.0.15+; 7.2.9+; 7.4.4+; 7.6.0+ | FGT-NDM `FGFW-ND-000305` | — |
| System | BIOS security Low and High level classification | 7.0.16+; 7.2.11+; 7.4.6+; 7.6.1+ | FGT-NDM `FGFW-ND-000305` | — |
| System | Access control for SNMP based on the MIB-view and VDOM | 7.2.0 and later | FGT-NDM `FGFW-ND-000210` | — |
| System | Backing up and restoring configuration files in YAML format | 7.2.0 and later | FGT-NDM `FGFW-ND-000180` | — |
| System | Remove split-task VDOMs and add a new administrative VDOM type | 7.2.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | VRRP on EMAC-VLAN interfaces | 7.2.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | Abbreviated TLS handshake after HA failover | 7.2.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | HA failover support for ZTNA proxy sessions | 7.2.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | Add warnings when upgrading an HA cluster that is out of synchronization | 7.2.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | Support up to 30 virtual clusters | 7.2.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | Verifying and accepting signed AV and IPS packages | 7.2.0 and later | FGT-NDM `FGFW-ND-000305`; IDPS `SRG-NET-000019-IDPS-00187` | — |
| System | Allow FortiGuard services and updates to initiate from a traffic VDOM | 7.2.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | Restrict SSH and telnet jump host capabilities | 7.2.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | Enable automatic firmware updates | 7.2.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | Deregistration from the GUI | 7.2.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | Add government end user option for FortiCare registration | 7.2.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | Support backing up configurations with password masking | 7.2.1 and later | FGT-NDM `FGFW-ND-000180` | — |
| System | New default certificate for HTTPS administrative access | 7.2.1 and later | FGT-NDM `FGFW-ND-000195` | `config system global; set admin-server-cert <CERT>; end` (a certificate issued by a DoD-approved CA) |
| System | Consolidate FGSP settings | 7.2.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | FortiManager as override server for IoT query services | 7.2.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | Remove maintainer account | 7.2.4 and later | FGT-NDM `FGFW-ND-000030`; FGT-NDM `FGFW-ND-000250` | — |
| System | Allow the FortiGate to override FortiCloud SSO administrator user permissions | 7.2.4 and later | FGT-NDM `FGFW-ND-000030`; FGT-NDM `FGFW-ND-000035` | — |
| System | Display warnings for supported Fabric devices passing their hardware EOS date | 7.2.5+; 7.4.0+ | FGT-NDM `FGFW-ND-000170` | — |
| System | Support checking for firmware updates daily when auto firmware upgrade is enabled | 7.2.6+; 7.4.0+ | FGT-NDM `FGFW-ND-000170` | — |
| System | Enable automatic firmware upgrades by default on entry-level FortiGates | 7.2.6 and later | FGT-NDM `FGFW-ND-000170` | — |
| System | Add built-in entropy source | 7.2.6+; 7.4.1+ | FGT-NDM `FGFW-ND-000280` | — |
| System | Enabling the INDEX extension | 7.2.8+; 7.4.4+ | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | Unauthorized firmware modification attempt reporting | 7.2.8+; 7.4.1+ | FGT-NDM `FGFW-ND-000305` | — |
| System | Single FortiGuard license for FortiGate A-P HA cluster | 7.2.9+; 7.4.6+; 7.6.1+ | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | Enhanced administrator password security | 7.2.11+; 7.4.8+; 7.6.1+ | FGT-NDM `FGFW-ND-000220` | — |
| System | FortiSentry real-time monitor | 7.2.11 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | Black box for FortiGate | 7.2.12 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | Add setting to control the upper limit of the FQDN refresh timer | 7.4.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | FortiConverter in the GUI | 7.4.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | Prevent FortiGates with an expired support contract from upgrading to a major or minor firmware release | 7.4.0 and later | FGT-NDM `FGFW-ND-000170` | — |
| System | FGCP HA between FortiGates of the same model with different AC and DC PSUs | 7.4.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | FortiGuard DLP service | 7.4.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | Prevent firmware upgrades when the support contract is expired using the GUI | 7.4.1 and later | FGT-NDM `FGFW-ND-000170` | — |
| System | Automatic firmware upgrade enhancements | 7.4.1 and later | FGT-NDM `FGFW-ND-000170` | — |
| System | Introduce selected availability (SA) version and label | 7.4.1 and later | FGT-NDM `FGFW-ND-000170` | — |
| System | View batch transaction commands through the REST API | 7.4.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | FGCP multi-version cluster upgrade | 7.4.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | Attack Surface Security Rating service | 7.4.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | Operational Technology Security Service | 7.4.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | Support automatic federated firmware updates of managed FortiAPs and FortiSwitches | 7.4.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | Support Enrollment over Secure Transport for automatic certificate management | 7.4.1 and later | FGT-NDM `FGFW-ND-000195` | — |
| System | Separate the SSHD host key from the administration server certificate | 7.4.2 and later | FGT-NDM `FGFW-ND-000260` | — |
| System | FortiOS REST API enhances FortiManager interaction with FortiExtender | 7.4.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | CLI system permissions | 7.4.2 and later | FGT-NDM `FGFW-ND-000035`; FGT-NDM `FGFW-ND-000285` | `config system accprofile; edit <PROFILE>; set cli-diagnose disable; set cli-exec disable; set cli-config disable; next; end` (for profiles that do not need these CLI commands) |
| System | Memory usage reduced on FortiGate models with 2 GB RAM | 7.4.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | Prevent firmware upgrade depending on the current firmware license's expiration date | 7.4.2 and later | FGT-NDM `FGFW-ND-000170` | — |
| System | Enhance IPv6 VRRP state control | 7.4.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | Add SNMP trap for memory usage on FortiGates | 7.4.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | Add SNMP trap for PSU power restore | 7.4.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | Updated default email notification server | 7.4.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | Configure TCP NPU session delay globally | 7.4.5+; 7.6.0+ | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | Automatic firmware upgrade control | 7.4.5+; 7.6.1+ | FGT-NDM `FGFW-ND-000170` | — |
| System | Sequential firmware upgrades for FortiGate Fabric devices | 7.4.5+; 7.6.0+ | FGT-NDM `FGFW-ND-000170` | — |
| System | Streamline timezone updates with a downloadable database | 7.4.5+; 7.6.0+ | FGT-NDM `FGFW-ND-000125` | — |
| System | FortiGate identity stored in TPM | 7.4.8 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | FortiOS Address Space Layout Randomization (ASLR), PIE, and RELRO | 7.4.8 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | Required firmware upgrades for FortiGate appliances with invalid support contracts or that have reached EOES | 7.4.9+; 7.6.4+ | FGT-NDM `FGFW-ND-000170` | — |
| System | Dedicated activation FQDNs for VM licensing | 7.4.10 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | Additional commands supported before device registration | 7.4.12+; 7.6.7+; 8.0.0+ | FGT-NDM `FGFW-ND-000170` | — |
| System | Enhancements to required upgrade when firmware license is invalid or device is EOES | 7.4.12+; 7.6.7+; 8.0.0+ | FGT-NDM `FGFW-ND-000170` | — |
| System | Restrict local administrator logins through the console | 7.6.0 and later | FGT-NDM `FGFW-ND-000030` | `config system global; set admin-restrict-local all; end` |
| System | Object usage included in the print tablesize command output | 7.6.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | Manual and automatic HA virtual MAC address assignment | 7.6.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | Backup heartbeat interface mitigates split-brain scenarios | 7.6.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | RSSO authenticated user logon information synchronized between FGSP peers | 7.6.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | FGSP support for failover with asymmetric traffic and UTM | 7.6.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | Encrypt configuration files in the eCryptfs file system | 7.6.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | Closed network VM license security enhancement | 7.6.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | OpenSSL FIPS provider installed globally at startup | 7.6.0 and later | FGT-NDM `FGFW-ND-000255` | `config system fips-cc; set status enable; end` |
| System | Ethernet Statistics Group | 7.6.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | Non-management VDOMs perform queries using SNMP v3 | 7.6.0 and later | FGT-NDM `FGFW-ND-000210` | — |
| System | SNMP support for BIOS security level | 7.6.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | Simplified device registration for Security Fabric devices | 7.6.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | Firmware upgrade report | 7.6.1 and later | FGT-NDM `FGFW-ND-000170` | — |
| System | Streamlined subscription and FortiGuard settings management | 7.6.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | FortiGate StateRamp support | 7.6.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | Monitor routing prefix for FGSP session failover | 7.6.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | Use per-FortiGate generated random password for private-data-encryption | 7.6.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | Optimizations for physical FortiGate devices with 2 GB RAM | 7.6.3 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | AMQP-powered subscription notifications for FortiGuard | 7.6.3 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | ACME External Account Binding support | 7.6.3 and later | FGT-NDM `FGFW-ND-000195` | — |
| System | Enhance administrative authentication and session monitoring | 7.6.4 and later | FGT-NDM `FGFW-ND-000085`; FGT-NDM `FGFW-ND-000090` | — |
| System | Enhanced firmware upgrade management for extension devices | 7.6.4 and later | FGT-NDM `FGFW-ND-000170` | — |
| System | Improve manual failover of FortiGates deployed in an A-P architecture with VWP and using wildcard VLAN | 7.6.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | Support IPv6 multicast route synchronization in HA | 7.6.4+; 8.0.0+ | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | FortiSASE-Sovereign licensing and management for FortiGate 91G and 901G | 7.6.5 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | Memory optimizations for start-up configs, NPs, and NTurbo | 7.6.5 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | Enhanced HTTPS management security with post-quantum TLS algorithms | 7.6.5 and later | FGT-NDM `FGFW-ND-000265` | — |
| System | Kernel Address Space Layout Randomization (KASLR) | 7.6.5+; 8.0.0+ | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | Legal third party disclosure panel | 7.6.7+; 8.0.0+ | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | Configurable timeout for log file system check | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | Administrator access hardening | 8.0.0 and later | FGT-NDM `FGFW-ND-000260`; FGT-NDM `FGFW-ND-000265`; FGT-NDM `FGFW-ND-000200` | `config system admin; edit <ADMIN>; set disallowed-login-methods <METHODS>; next; end` (block the login methods the administrator does not use) |
| System | SCP file transfers | 8.0.0 and later | FGT-NDM `FGFW-ND-000180` | — |
| System | VM license grace period monitoring enhancement | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | Configurable FQDN Host header for FortiGate proxy communication | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | Per VDOM replacement message customization | 8.0.0 and later | FGT-NDM `FGFW-ND-000050` | — |
| System | Configuration revisions and logout backup default changes | 8.0.0 and later | FGT-NDM `FGFW-ND-000180`; FGT-NDM `FGFW-ND-000185` | `config system global; set revision-backup-on-logout enable; end` |
| System | FortiAI assistant and CLI Code Lab | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | Auto-registration of FortiGate VMs to FortiManager Cloud | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | IPv6 support for in-band management IP | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | FGSP source IP and interface selection | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | HA monitoring support for software switch member interfaces | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | FGCP and FGSP synchronizes full-cone expectation sessions when session-pickup-expectation enabled | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | Enhanced FGCP monitoring with interface group awareness | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | GUI support for HA actions, health status, and config diff | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | FGSP synchronizes firewall-authenticated users | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | HA role shown in CLI prompt | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | Independent SNMP system information for HA members | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | SNMP support for new IP pool statistics OIDs | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | Enhanced FortiGuard server selection and load balancing | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | FortiGuard rating server prioritization improvements | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | API support to manage firmware for FortiGate extended devices | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | TR-069 (CWMP) support for FortiGate as managed CPE | 8.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | Encrypted configuration export | 8.0.1 and later | FGT-NDM `FGFW-ND-000180` | — |
| System | Connecting to HA secondary through logical interface | 8.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | Override wait time primary selection by HA uptime | 8.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| System | Expanded SNMP monitoring for IPsec VPN statistics | 8.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security Fabric | Security Fabric support in multi-VDOM environments | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security Fabric | Enhance Security Fabric configuration for FortiSandbox Cloud | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security Fabric | FortiWeb integration | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security Fabric | Show detailed user information about clients connected over a VPN through EMS | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security Fabric | Add FortiDeceptor as a Security Fabric device | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security Fabric | Add FortiAI as a Security Fabric device | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security Fabric | Improve communication performance between EMS and FortiGate with WebSockets | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security Fabric | Simplify EMS pairing with Security Fabric so one approval is needed for all devices | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security Fabric | Threat feed connectors per VDOM | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security Fabric | Nutanix connector | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security Fabric | Automation workflow improvements | 7.0.0 and later | FGT-NDM `FGFW-ND-000115`; FGT-FW `FNFG-FW-000105` | GUI: Security Fabric > Automation |
| Security Fabric | Microsoft Teams Notification action | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security Fabric | Replacement messages for email alerts | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security Fabric | Fabric connector event trigger | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security Fabric | Security Rating overlays | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security Fabric | Add test to check for two-factor authentication | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security Fabric | Add test to check for activated FortiCloud services | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security Fabric | FortiTester as a Security Fabric device | 7.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security Fabric | Simplify Fabric approval workflow for FortiAnalyzer | 7.0.1 and later | FGT-NDM `FGFW-ND-000110`; FGT-NDM `FGFW-ND-000295` | — |
| Security Fabric | Allow deep inspection certificates to be synchronized to EMS and distributed to FortiClient | 7.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security Fabric | Add tests for high priority vulnerabilities | 7.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security Fabric | Asset Identity Center page | 7.0.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security Fabric | Fabric Management page | 7.0.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security Fabric | Add FortiMonitor as a Security Fabric device | 7.0.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security Fabric | STIX format for external threat feeds | 7.0.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security Fabric | Display EMS ZTNA and endpoint tags in user widgets and Asset Identity Center | 7.0.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security Fabric | Replace FSSO-based FortiNAC tag connector with REST API | 7.0.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security Fabric | Add WebSocket for Security Fabric events | 7.0.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security Fabric | Enhance Fabric Management page | 7.0.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security Fabric | FortiGate Cloud logging in the Security Fabric | 7.0.4 and later | FGT-NDM `FGFW-ND-000110`; FGT-NDM `FGFW-ND-000295` | — |
| Security Fabric | Add FortiGuard outbreak alerts category | 7.0.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security Fabric | Add support for multitenant FortiClient EMS deployments | 7.0.8+; 7.2.1+ | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security Fabric | Rename FortiAI to FortiNDR | 7.0.8+; 7.2.0+ | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security Fabric | Allow FortiClient EMS connectors to trust EMS server certificate renewals based on the CN field | 7.0.11+; 7.2.4+ | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security Fabric | Validating FortiManager’s certificate before connection | 7.0.15+; 7.2.8+ | FGT-NDM `FGFW-ND-000195` | — |
| Security Fabric | Automatic serial number retrieval from FortiManager | 7.0.15+; 7.2.8+; 7.4.4+; 7.6.0+ | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security Fabric | Automatic regional discovery for FortiSandbox Cloud | 7.2.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security Fabric | Follow the upgrade path in a federated update | 7.2.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security Fabric | Register all HA members to FortiCare from the primary unit | 7.2.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security Fabric | Remove support for Security Fabric loose pairing | 7.2.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security Fabric | Allow FortiSwitch and FortiAP upgrade when the Security Fabric is disabled | 7.2.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security Fabric | Add new automation triggers for event logs | 7.2.0 and later | FGT-NDM `FGFW-ND-000115`; FGT-FW `FNFG-FW-000105` | GUI: Security Fabric > Automation |
| Security Fabric | Add IoT devices to Asset Identity Center page | 7.2.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security Fabric | Introduce distributed topology and security rating reports | 7.2.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security Fabric | SAP external connector | 7.2.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security Fabric | Using the REST API to push updates to external threat feeds | 7.2.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security Fabric | Support IPv6 dynamic addresses retrieved from Cisco ACI SDN connector | 7.2.1+; 7.4.0+ | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security Fabric | Certificate expiration trigger | 7.2.1 and later | FGT-NDM `FGFW-ND-000195` | — |
| Security Fabric | System automation actions to back up, reboot, or shut down the FortiGate | 7.2.1 and later | FGT-NDM `FGFW-ND-000180` | — |
| Security Fabric | Enhance automation trigger to execute only once at a scheduled date and time | 7.2.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security Fabric | Add PSIRT vulnerabilities to security ratings and notifications for critical vulnerabilities found on Fabric devices | 7.2.1 and later | FGT-NDM `FGFW-ND-000170` | — |
| Security Fabric | Add IoT vulnerabilities to the asset identity list and FortiGuard IoT security rating checks | 7.2.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security Fabric | Enhance the Fabric Connectors page | 7.2.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security Fabric | Add FortiPolicy as Security Fabric device | 7.2.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security Fabric | MAC address threat feed | 7.4.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security Fabric | Configuring FortiClient EMS and FortiClient EMS Cloud on a per-VDOM basis | 7.4.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security Fabric | Improve automation trigger and action selection | 7.4.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security Fabric | Update FortiVoice connector features | 7.4.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security Fabric | Support CIS compliance standards within security ratings | 7.4.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security Fabric | Add prompt for upgrade when a critical vulnerability is detected upon login | 7.4.1 and later | FGT-NDM `FGFW-ND-000170` | — |
| Security Fabric | Configure Purdue Levels for Fabric devices | 7.4.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security Fabric | Support for FortiVoice tag dynamic address in NAC policies | 7.4.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security Fabric | External resource entry limit enhancements | 7.4.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security Fabric | Support multi-tenant FortiClient Cloud fabric connectors | 7.4.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security Fabric | Apply threat feed connectors as source addresses in central SNAT | 7.6.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security Fabric | Support multi-tenant FortiClient Cloud fabric connectors in the GUI | 7.6.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security Fabric | Generic connector for importing addresses | 7.6.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security Fabric | Support mTLS client certification for external feed connections | 7.6.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security Fabric | Enhanced security rating customization | 7.6.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security Fabric | Enhanced security visibility for IoT/OT vulnerabilities | 7.6.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security Fabric | GUI support for mTLS of external feed connections | 7.6.3 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security Fabric | Enhancing FortiSandbox TLS security with CA and CN controls | 7.6.3 and later | FGT-NDM `FGFW-ND-000195` | — |
| Security Fabric | Multus CNI for Kubernetes connectors | 7.6.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security Fabric | Import IPv6 addresses from an APIC controller | 7.6.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security Fabric | Cloud-based Fabric Feed synchronization | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security Fabric | Label-based sandbox exemptions for sensitive data control | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security Fabric | Simultaneous FortiSandbox Cloud and on-premise integration | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security Fabric | Downstream FortiGates must approve upstream FortiGate when joining a security fabric | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security Fabric | Enhancement to certificate authorization for Security Fabric devices | 8.0.0 and later | FGT-NDM `FGFW-ND-000195` | — |
| Security Fabric | Support for Cisco ACI External EPG Subnets in Direct Connector | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security Fabric | Negation support in ACI direct connector address filters | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security Fabric | Centralized FortiTelemetry agent upgrade control | 8.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Security Fabric | Hashed URL and SNI list support for Web Filter profiles | 8.0.1 and later | ALG `SRG-NET-000019-ALG-000018` | — |
| Security Fabric | Security Fabric Topology page enhancements | 8.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Log and report | Add logs for the execution of CLI commands | 7.0.0 and later | FGT-NDM `FGFW-ND-000100` | `config system global; set cli-audit-log enable; end` |
| Log and report | Logging IP address threat feeds in sniffer mode | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Log and report | Enhance TLS logging | 7.0.1 and later | FGT-FW `FNFG-FW-000020` | — |
| Log and report | Generate unique user name for anonymized logs | 7.0.2 and later | FGT-NDM `FGFW-ND-000095` | `config log setting; set user-anonymize disable; end` |
| Log and report | Support TACACS+ accounting | 7.0.2 and later | FGT-NDM `FGFW-ND-000060`; FGT-NDM `FGFW-ND-000100` | — |
| Log and report | Add dstuser field to UTM logs | 7.0.2 and later | FGT-NDM `FGFW-ND-000095` | — |
| Log and report | Log REST API events | 7.0.4 and later | FGT-NDM `FGFW-ND-000060`; FGT-NDM `FGFW-ND-000080` | `config log setting; set rest-api-get enable; set rest-api-set enable; end` |
| Log and report | Add IOC detection for local out traffic | 7.2.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Log and report | HTTP transaction log fields | 7.2.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Log and report | Updated System Events log page | 7.2.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Log and report | New Security Events log page | 7.2.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Log and report | Improve FortiAnalyzer log caching | 7.2.0 and later | FGT-FW `FNFG-FW-000045` | — |
| Log and report | Add FortiAnalyzer Reports page | 7.2.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Log and report | Summary tabs on System Events and Security Events log pages | 7.2.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Log and report | Add time frame selector to log viewer pages | 7.2.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Log and report | Updating log viewer and log filters | 7.2.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Log and report | Consolidate log reports and settings into dedicated Reports and Log Settings pages | 7.2.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Log and report | Add Logs Sent Daily chart for remote logging sources | 7.2.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Log and report | Support switching to an alternate FortiAnalyzer if the main FortiAnalyzer is unavailable | 7.2.8+; 7.4.1+ | FGT-FW `FNFG-FW-000045`; FGT-NDM `FGFW-ND-000110` | — |
| Log and report | Introduce new log fields for long-live sessions | 7.4.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Log and report | Logging MAC address flapping events | 7.6.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Log and report | Non-management VDOMs send logs to both global and vdom-override syslog servers | 7.6.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Log and report | Logging message IDs | 7.6.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Log and report | Incorporating endpoint device data in the web filter UTM logs | 7.6.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Log and report | Set the source interface for syslog and NetFlow settings | 7.6.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Log and report | Logging detection of duplicate IPv4 addresses | 7.6.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Log and report | Logging local traffic per local-in policy | 7.6.0 and later | FGT-FW `FNFG-FW-000165` | — |
| Log and report | Logs generated when starting and stopping packet capture and TCP dump operations | 7.6.0 and later | FGT-FW `FNFG-FW-000155` | — |
| Log and report | Include zone information fields in logs | 7.6.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Log and report | Enhanced TACACS+ accounting log detail | 8.0.0 and later | FGT-NDM `FGFW-ND-000100` | — |
| Log and report | Custom log format support for syslog server | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Log and report | Secure log upload enhancements with SFTP and LZ4 support | 8.0.0 and later | FGT-NDM `FGFW-ND-000110` | — |
| Log and report | Add log messages for device and account license updates | 8.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | Collect only node IP addresses with K8s SDN connectors | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | Unicast HA on IBM VPC Cloud | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | Update AliCloud SDN connector to support Kubernetes filters | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | Synchronize wildcard FQDN resolved addresses to autoscale peers | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | Obtain FortiCare-generated license and certificates for GCP PAYG instances | 7.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | FortiGate VM on KVM running ARM processors | 7.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | Support MIME multipart bootstrapping on KVM with config drive | 7.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | Support GCP gVNIC interface | 7.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | FIPS cipher mode for OCI and GCP FortiGate VMs | 7.0.1 and later | FGT-NDM `FGFW-ND-000255` | — |
| Cloud | SD-WAN transit routing with Google Network Connectivity Center | 7.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | Support C5d instance type for AWS Outposts | 7.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | FGSP session sync on FortiGate-VMs on Azure with autoscaling enabled | 7.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | FortiFlex token and bootstrap configuration file fields in custom OVF template | 7.0.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | Subscription-based VDOM license for FortiGate-VM S-series | 7.0.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | Isolate CPUs used by DPDK engine | 7.0.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | AWS STS in AWS SDN connector | 7.0.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | Multitenancy support with AWS GWLB enhancement | 7.0.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | ATP bundle addition for S-series | 7.0.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | FortiCarrier upgrade license for FortiGate-VM S-series | 7.0.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | Injecting FortiFlex license via web proxy | 7.0.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | c6i instance support on AWS | 7.0.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | FortiGate-VM OVF package update | 7.0.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | Support c6g instances on AWS | 7.0.6 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | Add IPsec fast path in VPN and DPDK for FortiGate-VM | 7.0.6 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | Support Graviton c7g and c6gn instance types on AWS | 7.0.8 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | Support Ampere A1 Compute instances on OCI | 7.0.8+; 7.2.4+ | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | Add TPM support for FortiGate-VM | 7.0.8 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | Allow grace period for FortiFlex to begin passing traffic upon activation | 7.2.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | Azure new instance type support | 7.2.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | OCI X7 and X9 instance shapes | 7.2.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | GCP DPDK support | 7.2.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | External ID support in STS for AWS SDN connector | 7.2.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | Permanent trial mode for FortiGate-VM | 7.2.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | Allow FortiManager to apply license to a BYOL FortiGate-VM instance | 7.2.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | Enable high encryption on FGFM protocol for unlicensed FortiGate-VMs | 7.2.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | Implement sysrq for kernel crash | 7.2.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | Support various AWS endpoint ENI IP addresses in AWS SDN Connector | 7.2.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | Support automatic vCPU hot-add in FortiGate-VM for S-series and FortiFlex licenses | 7.2.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | Support for GCP ARM CPU-based T2A instance family | 7.2.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | Support for GCP shielded and confidential VM service | 7.2.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | VMware ESXi FortiGate-VM as ZTNA gateway | 7.2.5+; 7.4.0+ | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | Support the new AWS c7gn instance family | 7.2.6+; 7.4.0+ | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | Add OVF template support for VMware ESXi 8 | 7.2.6+; 7.4.1+ | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | FortiFlex grace period | 7.2.7 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | Support AWS local zones | 7.2.8 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | AliCloud supporting moving multiple EIPs on primary ENI for A-P HA | 7.2.8 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | Customizing the FortiFlex license token activation retry parameters | 7.2.8+; 7.4.2+ | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | AWS silent fips-cipher enablement | 7.2.8+; 7.4.4+ | FGT-NDM `FGFW-ND-000255` | — |
| Cloud | Azure Stack Hub marketplace deployment support | 7.2.8 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | VMware ESXi QAT support | 7.2.8 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | Azure marketplace support for ARM64 instances | 7.2.9+; 7.4.5+ | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | Support the AWS t4g, c6a, and c6in instance families | 7.4.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | Support SCCC backed by AliCloud | 7.4.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | Upgrade AWS ENA network interface driver to 2.8.3 | 7.4.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | Support UEFI-Preferred boot mode on AWS FortiGate-VM models | 7.4.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | OCI DRCC support | 7.4.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | Support multiple compartments and regions with single OCI SDN connector | 7.4.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | Add Cisco ACI ESG support for direct connector | 7.4.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | GCP support for C3 machine type | 7.4.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | AWS support for local zones | 7.4.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | AWS SBE support | 7.4.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | GCP support for C3A and C3D machine type | 7.4.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | Add FortiFlex GUI option | 7.4.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | AliCloud support for c7, c7a, and g5ne instance families | 7.4.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | AliCloud support change route table with IPv4 gateway for HA | 7.4.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | AWS SDN Connector support for alternate resources | 7.4.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | Integrate FortiGate Azure vWAN solution with Azure Monitor to capture health metrics | 7.4.2 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | GCP support for confidential computing | 7.4.3 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | Support the AWS c7i and c7a instance families | 7.4.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | Azure FortiGate-VM vWAN NVA support for PAYG metered billing | 7.4.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | GCP SDN connector to support IPv6 route table update via NextHopInstance | 7.4.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | Support for AliCloud Apsara Stack | 7.4.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | Azure SDN connector moves private IP address on trusted NIC during A-P HA failover | 7.4.5+; 7.6.1+ | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | Azure SDN connector relay through FortiManager support | 7.4.5+; 7.6.0+ | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | GCP SDN connector relay through FortiManager support | 7.4.5+; 7.6.0+ | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | OCI SDN connector IPv6 A-P HA failover support | 7.4.5 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | Azure SDN connector GraphQL bulk query support | 7.4.5+; 7.6.1+ | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | OCI SDN connector IPv6 address object support | 7.4.5+; 7.6.1+ | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | KVM Red Hat Enterprise Linux 9.4 support | 7.4.5+; 7.6.0+ | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | AliCloud GWLB support | 7.4.6+; 7.6.1+ | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | IBM Cloud virtual network interface support | 7.6.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | Support the AWS r8g instance family | 7.6.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | Support the AWS c8g instance family | 7.6.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | Support the OCI E5.Flex instance type | 7.6.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | AWS NitroTPM support | 7.6.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | AWS SDN connector IPv6 address object support | 7.6.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | GCP C4 Intel instance support | 7.6.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | FortiGate-VM GDC V support | 7.6.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | GCP SDN connector IPv6 address object support | 7.6.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | Support for Azure upcoming MANA NIC | 7.6.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | Azure SDN connector IPv6 address object support | 7.6.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | FGT_VM64_KVM IPsec performance improvement through virtio and RPS | 7.6.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | FGT_VM64_KVM IPsec performance through DPDK improvement | 7.6.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | FortiGate-VM config system affinity-packet-redistribution optimization | 7.6.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | OCI support for on-premise solutions | 7.6.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | AliCloud instance type support | 7.6.3 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | AWS c8gn instance type support | 7.6.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | Support for user managed scaling | 7.6.5 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Cloud | AWS SDN connector EKS filtering support | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| FortiOS Carrier | Selective GTP FGSP sync: only S10 tunnels | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| FortiOS Carrier | Selective GTP FGSP sync: only synchronize GTP tunnels | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| FortiOS Carrier | New RAT types | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| FortiOS Carrier | 3G to 4G/5G handover support | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| FortiOS Carrier | Increase GTP tunnel limit per profile to 50M tunnels | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| FortiOS Carrier | IPS can identify GTPv2 tunnels | 8.0.1 and later | IDPS `SRG-NET-000390-IDPS-00212` | — |
| FortiOS Carrier | IPv6 support for GTP-U with dynamic source ports | 8.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| FortiASIC | Improvements for NP7- or NP7Lite (SOC5)-offloaded GRE tunnels | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| FortiASIC | NP7 and NP7Lite (SOC5) offloading of TCP and UDP sessions denied by firewall policies to reduce CPU usage | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| FortiASIC | NP7 and NP7Lite (SOC5) support for traffic shaping based on dynamic RADIUS VSAs | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| FortiASIC | New SNMP counters to support CGNAT IP pool monitoring | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| FortiASIC | Hyperscale HA hardware session synchronization improves support for PBR sessions | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| FortiASIC | Hyperscale CGNAT EIF session timer options | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| FortiASIC | NP7 and NP7Lite (SOC5) support for offloading IPsec over a VNE interface | 8.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| FortiASIC | Including user information in EIF hardware log messages | 8.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| FortiASIC | Hyperscale support for the match-vip firewall policy option | 8.0.1 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Operational Technology | Add OT asset visibility and network topology to Asset Identity Center page | 7.2.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Operational Technology | Allow manual licensing for FortiGates in air-gap environments | 7.2.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Operational Technology | Configuring the Purdue Level for discovered assets based on detected interface | 7.4.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Operational Technology | Support for IEC 60870-5-101 serial to IEC 60870-5-104 TCP/IP transport | 7.4.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Operational Technology | Support for Modbus serial to Modbus TCP | 7.4.4 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Operational Technology | CLI to configure FGR-70F/FGR-70F-3G4G GPIO/DIO module alarm functionality | 7.4.6+; 7.6.1+ | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Operational Technology | SNMP traps and automation-stitch notifications for DIO module alarm functionality | 7.4.6+; 7.6.1+ | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Operational Technology | Support Ethernet layer protocols in the IPS engine | 7.6.3 and later | IDPS `SRG-NET-000390-IDPS-00212` | — |
| Operational Technology | MACsec support for FortiGate Rugged Models with hardware switch | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Operational Technology | FortiGate Rugged digital I/O trigger logging enhancement | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |
| Operational Technology | MQTT broker support on FortiGate Rugged | 8.0.0 and later | No direct requirement; if unused, disable (FGT-NDM `FGFW-ND-000200`) | — |

### Requirement reference

The STIG rules and SRG requirements used in the map and in this chapter's
text, with their severity in the current releases. The SRG ID column gives
the SRG requirement each one implements: for a STIG rule, the SRG
requirement the rule was written from; for an SRG requirement, its core SRG
ID.

[Download the requirement reference as CSV](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/data/volume-172-disa-srgs-and-stigs/30-fortigate-feature-version-and-stig-map-requirements.csv) (184 rows).

| STIG or SRG | Requirement | Severity | SRG ID | Requirement title |
| --- | --- | --- | --- | --- |
| FGT-NDM | `FGFW-ND-000005` | CAT II | `SRG-APP-000026-NDM-000208` | The FortiGate device must automatically audit account creation. |
| FGT-NDM | `FGFW-ND-000010` | CAT II | `SRG-APP-000027-NDM-000209` | The FortiGate device must automatically audit account modification. |
| FGT-NDM | `FGFW-ND-000020` | CAT II | `SRG-APP-000029-NDM-000211` | The FortiGate device must automatically audit account removal actions. |
| FGT-NDM | `FGFW-ND-000030` | CAT II | `SRG-APP-000148-NDM-000346` | The FortiGate device must have only one local account to be used as the account of last resort in the event the authentication server is unavailable. |
| FGT-NDM | `FGFW-ND-000035` | CAT II | `SRG-APP-000038-NDM-000213` | The FortiGate device must allow full access to only those individuals or roles designated by the ISSM. |
| FGT-NDM | `FGFW-ND-000040` | CAT II | `SRG-APP-000343-NDM-000289` | The FortiGate device must audit the execution of privileged functions. |
| FGT-NDM | `FGFW-ND-000045` | CAT II | `SRG-APP-000065-NDM-000214` | The FortiGate device must enforce the limit of three consecutive invalid logon attempts, after which time it must lock out the user account from accessing the device for 15 minutes. |
| FGT-NDM | `FGFW-ND-000050` | CAT II | `SRG-APP-000068-NDM-000215` | The FortiGate device must display the Standard Mandatory DoW Notice and Consent Banner before granting access to the device. |
| FGT-NDM | `FGFW-ND-000055` | CAT II | `SRG-APP-000069-NDM-000216` | The FortiGate device must retain the Standard Mandatory DoW Notice and Consent Banner on the screen until the administrator acknowledges the usage conditions and takes explicit actions to log on for further access. |
| FGT-NDM | `FGFW-ND-000060` | CAT II | `SRG-APP-000080-NDM-000220` | The FortiGate device must log all user activity. |
| FGT-NDM | `FGFW-ND-000065` | CAT II | `SRG-APP-000495-NDM-000318` | The FortiGate device must generate audit records when successful/unsuccessful attempts to modify administrator privileges occur. |
| FGT-NDM | `FGFW-ND-000070` | CAT II | `SRG-APP-000499-NDM-000319` | The FortiGate device must generate audit records when successful/unsuccessful attempts to delete administrator privileges occur. |
| FGT-NDM | `FGFW-ND-000075` | CAT II | `SRG-APP-000503-NDM-000320` | The FortiGate device must generate audit records when successful/unsuccessful logon attempts occur. |
| FGT-NDM | `FGFW-ND-000080` | CAT II | `SRG-APP-000504-NDM-000321` | The FortiGate device must generate audit records for privileged activities or other system-level access. |
| FGT-NDM | `FGFW-ND-000085` | CAT II | `SRG-APP-000505-NDM-000322` | The FortiGate device must generate audit records showing starting and ending time for administrator access to the system. |
| FGT-NDM | `FGFW-ND-000090` | CAT II | `SRG-APP-000506-NDM-000323` | The FortiGate device must generate audit records when concurrent logons from different workstations occur. |
| FGT-NDM | `FGFW-ND-000095` | CAT II | `SRG-APP-000100-NDM-000230` | The FortiGate device must generate audit records containing information that establishes the identity of any individual or process associated with the event. |
| FGT-NDM | `FGFW-ND-000100` | CAT II | `SRG-APP-000101-NDM-000231` | The FortiGate device must generate audit records containing the full-text recording of privileged commands. |
| FGT-NDM | `FGFW-ND-000105` | CAT II | `SRG-APP-000357-NDM-000293` | The FortiGate device must allocate audit record storage capacity in accordance with organization-defined audit record storage requirements. |
| FGT-NDM | `FGFW-ND-000110` | CAT II | `SRG-APP-000515-NDM-000325` | The FortiGate device must off-load audit records on to a different system or media than the system being audited. |
| FGT-NDM | `FGFW-ND-000115` | CAT II | `SRG-APP-000360-NDM-000295` | The FortiGate device must generate an immediate real-time alert of all audit failure events requiring real-time alerts. |
| FGT-NDM | `FGFW-ND-000120` | CAT II | `SRG-APP-000373-NDM-000298` | The FortiGate device must synchronize internal information system clocks using redundant authoritative time sources. |
| FGT-NDM | `FGFW-ND-000125` | CAT II | `SRG-APP-000374-NDM-000299` | The FortiGate device must record time stamps for audit records that can be mapped to Coordinated Universal Time (UTC) or Greenwich Mean Time (GMT). |
| FGT-NDM | `FGFW-ND-000130` | CAT II | `SRG-APP-000120-NDM-000237` | The FortiGate device must protect audit information from unauthorized deletion. |
| FGT-NDM | `FGFW-ND-000135` | CAT II | `SRG-APP-000121-NDM-000238` | The FortiGate device must protect audit tools from unauthorized access. |
| FGT-NDM | `FGFW-ND-000140` | CAT II | `SRG-APP-000122-NDM-000239` | The FortiGate device must protect audit tools from unauthorized modification. |
| FGT-NDM | `FGFW-ND-000145` | CAT II | `SRG-APP-000378-NDM-000302` | The FortiGate device must prohibit installation of software without explicit privileged status. |
| FGT-NDM | `FGFW-ND-000150` | CAT II | `SRG-APP-000380-NDM-000304` | The FortiGate device must enforce access restrictions associated with changes to device configuration. |
| FGT-NDM | `FGFW-ND-000155` | CAT II | `SRG-APP-000133-NDM-000244` | The FortiGate device must limit privileges to change the software resident within software libraries. |
| FGT-NDM | `FGFW-ND-000160` | CAT II | `SRG-APP-000516-NDM-000335` | The FortiGate device must enforce access restrictions associated with changes to the system components. |
| FGT-NDM | `FGFW-ND-000165` | CAT II | `SRG-APP-000516-NDM-000336` | The FortiGate device must use LDAP for authentication. |
| FGT-NDM | `FGFW-ND-000170` | CAT I | `SRG-APP-000516-NDM-000351` | The FortiGate device must be running an operating system release that is currently supported by the vendor. |
| FGT-NDM | `FGFW-ND-000175` | CAT II | `SRG-APP-000516-NDM-000334` | The FortiGate device must generate log records for a locally developed list of auditable events. |
| FGT-NDM | `FGFW-ND-000180` | CAT II | `SRG-APP-000516-NDM-000340` | The FortiGate device must conduct backups of system-level information contained in the information system when changes occur. |
| FGT-NDM | `FGFW-ND-000185` | CAT II | `SRG-APP-000516-NDM-000341` | The FortiGate device must support organizational requirements to conduct backups of information system documentation, including security-related documentation, when changes occur or weekly, whichever is sooner. |
| FGT-NDM | `FGFW-ND-000190` | CAT II | `SRG-APP-000408-NDM-000314` | FortiGate devices performing maintenance functions must restrict use of these functions to authorized personnel only. |
| FGT-NDM | `FGFW-ND-000195` | CAT II | `SRG-APP-000516-NDM-000344` | The FortiGate device must use DoW-approved Certificate Authorities (CAs) for public key certificates. |
| FGT-NDM | `FGFW-ND-000200` | CAT I | `SRG-APP-000142-NDM-000245` | The FortiGate device must prohibit the use of all unnecessary and/or non-secure functions, ports, protocols, and/or services. |
| FGT-NDM | `FGFW-ND-000205` | CAT II | `SRG-APP-000156-NDM-000250` | The FortiGate device must implement replay-resistant authentication mechanisms for network access to privileged accounts. |
| FGT-NDM | `FGFW-ND-000210` | CAT II | `SRG-APP-000395-NDM-000310` | The FortiGate device must authenticate SNMP messages using a FIPS-validated Keyed-Hash Message Authentication Code (HMAC). |
| FGT-NDM | `FGFW-ND-000215` | CAT II | `SRG-APP-000395-NDM-000347` | The FortiGate device must authenticate Network Time Protocol (NTP) sources using authentication that is cryptographically based. |
| FGT-NDM | `FGFW-ND-000220` | CAT II | `SRG-APP-000164-NDM-000252` | The FortiGate device must enforce a minimum 15-character password length. |
| FGT-NDM | `FGFW-ND-000225` | CAT II | `SRG-APP-000166-NDM-000254` | The FortiGate device must enforce password complexity by requiring that at least one uppercase character be used. |
| FGT-NDM | `FGFW-ND-000230` | CAT II | `SRG-APP-000167-NDM-000255` | The FortiGate device must enforce password complexity by requiring that at least one lowercase character be used. |
| FGT-NDM | `FGFW-ND-000235` | CAT II | `SRG-APP-000168-NDM-000256` | The FortiGate device must enforce password complexity by requiring at least one numeric character be used. |
| FGT-NDM | `FGFW-ND-000240` | CAT II | `SRG-APP-000169-NDM-000257` | The FortiGate device must enforce password complexity by requiring that at least one special character be used. |
| FGT-NDM | `FGFW-ND-000245` | CAT I | `SRG-APP-000172-NDM-000259` | The FortiGate device must use LDAPS for the LDAP connection. |
| FGT-NDM | `FGFW-ND-000250` | CAT II | `SRG-APP-000080-NDM-000345` | The FortiGate device must not have any default manufacturer passwords when deployed. |
| FGT-NDM | `FGFW-ND-000255` | CAT I | `SRG-APP-000179-NDM-000265` | The FortiGate device must use FIPS 140-2 approved algorithms for authentication to a cryptographic module. |
| FGT-NDM | `FGFW-ND-000260` | CAT I | `SRG-APP-000411-NDM-000330` | The FortiGate devices must use FIPS-validated Keyed-Hash Message Authentication Code (HMAC) to protect the integrity of nonlocal maintenance and diagnostic communications. |
| FGT-NDM | `FGFW-ND-000265` | CAT I | `SRG-APP-000412-NDM-000331` | The FortiGate device must implement cryptographic mechanisms using a FIPS 140-2 approved algorithm to protect the confidentiality of remote maintenance sessions. |
| FGT-NDM | `FGFW-ND-000270` | CAT II | `SRG-APP-000186-NDM-000266` | The FortiGate device must terminate idle sessions after 10 minutes of inactivity. |
| FGT-NDM | `FGFW-ND-000275` | CAT I | `SRG-APP-000190-NDM-000267` | The FortiGate device must terminate idle sessions after 10 minutes of inactivity. |
| FGT-NDM | `FGFW-ND-000280` | CAT II | `SRG-APP-000224-NDM-000270` | The FortiGate device must generate unique session identifiers using a FIPS 140-2-approved random number generator. |
| FGT-NDM | `FGFW-ND-000285` | CAT I | `SRG-APP-000231-NDM-000271` | The FortiGate device must only allow authorized administrators to view or change the device configuration, system files, and other files stored either in the device or on removable media (such as a flash drive). |
| FGT-NDM | `FGFW-ND-000290` | CAT II | `SRG-APP-000435-NDM-000315` | The FortiGate device must protect against known types of denial-of-service (DoS) attacks by employing organization-defined security safeguards. |
| FGT-NDM | `FGFW-ND-000295` | CAT I | `SRG-APP-000516-NDM-000350` | The FortiGate device must be configured to send log data to a central log server for the purpose of forwarding alerts to the administrators and the ISSO. |
| FGT-NDM | `FGFW-ND-000300` | CAT II | `SRG-APP-000001-NDM-000200` | The FortiGate device must limit the number of logon and user sessions. |
| FGT-NDM | `FGFW-ND-000305` | CAT II | `SRG-APP-000131-NDM-000243` | The FortiGate device must only install patches or updates that are validated by the vendor via digital signature or hash. |
| FGT-NDM | `FGFW-ND-000311` | CAT II | `SRG-APP-000170-NDM-000329` | The FortiGate device must require that when a password is changed, the characters are changed in at least eight of the positions within the password. |
| FGT-FW | `FNFG-FW-000005` | CAT I | `SRG-NET-000019-FW-000003` | The FortiGate firewall must use filters that use packet headers and packet attributes, including source and destination IP addresses and ports. |
| FGT-FW | `FNFG-FW-000015` | CAT II | `SRG-NET-000061-FW-000001` | The FortiGate firewall must use organization-defined filtering rules that apply to the monitoring of remote access traffic for the traffic from the VPN access points. |
| FGT-FW | `FNFG-FW-000020` | CAT II | `SRG-NET-000074-FW-000009` | The FortiGate firewall must generate traffic log entries containing information to establish what type of events occurred. |
| FGT-FW | `FNFG-FW-000025` | CAT II | `SRG-NET-000075-FW-000010` | The FortiGate firewall must generate traffic log entries containing information to establish when (date and time) the events occurred. |
| FGT-FW | `FNFG-FW-000030` | CAT II | `SRG-NET-000076-FW-000011` | The FortiGate firewall must generate traffic log entries containing information to establish the network location where the events occurred. |
| FGT-FW | `FNFG-FW-000035` | CAT III | `SRG-NET-000077-FW-000012` | The FortiGate firewall must generate traffic log entries containing information to establish the source of the events, such as the source IP address at a minimum. |
| FGT-FW | `FNFG-FW-000040` | CAT II | `SRG-NET-000078-FW-000013` | The FortiGate firewall must generate traffic log entries containing information to establish the outcome of the events, such as, at a minimum, the success or failure of the application of the firewall rule. |
| FGT-FW | `FNFG-FW-000045` | CAT II | `SRG-NET-000089-FW-000019` | In the event that communication with the central audit server is lost, the FortiGate firewall must continue to queue traffic log records locally. |
| FGT-FW | `FNFG-FW-000050` | CAT II | `SRG-NET-000098-FW-000021` | The FortiGate firewall must protect traffic log records from unauthorized access while in transit to the central audit server. |
| FGT-FW | `FNFG-FW-000055` | CAT II | `SRG-NET-000099-FW-000161` | The FortiGate firewall must protect the traffic log from unauthorized modification of local log records. |
| FGT-FW | `FNFG-FW-000060` | CAT I | `SRG-NET-000100-FW-000023` | The FortiGate firewall must protect the traffic log from unauthorized deletion of local log files and log records. |
| FGT-FW | `FNFG-FW-000065` | CAT II | `SRG-NET-000131-FW-000025` | The FortiGate firewall must disable or remove unnecessary network services and functions that are not used as part of its role in the architecture. |
| FGT-FW | `FNFG-FW-000070` | CAT II | `SRG-NET-000192-FW-000029` | The FortiGate firewall must block outbound traffic containing denial-of-service (DoS) attacks to protect against the use of internal information systems to launch any DoS attacks against other networks or endpoints. |
| FGT-FW | `FNFG-FW-000075` | CAT II | `SRG-NET-000193-FW-000030` | The FortiGate firewall implementation must manage excess bandwidth to limit the effects of packet flooding types of denial-of-service (DoS) attacks. |
| FGT-FW | `FNFG-FW-000085` | CAT II | `SRG-NET-000205-FW-000040` | The FortiGate firewall must filter traffic destined to the internal enclave in accordance with the specific traffic that is approved and registered in the Ports, Protocols, and Services Management (PPSM) Category Assurance List (CAL), Vulnerability Assessments (VAs) for that the enclave. |
| FGT-FW | `FNFG-FW-000090` | CAT II | `SRG-NET-000235-FW-000133` | The FortiGate firewall must fail to a secure state if the firewall filtering functions fail unexpectedly. |
| FGT-FW | `FNFG-FW-000100` | CAT II | `SRG-NET-000333-FW-000014` | The FortiGate firewall must send traffic log entries to a central audit server for management and configuration of the traffic log entries. |
| FGT-FW | `FNFG-FW-000105` | CAT II | `SRG-NET-000335-FW-000017` | If communication with the central audit server is lost, the FortiGate firewall must generate a real-time alert to, at a minimum, the SA and ISSO. |
| FGT-FW | `FNFG-FW-000110` | CAT I | `SRG-NET-000362-FW-000028` | The FortiGate firewall must employ filters that prevent or limit the effects of all types of commonly known denial-of-service (DoS) attacks, including flooding, packet sweeps, and unauthorized port scanning. |
| FGT-FW | `FNFG-FW-000115` | CAT II | `SRG-NET-000364-FW-000031` | The FortiGate firewall must apply ingress filters to traffic that is inbound to the network through any active external interface. |
| FGT-FW | `FNFG-FW-000120` | CAT II | `SRG-NET-000364-FW-000032` | The FortiGate firewall must apply egress filters to traffic outbound from the network through any internal interface. |
| FGT-FW | `FNFG-FW-000125` | CAT II | `SRG-NET-000364-FW-000035` | When employed as a premise firewall, FortiGate must block all outbound management traffic. |
| FGT-FW | `FNFG-FW-000130` | CAT II | `SRG-NET-000364-FW-000036` | The FortiGate firewall must restrict traffic entering the VPN tunnels to the management network to only the authorized management packets based on destination address. |
| FGT-FW | `FNFG-FW-000135` | CAT II | `SRG-NET-000364-FW-000040` | The FortiGate firewall must be configured to inspect all inbound and outbound traffic at the application layer. |
| FGT-FW | `FNFG-FW-000145` | CAT II | `SRG-NET-000364-FW-000042` | The FortiGate firewall must be configured to restrict it from accepting outbound packets that contain an illegitimate address in the source address field via an egress filter or by enabling Unicast Reverse Path Forwarding (uRPF). |
| FGT-FW | `FNFG-FW-000150` | CAT III | `SRG-NET-000392-FW-000042` | The FortiGate firewall must generate an alert that can be forwarded to, at a minimum, the Information System Security Officer (ISSO) and Information System Security Manager (ISSM) when denial-of-service (DoS) incidents are detected. |
| FGT-FW | `FNFG-FW-000155` | CAT II | `SRG-NET-000399-FW-000008` | The FortiGate firewall must allow authorized users to record a packet-capture-based IP, traffic type (TCP, UDP, or ICMP), or protocol. |
| FGT-FW | `FNFG-FW-000160` | CAT II | `SRG-NET-000492-FW-000006` | The FortiGate firewall must generate traffic log records when traffic is denied, restricted, or discarded. |
| FGT-FW | `FNFG-FW-000165` | CAT II | `SRG-NET-000493-FW-000007` | The FortiGate firewall must generate traffic log records when attempts are made to send packets between security zones that are not authorized to communicate. |
| IDPS | `SRG-NET-000018-IDPS-00018` | CAT II | `SRG-NET-000018` | The IPS must enforce approved authorizations by restricting or blocking the flow of harmful or suspicious communications traffic within the network. |
| IDPS | `SRG-NET-000019-IDPS-00019` | CAT II | `SRG-NET-000019` | The IPS must restrict or block harmful or suspicious communications traffic between interconnected networks based on attribute- and content-based inspection of the source, destination, headers, and/or content of the communications traffic. |
| IDPS | `SRG-NET-000019-IDPS-00187` | CAT II | `SRG-NET-000019` | The IDPS must immediately use updates made to policy filters, rules, signatures, and anomaly analysis algorithms for traffic detection and prevention functions. |
| IDPS | `SRG-NET-000113-IDPS-00013` | CAT II | `SRG-NET-000113` | The IDPS must provide audit record generation capability for detection events based on implementation of policy filters, rules, signatures, and anomaly analysis. |
| IDPS | `SRG-NET-000113-IDPS-00082` | CAT II | `SRG-NET-000113` | The IDPS must provide audit record generation capability for events where communication traffic is blocked or restricted based on policy filters, rules, signatures, and anomaly analysis. |
| IDPS | `SRG-NET-000235-IDPS-00169` | CAT II | `SRG-NET-000235` | The IDPS must fail to a secure state which maintains access control mechanisms when the IDPS hardware, software, or firmware fails on initialization/shutdown or experiences a sudden abort during normal operation. |
| IDPS | `SRG-NET-000246-IDPS-00205` | CAT II | `SRG-NET-000246` | The IDPS must automatically update malicious code protection mechanisms as new releases are available in accordance with organizational configuration management procedures. |
| IDPS | `SRG-NET-000249-IDPS-00176` | CAT II | `SRG-NET-000249` | The IPS must block malicious code. |
| IDPS | `SRG-NET-000318-IDPS-00182` | CAT II | `SRG-NET-000318` | To protect against unauthorized data mining, the IPS must prevent code injection attacks launched against application objects including, at a minimum, application URLs and application code. |
| IDPS | `SRG-NET-000318-IDPS-00183` | CAT II | `SRG-NET-000318` | To protect against unauthorized data mining, the IPS must prevent SQL injection attacks launched against data storage objects, including, at a minimum, databases, database records, and database fields. |
| IDPS | `SRG-NET-000362-IDPS-00197` | CAT II | `SRG-NET-000362` | The IPS must protect against or limit the effects of known and unknown types of denial-of-service (DoS) attacks by employing anomaly-based attack detection. |
| IDPS | `SRG-NET-000362-IDPS-00198` | CAT II | `SRG-NET-000362` | The IPS must protect against or limit the effects of known types of denial-of-service (DoS) attacks by employing signatures. |
| IDPS | `SRG-NET-000390-IDPS-00212` | CAT II | `SRG-NET-000390` | The IDPS must continuously monitor inbound communications traffic for unusual/unauthorized activities or conditions. |
| IDPS | `SRG-NET-000391-IDPS-00213` | CAT II | `SRG-NET-000391` | The IDPS must continuously monitor outbound communications traffic for unusual/unauthorized activities or conditions. |
| VPN | `SRG-NET-000019-VPN-000040` | CAT II | `SRG-NET-000019` | The VPN Gateway must ensure inbound and outbound traffic is configured with a security policy in compliance with information flow control policies. |
| VPN | `SRG-NET-000053-VPN-000170` | CAT II | `SRG-NET-000053` | The VPN Gateway must limit the number of concurrent sessions for user accounts to 1 or to an organization-defined number. |
| VPN | `SRG-NET-000062-VPN-000200` | CAT I | `SRG-NET-000062` | The TLS VPN Gateway must use TLS 1.2, at a minimum, to protect the confidentiality of sensitive data during transmission for remote access connections. |
| VPN | `SRG-NET-000063-VPN-000220` | CAT II | `SRG-NET-000063` | The VPN Gateway must be configured to use IPsec with SHA-2 at 384 bits or greater for hashing to protect the integrity of remote access sessions. |
| VPN | `SRG-NET-000074-VPN-000250` | CAT I | `SRG-NET-000074` | The IPSec VPN must be configured to use a Diffie-Hellman (DH) Group of 16 or greater for Internet Key Exchange (IKE) Phase 1. |
| VPN | `SRG-NET-000132-VPN-000450` | CAT II | `SRG-NET-000132` | The VPN Gateway must be configured to prohibit the use of all unnecessary and/or nonsecure functions, ports, protocols, and/or services, as defined in the PPSM CAL and vulnerability assessments. |
| VPN | `SRG-NET-000132-VPN-000460` | CAT II | `SRG-NET-000132` | The IPsec VPN Gateway must use IKEv2 for IPsec VPN security associations. |
| VPN | `SRG-NET-000138-VPN-000490` | CAT II | `SRG-NET-000138` | The VPN Gateway must uniquely identify and authenticate organizational users (or processes acting on behalf of organizational users). |
| VPN | `SRG-NET-000140-VPN-000500` | CAT I | `SRG-NET-000140` | The VPN Gateway must use multifactor authentication (e.g., DoD PKI) for network access to non-privileged accounts. |
| VPN | `SRG-NET-000147-VPN-000530` | CAT II | `SRG-NET-000147` | The IPsec VPN Gateway must use anti-replay mechanisms for security associations. |
| VPN | `SRG-NET-000148-VPN-000540` | CAT II | `SRG-NET-000148` | The VPN Gateway must uniquely identify all network-connected endpoint devices before establishing a connection. |
| VPN | `SRG-NET-000164-VPN-000560` | CAT II | `SRG-NET-000164` | The VPN Gateway, when utilizing PKI-based authentication, must validate certificates by constructing a certification path (which includes status information) to an accepted trust anchor. |
| VPN | `SRG-NET-000166-VPN-000580` | CAT II | `SRG-NET-000166` | The Remote Access VPN Gateway must use a separate authentication server (e.g., LDAP, RADIUS, TACACS+) to perform user authentication. |
| VPN | `SRG-NET-000166-VPN-000590` | CAT II | `SRG-NET-000166` | The VPN Gateway must map the authenticated identity to the user account for PKI-based authentication. |
| VPN | `SRG-NET-000213-VPN-000721` | CAT II | `SRG-NET-000213` | The Remote Access VPN Gateway must terminate remote access network connections after an organization-defined time period. |
| VPN | `SRG-NET-000230-VPN-000780` | CAT I | `SRG-NET-000230` | The IPSec VPN must be configured to use FIPS-validated SHA-2 at 384 bits or higher for Internet Key Exchange (IKE). |
| VPN | `SRG-NET-000230-VPN-002436` | CAT II | `SRG-NET-000230` | The VPN Gateway must use Always On VPN connections for remote computing. |
| VPN | `SRG-NET-000317-VPN-001090` | CAT I | `SRG-NET-000317` | The IPsec VPN Gateway must use AES encryption for the Internet Key Exchange (IKE) proposal to protect confidentiality of remote access sessions. |
| VPN | `SRG-NET-000337-VPN-001290` | CAT II | `SRG-NET-000337` | The VPN Gateway must renegotiate the IPsec security association (SA) after eight hours or less. |
| VPN | `SRG-NET-000337-VPN-001300` | CAT II | `SRG-NET-000337` | The VPN Gateway must renegotiate the IKE security association (SA) after eight hours or less. |
| VPN | `SRG-NET-000343-VPN-001370` | CAT II | `SRG-NET-000343` | The VPN Gateway must authenticate all network-connected endpoint devices before establishing a connection. |
| VPN | `SRG-NET-000355-VPN-002433` | CAT II | `SRG-NET-000355` | The VPN Gateway providing authentication intermediary services must only accept end entity certificates (user or machine) issued by DOD PKI or DOD-approved PKI Certification Authorities (CAs) for the establishment of VPN sessions. |
| VPN | `SRG-NET-000369-VPN-001620` | CAT II | `SRG-NET-000369` | The VPN Gateway must disable split-tunneling for remote clients VPNs. |
| VPN | `SRG-NET-000371-VPN-001640` | CAT I | `SRG-NET-000371` | The IPsec VPN Gateway must specify Perfect Forward Secrecy (PFS) during Internet Key Exchange (IKE) negotiation. |
| VPN | `SRG-NET-000371-VPN-001650` | CAT I | `SRG-NET-000371` | The VPN Gateway and Client must be configured to protect the confidentiality and integrity of transmitted information. |
| VPN | `SRG-NET-000492-VPN-001980` | CAT II | `SRG-NET-000492` | The VPN Gateway must generate log records when successful and/or unsuccessful VPN connection attempts occur. |
| VPN | `SRG-NET-000510-VPN-002180` | CAT II | `SRG-NET-000510` | The IPsec VPN Gateway IKE must use NIST FIPS-validated cryptography to implement encryption services for unclassified VPN traffic. |
| VPN | `SRG-NET-000512-VPN-002220` | CAT I | `SRG-NET-000512` | The IPsec VPN Gateway must use Internet Key Exchange (IKE) for IPsec VPN Security Associations (SAs). |
| VPN | `SRG-NET-000525-VPN-002330` | CAT I | `SRG-NET-000525` | The IPsec VPN must use AES256 or greater encryption for the IPsec proposal to protect the confidentiality of remote access sessions. |
| VPN | `SRG-NET-000530-VPN-002340` | CAT II | `SRG-NET-000530` | The TLS VPN Gateway that supports Government-only services must prohibit client negotiation to TLS 1.1, TLS 1.0, SSL 2.0, or SSL 3.0. |
| ALG | `SRG-NET-000018-ALG-000017` | CAT II | `SRG-NET-000018` | The ALG must enforce approved authorizations for controlling the flow of information within the network based on attribute- and content-based inspection of the source, destination, headers, and/or content of the communications traffic. |
| ALG | `SRG-NET-000019-ALG-000018` | CAT II | `SRG-NET-000019` | The ALG must restrict or block harmful or suspicious communications traffic by controlling the flow of information between interconnected networks based on attribute- and content-based inspection of the source, destination, headers, and/or content of the communications traffic. |
| ALG | `SRG-NET-000019-ALG-000019` | CAT II | `SRG-NET-000019` | The ALG must immediately use updates made to policy enforcement mechanisms such as policy filters, rules, signatures, and analysis algorithms for gateway and/or intermediary functions. |
| ALG | `SRG-NET-000062-ALG-000150` | CAT II | `SRG-NET-000062` | The ALG that provides intermediary services for TLS must be configured to comply with the required TLS settings in NIST SP 800-52. |
| ALG | `SRG-NET-000074-ALG-000043` | CAT II | `SRG-NET-000074` | The ALG must produce audit records containing information to establish what type of events occurred. |
| ALG | `SRG-NET-000131-ALG-000085` | CAT II | `SRG-NET-000131` | The ALG must not have unnecessary services and functions enabled. |
| ALG | `SRG-NET-000131-ALG-000086` | CAT II | `SRG-NET-000131` | The ALG must be configured to remove or disable unrelated or unneeded application proxy services. |
| ALG | `SRG-NET-000132-ALG-000087` | CAT II | `SRG-NET-000132` | The ALG must be configured to prohibit or restrict the use of functions, ports, protocols, and/or services, as defined in the PPSM CAL and vulnerability assessments. |
| ALG | `SRG-NET-000138-ALG-000063` | CAT II | `SRG-NET-000138` | The ALG providing user authentication intermediary services must uniquely identify and authenticate organizational users (or processes acting on behalf of organizational users). |
| ALG | `SRG-NET-000140-ALG-000094` | CAT II | `SRG-NET-000140` | The ALG providing user authentication intermediary services must use multifactor authentication for network access to non-privileged accounts. |
| ALG | `SRG-NET-000164-ALG-000100` | CAT II | `SRG-NET-000164` | The ALG that provides intermediary services for TLS must validate certificates used for TLS functions by performing RFC 5280-compliant certification path validation. |
| ALG | `SRG-NET-000246-ALG-000132` | CAT II | `SRG-NET-000246` | The ALG providing content filtering must update malicious code protection mechanisms and signature definitions whenever new releases are available in accordance with organizational configuration management policy. |
| ALG | `SRG-NET-000248-ALG-000133` | CAT II | `SRG-NET-000248` | The ALG providing content filtering must be configured to perform real-time scans of files from external sources at network entry/exit points as they are downloaded and prior to being opened or executed. |
| ALG | `SRG-NET-000249-ALG-000134` | CAT II | `SRG-NET-000249` | The ALG providing content filtering must block malicious code upon detection. |
| ALG | `SRG-NET-000249-ALG-000145` | CAT II | `SRG-NET-000249` | The ALG providing content filtering must delete or quarantine malicious code in response to malicious code detection. |
| ALG | `SRG-NET-000288-ALG-000109` | CAT II | `SRG-NET-000288` | The ALG providing content filtering must block or restrict detected prohibited mobile code. |
| ALG | `SRG-NET-000384-ALG-000136` | CAT II | `SRG-NET-000384` | The ALG providing content filtering must detect use of network services that have not been authorized or approved by the ISSM and ISSO, at a minimum. |
| ALG | `SRG-NET-000390-ALG-000139` | CAT II | `SRG-NET-000390` | The ALG providing content filtering must continuously monitor inbound communications traffic crossing internal security boundaries for unusual or unauthorized activities or conditions. |
| ALG | `SRG-NET-000391-ALG-000140` | CAT II | `SRG-NET-000391` | The ALG providing content filtering must continuously monitor outbound communications traffic crossing internal security boundaries for unusual/unauthorized activities or conditions. |
| ALG | `SRG-NET-000400-ALG-000097` | CAT I | `SRG-NET-000400` | The ALG providing user authentication intermediary services must transmit only encrypted representations of passwords. |
| ALG | `SRG-NET-000512-ALG-000066` | CAT II | `SRG-NET-000512` | The ALG that provides intermediary services for HTTP must inspect inbound and outbound HTTP traffic for protocol compliance and protocol anomalies. |
| ALG | `SRG-NET-000750-ALG-000140` | CAT II | `SRG-NET-000750` | The ALG must include only approved trust anchors in trust stores or certificate stores managed by the organization. |
| RTR | `SRG-NET-000018-RTR-000001` | CAT II | `SRG-NET-000018` | The router must be configured to enforce approved authorizations for controlling the flow of information within the network based on organization-defined information flow control policies. |
| RTR | `SRG-NET-000018-RTR-000002` | CAT II | `SRG-NET-000018` | The BGP router must be configured to reject inbound route advertisements for any Bogon prefixes. |
| RTR | `SRG-NET-000018-RTR-000003` | CAT II | `SRG-NET-000018` | The BGP router must be configured to reject inbound route advertisements for any prefixes belonging to the local autonomous system (AS). |
| RTR | `SRG-NET-000131-RTR-000035` | CAT III | `SRG-NET-000131` | The router must be configured to have all non-essential capabilities disabled. |
| RTR | `SRG-NET-000168-RTR-000078` | CAT II | `SRG-NET-000168` | The router must be configured to authenticate all routing protocol messages using NIST-validated FIPS 198-1 message authentication code algorithm. |
| RTR | `SRG-NET-000202-RTR-000001` | CAT I | `SRG-NET-000202` | The perimeter router must be configured to deny network traffic by default and allow network traffic by exception. |
| RTR | `SRG-NET-000205-RTR-000001` | CAT I | `SRG-NET-000205` | The router must be configured to restrict traffic destined to itself. |
| RTR | `SRG-NET-000205-RTR-000014` | CAT I | `SRG-NET-000205` | The perimeter router must be configured to restrict it from accepting outbound IP packets that contain an illegitimate address in the source address field via egress filter or by enabling Unicast Reverse Path Forwarding (uRPF). |
| RTR | `SRG-NET-000230-RTR-000001` | CAT II | `SRG-NET-000230` | The router must be configured to implement message authentication for all control plane protocols. |
| RTR | `SRG-NET-000230-RTR-000002` | CAT II | `SRG-NET-000230` | The BGP router must be configured to use a unique key for each autonomous system (AS) that it peers with. |
| RTR | `SRG-NET-000230-RTR-000003` | CAT II | `SRG-NET-000230` | The router must be configured to use keys with a duration not exceeding 180 days for authenticating routing protocol messages. |
| RTR | `SRG-NET-000362-RTR-000112` | CAT III | `SRG-NET-000362` | The router must be configured to have IP directed broadcast disabled on all interfaces. |
| RTR | `SRG-NET-000362-RTR-000115` | CAT II | `SRG-NET-000362` | The router must be configured to have Internet Control Message Protocol (ICMP) redirects disabled on all external interfaces. |
| RTR | `SRG-NET-000362-RTR-000117` | CAT II | `SRG-NET-000362` | The BGP router must be configured to use the maximum prefixes feature to protect against route table flooding and prefix de-aggregation attacks. |
| RTR | `SRG-NET-000364-RTR-000111` | CAT III | `SRG-NET-000364` | The perimeter router must be configured to have Link Layer Discovery Protocols (LLDPs) disabled on all external interfaces. |
| RTR | `SRG-NET-000364-RTR-000113` | CAT II | `SRG-NET-000364` | The perimeter router must be configured to block all outbound management traffic. |
| CC | `SRG-NET-000205-CLD-000085` | CAT I | `SRG-NET-000205` | The Infrastructure as a Service (IaaS)/Platform as a Service (PaaS) must implement a security stack that restricts traffic flow inbound and outbound between the IaaS and the Boundary Cloud Access Point (BCAP) or Internal Cloud Access Point (ICAP) connection. |
| CC | `SRG-NET-000205-CLD-000090` | CAT I | `SRG-NET-000205` | The Mission Owner's internet-facing applications must be configured to traverse the Cloud Access Point (CAP) and Virtual Datacenter Security Stack (VDSS) prior to communicating with the internet. |
| CC | `SRG-NET-000205-CLD-000100` | CAT II | `SRG-NET-000205` | The Infrastructure as a Service (IaaS)/Platform as a Service (PaaS) must be configured to maintain separation of all management and data traffic. |
| CC | `SRG-NET-000383-CLD-000105` | CAT I | `SRG-NET-000383` | For Infrastructure as a Service (IaaS)/Platform as a Service (PaaS), the Mission Owner must configure an intrusion detection and prevention system (IDPS) to protect DOD virtual machines (VMs), services, and applications. |
| CC | `SRG-NET-000390-CLD-000110` | CAT II | `SRG-NET-000390` | The Mission Owner of the Infrastructure as a Service (IaaS) or Platform as a Service (PaaS) must continuously monitor and protect inbound communications from external systems, other IaaS within the same cloud service environment, or collocated mission applications for unusual or unauthorized activities or conditions. |
| CC | `SRG-NET-000391-CLD-000115` | CAT II | `SRG-NET-000391` | The Mission Owner of the Infrastructure as a Service (IaaS) must continuously monitor outbound communications to other systems and enclaves for unusual or unauthorized activities or conditions. |
| CC | `SRG-OS-000001-CLD-000010` | CAT I | `SRG-OS-000001` | The Mission Owner must configure the customer service portal credentials for least privilege. |
| CC | `SRG-OS-000096-CLD-000060` | CAT II | `SRG-OS-000096` | The Mission Owner must configure the Infrastructure as a Service (IaaS)/Platform as a Service (PaaS) to prohibit or restrict the use of functions, ports, protocols, and/or services. |
| CC | `SRG-OS-000342-CLD-000020` | CAT II | `SRG-OS-000342` | The Infrastructure as a Service (IaaS)/Platform as a Service (PaaS) must perform centralized logging to capture and store log records. |
| CC | `SRG-OS-000368-CLD-000040` | CAT II | `SRG-OS-000368` | For Impact Levels 4 and 5, the Mission Owner must register all cloud-based services, their CSP/CSO, and connection method in the DISA Systems/Network Approval Process (SNAP) database Cloud Module. |
| CC | `SRG-OS-000368-CLD-000045` | CAT II | `SRG-OS-000368` | The Mission Owner of the Infrastructure as a Service (IaaS)/Platform as a Service (PaaS) must remove orphaned or unused virtual machine (VM) instances. |
| CC | `SRG-OS-000480-CLD-000025` | CAT II | `SRG-OS-000480` | The Mission owner must obtain Authorizing Official (AO) authorization for each cloud service offering (CSO) implemented in support of production or development environments prior to operational use. |
| CC | `SRG-OS-000480-CLD-000031` | CAT I | `SRG-OS-000480` | The Mission Owner must select and configure an Impact Level 4/5 cloud service offering (CSO) listed in the DISA Provisional Authorization (PA) DOD Cloud Catalog when hosting Controlled Unclassified Information (CUI). |

### Collecting evidence

Run `get system status` on the CLI and keep the output with the checklist,
together with a full configuration backup (`execute backup config sftp`,
or a FortiManager revision). Keep the output of `show system global`,
`show system admin`, `show system accprofile`, `show system
password-policy`, `show system interface`, `show log eventfilter`, `show
log setting`, `show log syslogd setting`, `show log fortianalyzer setting`,
`show system ntp`, `show system snmp user`, `show system fips-cc`, `show
firewall policy`, and `show firewall DoS-policy`, in every VDOM where the
setting is per VDOM. Add screenshots of *System > Administrators*, *System
> Admin Profiles*, *System > Settings*, *Log & Report > Log Settings*, and
*Security Fabric > Automation*. For each enabled function outside the
STIGs, keep the security profiles and the VPN, proxy, and routing
configuration as evidence for its SRG. Export a sample of the event and
traffic logs from FortiAnalyzer or the syslog server, showing the CLI audit
log entries and denied traffic, and keep the firmware upgrade history.

## Validation and Troubleshooting

- **A feature in the map is missing on your FortiGate.** Check the version
  column against your release (a backported feature may need a later patch
  in your train), and check whether the feature depends on the model, the
  RAM, NP or SOC acceleration, the license, or the cloud platform.
- **A STIG fix command is rejected.** Some fix texts predate the current
  CLI (`config firewall policy6`, `change-8-characters`, `security-level
  auth`). Use the command in the map, which was checked against the 8.0.1
  CLI Reference, and `?` on the CLI to list the options of your release.
- **Administrators are locked out after hardening.** Check the trusted
  hosts, the interface access list, `admin-restrict-local`, the remote
  server group, and the LDAPS CA certificate. Keep console access and the
  local account of last resort available while you test.
- **Logs stop reaching the central server.** Check the reliable syslog or
  FortiAnalyzer connection, the TLS settings and certificate on both sides,
  the source interface, and the automation stitches that should have
  alerted on the failure.
- **Traffic breaks after enabling FIPS-CC mode or strong cryptography.**
  Check VPN peers, SNMP managers, LDAP servers, and management tools for
  algorithms that are no longer allowed, and update them rather than
  weakening the FortiGate.
- **A requirement has no matching feature.** Some rules are met by
  procedure (firmware hash checks, the local audit list), by another system
  (the directory, FortiAnalyzer, the cloud environment), or not exactly at
  all. Record how each rule is met, not only which feature covers it.

## Security and Best Practices

- Keep FortiOS on a vendor-supported release and patch promptly; verify
  each image's signature or hash before installing it.
- Allow HTTPS and SSH only on the management interface, with TLS 1.2 or
  1.3, strong cryptography, FIPS-CC mode, a 10-minute idle timeout,
  lockout after three failures for 15 minutes, the DoD banner, trusted hosts,
  and local-in policies.
- Use LDAPS for administrators, one local account of last resort with a
  changed default password, and administrator profiles that limit System
  and Log and Report access to the administrators who need it.
- Enforce a 15-character administrator password with all character classes.
- Enable system and user event logging, the CLI audit log, traffic logging
  on every policy and on the implicit deny, and send logs to FortiAnalyzer
  or a reliable, encrypted syslog server with local disk logging as a
  queue; alert on every log failure event.
- Use authenticated NTP from two servers, SNMPv3 with SHA-256 and AES, and
  CA certificates from DoD-approved CAs only.
- Deny by default, allow only PPSM-registered traffic, apply DoS policies on
  every exposed interface, disable asymmetric routing, and keep IPS and
  antivirus fail-closed.
- Assess every enabled security profile, VPN, proxy, and routing protocol
  against its SRG, and disable the rest.
- Review this map each time Fortinet publishes a FortiOS release or DISA
  updates the FortiGate STIGs.

## References and Knowledge Checks

**References:**

- Fortinet, *FortiOS 7.0.0 New Features Guide*, *FortiOS 7.2.0 New Features
  Guide*, *FortiOS 7.4.0 New Features Guide*, *FortiOS 7.6.0 New Features
  Guide*, and *FortiOS 8.0.0 New Features Guide* (each covering its whole
  release train), with their tables of contents on docs.fortinet.com.
- Fortinet, *FortiOS 8.0.1 CLI Reference*, and the *FortiOS 7.6.0 CLI
  Reference* (for `min-change-characters`).
- DISA Fortinet FortiGate Firewall NDM STIG V1R6 and Fortinet FortiGate
  Firewall STIG V1R5 (`U_FN_FortiGate_Firewall_Y26M10_STIG.zip`), the
  Intrusion Detection and Prevention Systems SRG V3R4, the Virtual Private
  Network SRG V3R5, the Application Layer Gateway SRG V2R4, the Router SRG
  V5R2, and the Cloud Computing Mission Owner Operating System SRG V1R3
  and Network SRG V1R2, from the October 2026 STIG Library Compilation.
- [Chapter 03](03-the-srg-catalog-how-stigs-are-built-and-what-to-do-without-one.md)
  (SRG-based assessment),
  [Chapter 10](10-fortinet-products-stigs-and-srg-mapping.md) (Fortinet
  products and the FortiGate STIGs),
  [Chapter 11](11-fortiswitch-feature-version-and-srg-map.md) (the
  FortiSwitch map),
  [Chapter 12](12-fortianalyzer-feature-version-and-srg-map.md) (the
  FortiAnalyzer map, the model for this chapter),
  [Chapter 13](13-fortimanager-feature-version-and-srg-map.md) (FortiManager),
  [Chapter 14](14-fortiap-feature-version-and-srg-map.md) (FortiOS CLI
  verification), and
  [Chapter 29](29-fortisase-feature-version-and-srg-map.md) (the Cloud
  Computing SRG).

**Knowledge checks:**

1. Which two STIGs apply to FortiGate, and which SRG does each STIG rule
   implement? Where in the map do you find that?
2. Which SRGs cover a FortiGate that also runs IPS, IPsec VPN, web
   filtering, and BGP?
3. Which rule do the "No direct requirement" rows point to, and why?
4. Name three STIG fix commands that do not match the 8.0.1 CLI, and what
   the map uses instead.
5. How does the Firewall STIG make FortiGate alert when the syslog server
   stops receiving logs?
6. What does the Cloud Computing SRG ask of the Mission Owner when FortiGate
   VM runs in IaaS, and how does the FortiGate VM help meet it?

## Summary and Completion Checklist

FortiGate is the only Fortinet product with DISA STIGs: the FortiGate
Firewall NDM STIG for the management plane and the FortiGate Firewall STIG
for traffic filtering. This chapter maps 1363 features to the FortiOS
release that introduced them, to 184 requirements (60
FGT-NDM rules, 29 FGT-FW rules, 14 IDPS, 30 VPN,
22 ALG, 16 RTR, and 13 CC), and to the command that
configures them: 72 core platform features and 1291 features from
the FortiOS 7.0 through 8.0 New Features Guides, of which 190 map to
a requirement and 1101 fall under the rule to disable unnecessary
functions when unused. Every one of the 89 STIG rules is in the map, with
its fix text as the command, checked against the 8.0.1 CLI Reference.

- [ ] Can find the release that introduced a FortiGate feature.
- [ ] Can find each FortiGate STIG rule in the map, with its severity and
  SRG requirement.
- [ ] Can configure each rule with its fix text and recognize where the fix
  text no longer matches the CLI.
- [ ] Can map FortiGate functions outside the STIGs to their SRGs.
- [ ] Can explain the Cloud Computing SRG obligations for FortiGate VM in
  public cloud.
- [ ] Can collect FortiGate's evidence and record the rules it cannot meet
  exactly.
