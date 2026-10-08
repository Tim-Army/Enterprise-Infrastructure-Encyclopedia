# Chapter 20: FortiDDoS Feature, Version, and SRG Map

## Learning Objectives

- Find the FortiDDoS-F release that introduced a given feature.
- Map each FortiDDoS feature to the Network Device Management (NDM) or
  Firewall (FW) SRG requirement it helps satisfy.
- Explain which Firewall SRG requirements apply to a DDoS mitigation
  appliance, and which do not.
- Find the FortiDDoS command, or the web UI pane, that configures each
  feature to meet its requirement.
- Use the map to scope an SRG-based assessment of FortiDDoS, which has no
  STIG of its own.
- Record the requirements that FortiDDoS cannot meet exactly, with their
  mitigations.

## Theory and Architecture

FortiDDoS is Fortinet's distributed denial-of-service (DDoS) detection and
mitigation appliance. It sits inline between the external network and
the protected services as a transparent device: its traffic ports have no
IP or MAC addresses in the data path, and it is managed through separate
management ports. Instead of signatures, it learns the normal rates of
many thousands of Layer 3, 4, and 7 parameters for each group of protected
servers, sets thresholds from that traffic, and drops packets that exceed
them or that break protocol rules. It has **no DISA STIG** (Chapter 10), so it is assessed against
SRGs, as described in Chapter 03. Chapter 10 assigns it the **Network
Device Management (NDM) SRG** for the management plane, the way
administrators log in to and configure the appliance, and notes that its
filtering role relates to the **denial-of-service requirements of the
Firewall (FW) SRG**. For every FortiDDoS feature the chapter gives **which
FortiDDoS-F release introduced it**, **which requirement it relates to**,
and **which command or web UI pane configures it to meet that
requirement**.

Fortinet sells two FortiDDoS product lines with separate firmware. The
older B- and E-Series appliances run FortiDDoS 5.x (5.7.4 is the newest
release on docs.fortinet.com). The current **FortiDDoS-F** (F-Series)
hardware and the FortiDDoS VM run the FortiDDoS-F firmware, which started
at 6.1.0 and is documented in trains 6.1 through 8.0. This chapter covers
FortiDDoS-F; "FortiDDoS" below means FortiDDoS-F. Its configuration uses
a few objects again and again:

- **Service Protection Policies (SPPs)** (`config ddos spp rule`) group the
  protected subnets of servers with similar traffic. Each SPP has its own
  operating mode for each direction, **Detection Mode** (log only) or
  **Prevention Mode** (drop), its own learned traffic statistics, and its
  own thresholds.
- **Thresholds** are set for each SPP from **Traffic Statistics** and
  **System Recommendations**, then adjusted continuously by adaptive
  thresholds. Floods are drops caused by a threshold; anomalies are drops
  caused by a protocol rule; ACL drops are caused by an access list.
- **Profiles** (IP, ICMP, TCP, HTTP, SSL/TLS, NTP, DNS, DTLS, QUIC, and
  Video Conference) hold the anomaly checks, validation methods, and ACLs
  of a protocol, and are assigned to SPPs.
- **Global protection** settings apply to all traffic: the deployment mode
  (inline, asymmetric, or tap), the power fail bypass mode, global ACLs,
  IPv4 and domain blocklists, Do Not Track policies, tunnel endpoints, and
  cloud signaling to an upstream scrubbing service.
- **System settings** (`config system admin`,
  `config system password-policy`, `config system interface`, the
  authentication servers, SNMP, NTP, and `config log setting`) cover the
  management plane.

### Where the version data comes from

Fortinet publishes no Feature Matrix or New Features guide for
FortiDDoS-F, and the FortiDDoS-F Handbook has a "What's New" chapter for
its own train only. The **Release Notes** of every FortiDDoS-F release
have a "What's new" page, so the version column was built from those pages:
6.1.0 through 6.1.5, 6.2.0 through 6.2.3, 6.3.0 through 6.3.3 and 6.3.5,
6.4.0 through 6.4.2, 6.5.0 and 6.5.1, 6.6.0, 6.6.1, and 6.6.3, 7.0.0 through
7.0.5, 7.2.0 through 7.2.4, and 8.0.0 and 8.0.1. That is every release
Fortinet publishes on docs.fortinet.com for the 6.1 to 8.0 trains. Release
6.3.0 has no release notes of its own; its "What's new" page is a section of
the 6.3.1 release notes. Each feature is a heading on the page, or, on the
pages without feature headings, a top-level bullet. Three adjustments were
made:

- The 6.1.0 page lists the features that FortiDDoS-F added to the
  B/E-Series feature base; the 6.1.1 to 6.1.3 pages repeat that list, and
  only the 6.1.0 copy was used. Their lists of B/E-Series functions that
  FortiDDoS-F does not include, and of VM limits, are not features.
- The 6.6.1 page repeats the 6.6.0 list "for reference" and was skipped.
- The 7.2.2 page leaves a nested list unclosed in its HTML, so its later
  top-level bullets were read as top-level entries.

Thirteen releases add no features: 6.1.3, 6.1.4, 6.1.5, 6.2.2, 6.2.3,
6.3.5, 6.4.2, 6.6.1, 6.6.3, 7.0.2, 7.0.5, 7.2.3, and 7.2.4 are patch releases
whose "What's new" page says that they have no new features.

The table has two groups of rows:

- **Core platform features** (categories starting with *Core:*) are the
  long-standing capabilities that the requirements depend on: management
  access, administrator accounts and access profiles, password policy,
  logging and alerts, time, SNMP, firmware and backups, certificates, high
  availability, and the DDoS mitigation functions themselves (SPPs,
  operating modes, thresholds, anomaly checks, ACLs, blocklists, and the
  bypass mode). They existed in FortiDDoS-F 6.1.0, which "is built on the
  feature base of FortiDDoS B/E-Series", and are not in these lists; they
  were taken from the FortiDDoS-F 8.0.0 Handbook.
- **New features** are the 246 entries of the "What's new" pages.
  The categories were assigned for this chapter, because the release notes
  have none or use different ones from release to release, and the titles
  were shortened from the release notes text. An entry listed again in a
  later release or train is one row with all its versions.

| Version entry | Meaning |
| --- | --- |
| `6.1.0 or earlier` | A core feature that predates the oldest release notes used (FortiDDoS-F 6.1.0) |
| `6.4.0 and later` | Introduced in FortiDDoS-F 6.4.0 |
| `6.6.0+; 7.0.0+` | Listed in two trains: from 6.6.0 in the 6.6 train and from 7.0.0 in the 7.0 train |

Three cautions apply. First, "and later" means later in the same train
and, usually, in later trains; a feature of a patch release may reach a
newer train only in a later patch. Second, many features apply only to
some models (the 200F, 1500F, 2000F, 3000F, or the VM) or to a FortiGuard
subscription (IP reputation and domain reputation). Third, a core row
records a FortiDDoS capability, but its command or pane was checked
against the 8.0.0 Handbook and may differ on an older release: several
settings it uses arrived later, as the new-feature rows say (remote
administrator authentication in 6.3.0, the 5-minute default idle timeout
in 6.6.0, TCP syslog in 7.0.1, management TLS versions in 7.0.0, and the
pre-login banner in 8.0.0), and the *System > Settings* pane was
*System > Admin > Settings* before 8.0.0. FortiDDoS-F 8.0.1 has release
notes but, at the time of writing, no Handbook of its own.

### Where the SRG data comes from

The SRG column uses requirement IDs from the October 2026 DISA library:

| SRG column | SRG | Release | Applies to |
| --- | --- | --- | --- |
| **NDM** | Network Device Management SRG | V5R5, benchmark date 01 Jul 2026 | The management plane: administrator access, authentication, logging, time, SNMP, firmware, and backups (assigned by Chapter 10) |
| **FW** | Firewall SRG | V3R4, benchmark date 01 Jul 2026 | The DDoS filtering function: the denial-of-service, flooding, and bandwidth requirements, and the filtering, failure, and logging requirements that support them (from Chapter 10's note on FortiDDoS's filtering role) |

FortiDDoS is not a firewall: it passes all traffic that it does not
identify as an attack, and it leaves stateful access control to the
firewall behind it. So only part of the Firewall SRG applies, and this
chapter cites only those requirements:

- **Denial-of-service requirements, the core of FortiDDoS:** filters that
  prevent or limit commonly known DoS attacks, including floods and scans
  (FW `SRG-NET-000362-FW-000028`, CAT I); management of excess bandwidth
  against packet floods (FW `SRG-NET-000193-FW-000030`); blocking of
  outbound DoS attacks (FW `SRG-NET-000192-FW-000029`); organization-defined
  controls by type of DoS (FW `SRG-NET-000705-FW-000110`); and an alert to
  the ISSO and ISSM when DoS incidents are detected
  (FW `SRG-NET-000392-FW-000042`).
- **Related filtering:** filters on packet headers such as addresses and
  ports (FW `SRG-NET-000019-FW-000003`), ingress and egress filters
  (FW `SRG-NET-000364-FW-000031`, FW `SRG-NET-000364-FW-000032`), and
  blocking of illegitimate source addresses (FW `SRG-NET-000364-FW-000042`),
  which FortiDDoS meets with its ACLs, blocklists, reputation feeds, and
  address anomaly checks.
- **Failure:** failing to a secure state (FW `SRG-NET-000235-FW-000133`),
  which for FortiDDoS is the choice between fail-open and fail-closed.
- **Logging of the filtering decisions:** the content of the drop records
  (FW `SRG-NET-000074-FW-000009` through FW `SRG-NET-000078-FW-000013`),
  logging of dropped traffic (FW `SRG-NET-000492-FW-000006`), sending the
  records to a central server over TCP (FW `SRG-NET-000333-FW-000014`,
  FW `SRG-NET-000098-FW-000021`), protecting them
  (FW `SRG-NET-000099-FW-000161`, FW `SRG-NET-000100-FW-000023`), and
  alerting when the central server is lost (FW `SRG-NET-000335-FW-000017`).

The other Firewall SRG requirements are left out because they describe a
firewall's own job: deny by default and permit by exception, filtering by
the PPSM CAL, security zones, application-layer and IPv6 extension header
inspection of all traffic, the VPN and management traffic rules, subnet
isolation, and alternate communication paths. Those requirements belong to
the firewall behind FortiDDoS. The requirement not to run unnecessary
functions is taken from the NDM SRG for every row (below).

The requirement IDs are the **rule version IDs** from the XCCDF files, and
the severity is the rule's severity (high = CAT I, medium = CAT II, low =
CAT III). Each feature maps to one of three kinds of relationship:

- **Implements a requirement.** The feature is how FortiDDoS meets a
  requirement. Rate thresholds with adaptive learning implement the
  requirement to limit the effects of known DoS attacks
  (FW `SRG-NET-000362-FW-000028`), for example.
- **Must be configured to meet a requirement.** The feature is in scope of
  a requirement and has to be set up correctly. The password policy must
  require 15 characters and all four character types
  (NDM `SRG-APP-000164-NDM-000252`), for example.
- **No direct requirement.** The feature is operational, such as a
  platform, a GUI change, a graph, or a troubleshooting command. It has no
  requirement of its own, but if it is not needed it falls under the NDM
  requirement not to have unnecessary functions enabled
  (NDM `SRG-APP-000142-NDM-000245`).

The mapping is a starting point for an assessment, not a ruling. Confirm it
with your assessor, especially where a requirement is organization-defined
or depends on how FortiDDoS is deployed.

### Where the commands come from

Fortinet publishes **no CLI Reference for FortiDDoS-F**: the FortiDDoS-F
pages on docs.fortinet.com hold only the Handbook, the release notes, and
the VM and KVM deployment guides. The **FortiDDoS-F 8.0.0 Handbook** (dated
11 August 2026), the newest Handbook, prints the CLI syntax or an example
for many settings, next to the web UI procedure. Every command in the
table was checked against those CLI blocks, and every web UI pane against
the Handbook text. The check was automatic: each `config` path and nested
table, each `set` option against the block of the command it is entered
under, each listed option value against the documented values, each
`execute` and `get` command, and each GUI pane name. Where the Handbook
gives no CLI for a setting, the table names the web UI pane. Read the
column this way:

