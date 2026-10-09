# Chapter 27: FortiClient and EMS Feature, Version, and SRG Map

## Learning Objectives

- Find the FortiClient or FortiClient EMS release that introduced a given
  feature, and tell which of the two products the release number belongs
  to.
- Map each FortiClient and EMS feature to the Unified Endpoint Management
  (UEM) Server SRG, UEM Agent SRG, or Virtual Private Network (VPN) SRG
  requirement it helps satisfy.
- Explain why the UEM SRGs are the closest match for EMS and the managed
  FortiClient agent, why the VPN SRG applies to the client's remote access
  role, and where the host operating system STIGs take over.
- Find the EMS GUI pane, the FortiClient XML setting, or the `emscli`
  command that configures each feature to meet its requirement.
- Use the map to scope an SRG-based assessment of FortiClient and EMS,
  which have no STIG of their own.
- Record the requirements that FortiClient and EMS cannot meet exactly,
  with their mitigations.

## Theory and Architecture

FortiClient is Fortinet's endpoint agent for Windows, macOS, and Linux
(with separate apps for iOS, Android, and Chromebooks). One agent provides
remote access VPN (SSL VPN and IPsec VPN), zero trust network access
(ZTNA) to applications behind a FortiGate, vulnerability scanning, web and
video filtering, malware protection (antivirus, anti-ransomware,
anti-exploit, removable media control, and sandboxing), an application
firewall, and compliance telemetry: it reports the state of the endpoint
so that it can be tagged and treated according to its security posture.
FortiClient EMS (Endpoint Management Server) is the server that manages
the agents. It deploys and upgrades FortiClient, pushes endpoint profiles
and policies to it, collects its status, software inventory, and events,
evaluates the security posture tags, and shares them with FortiGate
through the Security Fabric. This chapter treats the two together,
because neither is useful without the other and most settings are made on
EMS and enforced on the endpoint.

The pieces fit together like this:

- **FortiClient Telemetry.** Each agent registers with EMS over the
  endpoint control protocol, a TLS connection to EMS on port 8013 by
  default, optionally protected by a connection key. It sends a keepalive
  at the configured interval (60 seconds by default), reports changes, and
  receives new configuration.
- **Endpoint profiles and policies.** An *endpoint profile* holds the
  settings of one area (Remote Access, ZTNA Destinations, Web Filter,
  Video Filter, Vulnerability Scan, Malware Protection, Sandbox, Firewall,
  System Settings, and others). An *endpoint policy* combines profiles and
  assigns them to endpoint groups, AD groups, or users, with separate
  on-fabric and off-fabric profiles when on-fabric detection rules are
  used. Every profile is ultimately an XML document: the *XML
  Configuration* view of a profile shows the FortiClient XML, documented in
  the FortiClient XML Reference, and accepts settings that the GUI does
  not show.
- **Security posture tags.** Tagging rules (called Zero Trust tagging
  rules before 7.4) evaluate the endpoint's OS, software, vulnerabilities,
  certificates, and more. EMS shares the tags with FortiGate, which uses
  them in firewall and ZTNA policies, and FortiClient can allow or deny a
  VPN connection by tag.
- **The EMS server.** EMS 7.0 and 7.2 run on Windows Server with SQL
  Server. EMS 7.4.0 moved to a Linux-based model, and EMS 8.0.0 installs on
  Ubuntu 22.04 or 24.04 LTS, Red Hat Enterprise Linux 9, or CentOS Stream 9,
  with PostgreSQL, or as a VM image, a Docker Compose deployment, or a
  Kubernetes deployment. The Linux-based EMS has a command line, `emscli`,
  documented in the EMS CLI Reference from 7.4.4.

FortiClient and EMS have **no DISA STIG** (Chapter 10), so they are
assessed against SRGs, as described in Chapter 03. Chapter 10 assigns the
**host operating system STIG** to the endpoints, with the **VPN SRG** for
the client's remote access role, and the **Windows Server STIG** to the EMS
server, with the **UEM Server and Agent SRGs** as the closest match for
central endpoint management. For every FortiClient and EMS feature this
chapter gives **which FortiClient or EMS release introduced it**, **which
requirement it relates to**, and **which GUI pane, XML setting, or command
configures it to meet that requirement**.

### Where the version data comes from

Fortinet publishes no Feature Matrix for FortiClient or EMS, but it does
publish one **FortiClient & FortiClient EMS New Features Guide** per
release train: **7.0**, **7.2**, **7.4**, and **8.0** (docs.fortinet.com
lists no 7.6 train). Each guide covers both products and has an *Index*
page per release that lists the features added in that release, under
three headings: *ZTNA* (with the rows *Endpoint: Fabric Agent* and
*Endpoint: Remote Access*), which holds the FortiClient features;
*FortiClient EMS*, which holds the EMS features; and *Other*. The two
products also have separate release notes. The *What's new* page of the
**EMS release notes** only points to the New Features Guide, and the
**FortiClient (Windows) release notes** have no new-features section, so
the guides are the version source, and the release notes were used to
confirm the release lists:

- docs.fortinet.com lists FortiClient (Windows) release notes for 7.0.0 to
  7.0.14, 7.2.0 to 7.2.15, 7.4.0 to 7.4.8, and 8.0.0, and EMS release notes
  for 7.0.0 to 7.0.13 (no 7.0.5), 7.2.0 to 7.2.15 (no 7.2.11), 7.4.0 to
  7.4.8 (no 7.4.2), and 8.0.0.
- The guides list features up to 7.0.8, 7.2.5, and 7.4.8. The EMS release
  notes of the later releases that have a *What's new* page (7.0.9, 7.0.10,
  and 7.2.6 to 7.2.13) point to a guide that lists nothing for them, so
  those releases, like the rest of the later patch releases, have no
  entries.

The version column was built from the Index pages of the four guides with
these rules:

- Each linked feature is one entry, with the release of the Index heading
  it is listed under. In the 7.0 guide, whose Index is one page with a
  heading per release, the heading (FortiClient or EMS) comes from the
  guide's table of contents.
- The 7.2 Index omits one feature that the guide's table of contents lists
  for 7.2.3 (IPsec VPN autoconnect using Entra ID logon session
  information); it was added as an entry.
- The *FortiClient XML configuration changes* and *EMS CLI commands
  changes* links that the 7.4.5 to 8.0.0 Index pages list under *Other*
  point to the change logs of the XML Reference and the CLI Reference, not
  to features, and are not entries. A feature linked under two releases
  (*Zero Trust tag renamed to security posture tag*, under 7.4.0 and 7.4.3)
  is one entry, at the first release.
- The trains were maintained in parallel, so the same feature is sometimes
  listed in more than one train (the ZTNA application catalog in 7.2.5 and
  7.4.1, for example). Each listing is its own entry, and the map merges
  related entries into one row with one version per product and train.

That gives 208 entries: 29 in 7.0 (3 in 7.0.0, 9 each in 7.0.1
and 7.0.3, 3 in 7.0.6, 2 in 7.0.7, and 1 each in 7.0.2, 7.0.4, and 7.0.8),
76 in 7.2 (16 each in 7.2.0 and 7.2.1, 20 in 7.2.2, 9 in 7.2.3, 4 in
7.2.4, and 11 in 7.2.5), 87 in 7.4 (8 in 7.4.0, 20 in 7.4.1, 17 in 7.4.3,
15 in 7.4.4, 16 in 7.4.5, 7 in 7.4.6, and 4 in 7.4.8), and 16 in 8.0.0. By
product, 85 entries are FortiClient features, 122 are EMS features, and 1
(firmware maturity levels) applies to both. Each entry title was taken
from the guide and shortened where needed.

The table has two groups of rows:

- **Core platform features** (categories starting with *Core:*) are the
  long-standing capabilities that the requirements depend on: the EMS
  server, its console access, administrators, roles, session and lockout
  settings, login banner, certificates, logs, alerts, backups, and Feature
  Select; FortiClient Telemetry, profiles and policies, deployment, the
  disconnect lock, log upload, and updates; and the FortiClient remote
  access, endpoint protection, and ZTNA functions. Each one is described in
  the **FortiClient EMS 7.0.0 Administration Guide** or the **FortiClient
  7.0.0 XML Reference**, so it existed in the oldest train and is not in the
  New Features Guides. A few core rows have a different version entry,
  explained below.
- **New features** are the 208 entries of the guides, merged into
  122 rows. The categories were assigned for this chapter, and the
  titles were shortened from the guide text.

FortiClient and EMS share release numbers, so every version entry names
the product whose release introduced the feature:

| Version entry | Meaning |
| --- | --- |
| `EMS 7.0.0 or earlier` | A core EMS feature described in the EMS 7.0.0 Administration Guide, present in the oldest 7.x release |
| `FortiClient 7.0.0 or earlier` | A core FortiClient feature described in the FortiClient 7.0.0 XML Reference or the EMS 7.0.0 Administration Guide |
| `FortiClient and EMS 7.0.0 or earlier` | A core feature that needs both products (Telemetry, the disconnect lock, ZTNA) |
| `EMS 7.2.4 and later` | Introduced in EMS 7.2.4 (listed under *FortiClient EMS* in the guide); later releases and trains include it |
| `FortiClient 7.2.3 and later` | Introduced in FortiClient 7.2.3 (listed under *ZTNA*, *Endpoint: Fabric Agent* or *Endpoint: Remote Access*) |
| `FortiClient and EMS 7.4.4 and later` | Listed under *Other* for 7.4.4 (firmware maturity levels), which applies to both products |
| `EMS 7.2.5+; EMS 7.4.1+` | Listed in each of those releases; the first release listed in each product and train is shown |
| `EMS 8.0 (release not stated)` | Documented in the EMS 8.0.0 Administration Guide or CLI Reference but not in the EMS 7.0.0 Administration Guide, and in no New Features Guide (the administrator lockout settings, FIPS mode, and SNMP traps) |
| `FortiClient 8.0 (release not stated)` | Documented in the FortiClient 8.0.0 XML Reference but not in the 7.0.0 XML Reference, and in no New Features Guide (the invalid EMS certificate action and saved VPN passwords) |

Four cautions apply. First, a feature listed for one product often needs
the other: a FortiClient feature is usually configured in an EMS profile,
so it needs an EMS release that offers the setting, and many features also
need a FortiOS release on the FortiGate. Check both products and the
FortiGate before you rely on a row. Second, many FortiClient features are
specific to an operating system (Windows only, or not on Linux, for
example); the guides say which. Third, Fortinet revises the guides in
place, so a core row records a capability of the 7.0 train, but a detail
of it may have arrived in a later patch. Fourth, a row records a
capability, but its pane, XML setting, and command were checked against
the 8.0.0 documents; EMS 7.0 and 7.2 run on Windows Server, have no
`emscli`, and place some settings differently (the 7.0 guide's
*Administration > User Settings* became *Administration > Admin User
Settings*, for example).

### Where the SRG data comes from

The SRG column uses requirement IDs from the October 2026 DISA library:

| SRG column | SRG | Release | Applies to |
| --- | --- | --- | --- |
| **UEM-S** | Unified Endpoint Management Server SRG | V2R6, benchmark date 30 Sep 2026 | EMS: its administrators, sessions, audit records, cryptography, updates, and the management of endpoints (policy distribution, software deployment, inventory, and the trusted channel to the agents) |
| **UEM-A** | Unified Endpoint Management Agent SRG | V2R2, benchmark date 29 Jun 2026 | FortiClient as the managed agent: enrollment and unenrollment, accepting policies only from its server, certificates, audit records, and sending endpoint logs to a server |
| **VPN** | Virtual Private Network SRG | V3R5, benchmark date 01 Jul 2026 | FortiClient as the remote access VPN client: banner, authentication, certificate validation, IPsec and TLS cryptography, split tunneling, always-on VPN, and logout |

The two UEM SRGs come from one DISA package
(`U_UEM_Y26M10_SRG.zip`), which holds the UEM Server SRG and the UEM Agent
SRG.

**Why the UEM SRGs.** DISA has no SRG for endpoint protection platforms
or endpoint VPN managers. The UEM SRGs describe a server that enrolls
endpoints, pushes signed policies to an agent, deploys software, queries
the endpoints for their status, software, and logs, and keeps its own
accounts and audit records, and an agent that accepts that management.
That is what EMS and FortiClient do, so the **UEM Server SRG** is the
primary SRG for EMS and the **UEM Agent SRG** for the managed agent. The
UEM Server SRG also has its own requirement to disable non-essential
capabilities (UEM-S `SRG-APP-000141-UEM-000079`), so the Network Device
Management (NDM) SRG is not needed: EMS is a server application, not a
network device. The UEM SRGs were written with mobile devices in mind;
requirements about mobile device functions (wiping a work profile, for
example) have no FortiClient equivalent, and the map cites only the
requirements that EMS and FortiClient touch.

**Why the VPN SRG.** FortiClient is the remote access client of a
FortiGate VPN gateway. Most VPN SRG requirements are written for the
gateway and are assessed on the FortiGate (Chapter 10), but the client
must be configured to match: the IPsec proposals, Diffie-Hellman groups,
key lifetimes, and PFS of an IPsec VPN tunnel are set in the EMS Remote
Access profile, and the client is where the banner (the disclaimer
message) is shown, the gateway certificate is validated, smart cards are
used, and the tunnel is kept up. The map cites the VPN requirements that a
FortiClient setting implements or must match.

**The host operating systems.** Neither SRG covers the operating system
under EMS or FortiClient, and the map does not cite operating system
rules row by row. As Chapter 10 says, each **endpoint** is assessed
against its own operating system STIG (Windows 11, macOS, RHEL, Ubuntu,
iOS and iPadOS, and so on), and those STIGs also carry the endpoint's own
antivirus, firewall, and FIPS requirements, which FortiClient's malware
protection and firewall may help meet. The **EMS server** is assessed
against the **Windows Server STIG** for EMS 7.0 and 7.2. From EMS 7.4.0 the
server is a Linux host, so assess it against the STIG of its distribution
instead: the **RHEL 9 STIG** (V2R10 in the import) or the **Ubuntu 22.04
or 24.04 LTS STIG** (V2R10 and V1R7). CentOS Stream 9 has no STIG; use
RHEL 9 or Ubuntu for a DoD deployment, or assess CentOS Stream against the
General Purpose Operating System SRG. The map has one row for this
(UEM-S `SRG-APP-000516-UEM-000391`, configuration according to DoD
guidance, including STIGs).

