# Chapter 21: FortiSandbox Feature, Version, and SRG Map

## Learning Objectives

- Find the FortiSandbox release that introduced a given feature.
- Map each FortiSandbox feature to the Network Device Management (NDM) or
  Intrusion Detection and Prevention Systems (IDPS) SRG requirement it
  helps satisfy.
- Explain why the IDPS SRG is used for the detection features of a
  malware sandbox, and which IDPS requirements do not apply.
- Find the FortiSandbox CLI command, or the web UI pane, that configures
  each feature to meet its requirement.
- Use the map to scope an SRG-based assessment of FortiSandbox, which has
  no STIG of its own.
- Record the requirements that FortiSandbox cannot meet exactly, with
  their mitigations.

## Theory and Architecture

FortiSandbox is Fortinet's malware detonation and analysis system. Other
devices send it files and URLs, it runs them through an antivirus scan, a
static scan with AI models, a FortiGuard and Community Cloud lookup, and,
when needed, a dynamic scan in which the file is opened inside a guest
virtual machine (VM) and its behavior is rated. It returns a verdict
(Clean, Low, Medium, or High Risk, or Malicious) to the device that sent
the file, and it builds malware and URL packages and IOC packages that
FortiGate and other devices download as extra signatures and blocklists.
It has **no DISA STIG** (Chapter 10), so it is assessed against SRGs, as
described in Chapter 03. Chapter 10 assigns it the **Network Device
Management (NDM) SRG** for the management plane and asks that its **threat
data and integrations be protected**. This chapter adds the **Intrusion
Detection and Prevention Systems (IDPS) SRG** for the detection, blocking,
and alerting features only, for the reasons given below. For every
FortiSandbox feature the chapter gives **which FortiSandbox release
introduced it**, **which requirement it relates to**, and **which command
or web UI pane configures it to meet that requirement**.

FortiSandbox runs on hardware appliances, as a VM on private and public
clouds, and as a Fortinet-hosted service; this chapter covers the
FortiSandbox firmware that the appliances and VMs run. Its configuration
uses a few ideas again and again:

- **Input sources.** Files arrive in five ways: **device mode** (FortiGate,
  FortiMail, FortiWeb, FortiClient, FortiProxy, and FortiADC send files, over
  OFTP or, for inline block, HTTPS, after the device is authorized), **sniffer mode** (FortiSandbox
  extracts files and URLs from spanned switch ports and raises network
  alerts), **adapters** (ICAP, BCC, and MTA adapters for web proxies and
  mail systems), **network shares** and cloud storage (scheduled scans
  with quarantine), and **on-demand** submission in the web UI or through
  the JSON API.
- **Scan profiles and VMs.** The *Scan Profile* decides which file types
  enter the job queue, which go through the FortiGuard prefilter, and which guest VMs open
  them; *VM Settings* holds the default, optional, and custom VM images and
  their clone counts. FortiSandbox runs in **Full Mode** (static and dynamic
  scans) or **Lite Mode** (static scans only).
- **Interfaces.** port1 is the administration port (HTTPS by default; HTTP,
  SSH, and Telnet can be enabled). port3 is reserved for the guest VMs'
  outgoing traffic, which is live malware traffic and must reach the
  Internet only from an isolated network. The other ports carry device,
  sniffer, and cluster traffic.
- **HA cluster.** Several units form a load-balancing cluster of a primary,
  an optional secondary that takes over on failure, and worker nodes; scan
  settings are made on the primary and pushed to the others.
- **System settings.** Administrators, admin profiles, password policy,
  LDAP, RADIUS, and SAML servers, certificates, the login disclaimer, SNMP,
  mail server alerts, FortiGuard updates, and backups are set under
  *System*, and logging under *Log & Report*.

### Where the version data comes from

Fortinet publishes no Feature Matrix and no New Features Guide for
FortiSandbox. The only "What's new" document is a one-page *What's New in
FortiSandbox 5.0* for the 5.0 train. The **Release Notes** of every
release, however, have a page that lists its new features: "New features
and enhancements" in 4.0.0 through 5.0.7, and "What's new" in 5.2.0
through 5.2.2. docs.fortinet.com lists the FortiSandbox trains 2.5 through
5.2; this chapter covers the 4.0 train, the oldest 4.x train, through 5.2,
the newest. The version column was built from those pages for every
release in those trains that has one: 4.0.0 through 4.0.6, 4.2.0, 4.2.1,
and 4.2.3 through 4.2.8, 4.4.0 through 4.4.8, 5.0.0 through 5.0.7, and
5.2.0 through 5.2.2, 35 releases in all. The release notes of 4.2.2, 4.4.9,
and 4.4.10 have no such page. Seven pages list no features: 4.0.3 through
4.0.6 and 4.2.7 say that the release contains bug fixes, and 5.0.4 and
5.2.1 that it brings no new features.

Each top-level bullet of a page is one entry; nested bullets are its
details. Four adjustments were made:

- The 4.4.1 and 4.4.2 pages give their one feature as a paragraph, not a
  bullet; the paragraph was used.
- The 4.4.0 page opens with an "Effective Sandboxing Throughput" section,
  a datasheet rating that the page repeats as a bullet; only the bullet
  was used.
- A bullet repeated word for word on the same page (the FortiClient
  Security Fabric page in 4.4.0, and OCR in 5.0.0) was used once.
- One 5.2.2 bullet holds two features in two paragraphs (faster ICAP
  verdicts, and the fallback to a full engine package); it was split.

The table has two groups of rows:

- **Core platform features** (categories starting with *Core:*) are the
  long-standing capabilities that the requirements depend on: management
  access, administrator accounts and admin profiles, remote authentication,
  logging and alerts, time, SNMP, firmware, FortiGuard updates, backups,
  the HA cluster, and the detection functions themselves (scan profiles,
  VMs, the prefilter, allowlists and blocklists, YARA rules, device mode,
  sniffer mode, adapters, network shares, and IOC packages). Each one is in
  the table of contents of the **FortiSandbox 4.0.0 Administration Guide**
  or the **4.0.0 CLI Reference**, so it existed in 4.0.0 and is not in the
  release notes lists. Five core rows have a different version entry,
  explained below.
- **New features** are the 498 entries of the release notes
  pages. The categories were assigned for this chapter, because the
  release notes group features differently from release to release, and
  the titles were shortened from the release notes text. An entry listed
  again in a later release or train is one row with all its versions.

| Version entry | Meaning |
| --- | --- |
| `4.0.0 or earlier` | A core feature that is in the 4.0.0 Administration Guide or CLI Reference, the oldest release covered |
| `4.4.0 and later` | Introduced in FortiSandbox 4.4.0 |
| `4.2.5+; 4.4.1+` | Listed in two trains: from 4.2.5 in the 4.2 train and from 4.4.1 in the 4.4 train |
| `4.4 (CC technote)` | Documented only in the *FortiSandbox 4.4 NDcPP Common Criteria Technote* (CC mode and its login lockout) |
| `5.2.2 or earlier` | In the 5.2.2 Administration Guide or CLI Reference, but in no release notes page and not found in the 4.0.0 documents checked |

Three cautions apply. First, "and later" means later in the same train
and, usually, in later trains; a feature of a patch release may reach a
newer train only in a later patch. Second, many features depend on the
model (G models for TPM storage of the disk encryption key, the 3000G for
encrypted storage formatting, appliances for local two-factor
authentication), on the platform (public cloud features), or on a license
or subscription (Windows and Office VM licenses, the Advanced subscription
for PAIX AI model updates, Real-Time Anti-Phishing, FortiToken Cloud).
Third, a core row records a FortiSandbox capability, but its command or
pane was checked against the 5.2.2 documents and may differ on an older
release: the 4.0.0 Administration Guide arranges some settings
differently (system time, firmware, and backup were under *General
configuration*), and several commands the core rows use arrived later, as
the new-feature rows say (trusted hosts raised from three to 50 in 4.2.1,
the SSH login disclaimer in 4.2.3, SAML SSO in 4.4.0, the password policy
and the system-admin command in 4.4.3, data-at-rest encryption in 5.2.0,
and SFTP backups and the option to disable legacy OFTP device
authentication in 5.2.2).

### Where the SRG data comes from

The SRG column uses requirement IDs from the October 2026 DISA library:

| SRG column | SRG | Release | Applies to |
| --- | --- | --- | --- |
| **NDM** | Network Device Management SRG | V5R5, benchmark date 01 Jul 2026 | The management plane: administrator access, authentication, logging, time, SNMP, firmware, backups, and the protection of stored threat data and device integrations (assigned by Chapter 10) |
| **IDPS** | Intrusion Detection and Prevention Systems SRG | V3R4, benchmark date 28 Oct 2025 | The detection function: malicious code detection, blocking, quarantine, and alerting, signature and engine updates, traffic monitoring in sniffer mode, the content and off-loading of detection records, integration with the monitoring architecture, and isolation of the detonation network |

Chapter 10 names only the NDM SRG, which covers how FortiSandbox is
managed but has no requirement about what it is for. The IDPS SRG is a
clearly better fit for that part, because its malicious code requirements
describe FortiSandbox's job almost word for word, and it is the SRG DISA
uses for network devices that detect and block threats. It is used here
for the detection features only:

- **Malicious code, the core of FortiSandbox:** detecting mobile code that
  is unsigned or behaves unusually (IDPS `SRG-NET-000228-IDPS-00196`),
  real-time monitoring of files from external sources at network entry and
  exit points (IDPS `SRG-NET-000248-IDPS-00206`), blocking malicious code
  (IDPS `SRG-NET-000249-IDPS-00176`) or quarantining it
  (IDPS `SRG-NET-000249-IDPS-00221`), and blocking prohibited mobile code
  at the enclave boundary (IDPS `SRG-NET-000229-IDPS-00163`).
- **Alerts:** an immediate alert to the system administrator when
  malicious code is detected (IDPS `SRG-NET-000249-IDPS-00222`), and alerts
  to the ISSM and ISSO for intrusion events and for new malware
  propagation (IDPS `SRG-NET-000392-IDPS-00214`,
  IDPS `SRG-NET-000392-IDPS-00219`).
- **Updates:** automatic updates of the malicious code protection
  (IDPS `SRG-NET-000246-IDPS-00205`, IDPS `SRG-NET-000251-IDPS-00178`) and
  immediate use of updated rules and signatures
  (IDPS `SRG-NET-000019-IDPS-00187`).
- **Sniffer mode:** monitoring inbound and outbound traffic for unusual
  activity (IDPS `SRG-NET-000390-IDPS-00212`,
  IDPS `SRG-NET-000391-IDPS-00213`), attribute- and content-based
  inspection (IDPS `SRG-NET-000019-IDPS-00019`), and restricting harmful
  traffic, which FortiSandbox does with TCP resets
  (IDPS `SRG-NET-000018-IDPS-00018`).
- **Detection records:** the content of the records (IDPS
  `SRG-NET-000074-IDPS-00059` through IDPS `SRG-NET-000078-IDPS-00063`),
  records of detection events (IDPS `SRG-NET-000113-IDPS-00013`), a format
  that central tools can use (IDPS `SRG-NET-000091-IDPS-00193`), and
  off-loading them to a central log server in real time
  (IDPS `SRG-NET-000334-IDPS-00191`, IDPS `SRG-NET-000511-IDPS-00012`).
- **Integrations and isolation:** integration with a network-wide
  monitoring capability, which for FortiSandbox means its device, adapter,
  IOC, and webhook integrations (IDPS `SRG-NET-000383-IDPS-00208`), and
  separate subnetworks for critical functions, which for FortiSandbox
  means the isolated port3 network that the guest VMs use
  (IDPS `SRG-NET-000715-IDPS-00120`).
- **Configuration:** the IDPS requirement to be configured according to
  DoD policy and best practices (IDPS `SRG-NET-000512-IDPS-00194`), next to
  its NDM counterpart.

The other IDPS requirements are left out because they describe an inline
intrusion prevention system: blocking denial-of-service, ICMP, and
injection attacks in passing traffic, reassembling fragmented packets,
detecting unauthorized network services, failing to a secure state in the
traffic path, and the PPSM rules for monitored traffic. FortiSandbox is not
in the traffic path; where blocking happens inline, FortiGate, FortiProxy,
FortiMail, or the ICAP client holds the file until FortiSandbox returns a
verdict, and the blocking requirement is met by the two systems together.
The requirement not to run unnecessary functions is taken from the NDM SRG
for every row (below).

The requirement IDs are the **rule version IDs** from the XCCDF files, and
the severity is the rule's severity (high = CAT I, medium = CAT II, low =
CAT III); every IDPS requirement used is CAT II. Each feature maps to one
of three kinds of relationship:

- **Implements a requirement.** The feature is how FortiSandbox meets a
  requirement. Dynamic analysis in guest VMs implements the requirement to
  detect mobile code that behaves unusually
  (IDPS `SRG-NET-000228-IDPS-00196`), for example.
- **Must be configured to meet a requirement.** The feature is in scope of
  a requirement and has to be set up correctly. The password policy must
  require 15 characters (NDM `SRG-APP-000164-NDM-000252`), for example.
- **No direct requirement.** The feature is operational, such as a
  platform, a GUI change, a report detail, or a troubleshooting command. It
  has no requirement of its own, but if it is not needed it falls under
  the NDM requirement not to have unnecessary functions enabled
  (NDM `SRG-APP-000142-NDM-000245`).

The mapping is a starting point for an assessment, not a ruling. Confirm it
with your assessor, especially the use of the IDPS SRG, and where a
requirement is organization-defined or depends on how FortiSandbox is
deployed.

### Where the commands come from

The command column was checked against the **FortiSandbox 5.2.2 CLI
Reference Guide** (2 October 2026), the newest CLI Reference, and the
**FortiSandbox 5.2.2 Administration Guide** of the same date. The
FortiSandbox CLI is not the FortiOS-style `config` and `set` tree: apart
from a few `set` and `unset` configuration commands for the ports and the
gateway, each command is a single word with options, such as
`device-authorization -m` or `set-tlsver -l`, and the CLI Reference says
that the CLI is meant for initial configuration and troubleshooting. Most
settings are therefore made in the web UI, and the column names the pane.
The check was automatic: each command name against the commands of the
CLI Reference, each option against that command's syntax and option table,
each listed option value against the documented values, each `set` and
`unset` attribute against their syntax, and each GUI pane against the
Administration Guide text or its outline. One command, `cc-mode-conf -e`,
is not in the 5.2.2 CLI Reference; it was checked against the
*FortiSandbox 4.4 NDcPP Common Criteria Technote*. Read the column this
way:

- Commands run on the FortiSandbox CLI, over the console, SSH, or the CLI
  console in the web UI. The full command set needs an admin profile with
  the JSON API / CLI option enabled; system-admin and rename-admin need the
  Super Admin profile. Options take their value directly after the letter, as in
  `-tscp`.
- **GUI:** entries name the FortiSandbox web UI pane.
- Statements are separated by `;` to fit in a table cell; on the CLI, enter
  each one on its own line. Values in `<ANGLE_BRACKETS>` are placeholders
  for your own names, addresses, and paths.
- For **"No direct requirement"** rows, the command shown is the one that
  disables the feature when it is unused. A dash (**—**) means there is
  nothing to change: the feature is a platform, a GUI change, a behavior
  change, a report or log detail, a troubleshooting command, or a
  capability that is off unless configured, or the 5.2.2 documents have no
  setting for it.

Some requirements cannot be met exactly with FortiSandbox settings. Record
them on the checklist as open findings with mitigations, or meet them
another way:

- **No PKI login on FortiSandbox itself.** The administrator types are
  local, LDAP, RADIUS, LDAP wildcard, and RADIUS wildcard, plus SAML single
  sign-on (4.4.0 and later); local two-factor authentication uses email,
  SMS, or FortiToken Mobile through FortiToken Cloud, and only on
  appliances and the FSA-VM0T. FortiSandbox has no certificate (CAC) login
  of its own, so DoD PKI multifactor authentication
  (NDM `SRG-APP-000149-NDM-000247`, CAT I) is met only through a SAML
  identity provider or a RADIUS server that enforces it. Keep one local
  account of last resort and record how the requirement is met.
- **FIPS and CC mode.** The 5.2.2 Administration Guide and CLI Reference
  do not mention FIPS 140 or a CC mode. The *FortiSandbox 4.4 NDcPP Common
  Criteria Technote* describes a CC mode (`cc-mode-conf -e`), with
  self-tests, restricted TLS and SSH cipher suites, and a configuration
  reset when it is enabled. The FIPS requirements
  (NDM `SRG-APP-000179-NDM-000265`, NDM `SRG-APP-000412-NDM-000331`,
  NDM `SRG-APP-000411-NDM-000330`) are otherwise met, if at all, by allowing
  only TLS 1.2 and 1.3 (the default) and SNMPv3 with SHA1 and AES. Check
  the NIST Cryptographic Module Validation Program and the NIAP product
  list for your FortiSandbox release.
- **Login lockout.** The only lockout setting documented is in the CC
  technote: in CC mode, three failed logins lock the account for three
  minutes by default, and *System > Settings* offers a Failed Sign-On
  Attempt Limit of 3 to 20 and a Lockout Period of 3 to 60 minutes; it
  does not apply to the console. The 5.2.2 Administration Guide lists no
  such fields. Outside CC mode, enforce the lockout of three attempts and
  15 minutes (NDM `SRG-APP-000065-NDM-000214`) on the authentication
  server, restrict logins with trusted hosts, and record the finding.
- **Password rules.** The password policy (4.4.3 and later) sets the
  minimum length (6 by default), the number of each character type,
  expiration, and reuse, for local administrators only. Administrator
  passwords can be 6 to 64 characters. There is no setting for the number
  of changed characters (NDM `SRG-APP-000170-NDM-000329`) or a check
  against a list of commonly used or compromised passwords
  (NDM `SRG-APP-000845-NDM-000220`). Prefer remote authentication.
- **Concurrent administrator sessions.** No setting limits the number of
  sessions per administrator (NDM `SRG-APP-000001-NDM-000200`). Record the
  finding, or enforce the limit on the authentication server.
- **NTP authentication.** The 4.0.0 Administration Guide offers FortiGuard
  or one NTP server with a fixed five-minute interval, the 5.2.2
  Administration Guide describes no NTP settings beyond the system time in
  the System Information widget, and no NTP authentication is documented
  (NDM `SRG-APP-000395-NDM-000347`). The CC technote lists NTP as excluded
  from the evaluated configuration. Use an NTP server on the protected
  management network and record the finding.
- **SNMPv3 algorithms.** SNMPv3 users offer MD5 or SHA1 for
  authentication and DES or AES for encryption. Use SHA1 and AES only
  (NDM `SRG-APP-000395-NDM-000310`); no SHA-2 option is offered.
- **Log buffering and lost log servers.** If the log server cannot be
  reached, FortiSandbox keeps up to 1024 logs and discards newer logs when
  the buffer is full. Nothing in the 5.2.2 Administration Guide alerts when
  a log server is lost (NDM `SRG-APP-000360-NDM-000295`,
  IDPS `SRG-NET-000335-IDPS-00014`); the CC technote mentions only an event
  log message when the TLS connection to FortiAnalyzer fails. Configure two
  log servers, and monitor log arrival and alert on the log server.
- **Firmware signatures.** The Administration Guide does not say that
  FortiSandbox verifies a digital signature on firmware images
  (NDM `SRG-APP-000131-NDM-000243`); the CC technote mentions a firmware
  integrity self-test in CC mode. Compare the image checksum with the one
  on the Fortinet support site before every upgrade.
- **Cluster traffic.** The post-quantum appendix of the 5.2.2
  Administration Guide says that the cluster protocol can fall back to
  plain text when encrypted communication cannot be established. Enable
  encryption on the primary node (`hc-primary -sg -e`) and keep cluster
  traffic on a dedicated, isolated network.
- **Defaults that share or trust too much.** Legacy OFTP device login
  authentication is enabled by default for backward compatibility and is
  described as less secure; it can be disabled only from 5.2.2
  (`device-authorization -q`). Upload of malicious and suspicious file
  information to the Community Cloud is enabled by default, so threat data
  leaves the enclave unless it is disabled
  (`upload-settings -tuploadcloud -d`). Treat both as findings until they are changed.
- **Settings with no command.** Most settings, including the idle timeout,
  the login disclaimer, admin profiles, the password policy, SNMP, log
  servers, and the scan profile, have no CLI command in the 5.2.2 CLI
  Reference, so those rows name the web UI pane. Several features listed
  in the release notes, such as PEXBox, the AI mode, and Content Disarm
  and Reconstruction, have no setting in the 5.2.2 documents; those rows
  end in a dash.

## Design Considerations

- **Pick the release first, then the features.** If your design depends on
  a feature introduced in a certain release (SAML SSO in 4.4.0, the
  password policy in 4.4.3, data-at-rest encryption in 5.2.0, or disabling
  legacy OFTP device authentication in 5.2.2), that sets the minimum
  FortiSandbox release, and it must be a vendor-supported release
  (NDM `SRG-APP-001035-NDM-000340`).
- **Isolate the detonation network.** port3 carries the traffic of files
  that are running as malware. Put it on its own network behind a
  firewall, with Internet access only, never a route to protected subnets
  or the management network, and do not reuse production addresses on it.
- **Keep management out of band.** Allow HTTPS and SSH only on port1 (or
  another administrative port) on a dedicated management network, set
  trusted hosts for every administrator, and keep the API port, if one is
  used, on that network too.
- **Protect the threat data.** Original files, job traces, IOC packages,
  and reports contain live malware and sensitive content from your own
  network. Limit Download Original File and the job views through admin
  profiles, keep retention periods to what the investigation process
  needs, encrypt data at rest where the model supports it, and send
  samples or statistics to Fortinet only if that sharing is approved.
- **Protect the integrations.** Authorize every new device manually,
  disable legacy OFTP authentication once all devices present
  certificates with their serial numbers, use DoD-issued certificates for
  ICAP, MTA, and BCC adapters, and send IOC packages and webhooks only to
  approved systems.
- **Decide where blocking happens.** FortiSandbox returns verdicts; the
  file is blocked by the device that holds it. Use inline block on
  FortiGate and FortiProxy, hold mode on ICAP, and quarantine on network
  shares where the policy is to block, and document which device meets the
  blocking requirement for each input source.
- **Turn off what is not used.** Telnet, HTTP, SNMP v1 and v2c, Community
  Cloud upload, cloud VMs, VM interaction, job archives, and unused input
  sources all need a reason to stay on.

## Implementation and Automation

### The FortiSandbox feature map

The SRG column uses the abbreviations defined in *Where the SRG data comes
from*. The requirement titles are listed in the next table. The command
column follows the conventions in *Where the commands come from*.

[Download the feature map as CSV](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/data/volume-172-disa-srgs-and-stigs/21-fortisandbox-feature-version-and-srg-map-feature-map.csv) (518 rows).