- Commands run on the FortiDDoS CLI, over SSH, the console, or the CLI
  Console in the web UI. The CLI is open to the admin account and to
  administrators with the super_admin_prof or a full read-write access
  profile; remote CLI users need super_admin_prof. `<SPP>` is the name of a Service
  Protection Policy and `<ADMIN>` the name of an administrator account.
- **GUI:** entries name the FortiDDoS web UI pane.
- Statements are separated by `;` to fit in a table cell; on the CLI, enter
  each one on its own line. Values in `<ANGLE_BRACKETS>` are placeholders
  for your own names, addresses, and keys.
- For **"No direct requirement"** rows, the command shown is the one that
  disables the feature when it is unused. A dash (**—**) means there is
  nothing to change: the feature is a platform, a GUI change, a behavior
  change, a graph or log detail, a troubleshooting command, or a
  capability that is off unless configured, or the Handbook has no
  setting for it.

Some requirements cannot be met exactly with FortiDDoS settings. Record
them on the checklist as open findings with mitigations, or meet them
another way:

- **No PKI login for administrators.** The administrator authentication
  types in the 8.0.0 Handbook are local, LDAP, RADIUS, and TACACS+; there is
  no certificate (CAC) login, and two-factor authentication is supported
  only through RADIUS (not LDAP or TACACS+). DoD PKI multifactor
  authentication for interactive logins (NDM `SRG-APP-000149-NDM-000247`,
  CAT I) cannot be met by FortiDDoS itself. Authenticate administrators
  against a RADIUS server that enforces DoD PKI or another approved second
  factor, keep one local account of last resort, and record the finding.
- **No FIPS mode.** The 8.0.0 Handbook does not mention FIPS 140 at all.
  The FIPS requirements (NDM `SRG-APP-000179-NDM-000265`,
  NDM `SRG-APP-000412-NDM-000331`, NDM `SRG-APP-000411-NDM-000330`) are met,
  if at all, by allowing only TLS 1.2 and 1.3 on the management ports
  (7.0.0 and later) and SNMPv3 with SHA and AES. Check the NIST
  Cryptographic Module Validation Program for a certificate covering your
  FortiDDoS release.
- **Login lockout.** After three failed logins FortiDDoS blocks the source
  IP address for five minutes, and each further attempt extends the block
  by five minutes. The behavior is fixed, and the five-minute block is
  shorter than the 15 minutes required (NDM `SRG-APP-000065-NDM-000214`).
  Enforce the lockout on the remote authentication server and restrict
  logins with trusted hosts.
- **Banner before 8.0.0.** The pre-login warning banner was added in 8.0.0
  (NDM `SRG-APP-000068-NDM-000215`, NDM `SRG-APP-000069-NDM-000216`), and
  it is off by default. Earlier releases have no banner; upgrade, or record
  the finding.
- **Password rules.** The password policy sets the minimum length (8 to
  32) and the character types, and applies only to new or changed
  passwords. The administrator password field accepts at most 16
  characters and a limited set of special characters, so long passphrases
  with spaces (NDM `SRG-APP-000860-NDM-000250`) are not possible. There is
  no setting for the number of changed characters
  (NDM `SRG-APP-000170-NDM-000329`) or a check against a list of commonly
  used or compromised passwords (NDM `SRG-APP-000845-NDM-000220`). Prefer
  remote authentication for administrators.
- **Concurrent administrator sessions.** No setting limits the number of
  sessions per administrator (NDM `SRG-APP-000001-NDM-000200`). Record the
  finding, or enforce the limit on the authentication server.
- **NTP authentication.** The NTP settings are only the servers and the
  synchronization interval; there is no NTP authentication
  (NDM `SRG-APP-000395-NDM-000347`). Use NTP servers on the protected
  management network and record the finding.
- **Log transport.** The Handbook's security hardening appendix says that
  FortiDDoS encrypts logs only to FortiAnalyzer and FortiManager and not to
  third-party syslog servers, and its FortiManager and FortiAnalyzer
  appendix even says that RFC 5424 and encrypted OFTP are not supported,
  although the 6.6.0 and 7.0.0 release notes and the remote log CLI add
  them. Check the behavior on your release. TCP syslog arrived in 7.0.1
  (FW `SRG-NET-000098-FW-000021`). Nothing in the Handbook alerts when the
  central log server stops accepting logs (FW `SRG-NET-000335-FW-000017`);
  monitor log arrival on the log server and alert from there.
- **Firmware signatures.** The Handbook mentions an integrity check during
  a CLI firmware upgrade but does not say that FortiDDoS verifies a digital
  signature on the image (NDM `SRG-APP-000131-NDM-000243`). Compare the
  image checksum with the one on the Fortinet support site before every
  upgrade.
- **Fail-open by default.** On power or system failure, copper and LC
  bypass ports fail open by default and pass traffic without inspection,
  and the out-of-memory action passes traffic by default. Fail-closed
  meets the secure-state requirement (FW `SRG-NET-000235-FW-000133`) but
  stops the protected links when FortiDDoS fails; many sites choose
  fail-open, or an HA pair, for availability. Decide with the authorizing
  official, and record the decision. Optical ports always fail closed
  unless they use a bypass module, and a VM depends on its host.
- **Settings with no command.** The Handbook has no CLI for the idle
  timeout, the management TLS versions, the banner, access profiles,
  SNMPv3 privacy, or most protection profile options, so those rows name
  the web UI pane. It also has no syntax for the shell access setting of
  6.4.1, so that row ends in a dash.

## Design Considerations

- **Pick the release first, then the features.** If your design depends on
  a feature introduced in a certain release (remote administrator
  authentication in 6.3.0, RADIUS two-factor authentication in 6.5.0,
  management TLS versions in 7.0.0, TCP syslog in 7.0.1, or the pre-login
  banner in 8.0.0), that sets the minimum FortiDDoS-F release, and it must
  be a vendor-supported release (NDM `SRG-APP-001035-NDM-000340`).
- **Keep management out of band.** Allow HTTPS and SSH only on a management
  port on a dedicated management network, restrict every administrator
  with trusted hosts, and never reach the management ports through the
  protected links.
- **Learn before you block.** Run each new SPP in Detection Mode while
  Traffic Statistics are collected, apply System Recommended thresholds,
  review the attack log for false positives, and only then switch the SPP
  to Prevention Mode in both directions.
- **Design SPPs around traffic, not organization.** Group servers with
  similar traffic (DNS servers, web servers, firewall NAT pools) in their
  own SPPs, so thresholds fit each group and profile options such as the
  inbound SYN service ACL can be used safely.
- **Decide the failure behavior on purpose.** Choose fail-open or
  fail-closed for each link, HA, and an external bypass bridge with the
  availability and security owners, and document the decision against
  FW `SRG-NET-000235-FW-000133`.
- **Log every drop off the box.** Send the DDoS attack log and the event
  log to a central log server over TCP (or encrypted OFTP to
  FortiAnalyzer), with alert email and SNMP traps for attacks and for log
  disk use.
- **Turn off what is not used.** Telnet, HTTP, the SQL access option, SNMP
  v1 and v2c, the Security Fabric connection, FortiGuard telemetry, proxy
  tunneling, Tap Mode, and Do Not Track entries all need a reason to stay
  on.

## Implementation and Automation

### The FortiDDoS feature map

The SRG column uses the abbreviations defined in *Where the SRG data comes
from*. The requirement titles are listed in the next table. The command
column follows the conventions in *Where the commands come from*.

[Download the feature map as CSV](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/data/volume-172-disa-srgs-and-stigs/20-fortiddos-feature-version-and-srg-map-feature-map.csv) (292 rows).