The requirement IDs are the **rule version IDs** from the XCCDF files,
and the severity is the rule's severity (high = CAT I, medium = CAT II,
low = CAT III). Each feature maps to one of three kinds of relationship:

- **Implements a requirement.** The feature is how FortiClient or EMS
  meets a requirement. The EMS login banner implements the UEM Server
  banner requirement (UEM-S `SRG-APP-000068-UEM-000037`), and the
  disconnect lock implements the UEM Agent requirement to prevent
  unenrollment (UEM-A `SRG-APP-000516-UEM-100011`), for example.
- **Must be configured to meet a requirement.** The feature is in scope
  of a requirement and has to be set up correctly. An IPsec VPN tunnel must
  propose AES-256 and use Diffie-Hellman group 16 or higher (VPN
  `SRG-NET-000525-VPN-002330`, VPN `SRG-NET-000074-VPN-000250`), for
  example.
- **No direct requirement.** The feature is operational, such as a
  dashboard, a deployment option, a DNS or gateway selection improvement,
  or a protection function that no UEM or VPN requirement covers. It has
  no requirement of its own, but if it is not needed it falls under the UEM
  Server requirement to disable non-essential capabilities (UEM-S
  `SRG-APP-000141-UEM-000079`). 71 rows are of this kind. The
  endpoint protection functions (malware protection, web filtering, the
  application firewall, and sandboxing) are among them: they are often
  required by the endpoint's own STIG or by DoD policy, but not by the UEM
  or VPN SRGs.

The mapping is a starting point for an assessment, not a ruling. Confirm
it with your assessor, especially the use of the UEM SRGs for EMS and
FortiClient and the split between client and gateway VPN requirements.

### Where the commands come from

EMS is configured in its GUI, and FortiClient is configured through EMS
endpoint profiles. The command column was therefore built from the
**8.0.0** documents, the newest release: the **FortiClient EMS
Administration Guide** for every GUI pane and field, the **FortiClient XML
Reference** for every XML setting, and the **FortiClient EMS CLI
Reference** for every `emscli` command. The check was automatic: each GUI
pane had to appear in the Administration Guide, or be a heading path of its
outline (the left-pane section and the profile or page under it), and each
field label in parentheses had to appear in the guide; each XML element
had to be a documented tag that follows its parent in the reference's
samples, with a documented value; and each `emscli` command had to be a
documented command whose options and values appear in its section. All
132 GUI panes, 74 field labels, 25 XML settings, and 15 commands passed.
Read the column this way:

- **GUI:** entries name the EMS pane (*left-pane section > page or
  profile*); the text in parentheses names the fields to set, with the
  value where it matters. FortiClient settings are set in the endpoint
  profile and reach the endpoints through the endpoint policy.
- **XML:** entries give the element path below `<forticlient_configuration>`
  and the value to set, as `vpn/options/allow_personal_vpns=0`. Enter them
  in the profile's XML Configuration view (or import an XML file).
  Values in `<ANGLE_BRACKETS>` are placeholders for your own values, and a
  path to a `connection` element applies to each provisioned tunnel.
- Commands are `emscli` commands, run with `sudo` on the Linux-based EMS
  (EMS 7.4 and later) or in the EMS VM console. Statements are separated
  by `;` to fit in a table cell; enter each one on its own line.
- For **"No direct requirement"** rows, the entry shown is where the
  feature is turned off or left unconfigured when it is unused, often
  *System Settings > Feature Select* or `emscli feature set --disable`. A
  dash (**—**) means there is nothing to change: the feature is a platform
  change, a GUI change, a performance or compatibility improvement, or a
  capability that does nothing until it is configured.

Some requirements cannot be met exactly with FortiClient and EMS
settings. Record them on the checklist as open findings with mitigations,
or meet them another way:

- **Signed policies.** The UEM SRGs require EMS to sign each policy and
  FortiClient to accept only policies signed by an authorized certificate
  (UEM-S `SRG-APP-000427-UEM-000500`, UEM-S `SRG-APP-000427-UEM-000501`,
  UEM-S `SRG-APP-000427-UEM-000502`, all CAT I, and UEM-A
  `SRG-APP-000427-UEM-100007`). The guides document no signing of endpoint
  profiles or policies; they reach FortiClient over the TLS endpoint
  control connection. Install an EMS endpoint control certificate from a
  DoD-approved CA, set the FortiClient action on an invalid EMS
  certificate to deny (`endpoint_control/invalid_cert_action=deny`), keep
  the connection key, and record the finding.
- **FIPS-validated cryptography.** EMS can run in OpenSSL FIPS mode (the
  `enable_fips` installation parameter, or `EMS_FIPS_ENABLED` and `fips`
  for Docker and Kubernetes), but the guides cite no FIPS 140-3 validation
  for it (UEM-S `SRG-APP-000555-UEM-000393`, UEM-S
  `SRG-APP-000514-UEM-000389`). For FortiClient the guides document no FIPS
  mode at all, and the EMS 8.0.0 release notes list a known issue that
  the FIPS feature is unsupported but appears among the installer
  features (UEM-A `SRG-APP-000555-UEM-100014`, CAT I, and VPN
  `SRG-NET-000510-VPN-002170`). Ask Fortinet for the validation status of
  the release you deploy, rely on the operating system's validated
  modules where they apply, and record the finding.
- **Local administrator passwords.** The guides document no length,
  complexity, history, or change rules for EMS local administrator
  passwords, and do not say how they are stored (UEM-S
  `SRG-APP-000164-UEM-000094`, UEM-S `SRG-APP-000166-UEM-000096`, UEM-S
  `SRG-APP-000165-UEM-000095`, UEM-S `SRG-APP-000170-UEM-000100`, UEM-S
  `SRG-APP-000171-UEM-000101`). Only the password age is set (*Change
  password after x days*, which applies to built-in and EMS local users).
  Log administrators on through SAML SSO with an identity provider that
  enforces CAC, or through the directory, keep the built-in admin as the
  account of last resort, and give it a 15-character password by
  procedure.
- **Lockout.** *Admin Lockout Attempt* (3 by default, at most 10) locks an
  administrator out for the *Admin Lockout Period* in seconds, and the
  lockout ends when the period passes; it does not hold the account until
  an administrator releases it (UEM-S `SRG-APP-000345-UEM-000218`). Set a
  long lockout period, and let the directory or identity provider enforce
  the lockout for directory and SAML administrators.
- **Multifactor authentication.** EMS administrators get multifactor or
  CAC logon only through SAML SSO (UEM-S `SRG-APP-000149-UEM-000083`, UEM-S
  `SRG-APP-000154-UEM-000088`); the RADIUS logon added in 7.4.4 uses PAP,
  CHAP, or EAP-MD5. Use SAML with a CAC-enforcing identity provider.
- **Audit content of administrator actions.** The guides do not list
  which administrator actions EMS logs (account creation and changes,
  privileged functions, logons) or the fields of its log records, and they
  document no notification of account events (UEM-S
  `SRG-APP-000026-UEM-000015`, UEM-S
  `SRG-APP-000027-UEM-000016`, UEM-S `SRG-APP-000343-UEM-000216`, UEM-S
  `SRG-APP-000503-UEM-000378`, UEM-S `SRG-APP-000291-UEM-000165`). The EMS
  Administration Guide says to log all administrator activity for audit
  purposes.
  Send EMS system logs to FortiAnalyzer or syslog, check the records during
  the assessment, and alert on account events there.
- **Software verification.** The guides describe no digital signature
  check of EMS installers before an EMS upgrade (UEM-S
  `SRG-APP-000479-UEM-000354`, UEM-S `SRG-APP-000131-UEM-000076`), and the
  automatic upgrade to the latest patch release (added in 7.2.5) is enabled
  by default in the 8.0.0 guide. Turn
  off automatic upgrade where upgrades go through change control, verify
  each installer's hash against the Fortinet support site, and sign the
  FortiClient installers that EMS builds with your own code signing
  certificate (*Sign Software Packages*).
- **VPN client gaps.** The SSL VPN TLS version is negotiated with the
  FortiGate, and the Remote Access profile has no minimum TLS version
  setting (VPN `SRG-NET-000062-VPN-000200`, VPN
  `SRG-NET-000530-VPN-002340`); split tunneling is offered by the gateway
  (VPN `SRG-NET-000369-VPN-001620`); and the guides document no explicit
  logout message (VPN `SRG-NET-000519-VPN-002290`). Enforce TLS 1.2 or
  later and full tunnels on the FortiGate, leave the profile's split tunnel
  and network exclusion settings empty, and record the logout message as a
  finding. IPsec VPN is the better choice: from 7.4.6 EMS hides the SSL VPN
  option by default, and FortiClient 8.0.0 supports only IKEv2 for IPsec
  VPN.
- **Unenrollment.** The disconnect lock prevents users from disconnecting
  FortiClient from EMS, but two options weaken it: *Allow endpoint admin to
  disconnect without a password*, and uninstalling by an endpoint
  administrator without the key (7.2.1). Leave both off (UEM-A
  `SRG-APP-000516-UEM-100011`). FortiClient cannot wipe the device, so
  preventing the unenrollment is the option that applies.
- **SNMP traps.** EMS sends SNMP traps with a community string only
  (`emscli config set snmp`). Leave SNMP traps disabled (UEM-S
  `SRG-APP-000141-UEM-000079`).
- **Cloud services.** FortiAI (8.0.0) sends administrator queries to
  `fortiai.forticloud.com`, *Statistics Collection* (8.0.0) is enabled by
  default, the FortiGuard Forensics service uploads endpoint artifacts to
  Fortinet, and endpoints can send usage statistics. Disable each one
  unless the authorizing official approves it (UEM-S
  `SRG-APP-000141-UEM-000079`).
- **No STIG.** Without a STIG there is no DoD baseline for FortiClient or
  EMS themselves; use this map, the UEM and VPN SRGs, and the operating
  system STIGs as the baseline, and record the settings that differ from
  it.

## Design Considerations

- **Pick the releases first, then the features.** If your design depends
  on a feature introduced in a certain release (IPsec VPN only when
  connected to EMS in FortiClient 7.2.1, secure remote access compliance in
  FortiClient 7.2.3, the Linux-based EMS in 7.4.0, RADIUS for EMS
  administrators in 7.4.4, scheduled EMS backups in 7.4.5), that sets the
  minimum release of both products, and they must be vendor-supported
  releases (UEM-S `SRG-APP-001035-UEM-000408`).
- **Choose the EMS platform deliberately.** EMS 7.4 and later run on
  Linux; plan the host STIG (RHEL 9 or Ubuntu), FIPS mode at installation,
  and the PostgreSQL database (local or remote) together, and migrate a
  Windows Server EMS 7.2 with Fortinet's migration tool.
- **Prefer IPsec VPN and ZTNA.** Build remote access on IKEv2 IPsec VPN
  with AES-256, SHA-384, Diffie-Hellman group 16 or higher, and PFS, or on
  ZTNA, with smart card (CAC) certificates or SAML with a CAC-enforcing
  identity provider, and require the gateway to check the EMS serial number
  and the endpoint's security posture tags.
- **Lock the agent to EMS.** Deploy FortiClient from EMS installers with a
  connection key, the disconnect lock, and the invalid certificate action
  set to deny, and install the EMS certificates from a DoD-approved CA, so
  that endpoints accept configuration only from your EMS.
- **Keep EMS on the management network.** Restrict remote HTTPS access to
  allowed hosts, restrict administrators to trusted hosts, open only the
  ports in *Required services and ports*, and enable the EMS host firewall
  (UEM-S `SRG-APP-000142-UEM-000080`).
- **Send the logs out.** Send EMS system logs and FortiClient logs
  (including OS events) to FortiAnalyzer or syslog, and back up the EMS
  database weekly or more often to another system (UEM-S
  `SRG-APP-000125-UEM-000074`, UEM-S `SRG-APP-000358-UEM-000228`).
- **Turn off what is not used.** Use Feature Select to remove the features
  you do not use (Chromebooks, SSL VPN, Web Filter, forensics, FortiPAM,
  and so on), and disable personal VPNs, FortiAI, statistics collection,
  SNMP traps, and multitenancy unless they are needed.

## Implementation and Automation

### The FortiClient and EMS feature map

The SRG column uses the abbreviations defined in *Where the SRG data
comes from*: **UEM-S** is the UEM Server SRG, **UEM-A** the UEM Agent SRG,
and **VPN** the Virtual Private Network SRG. The requirement titles are
listed in the next table. The command column follows the conventions in
*Where the commands come from*.

[Download the feature map as CSV](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/data/volume-172-disa-srgs-and-stigs/27-forticlient-and-ems-feature-version-and-srg-map-feature-map.csv) (185 rows).