| Category | Feature | Introduced (FortiSandbox) | SRG requirement(s) | Command to satisfy the requirement |
| --- | --- | --- | --- | --- |
| Core: Management access | Administrative access on port1 (HTTPS by default; HTTP, SSH, and Telnet optional) | 4.0.0 or earlier | NDM `SRG-APP-000142-NDM-000245`; NDM `SRG-APP-000412-NDM-000331`; NDM `SRG-APP-000172-NDM-000259`; NDM `SRG-APP-000408-NDM-000314` | GUI: System > Interfaces (Access Rights on port1: HTTPS and SSH only, HTTP and Telnet off; other administrative ports follow port1) |
| Core: Management access | Additional administrative ports, including aggregate interfaces | 4.0.0 or earlier | NDM `SRG-APP-000880-NDM-000290` | `set admin-port <PORT>` (a port on the dedicated management network, never port3 or a sniffer port) |
| Core: Management access | Web UI and SSH server certificates (Fortinet factory certificate by default) | 4.0.0 or earlier | NDM `SRG-APP-000516-NDM-000344`; NDM `SRG-APP-000910-NDM-000300` | GUI: System > Certificates (import a DoD-issued certificate and assign it to the HTTPS and SSH services with Service) |
| Core: Management access | Trusted hosts for each administrator (three IPv4 and three IPv6 hosts in 4.0.0) | 4.0.0 or earlier | NDM `SRG-APP-000408-NDM-000314`; NDM `SRG-APP-000038-NDM-000213` | GUI: System > Administrators (Restrict login to trusted host, on every account) |
| Core: Management access | Idle timeout for administrator sessions | 4.0.0 or earlier | NDM `SRG-APP-000190-NDM-000267`; NDM `SRG-APP-000220-NDM-000268` | GUI: System > Settings (Idle timeout: 5 minutes or less; the CC technote says it also applies to SSH and the console) |
| Core: Management access | Administrator logout | 4.0.0 or earlier | NDM `SRG-APP-000296-NDM-000280`; NDM `SRG-APP-000220-NDM-000268` | — |
| Core: Management access | Login disclaimer on the web UI | 4.0.0 or earlier | NDM `SRG-APP-000068-NDM-000215`; NDM `SRG-APP-000069-NDM-000216` | GUI: System > Login Disclaimer (enable it with the Standard Mandatory DoD Notice and Consent Banner) |
| Core: Management access | TLS versions of the HTTPS service | 4.0.0 or earlier | NDM `SRG-APP-000412-NDM-000331`; NDM `SRG-APP-000411-NDM-000330`; NDM `SRG-APP-000172-NDM-000259` | `set-tlsver -l`; `set-tlsver -r` (TLS 1.2 and 1.3, the default; TLS 1.0 and 1.1 are not supported) |
| Core: Management access | Login lockout after failed logins (CC mode) | 4.4 (CC technote) | NDM `SRG-APP-000065-NDM-000214` | GUI: System > Settings (Admin Session in CC mode: Failed Sign-On Attempt Limit 3 and Lockout Period 15 minutes; the 5.2.2 Administration Guide lists no lockout fields) |
| Core: Management access | CC mode of operation (NDcPP evaluated configuration, self-tests, restricted cipher suites) | 4.4 (CC technote) | NDM `SRG-APP-000179-NDM-000265`; NDM `SRG-APP-000412-NDM-000331`; NDM `SRG-APP-000411-NDM-000330`; NDM `SRG-APP-000516-NDM-000317` | `cc-mode-conf -e` (from the FortiSandbox 4.4 NDcPP technote; not in the 5.2.2 CLI Reference; it resets the configuration) |
| Core: Management access | TCP timestamp responses | 5.2.2 or earlier | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | `set-tcp-timestamp-response -d` |
| Core: Administrator accounts | Default admin account and local administrator accounts | 4.0.0 or earlier | NDM `SRG-APP-000148-NDM-000346`; NDM `SRG-APP-000153-NDM-000249`; NDM `SRG-APP-000178-NDM-000264` | GUI: System > Administrators (one local account of last resort with a password of 15 or more characters) |
| Core: Administrator accounts | Admin profiles (Super Admin, Read Only, and Device, and custom profiles with Read Write, Read Only, or None for each menu) | 4.0.0 or earlier | NDM `SRG-APP-000033-NDM-000212`; NDM `SRG-APP-000231-NDM-000271`; NDM `SRG-APP-000380-NDM-000304`; NDM `SRG-APP-000340-NDM-000288`; NDM `SRG-APP-000516-NDM-000335` | GUI: System > Admin Profiles (Super Admin only for the administrators who need it) |
| Core: Administrator accounts | JSON API and CLI access for each admin profile | 5.2.2 or earlier | NDM `SRG-APP-000340-NDM-000288`; NDM `SRG-APP-000408-NDM-000314` | GUI: System > Admin Profiles (API/CLI Access: Disallowed for profiles that do not need them) |
| Core: Administrator accounts | Device administrators limited to assigned devices and device groups | 4.0.0 or earlier | NDM `SRG-APP-000033-NDM-000212`; NDM `SRG-APP-000231-NDM-000271` | GUI: System > Device Groups |
| Core: Administrator accounts | Maintainer account for resetting administrator passwords from the console | 4.0.0 or earlier | NDM `SRG-APP-000408-NDM-000314`; NDM `SRG-APP-000148-NDM-000346` | `set-maintainer -d` (enable it only for a password recovery) |
| Core: Authentication | LDAP servers for administrator authentication (LDAPS or STARTTLS) | 4.0.0 or earlier | NDM `SRG-APP-000516-NDM-000336`; NDM `SRG-APP-000153-NDM-000249`; NDM `SRG-APP-000172-NDM-000259` | GUI: System > LDAP Servers (Secure Connection with LDAPS and the DoD CA certificate) |
| Core: Authentication | RADIUS servers for administrator authentication (primary and secondary, with RADIUS two-factor authentication) | 4.0.0 or earlier | NDM `SRG-APP-000516-NDM-000336`; NDM `SRG-APP-000820-NDM-000170`; NDM `SRG-APP-000825-NDM-000180` | GUI: System > RADIUS Servers (the RADIUS server enforces DoD PKI or another approved second factor) |
| Core: Authentication | Wildcard LDAP and RADIUS administrators (all accounts of a group) | 4.0.0 or earlier | NDM `SRG-APP-000153-NDM-000249`; NDM `SRG-APP-000033-NDM-000212` | GUI: System > Administrators (Type LDAP WILDCARD or RADIUS WILDCARD, with the narrowest admin profile) |
| Core: Authentication | Two-factor authentication for local administrators (email, SMS, or FortiToken Mobile) | 4.0.0 or earlier | NDM `SRG-APP-000820-NDM-000170`; NDM `SRG-APP-000825-NDM-000180` | GUI: System > Administrators (Two-factor Authentication; appliances only in 4.0.0, and FSA-VM0T with FortiToken Cloud in 5.2.2) |
| Core: Authentication | Timeout for RADIUS and LDAP authentication | 4.0.0 or earlier | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — (remote-auth-timeout keeps the default of 10 seconds unless the server is slow) |
| Core: Logging | Local event logs (system, VM, job, HA cluster, and notification events) | 4.0.0 or earlier | NDM `SRG-APP-000026-NDM-000208`; NDM `SRG-APP-000027-NDM-000209`; NDM `SRG-APP-000029-NDM-000211`; NDM `SRG-APP-000343-NDM-000289`; NDM `SRG-APP-000380-NDM-000304`; NDM `SRG-APP-000503-NDM-000320`; NDM `SRG-APP-000095-NDM-000225`; NDM `SRG-APP-000096-NDM-000226`; NDM `SRG-APP-000100-NDM-000230`; NDM `SRG-APP-000098-NDM-000228`; NDM `SRG-APP-000099-NDM-000229` | GUI: Log & Report > Events (keep the default categories) |
| Core: Logging | Local log levels and report retention | 4.0.0 or earlier | NDM `SRG-APP-000357-NDM-000293` | GUI: Log & Report > Settings (Log Level: Information and higher; local logs hold up to 1 GB) |
| Core: Logging | Remote log servers (syslog over TCP or UDP, CEF, and FortiAnalyzer) | 4.0.0 or earlier | NDM `SRG-APP-000515-NDM-000325`; NDM `SRG-APP-000516-NDM-000350`; IDPS `SRG-NET-000334-IDPS-00191`; IDPS `SRG-NET-000511-IDPS-00012`; IDPS `SRG-NET-000091-IDPS-00193` | GUI: Log & Report > Log Servers (two servers, syslog over TCP with Secure Connection or FortiAnalyzer, with Alert, Critical, Error, Warning, and Information logs) |
| Core: Logging | Recording of CLI input and output | 4.0.0 or earlier | NDM `SRG-APP-000101-NDM-000231` | `diagnose-clilog -e` (or CLI Logging under Log & Report > Settings) |
| Core: Logging | Protection of logs through admin profiles | 4.0.0 or earlier | NDM `SRG-APP-000119-NDM-000236`; NDM `SRG-APP-000120-NDM-000237` | GUI: System > Admin Profiles (Logs & Reports: Read Only or None for administrators who do not manage logs; log-purge deletes all system logs) |
| Core: Logging | Job event logs for every scanned file and URL (rating, malware name, source and destination addresses, service) | 4.0.0 or earlier | IDPS `SRG-NET-000113-IDPS-00013`; IDPS `SRG-NET-000074-IDPS-00059`; IDPS `SRG-NET-000075-IDPS-00060`; IDPS `SRG-NET-000076-IDPS-00061`; IDPS `SRG-NET-000077-IDPS-00062`; IDPS `SRG-NET-000078-IDPS-00063` | GUI: Log & Report > Events > Job Events (and Alert logs to the remote log servers) |
| Core: Logging | Network alerts (attackers, botnet connections, and malicious URLs seen in sniffer mode) | 4.0.0 or earlier | IDPS `SRG-NET-000392-IDPS-00214`; IDPS `SRG-NET-000390-IDPS-00212`; IDPS `SRG-NET-000391-IDPS-00213`; IDPS `SRG-NET-000113-IDPS-00013` | GUI: Log & Report > Network Alerts |
| Core: Alerts | Email notifications for detected malware and scheduled PDF reports | 4.0.0 or earlier | IDPS `SRG-NET-000249-IDPS-00222`; IDPS `SRG-NET-000392-IDPS-00219`; IDPS `SRG-NET-000392-IDPS-00214` | GUI: System > Mail Server (notification email to the ISSO and ISSM for Malicious and High Risk ratings) |
| Core: Alerts | SNMP traps (CPU, memory, and disk use, interface changes, and detected malware) | 4.0.0 or earlier | IDPS `SRG-NET-000249-IDPS-00222`; NDM `SRG-APP-000357-NDM-000293` | GUI: System > SNMP (SNMP v3 Events: Malware is detected and Hard disk usage is high) |
| Core: Time and SNMP | System time and NTP synchronization (FortiGuard or one NTP server) | 4.0.0 or earlier | NDM `SRG-APP-000920-NDM-000320`; NDM `SRG-APP-000374-NDM-000299`; NDM `SRG-APP-000925-NDM-000330` | GUI: Dashboard > Status (System Information widget, System Time: synchronize with a DoD NTP server) |
| Core: Time and SNMP | SNMPv3 users (authentication and privacy) | 4.0.0 or earlier | NDM `SRG-APP-000395-NDM-000310`; NDM `SRG-APP-000412-NDM-000331` | GUI: System > SNMP (Security Level: Encryption and authentication, with SHA1 and AES) |
| Core: Time and SNMP | SNMP v1 and v2c communities | 4.0.0 or earlier | NDM `SRG-APP-000395-NDM-000310`; NDM `SRG-APP-000142-NDM-000245` | GUI: System > SNMP (no v1 or v2c communities) |
| Core: System integrity | Firmware upgrades (web UI, and fw-upgrade over SCP, FTP, or HTTPS) | 4.0.0 or earlier | NDM `SRG-APP-000457-NDM-000352`; NDM `SRG-APP-001035-NDM-000340`; NDM `SRG-APP-000131-NDM-000243`; NDM `SRG-APP-000378-NDM-000302` | `fw-upgrade -b -tscp -s<SERVER> -u<USER> -f<IMAGE_PATH>` (compare the image checksum with the Fortinet support site first) |
| Core: System integrity | FortiGuard updates of antivirus signatures, engines, and AI models | 4.0.0 or earlier | IDPS `SRG-NET-000246-IDPS-00205`; IDPS `SRG-NET-000251-IDPS-00178`; IDPS `SRG-NET-000019-IDPS-00187` | GUI: System > FortiGuard (automatic updates from FDN, or Upload Package File on units without FDN access) |
| Core: System integrity | Configuration backup and restore through a remote server (CLI) | 4.0.0 or earlier | NDM `SRG-APP-000516-NDM-000340` | `backup-sysconf -s<SERVER> -tscp -u<USER> -f<FILE_PATH>` (after every change) |
| Core: System integrity | Configuration backup encryption passphrase | 4.0.0 or earlier | NDM `SRG-APP-000516-NDM-000340`; NDM `SRG-APP-000231-NDM-000271` | `set-cfg-backup-key -s` (a passphrase of the organization's own, not the default key) |
| Core: High availability | HA cluster of primary, secondary, and worker nodes (load balancing and failover) | 4.0.0 or earlier | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | `hc-settings -sc -tN` (standalone unit, if no cluster is used) |
| Core: High availability | Encryption of traffic between cluster members | 4.0.0 or earlier | NDM `SRG-APP-000231-NDM-000271`; NDM `SRG-APP-000412-NDM-000331` | `hc-primary -sg -e` (on the primary node; the cluster protocol can fall back to plain text) |
| Core: Detection | Antivirus, static, and dynamic (VM) scanning of files and URLs | 4.0.0 or earlier | IDPS `SRG-NET-000248-IDPS-00206`; IDPS `SRG-NET-000228-IDPS-00196`; IDPS `SRG-NET-000249-IDPS-00176` | GUI: Scan Policy and Object > Scan Profile |
| Core: Detection | Scan profiles (file types in the job queue and their VM associations) | 4.0.0 or earlier | IDPS `SRG-NET-000228-IDPS-00196`; IDPS `SRG-NET-000248-IDPS-00206` | GUI: Scan Policy and Object > Scan Profile (VM Association for every file type the site receives) |
| Core: Detection | FortiGuard sandboxing prefilter by file type | 4.0.0 or earlier | IDPS `SRG-NET-000228-IDPS-00196` | `sandboxing-prefilter -l` (files that pass the prefilter skip the VM scan; enable it only for file types where that is acceptable) |
| Core: Detection | VM images (default and optional VMs) and clone numbers | 4.0.0 or earlier | IDPS `SRG-NET-000228-IDPS-00196` | GUI: Scan Policy and Object > VM Settings |
| Core: Detection | VM Internet access through port3, and the simulated network (SIMNET) | 4.0.0 or earlier | IDPS `SRG-NET-000715-IDPS-00120` | `vm-internet -s -g<GATEWAY> -d<DNS_SERVER>` (port3 on an isolated network behind a firewall, with no access to protected subnets) |
| Core: Detection | Allowlist and blocklist of files and URLs | 4.0.0 or earlier | IDPS `SRG-NET-000249-IDPS-00176`; IDPS `SRG-NET-000228-IDPS-00196` | GUI: Scan Policy and Object > Allowlist/Blocklist (review the allowlist regularly) |
| Core: Detection | YARA rules | 4.0.0 or earlier | IDPS `SRG-NET-000228-IDPS-00196`; IDPS `SRG-NET-000019-IDPS-00187` | GUI: Scan Policy and Object > YARA Rules |
| Core: Detection | Web category risk ratings for URLs | 4.0.0 or earlier | IDPS `SRG-NET-000019-IDPS-00019` | GUI: Scan Policy and Object > Web Category |
| Core: Detection | Customized rating of scan results | 4.0.0 or earlier | IDPS `SRG-NET-000228-IDPS-00196` | GUI: Scan Policy and Object > Customized Rating |
| Core: Detection | On-demand file and URL submission (web UI and JSON API) | 4.0.0 or earlier | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Core: Detection | Job archive to a network share | 4.0.0 or earlier | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | GUI: Scan Policy and Object > Job Archive (leave it disabled unless needed; archived samples are live malware) |
| Core: Fabric integration | Device mode (files from FortiGate, FortiMail, FortiWeb, FortiClient, and other devices over OFTP) | 4.0.0 or earlier | IDPS `SRG-NET-000248-IDPS-00206`; IDPS `SRG-NET-000383-IDPS-00208` | GUI: Security Fabric > Device |
| Core: Fabric integration | Authorization of new devices (manual or automatic) | 4.0.0 or earlier | NDM `SRG-APP-000038-NDM-000213`; IDPS `SRG-NET-000383-IDPS-00208` | `device-authorization -m -o` (every new device authorized by an administrator) |
| Core: Fabric integration | Malware and URL packages for FortiGate and other devices | 4.0.0 or earlier | IDPS `SRG-NET-000249-IDPS-00176`; IDPS `SRG-NET-000249-IDPS-00221`; IDPS `SRG-NET-000383-IDPS-00208` | GUI: Threat Intelligence > IOC Packages |
| Core: Fabric integration | Adapters (ICAP, MTA, BCC, and Carbon Black) | 4.0.0 or earlier | IDPS `SRG-NET-000248-IDPS-00206`; IDPS `SRG-NET-000383-IDPS-00208` | GUI: Security Fabric > Adapter |
| Core: Fabric integration | Network share scans and quarantine | 4.0.0 or earlier | IDPS `SRG-NET-000249-IDPS-00221`; IDPS `SRG-NET-000248-IDPS-00206` | GUI: Security Fabric > Network Share (and Security Fabric > Quarantine) |
| Core: Fabric integration | Sniffer mode (files and network alerts from spanned switch ports) | 4.0.0 or earlier | IDPS `SRG-NET-000390-IDPS-00212`; IDPS `SRG-NET-000391-IDPS-00213`; IDPS `SRG-NET-000248-IDPS-00206`; IDPS `SRG-NET-000392-IDPS-00214` | GUI: Security Fabric > Sniffer |
| Core: Threat data | Upload of malicious and suspicious file information to the FortiSandbox Community Cloud | 4.0.0 or earlier | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | `upload-settings -tuploadcloud -d` (unless sharing with Fortinet is approved) |
| Core: Threat data | Retention of original files and job traces | 5.2.2 or earlier | NDM `SRG-APP-000231-NDM-000271` | GUI: System > Settings (Data Storage: delete original files and job traces after the organization's retention period) |
| Core: Threat data | Download of original files and job packages | 4.0.0 or earlier | NDM `SRG-APP-000231-NDM-000271` | GUI: System > Admin Profiles (Download Original File only in profiles that need it) |
| Core: Threat data | Job visibility (Super Admin sees all jobs; other administrators see their own jobs or those of their devices) | 4.0.0 or earlier | NDM `SRG-APP-000231-NDM-000271`; NDM `SRG-APP-000033-NDM-000212` | — |
| Core: Troubleshooting | Diagnose, test-network, tac-report, and tcpdump commands | 4.0.0 or earlier | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Core: Troubleshooting | Factory reset, configuration reset, and database cleanup | 4.0.0 or earlier | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — (factory-reset before the unit leaves service) |
| Dashboard | Redesigned menu layout and dashboard (Connectivity and Services, Scan Performance, Licenses, and System Resources widgets; Favorites menu) | 4.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| HA cluster | Cluster Management pages for administering an HA cluster | 4.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Updates | Reset of the FortiGuard settings to default | 4.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Licensing | One upload for VM, Microsoft Windows, and Microsoft Office licenses | 4.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Threat data | Warning before downloading samples or other malicious content | 4.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | Serial number or hostname in the browser tab and the CLI prompt | 4.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Public cloud | Custom VMs in a separate Virtual Private Cloud on AWS | 4.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Management access | Separate port for the JSON REST API | 4.0.0 and later | NDM `SRG-APP-000880-NDM-000290` | `set api-port <PORT>` (a port on the management network; the API port accepts no web UI logins) |
| Updates | Hostname in the HTTP CONNECT request of the FortiGuard proxy | 4.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Logging | Secured logging to FortiAnalyzer | 4.0.0 and later | NDM `SRG-APP-000515-NDM-000325`; NDM `SRG-APP-000119-NDM-000236`; IDPS `SRG-NET-000334-IDPS-00191` | GUI: Log & Report > Log Servers (Type FortiAnalyzer) |
| API | LDAP settings through the JSON RPC API (all settings and advanced fields) | 4.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Scan engine | Adaptive Scan Profile (the scan profile adjusts to the submission) | 4.0.0 and later | IDPS `SRG-NET-000228-IDPS-00196` | `sandboxing-adaptive -l` (not all models support it) |
| Scan engine | VM Scan Ratio (VM use balanced by system load) | 4.0.0 and later | IDPS `SRG-NET-000228-IDPS-00196` | `sandboxing-ratio -l` (a ratio of 100 scans every job in the VMs) |
| Dynamic analysis | PEXBox code emulation module for Windows malware | 4.0.0 and later | IDPS `SRG-NET-000228-IDPS-00196` | — (no setting in the 5.2.2 CLI Reference) |
| Scan engine | Rating Engine Plus (cloud rating) | 4.0.0 and later | IDPS `SRG-NET-000228-IDPS-00196` | — |
| Scan engine | Reset of the prescan configuration to default | 4.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Dynamic analysis | Deletion of a VM job during an interactive scan | 4.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Scan engine | Larger files (new file size limit and prescan settings) | 4.0.0 and later | IDPS `SRG-NET-000248-IDPS-00206` | `filesize-limit -l` (limits that cover the largest files the sources send) |
| URL analysis | Scan and rating of websites that do not return 200 OK | 4.0.0 and later | IDPS `SRG-NET-000228-IDPS-00196` | — |
| Device integration | FortiMail verdict returned as soon as known malware is detected | 4.0.0 and later | IDPS `SRG-NET-000249-IDPS-00176` | — |
| Static analysis | AI mode enabled by default | 4.0.0 and later | IDPS `SRG-NET-000228-IDPS-00196` | — (no setting in the 5.2.2 CLI Reference) |
| Dynamic analysis | Several VM types for the same file or URL | 4.0.0 and later | IDPS `SRG-NET-000228-IDPS-00196` | GUI: Scan Policy and Object > Scan Profile (VM Association) |
| Alerts | System health check alerts when a threshold is reached | 4.0.0 and later | NDM `SRG-APP-000357-NDM-000293` | GUI: System > Mail Server (Send scheduled system resource status report, with CPU, RAM, and disk thresholds) |
| Time | FortiGuard as an NTP server option | 4.0.0 and later | NDM `SRG-APP-000920-NDM-000320` | GUI: Dashboard > Status (prefer a DoD NTP server to FortiGuard) |
| HA cluster | Cluster IP on an aggregate interface | 4.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Platform | Rescue mode on Hyper-V | 4.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Platform | FortiSandbox 3000F | 4.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Platform | LACP interfaces for health check and the MTA adapter | 4.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Backup | Configuration backup file named after the hostname | 4.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Scan engine | One Sandbox Rating Engine for Windows, Android, and Linux | 4.0.0 and later | IDPS `SRG-NET-000228-IDPS-00196` | — |
| Reports | Redesigned job PDF report (extracted URLs, VM images, antivirus signature, BCC job details, system information, and settings) | 4.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Logging | Malware category field in the job event logs | 4.0.0 and later | IDPS `SRG-NET-000074-IDPS-00059` | — |
| Reports | Detected malware name in the Suspicious Indicator Detail table | 4.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Reports | VM category (Default, Optional, or Custom) in the report | 4.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Reports | Submit condition (scan profile or scan ratio) in the job details report | 4.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Logging | Logging of scan performance | 4.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| CLI | prescan-config command for the prescan module | 4.0.0 and later | IDPS `SRG-NET-000248-IDPS-00206` | `prescan-config -l` |
| CLI | tac-report runs the diagnose commands, including 4.0 features | 4.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| CLI | test-network checks network speed and Community Cloud query and submission | 4.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| CLI | status shows the file system state of the boot and data disks | 4.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| CLI | admin-pwd-reset renamed reset-admin-pwd | 4.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | Scan Profile page layout | 4.0.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Device integration | FortiAI integration (FortiNDR from 4.2.0, with network response detection) | 4.0.1+; 4.2.0+ | IDPS `SRG-NET-000383-IDPS-00208` | GUI: Security Fabric > FortiNDR |
| Dynamic analysis | Internal VM scan timeout adjusted for detection | 4.0.1 and later | IDPS `SRG-NET-000228-IDPS-00196` | — |
| Public cloud | Parallel scan on AWS and Azure | 4.0.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Scan engine | On-demand scans forced to the VM continue even when the sample is allowlisted | 4.0.1 and later | IDPS `SRG-NET-000228-IDPS-00196` | — |
| Scan engine | MD5 and SHA1 entries in the custom allowlist and blocklist | 4.0.1 and later | IDPS `SRG-NET-000249-IDPS-00176` | GUI: Scan Policy and Object > Allowlist/Blocklist |
| Licensing | Perpetual custom VM license | 4.0.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Alerts | SNMP trap for contract and license expiration | 4.0.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Logging | Encrypted communication with syslog servers | 4.0.1 and later | NDM `SRG-APP-000515-NDM-000325`; NDM `SRG-APP-000119-NDM-000236`; IDPS `SRG-NET-000334-IDPS-00191` | GUI: Log & Report > Log Servers (Secure Connection) |
| Logging | Event log for the system health check | 4.0.1 and later | NDM `SRG-APP-000357-NDM-000293` | — |
| Logging | Logging rate and resilience to FortiAnalyzer | 4.0.1 and later | NDM `SRG-APP-000515-NDM-000325` | — |
| CLI | Aggregate interface IP address set in the CLI | 4.0.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| API | Disk and inode use in the get-system-status API response | 4.0.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| CLI | Command to cancel processing jobs | 4.0.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Dashboard | Performance widgets | 4.0.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | Fortinet logo and firmware version in the web UI | 4.0.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Scan engine | False positive and false negative submissions for URLs | 4.0.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Threat data | Option to leave the password out of downloaded job files and packages | 4.0.2 and later | NDM `SRG-APP-000231-NDM-000271` | GUI: System > Settings (keep a customized password on original files and no readme file with the password) |
| Public cloud | Instance types with Elastic Network Adapter on AWS | 4.0.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| ICAP adapter | ICAP PUT method | 4.0.2 and later | IDPS `SRG-NET-000248-IDPS-00206` | GUI: Security Fabric > Adapter |
| Static analysis | YARA engine upgrade with the Magic module | 4.0.2 and later | IDPS `SRG-NET-000228-IDPS-00196` | GUI: Scan Policy and Object > YARA Rules |
| Public cloud | Hot-standby VMs on AWS and Azure | 4.0.2+; 4.2.0+ | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| System | jQuery library upgrade | 4.0.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Public cloud | Hard disk expansion on AWS and Azure (resize-hd) | 4.0.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Dashboard | Scan Performance page with historical use | 4.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| VMs | Custom VM changes on FortiSandbox | 4.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | Neutrino GUI framework | 4.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Dashboard | FortiAnalyzer on the Connectivity widget | 4.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Dashboard | FortiNDR on the Connectivity widget | 4.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Dashboard | Last 7 days in the System Resources Usage widget | 4.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Reports | Recorded video link on the Job Detail page | 4.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Inline block | Inline blocking with FortiOS 7.2 (FortiGate holds the file until the verdict) | 4.2.0 and later | IDPS `SRG-NET-000249-IDPS-00176`; IDPS `SRG-NET-000229-IDPS-00163` | GUI: Security Fabric > Device (Inline Block on each authorized FortiGate) |
| ICAP adapter | Several ICAP adapter profiles for multi-tenancy | 4.2.0 and later | IDPS `SRG-NET-000248-IDPS-00206` | GUI: Security Fabric > Adapter |
| ICAP adapter | Hold option for ICAP adapter deployments | 4.2.0 and later | IDPS `SRG-NET-000249-IDPS-00176` | GUI: Security Fabric > Adapter (hold the file until the verdict) |
| API | Aggregate interfaces through JSON RPC | 4.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| API | Download of macro content through JSON RPC | 4.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| API | False positive and false negative marking through JSON RPC, with automatic submission to Fortinet | 4.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Sniffer | TCP reset (TCP RST) of sessions with suspicious files, URLs, and network alerts in sniffer mode | 4.2.0+; 4.4.0+ | IDPS `SRG-NET-000249-IDPS-00176`; IDPS `SRG-NET-000018-IDPS-00018` | GUI: Security Fabric > Sniffer (TCP RST for file-based and network alert detection) |
| API | System resource check through the API | 4.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| URL analysis | Configurable Internet browser for dynamic scans | 4.2.0 and later | IDPS `SRG-NET-000228-IDPS-00196` | — |
| Dynamic analysis | Pipeline Scan Mode (one VM instance scans several jobs; URLs from 4.4.3) | 4.2.0+; 4.4.3+ | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | `sandboxing-pipeline -d` (the default) |
| Scan engine | Rating Engine Service mode | 4.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Dynamic analysis | One tracer engine for Windows, Android, and Linux | 4.2.0 and later | IDPS `SRG-NET-000228-IDPS-00196` | — |
| Dynamic analysis | Resilient log tracking in dynamic analysis | 4.2.0 and later | IDPS `SRG-NET-000228-IDPS-00196` | — |
| Email adapters | Faster email relay with the MTA adapter | 4.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| URL analysis | Similar URLs whose payload has changed | 4.2.0 and later | IDPS `SRG-NET-000228-IDPS-00196` | — |
| Dynamic analysis | Minimum dynamic scan timeout of 30 seconds on high-end models | 4.2.0 and later | IDPS `SRG-NET-000228-IDPS-00196` | — |
| HA cluster | Warning event for system time differences in an HA cluster | 4.2.0 and later | NDM `SRG-APP-000920-NDM-000320` | — |
| Backup | Configuration backup, restore, and revisions in the web UI | 4.2.0 and later | NDM `SRG-APP-000516-NDM-000340` | GUI: System > System Recovery (Remote Backup on a schedule) |
| System | OpenSSL library upgrade | 4.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Public cloud | Custom Linux VMs on public cloud | 4.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Reports | Customizable reports (white labeling) | 4.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Logging | Submit Time, Rated By, and File Type fields in FortiAnalyzer logs | 4.2.0 and later | IDPS `SRG-NET-000074-IDPS-00059`; IDPS `SRG-NET-000075-IDPS-00060` | — |
| Reports | Rated By names in the job reports | 4.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Logging | Periodic scan statistics logs to FortiAnalyzer | 4.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Logging | Periodic system resource logs to FortiAnalyzer | 4.2.0 and later | NDM `SRG-APP-000357-NDM-000293` | — |
| Inline block | device-authorization option to enable or disable inline blocking on FortiGate | 4.2.0 and later | IDPS `SRG-NET-000249-IDPS-00176` | GUI: Security Fabric > Device (the 5.2.2 device-authorization command has no inline block option) |
| CLI | test-network checks FortiAnalyzer, Cloud VM, and public cloud connectivity | 4.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| CLI | show lists the HA cluster external IP address | 4.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| CLI | tac-report updated for the 4.2.0 features | 4.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Threat data | device-clean-pdf (job PDF of clean jobs sent to the requesting device) | 4.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | `device-clean-pdf -d` (the default; a template PDF is sent) |
| Dashboard | Notice on the Community Cloud icon when community submission is disabled | 4.2.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | Tooltip on the VM clone update icon | 4.2.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Licensing | One license upload link on hardware units | 4.2.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | French and Japanese translations of new labels and messages | 4.2.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Management access | Up to 50 trusted hosts for web UI logins | 4.2.1 and later | NDM `SRG-APP-000408-NDM-000314`; NDM `SRG-APP-000038-NDM-000213` | GUI: System > Administrators (Restrict login to trusted host) |
| Network share | Network share scans of Microsoft Azure Blob Storage | 4.2.1 and later | IDPS `SRG-NET-000248-IDPS-00206` | GUI: Security Fabric > Network Share |
| Device integration | Device registration before any VM is configured | 4.2.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| API | JSON API for the VM scan timeout of non-executable files | 4.2.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| VMs | Windows Cloud VM service on appliances | 4.2.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — (cloud VMs scan files in Fortinet's cloud; use them only if approved) |
| Threat data | Upload of detection statistics (summary and details) to FortiGuard | 4.2.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | `upload-settings -tuploadstats -d` (the default) |
| Inline block | Result caching for inline block | 4.2.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Scan engine | Fault tolerance of the scan engine | 4.2.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Inline block | Duplicate submissions in inline block | 4.2.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Dynamic analysis | Detection of a Windows blue screen (BSOD) | 4.2.1 and later | IDPS `SRG-NET-000228-IDPS-00196` | — |
| Scan engine | Not Applied and Unknown options in Customized Rating for timeouts and encrypted files | 4.2.1 and later | IDPS `SRG-NET-000228-IDPS-00196` | GUI: Scan Policy and Object > Customized Rating |
| URL analysis | Cloud query of websites on the FortiGuard allowlist and blocklist | 4.2.1 and later | IDPS `SRG-NET-000019-IDPS-00019` | — |
| Licensing | Licensing logic for additional licenses | 4.2.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Licensing | Office 2019 upgrade license | 4.2.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Platform | FSA-VM00 as a dispatcher | 4.2.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Reports | Clean behavior left out of the job report | 4.2.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Logging | FQDN for log servers | 4.2.1 and later | NDM `SRG-APP-000516-NDM-000350` | GUI: Log & Report > Log Servers |
| Reports | FortiWeb http_host and session_id in the job report | 4.2.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Reports | MTA adapter message ID in the job report | 4.2.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Reports | Web browser in the job report | 4.2.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| CLI | tac-report shows diagnose-sys-perf for more time ranges | 4.2.3 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| CLI | vm-license shows more license information | 4.2.3 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Dashboard | User-defined file type groups in the File Statistics widget | 4.2.3 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| API | REST API query of the pending job count | 4.2.3 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Sniffer | Replacement message in sniffer mode when TCP reset is enabled | 4.2.3 and later | IDPS `SRG-NET-000249-IDPS-00176` | GUI: Security Fabric > Sniffer |
| Scan engine | CSV files in the Microsoft Office scan profile group | 4.2.3 and later | IDPS `SRG-NET-000248-IDPS-00206` | GUI: Scan Policy and Object > Scan Profile |
| Network share | Network share scans of 10,000 files (conserve mode) | 4.2.3 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| VMs | More VM memory on the VM00, 500F, and 1000F | 4.2.3 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| VMs | Optional VM WIN10O19V1 (Windows 10 with Office 2019) | 4.2.3 and later | IDPS `SRG-NET-000228-IDPS-00196` | GUI: Scan Policy and Object > VM Settings |
| Management access | Login disclaimer on SSH sessions | 4.2.3 and later | NDM `SRG-APP-000068-NDM-000215`; NDM `SRG-APP-000069-NDM-000216` | GUI: System > Login Disclaimer |
| ICAP adapter | application/octet-stream in ICAP request mode | 4.2.4+; 4.4.0+ | IDPS `SRG-NET-000248-IDPS-00206` | GUI: Security Fabric > Adapter |
| VMs | Windows 10 2021 LTSC VM with Office 2021 (WIN10LTSCO21V1) | 4.2.5+; 4.4.1+ | IDPS `SRG-NET-000228-IDPS-00196` | GUI: Scan Policy and Object > VM Settings |
| VMs | Windows 10 2021 LTSC VM with Office 2019 (WIN10LTSCO19V1) | 4.2.6+; 4.4.2+ | IDPS `SRG-NET-000228-IDPS-00196` | GUI: Scan Policy and Object > VM Settings |
| Device integration | FortiManager 7.6.0 | 4.2.8+; 4.4.7+ | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| VMs | Custom VM upload and update in the web UI | 4.4.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | Reorganized System and Scan Profile settings | 4.4.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | Log & Report Settings page | 4.4.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Dashboard | System Resource widget | 4.4.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | Adjustable columns on the File and URL On Demand pages | 4.4.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | Filtering, sorting, and Last Seen column on the Device and FortiClient pages | 4.4.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | VM Settings page usability and status indicators | 4.4.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| VMs | Installed applications list (meta information) for custom VMs | 4.4.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | Windows and macOS cloud VMs combined, with separate local and remote key counts | 4.4.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | Admin Profile page layout | 4.4.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | ICAP adapter page labels | 4.4.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Dashboard | 0-day detection statistics in the Scan Performance widget | 4.4.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Inline block | Inline Block setting on the device page | 4.4.0 and later | IDPS `SRG-NET-000249-IDPS-00176` | GUI: Security Fabric > Device |
| Authentication | Test connection for LDAP remote administrators | 4.4.0 and later | NDM `SRG-APP-000516-NDM-000336` | GUI: System > LDAP Servers |
| Logging | Port number for FortiAnalyzer log servers | 4.4.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Dynamic analysis | VM Interaction (interactive on-demand scans) | 4.4.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | GUI: System > Admin Profiles (Allow On-Demand Scan Interaction only in profiles that need it) |
| HA cluster | Auto-refresh of the Cluster Management pages | 4.4.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| HA cluster | Refresh button on the HA cluster Job Summary page | 4.4.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | Renamed Scan Timeout labels | 4.4.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Platform | FortiSandbox on Oracle Cloud Infrastructure (OCI) | 4.4.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| ICAP adapter | Imported certificates for the ICAP adapter | 4.4.0 and later | NDM `SRG-APP-000516-NDM-000344`; IDPS `SRG-NET-000383-IDPS-00208` | GUI: System > Certificates (a DoD-issued certificate for ICAP over SSL) |
| ICAP adapter | Editable default profile with several ICAP profiles | 4.4.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Network share | SMB 3.1.1 for network share scans | 4.4.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| ICAP adapter | ICAP return code 202 (submission accepted) | 4.4.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Management access | TLS 1.3 | 4.4.0 and later | NDM `SRG-APP-000412-NDM-000331`; NDM `SRG-APP-000172-NDM-000259` | `set-tlsver -l`; `device-ssl -l` |
| Anti-phishing | Real-Time Anti-Phishing (RTAP) service for 0-day phishing sites | 4.4.0 and later | IDPS `SRG-NET-000019-IDPS-00019`; IDPS `SRG-NET-000228-IDPS-00196` | GUI: System > FortiGuard (Real-time Zero-Day Anti-Phishing Service Settings; subscription) |
| Network share | Prioritized network share scan jobs with user rights and groups | 4.4.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| URL analysis | QR code analysis of embedded URLs | 4.4.0 and later | IDPS `SRG-NET-000228-IDPS-00196` | `sandboxing-embeddedobj -l` (QR code extraction, type qr, is off by default; set -n to 1 or more to enable it) |
| Inline block | Configurable file type list for inline block scans | 4.4.0 and later | IDPS `SRG-NET-000248-IDPS-00206`; IDPS `SRG-NET-000249-IDPS-00176` | GUI: Security Fabric > Device |
| ICAP adapter | Hold for dynamic scans of ICAP submissions | 4.4.0 and later | IDPS `SRG-NET-000249-IDPS-00176` | GUI: Security Fabric > Adapter |
| VMs | Optional VM with Office 2021 | 4.4.0 and later | IDPS `SRG-NET-000228-IDPS-00196` | GUI: Scan Policy and Object > VM Settings |
| VMs | Windows 11 for dynamic scans | 4.4.0 and later | IDPS `SRG-NET-000228-IDPS-00196` | GUI: Scan Policy and Object > VM Settings |
| Static analysis | Installer-type archive files | 4.4.0 and later | IDPS `SRG-NET-000248-IDPS-00206` | — |
| VMs | CPU and memory settings for custom VMs (vm-customized parameters from 5.0.0) | 4.4.0+; 5.0.0+ | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| URL analysis | Embedded URL scanning enabled by default | 4.4.0 and later | IDPS `SRG-NET-000228-IDPS-00196` | `sandboxing-embeddedobj -l` (3 embedded URLs and 3 embedded files by default, up to 30) |
| URL analysis | DNS queries of URL scans through port3 | 4.4.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| URL analysis | Terrorism, URL Shortening, Crypto Mining, and Potentially Unwanted Program web filtering categories | 4.4.0 and later | IDPS `SRG-NET-000019-IDPS-00019` | GUI: Scan Policy and Object > Web Category |
| Static analysis | YARA engine 4.2.3 | 4.4.0 and later | IDPS `SRG-NET-000228-IDPS-00196` | — |
| URL analysis | Override ratings for URL categories such as Phishing | 4.4.0 and later | IDPS `SRG-NET-000019-IDPS-00019` | GUI: Scan Policy and Object > Web Category |
| Network share | Option to skip the placeholder file for quarantined network share files | 4.4.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Dynamic analysis | Scan timeout for executable files | 4.4.0 and later | IDPS `SRG-NET-000228-IDPS-00196` | GUI: Scan Policy and Object > Scan Profile (Advanced tab) |
| Public cloud | Custom Linux VMs on AWS | 4.4.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Dynamic analysis | Microsoft OneNote files | 4.4.0 and later | IDPS `SRG-NET-000248-IDPS-00206` | — |
| System | Self-check of configuration, connectivity, and services | 4.4.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Authentication | Single sign-on (SAML) for administrators | 4.4.0 and later | NDM `SRG-APP-000516-NDM-000336`; NDM `SRG-APP-000149-NDM-000247`; NDM `SRG-APP-000820-NDM-000170` | GUI: System > SAML SSO (an IdP that enforces DoD PKI) |
| System | Hardware status (temperature, fans, disks, and power supplies) in the MIB and the CLI | 4.4.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Platform | Effective Sandboxing Throughput raised 5 to 10 times | 4.4.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| System | Kernel, Python, OpenSSL, and Apache upgrades | 4.4.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Administrators | Administrator types for device groups and network share submissions (Netshare administrators and groups) | 4.4.0 and later | NDM `SRG-APP-000033-NDM-000212`; NDM `SRG-APP-000231-NDM-000271` | GUI: System > Netshare Groups |
| Network share | Database cleanup of network share scans by retention | 4.4.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Administrators | Deletion of the built-in admin account | 4.4.0 and later | NDM `SRG-APP-000148-NDM-000346` | `rename-admin -uadmin -n<NEW_NAME>` (then delete it in the web UI, or keep it as the account of last resort) |
| Reports | Job Details display settings and field names | 4.4.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Reports | Web filtering rating and redirected URL in URL scan job reports | 4.4.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Reports | MITRE ATT&CK version 11 in the Job Detail report | 4.4.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Logging | File type in the event log | 4.4.0 and later | IDPS `SRG-NET-000074-IDPS-00059` | — |
| Reports | Overflow VM indicator in the job details | 4.4.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Email adapters | Warning when MTA adapter email accounts exceed the license | 4.4.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| API | File submission from remote and network share paths through the API | 4.4.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| CLI | Low-level hard disk format that erases all data and keeps the default licenses | 4.4.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| CLI | Command to show the MTA queue | 4.4.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | Faster web page loading | 4.4.3 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | Automatic login to the CLI console in the web UI | 4.4.3 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | GUI: System > Admin Profiles (GUI Console only in profiles that need it) |
| GUI | Cloud VM region in the System Checklist | 4.4.3 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | Warning to keep the file and job retention settings the same | 4.4.3 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Scan engine | Limit of 30 archive passwords | 4.4.3 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | Source device and user filters on the job search page | 4.4.3 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | Tooltips for default ratings on the Web Category page | 4.4.3 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Device integration | New FortiWeb model | 4.4.3 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Public cloud | Network share scans on AWS in the Hong Kong region | 4.4.3 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| VMs | Windows 11 VMs with Office 2019 and with Office 2021 | 4.4.3 and later | IDPS `SRG-NET-000228-IDPS-00196` | GUI: Scan Policy and Object > VM Settings |
| VMs | Custom VMs with Windows 11 | 4.4.3+; 5.0.0+ | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| VMs | Ubuntu 18 optional VM (Ubuntu18V5) | 4.4.3 and later | IDPS `SRG-NET-000228-IDPS-00196` | GUI: Scan Policy and Object > VM Settings |
| Scan engine | Files of up to 30 GB | 4.4.3 and later | IDPS `SRG-NET-000248-IDPS-00206` | `filesize-limit -l` |
| Public cloud | Idle custom VM instances deallocated in hot standby | 4.4.3 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Anti-phishing | RTAP screenshots of URLs rated clean | 4.4.3 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Anti-phishing | More FortiGuard RTAP servers for redundancy | 4.4.3 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Anti-phishing | Proxy for the Real-Time Anti-Phishing service | 4.4.3 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| VMs | Default VM of the VM00 changed to WIN10LTSCO21V1 | 4.4.3 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Sniffer | Allowlist and blocklist overrides in sniffer mode | 4.4.3 and later | IDPS `SRG-NET-000249-IDPS-00176` | GUI: Scan Policy and Object > Allowlist/Blocklist |
| Platform | Firmware builds for GCP and OCI | 4.4.3 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Administrators | Password policy for local administrators (length, character types, expiration, and reuse) | 4.4.3 and later | NDM `SRG-APP-000164-NDM-000252`; NDM `SRG-APP-000166-NDM-000254`; NDM `SRG-APP-000167-NDM-000255`; NDM `SRG-APP-000168-NDM-000256`; NDM `SRG-APP-000169-NDM-000257`; NDM `SRG-APP-000860-NDM-000250` | GUI: System > Password Policy (Minimum password length 15, at least one of each character type, Allow password reuse off) |
| Authentication | Several LDAP and RADIUS users | 4.4.3 and later | NDM `SRG-APP-000516-NDM-000336`; NDM `SRG-APP-000153-NDM-000249` | GUI: System > Administrators |
| Public cloud | Premium disks on Azure for custom VMs | 4.4.3+; 5.0.0+ | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Administrators | Netshare users with Full Access can change their network share configuration | 4.4.3 and later | NDM `SRG-APP-000033-NDM-000212` | GUI: System > Admin Profiles |
| Logging | Event logs for the confirm-id command | 4.4.3 and later | NDM `SRG-APP-000343-NDM-000289` | — |
| System integrity | Proxy server for fw-upgrade | 4.4.3 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| CLI | More debug information in tac-report | 4.4.3 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| CLI | Grouping and order of the CLI commands | 4.4.3 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Management access | TLS cipher suites for administrative HTTPS and OFTP fabric connections | 4.4.3 and later | NDM `SRG-APP-000412-NDM-000331`; NDM `SRG-APP-000411-NDM-000330`; IDPS `SRG-NET-000383-IDPS-00208` | `device-ssl -j` (weak cipher suites and certificates refused, the default) |
| Updates | Engine package upload in the CLI for air-gapped units | 4.4.3 and later | IDPS `SRG-NET-000246-IDPS-00205` | `fw-upgrade -e -tscp -s<SERVER> -u<USER> -f<PACKAGE_PATH>` |
| Administrators | CLI command to create and delete administrator accounts (system-admin) | 4.4.3 and later | NDM `SRG-APP-000153-NDM-000249`; NDM `SRG-APP-000033-NDM-000212` | `system-admin -c -u<ADMIN> -fread-only -tradius -lr<RADIUS_SERVER> -t4<MGMT_SUBNET>` (a remote account with the narrowest profile and trusted hosts) |
| Dashboard | Historical data for the Scan Statistics widget | 4.4.4 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Public cloud | Nested VMs on Azure with local VMs | 4.4.4 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| System | File system upgrade for newer WIN10LTSC VMs | 4.4.4 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Anti-phishing | RTAP server list downloaded over port 443 | 4.4.4 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Reports | Option to leave screenshots out of PDF job reports | 4.4.4 and later | NDM `SRG-APP-000231-NDM-000271` | GUI: Log & Report > Customize Report (Print screenshot off for reports that leave the enclave) |
| Anti-phishing | Detailed reason for RTAP verdicts | 4.4.4 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Reports | Smaller job PDF reports | 4.4.4 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Inline block | Inline block policy with FortiProxy | 4.4.5 and later | IDPS `SRG-NET-000249-IDPS-00176` | GUI: Security Fabric > Device |
| ICAP adapter | Configurable ICAP service name | 4.4.6 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| ICAP adapter | New ICAP encodings and content types | 4.4.6 and later | IDPS `SRG-NET-000248-IDPS-00206` | GUI: Security Fabric > Adapter |
| Sniffer | Q-in-Q traffic in sniffer mode | 4.4.6+; 5.0.0+ | IDPS `SRG-NET-000390-IDPS-00212`; IDPS `SRG-NET-000391-IDPS-00213` | GUI: Security Fabric > Sniffer (Interface MTU) |
| Dynamic analysis | Customized ratings for application crashes during dynamic scans | 4.4.7+; 5.0.0+ | IDPS `SRG-NET-000228-IDPS-00196` | GUI: Scan Policy and Object > Customized Rating |
| Logging | Log of each VM rescan, with the job ID and the reason | 4.4.7+; 5.0.0+ | IDPS `SRG-NET-000113-IDPS-00013` | — |
| Dynamic analysis | Job configuration protection against detection evasion | 4.4.8+; 5.0.2+ | IDPS `SRG-NET-000228-IDPS-00196` | — |
| VMs | Redesigned VM Settings page for the Universal VM | 5.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Threat intelligence | Incident Assist page for SOC monitoring and investigation | 5.0.0 and later | IDPS `SRG-NET-000392-IDPS-00214` | GUI: Threat Intelligence > Incident Assist |
| Reports | Redesigned Job Detail page | 5.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Threat intelligence | Threat intelligence enrichment through the FortiGuard IOC service | 5.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Email adapters | Email Management page for email not delivered through the MTA adapter | 5.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Dynamic analysis | VM Interaction on Linux VMs | 5.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | GUI: System > Admin Profiles (Allow On-Demand Scan Interaction only in profiles that need it) |
| GUI | Option to hide clean and debug tracer logs on the Job Detail page | 5.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | GUI themes | 5.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | Latest web application framework for the GUI pages | 5.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Dashboard | System Dashboard content and layout | 5.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | Simplified On Demand submission page with advanced options | 5.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | VM Association page | 5.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | System Settings page (Alert Notification and VM External Network Access) | 5.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | Update status on the FortiGuard page | 5.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | Tree view design | 5.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Scan engine | False positive or false negative mark when submitting a job to FortiGuard | 5.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | Compressed-file icon on the job search page | 5.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Reports | Tracer log download for Linux files | 5.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Network share | Network share scans of Google Cloud Storage | 5.0.0 and later | IDPS `SRG-NET-000248-IDPS-00206` | GUI: Security Fabric > Network Share |
| Network share | Network share scans of Microsoft OneDrive and SharePoint | 5.0.0 and later | IDPS `SRG-NET-000248-IDPS-00206` | GUI: Security Fabric > Network Share |
| Network share | Network share scans of SFTP sites | 5.0.0 and later | IDPS `SRG-NET-000248-IDPS-00206` | GUI: Security Fabric > Network Share |
| Public cloud | Nested VMs on AWS, Azure, GCP, and OCI | 5.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Public cloud | Azure client ID instead of an email address | 5.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Email adapters | Custom certificates for the MTA and BCC adapters | 5.0.0 and later | NDM `SRG-APP-000516-NDM-000344`; IDPS `SRG-NET-000383-IDPS-00208` | GUI: Security Fabric > Adapter (a DoD-issued certificate) |
| Static analysis | PAIX AI engine for 0-day malware (Windows executables, Android, Office, and PDF) | 5.0.0 and later | IDPS `SRG-NET-000228-IDPS-00196`; IDPS `SRG-NET-000246-IDPS-00205` | GUI: System > FortiGuard (AI Engine and Model, updated with the Advanced Subscription) |
| Dynamic analysis | Application-level behavioral tracking | 5.0.0 and later | IDPS `SRG-NET-000228-IDPS-00196` | — |
| Static analysis | Optical character recognition (OCR) of images | 5.0.0 and later | IDPS `SRG-NET-000228-IDPS-00196` | `sandboxing-embeddedobj -l` (OCR, type ocr, is off by default; set -n to 1 or more to enable it) |
| VMs | Android VM for APK files | 5.0.0 and later | IDPS `SRG-NET-000228-IDPS-00196` | GUI: Scan Policy and Object > VM Settings |
| Static analysis | Extraction of files embedded in Office and PDF files | 5.0.0 and later | IDPS `SRG-NET-000248-IDPS-00206`; IDPS `SRG-NET-000228-IDPS-00196` | `sandboxing-embeddedobj -l` (3 embedded URLs and 3 embedded files by default, up to 30) |
| Public cloud | VM recording with nested VMs | 5.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| URL analysis | QR code images in FortiMail URL submissions | 5.0.0 and later | IDPS `SRG-NET-000228-IDPS-00196` | — |
| Scan engine | Faster aggregation of archive results | 5.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| URL analysis | Dynamic scan skipped for URLs rated High Risk by a customized category | 5.0.0 and later | IDPS `SRG-NET-000019-IDPS-00019` | GUI: Scan Policy and Object > Web Category |
| Scan engine | Up to 30 passwords for PDF and Office files in the scan profile | 5.0.0 and later | IDPS `SRG-NET-000248-IDPS-00206` | GUI: Scan Policy and Object > Scan Profile |
| Network share | Network share scan performance | 5.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Scan engine | Job result caching | 5.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Static analysis | New file types (.vbe, .ics, .vcs, .pub, .udf, and ISO in UDF 2.5) | 5.0.0 and later | IDPS `SRG-NET-000248-IDPS-00206` | — |
| Static analysis | UTF-8 encoded attachments in MIME email | 5.0.0 and later | IDPS `SRG-NET-000248-IDPS-00206` | — |
| Email adapters | Password extraction from email submitted through the BCC adapter | 5.0.0 and later | IDPS `SRG-NET-000248-IDPS-00206` | — |
| URL analysis | Scan of script files downloaded by URL jobs | 5.0.0 and later | IDPS `SRG-NET-000228-IDPS-00196` | — |
| Static analysis | Trusted-vendor check of archive files | 5.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Network share | Options to skip unchanged files | 5.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| System | More disk capacity for job retention | 5.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| System | Database scalability and reliability | 5.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| HA cluster | SSL certificates for communication between cluster nodes | 5.0.0 and later | NDM `SRG-APP-000231-NDM-000271`; NDM `SRG-APP-000412-NDM-000331` | `hc-primary -sg -e` |
| System | FortiSandbox OS software upgrade | 5.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Public cloud | AWS and Azure SDK update for newer regions | 5.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Public cloud | Serial number as the remote access password of interactive custom VMs | 5.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Device integration | TLS 1.3 by default for device connections | 5.0.0 and later | NDM `SRG-APP-000412-NDM-000331`; IDPS `SRG-NET-000383-IDPS-00208` | `device-ssl -g` (the default) |
| Public cloud | Availability zones for nested VMs on Azure | 5.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| System | Automatic file system conversion for newer optional VMs | 5.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| VMs | HTTP CONNECT and SOCKS5 proxy for cloud VMs | 5.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| VMs | HTTP CONNECT proxy for VM network access | 5.0.0 and later | IDPS `SRG-NET-000715-IDPS-00120` | GUI: System > Settings (VM External Network Access, Use Proxy) |
| ICAP adapter | Limit of 32 ICAP profiles | 5.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Reports | AI-based threat summary | 5.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Reports | Option to hide debug tracer logs in PDF reports | 5.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Reports | Five cover page designs for the Job Detail PDF report | 5.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Logging | Kernel panic, segmentation fault, and out-of-memory events in the system event log | 5.0.0 and later | IDPS `SRG-NET-000236-IDPS-00170`; NDM `SRG-APP-000095-NDM-000225` | — |
| Logging | Daemon restart events in the system event log | 5.0.0 and later | IDPS `SRG-NET-000236-IDPS-00170` | — |
| Reports | Engine versions in reports and on the Job Detail page | 5.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Threat data | Serial number sent with files submitted to the Community Cloud | 5.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | `upload-settings -tuploadcloud -d` |
| Email adapters | From and To fields for email submitted through the BCC adapter | 5.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Threat intelligence | Sharing of IOCs through STIX/TAXII packages and servers | 5.0.0 and later | IDPS `SRG-NET-000383-IDPS-00208` | GUI: Threat Intelligence > IOC Packages (STIX/TAXII Integration only with approved servers) |
| CLI | More debug output in tac-report and test-network (HA cluster, web category overrides, and proxy) | 5.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| CLI | Database status in the status command | 5.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| CLI | File system type in the debug commands | 5.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Reports | Job Details report page (Info labels, icons, and tree view panel) | 5.0.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| VMs | Windows 11 IoT Enterprise LTSC VM with Office 2021 for AWS and Azure | 5.0.1 and later | IDPS `SRG-NET-000228-IDPS-00196` | GUI: Scan Policy and Object > VM Settings |
| Licensing | Windows-only license and Windows activation SKU | 5.0.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Network share | Scans of SharePoint files | 5.0.2 and later | IDPS `SRG-NET-000248-IDPS-00206` | GUI: Security Fabric > Network Share |
| HA cluster | Standby secondary node that processes no jobs | 5.0.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| URL analysis | Dynamic scans of URLs embedded in QR codes | 5.0.2 and later | IDPS `SRG-NET-000228-IDPS-00196` | `sandboxing-embeddedobj -l` (QR code extraction, type qr, is off by default; set -n to 1 or more to enable it) |
| Threat data | Option to keep the job folder of clean jobs | 5.0.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Device integration | Long URLs submitted by FortiMail | 5.0.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Static analysis | Extraction and scanning of Microsoft Outlook PST files | 5.0.2+; 5.2.0+ | IDPS `SRG-NET-000248-IDPS-00206` | — |
| URL analysis | URLs extracted from .eml files from all input sources | 5.0.2 and later | IDPS `SRG-NET-000228-IDPS-00196` | — |
| URL analysis | File downloads from Google Drive | 5.0.2 and later | IDPS `SRG-NET-000248-IDPS-00206` | — |
| Static analysis | multipart/related content type | 5.0.2 and later | IDPS `SRG-NET-000248-IDPS-00206` | — |
| Scan engine | Custom rating of document files | 5.0.2 and later | IDPS `SRG-NET-000228-IDPS-00196` | GUI: Scan Policy and Object > Customized Rating |
| Static analysis | File typing of PowerShell (PS1) files | 5.0.2 and later | IDPS `SRG-NET-000248-IDPS-00206` | — |
| Static analysis | AI engine 05000.00025 released as GA | 5.0.2 and later | IDPS `SRG-NET-000246-IDPS-00205` | — |
| GUI | Redesigned GUI console | 5.0.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | Malware Package page | 5.0.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Authentication | Import of IdP metadata on the SAML SSO page | 5.0.2 and later | NDM `SRG-APP-000516-NDM-000336` | GUI: System > SAML SSO |
| GUI | Deletion of several FortiGate and FortiClient devices at once | 5.0.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| ICAP adapter | Up to 1000 ICAP connections | 5.0.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Device integration | Automatic deletion of idle devices | 5.0.2 and later | IDPS `SRG-NET-000383-IDPS-00208` | GUI: System > Settings (Data Storage; deleted devices must be authorized again) |
| Licensing | Pooled MTA seat licenses in an HA cluster | 5.0.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Platform | FortiSandbox VMS deployment model for on-premises and public cloud | 5.0.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Administrators | CLI command to change one's own password (change-password) | 5.0.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Platform | FortiSandbox PaaS | 5.0.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Threat data | Secure connection to the FortiSandbox Community Cloud and threat intelligence | 5.0.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | GUI: System > FortiGuard (Secure Connection on, if the Community Cloud is used) |
| Platform | Root-OU IAM accounts on FortiSandbox PaaS | 5.0.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Authentication | Admin profile assigned from the SAML assertion | 5.0.2 and later | NDM `SRG-APP-000153-NDM-000249`; NDM `SRG-APP-000033-NDM-000212` | GUI: System > SAML SSO |
| Threat data | HTTP Community Cloud queries through a proxy | 5.0.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Reports | All extracted URLs in the job report PDF | 5.0.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | Arabic file names on the Job Search and Details pages | 5.0.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Logging | System event when concurrent connections exceed the limit | 5.0.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Platform | Built-in email server on FortiSandbox PaaS | 5.0.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| VMs | AndroidVMV5 setup scripts | 5.0.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| System | Disk health in hardware-info, tac-report, and SNMP | 5.0.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| CLI | disk-usage command for system, job, and VM disk use | 5.0.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Public cloud | ENA attribute of custom VMs installed from a VHD file on AWS | 5.0.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Scan engine | Lite Mode (mainly static analysis, for large volumes of files) | 5.0.3 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | `lite-mode -d` (Full Mode, the default; Lite Mode has no dynamic scan) |
| Static analysis | Content Disarm and Reconstruction (CDR) for the API and ICAP | 5.0.3 and later | IDPS `SRG-NET-000249-IDPS-00176` | — |
| Logging | FortiAnalyzer Cloud as a log server | 5.0.3 and later | NDM `SRG-APP-000515-NDM-000325`; NDM `SRG-APP-000516-NDM-000350` | GUI: Log & Report > Log Servers |
| Static analysis | Valid subscription required for manual PAIX package uploads | 5.0.3 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| VMs | User-defined file extensions for custom Linux VMs | 5.0.3 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Anti-phishing | RTAP queries for URLs filtered out of the dynamic scan | 5.0.3 and later | IDPS `SRG-NET-000019-IDPS-00019` | `url-deep-check -e -a` (RTAP checks of all URLs; RTAP subscription) |
| Anti-phishing | CAPTCHA recognition in the Real-Time Anti-Phishing service | 5.0.3 and later | IDPS `SRG-NET-000019-IDPS-00019` | — |
| URL analysis | URLs extracted from .msg files | 5.0.3 and later | IDPS `SRG-NET-000228-IDPS-00196` | — |
| ICAP adapter | Several file extractions in ICAP REQMOD | 5.0.3 and later | IDPS `SRG-NET-000248-IDPS-00206` | — |
| Dashboard | RTAP Statistics | 5.0.3 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| VMs | Browser selection for cloud VMs | 5.0.3 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | Filters on the job and on-demand pages | 5.0.3 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | VM Jobs page view size and clone filter | 5.0.3 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | Date format in the allowlist and blocklist | 5.0.3 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Dynamic analysis | Force dynamic scan on antivirus and static detections | 5.0.3 and later | IDPS `SRG-NET-000228-IDPS-00196` | GUI: Scan Policy and Object > Scan Profile (Advanced tab) |
| VMs | Storage type for customized VMs | 5.0.3 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Device integration | Proxy for sending password-protected encrypted files | 5.0.3 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Inline block | More file types in the inline block profile | 5.0.3 and later | IDPS `SRG-NET-000248-IDPS-00206`; IDPS `SRG-NET-000249-IDPS-00176` | GUI: Security Fabric > Device |
| Scan engine | Choice of the child files to scan within an archive (File On-Demand) | 5.0.3 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| API | Concurrent API connections | 5.0.3 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| CLI | SSD status in tac-report | 5.0.3 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Public cloud | Private link authentication on AWS | 5.0.3 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| CLI | prescan-config timeouts and limits by file size for unpacking and YARA scans | 5.0.3 and later | IDPS `SRG-NET-000248-IDPS-00206` | `prescan-config -l` |
| Threat data | Encryption option of format-storage on the 3000G | 5.0.3 and later | NDM `SRG-APP-000231-NDM-000271` | `format-storage -k <BASE64_PASSPHRASE>` (3000G only; it erases all data) |
| Inline block | Inline behavior timeout extended to 180 seconds | 5.0.5 and later | IDPS `SRG-NET-000249-IDPS-00176` | `inline-block-timeout -l` (a timeout of 20 to 180 seconds; the action for the submitted file is skip, the default, or scan in the VM) |
| CLI | Power supply status (ps-status) on more models, including the 1500G | 5.0.5+; 5.2.0+ | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Dynamic analysis | Automatic rescan of documents when the application crashes | 5.0.6 and later | IDPS `SRG-NET-000228-IDPS-00196` | — |
| Scan engine | Rating of files hosted on trusted Fortinet domains | 5.0.6 and later | IDPS `SRG-NET-000228-IDPS-00196` | — |
| HA cluster | Cluster Management mode (primary or secondary nodes that do not scan) | 5.0.6+; 5.2.0+ | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| VMs | RHEL9 custom VMs | 5.0.6 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| System | System security and stability enhancements | 5.0.7+; 5.2.0+ | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| CLI | scan-perf command for scan performance statistics | 5.0.7+; 5.2.0+ | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Dashboard | New dashboard page | 5.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Threat intelligence | Threat Intelligence menu | 5.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Reports | FortiGuard threat intelligence in Job Details reports | 5.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| VMs | Cloud VM names for Windows, Linux, Android, and macOS | 5.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Dashboard | Lite Mode widgets | 5.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | Warning banner in global conserve mode | 5.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Alerts | Trap port number for SNMP v3 | 5.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Static analysis | Adjustable image category ratings | 5.2.0 and later | IDPS `SRG-NET-000228-IDPS-00196` | GUI: Scan Policy and Object > Image Category |
| Threat intelligence | MITRE ATT&CK matrix of all threats in a time period | 5.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| System | Best practice compliance checklists | 5.2.0 and later | NDM `SRG-APP-000516-NDM-000317`; IDPS `SRG-NET-000512-IDPS-00194` | GUI: System > Best Practices (System Hardening) |
| Scan engine | Archive rating that shows malicious or suspicious child files | 5.2.0 and later | IDPS `SRG-NET-000228-IDPS-00196` | — |
| Reports | Job Detail and tree view readability | 5.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | Modify URL package page style | 5.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | GUI migrated to the Neutrino framework | 5.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Network share | Sentinel Mode for AWS S3 buckets (event-driven) | 5.2.0 and later | IDPS `SRG-NET-000248-IDPS-00206` | GUI: Security Fabric > Network Share |
| Threat intelligence | Webhook callbacks of verdicts to FortiSOAR | 5.2.0 and later | IDPS `SRG-NET-000383-IDPS-00208` | GUI: Threat Intelligence > Threat Intelligence Settings (WebHook Integration with token authentication) |
| Device integration | Up to 10,000 FortiClients | 5.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Platform | Hyper-V on Windows Server 2025 | 5.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Inline block | HTA files in the inline block profile | 5.2.0 and later | IDPS `SRG-NET-000248-IDPS-00206` | GUI: Security Fabric > Device |
| Inline block | Android, Linux, and macOS files for inline block | 5.2.0 and later | IDPS `SRG-NET-000248-IDPS-00206` | GUI: Security Fabric > Device |
| ICAP adapter | ICAP resilience in conserve mode | 5.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Threat data | Lightning Mode (clean job details are not saved) | 5.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | `lightning-mode -d` (the default) |
| Static analysis | AI-based FIRE image categorization with OCR and QR code extraction | 5.2.0 and later | IDPS `SRG-NET-000228-IDPS-00196` | `sandboxing-embeddedobj -l` (image classification, type image, is off by default; set -n to 1 or more to enable it) |
| ICAP adapter | Antivirus scan daemon for ICAP quick scans | 5.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Dynamic analysis | Dynamic scans in as little as 15 seconds | 5.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Inline block | Faster verdicts for inline block and ICAP when a suspicious file is found in a compressed file | 5.2.0 and later | IDPS `SRG-NET-000249-IDPS-00176` | — |
| Network share | Event-driven network share scans and a one-minute minimum interval | 5.2.0 and later | IDPS `SRG-NET-000248-IDPS-00206` | GUI: Security Fabric > Network Share |
| URL analysis | Multi-stage evasion in URL detonation jobs | 5.2.0 and later | IDPS `SRG-NET-000228-IDPS-00196` | — |
| Network share | Network share scans resume after a reboot | 5.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| URL analysis | URL processing | 5.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| URL analysis | URLs extracted from executable scripts, SVG files, and all other file types | 5.2.0 and later | IDPS `SRG-NET-000228-IDPS-00196` | `sandboxing-embeddedobj -l` (3 embedded URLs and 3 embedded files by default, up to 30) |
| System | Global conserve mode | 5.2.0 and later | NDM `SRG-APP-000435-NDM-000315` | — |
| Static analysis | LZIP archives | 5.2.0 and later | IDPS `SRG-NET-000248-IDPS-00206` | — |
| Dynamic analysis | Rescan of jobs that were scanned dynamically | 5.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| VMs | Android Docker environment | 5.2.0 and later | IDPS `SRG-NET-000228-IDPS-00196` | — |
| VMs | AndroidVM6 (older Android VMs disabled) | 5.2.0 and later | IDPS `SRG-NET-000228-IDPS-00196` | GUI: Scan Policy and Object > VM Settings |
| ICAP adapter | Full scan timeout through the ICAP adapter of up to 30 minutes | 5.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Threat intelligence | Malware clustering model based on sandbox behavior | 5.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Reports | QR code or URL shown for embedded URLs | 5.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Threat intelligence | Manual uploads and URL detonations on the Incident Assist page | 5.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Threat intelligence | Automatic IOC validation against FortiGuard for every suspicious file | 5.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Reports | Installer details in PDF reports | 5.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Threat data | Data-at-Rest Encryption (DARE) of configuration and job data | 5.2.0 and later | NDM `SRG-APP-000231-NDM-000271` | `set-dare-encryption -e` (before the unit joins a cluster; not on cloud VMs or E models; only a factory reset disables it) |
| Management access | Central management of CA certificates | 5.2.0 and later | NDM `SRG-APP-000910-NDM-000300` | GUI: System > Certificates |
| CLI | diagnose-debug option for report generation | 5.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Alerts | Email alerts when the system enters and leaves conserve mode | 5.2.0 and later | NDM `SRG-APP-000357-NDM-000293` | GUI: System > Mail Server |
| Dashboard | Scan Performance widget data | 5.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Reports | CSV reports with predefined columns | 5.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| CLI | Conserve mode in tac-report | 5.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| URL analysis | URL deep scan (recursive analysis, redirects, and chained URL detonation) | 5.2.0 and later | IDPS `SRG-NET-000228-IDPS-00196`; IDPS `SRG-NET-000019-IDPS-00019` | `url-deep-check -e -r` (recursive URL checks) |
| API | Image category scoring in the API | 5.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| API | Submit multiple files option in the administrator creation API | 5.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Static analysis | paix-ioc command for enriched PAIX IOCs | 5.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | `paix-ioc -d` (the default) |
| URL analysis | Number of embedded URLs for dynamic scans, and sandboxing-embedded-url renamed sandboxing-embeddedobj | 5.2.0 and later | IDPS `SRG-NET-000228-IDPS-00196` | `sandboxing-embeddedobj -l` (3 embedded URLs and 3 embedded files by default, up to 30) |
| Updates | FDN update schedule and server port on the FortiGuard page | 5.2.2 and later | IDPS `SRG-NET-000246-IDPS-00205` | GUI: System > FortiGuard (Server Update Settings: Adaptive or a short custom interval) |
| Public cloud | Larger EC2 instance types for non-nested AWS clones | 5.2.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| URL analysis | Parked Domain web category | 5.2.2 and later | IDPS `SRG-NET-000019-IDPS-00019` | GUI: Scan Policy and Object > Web Category |
| Reports | FortiGuard IOC message when no IOC data is available | 5.2.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Backup | Remote SCP server check that works without ping | 5.2.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Logging | Original submission ID in the event log for dropped duplicates | 5.2.2 and later | IDPS `SRG-NET-000074-IDPS-00059` | — |
| ICAP adapter | ICAP adapter verdict timeout of up to 12 hours | 5.2.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Updates | Fallback to the full package when a delta engine update fails | 5.2.2 and later | IDPS `SRG-NET-000246-IDPS-00205` | — |
| Threat intelligence | Malware packages exclude files with trusted digital signatures | 5.2.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Threat data | Disk encryption passphrase stored in the TPM on G models | 5.2.2 and later | NDM `SRG-APP-000231-NDM-000271` | `set-dare-encryption -l` |
| Logging | ICAP adapter debug logs | 5.2.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Scan engine | filesize-limit can remove the size and extraction limits | 5.2.2 and later | IDPS `SRG-NET-000248-IDPS-00206` | `filesize-limit -l` |
| API | get-job-ids filtered by the serial number of the device | 5.2.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| CLI | Conserve mode in the status command | 5.2.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Device integration | Legacy OFTP device login authentication can be disabled (certificate identity required) | 5.2.2 and later | IDPS `SRG-NET-000383-IDPS-00208`; NDM `SRG-APP-000038-NDM-000213` | `device-authorization -q` (once every device's certificate carries its serial number) |
| Backup | SFTP for remote configuration backup and restore | 5.2.2 and later | NDM `SRG-APP-000516-NDM-000340` | `backup-sysconf -s<SERVER> -tsftp -u<USER> -f<FILE_PATH>` |
| API | pwd_protected attribute in the job verdict response | 5.2.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| VMs | UEFI boot for custom VMs | 5.2.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| CLI | diagnose-debug events streams event logs | 5.2.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Updates | reset-sandbox-av command to reset antivirus and network alert signatures | 5.2.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| CLI | User information in tac-report | 5.2.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| API | PCAP download through the job detail API | 5.2.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |

### Requirement reference

The requirements used in the map and in this chapter's text, with their
severity in the current SRG releases:

[Download the requirement reference as CSV](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/data/volume-172-disa-srgs-and-stigs/21-fortisandbox-feature-version-and-srg-map-requirements.csv) (95 rows).

| SRG | Requirement | Severity | Requirement title |
| --- | --- | --- | --- |
| NDM | `SRG-APP-000001-NDM-000200` | CAT II | The network device must limit the number of concurrent sessions to an organization-defined number for each administrator account and/or administrator account type. |
| NDM | `SRG-APP-000026-NDM-000208` | CAT II | The network device must automatically audit account creation. |
| NDM | `SRG-APP-000027-NDM-000209` | CAT II | The network device must automatically audit account modification. |
| NDM | `SRG-APP-000029-NDM-000211` | CAT II | The network device must automatically audit account removal actions. |
| NDM | `SRG-APP-000033-NDM-000212` | CAT I | The network device must be configured to assign appropriate user roles or access levels to authenticated users. |
| NDM | `SRG-APP-000038-NDM-000213` | CAT II | The network device must enforce approved authorizations for controlling the flow of management information within the network device based on information flow control policies. |
| NDM | `SRG-APP-000065-NDM-000214` | CAT II | The network device must be configured to enforce the limit of three consecutive invalid logon attempts, after which time it must block any login attempt for 15 minutes. |
| NDM | `SRG-APP-000068-NDM-000215` | CAT II | The network device must display the Standard Mandatory DoD Notice and Consent Banner before granting access to the device. |
| NDM | `SRG-APP-000069-NDM-000216` | CAT II | The network device must retain the Standard Mandatory DoD Notice and Consent Banner on the screen until the administrator acknowledges the usage conditions and takes explicit actions to log on for further access. |
| NDM | `SRG-APP-000095-NDM-000225` | CAT II | The network device must produce audit log records containing sufficient information to establish what type of event occurred. |
| NDM | `SRG-APP-000096-NDM-000226` | CAT II | The network device must produce audit records containing information to establish when (date and time) the events occurred. |
| NDM | `SRG-APP-000098-NDM-000228` | CAT II | The network device must produce audit log records containing information to establish the source of events. |
| NDM | `SRG-APP-000099-NDM-000229` | CAT II | The network device must produce audit records that contain information to establish the outcome of the event. |
| NDM | `SRG-APP-000100-NDM-000230` | CAT II | The network device must generate audit records containing information that establishes the identity of any individual or process associated with the event. |
| NDM | `SRG-APP-000101-NDM-000231` | CAT II | The network device must generate audit records containing the full-text recording of privileged commands. |
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
| NDM | `SRG-APP-000515-NDM-000325` | CAT II | The network device must off-load audit records onto a different system or media than the system being audited. |
| NDM | `SRG-APP-000516-NDM-000317` | CAT II | The network device must be configured in accordance with the security configuration settings based on DoD security configuration or implementation guidance, including STIGs, NSA configuration guides, CTOs, and DTMs. |
| NDM | `SRG-APP-000516-NDM-000335` | CAT II | The network device must enforce access restrictions associated with changes to the system components. |
| NDM | `SRG-APP-000516-NDM-000336` | CAT I | The network device must be configured to use at least one authentication server for the purpose of authenticating users prior to granting administrative access. For boundary devices, two authentication servers are required. |
| NDM | `SRG-APP-000516-NDM-000340` | CAT II | The network device must be configured to conduct backups of system level information contained in the information system when changes occur. |
| NDM | `SRG-APP-000516-NDM-000344` | CAT II | The network device must obtain its public key certificates from an appropriate certificate policy through an approved service provider. |
| NDM | `SRG-APP-000516-NDM-000350` | CAT I | The network device must be configured to send log data to at least one central log server for the purpose of forwarding alerts to the administrators and the information system security officer (ISSO). For boundary devices, two log servers are required. |
| NDM | `SRG-APP-000820-NDM-000170` | CAT II | The network device must be configured to implement multifactor authentication for local; network; and/or remote access to privileged accounts; and/or nonprivileged accounts such that one of the factors is provided by a device separate from the system gaining access. |
| NDM | `SRG-APP-000825-NDM-000180` | CAT II | The network device must be configured to implement multifactor authentication for local; network; and/or remote access to privileged accounts; and/or nonprivileged accounts such that the device meets organization-defined strength of mechanism requirements. |
| NDM | `SRG-APP-000845-NDM-000220` | CAT II | The network device must be configured to verify, when users create or update passwords, the passwords are not found on the list of commonly used, expected, or compromised passwords in IA-5 (1) (a) for password-based authentication. |
| NDM | `SRG-APP-000860-NDM-000250` | CAT II | The network device must be configured to allow user selection of long passwords and passphrases, including spaces and all printable characters for password-based authentication. |
| NDM | `SRG-APP-000880-NDM-000290` | CAT II | The network device must be configured to protect nonlocal maintenance sessions by separating the maintenance session from other network sessions with the system by logically separated communications paths. |
| NDM | `SRG-APP-000910-NDM-000300` | CAT II | The network device must be configured to include only approved trust anchors in trust stores or certificate stores managed by the organization. |
| NDM | `SRG-APP-000920-NDM-000320` | CAT II | The network device must be configured to synchronize system clocks within and between systems or system components. |
| NDM | `SRG-APP-000925-NDM-000330` | CAT II | The network device must be configured to compare the internal system clocks on an organization-defined frequency with organization-defined authoritative time source. |
| NDM | `SRG-APP-001035-NDM-000340` | CAT I | The network device hardware and software must be a version supported by the vendor. |
| IDPS | `SRG-NET-000018-IDPS-00018` | CAT II | The IPS must enforce approved authorizations by restricting or blocking the flow of harmful or suspicious communications traffic within the network. |
| IDPS | `SRG-NET-000019-IDPS-00019` | CAT II | The IPS must restrict or block harmful or suspicious communications traffic between interconnected networks based on attribute- and content-based inspection of the source, destination, headers, and/or content of the communications traffic. |
| IDPS | `SRG-NET-000019-IDPS-00187` | CAT II | The IDPS must immediately use updates made to policy filters, rules, signatures, and anomaly analysis algorithms for traffic detection and prevention functions. |
| IDPS | `SRG-NET-000074-IDPS-00059` | CAT II | The IDPS must produce audit records containing sufficient information to establish what type of event occurred, including, at a minimum, event descriptions, policy filter, rule or signature invoked, port, protocol, and criticality level/alert code or description. |
| IDPS | `SRG-NET-000075-IDPS-00060` | CAT II | The IDPS must produce audit records containing information to establish when (date and time) the events occurred. |
| IDPS | `SRG-NET-000076-IDPS-00061` | CAT II | The IDPS must produce audit records containing information to establish where the event was detected, including, at a minimum, network segment, destination address, and IDPS component which detected the event. |
| IDPS | `SRG-NET-000077-IDPS-00062` | CAT II | The IDPS must produce audit records containing information to establish the source of the event, including, at a minimum, originating source address. |
| IDPS | `SRG-NET-000078-IDPS-00063` | CAT II | The IDPS must produce audit records containing information to establish the outcome of events associated with detected harmful or potentially harmful traffic, including, at a minimum, capturing all associated communications traffic. |
| IDPS | `SRG-NET-000091-IDPS-00193` | CAT II | The IDPS must provide log information in a format that can be extracted and used by centralized analysis tools. |
| IDPS | `SRG-NET-000113-IDPS-00013` | CAT II | The IDPS must provide audit record generation capability for detection events based on implementation of policy filters, rules, signatures, and anomaly analysis. |
| IDPS | `SRG-NET-000228-IDPS-00196` | CAT II | The IDPS must detect, at a minimum, mobile code that is unsigned or exhibiting unusual behavior, has not undergone a risk assessment, or is prohibited for use based on a risk assessment. |
| IDPS | `SRG-NET-000229-IDPS-00163` | CAT II | The IPS must block any prohibited mobile code at the enclave boundary when it is detected. |
| IDPS | `SRG-NET-000236-IDPS-00170` | CAT II | In the event of a failure of the IDPS function, the IDPS must save diagnostic information, log system messages, and load the most current security policies, rules, and signatures when restarted. |
| IDPS | `SRG-NET-000246-IDPS-00205` | CAT II | The IDPS must automatically update malicious code protection mechanisms as new releases are available in accordance with organizational configuration management procedures. |
| IDPS | `SRG-NET-000248-IDPS-00206` | CAT II | The IDPS must perform real-time monitoring of files from external sources at network entry/exit points. |
| IDPS | `SRG-NET-000249-IDPS-00176` | CAT II | The IPS must block malicious code. |
| IDPS | `SRG-NET-000249-IDPS-00221` | CAT II | The IPS must quarantine or block malicious code. |
| IDPS | `SRG-NET-000249-IDPS-00222` | CAT II | The IDPS must send an immediate (within seconds) alert to, at a minimum, the system administrator when malicious code is detected. |
| IDPS | `SRG-NET-000251-IDPS-00178` | CAT II | The IDPS must automatically update malicious code protection mechanisms as new releases are available in accordance with organizational configuration management policy. |
| IDPS | `SRG-NET-000334-IDPS-00191` | CAT II | The IDPS must off-load log records to a centralized log server. |
| IDPS | `SRG-NET-000335-IDPS-00014` | CAT II | The IDPS must provide an alert to, at a minimum, the system administrator and ISSO when any audit failure events occur. |
| IDPS | `SRG-NET-000383-IDPS-00208` | CAT II | IDPS components, including sensors, event databases, and management consoles must integrate with a network-wide monitoring capability. |
| IDPS | `SRG-NET-000390-IDPS-00212` | CAT II | The IDPS must continuously monitor inbound communications traffic for unusual/unauthorized activities or conditions. |
| IDPS | `SRG-NET-000391-IDPS-00213` | CAT II | The IDPS must continuously monitor outbound communications traffic for unusual/unauthorized activities or conditions. |
| IDPS | `SRG-NET-000392-IDPS-00214` | CAT II | The IDPS must send an alert to, at a minimum, the information system security manager (ISSM) and information system security officer (ISSO) when intrusion detection events are detected which indicate a compromise or potential for compromise. |
| IDPS | `SRG-NET-000392-IDPS-00219` | CAT II | The IDPS must generate an alert to, at a minimum, the ISSM and ISSO when new active propagation of malware infecting DoD systems or malicious code adversely affecting the operations and/or security of DoD systems is detected. |
| IDPS | `SRG-NET-000511-IDPS-00012` | CAT II | The IDPS must off-load log records to a centralized log server in real-time. |
| IDPS | `SRG-NET-000512-IDPS-00194` | CAT II | The IDPS must be configured in accordance with the security configuration settings based on DoD security policy and technology-specific security best practices. |
| IDPS | `SRG-NET-000715-IDPS-00120` | CAT II | The IDPS must implement physically or logically separate subnetworks to isolate organization-defined critical system components and functions. |

### Collecting evidence

Run `status` (firmware version, serial number, system time, and disk and
database state), `show` (the port addresses, administrative ports, and
gateway), `set-tlsver -l`, `device-ssl -l`, `device-authorization -l`,
`upload-settings -l`, `diagnose-clilog -l`, `set-maintainer -l`,
`hc-status -l`, and `sandbox-engines` (the FortiGuard engine and signature
versions), and keep the output with the checklist. Add screenshots or
exports of the panes the map cites, above all *System > Interfaces*,
*System > Administrators*, *System > Admin Profiles*, *System > Password
Policy*, *System > Settings*, *System > Login Disclaimer*, *System > SNMP*,
*System > Certificates*, *System > FortiGuard*, *Log & Report > Log
Servers*, *Security Fabric > Device*, and *Scan Policy and Object > Scan
Profile*. Export the system and job events from the central log server,
and keep the firmware upgrade record and the configuration backup
schedule.

## Validation and Troubleshooting

- **A feature in the map is missing on your FortiSandbox.** Check the
  version column against the FortiSandbox release, and check whether the
  feature depends on the model, the platform (hardware, VM, or public
  cloud), a license or subscription, Lite Mode (which has no dynamic scan,
  adapters, sniffer, or quarantine), or the node's role in an HA cluster
  (some pages do not display on worker nodes).
- **A command is rejected.** The commands were checked against the 5.2.2
  CLI Reference. Older releases may lack the command or option (for
  example `device-authorization -q` before 5.2.2), the CLI is
  case-sensitive, and the admin profile must allow CLI access.
- **A setting is not where the map says.** The menus were reorganized
  several times (4.4.0 reorganized the System and Scan Profile settings,
  and 5.0.0 and 5.2.0 moved the GUI to new frameworks). Look for the setting under the
  older name, and check the Administration Guide of your release.
- **Files are not being scanned dynamically.** Check the Scan Profile VM
  Association, the VM status and licenses, port3 connectivity (SIMNET
  starts when the VMs cannot reach the Internet), the prefilter settings,
  and conserve mode.
- **Logs do not reach the log server.** Check the server type, port,
  Secure Connection, and log levels under *Log & Report > Log Servers*, and
  the path from FortiSandbox; remember that only 1024 logs are buffered.
- **A requirement has no matching feature.** Some requirements are met by
  procedure (checksum checks, password changes), by another system (the
  authentication server, the central log server, the inline device that
  blocks the file), or not at all. Record how each requirement is met,
  not just which feature covers it.

## Security and Best Practices

- Keep FortiSandbox on a vendor-supported release, keep FortiGuard updates
  automatic, and install patches promptly, after checking the image
  checksum.
- Authenticate administrators against a SAML identity provider or RADIUS
  server that enforces DoD PKI, keep one local account of last resort with
  a strong password, enable the password policy, and give each
  administrator the narrowest admin profile that works.
- Allow only HTTPS and SSH on the administrative ports, set trusted hosts
  for every account, enable the login disclaimer with the DoD banner, and
  set the idle timeout to 5 minutes or less.
- Replace the factory certificate with a DoD-issued certificate, use
  SNMPv3 with SHA1 and AES only, synchronize time with a DoD NTP server,
  and send logs to two central log servers.
- Isolate port3, encrypt cluster traffic, authorize devices manually, and
  disable Community Cloud upload unless sharing is approved.
- Review this map each time Fortinet publishes a FortiSandbox release or
  DISA updates the NDM or IDPS SRG.

## References and Knowledge Checks

**References:**

- Fortinet, *FortiSandbox Release Notes*, page "New features and
  enhancements" (4.0.0 to 5.0.7) or "What's new" (5.2.0 to 5.2.2), releases
  4.0.0 to 4.0.6, 4.2.0, 4.2.1, 4.2.3 to 4.2.8, 4.4.0 to 4.4.8, 5.0.0 to
  5.0.7, and 5.2.0 to 5.2.2 (docs.fortinet.com, FortiSandbox
  documentation).
- Fortinet, *FortiSandbox 5.2.2 CLI Reference Guide* and *FortiSandbox
  5.2.2 Administration Guide*.
- Fortinet, *FortiSandbox 4.0.0 Administration Guide* and *4.0.0 CLI
  Reference* (tables of contents, for the core features).
- Fortinet, *FortiSandbox 4.4 NDcPP Common Criteria Technote*.
- DISA Network Device Management SRG V5R5 and Intrusion Detection and
  Prevention Systems SRG V3R4, from the October 2026 STIG Library
  Compilation.
- [Chapter 03](03-the-srg-catalog-how-stigs-are-built-and-what-to-do-without-one.md)
  (SRG-based assessment),
  [Chapter 10](10-fortinet-products-stigs-and-srg-mapping.md) (Fortinet
  products),
  [Chapter 11](11-fortiswitch-feature-version-and-srg-map.md) (the
  FortiSwitch map), and
  [Chapter 12](12-fortianalyzer-feature-version-and-srg-map.md) (the
  FortiAnalyzer map, the model for this chapter).

**Knowledge checks:**

1. Which two SRGs apply to FortiSandbox in this chapter, and which part of
   the system does each one cover?
2. Why is the IDPS SRG a better fit than the NDM SRG for the detection
   features, and which IDPS requirements do not apply?
3. Where does the version data come from, and why is there no New Features
   Guide behind the version column?
4. Why must port3 be isolated, and which requirement does that isolation
   support?
5. Which defaults send threat data out of the enclave or weaken device
   authentication, and which commands change them?
6. Which requirements can FortiSandbox not meet exactly, and how do you
   handle them?

## Summary and Completion Checklist

FortiSandbox has no STIG, so it is assessed against the NDM SRG for its
management plane and the protection of its threat data and integrations,
and against the malicious code, alerting, update, monitoring, and logging
requirements of the IDPS SRG for its detection function. This chapter
maps 518 features to the FortiSandbox release that introduced them,
to 95 SRG requirements, and to the FortiSandbox command or web UI
pane that configures them: 62 core platform features, and 456
features from the FortiSandbox 4.0.0 through 5.2.2 release notes.
Operational features with no direct requirement fall under the
requirement to disable unnecessary functions when unused.

- [ ] Can find the release that introduced a FortiSandbox feature.
- [ ] Can map a FortiSandbox feature to its NDM or IDPS SRG requirement.
- [ ] Can explain why the IDPS SRG is used for the detection features.
- [ ] Can find the FortiSandbox command or web UI pane that meets the
  requirement.
- [ ] Can collect FortiSandbox evidence and record the requirements
  FortiSandbox cannot meet exactly.