| Category | Feature | Introduced (FortiDDoS-F) | SRG requirement(s) | Command to satisfy the requirement |
| --- | --- | --- | --- | --- |
| Core: Management access | Administrative access per management port (HTTPS, SSH, ping, SNMP, HTTP, Telnet, SQL) | 6.1.0 or earlier | NDM `SRG-APP-000142-NDM-000245`; NDM `SRG-APP-000412-NDM-000331`; NDM `SRG-APP-000408-NDM-000314`; NDM `SRG-APP-000172-NDM-000259`; NDM `SRG-APP-000880-NDM-000290` | `config system interface; edit mgmt1; set allowaccess https ssh; next; end` (dedicated management network; leave out HTTP, Telnet, and SQL) |
| Core: Management access | Web UI over HTTPS only (HTTP requests redirected to the HTTPS port) | 6.1.0 or earlier | NDM `SRG-APP-000172-NDM-000259`; NDM `SRG-APP-000412-NDM-000331` | GUI: System > Settings (HTTP Port: HTTP is not supported and is redirected to HTTPS) |
| Core: Management access | Administrative HTTPS, SSH, and Telnet port numbers | 6.1.0 or earlier | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — (non-standard HTTPS and SSH ports, as the Handbook's security hardening appendix suggests, are optional) |
| Core: Management access | Web UI server certificate (Factory certificate by default) | 6.1.0 or earlier | NDM `SRG-APP-000516-NDM-000344`; NDM `SRG-APP-000910-NDM-000300` | GUI: System > Certificate > Web Administration (HTTPS Server Certificate: a DoD-issued certificate, not Factory) |
| Core: Management access | Certificate signing requests and certificate import | 6.1.0 or earlier | NDM `SRG-APP-000516-NDM-000344`; NDM `SRG-APP-000910-NDM-000300` | GUI: System > Certificate > Generate and Import (generate the key pair on FortiDDoS and have a DoD CA sign the request) |
| Core: Management access | Trusted hosts for each administrator (up to three subnets) | 6.1.0 or earlier | NDM `SRG-APP-000408-NDM-000314`; NDM `SRG-APP-000038-NDM-000213` | `config system admin; edit <ADMIN>; set trusted-hosts <MGMT_SUBNET>; next; end` (set on every administrator account) |
| Core: Management access | Idle timeout for administrator sessions | 6.1.0 or earlier | NDM `SRG-APP-000190-NDM-000267`; NDM `SRG-APP-000220-NDM-000268` | GUI: System > Settings (Idle Timeout: 10 minutes or less) |
| Core: Management access | Login lockout (source IP blocked for five minutes after three failed logins) | 6.1.0 or earlier | NDM `SRG-APP-000065-NDM-000214` | — (fixed behavior; no setting, and the block is five minutes, not 15) |
| Core: Management access | Administrator logout from the user menu | 6.1.0 or earlier | NDM `SRG-APP-000296-NDM-000280`; NDM `SRG-APP-000220-NDM-000268` | — |
| Core: Management access | Protection of the management port from DoS (an SPP for the management address) | 6.1.0 or earlier | NDM `SRG-APP-000435-NDM-000315` | GUI: Service Protection > Service Protection Policy (only where the management port is reached through FortiDDoS traffic ports) |
| Core: Administrator accounts | Local administrator accounts and the admin (globaladmin) account | 6.1.0 or earlier | NDM `SRG-APP-000148-NDM-000346`; NDM `SRG-APP-000153-NDM-000249`; NDM `SRG-APP-000178-NDM-000264` | `config system admin; edit <ADMIN>; set auth-strategy local; set access-profile <PROFILE>; set password <PASSWORD_15_CHARS_MIN>; next; end` (one local account of last resort) |
| Core: Administrator accounts | Access profiles (None, Read Only, or Read-Write for each menu area) | 6.1.0 or earlier | NDM `SRG-APP-000033-NDM-000212`; NDM `SRG-APP-000231-NDM-000271`; NDM `SRG-APP-000380-NDM-000304`; NDM `SRG-APP-000340-NDM-000288`; NDM `SRG-APP-000516-NDM-000335` | GUI: System > Admin > Access Profile (super_admin_prof only for the administrators who need it) |
| Core: Administrator accounts | Password policy for administrators (length and character types) | 6.1.0 or earlier | NDM `SRG-APP-000164-NDM-000252`; NDM `SRG-APP-000166-NDM-000254`; NDM `SRG-APP-000167-NDM-000255`; NDM `SRG-APP-000168-NDM-000256`; NDM `SRG-APP-000169-NDM-000257`; NDM `SRG-APP-000860-NDM-000250` | `config system password-policy; set status enable; set apply-to admin-user; set minimum-length 15; set must-contain lower-case-letter upper-case-letter number non-alphanumeric; end` |
| Core: Administrator accounts | REST API administrator accounts (authorization token, CORS, trusted hosts) | 6.1.0 or earlier | NDM `SRG-APP-000408-NDM-000314`; NDM `SRG-APP-000153-NDM-000249`; NDM `SRG-APP-000038-NDM-000213` | GUI: System > Admin (Create > REST API Admin only where needed, with Restrict to Trusted Hosts and a profile other than super_admin_prof) |
| Core: Administrator accounts | Private data encryption key for stored passwords and keys | 6.1.0 or earlier | NDM `SRG-APP-000171-NDM-000258`; NDM `SRG-APP-000231-NDM-000271` | GUI: System > Settings (Private Data Encryption: a custom 32-character hexadecimal key, the same on both HA peers) |
| Core: Logging and alerts | Local event log (admin, configuration, system, HA, update, and user categories) | 6.1.0 or earlier | NDM `SRG-APP-000026-NDM-000208`; NDM `SRG-APP-000027-NDM-000209`; NDM `SRG-APP-000028-NDM-000210`; NDM `SRG-APP-000029-NDM-000211`; NDM `SRG-APP-000343-NDM-000289`; NDM `SRG-APP-000380-NDM-000304`; NDM `SRG-APP-000095-NDM-000225`; NDM `SRG-APP-000096-NDM-000226`; NDM `SRG-APP-000100-NDM-000230` | `config log setting local; set loglevel notification; set event-log-category admin configuration system ha update user health_check default_gateway; end` |
| Core: Logging and alerts | Login events (successful and failed administrator logins) | 6.1.0 or earlier | NDM `SRG-APP-000503-NDM-000320`; NDM `SRG-APP-000505-NDM-000322`; NDM `SRG-APP-000098-NDM-000228`; NDM `SRG-APP-000099-NDM-000229` | GUI: Log & Report > Log Access > Login Events |
| Core: Logging and alerts | DDoS attack log (every drop event, with SPP, direction, source, destination, and drop count; always enabled) | 6.1.0 or earlier | FW `SRG-NET-000492-FW-000006`; FW `SRG-NET-000074-FW-000009`; FW `SRG-NET-000075-FW-000010`; FW `SRG-NET-000076-FW-000011`; FW `SRG-NET-000077-FW-000012`; FW `SRG-NET-000078-FW-000013` | — (all DDoS attack log categories are enabled and cannot be disabled) |
| Core: Logging and alerts | Remote syslog servers for the event log (up to three) | 6.1.0 or earlier | NDM `SRG-APP-000515-NDM-000325`; NDM `SRG-APP-000516-NDM-000350` | `config log setting remote; edit 1; set status enable; set ip-address <SYSLOG_SERVER>; set port 514; set event-log-status enable; set loglevel Notification; set event-log-category admin configuration system ha update user; next; end` |
| Core: Logging and alerts | Remote syslog servers for the DDoS attack log | 6.1.0 or earlier | FW `SRG-NET-000333-FW-000014`; NDM `SRG-APP-000515-NDM-000325` | `config log setting ddos-attack-log-remote; edit <ATTACK_SYSLOG>; set status enable; set ip-address <SYSLOG_SERVER>; set port 514; set global enable; set spp <SPP>; next; end` |
| Core: Logging and alerts | Minimum drops for remote attack logs and SNMP traps | 6.1.0 or earlier | FW `SRG-NET-000333-FW-000014` | `config log setting remote-log-settings; set minimum-drops 1; end` (the default; a higher value suppresses low-drop logs) |
| Core: Logging and alerts | Local log disk size and disk-full action | 6.1.0 or earlier | NDM `SRG-APP-000357-NDM-000293` | GUI: Log & Report > Log Configuration > Local Log Settings (File Size and Disk full set to the organization's retention plan, with remote syslog) |
| Core: Logging and alerts | Attack log purge watermark and automatic purge | 6.1.0 or earlier | NDM `SRG-APP-000357-NDM-000293`; FW `SRG-NET-000100-FW-000023` | `config ddos global attack-event-purge; set purge-watermark 2000000; end` (and keep the attack log on a remote syslog server) |
| Core: Logging and alerts | Alert email for event log categories | 6.1.0 or earlier | NDM `SRG-APP-000360-NDM-000295`; NDM `SRG-APP-000795-NDM-000130`; FW `SRG-NET-000392-FW-000042` | `config log alertemail setting; set categories admin diskfull ha update; end`; `config log alertemail recipient; edit <RECIPIENT>; set address <ISSO_EMAIL>; next; end` (mail server under System > Maintenance > Mail Server) |
| Core: Logging and alerts | SNMP traps for CPU, memory, and log disk thresholds | 6.1.0 or earlier | NDM `SRG-APP-000357-NDM-000293`; NDM `SRG-APP-000360-NDM-000295` | `config system snmp threshold; set logdisk 75 1 7200 3600; end` (alert before the log disk fills) |
| Core: Logging and alerts | SNMP trap receivers for DDoS attack logs | 6.1.0 or earlier | FW `SRG-NET-000392-FW-000042` | `config log setting ddos-attack-snmp-trap-receivers; edit <TRAP_RECEIVER>; set status enable; set type all_attack_logs; set global enable; set ip-address <SNMP_MANAGER>; set snmp-version v3; set v3-access-type privacy; set authentication-passphrase <AUTH_KEY>; set privacy-passphrase <PRIV_KEY>; next; end` |
| Core: Logging and alerts | Protection of logs through access profiles | 6.1.0 or earlier | NDM `SRG-APP-000119-NDM-000236`; NDM `SRG-APP-000120-NDM-000237`; FW `SRG-NET-000099-FW-000161`; FW `SRG-NET-000100-FW-000023` | GUI: System > Admin > Access Profile (Log & Report: Read Only, or None, for every administrator who does not manage logs) |
| Core: Time and SNMP | NTP time synchronization | 6.1.0 or earlier | NDM `SRG-APP-000920-NDM-000320`; NDM `SRG-APP-000374-NDM-000299`; NDM `SRG-APP-000925-NDM-000330` | `config system time ntp; set ntpsync enable; set ntpserver <NTP_SERVER>; set syncinterval 60; end` |
| Core: Time and SNMP | SNMPv3 users (authentication and privacy) | 6.1.0 or earlier | NDM `SRG-APP-000395-NDM-000310`; NDM `SRG-APP-000412-NDM-000331` | GUI: System > SNMP > Config (SNMPv3: Auth And Privacy with SHA and AES 128) |
| Core: Time and SNMP | SNMP v1 and v2c communities | 6.1.0 or earlier | NDM `SRG-APP-000395-NDM-000310`; NDM `SRG-APP-000142-NDM-000245` | `config system snmp community; edit <ID>; set status disable; next; end` |
| Core: System integrity | Firmware upgrades (super_admin_prof only) | 6.1.0 or earlier | NDM `SRG-APP-000457-NDM-000352`; NDM `SRG-APP-001035-NDM-000340`; NDM `SRG-APP-000131-NDM-000243`; NDM `SRG-APP-000378-NDM-000302` | GUI: System > Firmware (compare the image checksum on the Fortinet support site before upgrading) |
| Core: System integrity | FortiGuard updates (IP reputation, domain reputation, and geolocation databases) | 6.1.0 or earlier | FW `SRG-NET-000362-FW-000028`; FW `SRG-NET-000364-FW-000031` | `config system fortiguard; set scheduled-update-status enable; set scheduled-update-frequency daily; end` |
| Core: System integrity | Configuration backup and restore | 6.1.0 or earlier | NDM `SRG-APP-000516-NDM-000340` | GUI: System > Maintenance > Backup & Restore (back up after every change and store the file encrypted) |
| Core: High availability | Active-passive HA cluster (configuration and threshold synchronization) | 6.1.0 or earlier | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | `config system ha; set mode standalone; end` |
| Core: DDoS mitigation | Service Protection Policies (SPPs) with protected subnets | 6.1.0 or earlier | FW `SRG-NET-000362-FW-000028`; FW `SRG-NET-000193-FW-000030`; FW `SRG-NET-000705-FW-000110` | GUI: Service Protection > Service Protection Policy (one SPP for each group of servers with similar traffic) |
| Core: DDoS mitigation | Detection Mode and Prevention Mode for each SPP and direction | 6.1.0 or earlier | FW `SRG-NET-000362-FW-000028`; FW `SRG-NET-000193-FW-000030`; FW `SRG-NET-000192-FW-000029` | `config ddos spp rule; edit <SPP>; set inbound-operating-mode prevention; set outbound-operating-mode prevention; next; end` (after the learning period in Detection Mode) |
| Core: DDoS mitigation | Rate thresholds for Layer 3, 4, and 7 parameters with continuous learning and adaptive thresholds | 6.1.0 or earlier | FW `SRG-NET-000362-FW-000028`; FW `SRG-NET-000193-FW-000030`; FW `SRG-NET-000705-FW-000110` | `config ddos spp rule; edit <SPP>; set adaptive-mode adaptive; next; end` |
| Core: DDoS mitigation | Traffic statistics and System Recommended thresholds | 6.1.0 or earlier | FW `SRG-NET-000362-FW-000028`; FW `SRG-NET-000705-FW-000110` | `execute generate-traffic-stats spp <SPP> <PERIOD>`; `config ddos spp rule; edit <SPP>; set system-recommendation enable; next; end` |
| Core: DDoS mitigation | Source tracking and blocking periods for attacking sources | 6.1.0 or earlier | FW `SRG-NET-000362-FW-000028`; FW `SRG-NET-000193-FW-000030` | `config ddos spp rule; edit <SPP>; set blocking-period <SECONDS>; set source-blocking-period <SECONDS>; next; end` |
| Core: DDoS mitigation | Protocol anomaly protection (IP, UDP, TCP, ICMP, and HTTP header anomalies) | 6.1.0 or earlier | FW `SRG-NET-000362-FW-000028`; FW `SRG-NET-000364-FW-000042` | GUI: Service Protection > IP Profile (and the ICMP, TCP, and HTTP profiles of each SPP) |
| Core: DDoS mitigation | TCP session state protection (SYN flood mitigation, foreign packet validation, aggressive aging) | 6.1.0 or earlier | FW `SRG-NET-000362-FW-000028`; FW `SRG-NET-000193-FW-000030` | GUI: Service Protection > TCP Profile |
| Core: DDoS mitigation | Global access control lists (deny by source address and service) | 6.1.0 or earlier | FW `SRG-NET-000019-FW-000003`; FW `SRG-NET-000364-FW-000031`; FW `SRG-NET-000364-FW-000032` | `config ddos global acl; edit <ACL_ID>; set source-address <ADDRESS>; set action deny; next; end` |
| Core: DDoS mitigation | SPP access control lists | 6.1.0 or earlier | FW `SRG-NET-000019-FW-000003`; FW `SRG-NET-000364-FW-000031`; FW `SRG-NET-000364-FW-000032` | `config ddos spp rule; edit <SPP>; config acl; edit <ACL>; set status enable; set action reject; set ip-version IPv4; set source-address4-type addr4; set source-address-v4 <ADDRESS>; set service-type service; set service-id <SERVICE>; next; end; next; end` |
| Core: DDoS mitigation | Blocklisted IPv4 addresses and domains | 6.1.0 or earlier | FW `SRG-NET-000364-FW-000031`; FW `SRG-NET-000362-FW-000028` | GUI: Global Protection > Blocklist > Blocklisted IPv4 (and Blocklisted Domains) |
| Core: DDoS mitigation | Power fail bypass mode (fail-open or fail-closed on power or system failure) | 6.1.0 or earlier | FW `SRG-NET-000235-FW-000133` | `config ddos global deployment; set power-fail-bypass-mode fail-closed; end` (where the protected links must not pass unfiltered traffic; record the decision if fail-open is chosen for availability) |
| Core: DDoS mitigation | Asymmetric Mode for networks where FortiDDoS does not see both directions | 6.1.0 or earlier | FW `SRG-NET-000362-FW-000028` | `config ddos global deployment; set asymmetric-mode enable; end` (only for asymmetric, multi-link, or load-balanced deployments) |
| Core: DDoS mitigation | Tap Mode (out-of-path detection with a bypass bridge) | 6.1.0 or earlier | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | `config ddos global deployment; set tap-mode disable; end` |
| Core: DDoS mitigation | Do Not Track policies (addresses that are passed without inspection) | 6.1.0 or earlier | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | GUI: Global Protection > Do Not Track Policy (delete entries that are not needed) |
| Core: DDoS mitigation | Dashboard, Top Attacks, and Monitor graphs | 6.1.0 or earlier | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Core: DDoS mitigation | Attack reports (on demand or scheduled) | 6.1.0 or earlier | FW `SRG-NET-000392-FW-000042` | GUI: Log & Report > Report Configuration (scheduled reports to the ISSO) |
| Core: Troubleshooting | Packet capture, diagnose commands, and debug files | 6.1.0 or earlier | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Platform | FortiDDoS-F VM support in several hypervisor environments (VMware, with SR-IOV where available) | 6.1.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| NTP protection | NTP support from the E-Series on all models | 6.1.0 and later | FW `SRG-NET-000362-FW-000028` | GUI: Service Protection > NTP Profile |
| SSL/TLS protection | Additional SSL DDoS mitigation settings | 6.1.0 and later | FW `SRG-NET-000362-FW-000028` | GUI: Service Protection > SSL/TLS Profile |
| Platform | 16 SPPs on the 1500F (and 4, 8, or 16 on VM04, VM08, and VM16) | 6.1.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Thresholds | Split System Recommendation for Layer 4 scalars and ICMP, TCP ports, and UDP ports (from B/E-Series 5.4.0) | 6.1.0 and later | FW `SRG-NET-000705-FW-000110` | GUI: Service Protection > Service Protection Policy (Threshold Settings > System Recommendation) |
| Thresholds | DNS Rcode scalars in Traffic Statistics and System Recommendations | 6.1.0 and later | FW `SRG-NET-000362-FW-000028`; FW `SRG-NET-000705-FW-000110` | — |
| Thresholds | NTP scalars in Traffic Statistics and System Recommendations | 6.1.0 and later | FW `SRG-NET-000362-FW-000028`; FW `SRG-NET-000705-FW-000110` | — |
| ACLs | Common UDP source reflection ports pre-populated as global service objects | 6.1.0 and later | FW `SRG-NET-000019-FW-000003`; FW `SRG-NET-000364-FW-000031` | GUI: System > Address and Service (use the reflection port services in Global or SPP ACLs) |
| ACLs | Service objects with source or destination ports (source port ACLs for UDP reflection ports) | 6.1.0 and later | FW `SRG-NET-000019-FW-000003`; FW `SRG-NET-000364-FW-000031` | `config system service; edit <SERVICE>; set protocol-type udp; set specify-source-port enable; set source-port-min <PORT>; set source-port-max <PORT>; next; end` |
| ACLs | IP address and subnet objects assigned to Global or SPP ACLs | 6.1.0 and later | FW `SRG-NET-000019-FW-000003` | `config system address4; edit <ADDRESS>; set type ip-netmask; set ip-netmask <IP/MASK>; next; end` |
| IP protection | Private (bogon) and multicast IP ACLs in any SPP | 6.1.0 and later | FW `SRG-NET-000364-FW-000042`; FW `SRG-NET-000364-FW-000031` | GUI: Service Protection > IP Profile (All Private IP ACL and All Multicast IP ACL, for SPPs that never receive them) |
| Service protection | SPP profiles for IP, ICMP, TCP, HTTP, SSL/TLS, NTP, and DNS (one profile for many SPPs) | 6.1.0 and later | FW `SRG-NET-000362-FW-000028`; FW `SRG-NET-000705-FW-000110` | `config ddos spp rule; edit <SPP>; set ip-profile <IP_PROFILE>; set icmp-profile <ICMP_PROFILE>; set tcp-profile <TCP_PROFILE>; set http-profile <HTTP_PROFILE>; set ssltls-profile <SSLTLS_PROFILE>; set ntp-profile <NTP_PROFILE>; set dns-profile <DNS_PROFILE>; next; end` |
| Service protection | Source MAC address for aggressive aging per SPP | 6.1.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| IP protection | Strict anomaly options in the SPP profiles (Layer 2 to Layer 7) | 6.1.0 and later | FW `SRG-NET-000362-FW-000028`; FW `SRG-NET-000364-FW-000042` | GUI: Service Protection > IP Profile (IP Strict Anomalies, and the strict options of the other profiles) |
| Cloud signaling | Cloud signaling thresholds in pps and Mbps for each protected subnet | 6.1.0 and later | FW `SRG-NET-000193-FW-000030`; FW `SRG-NET-000705-FW-000110` | `config ddos spp rule; edit <SPP>; set cloud-signaling-status enable; config address; edit <SUBNET>; set signaling-threshold-kpps <KPPS>; set signaling-threshold-mbps <MBPS>; next; end; next; end` (signaling devices under Global Protection > Cloud Signaling) |
| Service protection | Protected subnets entered for each SPP | 6.1.0 and later | FW `SRG-NET-000362-FW-000028` | `config ddos spp rule; edit <SPP>; config address; edit <SUBNET>; set type ipv4-netmask; set ip-netmask <IP/MASK>; next; end; next; end` |
| DNS protection | Explicit TCP thresholds for DNS query, question count, fragment, MX, and ALL | 6.1.0 and later | FW `SRG-NET-000362-FW-000028` | — |
| IP protection | IP reputation and domain reputation set for each SPP (IP and DNS profiles) | 6.1.0 and later | FW `SRG-NET-000364-FW-000031`; FW `SRG-NET-000362-FW-000028` | GUI: Service Protection > IP Profile (IP Reputation; Domain Reputation in the DNS Profile; FortiGuard subscriptions) |
| SSL/TLS protection | Cipher anomaly option in the SSL/TLS profile | 6.1.0 and later | FW `SRG-NET-000362-FW-000028` | `config ddos spp ssl-tls profile; edit <SSLTLS_PROFILE>; set protocol-anomaly enable; set cipher-anomaly enable; next; end` |
| Troubleshooting | tcpdump-style packet capture | 6.1.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| HTTP protection | Additional known method anomalies | 6.1.0 and later | FW `SRG-NET-000362-FW-000028` | GUI: Service Protection > HTTP Profile |
| High availability | HA override option removed (priority or uptime decides the primary) | 6.1.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Logging and alerts | Event logs when the alert mail server is unreachable or authentication fails | 6.1.1 and later | NDM `SRG-APP-000360-NDM-000295` | — (logged automatically) |
| Service protection | HTTP and HTTPS service ports for each SPP | 6.1.1 and later | FW `SRG-NET-000362-FW-000028` | `config ddos spp rule; edit <SPP>; set http-service-port <PORTS>; set ssl-service-port <PORTS>; next; end` |
| Platform | KVM hypervisor support | 6.1.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| TCP protection | SYN/ACK and SYN/ACK per destination thresholds in Asymmetric Mode | 6.2.0 and later | FW `SRG-NET-000362-FW-000028`; FW `SRG-NET-000193-FW-000030` | GUI: Service Protection > Service Protection Policy (manual thresholds; not learned or recommended) |
| UDP protection | DTLS profile for SPPs (DTLS direct and reflection attacks) | 6.2.0 and later | FW `SRG-NET-000362-FW-000028` | `config ddos spp rule; edit <SPP>; set dtls-profile <DTLS_PROFILE>; next; end` |
| UDP protection | Possible UDP Reflection Flood detection for source ports 1 to 9999 | 6.2.0 and later | FW `SRG-NET-000362-FW-000028`; FW `SRG-NET-000193-FW-000030` | — |
| Thresholds | System Recommendation option for outbound thresholds (actual traffic or system maximum) | 6.2.0 and later | FW `SRG-NET-000192-FW-000029`; FW `SRG-NET-000705-FW-000110` | GUI: Service Protection > Service Protection Policy (System Recommendation outbound option) |
| ACLs | Global ACLs handled by a dedicated global SPP, with their own Top Attacks table and drop graphs | 6.2.0 and later | FW `SRG-NET-000019-FW-000003`; FW `SRG-NET-000492-FW-000006` | GUI: Global Protection > Access Control List (global ACLs always drop, whatever the SPP mode) |
| GUI | Protection Subnets List page | 6.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| ACLs | Blocklisted IPv4 and Blocklisted Domains pages (counts, last update, add, delete, and search) | 6.2.0 and later | FW `SRG-NET-000364-FW-000031` | GUI: Global Protection > Blocklist > Blocklisted Domains |
| GUI | Navigation between SPPs in the SPP pages | 6.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| FortiGuard | FortiGuard scheduled updates daily or weekly only | 6.2.0 and later | FW `SRG-NET-000362-FW-000028`; FW `SRG-NET-000364-FW-000031` | `config system fortiguard; set scheduled-update-status enable; set scheduled-update-frequency daily; end` |
| GUI | Reboot and Shutdown commands in the user menu | 6.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Logging and alerts | Domain Reputation attack log event separated from the Domain Blocklist event | 6.2.0 and later | FW `SRG-NET-000074-FW-000009` | — |
| GUI | FortiView Threat Map time period selection | 6.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | Date and time tooltips on long-period graphs | 6.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Troubleshooting | CLI command to restart the web server (nginx) | 6.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Bypass | CLI command to show the inline or bypass status of the traffic ports | 6.2.0 and later | FW `SRG-NET-000235-FW-000133` | `get system bypass-status` |
| Troubleshooting | diagnose dataplane geo-ip (geolocation of an IPv4 address) | 6.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | GUI labeling, units, field sizes, and tooltip improvements | 6.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | CSV downloads of tables such as the attack log not available | 6.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Troubleshooting | get system performance (CPU, memory, and disk usage) | 6.2.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Troubleshooting | RRD check and reset commands (diagnose debug rrd_files_check, execute spp-rrd-reset, execute rrd-reset) | 6.2.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Platform | Console port for FortiDDoS VM on VMware and KVM | 6.2.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | Inbound and outbound operation mode columns in the Protection Subnets list | 6.2.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | SPP shown in the Dashboard attack log widget | 6.2.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Platform | VM model shown in the header bar | 6.2.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| DNS protection | DNS profile FQDN allowlist and blocklist files, manual entries, regex, and 0x20 mixed-case FQDNs | 6.3.0 and later | FW `SRG-NET-000362-FW-000028`; FW `SRG-NET-000364-FW-000031` | GUI: Service Protection > DNS Profile |
| DNS protection | Incomplete DNS header anomaly (blocks non-DNS traffic to port 53) | 6.3.0 and later | FW `SRG-NET-000362-FW-000028` | GUI: Service Protection > DNS Profile (DNS header anomaly: Incomplete DNS) |
| DNS protection | DNSSEC inspection, anomalies, and mitigation | 6.3.0 and later | FW `SRG-NET-000362-FW-000028` | GUI: Service Protection > DNS Profile |
| UDP protection | Monitoring of user-entered UDP service ports above 9999 for reflection floods | 6.3.0 and later | FW `SRG-NET-000362-FW-000028` | `config ddos spp rule; edit <SPP>; set udp-service-port <PORTS>; next; end` |
| Security Fabric | FortiDDoS graphs and tables on the FortiGate Security Fabric dashboard | 6.3.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | `config system csf; set status disable; end` |
| SSL/TLS protection | SSL/TLS traffic inspection for HTTP anomalies and thresholds (1500F; experimental in 6.3.0) | 6.3.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | `config ddos spp ssl-tls profile; edit <SSLTLS_PROFILE>; set ssl-inspection-mode disable; next; end` (it requires the servers' certificates and private keys on FortiDDoS) |
| Administrator accounts | LDAP, RADIUS, and TACACS+ remote password authentication for GUI, CLI, and console logins | 6.3.0 and later | NDM `SRG-APP-000516-NDM-000336`; NDM `SRG-APP-000153-NDM-000249`; NDM `SRG-APP-000148-NDM-000346` | `config system authentication radius; set state enable; set primary-server <RADIUS_SERVER>; set primary-secret <SECRET>; set backup-server <RADIUS_SERVER_2>; set backup-secret <SECRET>; set require-msg-auth; end`; `config system admin; edit <ADMIN>; set auth-strategy radius; set access-profile <PROFILE>; next; end` (or TACACS+, or LDAP over TLS) |
| TCP protection | Foreign packet threshold with foreign packet validation | 6.3.0 and later | FW `SRG-NET-000362-FW-000028` | GUI: Service Protection > TCP Profile |
| IP protection | Phishing, spam, and Tor exit node categories for IP reputation | 6.3.0 and later | FW `SRG-NET-000364-FW-000031` | GUI: Service Protection > IP Profile |
| Troubleshooting | Customer folder in the debug file; more SNMP debug logs | 6.3.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Troubleshooting | Additional packet capture options | 6.3.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Logging and alerts | Event log entry when an administrator changes the system time | 6.3.0 and later | NDM `SRG-APP-000343-NDM-000289`; NDM `SRG-APP-000380-NDM-000304` | — (logged automatically) |
| Bypass | Out of memory action (pass traffic or drop packets) | 6.3.0 and later | FW `SRG-NET-000235-FW-000133` | `config ddos global settings; set out-of-memory-mode Drop; end` (Bypass, the default, passes traffic without mitigation; record the choice) |
| Troubleshooting | RRD troubleshooting and repair commands | 6.3.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | Reboot, shutdown, configuration backup and restore, and password change in the user menu | 6.3.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | GUI enhancements (more characters in administrator names, port speed, ACL status, column settings) | 6.3.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | Top Attacks header stays visible when scrolling | 6.3.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Logging and alerts | Global deny rule names in the attack log | 6.3.1 and later | FW `SRG-NET-000074-FW-000009` | — |
| GUI | Dashboard enhancements (operating mode of all SPPs, system resources) | 6.3.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Troubleshooting | Transceiver information in get transceiver status | 6.3.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| DNS protection | DQRM timer change for performance | 6.3.3 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| DNS protection | DNS profile options (bitcoin mining domains in domain reputation; drop when no cache match) | 6.4.0 and later | FW `SRG-NET-000362-FW-000028`; FW `SRG-NET-000364-FW-000031` | GUI: Service Protection > DNS Profile |
| Bypass | Toggle the bypass ports between inline and bypass from the Dashboard | 6.4.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | Dashboard widgets can be pinned and expanded | 6.4.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| UDP protection | QUIC profile, thresholds, and graphs | 6.4.0 and later | FW `SRG-NET-000362-FW-000028` | `config ddos spp rule; edit <SPP>; set quic-profile <QUIC_PROFILE>; next; end` |
| Reports | Reports per SPP or group of SPPs, report periods from one hour to one year, and reports when a drop threshold is exceeded | 6.4.0 and later | FW `SRG-NET-000392-FW-000042` | GUI: Log & Report > Report Configuration |
| GUI | Direction and SPP filters in the DDoS attack log | 6.4.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | Direction in the anomaly drop graphs | 6.4.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| SNMP | FORTINET-CORE-MIB and FORTINET-FORTIDDOS-MIB included in the build | 6.4.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| HTTP protection | HTTP anomalies detected on the HTTP flow rather than per packet | 6.4.0 and later | FW `SRG-NET-000362-FW-000028` | GUI: Service Protection > HTTP Profile |
| Administrator accounts | LDAPS and STARTTLS for CLI logins | 6.4.0 and later | NDM `SRG-APP-000516-NDM-000336`; NDM `SRG-APP-000172-NDM-000259` | `config system authentication LDAP; set state enable; set server <LDAP_SERVER>; set port 636; set cnid <CNID>; set dn <BASE_DN>; set secure ldaps; set ca-profile <CA_PROFILE>; end`; `config system admin; edit <ADMIN>; set auth-strategy ldap; next; end` |
| Troubleshooting | execute restapi-restart | 6.4.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| DNS protection | International domain names (IDN) in the DNS tables | 6.4.1 and later | FW `SRG-NET-000362-FW-000028` | — |
| Management access | Shell access set from the CLI (allowed users, password, and duration) | 6.4.1 and later | NDM `SRG-APP-000142-NDM-000245`; NDM `SRG-APP-000340-NDM-000288`; NDM `SRG-APP-000408-NDM-000314` | — (the command is not in the 8.0.0 Handbook; leave shell access unset unless Fortinet support needs it) |
| UDP protection | DTLS content types 25 and 26 | 6.4.1 and later | FW `SRG-NET-000362-FW-000028` | — |
| GUI | Refreshed GUI pages and graphs | 6.5.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | GUI and graph updates (UDP reflection port table, links to Monitor graphs; FortiView Threat Map removed) | 6.5.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Thresholds | System Recommended thresholds for DNS TCP at twice the UDP thresholds; DNS query per source | 6.5.0 and later | FW `SRG-NET-000705-FW-000110` | — |
| ACLs | IPv6 geolocation and geolocation ACLs (IPv4 and IPv6) in SPPs | 6.5.0 and later | FW `SRG-NET-000364-FW-000031`; FW `SRG-NET-000019-FW-000003` | `config system address4; edit <GEO_ADDRESS>; set type geo; set country <COUNTRY>; next; end` (used in an SPP ACL) |
| GUI | SPP policy list shows the profiles of each SPP | 6.5.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | Reordering and deleting in the SPP ACL list | 6.5.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Administrator accounts | Two-factor authentication (2FA) for RADIUS remote authentication | 6.5.0 and later | NDM `SRG-APP-000820-NDM-000170`; NDM `SRG-APP-000825-NDM-000180` | GUI: System > Authentication > RADIUS (with a RADIUS server that enforces the second factor) |
| Administrator accounts | Remote password authentication for CLI users (RADIUS, LDAP, TACACS+) | 6.5.0 and later | NDM `SRG-APP-000516-NDM-000336`; NDM `SRG-APP-000153-NDM-000249` | `config system admin; edit <ADMIN>; set auth-strategy radius; next; end` (CLI users need a local user name with super_admin_prof) |
| DNS protection | DNS proxy validation, dynamic updates, known opcode anomalies, and resource record ACLs under flood | 6.5.0 and later | FW `SRG-NET-000362-FW-000028` | GUI: Service Protection > DNS Profile |
| Thresholds | Anomaly tracking changes for most active source and port thresholds | 6.5.0 and later | FW `SRG-NET-000362-FW-000028` | — |
| Troubleshooting | Packet capture from the management ports | 6.5.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Troubleshooting | Debug file split into customer and developer files | 6.5.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | License and FortiGuard subscription icons | 6.5.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Logging and alerts | CSV download of up to 100,000 DDoS attack logs | 6.5.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| DNS protection | Drop log for good FQDNs with bad resource record queries (NODATA) | 6.5.0 and later | FW `SRG-NET-000492-FW-000006` | — |
| GUI | FortiView updates | 6.5.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Logging and alerts | Event logs describe FortiGuard update actions | 6.5.0 and later | NDM `SRG-APP-000095-NDM-000225` | — |
| GUI | Disabled global ACLs hidden from the ACL drop graphs | 6.5.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | Drops of disabled or deleted global ACLs in the aggregate graph | 6.5.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Troubleshooting | execute recover-gui | 6.5.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Logging and alerts | Event log for a data plane (VPP) restart | 6.5.0 and later | NDM `SRG-APP-000095-NDM-000225` | — |
| High availability | Merging traffic statistics from the HA secondary to the primary | 6.5.0 and later | FW `SRG-NET-000705-FW-000110` | GUI: System > Maintenance > Traffic Statistics Management |
| Certificates | Certificates with password files | 6.5.0 and later | NDM `SRG-APP-000516-NDM-000344` | GUI: System > Certificate > Generate and Import |
| Logging and alerts | One Update event log filter for IP reputation, domain reputation, and geolocation updates | 6.5.1+; 6.6.0+ | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | GUI and graph updates (event log at 90% CPU, RAM, or log disk; input validation on graphs) | 6.6.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Administrator accounts | RADIUS vendor-specific attributes and TACACS+ custom attributes | 6.6.0 and later | NDM `SRG-APP-000153-NDM-000249`; NDM `SRG-APP-000033-NDM-000212` | GUI: System > Authentication > RADIUS (Fortinet VSAs for the access profile and trusted hosts; TACACS+ shell profiles) |
| Logging and alerts | RFC 5424 and FortiAnalyzer encrypted (OFTP) syslog formats | 6.6.0+; 7.0.0+ | NDM `SRG-APP-000515-NDM-000325`; NDM `SRG-APP-000516-NDM-000350`; FW `SRG-NET-000333-FW-000014` | `config log setting remote; edit 1; set status enable; set ip-address <FAZ_IP>; set fortianalyzer enable; set encrypt-traffic-to-fortianalyzer; next; end`; `config log setting ddos-attack-log-remote; edit <ATTACK_SYSLOG>; set status enable; set ip-address <FAZ_IP>; set fortianalyzer enable; set encrypt-traffic-to-fortianalyzer enable; next; end` |
| FortiGuard | FQDN proxy tunneling for FortiGuard updates | 6.6.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | `config system fortiguard; set tunneling-status disable; end` |
| System integrity | Daily configuration backup and debug upload over SFTP, with server folders | 6.6.0 and later | NDM `SRG-APP-000516-NDM-000340` | `config system daily-config-backup; set status enable; set server <BACKUP_SERVER>; set server-type SFTP; set sftp-username <USER>; set sftp-password <PASSWORD>; end` |
| Logging and alerts | Event logs for failed configuration restores and daily backup results | 6.6.0 and later | NDM `SRG-APP-000516-NDM-000340`; NDM `SRG-APP-000095-NDM-000225` | — |
| ACLs | Geolocation data downloaded dynamically from FortiGuard | 6.6.0 and later | FW `SRG-NET-000364-FW-000031` | — |
| Troubleshooting | CLI error messages explained; Flowspec ACL output from the CLI | 6.6.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Platform | KVM deployment (log disk formatted automatically; SPP-1 created) | 6.6.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Logging and alerts | SPP names instead of SPP IDs in the debug file and attack log | 6.6.0 and later | FW `SRG-NET-000076-FW-000011` | — |
| Management access | Default idle timeout lowered from 30 to 5 minutes (1 to 480 minutes) | 6.6.0 and later | NDM `SRG-APP-000190-NDM-000267` | GUI: System > Settings (Idle Timeout: 10 minutes or less) |
| ACLs | Faster application of the IPv4 and domain blocklists | 6.6.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| DNS protection | Multiple DNS queries in one TCP session blocked | 6.6.0 and later | FW `SRG-NET-000362-FW-000028` | — |
| GUI | GUI and graph updates (certificate type, FQDN lists, SSL/TLS version anomaly redesign, log search) | 7.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| UDP protection | Low UDP ports (1024 to 9999) as UDP service ports | 7.0.0 and later | FW `SRG-NET-000362-FW-000028` | `config ddos spp rule; edit <SPP>; set udp-service-port <PORTS>; next; end` |
| High availability | Inter-appliance HA protocol change | 7.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Service protection | Video Conference profile (Zoom) | 7.0.0 and later | FW `SRG-NET-000362-FW-000028` | `config ddos spp rule; edit <SPP>; set video-conferencing-profile <VIDEO_PROFILE>; next; end` |
| Troubleshooting | Network diagnostics (deep packet trace) | 7.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Bypass | Fail-closed mode works as in 6.4 (manual bypass not available in fail-closed mode) | 7.0.0 and later | FW `SRG-NET-000235-FW-000133` | `config ddos global deployment; set power-fail-bypass-mode fail-closed; end` |
| Management access | TLS versions for the management ports (TLS 1.1, 1.2, and 1.3) | 7.0.0 and later | NDM `SRG-APP-000412-NDM-000331`; NDM `SRG-APP-000411-NDM-000330`; NDM `SRG-APP-000172-NDM-000259` | GUI: System > Settings (TLS Versions: disable TLS 1.1; allow only TLS 1.2 and 1.3) |
| DNS protection | Domain reputation category for DNS tunneling | 7.0.0 and later | FW `SRG-NET-000362-FW-000028`; FW `SRG-NET-000364-FW-000031` | GUI: Service Protection > DNS Profile |
| Service protection | GRE tunnel endpoints in an SPP | 7.0.0 and later | FW `SRG-NET-000364-FW-000031`; FW `SRG-NET-000362-FW-000028` | GUI: Global Protection > GRE Tunnel Endpoint |
| Administrator accounts | Permission changes for admin and global-admin users | 7.0.0 and later | NDM `SRG-APP-000033-NDM-000212`; NDM `SRG-APP-000340-NDM-000288` | GUI: System > Admin > Access Profile |
| DNS protection | TTL-less DNS LQ Populate (legitimate query table) | 7.0.1 and later | FW `SRG-NET-000362-FW-000028` | GUI: Global Protection > DNS LQ Populate |
| DNS protection | TCP DNS improvements (SYN validation, foreign packet validation, multiple queries per packet) | 7.0.1 and later | FW `SRG-NET-000362-FW-000028` | — |
| High availability | Unicast TCP HA and synchronization of uploaded tables (certificates, blocklists, FQDN files) | 7.0.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Thresholds | SYN-ACK parameters in Traffic Statistics and System Recommended thresholds in Asymmetric Mode | 7.0.1 and later | FW `SRG-NET-000705-FW-000110` | — |
| Logging and alerts | GUI, log, and profile updates (TLS 1.1 disabled on upgrade, IP Land Attack anomaly, TCP syslog, event trap for each SPP) | 7.0.1 and later | FW `SRG-NET-000098-FW-000021`; FW `SRG-NET-000362-FW-000028`; FW `SRG-NET-000392-FW-000042`; NDM `SRG-APP-000412-NDM-000331` | `config log setting remote; edit 1; set proto tcp; next; end`; `config log setting ddos-attack-log-remote; edit <ATTACK_SYSLOG>; set proto tcp; next; end` (and TLS 1.1 left disabled) |
| Security Fabric | GUI and graph updates (Data Path Resources graphs, report cloning, external IP list connectors, Fabric connector) | 7.0.3 and later | FW `SRG-NET-000364-FW-000031` | `config system external-resource; edit <CONNECTOR>; set type address; set status enable; set resource <URI>; set verify-host-cert enable; next; end` |
| IP protection | TCP and UDP enhancements (UDP empty checksum option, TCP DNS through all DNS features, UDP reflection flood logs, 256 UDP service ports) | 7.0.3 and later | FW `SRG-NET-000362-FW-000028` | GUI: Service Protection > IP Profile |
| TCP protection | Foreign packet pause timer for link events | 7.0.3 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| High availability | HA partner switches from fail-closed to fail-open on a link failure | 7.0.3 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| SNMP | SNMP polling of global and SPP drop counts and attack flags | 7.0.3 and later | FW `SRG-NET-000392-FW-000042` | `config ddos global settings; set snmp-minimum-drops <DROPS>; end` |
| System integrity | Daily configuration backup at local time, on demand, or as a test | 7.0.3 and later | NDM `SRG-APP-000516-NDM-000340` | `config system daily-config-backup; set scheduled-time <HH:MM>; end` |
| High availability | Traffic statistics merged automatically between HA primary and secondary | 7.0.4 and later | FW `SRG-NET-000705-FW-000110` | GUI: System > High Availability |
| ACLs | Automatic Layer 3 and Layer 4 distress ACLs (ADACLs) under large floods on the 3000F | 7.0.4 and later | FW `SRG-NET-000362-FW-000028`; FW `SRG-NET-000193-FW-000030` | — |
| GUI | Top Attacks single-column layout on small screens | 7.0.4 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| High availability | Low traffic rate on links signals the HA partner to pause foreign packet validation | 7.0.4 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Logging and alerts | Separate attack log event for SYN with payload | 7.0.4 and later | FW `SRG-NET-000074-FW-000009` | — |
| GUI | Last 20 emergency, alert, and critical event logs on the Dashboard | 7.0.4 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| UDP protection | IKE (UDP 500) anomaly and flood protection | 7.0.4 and later | FW `SRG-NET-000362-FW-000028` | — |
| GUI | Attack log filter by drop count | 7.0.4 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| High availability | Link status signaling to the HA partner | 7.0.4 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| High availability | Distress ACLs and ADACLs independent on each HA partner | 7.0.4 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| DNS protection | Thresholds for the top 512 FQDN rates in DNS responses | 7.0.4 and later | FW `SRG-NET-000362-FW-000028`; FW `SRG-NET-000193-FW-000030` | — |
| GUI | Outbound system-generated validation packets shown | 7.0.4 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Troubleshooting | S.M.A.R.T. SSD integrity commands (checklogdisk removed) | 7.0.4 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Service protection | Bypass VLAN (ignore private VLAN traffic) | 7.0.4 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — (off by default; enable only for VLANs with private addresses) |
| ACLs | IPsec tunnel endpoint lists (only VPN traffic between the listed local and remote IPs) | 7.0.4 and later | FW `SRG-NET-000364-FW-000031`; FW `SRG-NET-000019-FW-000003` | GUI: Global Protection > IPSEC |
| GUI | SPP links on the Top Attacks Summary page | 7.0.4 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Logging and alerts | Attack log backup removed (download logs or use the debug files) | 7.0.4 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| ACLs | TTL options removed from 3000F distress ACLs | 7.0.4 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Cloud signaling | Cloud signaling devices only for third-party service providers | 7.0.4 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Cloud signaling | Last Successful Attack Sent column for signaling devices | 7.0.4 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | SPP membership changed from the Protection Subnets List | 7.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | Links to the SPP from the Protection Subnets List | 7.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| High availability | Pause HA during upgrades with the HA settings kept | 7.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Thresholds | Traffic statistics from peak or 95th percentile traffic | 7.2.0 and later | FW `SRG-NET-000705-FW-000110` | — |
| GUI | Link Down Sync setting shown for each port pair | 7.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Logging and alerts | Management CPU usage and an event log when it exceeds 90% for five minutes | 7.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Thresholds | TCP and UDP port low traffic thresholds adjustable without new System Recommendations | 7.2.0 and later | FW `SRG-NET-000705-FW-000110` | `config ddos spp rule; edit <SPP>; set threshold-system-recommended-layer-4-tcp-port-low-traffic <PPS>; set threshold-system-recommended-layer-4-udp-port-low-traffic <PPS>; next; end` |
| IP protection | IP-in-IP tunneling attack detection | 7.2.0 and later | FW `SRG-NET-000362-FW-000028`; FW `SRG-NET-000364-FW-000031` | GUI: Service Protection > IP Profile |
| IP protection | Drop of unratified Layer 3 protocols (IP strict anomalies) | 7.2.0 and later | FW `SRG-NET-000362-FW-000028`; FW `SRG-NET-000364-FW-000031` | GUI: Service Protection > IP Profile |
| Logging and alerts | Event logs for user and system bypass actions | 7.2.0 and later | NDM `SRG-APP-000343-NDM-000289`; NDM `SRG-APP-000095-NDM-000225` | — |
| FortiGuard | GEO Update Status option to stop geolocation database downloads | 7.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | GUI: System > FortiGuard (GEO Update Status disabled when geolocation is not used) |
| Logging and alerts | Event logs for power supply failures | 7.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Troubleshooting | Bypass, transceiver, and interface details in the full debug file | 7.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Bypass | Shorter outages on inline and bypass transitions after a data plane crash | 7.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | Bypass status icon turns red in bypass mode | 7.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | Several debug files deleted at once | 7.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | Scalar threshold pages reached from the DNS graphs | 7.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Troubleshooting | Debug file compression | 7.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | Data plane CPU data cleared to add management CPU metrics | 7.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| IP protection | UDP empty checksum check disabled by default | 7.2.1 and later | FW `SRG-NET-000362-FW-000028` | GUI: Service Protection > IP Profile (enable it except in SPPs that carry IPsec NAT traversal) |
| TCP protection | ACK=0 check for SYN packets in TCP strict anomalies | 7.2.1 and later | FW `SRG-NET-000362-FW-000028` | GUI: Service Protection > TCP Profile |
| GUI | Attacked destination drop distribution tables; SYN-ACK and DNS response graphs rearranged | 7.2.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | Context-sensitive help on all GUI pages | 7.2.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Thresholds | Scalar thresholds for UDP fragments, UDP port 53, and DNS Rcode 0 per destination | 7.2.2 and later | FW `SRG-NET-000362-FW-000028`; FW `SRG-NET-000193-FW-000030` | — |
| Logging and alerts | Custom FQDN for the mail server HELO/EHLO check | 7.2.2 and later | NDM `SRG-APP-000360-NDM-000295` | GUI: System > Settings (FQDN) |
| Bypass | Bypass status of port pairs cross-connected to the optical bypass module (2000F and 3000F) | 7.2.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| DNS protection | FQDN check for DNS LQ Populate | 7.2.2 and later | FW `SRG-NET-000362-FW-000028` | — |
| ACLs | IPv6 geolocation database management | 7.2.2 and later | FW `SRG-NET-000364-FW-000031` | — |
| ACLs | IPsec tunnel endpoints monitor only ESP (protocol 50) | 7.2.2 and later | FW `SRG-NET-000364-FW-000031` | GUI: Global Protection > IPSEC |
| GUI | Top Attacks SPP tables added or removed with widget controls | 7.2.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Thresholds | TCP port low traffic threshold range up to 262,140 pps | 7.2.2 and later | FW `SRG-NET-000705-FW-000110` | — |
| GUI | Faster event log filtering | 7.2.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | GUI labels for Chinese, Japanese, Korean, and Spanish | 7.2.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Service protection | Bypass Reversed Traffic for hair-pinned traffic | 7.2.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — (off by default; enable only where hair-pinned traffic is seen) |
| TCP protection | Foreign packet threshold kept when foreign packet validation is disabled and re-enabled | 7.2.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | Non-IP Ethertypes graph | 7.2.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| DNS protection | DNS Suspicious Sources (NXDOMAIN and NODATA responses) | 7.2.2 and later | FW `SRG-NET-000362-FW-000028` | — |
| Troubleshooting | More tables in the customer and full debug files | 7.2.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| ACLs | Geolocation package without regions | 7.2.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| TCP protection | Allow Inbound SYN-ACK set in the TCP profile of each SPP | 8.0.0 and later | FW `SRG-NET-000362-FW-000028` | GUI: Service Protection > TCP Profile (disable it for SPPs that expect only inbound sessions) |
| GUI | System > Settings moved to the main System menu | 8.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Thresholds | ESP and UDP source port 53 per destination thresholds | 8.0.0 and later | FW `SRG-NET-000362-FW-000028`; FW `SRG-NET-000193-FW-000030` | — |
| Thresholds | Rcode 0 and Rcode 1 to 15 threshold ranges in System Recommendations | 8.0.0 and later | FW `SRG-NET-000705-FW-000110` | — |
| DNS protection | DNS Query TKEY threshold | 8.0.0 and later | FW `SRG-NET-000362-FW-000028` | — |
| Thresholds | Fewer false positives for UDP applications such as Microsoft Teams and Zoom | 8.0.0 and later | FW `SRG-NET-000705-FW-000110` | — |
| Thresholds | Three TCP port ranges in System Recommendations | 8.0.0 and later | FW `SRG-NET-000705-FW-000110` | — |
| GUI | Custom dashboard views for super_admin_prof users | 8.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Management access | Pre-login warning banner (disabled by default, customizable) | 8.0.0 and later | NDM `SRG-APP-000068-NDM-000215`; NDM `SRG-APP-000069-NDM-000216` | GUI: System > Settings (Pre Login Warning enabled); GUI: System > Replacement Messages (Pre-Login Disclaimer Message: the Standard Mandatory DoD Notice and Consent Banner) |
| FortiGuard | Attack telemetry sent to FortiGuard (opt-out) | 8.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | `config system global; set fds-statistics disable; end` |
| TCP protection | Inbound SYN service ACL for each SPP (drops all inbound SYN packets) | 8.0.0 and later | FW `SRG-NET-000362-FW-000028`; FW `SRG-NET-000364-FW-000031` | GUI: Service Protection > Service Protection Policy (only for SPPs that never expect inbound SYN packets) |
| Logging and alerts | Mail server settings moved to System > Maintenance > Mail Server | 8.0.0 and later | NDM `SRG-APP-000360-NDM-000295` | GUI: System > Maintenance > Mail Server |
| GUI | Custom Monitor page | 8.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | Collapsible sections on the DNS Profile page | 8.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Reports | Pie and bar graphs on the Report Browse page | 8.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | Logarithmic (base 2) graph labels | 8.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| SNMP | SNMP trap with threshold for Data Path Resources | 8.0.0 and later | FW `SRG-NET-000392-FW-000042`; NDM `SRG-APP-000360-NDM-000295` | `config log setting ddos-attack-snmp-trap-receivers; edit <TRAP_RECEIVER>; set status enable; set type data_path_resources; set data-path-resources-threshold 90; set ip-address <SNMP_MANAGER>; next; end` |
| GUI | File selector for firmware upload | 8.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Troubleshooting | CSV of ACLs, blocklist, and external resource files in the debug files | 8.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | Main menu and submenus reorganized | 8.0.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| SSL/TLS protection | JA4 TLS fingerprint thresholds against TLS floods without decryption | 8.0.1 and later | FW `SRG-NET-000362-FW-000028`; FW `SRG-NET-000193-FW-000030` | — |
| UDP protection | STUN thresholds for UDP port 3478 and STUN anomalies | 8.0.1 and later | FW `SRG-NET-000362-FW-000028` | — |
| ACLs | Automated distress ACL threshold set as a CPU percentage | 8.0.1 and later | FW `SRG-NET-000362-FW-000028`; FW `SRG-NET-000193-FW-000030` | GUI: Global Protection > Access Control List (Auto-Distress ACL) |
| Thresholds | System Recommended thresholds created in one action on the Threshold Settings page | 8.0.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| ACLs | IPsec tunnel endpoints configured for each SPP | 8.0.1 and later | FW `SRG-NET-000364-FW-000031`; FW `SRG-NET-000019-FW-000003` | GUI: Service Protection > Service Protection Policy (IPsec tunnel endpoints of the SPP) |
| Reports | Yesterday report period | 8.0.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Reports | Simplified report configuration | 8.0.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | Comment field for protected subnets | 8.0.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Logging and alerts | Port logical names in port up and down event logs | 8.0.1 and later | NDM `SRG-APP-000097-NDM-000227` | — |
| IP protection | IP profile blocks invalid and non-public address ranges (loopback, APIPA, CGNAT, TEST-NET, reserved) | 8.0.1 and later | FW `SRG-NET-000364-FW-000042`; FW `SRG-NET-000364-FW-000031` | GUI: Service Protection > IP Profile |
| Reports | Top Attacks Summary report tables scheduled and sent by email | 8.0.1 and later | FW `SRG-NET-000392-FW-000042` | GUI: Log & Report > Report Configuration |
| GUI | Event Detail column in the attack log | 8.0.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | Dashboard Top Attacks tables added, removed, rearranged, and resized | 8.0.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Reports | Top Attacks Summary tables in reports | 8.0.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | Favorites menu | 8.0.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Troubleshooting | Debug files generated from the CLI and uploaded by TFTP or FTP | 8.0.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Logging and alerts | Alert mail settings for log levels and categories | 8.0.1 and later | NDM `SRG-APP-000360-NDM-000295` | GUI: Log & Report > Log Configuration > Alert Email Settings |
| GUI | Global Settings > Deployment reorganized | 8.0.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| DNS protection | DNS Packet Track per Source renamed DNS Suspicious Sources | 8.0.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | New color scheme for resource use on the Dashboard | 8.0.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |

### Requirement reference

The requirements used in the map and in this chapter's text, with their
severity in the current SRG releases:

[Download the requirement reference as CSV](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/data/volume-172-disa-srgs-and-stigs/20-fortiddos-feature-version-and-srg-map-requirements.csv) (90 rows).

| SRG | Requirement | Severity | Requirement title |
| --- | --- | --- | --- |
| NDM | `SRG-APP-000001-NDM-000200` | CAT II | The network device must limit the number of concurrent sessions to an organization-defined number for each administrator account and/or administrator account type. |
| NDM | `SRG-APP-000026-NDM-000208` | CAT II | The network device must automatically audit account creation. |
| NDM | `SRG-APP-000027-NDM-000209` | CAT II | The network device must automatically audit account modification. |
| NDM | `SRG-APP-000028-NDM-000210` | CAT II | The network device must automatically audit account disabling actions. |
| NDM | `SRG-APP-000029-NDM-000211` | CAT II | The network device must automatically audit account removal actions. |
| NDM | `SRG-APP-000033-NDM-000212` | CAT I | The network device must be configured to assign appropriate user roles or access levels to authenticated users. |
| NDM | `SRG-APP-000038-NDM-000213` | CAT II | The network device must enforce approved authorizations for controlling the flow of management information within the network device based on information flow control policies. |
| NDM | `SRG-APP-000065-NDM-000214` | CAT II | The network device must be configured to enforce the limit of three consecutive invalid logon attempts, after which time it must block any login attempt for 15 minutes. |
| NDM | `SRG-APP-000068-NDM-000215` | CAT II | The network device must display the Standard Mandatory DoD Notice and Consent Banner before granting access to the device. |
| NDM | `SRG-APP-000069-NDM-000216` | CAT II | The network device must retain the Standard Mandatory DoD Notice and Consent Banner on the screen until the administrator acknowledges the usage conditions and takes explicit actions to log on for further access. |
| NDM | `SRG-APP-000095-NDM-000225` | CAT II | The network device must produce audit log records containing sufficient information to establish what type of event occurred. |
| NDM | `SRG-APP-000096-NDM-000226` | CAT II | The network device must produce audit records containing information to establish when (date and time) the events occurred. |
| NDM | `SRG-APP-000097-NDM-000227` | CAT II | The network device must produce audit records containing information to establish where the events occurred. |
| NDM | `SRG-APP-000098-NDM-000228` | CAT II | The network device must produce audit log records containing information to establish the source of events. |
| NDM | `SRG-APP-000099-NDM-000229` | CAT II | The network device must produce audit records that contain information to establish the outcome of the event. |
| NDM | `SRG-APP-000100-NDM-000230` | CAT II | The network device must generate audit records containing information that establishes the identity of any individual or process associated with the event. |
| NDM | `SRG-APP-000119-NDM-000236` | CAT II | The network device must protect audit information from unauthorized modification. |
| NDM | `SRG-APP-000120-NDM-000237` | CAT II | The network device must protect audit information from unauthorized deletion. |
| NDM | `SRG-APP-000131-NDM-000243` | CAT II | The network device must prevent the installation of patches, service packs, or application components without verification the software component has been digitally signed using a certificate that is recognized and approved by the organization. |
| NDM | `SRG-APP-000142-NDM-000245` | CAT I | The network device must be configured to prohibit the use of all unnecessary and/or nonsecure functions, ports, protocols, and/or services |
| NDM | `SRG-APP-000148-NDM-000346` | CAT II | The network device must be configured with only one local account to be used as the account of last resort in the event the authentication server is unavailable. |
| NDM | `SRG-APP-000149-NDM-000247` | CAT I | The network device must be configured to use DoD PKI as multi-factor authentication (MFA) for interactive logins. |
| NDM | `SRG-APP-000153-NDM-000249` | CAT II | The network device must be configured to authenticate each administrator prior to authorizing privileges based on assignment of group or role. |
| NDM | `SRG-APP-000164-NDM-000252` | CAT II | The network device must enforce a minimum 15-character password length. |
| NDM | `SRG-APP-000166-NDM-000254` | CAT II | The network device must enforce password complexity by requiring that at least one uppercase character be used. |
| NDM | `SRG-APP-000167-NDM-000255` | CAT II | The network device must enforce password complexity by requiring that at least one lowercase character be used. |
| NDM | `SRG-APP-000168-NDM-000256` | CAT II | The network device must enforce password complexity by requiring that at least one numeric character be used. |
| NDM | `SRG-APP-000169-NDM-000257` | CAT II | The network device must enforce password complexity by requiring that at least one special character be used. |
| NDM | `SRG-APP-000170-NDM-000329` | CAT II | The network device must require that when a password is changed, the characters are changed in at least eight of the positions within the password. |
| NDM | `SRG-APP-000171-NDM-000258` | CAT I | The network device must be configured to store passwords using an approved salted key derivation function, preferably using a keyed hash for password-based authentication. |
| NDM | `SRG-APP-000172-NDM-000259` | CAT I | The network device must transmit only encrypted representations of passwords. |
| NDM | `SRG-APP-000178-NDM-000264` | CAT I | The network device must obscure feedback of authentication information during the authentication process to protect the information from possible exploitation/use by unauthorized individuals. |
| NDM | `SRG-APP-000179-NDM-000265` | CAT I | The network device must use FIPS 140-2 approved algorithms for authentication to a cryptographic module. |
| NDM | `SRG-APP-000190-NDM-000267` | CAT I | The network device must terminate all network connections associated with a device management session at the end of the session, or the session must be terminated after five minutes of inactivity except to fulfill documented and validated mission requirements. |
| NDM | `SRG-APP-000220-NDM-000268` | CAT II | The network device must invalidate session identifiers upon administrator logout or other session termination. |
| NDM | `SRG-APP-000231-NDM-000271` | CAT I | The network device must only allow authorized administrators to view or change the device configuration, system files, and other files stored either in the device or on removable media (such as a flash drive). |
| NDM | `SRG-APP-000296-NDM-000280` | CAT II | The network device must be configured to provide a logout mechanism for administrator-initiated communication sessions. |
| NDM | `SRG-APP-000340-NDM-000288` | CAT I | The network device must prevent non-privileged users from executing privileged functions to include disabling, circumventing, or altering implemented security safeguards/countermeasures. |
| NDM | `SRG-APP-000343-NDM-000289` | CAT II | The network device must audit the execution of privileged functions. |
| NDM | `SRG-APP-000357-NDM-000293` | CAT II | The network device must allocate audit record storage capacity in accordance with organization-defined audit record storage requirements. |
| NDM | `SRG-APP-000360-NDM-000295` | CAT II | The network device must generate an immediate real-time alert of all audit failure events requiring real-time alerts. |
| NDM | `SRG-APP-000374-NDM-000299` | CAT II | The network device must record time stamps for audit records that can be mapped to Coordinated Universal Time (UTC) or Greenwich Mean Time (GMT). |
| NDM | `SRG-APP-000378-NDM-000302` | CAT II | The network device must prohibit installation of software without explicit privileged status. |
| NDM | `SRG-APP-000380-NDM-000304` | CAT II | The network device must enforce access restrictions associated with changes to device configuration. |
| NDM | `SRG-APP-000395-NDM-000310` | CAT II | The network device must be configured to authenticate SNMP messages using a FIPS-validated Keyed-Hash Message Authentication Code (HMAC). |
| NDM | `SRG-APP-000395-NDM-000347` | CAT II | The network device must authenticate Network Time Protocol sources using authentication that is cryptographically based. |
| NDM | `SRG-APP-000408-NDM-000314` | CAT II | Network devices performing maintenance functions must restrict use of these functions to authorized personnel only. |
| NDM | `SRG-APP-000411-NDM-000330` | CAT I | The network devices must use FIPS-validated Keyed-Hash Message Authentication Code (HMAC) to protect the integrity of nonlocal maintenance and diagnostic communications. |
| NDM | `SRG-APP-000412-NDM-000331` | CAT I | The network device must be configured to implement cryptographic mechanisms using a FIPS 140-2 approved algorithm to protect the confidentiality of remote maintenance sessions |
| NDM | `SRG-APP-000435-NDM-000315` | CAT II | The network device must be configured to protect against known types of denial-of-service (DoS) attacks by employing organization-defined security safeguards. |
| NDM | `SRG-APP-000457-NDM-000352` | CAT II | The network device must install security-relevant firmware updates within 30 days unless the time period is directed by an authoritative source (e.g., IAVM, CTOs, DTMs, STIGs). |
| NDM | `SRG-APP-000503-NDM-000320` | CAT II | The network device must generate audit records when successful/unsuccessful logon attempts occur. |
| NDM | `SRG-APP-000505-NDM-000322` | CAT II | The network device must generate audit records showing starting and ending time for administrator access to the system. |
| NDM | `SRG-APP-000515-NDM-000325` | CAT II | The network device must off-load audit records onto a different system or media than the system being audited. |
| NDM | `SRG-APP-000516-NDM-000335` | CAT II | The network device must enforce access restrictions associated with changes to the system components. |
| NDM | `SRG-APP-000516-NDM-000336` | CAT I | The network device must be configured to use at least one authentication server for the purpose of authenticating users prior to granting administrative access. For boundary devices, two authentication servers are required. |
| NDM | `SRG-APP-000516-NDM-000340` | CAT II | The network device must be configured to conduct backups of system level information contained in the information system when changes occur. |
| NDM | `SRG-APP-000516-NDM-000344` | CAT II | The network device must obtain its public key certificates from an appropriate certificate policy through an approved service provider. |
| NDM | `SRG-APP-000516-NDM-000350` | CAT I | The network device must be configured to send log data to at least one central log server for the purpose of forwarding alerts to the administrators and the information system security officer (ISSO). For boundary devices, two log servers are required. |
| NDM | `SRG-APP-000795-NDM-000130` | CAT II | The network device must be configured to alert organization-defined personnel or roles upon detection of unauthorized access, modification, or deletion of audit information. |
| NDM | `SRG-APP-000820-NDM-000170` | CAT II | The network device must be configured to implement multifactor authentication for local; network; and/or remote access to privileged accounts; and/or nonprivileged accounts such that one of the factors is provided by a device separate from the system gaining access. |
| NDM | `SRG-APP-000825-NDM-000180` | CAT II | The network device must be configured to implement multifactor authentication for local; network; and/or remote access to privileged accounts; and/or nonprivileged accounts such that the device meets organization-defined strength of mechanism requirements. |
| NDM | `SRG-APP-000845-NDM-000220` | CAT II | The network device must be configured to verify, when users create or update passwords, the passwords are not found on the list of commonly used, expected, or compromised passwords in IA-5 (1) (a) for password-based authentication. |
| NDM | `SRG-APP-000860-NDM-000250` | CAT II | The network device must be configured to allow user selection of long passwords and passphrases, including spaces and all printable characters for password-based authentication. |
| NDM | `SRG-APP-000880-NDM-000290` | CAT II | The network device must be configured to protect nonlocal maintenance sessions by separating the maintenance session from other network sessions with the system by logically separated communications paths. |
| NDM | `SRG-APP-000910-NDM-000300` | CAT II | The network device must be configured to include only approved trust anchors in trust stores or certificate stores managed by the organization. |
| NDM | `SRG-APP-000920-NDM-000320` | CAT II | The network device must be configured to synchronize system clocks within and between systems or system components. |
| NDM | `SRG-APP-000925-NDM-000330` | CAT II | The network device must be configured to compare the internal system clocks on an organization-defined frequency with organization-defined authoritative time source. |
| NDM | `SRG-APP-001035-NDM-000340` | CAT I | The network device hardware and software must be a version supported by the vendor. |
| FW | `SRG-NET-000019-FW-000003` | CAT I | The firewall must be configured to use filters that use packet headers and packet attributes, including source and destination IP addresses and ports, to prevent the flow of unauthorized or suspicious traffic between interconnected networks with different security policies (including perimeter firewalls and server VLANs). |
| FW | `SRG-NET-000074-FW-000009` | CAT II | The firewall must generate traffic log entries containing information to establish what type of events occurred. |
| FW | `SRG-NET-000075-FW-000010` | CAT II | The firewall must generate traffic log entries containing information to establish when (date and time) the events occurred. |
| FW | `SRG-NET-000076-FW-000011` | CAT II | The firewall must generate traffic log entries containing information to establish the location on the network where the events occurred. |
| FW | `SRG-NET-000077-FW-000012` | CAT III | The firewall must generate traffic log entries containing information to establish the source of the events, such as the source IP address at a minimum. |
| FW | `SRG-NET-000078-FW-000013` | CAT II | The firewall must generate traffic log entries containing information to establish the outcome of the events, such as, at a minimum, the success or failure of the application of the firewall rule. |
| FW | `SRG-NET-000098-FW-000021` | CAT II | The firewall must be configured to use TCP when sending log records to the central audit server. |
| FW | `SRG-NET-000099-FW-000161` | CAT II | The firewall must protect the traffic log from unauthorized modification of local log records. |
| FW | `SRG-NET-000100-FW-000023` | CAT II | The firewall must protect the traffic log from unauthorized deletion of local log files and log records. |
| FW | `SRG-NET-000192-FW-000029` | CAT II | The firewall must block outbound traffic containing denial-of-service (DoS) attacks to protect against the use of internal information systems to launch any DoS attacks against other networks or endpoints. |
| FW | `SRG-NET-000193-FW-000030` | CAT II | The firewall implementation must manage excess bandwidth to limit the effects of packet flooding types of denial-of-service (DoS) attacks. |
| FW | `SRG-NET-000235-FW-000133` | CAT II | The firewall must fail to a secure state upon the failure of the following: system initialization, shutdown, or system abort. |
| FW | `SRG-NET-000333-FW-000014` | CAT II | The firewall must be configured to send traffic log entries to a central audit server for management and configuration of the traffic log entries. |
| FW | `SRG-NET-000335-FW-000017` | CAT II | If communication with the central audit server is lost, the firewall must generate a real-time alert to, at a minimum, the systems administrator (SA) and information system security officer (ISSO). |
| FW | `SRG-NET-000362-FW-000028` | CAT I | The firewall must employ filters that prevent or limit the effects of all types of commonly known denial-of-service (DoS) attacks, including flooding, packet sweeps, and unauthorized port scanning. |
| FW | `SRG-NET-000364-FW-000031` | CAT II | The firewall must apply ingress filters to traffic that is inbound to the network through any active external interface. |
| FW | `SRG-NET-000364-FW-000032` | CAT II | The firewall must apply egress filters to traffic that is outbound from the network through any internal interface. |
| FW | `SRG-NET-000364-FW-000042` | CAT II | The firewall must be configured to restrict it from accepting outbound packets that contain an illegitimate address in the source address field via an egress filter or by enabling Unicast Reverse Path Forwarding (uRPF). |
| FW | `SRG-NET-000392-FW-000042` | CAT III | The firewall must generate an alert that can be forwarded to, at a minimum, the ISSO and ISSM when denial-of-service (DoS) incidents are detected. |
| FW | `SRG-NET-000492-FW-000006` | CAT II | The firewall must generate traffic log records when traffic is denied, restricted, or discarded. |
| FW | `SRG-NET-000705-FW-000110` | CAT II | The firewall must be configured to employ organization-defined controls by type of denial-of-service (DoS) to achieve the DoS objective. |

### Collecting evidence

Run `show full-configuration` and `get system status` (the release, the
FortiGuard database versions, and the HA mode) and keep the output with
the checklist. Add screenshots or exports of the panes the map cites that
have no CLI: *System > Settings* (idle timeout, TLS versions, and pre-login
warning), *System > Admin > Access Profile*, *System > SNMP > Config*,
*System > Certificate > Web Administration*, and the IP, TCP, HTTP, and DNS
profiles of each SPP. Export the event log and the DDoS attack log, and the
*Log & Report > Log Access > Login Events* page, from the central log
server, and keep the firmware upgrade record and the configuration backup
schedule.

## Validation and Troubleshooting

- **A feature in the map is missing on your FortiDDoS.** Check the version
  column against the FortiDDoS-F release, and check whether the feature
  depends on the model, the VM, a FortiGuard subscription, or Asymmetric
  Mode (DNS profile options that cannot work in Asymmetric Mode are
  hidden).
- **A command is rejected.** The commands were checked against the CLI in
  the 8.0.0 Handbook. Older releases may lack the option or spell it
  differently, and CLI access needs the super_admin_prof or a full
  read-write access profile.
- **A setting is not where the map says.** Before 8.0.0 the *System >
  Settings* pane was *System > Admin > Settings*, and 8.0.1 reorganized the
  main menu; look for the setting under the older name.
- **Legitimate traffic is dropped after Prevention Mode is enabled.** Check
  the attack log for the threshold, anomaly, or ACL that dropped it,
  compare the thresholds with the traffic statistics, and adjust that
  threshold or profile option rather than returning the SPP to Detection
  Mode.
- **Logs do not reach the log server.** Check the remote log status, the
  protocol (UDP or TCP) and port, the minimum drops setting, and the path
  from the management port; UDP syslog gives no error when the server is
  not listening.
- **A requirement has no matching feature.** Some requirements are met by
  procedure (password changes), by another system (the authentication
  server, the central log server, the firewall behind FortiDDoS), or not at
  all. Record how each requirement is met, not just which feature covers
  it.

## Security and Best Practices

- Keep FortiDDoS on a vendor-supported release and install patches
  promptly, after checking the image checksum.
- Authenticate administrators against a RADIUS server with a second
  factor, keep one local account of last resort with a strong password,
  enable the password policy, and give each administrator the narrowest
  access profile that works.
- Allow only HTTPS with TLS 1.2 or 1.3 and SSH on the management port, set
  trusted hosts for every account, enable the pre-login warning with the
  DoD banner, and set the idle timeout to 10 minutes or less.
- Replace the factory web UI certificate with a DoD-issued certificate,
  use SNMPv3 with authentication and privacy only, and synchronize time
  with NTP.
- Keep FortiGuard IP and domain reputation current, review thresholds and
  the attack log regularly, and review this map each time Fortinet
  publishes a FortiDDoS-F release or DISA updates the NDM or Firewall SRG.

## References and Knowledge Checks

**References:**

- Fortinet, *FortiDDoS-F Release Notes*, page "What's new", releases 6.1.0
  to 6.1.5, 6.2.0 to 6.2.3, 6.3.0 (in the 6.3.1 release notes) to 6.3.3 and
  6.3.5, 6.4.0 to 6.4.2, 6.5.0 and 6.5.1, 6.6.0, 6.6.1, and 6.6.3, 7.0.0 to
  7.0.5, 7.2.0 to 7.2.4, and 8.0.0 and 8.0.1 (docs.fortinet.com, FortiDDoS-F
  documentation).
- Fortinet, *FortiDDoS-F 8.0.0 Handbook*, including Appendix J (Security
  Hardening).
- DISA Network Device Management SRG V5R5 and Firewall SRG V3R4, from the
  October 2026 STIG Library Compilation.
- [Chapter 03](03-the-srg-catalog-how-stigs-are-built-and-what-to-do-without-one.md)
  (SRG-based assessment),
  [Chapter 10](10-fortinet-products-stigs-and-srg-mapping.md) (Fortinet
  products),
  [Chapter 11](11-fortiswitch-feature-version-and-srg-map.md) (the
  FortiSwitch map), and
  [Chapter 12](12-fortianalyzer-feature-version-and-srg-map.md) (the
  FortiAnalyzer map, the model for this chapter).

**Knowledge checks:**

1. Which two SRGs apply to FortiDDoS, and which part of the appliance does
   each one cover?
2. Why does only part of the Firewall SRG apply to FortiDDoS, and which
   requirement is its CAT I DoS requirement?
3. Where does the version data come from, and why is there no CLI
   Reference behind the command column?
4. What is the difference between Detection Mode and Prevention Mode, and
   when should an SPP move from one to the other?
5. What does the choice between fail-open and fail-closed mean for the
   secure-state requirement?
6. Which requirements can FortiDDoS not meet exactly, and how do you handle
   them?

## Summary and Completion Checklist

FortiDDoS has no STIG, so it is assessed against the NDM SRG for its
management plane and against the denial-of-service, filtering, failure,
and logging requirements of the Firewall SRG for its mitigation function.
This chapter maps 292 features to the FortiDDoS-F release that
introduced them, to 90 SRG requirements, and to the FortiDDoS
command or web UI pane that configures them: 51 core platform
features, and 241 features from the FortiDDoS-F 6.1.0 through 8.0.1
release notes. Operational features with no direct requirement fall under
the requirement to disable unnecessary functions when unused.

- [ ] Can find the release that introduced a FortiDDoS-F feature.
- [ ] Can map a FortiDDoS feature to its NDM or Firewall SRG requirement.
- [ ] Can explain which Firewall SRG requirements apply to FortiDDoS.
- [ ] Can find the FortiDDoS command or web UI pane that meets the
  requirement.
- [ ] Can collect FortiDDoS evidence and record the requirements FortiDDoS
  cannot meet exactly.