| Category | Feature | Introduced (FortiClient or EMS) | SRG requirement(s) | Command to satisfy the requirement |
| --- | --- | --- | --- | --- |
| Core: EMS platform | EMS server host: Windows Server for EMS 7.0 and 7.2; Linux (Ubuntu 22.04 or 24.04, RHEL 9, CentOS Stream 9) from EMS 7.4.0 | EMS 7.0.0 or earlier | UEM-S `SRG-APP-000516-UEM-000391` | Assess the host against its operating system STIG (see Where the SRG data comes from) |
| Core: EMS platform | Supported EMS release and EMS upgrades | EMS 7.0.0 or earlier | UEM-S `SRG-APP-001035-UEM-000408`; UEM-S `SRG-APP-000456-UEM-000330`; UEM-S `SRG-APP-000479-UEM-000354` | GUI: Dashboard > Status (System Information); `emscli execute upgrade ems --local.file <INSTALLER_FILE>` |
| Core: EMS platform | EMS FIPS mode (OpenSSL FIPS mode, set at installation) | EMS 8.0 (release not stated) | UEM-S `SRG-APP-000514-UEM-000389`; UEM-S `SRG-APP-000555-UEM-000393`; UEM-S `SRG-APP-000179-UEM-000110`; UEM-S `SRG-APP-000412-UEM-000283` | Install with the enable_fips installation parameter; `emscli system get info fips` |
| Core: EMS platform | Required services and ports, and the EMS host firewall | EMS 7.0.0 or earlier | UEM-S `SRG-APP-000142-UEM-000080`; UEM-S `SRG-APP-000383-UEM-000254` | `emscli execute enable-firewall`; `emscli system set firewall deny --adapter <ADAPTER> --service <SERVICE>` |
| Core: EMS platform | Remote HTTPS access to the EMS console, allowed hosts, and HTTP-to-HTTPS redirect | EMS 7.0.0 or earlier | UEM-S `SRG-APP-000191-UEM-000118`; UEM-S `SRG-APP-000412-UEM-000283`; UEM-S `SRG-APP-000439-UEM-000313` | GUI: System Settings > EMS Settings (Remote HTTPS Access: on, Redirect HTTP Request to HTTPS: on); `emscli config set console --allowed.hosts <HOST_LIST>` |
| Core: EMS platform | TLS 1.0 and 1.1 for EMS file downloads | EMS 7.0.0 or earlier | UEM-S `SRG-APP-000014-UEM-000009` | GUI: System Settings > EMS Settings (Enable TLS 1.0/1.1: off) |
| Core: EMS platform | EMS server certificates (web server, endpoint control, and Chromebook services) | EMS 7.0.0 or earlier | UEM-S `SRG-APP-000427-UEM-000298`; UEM-S `SRG-APP-000191-UEM-000119`; UEM-S `SRG-APP-000605-UEM-000401` | GUI: System Settings > EMS Server Certificates; GUI: System Settings > EMS Settings (Webserver Certificate, Endpoint Control Certificate) (certificates from a DoD-approved CA) |
| Core: EMS platform | EMS database backup and restore | EMS 7.0.0 or earlier | UEM-S `SRG-APP-000125-UEM-000074` | `emscli execute backup --remote.file <FILE> --remote.ip <HOST> --remote.user <USER> --compress.type zip --backup.password <PASSWORD>` |
| Core: EMS platform | Time stamps from the EMS host clock | EMS 7.0.0 or earlier | UEM-S `SRG-APP-000116-UEM-000067`; UEM-S `SRG-APP-000374-UEM-000244` | `emscli execute time synch` (synchronize the host with DoD-approved time sources) |
| Core: EMS platform | Feature Select (features shown in EMS and enabled on endpoints) | EMS 7.0.0 or earlier | UEM-S `SRG-APP-000141-UEM-000079`; UEM-S `SRG-APP-000383-UEM-000254` | GUI: System Settings > Feature Select; `emscli feature set --disable --name <FEATURE>` |
| Core: EMS platform | SNMP traps from EMS (community string) | EMS 8.0 (release not stated) | No direct requirement; if unused, disable (UEM-S `SRG-APP-000141-UEM-000079`) | `emscli config get snmp` (leave SNMP traps disabled) |
| Core: EMS platform | Multitenancy (multiple customer sites) | EMS 7.0.0 or earlier | No direct requirement; if unused, disable (UEM-S `SRG-APP-000141-UEM-000079`) | GUI: System Settings > EMS Settings (Manage Multiple Customer Sites: off) |
| Core: EMS platform | Chromebook management (Google domains and the Web Filter extension) | EMS 7.0.0 or earlier | No direct requirement; if unused, disable (UEM-S `SRG-APP-000141-UEM-000079`) | GUI: System Settings > Feature Select |
| Core: EMS administration | Administrator accounts: built-in admin, EMS local, Windows, and LDAP administrators, with trusted hosts | EMS 7.0.0 or earlier | UEM-S `SRG-APP-000148-UEM-000082`; UEM-S `SRG-APP-000151-UEM-000085`; UEM-S `SRG-APP-000329-UEM-000202` | GUI: Administration > Admin Users (Restrict Login to Trusted Hosts: on) (keep the built-in admin as the account of last resort) |
| Core: EMS administration | Administrator roles (super, standard, endpoint, read-only, restricted, and custom roles) | EMS 7.0.0 or earlier | UEM-S `SRG-APP-000380-UEM-000251`; UEM-S `SRG-APP-000133-UEM-000078`; UEM-S `SRG-APP-000090-UEM-000051` | GUI: Administration > Admin Roles |
| Core: EMS administration | Session expiry, disabling of inactive administrator accounts, and password age | EMS 7.0.0 or earlier | UEM-S `SRG-APP-000295-UEM-000169`; UEM-S `SRG-APP-000003-UEM-000003`; UEM-S `SRG-APP-000025-UEM-000014`; UEM-S `SRG-APP-000174-UEM-000104` | GUI: Administration > Admin User Settings (Expire login session after x minutes: 15, Disable administrators' accounts when inactive for x days: 35, Change password after x days: 180) |
| Core: EMS administration | Administrator lockout after failed logons | EMS 8.0 (release not stated) | UEM-S `SRG-APP-000065-UEM-000036`; UEM-S `SRG-APP-000345-UEM-000218` | GUI: System Settings > EMS Settings (Admin Lockout Attempt: 3, Admin Lockout Period) |
| Core: EMS administration | Login banner before EMS logon | EMS 7.0.0 or earlier | UEM-S `SRG-APP-000068-UEM-000037`; UEM-S `SRG-APP-000069-UEM-000038` | GUI: System Settings > EMS Settings (Enable login banner: on) (enter the Standard Mandatory DoD Notice and Consent Banner) |
| Core: EMS administration | Local administrator passwords | EMS 7.0.0 or earlier | UEM-S `SRG-APP-000164-UEM-000094`; UEM-S `SRG-APP-000166-UEM-000096`; UEM-S `SRG-APP-000165-UEM-000095`; UEM-S `SRG-APP-000170-UEM-000100`; UEM-S `SRG-APP-000171-UEM-000101` | — (no password length, complexity, or history setting is documented; use directory accounts) |
| Core: EMS administration | Administrator authentication through Active Directory (LDAP or LDAPS) | EMS 7.0.0 or earlier | UEM-S `SRG-APP-000023-UEM-000012`; UEM-S `SRG-APP-000148-UEM-000082`; UEM-S `SRG-APP-000191-UEM-000117` | GUI: Administration > Authentication Servers (LDAPS connection: on, Certificate hostname check: on) |
| Core: EMS administration | SAML single sign-on for administrators (FortiAuthenticator, FortiGate, Entra ID, Okta, AD FS) | EMS 7.0.0 or earlier | UEM-S `SRG-APP-000149-UEM-000083`; UEM-S `SRG-APP-000154-UEM-000088`; UEM-S `SRG-APP-000177-UEM-000108` | GUI: Administration > SAML SSO (use an identity provider that enforces CAC) |
| Core: EMS administration | Fabric devices: FortiGate connections authorized by EMS | EMS 7.0.0 or earlier | UEM-S `SRG-APP-000191-UEM-000117`; UEM-S `SRG-APP-000580-UEM-000398` | GUI: Fabric & Connectors > Fabric Devices (authorize only known FortiGates) |
| Core: EMS logging | EMS logs: log level and automatic clearing of logs, alerts, and events | EMS 7.0.0 or earlier | UEM-S `SRG-APP-000089-UEM-000049`; UEM-S `SRG-APP-000090-UEM-000051`; UEM-S `SRG-APP-000120-UEM-000070` | GUI: System Settings > Logs (Log level: Info, Automatically clear logs older than) |
| Core: EMS logging | Log Viewer | EMS 7.0.0 or earlier | UEM-S `SRG-APP-000516-UEM-000392`; UEM-S `SRG-APP-000089-UEM-000050`; UEM-S `SRG-APP-000118-UEM-000068` | GUI: Administration > Log Viewer |
| Core: EMS logging | EMS alerts by email, and the SMTP server | EMS 7.0.0 or earlier | UEM-S `SRG-APP-000474-UEM-000349`; UEM-S `SRG-APP-000108-UEM-000062`; UEM-S `SRG-APP-000191-UEM-000117` | GUI: System Settings > EMS Alerts; GUI: System Settings > SMTP Server (Security: SMTPS) |
| Core: EMS logging | Endpoint alerts (malware, vulnerabilities, out-of-date signatures and software, Telemetry disconnected by the user) | EMS 7.0.0 or earlier | UEM-A `SRG-APP-000089-UEM-100002`; UEM-S `SRG-APP-000474-UEM-000349` | GUI: System Settings > Endpoint Alerts |
| Core: Endpoint management | FortiClient Telemetry: endpoint control connection to EMS over TLS (port 8013) with a connection key | FortiClient and EMS 7.0.0 or earlier | UEM-S `SRG-APP-000191-UEM-000119`; UEM-S `SRG-APP-000395-UEM-000266`; UEM-S `SRG-APP-000580-UEM-000398`; UEM-S `SRG-APP-000439-UEM-000313`; UEM-A `SRG-APP-000516-UEM-100010` | GUI: System Settings > EMS Settings (FortiClient Telemetry Connection Key) (endpoints register with the EMS FQDN) |
| Core: Endpoint management | Disconnect lock: Require Password to Disconnect from EMS (with silent registration and disable unregister) | FortiClient and EMS 7.0.0 or earlier | UEM-A `SRG-APP-000516-UEM-100011`; UEM-A `SRG-APP-000516-UEM-100010` | GUI: Endpoint Profiles > System Settings (Require Password to Disconnect from EMS: on); XML: `endpoint_control/disable_unregister=1` |
| Core: Endpoint management | Action on an invalid EMS certificate (allow, warn, or deny) | FortiClient 8.0 (release not stated) | UEM-A `SRG-APP-000175-UEM-100008`; UEM-A `SRG-APP-000516-UEM-100006`; UEM-S `SRG-APP-000395-UEM-000266` | XML: `endpoint_control/invalid_cert_action=deny` |
| Core: Endpoint management | Keep-alive interval and offline timeout of endpoints | EMS 7.0.0 or earlier | UEM-S `SRG-APP-000472-UEM-000347` | GUI: System Settings > EMS Settings (Keep Alive Interval, Offline Timeout) |
| Core: Endpoint management | Endpoint policies and profiles assigned to endpoint groups | EMS 7.0.0 or earlier | UEM-S `SRG-APP-000427-UEM-000500`; UEM-S `SRG-APP-000427-UEM-000501`; UEM-S `SRG-APP-000427-UEM-000502`; UEM-A `SRG-APP-000427-UEM-100007`; UEM-A `SRG-APP-000089-UEM-100004` | GUI: Endpoint Policy & Components > Manage Policies; GUI: Endpoint Profiles > Manage Profiles |
| Core: Endpoint management | Endpoint list, status, and actions (quarantine, block, deregister, scan, upload logs) | EMS 7.0.0 or earlier | UEM-S `SRG-APP-000472-UEM-000347`; VPN `SRG-NET-000314-VPN-001060` | GUI: Endpoints > All Endpoints |
| Core: Endpoint management | Software inventory of endpoints | EMS 7.0.0 or earlier | UEM-S `SRG-APP-000472-UEM-000347` | GUI: Software Inventory > Applications |
| Core: Endpoint management | FortiClient installers and deployment to endpoints | EMS 7.0.0 or earlier | UEM-S `SRG-APP-000378-UEM-000248`; UEM-S `SRG-APP-000456-UEM-000330` | GUI: Deployment & Installers > Manage Deployment; GUI: Deployment & Installers > FortiClient Installer |
| Core: Endpoint management | Code signing of Windows installers (Sign Software Packages) | EMS 7.0.0 or earlier | UEM-S `SRG-APP-000427-UEM-000299`; UEM-S `SRG-APP-000427-UEM-000300`; UEM-S `SRG-APP-000131-UEM-000076` | GUI: System Settings > EMS Settings (Sign Software Packages: on) |
| Core: Endpoint management | CA certificates installed on endpoints | EMS 7.0.0 or earlier | UEM-A `SRG-APP-000427-UEM-100009`; UEM-S `SRG-APP-000427-UEM-000298` | GUI: Endpoint Policy & Components > CA Certificates; GUI: Endpoint Profiles > System Settings (Install CA Certificate on Client: on) |
| Core: Endpoint management | Security posture (Zero Trust) tagging rules | EMS 7.0.0 or earlier | UEM-S `SRG-APP-000378-UEM-000249` | GUI: Security Posture Tags > Security Posture Tagging Rules |
| Core: Endpoint management | On-fabric detection rules (separate on-fabric and off-fabric profiles) | EMS 7.0.0 or earlier | No direct requirement; if unused, disable (UEM-S `SRG-APP-000141-UEM-000079`) | GUI: Endpoint Policy & Components > On-fabric Detection Rules |
| Core: Endpoint management | Quarantine management of files and allowlist | EMS 7.0.0 or earlier | No direct requirement; if unused, disable (UEM-S `SRG-APP-000141-UEM-000079`) | GUI: Quarantine Management > Files |
| Core: FortiClient logging | FortiClient local logs: level and logged features | FortiClient 7.0.0 or earlier | UEM-A `SRG-APP-000089-UEM-100004`; UEM-A `SRG-APP-000097-UEM-100005`; UEM-A `SRG-APP-000089-UEM-100012` | GUI: Endpoint Profiles > System Settings (Level: Info, Features); XML: `system/log_settings/level=6` |
| Core: FortiClient logging | FortiClient log upload to FortiAnalyzer or syslog, with OS events and software inventory | FortiClient 7.0.0 or earlier | UEM-A `SRG-APP-000358-UEM-100013`; UEM-A `SRG-APP-000358-UEM-100003`; UEM-S `SRG-APP-000358-UEM-000228`; UEM-S `SRG-APP-000515-UEM-000390`; VPN `SRG-NET-000334-VPN-001260` | GUI: Endpoint Profiles > System Settings (Upload Logs to FortiAnalyzer/FortiManager: on, SSL Enabled: on, Send OS Events: on); XML: `system/log_settings/remote_logging/log_upload_ssl_enabled=1` |
| Core: FortiClient agent | Signature and engine updates from FortiGuard or FortiManager | EMS 7.0.0 or earlier | UEM-S `SRG-APP-000456-UEM-000330`; UEM-S `SRG-APP-000439-UEM-000313` | GUI: System Settings > FortiGuard Services (Enable SSL: on); GUI: Endpoint Profiles > System Settings (FortiGuard Server Location) |
| Core: Remote access | Provisioned SSL VPN and IPsec VPN tunnels (Remote Access profile) | FortiClient 7.0.0 or earlier | VPN `SRG-NET-000371-VPN-001650`; VPN `SRG-NET-000510-VPN-002170`; VPN `SRG-NET-000138-VPN-000490` | GUI: Endpoint Profiles > Remote Access |
| Core: Remote access | Personal VPN connections created by the user | FortiClient 7.0.0 or earlier | VPN `SRG-NET-000132-VPN-000450`; VPN `SRG-NET-000019-VPN-000040` | GUI: Endpoint Profiles > Remote Access (Allow Personal VPN: off); XML: `vpn/options/allow_personal_vpns=0` |
| Core: Remote access | VPN gateway certificate validation | FortiClient 7.0.0 or earlier | VPN `SRG-NET-000580-VPN-002410`; VPN `SRG-NET-000164-VPN-000560`; VPN `SRG-NET-000355-VPN-002433` | GUI: Endpoint Profiles > Remote Access (Do Not Accept Invalid Server Certificate: on); XML: `vpn/sslvpn/options/disallow_invalid_server_certificate=1`; XML: `vpn/ipsecvpn/options/disallow_invalid_server_certificate=1` |
| Core: Remote access | VPN disclaimer message the user must accept | FortiClient 7.0.0 or earlier | VPN `SRG-NET-000041-VPN-000110`; VPN `SRG-NET-000042-VPN-000120` | GUI: Endpoint Profiles > Remote Access (Disclaimer Message); XML: `vpn/ipsecvpn/connections/connection/disclaimer_msg=<DOD_NOTICE>` |
| Core: Remote access | Certificate and smart card (CAC) authentication for VPN | FortiClient 7.0.0 or earlier | VPN `SRG-NET-000341-VPN-001350`; VPN `SRG-NET-000342-VPN-001360`; VPN `SRG-NET-000140-VPN-000500`; VPN `SRG-NET-000145-VPN-000510`; VPN `SRG-NET-000166-VPN-000590`; UEM-A `SRG-APP-000176-UEM-100001` | GUI: Endpoint Profiles > Remote Access (Use Smart Card Certificates: on); XML: `vpn/ipsecvpn/options/usesmcardcert=1`; XML: `vpn/ipsecvpn/connections/connection/ike_settings/authentication_method=Smartcard X509 Certificate` |
| Core: Remote access | IPsec VPN phase 1: IKE version, DH groups, proposals, and key life | FortiClient 7.0.0 or earlier | VPN `SRG-NET-000512-VPN-002220`; VPN `SRG-NET-000132-VPN-000460`; VPN `SRG-NET-000074-VPN-000250`; VPN `SRG-NET-000317-VPN-001090`; VPN `SRG-NET-000230-VPN-000780`; VPN `SRG-NET-000337-VPN-001300` | GUI: Endpoint Profiles > Remote Access (DH Groups, Key Life); XML: `vpn/ipsecvpn/connections/connection/ike_settings/version=2`; XML: `vpn/ipsecvpn/connections/connection/ike_settings/dhgroup=<DH_GROUPS>`; XML: `vpn/ipsecvpn/connections/connection/ike_settings/proposals/proposal=<PROPOSAL>` (AES256 with SHA384, DH group 16 or higher, key life 28800 seconds or less) |
| Core: Remote access | IPsec VPN phase 2: proposals, PFS, replay detection, and key life | FortiClient 7.0.0 or earlier | VPN `SRG-NET-000525-VPN-002330`; VPN `SRG-NET-000063-VPN-000220`; VPN `SRG-NET-000371-VPN-001640`; VPN `SRG-NET-000147-VPN-000530`; VPN `SRG-NET-000337-VPN-001290` | GUI: Endpoint Profiles > Remote Access (Enable Replay Detection: on, Enable Perfect Forward Secrecy (PFS): on); XML: `vpn/ipsecvpn/connections/connection/ipsec_settings/pfs=1`; XML: `vpn/ipsecvpn/connections/connection/ipsec_settings/replay_detection=1`; XML: `vpn/ipsecvpn/connections/connection/ipsec_settings/key_life_seconds=<SECONDS>` |
| Core: Remote access | Split tunnel and negative split tunnel (network exclusion, application based) | FortiClient 7.0.0 or earlier | VPN `SRG-NET-000369-VPN-001620` | GUI: Endpoint Profiles > Remote Access (Split Tunnel) (leave unset, and disable split tunneling on the FortiGate) |
| Core: Remote access | VPN autoconnect, always up, and VPN before logon | FortiClient 7.0.0 or earlier | VPN `SRG-NET-000230-VPN-002436` | GUI: Endpoint Profiles > Remote Access (Show VPN before Logon: on); XML: `vpn/options/autoconnect_tunnel=<TUNNEL_NAME>` |
| Core: Remote access | Disconnect IPsec VPN when the user logs off | FortiClient 7.0.0 or earlier | VPN `SRG-NET-000518-VPN-002280`; VPN `SRG-NET-000213-VPN-000720` | XML: `vpn/ipsecvpn/options/disconnect_on_log_off=1` |
| Core: Remote access | Block IPv6 traffic outside the IPsec VPN interface | FortiClient 7.0.0 or earlier | VPN `SRG-NET-000371-VPN-001650` | XML: `vpn/ipsecvpn/options/block_ipv6=1` |
| Core: Remote access | Saved VPN passwords | FortiClient 8.0 (release not stated) | No direct requirement; if unused, disable (UEM-S `SRG-APP-000141-UEM-000079`) | XML: `vpn/ipsecvpn/connections/connection/ui/save_password=0` |
| Core: Endpoint protection | Malware Protection: antivirus real-time protection and scans, anti-exploit, cloud-based malware detection | FortiClient 7.0.0 or earlier | No direct requirement; if unused, disable (UEM-S `SRG-APP-000141-UEM-000079`) | GUI: Endpoint Profiles > Malware Protection |
| Core: Endpoint protection | Removable media access control | FortiClient 7.0.0 or earlier | No direct requirement; if unused, disable (UEM-S `SRG-APP-000141-UEM-000079`) | GUI: Endpoint Profiles > Malware Protection (Removable Media Access) |
| Core: Endpoint protection | Sandbox detection (FortiSandbox) | FortiClient 7.0.0 or earlier | No direct requirement; if unused, disable (UEM-S `SRG-APP-000141-UEM-000079`) | GUI: Endpoint Profiles > Sandbox |
| Core: Endpoint protection | Web Filter | FortiClient 7.0.0 or earlier | No direct requirement; if unused, disable (UEM-S `SRG-APP-000141-UEM-000079`) | GUI: Endpoint Profiles > Web Filter |
| Core: Endpoint protection | Application Firewall | FortiClient 7.0.0 or earlier | No direct requirement; if unused, disable (UEM-S `SRG-APP-000141-UEM-000079`) | GUI: Endpoint Profiles > Firewall |
| Core: Endpoint protection | Vulnerability Scan of endpoints | FortiClient 7.0.0 or earlier | UEM-S `SRG-APP-000472-UEM-000347` | GUI: Endpoint Profiles > Vulnerability Scan; GUI: Dashboard > Vulnerability Scan |
| Core: Endpoint protection | Single Sign-On Mobility Agent (SSOMA) for FortiAuthenticator | FortiClient 7.0.0 or earlier | No direct requirement; if unused, disable (UEM-S `SRG-APP-000141-UEM-000079`) | GUI: Endpoint Profiles > System Settings (FortiClient Single Sign-On Mobility Agent: off) |
| Core: Endpoint protection | Usage statistics sent to Fortinet from endpoints | FortiClient 7.0.0 or earlier | No direct requirement; if unused, disable (UEM-S `SRG-APP-000141-UEM-000079`) | GUI: Endpoint Profiles > System Settings (Send Usage Statistics to Fortinet: off) |
| Core: ZTNA | ZTNA connection rules and ZTNA destinations (TCP forwarding through the FortiGate ZTNA access proxy) | FortiClient and EMS 7.0.0 or earlier | VPN `SRG-NET-000343-VPN-001370`; VPN `SRG-NET-000371-VPN-001650` | GUI: Endpoint Profiles > ZTNA Destinations |
| Remote access | SSL VPN security improvements: the Do Not Warn Invalid Server Certificate option removed and off by default | FortiClient 7.0.0 and later | VPN `SRG-NET-000580-VPN-002410`; VPN `SRG-NET-000164-VPN-000560` | GUI: Endpoint Profiles > Remote Access (Do Not Accept Invalid Server Certificate: on) |
| User verification | Sending invitation emails to endpoint users | EMS 7.0.0 and later | No direct requirement; if unused, disable (UEM-S `SRG-APP-000141-UEM-000079`) | GUI: User Management > Invitations |
| Endpoint management | FortiClient license and EMS communication enhancements: prohibit users from shutting down FortiClient, locally stored license expiry | EMS 7.0.0 and later | UEM-A `SRG-APP-000516-UEM-100011` | GUI: Endpoint Profiles > System Settings (Allow User to Shutdown When Registered to EMS: off); XML: `system/ui/allow_shutdown_when_registered=0` |
| ZTNA | Improved TCP forwarding performance | FortiClient 7.0.1 and later | No direct requirement; if unused, disable (UEM-S `SRG-APP-000141-UEM-000079`) | — |
| Remote access | Dual stack IPv4 and IPv6 for SSL VPN, and on FortiClient (Linux) | FortiClient 7.0.1+; FortiClient 7.2.5+ | No direct requirement; if unused, disable (UEM-S `SRG-APP-000141-UEM-000079`) | — |
| Remote access | SAML authentication for SSL VPN (browser as external user agent) and IPsec VPN | FortiClient 7.0.1+; FortiClient 7.2.4+ | VPN `SRG-NET-000140-VPN-000500`; VPN `SRG-NET-000166-VPN-000580`; VPN `SRG-NET-000145-VPN-000510` | GUI: Endpoint Profiles > Remote Access (use an identity provider that enforces CAC) |
| ZTNA | EMS distributes FortiGate SSL deep inspection CA certificates | EMS 7.0.1 and later | UEM-A `SRG-APP-000427-UEM-100009` | GUI: Endpoint Policy & Components > CA Certificates |
| Security posture tags | Zero Trust tagging rule enhancements: vulnerability severity, OS comparators, macOS 14, FortiClient version, wildcard certificate subject CN | EMS 7.0.1+; FortiClient 7.2.2+ | UEM-S `SRG-APP-000378-UEM-000249` | GUI: Security Posture Tags > Security Posture Tagging Rules |
| ZTNA | ZTNA TCP forwarding rules provisioned by EMS, and FQDN-based forwarding services | EMS 7.0.1+; FortiClient 7.0.3+ | VPN `SRG-NET-000343-VPN-001370`; VPN `SRG-NET-000371-VPN-001650` | GUI: Endpoint Profiles > ZTNA Destinations |
| FortiGuard services | FortiGuard Outbreak Alerts service, and tagging of endpoints with specific vulnerabilities | EMS 7.0.1 and later | UEM-S `SRG-APP-000474-UEM-000349`; UEM-S `SRG-APP-000378-UEM-000249` | GUI: FortiGuard Outbreak Alerts |
| EMS logging | Diagnostic tool (EMS debug logs, optional database backup) | EMS 7.0.1 and later | UEM-S `SRG-APP-000226-UEM-000137` | GUI: Administration > Generate Diagnostic Logs |
| Chromebook | FortiClient Cloud Chromebook support | EMS 7.0.1 and later | No direct requirement; if unused, disable (UEM-S `SRG-APP-000141-UEM-000079`) | GUI: System Settings > Feature Select |
| Endpoint protection | Anti-ransomware file backup and restoration, and FDS updates of its behavior rules | FortiClient 7.0.2 and later | No direct requirement; if unused, disable (UEM-S `SRG-APP-000141-UEM-000079`) | GUI: Endpoint Profiles > Malware Protection (Anti-Ransomware) |
| FortiClient logging | Logging to FortiAnalyzer Cloud, its configuration improvements, and the FortiAnalyzer Cloud entitlement for FortiClient Cloud | FortiClient 7.0.3+; FortiClient 7.2.0+; EMS 7.4.3+; FortiClient 7.4.3+ | UEM-A `SRG-APP-000358-UEM-100013`; UEM-S `SRG-APP-000358-UEM-000228` | GUI: Endpoint Profiles > System Settings (Upload Logs to FortiAnalyzer/FortiManager: on) |
| ZTNA | Browser as external user agent for ZTNA user authentication | FortiClient 7.0.3 and later | No direct requirement; if unused, disable (UEM-S `SRG-APP-000141-UEM-000079`) | — |
| Remote access | FortiGate-powered host check for the free VPN client | FortiClient 7.0.3 and later | No direct requirement; if unused, disable (UEM-S `SRG-APP-000141-UEM-000079`) | — |
| Security posture tags | Tag management and visibility; Zero Trust tags renamed security posture tags; security posture tag enhancements | EMS 7.0.3+; FortiClient 7.4.0+; EMS 7.4.3+ | UEM-S `SRG-APP-000378-UEM-000249` | GUI: Security Posture Tags > Tag Monitor |
| Endpoint management | Separate endpoint profiles (Remote Access, ZTNA, Web Filter, and other profile types) | EMS 7.0.3 and later | UEM-S `SRG-APP-000380-UEM-000251` | GUI: Endpoint Profiles > Manage Profiles |
| EMS administration | Certificate provisioning for Active Directory LDAPS connections | EMS 7.0.3 and later | UEM-S `SRG-APP-000191-UEM-000117` | GUI: Administration > Authentication Servers (LDAPS connection: on, Certificate) |
| EMS platform | Redundancy using SQL Server, and Azure SQL managed instance support | EMS 7.0.3+; EMS 7.2.0+ | No direct requirement; if unused, disable (UEM-S `SRG-APP-000141-UEM-000079`) | — |
| User verification | Individual onboarding, authentication server configuration for onboarding, and group assignment by invitation code | EMS 7.0.6+; EMS 7.2.0+ | UEM-S `SRG-APP-000148-UEM-000082`; UEM-A `SRG-APP-000516-UEM-100010` | GUI: System Settings > EMS Settings (Enforce User Verification: Enable, Onboarding Lockout Attempt: 3) |
| Licensing | User-based licensing, FortiFlex support, and removal of legacy license SKUs | EMS 7.0.6+; EMS 7.2.2+; EMS 7.4.0+ | No direct requirement; if unused, disable (UEM-S `SRG-APP-000141-UEM-000079`) | — |
| Forensics | FortiGuard Forensics service (on-premise EMS, macOS reports, on-demand artifact collection) and the forensics agent in FortiClient (Windows) | EMS 7.0.6+; EMS 7.2.2+; FortiClient 7.2.2+; EMS 7.4.1+ | No direct requirement; if unused, disable (UEM-S `SRG-APP-000141-UEM-000079`) | GUI: System Settings > Feature Select |
| ZTNA | ZTNA certificate serial number mismatch handling | FortiClient 7.0.7 and later | VPN `SRG-NET-000343-VPN-001370` | — |
| Remote access | Autoconnect with Microsoft Entra ID (Azure AD) logon: SSL VPN, IPsec VPN, and ZTNA automatic login | FortiClient 7.0.7+; FortiClient 7.2.3+; FortiClient 7.4.3+ | VPN `SRG-NET-000230-VPN-002436` | GUI: Endpoint Profiles > Remote Access |
| ZTNA | Wildcard support for ZTNA FQDN rules | FortiClient 7.2.0 and later | No direct requirement; if unused, disable (UEM-S `SRG-APP-000141-UEM-000079`) | — |
| ZTNA | FortiGate ZTNA service portal support, and GUI for ZTNA portals and SaaS applications in ZTNA Destination profiles | FortiClient 7.2.0+; EMS 7.2.1+ | No direct requirement; if unused, disable (UEM-S `SRG-APP-000141-UEM-000079`) | GUI: Endpoint Profiles > ZTNA Destinations |
| ZTNA | Inline CASB solution for SaaS applications | FortiClient 7.2.0 and later | No direct requirement; if unused, disable (UEM-S `SRG-APP-000141-UEM-000079`) | — |
| FortiPAM | FortiPAM integration: privileged access agent, client executable integrity check, and admin session recording | FortiClient 7.2.0 and later | No direct requirement; if unused, disable (UEM-S `SRG-APP-000141-UEM-000079`) | GUI: Endpoint Profiles > System Settings (Privileged Access Agent: off) |
| Security posture tags | FortiEDR, FortiSIEM, and Fabric connector tags for security posture checks | FortiClient 7.2.0+; EMS 7.2.5+ | UEM-S `SRG-APP-000378-UEM-000249` | GUI: Security Posture Tags > Security Posture Tagging Rules |
| Remote access | Closest gateway selection for VPN, and closest PoP for IPsec VPN using GeoDNS | FortiClient 7.2.0+; FortiClient 8.0.0+ | No direct requirement; if unused, disable (UEM-S `SRG-APP-000141-UEM-000079`) | — |
| Remote access | VPN autoconnect and always up logic improvement | FortiClient 7.2.0 and later | VPN `SRG-NET-000230-VPN-002436` | GUI: Endpoint Profiles > Remote Access |
| Remote access | Load-balanced SSL VPN and IPsec VPN gateways with one FQDN | FortiClient 7.2.0+; FortiClient 7.4.3+ | No direct requirement; if unused, disable (UEM-S `SRG-APP-000141-UEM-000079`) | — |
| EMS platform | Improved certificate UX | EMS 7.2.0 and later | UEM-S `SRG-APP-000427-UEM-000298` | GUI: System Settings > EMS Server Certificates |
| Security posture tags | ZTNA AD group lookup rule improvement, and DWORD and string values in registry key tagging rules | EMS 7.2.0 and later | UEM-S `SRG-APP-000378-UEM-000249` | GUI: Security Posture Tags > Security Posture Tagging Rules |
| EMS administration | AD connector (proxy between EMS and the AD server) | EMS 7.2.0 and later | UEM-S `SRG-APP-000191-UEM-000117` | GUI: Administration > Authentication Servers (Use Connector) |
| Endpoint management | Initial FortiClient deployment changes | EMS 7.2.0 and later | UEM-S `SRG-APP-000378-UEM-000248` | GUI: Deployment & Installers > Manage Deployment |
| Web Filter | Web Filter and Video Filter changes: Linux support, Video Filter profile, ISDB queries, scheduling, remote categories, Referrer Host, search keyword scanning | FortiClient 7.2.1+; EMS 7.4.3+; FortiClient 7.4.3+; EMS 8.0.0+ | No direct requirement; if unused, disable (UEM-S `SRG-APP-000141-UEM-000079`) | GUI: Endpoint Profiles > Web Filter |
| Endpoint management | FortiClient agent upgrade improvements and transparent FortiClient upgrade | FortiClient 7.2.1+; FortiClient 7.4.0+ | UEM-S `SRG-APP-000456-UEM-000330`; UEM-S `SRG-APP-000378-UEM-000248` | GUI: Deployment & Installers > Manage Deployment |
| SSOMA | SSOMA improvements and FSSOMA connectivity status | FortiClient 7.2.1+; FortiClient 7.4.4+ | No direct requirement; if unused, disable (UEM-S `SRG-APP-000141-UEM-000079`) | GUI: Endpoint Profiles > System Settings (FortiClient Single Sign-On Mobility Agent: off) |
| Remote access | Network lockdown for off-fabric endpoints (SSL VPN, then IPsec VPN with hotel mode) | FortiClient 7.2.1 and later | VPN `SRG-NET-000230-VPN-002436`; VPN `SRG-NET-000019-VPN-000040` | GUI: Endpoint Profiles > Remote Access (Network Lockdown: on) |
| Remote access | IPsec VPN connection only when FortiClient is connected to EMS, with the EMS serial number in FortiOS logs | FortiClient 7.2.1 and later | VPN `SRG-NET-000343-VPN-001370`; VPN `SRG-NET-000148-VPN-000540` | — (enable vpn-ems-sn-check on the FortiGate) |
| Remote access | Certificate path configuration for automated certificate selection | FortiClient 7.2.1 and later | VPN `SRG-NET-000166-VPN-000590` | GUI: Endpoint Profiles > Remote Access |
| Fabric connectors | FortiGate per-VDOM connection, Fabric Devices enhancements, and token (OAuth 2.0) authentication of Fabric connectors | EMS 7.2.1+; EMS 7.4.1+ | UEM-S `SRG-APP-000191-UEM-000117`; UEM-S `SRG-APP-000580-UEM-000398` | GUI: Fabric & Connectors > Fabric Devices |
| EMS administration | Entra ID integration (Entra ID authentication server) | EMS 7.2.1 and later | UEM-S `SRG-APP-000023-UEM-000012` | GUI: Administration > Authentication Servers |
| Endpoint management | Send endpoints a one-way message | EMS 7.2.1 and later | No direct requirement; if unused, disable (UEM-S `SRG-APP-000141-UEM-000079`) | — |
| MDM | MDM integration for mobile ZTNA certificates: Jamf, Intune, Workspace ONE, ManageEngine, with EMS HA and multitenancy | EMS 7.2.1+; EMS 7.4.0+ | No direct requirement; if unused, disable (UEM-S `SRG-APP-000141-UEM-000079`) | GUI: System Settings > MDM Integration |
| Endpoint management | FortiClient and EMS persistent connection | EMS 7.2.1 and later | UEM-S `SRG-APP-000191-UEM-000119` | GUI: System Settings > EMS Settings (Use Persistent Connections) |
| Endpoint management | Administrator can uninstall FortiClient without the disconnect password | EMS 7.2.1 and later | UEM-A `SRG-APP-000516-UEM-100011` | GUI: Endpoint Profiles > System Settings (Allow endpoint admin to disconnect without a password: off) |
| EMS administration | SAML SSO enhancements for administrator logon | EMS 7.2.1 and later | UEM-S `SRG-APP-000149-UEM-000083` | GUI: Administration > SAML SSO |
| Remote access | Encryption recommended by the NCSC: AES-GCM and PRF algorithms for IPsec VPN proposals | FortiClient 7.2.2 and later | VPN `SRG-NET-000525-VPN-002330`; VPN `SRG-NET-000230-VPN-000780`; VPN `SRG-NET-000510-VPN-002170` | GUI: Endpoint Profiles > Remote Access (Encryption, Authentication) |
| Remote access | SSL VPN DTLS and split DNS on macOS and Linux, split DNS for IPsec VPN, and DNS resilience with the Windows NRPT | FortiClient 7.2.2+; FortiClient 7.4.8+; FortiClient 8.0.0+ | No direct requirement; if unused, disable (UEM-S `SRG-APP-000141-UEM-000079`) | — |
| Endpoint protection | PUA detection, and vulnerability scan on new software or PUA detection | EMS 7.2.2+; EMS 7.4.5+ | UEM-S `SRG-APP-000472-UEM-000347` | GUI: Dashboard > Vulnerability Scan |
| Endpoint management | Export endpoint information | EMS 7.2.2 and later | No direct requirement; if unused, disable (UEM-S `SRG-APP-000141-UEM-000079`) | — |
| EMS administration | Password recovery for EMS administrators (PasswordRecovery tool) | EMS 7.2.2 and later | UEM-S `SRG-APP-000151-UEM-000085` | — (restrict root access to the EMS host) |
| EMS logging | Fortinet email server for sending alerts | EMS 7.2.2 and later | No direct requirement; if unused, disable (UEM-S `SRG-APP-000141-UEM-000079`) | GUI: System Settings > SMTP Server |
| Endpoint protection | Exceptions for the Firewall Detect & Block Exploits feature | EMS 7.2.2 and later | No direct requirement; if unused, disable (UEM-S `SRG-APP-000141-UEM-000079`) | GUI: Endpoint Profiles > Firewall |
| Remote access | Secure remote access compliance enforcement: allow or deny VPN by security posture tag | FortiClient 7.2.3+; FortiClient 7.4.3+ | UEM-S `SRG-APP-000378-UEM-000249`; VPN `SRG-NET-000343-VPN-001370` | XML: `vpn/options/secure_remote_access=1` |
| Remote access | IKEv2 for FortiClient (macOS), IKEv2 on multiple protocols, and LDAP for IPsec IKEv2 VPN | FortiClient 7.2.3+; FortiClient 7.4.1+ | VPN `SRG-NET-000132-VPN-000460` | XML: `vpn/ipsecvpn/connections/connection/ike_settings/version=2` |
| Remote access | IPsec VPN and ZTNA prioritized over SSL VPN; SSL VPN option hidden in EMS by default | FortiClient 7.2.3+; EMS 7.4.6+ | VPN `SRG-NET-000132-VPN-000450` | `emscli feature get --name <FEATURE>` (keep the sslvpn feature disabled) |
| Endpoint management | Managing 3000 profiles and policies | EMS 7.2.3 and later | No direct requirement; if unused, disable (UEM-S `SRG-APP-000141-UEM-000079`) | — |
| Remote access | IPsec VPN through FortiADC | FortiClient 7.2.4 and later | No direct requirement; if unused, disable (UEM-S `SRG-APP-000141-UEM-000079`) | — |
| Remote access | Source IP address anchoring for IPsec VPN (public IP in on-fabric detection rules) | FortiClient 7.2.4 and later | VPN `SRG-NET-000019-VPN-002435` | GUI: Endpoint Policy & Components > On-fabric Detection Rules |
| EMS logging | Sending EMS system log messages to FortiAnalyzer | EMS 7.2.4 and later | UEM-S `SRG-APP-000358-UEM-000228`; UEM-S `SRG-APP-000515-UEM-000390`; UEM-S `SRG-APP-000125-UEM-000074` | GUI: System Settings > Logs (Send system log messages externally: FortiAnalyzer) |
| Remote access | IPsec VPN with FortiToken Mobile push MFA | FortiClient 7.2.5 and later | VPN `SRG-NET-000140-VPN-000500`; VPN `SRG-NET-000145-VPN-000510` | — (configured on the FortiGate) |
| Remote access | SAML authentication for VPN before logon | FortiClient 7.2.5 and later | VPN `SRG-NET-000230-VPN-002436`; VPN `SRG-NET-000140-VPN-000500` | GUI: Endpoint Profiles > Remote Access (Show VPN before Logon: on) |
| ZTNA | ZTNA application catalog, and auto-detected FortiGate non-web ZTNA applications | EMS 7.2.5+; EMS 7.4.1+ | No direct requirement; if unused, disable (UEM-S `SRG-APP-000141-UEM-000079`) | GUI: Fabric & Connectors > ZTNA Applications Catalog |
| EMS platform | Post-installation setup wizard | EMS 7.2.5+; EMS 7.4.3+ | No direct requirement; if unused, disable (UEM-S `SRG-APP-000141-UEM-000079`) | — |
| EMS platform | Automatic upgrade of EMS to the latest patch release | EMS 7.2.5+; EMS 7.4.1+ | UEM-S `SRG-APP-000456-UEM-000330`; UEM-S `SRG-APP-000380-UEM-000251` | GUI: System Settings > EMS Settings (Let EMS schedule automatic upgrade); `emscli config set autoupgrade --enable false` (when upgrades must go through change control) |
| Endpoint management | On-fabric detection based on destination address | EMS 7.2.5+; EMS 7.4.1+ | No direct requirement; if unused, disable (UEM-S `SRG-APP-000141-UEM-000079`) | GUI: Endpoint Policy & Components > On-fabric Detection Rules |
| ZTNA | JWT support for ZTNA UID and tag sharing | FortiClient 7.4.0 and later | No direct requirement; if unused, disable (UEM-S `SRG-APP-000141-UEM-000079`) | GUI: System Settings > EMS Settings (Enable ZTNA Token: off) |
| Endpoint management | FortiClient (Linux) and ARM installer creation, and uploading a custom FortiClient installer | EMS 7.4.0 and later | UEM-S `SRG-APP-000378-UEM-000248`; UEM-S `SRG-APP-000131-UEM-000076` | GUI: Deployment & Installers > FortiClient Installer |
| EMS platform | Linux-based EMS model, with RHEL 9 and CentOS 9 support | EMS 7.4.0 and later | UEM-S `SRG-APP-000516-UEM-000391` | Assess the Linux host against its operating system STIG |
| Fabric connectors | Access key for Security Fabric devices connecting to FortiClient Cloud | EMS 7.4.0 and later | No direct requirement; if unused, disable (UEM-S `SRG-APP-000141-UEM-000079`) | — |
| Security posture tags | Security posture rules based on the CrowdStrike ZTA score | FortiClient 7.4.1 and later | UEM-S `SRG-APP-000378-UEM-000249` | GUI: Security Posture Tags > Security Posture Tagging Rules |
| FortiClient GUI | FortiTray icons for on-fabric and VPN status, FortiClient GUI enhancement, and FortiClient GUI update | EMS 7.4.1+; FortiClient 7.4.1+; FortiClient 8.0.0+ | No direct requirement; if unused, disable (UEM-S `SRG-APP-000141-UEM-000079`) | — |
| FortiClient logging | Sending email events from the Microsoft Exchange server | FortiClient 7.4.1 and later | No direct requirement; if unused, disable (UEM-S `SRG-APP-000141-UEM-000079`) | GUI: Endpoint Profiles > System Settings |
| ZTNA | ZTNA destinations over UDP | FortiClient 7.4.1 and later | No direct requirement; if unused, disable (UEM-S `SRG-APP-000141-UEM-000079`) | — |
| Remote access | IPsec VPN over TCP on Windows, macOS, and Linux | FortiClient 7.4.1 and later | No direct requirement; if unused, disable (UEM-S `SRG-APP-000141-UEM-000079`) | — |
| Remote access | IKEv2 session resumption | FortiClient 7.4.1 and later | No direct requirement; if unused, disable (UEM-S `SRG-APP-000141-UEM-000079`) | GUI: Endpoint Profiles > Remote Access (Enable Session Resumption: off) |
| Endpoint management | FortiClient hotfix deployment via EMS | EMS 7.4.1 and later | UEM-S `SRG-APP-000456-UEM-000330` | GUI: Deployment & Installers > FortiClient Installer |
| EMS platform | EMS as a VM image (KVM, VMware, then Hyper-V and VirtualBox) | EMS 7.4.1 and later | UEM-S `SRG-APP-000516-UEM-000391` | Assess the VM host as a Linux server |
| EMS administration | Assign AD and local Windows server groups to admin roles | EMS 7.4.1 and later | UEM-S `SRG-APP-000023-UEM-000012`; UEM-S `SRG-APP-000380-UEM-000251` | GUI: Administration > Admin Users |
| Endpoint protection | FortiEndpoint (FortiClient integration of the FortiEDR agent) | EMS 7.4.1 and later | No direct requirement; if unused, disable (UEM-S `SRG-APP-000141-UEM-000079`) | GUI: System Settings > Feature Select |
| Remote access | EAP-TTLS for IPsec VPN (LDAP user authentication over a TLS tunnel) | FortiClient 7.4.3 and later | VPN `SRG-NET-000166-VPN-000580` | GUI: Endpoint Profiles > Remote Access (EAP Authentication Method: EAP-TTLS) |
| ZTNA | Upload a custom certificate and private key for ZTNA | EMS 7.4.3 and later | UEM-S `SRG-APP-000427-UEM-000298` | GUI: System Settings > EMS Settings (EMS CA Certificate (ZTNA)) |
| EMS logging | Consolidated endpoint events, with EMS installed with a separate time series Elasticsearch database | EMS 7.4.3 and later | UEM-A `SRG-APP-000358-UEM-100013`; UEM-S `SRG-APP-000516-UEM-000392` | GUI: Endpoints > All Events |
| Endpoint protection | Vulnerability detection popup on endpoints | EMS 7.4.3 and later | No direct requirement; if unused, disable (UEM-S `SRG-APP-000141-UEM-000079`) | — |
| Licensing | Behavior of EMS with an expired license (endpoints no longer deregistered) | EMS 7.4.3 and later | No direct requirement; if unused, disable (UEM-S `SRG-APP-000141-UEM-000079`) | — |
| Endpoint protection | FortiDeceptor integration (deception tokens and lures) | FortiClient 7.4.4 and later | No direct requirement; if unused, disable (UEM-S `SRG-APP-000141-UEM-000079`) | GUI: Endpoint Profiles > FortiDeceptor Campaign |
| Endpoint protection | FortiData integration (data protection) | FortiClient 7.4.4 and later | No direct requirement; if unused, disable (UEM-S `SRG-APP-000141-UEM-000079`) | GUI: Endpoint Profiles > Data Protection |
| Remote access | Dual IPsec VPN tunnel support | FortiClient 7.4.4 and later | No direct requirement; if unused, disable (UEM-S `SRG-APP-000141-UEM-000079`) | — |
| EMS administration | RADIUS server authentication for administrators | EMS 7.4.4 and later | UEM-S `SRG-APP-000148-UEM-000082`; UEM-S `SRG-APP-000023-UEM-000012` | GUI: Administration > RADIUS (Authentication Method) |
| EMS platform | EMS VM CLI and EMS CLI (emscli) enhancements | EMS 7.4.4 and later | UEM-S `SRG-APP-000380-UEM-000251` | `emscli system get info` |
| Endpoint management | Endpoint health check (feature status of each endpoint) | EMS 7.4.4 and later | UEM-S `SRG-APP-000472-UEM-000347`; UEM-S `SRG-APP-000474-UEM-000349` | GUI: Endpoints > All Endpoints |
| EMS platform | EMS upgrade notification improvement | EMS 7.4.4 and later | UEM-S `SRG-APP-000456-UEM-000330` | GUI: System Settings > EMS Alerts (New EMS version is available for deployment) |
| User verification | Custom invitation email template for on-premise EMS | EMS 7.4.4 and later | No direct requirement; if unused, disable (UEM-S `SRG-APP-000141-UEM-000079`) | GUI: System Settings > Invitation Email Template |
| EMS platform | Upgrade and compatibility matrix signature, and firmware maturity levels (Feature and Mature tags) | EMS 7.4.4+; FortiClient and EMS 7.4.4+ | UEM-S `SRG-APP-001035-UEM-000408` | GUI: Dashboard > Status (System Information) |
| Remote access | Windows Hello for Business with FortiGate SAML-based IPsec VPN | FortiClient 7.4.5 and later | VPN `SRG-NET-000140-VPN-000500`; VPN `SRG-NET-000145-VPN-000510` | GUI: Endpoint Profiles > Remote Access |
| EMS platform | Deploying EMS with Docker Compose or on Kubernetes | EMS 7.4.5 and later | UEM-S `SRG-APP-000516-UEM-000391`; UEM-S `SRG-APP-000514-UEM-000389` | Set EMS_FIPS_ENABLED (Docker Compose) or fips (Kubernetes) to true |
| EMS platform | EMS Performance dashboard | EMS 7.4.5 and later | UEM-S `SRG-APP-000474-UEM-000349` | GUI: Dashboard > Performance |
| EMS platform | EMS scheduled backup to a remote server | EMS 7.4.5 and later | UEM-S `SRG-APP-000125-UEM-000074` | GUI: System Settings > EMS Settings (Scheduled Backup, Backup Server) |
| Security posture tags | Tag evaluation visibility, and improved ZTNA and VPN troubleshooting | EMS 7.4.5 and later | No direct requirement; if unused, disable (UEM-S `SRG-APP-000141-UEM-000079`) | — |
| EMS platform | Adding and expanding disks on EMS VMs | EMS 7.4.5 and later | No direct requirement; if unused, disable (UEM-S `SRG-APP-000141-UEM-000079`) | — |
| EMS platform | EMS VM HA clusters created with the EMSCLI, with witness nodes | EMS 7.4.5 and later | UEM-S `SRG-APP-000225-UEM-000136` | `emscli ha get status` |
| EMS platform | EMS VM password recovery ISO | EMS 7.4.5 and later | No direct requirement; if unused, disable (UEM-S `SRG-APP-000141-UEM-000079`) | — |
| EMS platform | Open source licensing requirements page | EMS 7.4.5 and later | No direct requirement; if unused, disable (UEM-S `SRG-APP-000141-UEM-000079`) | — |
| EMS platform | EMS in air-gapped environments (dependencies bundle or HTTP proxy) | EMS 7.4.6 and later | No direct requirement; if unused, disable (UEM-S `SRG-APP-000141-UEM-000079`) | — |
| EMS platform | PostgreSQL database: auto-adjusted configuration, versions 15 to 18, standalone remote DB on RHEL, DB node timeout | EMS 7.4.6+; EMS 8.0.0+ | No direct requirement; if unused, disable (UEM-S `SRG-APP-000141-UEM-000079`) | — |
| Remote access | EMS GUI changes from 7.4.6 (auto start, traffic keep strategy, session resumption, mode config types) | EMS 7.4.6 and later | No direct requirement; if unused, disable (UEM-S `SRG-APP-000141-UEM-000079`) | — |
| Remote access | IPsec VPN failover with priority groups | FortiClient 7.4.8 and later | No direct requirement; if unused, disable (UEM-S `SRG-APP-000141-UEM-000079`) | — |
| EMS platform | Setting EMS network routes | EMS 7.4.8+; EMS 8.0.0+ | No direct requirement; if unused, disable (UEM-S `SRG-APP-000141-UEM-000079`) | — |
| Endpoint management | New OS support for Windows and Linux endpoints | FortiClient 8.0.0 and later | No direct requirement; if unused, disable (UEM-S `SRG-APP-000141-UEM-000079`) | — |
| Remote access | Excluding ZTNA application traffic from the IKEv2 VPN tunnel | FortiClient 8.0.0 and later | VPN `SRG-NET-000369-VPN-001620` | XML: `vpn/options/exclude_ztna_apps=0` |
| Remote access | Post-quantum preshared key (PPK) for IPsec VPN | FortiClient 8.0.0 and later | VPN `SRG-NET-000371-VPN-001650` | XML: `vpn/ipsecvpn/connections/connection/ike_settings/ppk_mode=<PPK_MODE>` |
| EMS administration | FortiAI assistant for EMS administrators (cloud service) | EMS 8.0.0 and later | No direct requirement; if unused, disable (UEM-S `SRG-APP-000141-UEM-000079`) | `emscli config set ai --enable.feature false` |
| Security posture tags | Endpoint posture risk and visibility scores | EMS 8.0.0 and later | UEM-S `SRG-APP-000378-UEM-000249` | GUI: Dashboard > Endpoint Posture Score |
| EMS platform | New EMS version installed side by side with production EMS | EMS 8.0.0 and later | No direct requirement; if unused, disable (UEM-S `SRG-APP-000141-UEM-000079`) | — |
| EMS administration | SCIM connection between EMS and the SAML identity provider | EMS 8.0.0 and later | UEM-S `SRG-APP-000023-UEM-000012` | GUI: Administration > Authentication Servers |
| Endpoint protection | Granular process-level access control on endpoints | EMS 8.0.0 and later | No direct requirement; if unused, disable (UEM-S `SRG-APP-000141-UEM-000079`) | GUI: Endpoint Profiles > System Settings |
| Remote access | Improvements to creating and editing remote access profiles | EMS 8.0.0 and later | No direct requirement; if unused, disable (UEM-S `SRG-APP-000141-UEM-000079`) | GUI: Endpoint Profiles > Remote Access |
| EMS platform | Anonymous statistics sent to Fortinet | EMS 8.0.0 and later | No direct requirement; if unused, disable (UEM-S `SRG-APP-000141-UEM-000079`) | GUI: System Settings > EMS Settings (Statistics Collection: off); `emscli config set stats --enabled false` |

### Requirement reference

The requirements used in the map and in this chapter's text, with their
severity in the current releases:

[Download the requirement reference as CSV](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/data/volume-172-disa-srgs-and-stigs/27-forticlient-and-ems-feature-version-and-srg-map-requirements.csv) (124 rows).

| SRG | Requirement | Severity | Requirement title |
| --- | --- | --- | --- |
| UEM-S | `SRG-APP-000003-UEM-000003` | CAT II | The UEM server must initiate a session lock after a 15-minute period of inactivity. |
| UEM-S | `SRG-APP-000014-UEM-000009` | CAT II | The UEM server must use TLS 1.2, or higher, to protect the confidentiality of sensitive data during electronic dissemination using remote access. |
| UEM-S | `SRG-APP-000023-UEM-000012` | CAT II | The UEM server must provide automated mechanisms for supporting account management functions. |
| UEM-S | `SRG-APP-000025-UEM-000014` | CAT II | The UEM server must automatically disable accounts after a 35-day period of account inactivity. |
| UEM-S | `SRG-APP-000026-UEM-000015` | CAT II | The UEM server must automatically audit account creation. |
| UEM-S | `SRG-APP-000027-UEM-000016` | CAT II | The UEM server must automatically audit account modification. |
| UEM-S | `SRG-APP-000065-UEM-000036` | CAT II | The UEM server must enforce the limit of three consecutive invalid logon attempts by a user during a 15-minute time period. |
| UEM-S | `SRG-APP-000068-UEM-000037` | CAT II | The UEM server must display the Standard Mandatory DoW Notice and Consent Banner before granting access to the application. |
| UEM-S | `SRG-APP-000069-UEM-000038` | CAT III | The UEM server must retain the access banner until the user acknowledges acceptance of the access conditions. |
| UEM-S | `SRG-APP-000089-UEM-000049` | CAT II | The UEM server must provide audit record generation capability for DoW-defined auditable events within all application components. |
| UEM-S | `SRG-APP-000089-UEM-000050` | CAT II | The UEM server must be configured to provide audit records in a manner suitable for the authorized administrators to interpret the information. |
| UEM-S | `SRG-APP-000090-UEM-000051` | CAT II | The UEM server must be configured to allow only specific administrator roles to select which auditable events are to be audited. |
| UEM-S | `SRG-APP-000108-UEM-000062` | CAT II | The UEM SRG must alert the information system security officer (ISSO) and system administrator (SA) (at a minimum) in the event of an audit processing failure. |
| UEM-S | `SRG-APP-000116-UEM-000067` | CAT II | The UEM server must use host operating system clocks to generate time stamps for audit records. |
| UEM-S | `SRG-APP-000118-UEM-000068` | CAT II | The UEM server must protect audit information from any type of unauthorized read access. |
| UEM-S | `SRG-APP-000120-UEM-000070` | CAT II | The UEM server must protect audit information from unauthorized deletion. |
| UEM-S | `SRG-APP-000125-UEM-000074` | CAT II | The UEM server must back up audit records at least every seven days onto a log management server. |
| UEM-S | `SRG-APP-000131-UEM-000076` | CAT II | The UEM server must prevent the installation of patches, service packs, or application components without verification the software component has been digitally signed using a certificate that is recognized and approved by the organization. |
| UEM-S | `SRG-APP-000133-UEM-000078` | CAT II | The UEM server must limit privileges to change the software resident within software libraries. |
| UEM-S | `SRG-APP-000141-UEM-000079` | CAT II | The UEM server must be configured to disable nonessential capabilities. |
| UEM-S | `SRG-APP-000142-UEM-000080` | CAT II | The firewall protecting the UEM server platform must be configured so only DoW-approved ports, protocols, and services are enabled. (Refer to the DoW Ports, Protocols, Services Management [PPSM] Category Assurance Levels [CAL] list for DoW-approved ports, protocols, and services). |
| UEM-S | `SRG-APP-000148-UEM-000082` | CAT II | The UEM server must uniquely identify and authenticate organizational users (or processes acting on behalf of organizational users). |
| UEM-S | `SRG-APP-000149-UEM-000083` | CAT II | The UEM server must be configured to use a DoW Central Directory Service to provide multifactor authentication for network access to privileged and nonprivileged accounts. |
| UEM-S | `SRG-APP-000151-UEM-000085` | CAT II | All UEM server local accounts created during application installation and configuration must be removed. Note: In this context local accounts refers to user and or administrator accounts on the server that use user name and password for user access and authentication. |
| UEM-S | `SRG-APP-000154-UEM-000088` | CAT II | The UEM server must be configured to use DoW PKI for multifactor authentication. This requirement is included in SRG-APP-000149. |
| UEM-S | `SRG-APP-000164-UEM-000094` | CAT II | The UEM server must enforce a minimum 15-character password length. |
| UEM-S | `SRG-APP-000165-UEM-000095` | CAT II | The UEM server must prohibit password reuse for a minimum of five generations. |
| UEM-S | `SRG-APP-000166-UEM-000096` | CAT II | The UEM server must enforce password complexity by requiring that at least one uppercase character be used. |
| UEM-S | `SRG-APP-000170-UEM-000100` | CAT II | UEM server must require the change of at least 50 percent of the previous password's characters. |
| UEM-S | `SRG-APP-000171-UEM-000101` | CAT II | For UEM server using password authentication, the application must store only cryptographic representations of passwords. |
| UEM-S | `SRG-APP-000174-UEM-000104` | CAT II | The UEM server must enforce a 180-day maximum password lifetime restriction. |
| UEM-S | `SRG-APP-000177-UEM-000108` | CAT II | The UEM server must map the authenticated identity to the individual user or group account for PKI-based authentication. |
| UEM-S | `SRG-APP-000179-UEM-000110` | CAT I | The UEM server must use FIPS-validated SHA-2 or higher hash function to protect the integrity of keyed-hash message authentication code (HMAC), Key Derivation Functions (KDFs), Random Bit Generation, and hash-only applications. |
| UEM-S | `SRG-APP-000191-UEM-000117` | CAT II | The UEM server must be configured to provide a trusted communication channel between itself and authorized IT entities using [selection: -IPsec, -SSH, -mutually authenticated TLS, -mutually authenticated DTLS, -HTTPS]. |
| UEM-S | `SRG-APP-000191-UEM-000118` | CAT II | The UEM server must be configured to invoke either host-OS functionality or server functionality to provide a trusted communication channel between itself and remote administrators that provides assured identification of its endpoints and protection of the communicated data from modification and disclosure using [selection: -IPsec, -SSH, -TLS, -HTTPS]. |
| UEM-S | `SRG-APP-000191-UEM-000119` | CAT II | The UEM server must be configured to invoke either host-OS functionality or server functionality to provide a trusted communication channel between itself and managed devices that provides assured identification of its endpoints and protection of the communicated data from modification and disclosure using [selection: -TLS, -HTTPS]. |
| UEM-S | `SRG-APP-000225-UEM-000136` | CAT II | The UEM server must fail to a secure state if system initialization fails, shutdown fails, or aborts fail. |
| UEM-S | `SRG-APP-000226-UEM-000137` | CAT II | In the event of a system failure, the UEM server must preserve any information necessary to determine cause of failure and any information necessary to return to operations with least disruption to mission processes. |
| UEM-S | `SRG-APP-000291-UEM-000165` | CAT II | The UEM server must notify system administrators (SAs) and the information system security officer (ISSO) when accounts are created. |
| UEM-S | `SRG-APP-000295-UEM-000169` | CAT II | The UEM server must automatically terminate a user session after an organization-defined period of user inactivity. |
| UEM-S | `SRG-APP-000329-UEM-000202` | CAT II | The UEM server must be configured to have at least one user in defined administrator roles. |
| UEM-S | `SRG-APP-000343-UEM-000216` | CAT II | The UEM server must audit the execution of privileged functions. |
| UEM-S | `SRG-APP-000345-UEM-000218` | CAT II | The UEM server must automatically lock the account until the locked account is released by an administrator when three unsuccessful login attempts in 15 minutes are exceeded. |
| UEM-S | `SRG-APP-000358-UEM-000228` | CAT II | The UEM server must be configured to transfer UEM server logs to another server for storage, analysis, and reporting. Note: UEM server logs include logs of UEM events and logs transferred to the UEM server by UEM agents of managed devices. |
| UEM-S | `SRG-APP-000374-UEM-000244` | CAT II | The UEM server must be configured to record time stamps for audit records that can be mapped to Coordinated Universal Time (UTC) or Greenwich Mean Time (GMT). |
| UEM-S | `SRG-APP-000378-UEM-000248` | CAT II | The UEM server must prohibit user installation of software by an administrator without the appropriate assigned permission for software installation. |
| UEM-S | `SRG-APP-000378-UEM-000249` | CAT II | The UEM server must be configured to only allow enrolled devices that are compliant with UEM policies and assigned to a user in the application access group to download applications. |
| UEM-S | `SRG-APP-000380-UEM-000251` | CAT II | The UEM server must enforce access restrictions associated with changes to the server configuration. |
| UEM-S | `SRG-APP-000383-UEM-000254` | CAT II | The UEM server must disable organization-defined functions, ports, protocols, and services (within the application) deemed unnecessary and/or nonsecure. |
| UEM-S | `SRG-APP-000395-UEM-000266` | CAT I | Before establishing a connection to any endpoint device being managed, the UEM server must establish a trusted path between the server and endpoint that provides assured identification of the end point using a bidirectional authentication mechanism configured with a FIPS-validated Advanced Encryption Standard (AES) cipher block algorithm to authenticate with the device. |
| UEM-S | `SRG-APP-000412-UEM-000283` | CAT I | The UEM server must configure web management tools with FIPS-validated Advanced Encryption Standard (AES) cipher block algorithm to protect the confidentiality of maintenance and diagnostic communications for nonlocal maintenance sessions. |
| UEM-S | `SRG-APP-000427-UEM-000298` | CAT II | The UEM server must only allow the use of DoW PKI established certificate authorities for verification of the establishment of protected sessions. |
| UEM-S | `SRG-APP-000427-UEM-000299` | CAT II | The UEM server must be configured to use X.509v3 certificates for code signing for system software updates. |
| UEM-S | `SRG-APP-000427-UEM-000300` | CAT II | The UEM server must be configured to use X.509v3 certificates for code signing for integrity verification. |
| UEM-S | `SRG-APP-000427-UEM-000500` | CAT I | The UEM server must provide digitally signed policies and policy updates to the UEM agent. |
| UEM-S | `SRG-APP-000427-UEM-000501` | CAT I | The UEM server must sign policies and policy updates using a private key associated with [selection: an X509 certificate, a public key provisioned to the agent trusted by the agent] for policy verification. |
| UEM-S | `SRG-APP-000427-UEM-000502` | CAT I | The UEM server, for each unique policy managed, must validate the policy is appropriate for an agent using [selection: a private key associated with an X509 certificate representing the agent, a token issued by the agent] associated with a policy signing key uniquely associated with the policy. |
| UEM-S | `SRG-APP-000439-UEM-000313` | CAT I | The UEM server must connect to [assignment: [list of applications]] and managed mobile devices with an authenticated and secure (encrypted) connection to protect the confidentiality and integrity of transmitted information. |
| UEM-S | `SRG-APP-000456-UEM-000330` | CAT I | The UEM server must install security-relevant software updates within 30 days unless the time period is directed by an authoritative source (e.g., IAVM, CTOs, DTMs, STIGs). |
| UEM-S | `SRG-APP-000472-UEM-000347` | CAT II | The UEM server must be configured with the periodicity of the following commands to the agent of six hours or less: - query connectivity status; - query the current version of the managed device firmware/software; - query the current version of installed mobile applications; - read audit logs kept by the managed device. |
| UEM-S | `SRG-APP-000474-UEM-000349` | CAT II | The UEM server must alert the system administrator (SA) when anomalies in the operation of security functions are discovered. |
| UEM-S | `SRG-APP-000479-UEM-000354` | CAT II | The UEM server must be configured to verify software updates to the server using a digital signature mechanism prior to installing those updates. |
| UEM-S | `SRG-APP-000503-UEM-000378` | CAT II | The UEM server must generate audit records when successful/unsuccessful logon attempts occur. |
| UEM-S | `SRG-APP-000514-UEM-000389` | CAT I | The UEM server must use a FIPS-validated cryptographic module to generate cryptographic hashes. |
| UEM-S | `SRG-APP-000515-UEM-000390` | CAT II | The UEM server must, at a minimum, off-load audit logs of interconnected systems in real time and off-load standalone systems weekly. |
| UEM-S | `SRG-APP-000516-UEM-000391` | CAT II | The UEM server must be configured in accordance with the security configuration settings based on DoW security configuration or implementation guidance, including STIGs, NSA configuration guides, CTOs, and DTMs. |
| UEM-S | `SRG-APP-000516-UEM-000392` | CAT II | The UEM server must be configured to allow authorized administrators to read all audit data from audit records on the server. |
| UEM-S | `SRG-APP-000555-UEM-000393` | CAT I | The UEM server must be configured to implement FIPS 140-3 mode for all server and agent encryption. |
| UEM-S | `SRG-APP-000580-UEM-000398` | CAT II | The UEM server must authenticate endpoint devices (servers) before establishing a local, remote, and/or network connection using bidirectional authentication that is cryptographically based. |
| UEM-S | `SRG-APP-000605-UEM-000401` | CAT II | The UEM server must validate certificates used for Transport Layer Security (TLS) functions by performing RFC 5280-compliant certification path validation. |
| UEM-S | `SRG-APP-001035-UEM-000408` | CAT I | The UEM server must be a version supported by the vendor. |
| UEM-A | `SRG-APP-000089-UEM-100002` | CAT II | The UEM Agent must provide an alert via the trusted channel to the UEM Server in the event of any of the following audit events: -successful application of policies to a mobile device -receiving or generating periodic reachability events -change in enrollment state -failure to install an application from the UEM Server -failure to update an application from the UEM Server. |
| UEM-A | `SRG-APP-000089-UEM-100004` | CAT II | The UEM Agent must generate a UEM Agent audit record of the following auditable events:-startup and shutdown of the UEM Agent-UEM policy updated-any modification commanded by the UEM Server. |
| UEM-A | `SRG-APP-000089-UEM-100012` | CAT II | The UEM Agent must be configured to enable the following function: read audit logs of the managed endpoint device. |
| UEM-A | `SRG-APP-000097-UEM-100005` | CAT II | The UEM Agent must record within each UEM Agent audit record the following information: -date and time of the event -type of event -subject identity -(if relevant) the outcome (success or failure) of the event. |
| UEM-A | `SRG-APP-000175-UEM-100008` | CAT II | The UEM Agent must not install policies if the policy-signing certificate is deemed invalid. |
| UEM-A | `SRG-APP-000176-UEM-100001` | CAT II | The UEM Agent must use managed endpoint device key storage for all persistent secret and private keys. |
| UEM-A | `SRG-APP-000358-UEM-100003` | CAT II | The UEM Agent must queue alerts if the trusted channel is not available. |
| UEM-A | `SRG-APP-000358-UEM-100013` | CAT II | The UEM Agent must be configured to enable the following function: transfer managed endpoint device audit logs read by the UEM Agent to an UEM server or third-party audit management server. |
| UEM-A | `SRG-APP-000427-UEM-100007` | CAT II | The UEM Agent must only accept policies and policy updates that are digitally signed by a certificate that has been authorized for policy updates by the UEM Server. |
| UEM-A | `SRG-APP-000427-UEM-100009` | CAT II | The UEM Agent must perform the following functions: Import the certificates to be used for authentication of UEM Agent communications. |
| UEM-A | `SRG-APP-000516-UEM-100006` | CAT II | The UEM Agent must record the reference identifier of the UEM Server during the enrollment process. |
| UEM-A | `SRG-APP-000516-UEM-100010` | CAT II | The UEM Agent must perform the following functions: -enroll in management -configure whether users can unenroll from management -configure periodicity of reachability events. |
| UEM-A | `SRG-APP-000516-UEM-100011` | CAT II | The UEM Agent must be configured to perform one of the following actions upon an attempt to unenroll the mobile device from management: -prevent the unenrollment from occurring -wipe the device to factory default settings -wipe the work profile with all associated applications and data. |
| UEM-A | `SRG-APP-000555-UEM-100014` | CAT I | All UEM Agent cryptography supporting DoW functionality must be FIPS 140-3 validated. |
| VPN | `SRG-NET-000019-VPN-000040` | CAT II | The VPN Gateway must ensure inbound and outbound traffic is configured with a security policy in compliance with information flow control policies. |
| VPN | `SRG-NET-000019-VPN-002435` | CAT II | The TLS VPN must be configured to limit authenticated client sessions to initial session source IP. |
| VPN | `SRG-NET-000041-VPN-000110` | CAT II | The Remote Access VPN Gateway and/or client must display the Standard Mandatory DOD Notice and Consent Banner before granting remote access to the network. |
| VPN | `SRG-NET-000042-VPN-000120` | CAT II | The Remote Access VPN Gateway and/or client must enforce a policy to retain the Standard Mandatory DOD Notice and Consent Banner on the screen until users acknowledge the usage conditions and take explicit actions to log on for further access. |
| VPN | `SRG-NET-000062-VPN-000200` | CAT I | The TLS VPN Gateway must use TLS 1.2, at a minimum, to protect the confidentiality of sensitive data during transmission for remote access connections. |
| VPN | `SRG-NET-000063-VPN-000220` | CAT II | The VPN Gateway must be configured to use IPsec with SHA-2 at 384 bits or greater for hashing to protect the integrity of remote access sessions. |
| VPN | `SRG-NET-000074-VPN-000250` | CAT I | The IPSec VPN must be configured to use a Diffie-Hellman (DH) Group of 16 or greater for Internet Key Exchange (IKE) Phase 1. |
| VPN | `SRG-NET-000132-VPN-000450` | CAT II | The VPN Gateway must be configured to prohibit the use of all unnecessary and/or nonsecure functions, ports, protocols, and/or services, as defined in the PPSM CAL and vulnerability assessments. |
| VPN | `SRG-NET-000132-VPN-000460` | CAT II | The IPsec VPN Gateway must use IKEv2 for IPsec VPN security associations. |
| VPN | `SRG-NET-000138-VPN-000490` | CAT II | The VPN Gateway must uniquely identify and authenticate organizational users (or processes acting on behalf of organizational users). |
| VPN | `SRG-NET-000140-VPN-000500` | CAT I | The VPN Gateway must use multifactor authentication (e.g., DoD PKI) for network access to non-privileged accounts. |
| VPN | `SRG-NET-000145-VPN-000510` | CAT II | The VPN Client must implement multifactor authentication for network access to nonprivileged accounts such that one of the factors is provided by a device separate from the system gaining access. |
| VPN | `SRG-NET-000147-VPN-000530` | CAT II | The IPsec VPN Gateway must use anti-replay mechanisms for security associations. |
| VPN | `SRG-NET-000148-VPN-000540` | CAT II | The VPN Gateway must uniquely identify all network-connected endpoint devices before establishing a connection. |
| VPN | `SRG-NET-000164-VPN-000560` | CAT II | The VPN Gateway, when utilizing PKI-based authentication, must validate certificates by constructing a certification path (which includes status information) to an accepted trust anchor. |
| VPN | `SRG-NET-000166-VPN-000580` | CAT II | The Remote Access VPN Gateway must use a separate authentication server (e.g., LDAP, RADIUS, TACACS+) to perform user authentication. |
| VPN | `SRG-NET-000166-VPN-000590` | CAT II | The VPN Gateway must map the authenticated identity to the user account for PKI-based authentication. |
| VPN | `SRG-NET-000213-VPN-000720` | CAT III | The VPN Gateway must terminate all network connections associated with a communications session at the end of the session. |
| VPN | `SRG-NET-000230-VPN-000780` | CAT I | The IPSec VPN must be configured to use FIPS-validated SHA-2 at 384 bits or higher for Internet Key Exchange (IKE). |
| VPN | `SRG-NET-000230-VPN-002436` | CAT II | The VPN Gateway must use Always On VPN connections for remote computing. |
| VPN | `SRG-NET-000314-VPN-001060` | CAT II | The VPN Gateway administrator accounts or security policy must be configured to allow the system administrator to immediately disconnect or disable remote access to devices and/or users when needed. |
| VPN | `SRG-NET-000317-VPN-001090` | CAT I | The IPsec VPN Gateway must use AES encryption for the Internet Key Exchange (IKE) proposal to protect confidentiality of remote access sessions. |
| VPN | `SRG-NET-000334-VPN-001260` | CAT II | The VPN Gateway must off-load audit records onto a different system or media than the system being audited. |
| VPN | `SRG-NET-000337-VPN-001290` | CAT II | The VPN Gateway must renegotiate the IPsec security association (SA) after eight hours or less. |
| VPN | `SRG-NET-000337-VPN-001300` | CAT II | The VPN Gateway must renegotiate the IKE security association (SA) after eight hours or less. |
| VPN | `SRG-NET-000341-VPN-001350` | CAT II | The VPN Gateway must accept the Common Access Card (CAC) credential. |
| VPN | `SRG-NET-000342-VPN-001360` | CAT II | The VPN Gateway must electronically verify the Common Access Card (CAC) credential. |
| VPN | `SRG-NET-000343-VPN-001370` | CAT II | The VPN Gateway must authenticate all network-connected endpoint devices before establishing a connection. |
| VPN | `SRG-NET-000355-VPN-002433` | CAT II | The VPN Gateway providing authentication intermediary services must only accept end entity certificates (user or machine) issued by DOD PKI or DOD-approved PKI Certification Authorities (CAs) for the establishment of VPN sessions. |
| VPN | `SRG-NET-000369-VPN-001620` | CAT II | The VPN Gateway must disable split-tunneling for remote clients VPNs. |
| VPN | `SRG-NET-000371-VPN-001640` | CAT I | The IPsec VPN Gateway must specify Perfect Forward Secrecy (PFS) during Internet Key Exchange (IKE) negotiation. |
| VPN | `SRG-NET-000371-VPN-001650` | CAT I | The VPN Gateway and Client must be configured to protect the confidentiality and integrity of transmitted information. |
| VPN | `SRG-NET-000510-VPN-002170` | CAT II | The VPN Gateway must use a FIPS-validated cryptographic module to implement encryption services for unclassified information requiring confidentiality. |
| VPN | `SRG-NET-000512-VPN-002220` | CAT I | The IPsec VPN Gateway must use Internet Key Exchange (IKE) for IPsec VPN Security Associations (SAs). |
| VPN | `SRG-NET-000518-VPN-002280` | CAT II | The VPN Client logout function must be configured to terminate the session on/with the VPN Gateway. |
| VPN | `SRG-NET-000519-VPN-002290` | CAT II | The VPN Client must display an explicit logout message to users indicating the reliable termination of authenticated communications sessions. |
| VPN | `SRG-NET-000525-VPN-002330` | CAT I | The IPsec VPN must use AES256 or greater encryption for the IPsec proposal to protect the confidentiality of remote access sessions. |
| VPN | `SRG-NET-000530-VPN-002340` | CAT II | The TLS VPN Gateway that supports Government-only services must prohibit client negotiation to TLS 1.1, TLS 1.0, SSL 2.0, or SSL 3.0. |
| VPN | `SRG-NET-000580-VPN-002410` | CAT II | The VPN Gateway must validate certificates used for Transport Layer Security (TLS) functions by performing RFC 5280-compliant certification path validation. |

### Collecting evidence

On the EMS host, run `sudo emscli system get info` and keep the output
(EMS version, FIPS state, operating system, and kernel) with the
checklist, together with the operating system assessment of the host.
Add screenshots or exports of the panes the map cites, above all
*Administration > Admin Users*, *Administration > Admin Roles*,
*Administration > Admin User Settings*, *Administration > SAML SSO*,
*System Settings > EMS Settings* (remote HTTPS access, login banner,
lockout, user verification, code signing, and scheduled backup),
*System Settings > Logs*, *System Settings > EMS Server Certificates*, and
*System Settings > Feature Select*. Export each endpoint profile in use
(*Endpoint Profiles > Manage Profiles*) so that its XML, including the
Remote Access and System Settings profiles, is part of the evidence, and
list the endpoint policies and the groups they apply to. From
*Endpoints > All Endpoints*, export the endpoint list with the FortiClient
version and connection state of each endpoint, and keep the backup
schedule and the location of the EMS database backups.

## Validation and Troubleshooting

- **A feature in the map is missing.** Check the version column against
  both products: a FortiClient feature needs a FortiClient release and,
  usually, an EMS release that offers the setting, and many features need
  a license (ZTNA, EPP) or a FortiOS release on the FortiGate.
- **A setting is not where the map says.** EMS 7.0 and 7.2 run on Windows
  Server and have no `emscli`; some panes were renamed (Zero Trust tags
  became security posture tags in 7.4); and from 7.4.6 the SSL VPN option
  is hidden until it is enabled with `emscli feature set`. Check the
  Administration Guide of your release.
- **A setting has no field in the GUI.** Use the profile's XML
  Configuration view; the XML Reference documents settings that the GUI
  does not show, such as `endpoint_control/invalid_cert_action`.
- **Endpoints stop connecting after hardening.** Check that the endpoint
  control certificate is trusted by the endpoints and matches the EMS FQDN,
  that port 8013 is open, and that the connection key matches; with the
  invalid certificate action set to deny, an untrusted certificate blocks
  every endpoint.
- **An IPsec VPN tunnel fails after the proposals are changed.** The
  phase 1 and phase 2 proposals, Diffie-Hellman groups, and key lifetimes
  in the Remote Access profile must match the FortiGate phase 1 and phase 2
  configuration.
- **A requirement has no matching feature.** Some requirements are met by
  procedure (account reviews, hash checks), by another system (the
  identity provider, FortiAnalyzer, the FortiGate), or by the host
  operating system. Record how each requirement is met, not just which
  feature covers it.

## Security and Best Practices

- Keep FortiClient and EMS on vendor-supported releases, and install
  security updates within 30 days (UEM-S `SRG-APP-000456-UEM-000330`),
  under change control.
- Log administrators on through SAML SSO with CAC, give each a
  least-privilege admin role and trusted hosts, set the session to expire
  after 15 minutes, disable accounts after 35 days of inactivity, and enable
  the login banner.
- Run EMS in FIPS mode where required, install certificates from a
  DoD-approved CA for the web server and endpoint control, and restrict
  remote HTTPS access to the management network.
- Deploy FortiClient with a connection key and the disconnect lock, set the
  invalid EMS certificate action to deny, and sign the installers.
- Configure IPsec VPN tunnels with IKEv2, AES-256, SHA-384,
  Diffie-Hellman group 16 or higher, PFS, and replay detection; reject
  invalid gateway certificates; use smart card certificates; show the DoD
  notice as the disclaimer message; and disable personal VPNs.
- Send EMS and FortiClient logs to FortiAnalyzer or syslog, and back up
  the EMS database to another system.
- Review this map each time Fortinet publishes a FortiClient or EMS
  release or DISA updates the UEM or VPN SRGs.

## References and Knowledge Checks

**References:**

- Fortinet, *FortiClient & FortiClient EMS New Features Guide*, trains 7.0,
  7.2, 7.4, and 8.0, including the Index page of each release
  (docs.fortinet.com, FortiClient documentation).
- Fortinet, *FortiClient EMS Release Notes* (page "What's new") and
  *FortiClient (Windows) Release Notes*, releases 7.0.0 to 8.0.0.
- Fortinet, *FortiClient EMS 7.0.0 Administration Guide* and *FortiClient
  7.0.0 XML Reference* (for the core features), and *FortiClient 8.0.0 EMS
  Administration Guide*, *FortiClient 8.0.0 XML Reference*, *FortiClient
  EMS 8.0.0 CLI Reference*, *FortiClient 8.0.0 Administration Guide*, and
  *FortiClient EMS 8.0.0 Release Notes*.
- DISA Unified Endpoint Management Server SRG V2R6, Unified Endpoint
  Management Agent SRG V2R2, and Virtual Private Network SRG V3R5, from the
  October 2026 STIG Library Compilation.
- [Chapter 03](03-the-srg-catalog-how-stigs-are-built-and-what-to-do-without-one.md)
  (SRG-based assessment),
  [Chapter 10](10-fortinet-products-stigs-and-srg-mapping.md) (Fortinet
  products),
  [Chapter 11](11-fortiswitch-feature-version-and-srg-map.md) (the
  FortiSwitch map), and
  [Chapter 12](12-fortianalyzer-feature-version-and-srg-map.md) (the
  FortiAnalyzer map, the model for this one).

**Knowledge checks:**

1. Why are the UEM Server and UEM Agent SRGs the closest match for EMS
   and FortiClient, and what does the VPN SRG add?
2. Which operating system STIG applies to an EMS 7.2 server, and which to
   an EMS 8.0 server?
3. Where does the version data come from, and how does the version column
   show whether a release number belongs to FortiClient or to EMS?
4. Which FortiClient settings keep an endpoint enrolled in EMS and make it
   accept configuration only from that EMS?
5. Which Remote Access profile settings must match the VPN SRG's IPsec
   requirements, and which VPN requirements are left to the FortiGate?
6. Which requirements can FortiClient and EMS not meet exactly, and how do
   you handle them?

## Summary and Completion Checklist

FortiClient and FortiClient EMS have no STIG, so they are assessed against
the UEM Server SRG for EMS, the UEM Agent SRG for the managed FortiClient
agent, and the VPN SRG for its remote access role, with the operating
system STIGs for the endpoints and the EMS host. This chapter maps
185 features to the FortiClient or EMS release that introduced them,
to 124 requirements (71 UEM-S, 14 UEM-A, and 39
VPN), and to the GUI pane, XML setting, or command that configures them:
63 core platform features, and 122 features from the
FortiClient & FortiClient EMS 7.0 through 8.0 New Features Guides.
Operational features with no direct requirement fall under the requirement
to disable non-essential capabilities when unused, and the operating
system STIGs still apply in full to every endpoint and to the EMS host.

- [ ] Can explain why FortiClient and EMS are assessed against the UEM
  Server, UEM Agent, and VPN SRGs, and where the operating system STIGs
  apply.
- [ ] Can find the FortiClient or EMS release that introduced a feature.
- [ ] Can map a FortiClient or EMS feature to its UEM or VPN requirement.
- [ ] Can find the GUI pane, XML setting, or command that meets the
  requirement.
- [ ] Can collect the evidence and record the requirements that FortiClient
  and EMS cannot meet exactly.
