# Chapter 19: FortiADC Feature, Version, and SRG Map

## Learning Objectives

- Find the FortiADC release that introduced a given feature.
- Map each FortiADC feature to the Application Layer Gateway (ALG),
  Network Device Management (NDM), or Virtual Private Network (VPN) SRG
  requirement it helps satisfy.
- Find the FortiADC CLI command that configures each feature to meet its
  requirement.
- Use the map to scope an SRG-based assessment of FortiADC, which has no
  STIG of its own.
- Decide when the VPN SRG applies to an application delivery controller.
- Record the requirements that FortiADC cannot meet exactly, with their
  mitigations.

## Theory and Architecture

FortiADC is Fortinet's application delivery controller: a server load
balancer that sits in front of application servers and adds SSL
offloading, a web application firewall (WAF), global server load balancing
(GSLB) with its own DNS server, and link load balancing. It has **no DISA
STIG** (Chapter 10), so it is assessed against SRGs, as described in
Chapter 03. Chapter 10 assigns it the **Application Layer Gateway (ALG)
SRG** for the data plane, the reverse proxy that terminates client
connections, offloads TLS, authenticates users, and inspects and filters
application traffic; the **Network Device Management (NDM) SRG** for the
management plane, the way administrators log in to and configure the
appliance; and the **Virtual Private Network (VPN) SRG** where FortiADC
terminates VPN or TLS sessions for remote users. For every FortiADC
feature the chapter gives **which FortiADC release introduced it**, **which
requirement it relates to**, and **which command configures it to meet
that requirement**.

FortiADC has its own CLI, organized by function rather than copied from
FortiOS. The objects the map uses most are:

- **Virtual servers** (`config load-balance virtual-server`) listen on an
  address and port and pass traffic to a **real server pool**
  (`config load-balance pool`). A Layer 4 virtual server forwards packets;
  a Layer 7 virtual server is a full proxy that can apply an application
  profile, a client SSL profile, an authentication policy, a WAF profile,
  and antivirus, IPS, and DoS profiles; a Layer 2 virtual server serves
  transparent and SSL forward proxy deployments.
- **Profiles** set the behavior of a virtual server:
  `config load-balance profile` (the application protocol, timeouts, IP
  reputation, and geo IP lists), `config load-balance client-ssl-profile`
  (the TLS versions, ciphers, and client certificate checks on the client
  side), and `config load-balance real-server-ssl-profile` (TLS to the
  real servers).
- **WAF profiles** (`config security waf profile`) group the web
  protection modules: web attack signatures, SQL and XSS injection
  detection, HTTP protocol constraints, URL protection, input validation,
  cookie security, CSRF protection, bot detection, API protection, and
  data loss prevention.
- **Authentication** for application users is set by user groups
  (`config user user-group`) and authentication policies
  (`config load-balance auth-policy`), with local users, LDAP, RADIUS,
  TACACS+, SAML, or OAuth. From 8.0.0 the **Application Access Manager**
  groups these modules, and its **Agentless Application Gateway (AAG)**
  publishes internal RDP, VDI, SSH, and web applications to remote users
  through a web portal.
- **System settings** (`config system global`, `config system admin`,
  `config system accprofile`, `config system password-policy`, and
  `config log setting`) cover the management plane.

FortiADC also runs a global DNS server for GSLB, link load balancing,
dynamic routing, and several Fortinet and third-party cloud services
(FortiGuard, FortiSandbox Cloud, FortiGuard Advanced Bot Protection, AI
Threat Analytics, FortiIdentity Cloud, and the FortiAI Assistant). Those
services are outside the enclave and are not assessed here, so use them
only if they are authorized for your environment.

### Where the version data comes from

Fortinet publishes two kinds of per-release feature lists for FortiADC. The
**Release Notes** of every release have a "What's new" page, and from 7.6
each train also has a cumulative **New Features guide** (one for 7.6.0
to 7.6.7 and one for 8.0.0 to 8.0.4), with an index page per release and
each entry tagged with the release that introduced it. The FortiADC
Administration Guide (called the Handbook up to 7.4) has no "What's new"
chapter. The version column was built from the best source for each train:

- **7.0, 7.1, 7.2, and 7.4 trains:** the "What's new" page of the release
  notes of every release: 7.0.0 through 7.0.6, 7.1.0 through 7.1.5, 7.2.0
  through 7.2.8, and 7.4.0 through 7.4.11. Each feature is a heading on
  the page; its category is the heading above it.
- **7.6 and 8.0 trains:** the per-release index pages of the two New
  Features guides, for 7.6.0 through 7.6.7 and 8.0.0 through 8.0.4. The
  release notes of these trains point to the guides (the 7.6.1 "What's
  new" page has no list of its own and the 7.6.0 page is a short list), so
  the guides are the authoritative lists. Two entries that the guides'
  tables of contents tag with a release but that are missing from that
  release's index page were added (7.6.4 "New CLI Commands for Virtual
  Server and Pool Statistics" and 8.0.3 "OpenSSL Upgrade to 3.5"), and
  every release notes entry of these trains was checked against the guide.

That is all 47 releases Fortinet publishes on docs.fortinet.com for the
7.0 to 8.0 trains. Seventeen of them add no features: 7.0.3 to 7.0.6,
7.1.2 to 7.1.5, 7.2.5, 7.2.6, 7.2.8, and 7.4.6 to 7.4.11 are patch releases
whose "What's new" page says that no new features or enhancements are
included. In 7.4.2 the three new license bundles are one entry.

The table has two groups of rows:

- **Core platform features** (categories starting with *Core:*) are the
  long-standing capabilities that the requirements depend on: management
  access, administrator accounts and authentication, password policy,
  banners, logging and alerts, time, SNMP, firmware and backups,
  certificates, high availability, and the application delivery functions
  themselves (virtual servers, SSL offloading, user authentication, the
  WAF, IPS, antivirus, DoS protection, and GSLB). They existed before
  FortiADC 7.0.0 and are not in any of these lists; they were taken from
  the FortiADC 8.0.3 CLI Reference and Administration Guide.
- **New features** are the 253 entries of the "What's new" pages
  and New Features guide index pages. The categories were assigned for
  this chapter, because the source categories differ from release to
  release, and some titles were lightly edited for clarity. An entry
  listed again in a later release or train is one row with all its
  versions: auto-populated real servers, for example, are listed in 7.2.3
  and again in 7.4.3.

| Version entry | Meaning |
| --- | --- |
| `7.0.0 or earlier` | A core feature that predates the oldest release notes used (FortiADC 7.0.0) |
| `7.4.1 and later` | Introduced in FortiADC 7.4.1 |
| `7.2.3+; 7.4.3+` | Listed in two trains: from 7.2.3 in the 7.2 train and from 7.4.3 in the 7.4 train |

Three cautions apply. First, a feature introduced in a patch release of an
older train may reach a newer train only in a later patch, so "and later"
means later in the same train and, usually, in later trains; the 7.2.3
release notes warn, for example, that auto-populated real servers were lost
on an upgrade to 7.4.0 and returned only in 7.4.3. Second, many features
apply only to some platforms (hardware models, FortiADC-VM, or one public
cloud) or licenses (the 7.4.2 license bundles, FortiFlex, and the cloud
services). Third, a core row records a FortiADC capability, but its
command was checked against the 8.0.3 CLI Reference and may differ on an
older release; several settings it uses arrived later, as the new-feature
rows say (for example the lockout settings in the CLI in 7.6.0, NTP
authentication and syslog encryption settings in 7.6.1, and the option to
disable the default admin account in 8.0.1). FortiADC 8.0.4 has release
notes and New Features entries but, at the time of writing, no CLI
Reference of its own.

### Where the SRG data comes from

The SRG column uses requirement IDs from the October 2026 DISA library:

| SRG column | SRG | Release | Applies to |
| --- | --- | --- | --- |
| **ALG** | Application Layer Gateway SRG | V2R4, benchmark date 01 Jul 2026 | The data plane: virtual servers, SSL offloading, the WAF and other security profiles, user authentication for applications, and the traffic and security logs (assigned by Chapter 10) |
| **NDM** | Network Device Management SRG | V5R5, benchmark date 01 Jul 2026 | The management plane: administrator access, authentication, logging, time, SNMP, firmware, and backups (assigned by Chapter 10) |
| **VPN** | Virtual Private Network SRG | V3R5, benchmark date 01 Jul 2026 | Remote user access that FortiADC terminates: the Agentless Application Gateway portal and ZTNA access to virtual servers (assigned by Chapter 10 where FortiADC terminates VPN or TLS for remote users) |

The ALG SRG is written for every kind of application layer gateway, and a
reverse proxy with a WAF is one of the cases it fits best: the HTTP
requirement (ALG `SRG-NET-000512-ALG-000066`), the injection requirements,
the TLS requirements, and the user authentication intermediary
requirements all apply. The requirements for an ALG that is part of a
cross-domain solution (CDS) do not apply, and neither do the SMTP and
spam requirements unless FortiADC load balances mail with an inspecting
profile. FortiADC does not terminate IPsec tunnels (a Layer 4 virtual
server can only load balance them, from 7.6.3), so the IPsec requirements
of the VPN SRG do not apply; its TLS gateway, remote user authentication,
and session requirements apply to the AAG portal, for example VPN
`SRG-NET-000062-VPN-000200` (TLS 1.2 at a minimum). The global DNS server
is covered by none of the three SRGs; if FortiADC answers DNS for the
enclave, assess that function separately.

The requirement IDs are the **rule version IDs** from the XCCDF files, and
the severity is the rule's severity (high = CAT I, medium = CAT II, low =
CAT III). Each feature maps to one of three kinds of relationship:

- **Implements a requirement.** The feature is how FortiADC meets a
  requirement. Web attack signatures implement the requirement to detect
  SQL injection attacks (ALG `SRG-NET-000319-ALG-000020`), for example.
- **Must be configured to meet a requirement.** The feature is in scope of
  a requirement and has to be set up correctly. A client SSL profile must
  allow only TLS 1.2 and later and approved ciphers (ALG
  `SRG-NET-000062-ALG-000150`), for example.
- **No direct requirement.** The feature is operational, such as a
  scripting function, a platform, a license, a diagnose command, or a GUI
  change. It has no requirement of its own, but if it is not needed it
  falls under the ALG requirement not to have unnecessary services and
  functions enabled (ALG `SRG-NET-000131-ALG-000085`); for a
  management-plane function the NDM equivalent is NDM
  `SRG-APP-000142-NDM-000245`.

The mapping is a starting point for an assessment, not a ruling. Confirm it
with your assessor, especially where a requirement is organization-defined
or depends on how FortiADC is deployed.

### Where the commands come from

Every command was checked against the **FortiADC 8.0.3 CLI Reference**
(dated 03 April 2026), the newest CLI Reference Fortinet publishes for
FortiADC, and every web UI pane named in the table against the **FortiADC
8.0.3 Administration Guide**. The check was automatic: each `config` path
and nested table, each `set` option against the syntax (or the examples)
of the command it is entered under, each listed option value against the
documented values, and each GUI pane name. Read the column this way:

- Commands run on the FortiADC CLI, over SSH, the console, or the CLI
  console in the web UI. With VDOMs enabled, enter `config global` or
  `config vdom` first. Profiles take effect only when a virtual server
  uses them; `<VS>`, `<LB_PROFILE>`, `<CLIENT_SSL_PROFILE>`,
  `<WAF_PROFILE>`, `<IPS_PROFILE>`, and `<AV_PROFILE>` are their names.
- **GUI:** entries name the FortiADC web UI pane.
- Statements are separated by `;` to fit in a table cell; on the CLI, enter
  each one on its own line. Values in `<ANGLE_BRACKETS>` are placeholders
  for your own names, addresses, and keys.
- For **"No direct requirement"** rows, the command shown is the one that
  disables the feature when it is unused. A dash (**—**) means there is
  nothing to change: the feature is a platform, a license, a GUI change, a
  scripting function, a diagnose command, or a capability that is off
  unless configured.

Some requirements cannot be met exactly with FortiADC settings. Record
them on the checklist as open findings with mitigations, or meet them
another way:

- **No PKI login for administrators.** The administrator authentication
  types in the 8.0.3 CLI Reference and Administration Guide are local,
  LDAP, RADIUS, and TACACS+ (plus Security Fabric SSO from 8.0.1); there is
  no certificate (CAC) login, so DoD PKI multifactor authentication for interactive
  logins (NDM `SRG-APP-000149-NDM-000247`, CAT I) cannot be met by
  FortiADC itself. Local administrators can use two-factor authentication
  through FortiIdentity Cloud, a cloud service that the Administration
  Guide says is not supported in HA. Authenticate administrators against a
  RADIUS or TACACS+ server, or through FortiGate Security Fabric SSO
  (8.0.1), that enforces DoD PKI, and record the finding.
- **No FIPS-CC mode command.** The 8.0.3 CLI Reference mentions FIPS-CC
  mode only in passing, in its notes on SSH connections, and documents no
  command to enable it; the Administration Guide describes no such mode.
  Otherwise FIPS appears only as HSM support (7.0.0) and as FIPS-compliant
  cipher options for GSLB (8.0.1). The FIPS requirements
  (NDM `SRG-APP-000179-NDM-000265`, ALG `SRG-NET-000510-ALG-000111`) are
  met, if at all, by restricting TLS to approved versions and ciphers and
  keeping keys in a FIPS-validated HSM. Check the NIST Cryptographic Module
  Validation Program for a certificate covering your FortiADC release.
- **Web UI TLS settings.** The 8.0.3 CLI Reference has no setting for the
  TLS versions and ciphers of the web UI and REST API (NDM
  `SRG-APP-000412-NDM-000331`); 8.0.4 adds them. On earlier releases,
  restrict management access to a dedicated network and record the
  finding.
- **Password rules.** The password policy sets the minimum length (up to
  32) and the character types. There is no setting for the number of
  changed characters (NDM `SRG-APP-000170-NDM-000329`) or a check against
  a list of commonly used or compromised passwords (NDM
  `SRG-APP-000845-NDM-000220`). Prefer remote authentication for
  administrators.
- **Concurrent administrator sessions.** No setting limits the number of
  sessions per administrator (NDM `SRG-APP-000001-NDM-000200`). Record the
  finding, or enforce the limit on the authentication server.
- **LDAP over TLS.** The `config user ldap` syntax in the 8.0.3 CLI
  Reference has only the server, port, CN, and DN; LDAPS, StartTLS, and
  the CA profile are set in the web UI (Application Access Manager >
  Remote Server), as the LDAP rows say.
- **Banner for application users.** FortiADC has a pre-login banner for
  administrators but no notice and consent page setting for the users of a
  virtual server or the AAG portal (ALG `SRG-NET-000041-ALG-000022`, VPN
  `SRG-NET-000041-VPN-000110`). Show the banner in the application, in a
  customized authentication form, or on the AAG login page.
- **Firmware signatures.** The documents do not say that FortiADC verifies
  a digital signature on the firmware image (NDM
  `SRG-APP-000131-NDM-000243`). Compare the image checksum with the one in
  the release notes before every upgrade.
- **Settings with no command.** Several rows mapped to a requirement end in
  a dash because the feature is a signature database, a GUI page, or a
  behavior change with nothing to set, or because its setting is not in
  the 8.0.3 CLI Reference (the 8.0.4 configuration file encryption,
  automatic patch upgrades, and real server host name verification, for
  example).

## Design Considerations

- **Pick the release first, then the features.** If your design depends on
  a feature introduced in a certain release (for example lockout settings
  in the CLI in 7.6.0, NTP authentication in 7.6.1, the option to disable
  the default admin account in 8.0.1, or web UI TLS settings in 8.0.4),
  that sets the minimum FortiADC release, and it must be a vendor-supported
  release (NDM `SRG-APP-001035-NDM-000340`).
- **Separate management from application traffic.** Allow HTTPS and SSH
  only on a dedicated management interface or the HA management interface,
  never on interfaces that carry virtual servers, and restrict
  administrators with trusted hosts and the management trusted IP list.
- **Offload TLS deliberately.** Use client SSL profiles that allow only
  TLS 1.2 and 1.3 with approved ciphers, DoD-issued server certificates,
  and re-encryption to the real servers where the data requires it.
- **Put a WAF profile on every web virtual server.** Web attack signatures,
  injection detection, HTTP protocol constraints, and cookie security turn
  the load balancer into the application layer gateway the ALG SRG
  expects; review WAF exceptions and signature staging regularly.
- **Authenticate users at the gateway when the application cannot.** Use
  client certificates (mutual TLS) or SAML with a DoD PKI identity provider
  rather than HTML forms with passwords, and limit authentication session
  lifetimes.
- **Treat the AAG portal as remote access.** When FortiADC publishes
  internal applications to remote users, the VPN SRG applies: TLS 1.2 or
  later, MFA, a separate authentication server, session time limits, and
  logging of every connection attempt.
- **Turn off what is not used.** Cloud services that are not authorized,
  DoH and DoT, the Security Fabric connection, LLDP, telemetry to
  FortiGuard, the FortiAI Assistant, shell access, Telnet, and SNMP v1 and
  v2c are all functions that need a reason to stay on.

## Implementation and Automation

### The FortiADC feature map

The SRG column uses the abbreviations defined in *Where the SRG data comes
from*. The requirement titles are listed in the next table. The command
column follows the conventions in *Where the commands come from*.

| Category | Feature | Introduced (FortiADC) | SRG requirement(s) | Command to satisfy the requirement |
| --- | --- | --- | --- | --- |
| Core: Management access | Administrative access per interface (HTTP, HTTPS, ping, SNMP, SSH, Telnet) | 7.0.0 or earlier | NDM `SRG-APP-000142-NDM-000245`; NDM `SRG-APP-000412-NDM-000331`; NDM `SRG-APP-000408-NDM-000314`; NDM `SRG-APP-000172-NDM-000259`; NDM `SRG-APP-000880-NDM-000290` | `config system interface; edit <MGMT_PORT>; set allowaccess https ssh; next; end` (management interface only; leave out HTTP and Telnet) |
| Core: Management access | HTTP-to-HTTPS redirect for the web UI | 7.0.0 or earlier | NDM `SRG-APP-000172-NDM-000259`; NDM `SRG-APP-000412-NDM-000331` | GUI: System > Settings (Redirect to HTTPS, enabled by default) |
| Core: Management access | TLS versions and cipher suites for the web UI and REST API | 7.0.0 or earlier | NDM `SRG-APP-000412-NDM-000331`; NDM `SRG-APP-000411-NDM-000330`; NDM `SRG-APP-000179-NDM-000265` | — (no setting in the 8.0.3 CLI Reference; see the 8.0.4 row "Configurable TLS parameters") |
| Core: Management access | SSH CBC ciphers and HMAC-MD5 for administration | 7.0.0 or earlier | NDM `SRG-APP-000412-NDM-000331`; NDM `SRG-APP-000411-NDM-000330` | `config system global; set ssh-cbc-cipher disable; set ssh-hmac-md5 disable; end` |
| Core: Management access | Administrative HTTP, HTTPS, SSH, and Telnet port numbers | 7.0.0 or earlier | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Core: Management access | Web UI server certificate | 7.0.0 or earlier | NDM `SRG-APP-000516-NDM-000344`; NDM `SRG-APP-000910-NDM-000300` | GUI: System > Settings (HTTPS Server Cert: a DoD-issued certificate) |
| Core: Management access | Trusted hosts for each administrator | 7.0.0 or earlier | NDM `SRG-APP-000408-NDM-000314`; NDM `SRG-APP-000038-NDM-000213` | `config system admin; edit <ADMIN>; set trusted-hosts <MGMT_SUBNET>; next; end` |
| Core: Management access | Idle timeout for administrator sessions | 7.0.0 or earlier | NDM `SRG-APP-000190-NDM-000267` | `config system global; set admin-idle-timeout 10; end` |
| Core: Management access | Pre-login banner for administrators | 7.0.0 or earlier | NDM `SRG-APP-000068-NDM-000215` | `config system global; set pre-login-banner enable; end` (banner text under System > Replacement Messages) |
| Core: Management access | Shell access | 7.0.0 or earlier | NDM `SRG-APP-000142-NDM-000245`; NDM `SRG-APP-000340-NDM-000288` | `config system global; set shell-access disable; end` |
| Core: Administrator accounts | Local administrator accounts | 7.0.0 or earlier | NDM `SRG-APP-000148-NDM-000346`; NDM `SRG-APP-000153-NDM-000249` | `config system admin; edit <ADMIN>; set auth-strategy local; set access-profile <PROFILE>; set password <PASSWORD_15_CHARS_MIN>; next; end` |
| Core: Administrator accounts | Access profiles (none, read, read-write per functional area) | 7.0.0 or earlier | NDM `SRG-APP-000033-NDM-000212`; NDM `SRG-APP-000231-NDM-000271`; NDM `SRG-APP-000380-NDM-000304`; NDM `SRG-APP-000340-NDM-000288` | `config system accprofile; edit <PROFILE>; set system read; set log read; set security read; next; end` |
| Core: Administrator accounts | Global administrators and VDOM administrators | 7.0.0 or earlier | NDM `SRG-APP-000033-NDM-000212`; NDM `SRG-APP-000153-NDM-000249` | `config system admin; edit <ADMIN>; set is-system-admin no; set vdom <VDOM>; next; end` (global access only for the administrators who need it) |
| Core: Administrator accounts | Password policy for administrators (length and character types) | 7.0.0 or earlier | NDM `SRG-APP-000164-NDM-000252`; NDM `SRG-APP-000166-NDM-000254`; NDM `SRG-APP-000167-NDM-000255`; NDM `SRG-APP-000168-NDM-000256`; NDM `SRG-APP-000169-NDM-000257` | `config system password-policy; set status enable; set apply-to admin-user; set minimum-length 15; set must-contain upper-case-letter lower-case-letter number non-alphanumeric; end` |
| Core: Administrator accounts | Remote administrator authentication with RADIUS | 7.0.0 or earlier | NDM `SRG-APP-000516-NDM-000336`; NDM `SRG-APP-000153-NDM-000249` | `config user radius; edit <RADIUS>; set server <RADIUS_SERVER>; set secret <SECRET>; set auth-type ms_chapv2; next; end`; `config system admin; edit <ADMIN>; set auth-strategy radius; set radius-server <RADIUS>; set access-profile <PROFILE>; next; end` |
| Core: Administrator accounts | Remote administrator authentication with LDAP | 7.0.0 or earlier | NDM `SRG-APP-000516-NDM-000336`; NDM `SRG-APP-000153-NDM-000249`; NDM `SRG-APP-000172-NDM-000259` | `config user ldap; edit <LDAP>; set server <LDAP_SERVER>; set port 636; set cnid <CNID>; set dn <BASE_DN>; next; end`; `config system admin; edit <ADMIN>; set auth-strategy ldap; set ldap-server <LDAP>; next; end` (LDAPS or StartTLS and the CA profile are set in the web UI under Application Access Manager > Remote Server) |
| Core: Administrator accounts | Two-factor authentication for local administrators (FortiIdentity Cloud) | 7.0.0 or earlier | NDM `SRG-APP-000820-NDM-000170`; NDM `SRG-APP-000825-NDM-000180` | GUI: System > Administrator (Two-factor Authentication; a cloud service, so only if authorized) |
| Core: Administrator accounts | Audit of administrator and configuration changes (event log) | 7.0.0 or earlier | NDM `SRG-APP-000026-NDM-000208`; NDM `SRG-APP-000027-NDM-000209`; NDM `SRG-APP-000343-NDM-000289`; NDM `SRG-APP-000380-NDM-000304` | `config log setting local; set event-log-status enable; set event-log-category admin configuration system user; end` |
| Core: Logging and alerts | Local logging of event, security, and traffic logs | 7.0.0 or earlier | NDM `SRG-APP-000503-NDM-000320`; NDM `SRG-APP-000505-NDM-000322`; NDM `SRG-APP-000095-NDM-000225`; NDM `SRG-APP-000096-NDM-000226`; ALG `SRG-NET-000503-ALG-000038`; ALG `SRG-NET-000505-ALG-000039` | `config log setting local; set status enable; set event-log-status enable; set attack-log-status enable; set loglevel information; end` |
| Core: Logging and alerts | Security (attack) logs for WAF, IPS, antivirus, DoS, geo IP, IP reputation, and firewall | 7.0.0 or earlier | ALG `SRG-NET-000074-ALG-000043`; ALG `SRG-NET-000075-ALG-000044`; ALG `SRG-NET-000076-ALG-000045`; ALG `SRG-NET-000077-ALG-000046`; ALG `SRG-NET-000078-ALG-000047`; ALG `SRG-NET-000079-ALG-000048` | `config log setting local; set attack-log-status enable; set attack-log-category waf ips av ddos geo ipreputation fw; end` |
| Core: Logging and alerts | Traffic logs for virtual servers | 7.0.0 or earlier | ALG `SRG-NET-000074-ALG-000043`; ALG `SRG-NET-000077-ALG-000046`; ALG `SRG-NET-000370-ALG-000125` | `config load-balance virtual-server; edit <VS>; set traffic-log enable; next; end`; `config log setting local; set traffic-log-status enable; set traffic-log-category slb; end` |
| Core: Logging and alerts | Remote syslog servers | 7.0.0 or earlier | NDM `SRG-APP-000515-NDM-000325`; NDM `SRG-APP-000516-NDM-000350`; ALG `SRG-NET-000334-ALG-000050`; ALG `SRG-NET-000511-ALG-000051` | `config log setting remote; edit <SYSLOG_ID>; set status enable; set server <SYSLOG_SERVER>; set proto tcpssl; set event-log-status enable; set attack-log-status enable; set traffic-log-status enable; next; end` |
| Core: Logging and alerts | Local log disk full action | 7.0.0 or earlier | NDM `SRG-APP-000357-NDM-000293`; NDM `SRG-APP-000360-NDM-000295`; ALG `SRG-NET-000088-ALG-000054` | `config log setting local; set disk-full nolog; end` (and alert on disk usage through an automation stitch) |
| Core: Logging and alerts | Alert email and automation stitches (triggers and actions) | 7.0.0 or earlier | NDM `SRG-APP-000360-NDM-000295`; ALG `SRG-NET-000088-ALG-000054`; ALG `SRG-NET-000392-ALG-000141`; ALG `SRG-NET-000249-ALG-000146` | `config system mailserver; set address <SMTP_SERVER>; set security starttls; set smtp-auth enable; end`; `config system alert-email; edit <ALERT_EMAIL>; set to <ISSO_EMAIL>; next; end`; GUI: Security Fabric > Automation |
| Core: Logging and alerts | Protection of logs through access profiles | 7.0.0 or earlier | NDM `SRG-APP-000119-NDM-000236`; ALG `SRG-NET-000098-ALG-000056`; ALG `SRG-NET-000099-ALG-000057`; ALG `SRG-NET-000100-ALG-000058` | `config system accprofile; edit <PROFILE>; set log read; next; end` |
| Core: Time and SNMP | NTP time synchronization | 7.0.0 or earlier | NDM `SRG-APP-000920-NDM-000320`; NDM `SRG-APP-000374-NDM-000299` | `config system time ntp; set ntpsync enable; config ntp-server; edit 1; set server <NTP_SERVER>; next; end; end` |
| Core: Time and SNMP | SNMPv3 users | 7.0.0 or earlier | NDM `SRG-APP-000395-NDM-000310`; NDM `SRG-APP-000412-NDM-000331` | `config system snmp user; edit <SNMP_USER>; set status enable; set security-level authpriv; set auth-proto sha256; set auth-pwd <AUTH_KEY>; set priv-proto aes256; set priv-pwd <PRIV_KEY>; next; end` |
| Core: Time and SNMP | SNMP v1 and v2c communities | 7.0.0 or earlier | NDM `SRG-APP-000395-NDM-000310`; NDM `SRG-APP-000142-NDM-000245` | `config system snmp community; edit <ID>; set status disable; next; end` |
| Core: System integrity | Firmware upgrades | 7.0.0 or earlier | NDM `SRG-APP-000457-NDM-000352`; NDM `SRG-APP-001035-NDM-000340`; NDM `SRG-APP-000131-NDM-000243` | GUI: System > Firmware (check the image checksum published in the release notes before upgrading) |
| Core: System integrity | FortiGuard updates (WAF signatures, IPS, antivirus, IP reputation, and geo IP) | 7.0.0 or earlier | ALG `SRG-NET-000019-ALG-000019`; ALG `SRG-NET-000246-ALG-000132`; ALG `SRG-NET-000251-ALG-000131` | `config system fortiguard; set scheduled-update-status enable; set scheduled-update-frequency daily; end` |
| Core: System integrity | Scheduled configuration backup | 7.0.0 or earlier | NDM `SRG-APP-000516-NDM-000340` | `config system auto-backup; set scheduled-backup-status enable; set scheduled-backup-frequency daily; set storage sftp; set address <SFTP_SERVER>; set username <USER>; set password <PASSWORD>; end` |
| Core: System integrity | Central management (FortiADC Manager) | 7.0.0 or earlier | NDM `SRG-APP-000516-NDM-000340`; NDM `SRG-APP-000516-NDM-000335` | `config system central-management; set status enable; set mgmt-type FortiADC-Manager; set mgmt-addr <MANAGER_ADDRESS>; end` |
| Core: System integrity | Configuration synchronization between appliances (config-sync, not HA) | 7.0.0 or earlier | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | `config system global; set config-sync disable; end` |
| Core: System integrity | Virtual domains (VDOMs) | 7.0.0 or earlier | ALG `SRG-NET-000715-ALG-000120` | `config system global; set vdom-admin enable; set vdom-mode independent-network; end` (where tenants or applications must be separated) |
| Core: High availability | High availability (active-passive, active-active, and active-active-VRRP clusters) | 7.0.0 or earlier | ALG `SRG-NET-000365-ALG-000123`; ALG `SRG-NET-000235-ALG-000118`; ALG `SRG-NET-000236-ALG-000119`; ALG `SRG-NET-000362-ALG-000120` | `config system ha; set mode active-passive; set group-id <GROUP_ID>; set group-name <GROUP>; set hbdev <HB_PORT>; set datadev <DATA_PORT>; end` |
| Core: Certificates | Local, CA, and intermediate CA certificates (trust store) | 7.0.0 or earlier | ALG `SRG-NET-000750-ALG-000140`; ALG `SRG-NET-000755-ALG-000150`; NDM `SRG-APP-000910-NDM-000300` | GUI: System > Certificates (keep only DoD and organization-approved CA certificates) |
| Core: Certificates | Certificate verification (CA group, OCSP, and CRL) | 7.0.0 or earlier | ALG `SRG-NET-000164-ALG-000100`; ALG `SRG-NET-000345-ALG-000099`; ALG `SRG-NET-000355-ALG-000117`; NDM `SRG-APP-000175-NDM-000262`; NDM `SRG-APP-000875-NDM-000280` | `config system certificate certificate_verify; edit <VERIFY>; config group_member; edit 1; set ca-certificate <DOD_CA>; set ocsp <OCSP>; set crl <CRL>; next; end; next; end` |
| Core: Certificates | Certificate revocation lists (CRL) | 7.0.0 or earlier | ALG `SRG-NET-000345-ALG-000099`; NDM `SRG-APP-000875-NDM-000280` | `config system certificate crl; edit <CRL>; set http-url <CRL_URL>; next; end` |
| Core: Server load balancing | Virtual servers (Layer 2, Layer 4, and Layer 7) | 7.0.0 or earlier | ALG `SRG-NET-000018-ALG-000017`; ALG `SRG-NET-000364-ALG-000122`; ALG `SRG-NET-000362-ALG-000120` | `config load-balance virtual-server; edit <VS>; set type l7-load-balance; set load-balance-profile <LB_PROFILE>; set load-balance-pool <POOL>; set waf-profile <WAF_PROFILE>; set status enable; next; end` |
| Core: Server load balancing | Real server pools and health checks | 7.0.0 or earlier | ALG `SRG-NET-000362-ALG-000120`; ALG `SRG-NET-000365-ALG-000123` | `config load-balance pool; edit <POOL>; set health-check-ctrl enable; set health-check-list <HEALTH_CHECK>; next; end` |
| Core: Server load balancing | Client SSL profiles (SSL offloading: TLS versions and ciphers) | 7.0.0 or earlier | ALG `SRG-NET-000062-ALG-000150`; ALG `SRG-NET-000510-ALG-000111`; ALG `SRG-NET-000062-ALG-000092` | `config load-balance client-ssl-profile; edit <CLIENT_SSL_PROFILE>; set ssl-allowed-versions tlsv1.2 tlsv1.3; set ssl-ciphers <APPROVED_CIPHERS>; set renegotiation disable; next; end`; `config load-balance virtual-server; edit <VS>; set client-ssl-profile <CLIENT_SSL_PROFILE>; next; end` |
| Core: Server load balancing | Client certificate authentication (mutual TLS) | 7.0.0 or earlier | ALG `SRG-NET-000140-ALG-000094`; ALG `SRG-NET-000166-ALG-000101`; ALG `SRG-NET-000355-ALG-000117`; ALG `SRG-NET-000164-ALG-000100` | `config load-balance client-ssl-profile; edit <CLIENT_SSL_PROFILE>; set client-certificate-verify <VERIFY>; set client-certificate-verify-option required; next; end` |
| Core: Server load balancing | Real server SSL profiles (re-encryption to back-end servers) | 7.0.0 or earlier | ALG `SRG-NET-000062-ALG-000150`; ALG `SRG-NET-000164-ALG-000100` | `config load-balance real-server-ssl-profile; edit <RS_SSL_PROFILE>; set ssl enable; set allow-ssl-versions tlsv1.2 tlsv1.3; set server-cert-verify <VERIFY>; next; end` |
| Core: Server load balancing | HTTP-to-HTTPS redirection on virtual servers | 7.0.0 or earlier | ALG `SRG-NET-000062-ALG-000150`; ALG `SRG-NET-000230-ALG-000113` | `config load-balance virtual-server; edit <VS>; set http2https enable; next; end` |
| Core: Server load balancing | Application profiles (HTTP timeouts and X-Forwarded-For) | 7.0.0 or earlier | ALG `SRG-NET-000512-ALG-000066`; ALG `SRG-NET-000077-ALG-000046`; ALG `SRG-NET-000705-ALG-000110` | `config load-balance profile; edit <LB_PROFILE>; set http-x-forwarded-for enable; set client-header-timeout <SECONDS>; set client-body-timeout <SECONDS>; next; end` |
| Core: Server load balancing | Connection and transaction rate limits on virtual servers | 7.0.0 or earlier | ALG `SRG-NET-000705-ALG-000110`; ALG `SRG-NET-000362-ALG-000112` | `config load-balance virtual-server; edit <VS>; set connection-limit <MAX>; set connection-rate-limit <RATE>; set trans-rate-limit <RATE>; next; end` |
| Core: Server load balancing | Content routing and content rewriting | 7.0.0 or earlier | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Core: Server load balancing | Persistence rules | 7.0.0 or earlier | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Core: Server load balancing | Caching, compression, and PageSpeed (application optimization) | 7.0.0 or earlier | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Core: Server load balancing | Lua scripting | 7.0.0 or earlier | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — (attach only approved scripts to virtual servers) |
| Core: Server load balancing | Error pages and error messages | 7.0.0 or earlier | ALG `SRG-NET-000273-ALG-000129`; ALG `SRG-NET-000402-ALG-000130` | GUI: Server Load Balance > Advanced Profiles (Error Page; remove internal details) |
| Core: Server load balancing | Authentication policies for users (HTML form, HTTP basic, and NTLM) with LDAP, RADIUS, or local users | 7.0.0 or earlier | ALG `SRG-NET-000138-ALG-000063`; ALG `SRG-NET-000138-ALG-000088`; ALG `SRG-NET-000138-ALG-000089` | `config user user-group; edit <USER_GROUP>; set client-auth-method html_form_auth; set auth-log all; next; end`; `config load-balance virtual-server; edit <VS>; set auth-policy <AUTH_POLICY>; next; end` |
| Core: Server load balancing | Authentication session timeout and remote user credential cache | 7.0.0 or earlier | ALG `SRG-NET-000213-ALG-000107`; ALG `SRG-NET-000517-ALG-000006`; ALG `SRG-NET-000344-ALG-000098`; ALG `SRG-NET-000337-ALG-000096` | `config user user-group; edit <USER_GROUP>; set auth-session-timeout 15; set user-cache-timeout <SECONDS>; next; end` |
| Core: Server load balancing | SAML service provider for user single sign-on | 7.0.0 or earlier | ALG `SRG-NET-000138-ALG-000063`; ALG `SRG-NET-000138-ALG-000088`; ALG `SRG-NET-000230-ALG-000113` | `config user saml-sp; edit <SAML_SP>; set idp-metadata <IDP_METADATA>; set local-cert <SP_CERT>; next; end` |
| Core: Server load balancing | SSL forward proxy (re-signing CA) | 7.0.0 or earlier | ALG `SRG-NET-000062-ALG-000092`; ALG `SRG-NET-000750-ALG-000140` | `config load-balance client-ssl-profile; edit <CLIENT_SSL_PROFILE>; set forward-proxy enable; set forward-proxy-local-signing-CA <DOD_ISSUED_SUBCA>; next; end` (only where outbound SSL inspection is required) |
| Core: Global load balancing | Global server load balancing and the global DNS server | 7.0.0 or earlier | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Core: Global load balancing | DNS recursion | 7.0.0 or earlier | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | `config global-dns-server general; set recursion-status disable; end` |
| Core: Link load balancing | Link load balancing (link groups, link policies, and virtual tunnels) | 7.0.0 or earlier | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Core: Network security | Firewall policies (default deny) | 7.0.0 or earlier | ALG `SRG-NET-000202-ALG-000124`; ALG `SRG-NET-000018-ALG-000017`; NDM `SRG-APP-000038-NDM-000213` | `config firewall policy; set default-action deny; end` |
| Core: Network security | IP reputation | 7.0.0 or earlier | ALG `SRG-NET-000019-ALG-000018`; ALG `SRG-NET-000392-ALG-000142` | `config load-balance profile; edit <LB_PROFILE>; set ip-reputation enable; next; end` |
| Core: Network security | Geo IP block lists | 7.0.0 or earlier | ALG `SRG-NET-000364-ALG-000122`; ALG `SRG-NET-000019-ALG-000018` | `config load-balance geoip-list; edit <GEOIP_LIST>; set action deny; set log enable; next; end`; `config load-balance profile; edit <LB_PROFILE>; set geoip-list <GEOIP_LIST>; next; end` |
| Core: Network security | Intrusion prevention (IPS) | 7.0.0 or earlier | ALG `SRG-NET-000383-ALG-000135`; ALG `SRG-NET-000390-ALG-000139`; ALG `SRG-NET-000391-ALG-000140`; ALG `SRG-NET-000362-ALG-000126`; ALG `SRG-NET-000392-ALG-000141` | `config security ips profile; edit <IPS_PROFILE>; config entries; edit 1; set severity high critical; set action block; set log enable; next; end; next; end`; `config load-balance virtual-server; edit <VS>; set ips-profile <IPS_PROFILE>; next; end` |
| Core: Network security | Antivirus scanning | 7.0.0 or earlier | ALG `SRG-NET-000248-ALG-000133`; ALG `SRG-NET-000249-ALG-000134`; ALG `SRG-NET-000765-ALG-000170`; ALG `SRG-NET-000249-ALG-000145` | `config security antivirus profile; edit <AV_PROFILE>; set av-virus-log enable; set oversize block; set options quarantine; next; end`; `config load-balance virtual-server; edit <VS>; set av-profile <AV_PROFILE>; next; end` |
| Core: Network security | FortiSandbox integration | 7.0.0 or earlier | ALG `SRG-NET-000765-ALG-000170` | `config system fortisandbox; set status enable; set type fsa; set server <FSA_SERVER>; set enc-algorithm high; end` |
| Core: Network security | DoS protection (TCP SYN flood, HTTP request flood, HTTP access limit) | 7.0.0 or earlier | ALG `SRG-NET-000362-ALG-000112`; ALG `SRG-NET-000362-ALG-000155`; ALG `SRG-NET-000705-ALG-000110`; ALG `SRG-NET-000392-ALG-000148` | `config security dos tcp-synflood-protection; edit <SYN_PROFILE>; set syncookie enable; set max-half-open <COUNT>; next; end`; `config security dos http-request-flood-protection; edit <HTTP_FLOOD>; set status enable; set action deny; set log enable; next; end`; `config load-balance virtual-server; edit <VS>; set dos-profile <DOS_PROFILE>; next; end` |
| Core: Web application firewall | WAF profiles applied to virtual servers | 7.0.0 or earlier | ALG `SRG-NET-000018-ALG-000017`; ALG `SRG-NET-000019-ALG-000018`; ALG `SRG-NET-000512-ALG-000062` | `config security waf profile; edit <WAF_PROFILE>; set web-attack-signature <SIGNATURE_PROFILE>; set http-protocol-constraint <CONSTRAINT_PROFILE>; set url-protection <URL_PROTECTION>; next; end`; `config load-balance virtual-server; edit <VS>; set waf-profile <WAF_PROFILE>; next; end` |
| Core: Web application firewall | Web attack signatures (SQL injection, XSS, and other attack classes) | 7.0.0 or earlier | ALG `SRG-NET-000318-ALG-000152`; ALG `SRG-NET-000319-ALG-000020`; ALG `SRG-NET-000318-ALG-000014`; ALG `SRG-NET-000319-ALG-000015`; ALG `SRG-NET-000318-ALG-000151`; ALG `SRG-NET-000319-ALG-000153` | `config security waf web-attack-signature; edit <SIGNATURE_PROFILE>; set high-severity-action deny; set medium-severity-action deny; set low-severity-action alert; set request-body-detection enable; next; end` |
| Core: Web application firewall | SQL and XSS injection detection (heuristic) | 7.0.0 or earlier | ALG `SRG-NET-000318-ALG-000152`; ALG `SRG-NET-000319-ALG-000020`; ALG `SRG-NET-000319-ALG-000153` | `config security waf profile; edit <WAF_PROFILE>; set heuristic-sql-xss-injection-detection <INJECTION_PROFILE>; next; end` |
| Core: Web application firewall | HTTP protocol constraints | 7.0.0 or earlier | ALG `SRG-NET-000512-ALG-000066`; ALG `SRG-NET-000401-ALG-000127`; ALG `SRG-NET-000380-ALG-000128` | `config security waf http-protocol-constraint; edit <CONSTRAINT_PROFILE>; set illegal-http-version-check enable; set illegal-host-name-check enable; next; end` |
| Core: Web application firewall | URL protection (URL access and file extension rules) | 7.0.0 or earlier | ALG `SRG-NET-000015-ALG-000016`; ALG `SRG-NET-000202-ALG-000124` | `config security waf profile; edit <WAF_PROFILE>; set url-protection <URL_PROTECTION>; next; end` |
| Core: Web application firewall | Input validation (parameter validation, hidden fields, and file restriction) | 7.0.0 or earlier | ALG `SRG-NET-000401-ALG-000127`; ALG `SRG-NET-000380-ALG-000128`; ALG `SRG-NET-000289-ALG-000110` | `config security waf profile; edit <WAF_PROFILE>; set input-validation-policy <INPUT_POLICY>; next; end` |
| Core: Web application firewall | XML and JSON validation | 7.0.0 or earlier | ALG `SRG-NET-000401-ALG-000127`; ALG `SRG-NET-000380-ALG-000128` | `config security waf profile; edit <WAF_PROFILE>; set xml-validation <XML_DETECTION>; set json-validation <JSON_DETECTION>; next; end` |
| Core: Web application firewall | Cookie security (signing or encryption, HttpOnly, and Secure flags) | 7.0.0 or earlier | ALG `SRG-NET-000230-ALG-000113`; ALG `SRG-NET-000233-ALG-000115` | `config security waf cookie-security; edit <COOKIE_POLICY>; set security-mode signed; set httponly enable; set secure enable; next; end`; `config security waf profile; edit <WAF_PROFILE>; set cookie-security <COOKIE_POLICY>; next; end` |
| Core: Web application firewall | CSRF protection | 7.0.0 or earlier | ALG `SRG-NET-000230-ALG-000113` | `config security waf profile; edit <WAF_PROFILE>; set csrf-protection <CSRF_POLICY>; next; end` |
| Core: Web application firewall | HTTP header security (security response headers) | 7.0.0 or earlier | ALG `SRG-NET-000228-ALG-000108`; ALG `SRG-NET-000288-ALG-000109` | GUI: Web Application Firewall > WAF Profile (HTTP Header Security) |
| Core: Web application firewall | Brute force login protection | 7.0.0 or earlier | ALG `SRG-NET-000362-ALG-000112`; ALG `SRG-NET-000138-ALG-000063` | `config security waf profile; edit <WAF_PROFILE>; set brute-force-login <BRUTE_FORCE_POLICY>; next; end` |
| Core: Web application firewall | Sensitive data protection (data types in responses) | 7.0.0 or earlier | ALG `SRG-NET-000391-ALG-000140` | GUI: Web Application Firewall > Sensitive Data Protection |
| Core: Web application firewall | Web anti-defacement | 7.0.0 or earlier | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | `config security wad profile; edit <WAD_PROFILE>; set monitor disable; next; end` |
| Core: Web application firewall | Web vulnerability scanner | 7.0.0 or earlier | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Core: Security Fabric | Security Fabric connection | 7.0.0 or earlier | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | `config system csf; set status disable; end` |
| Server load balancing | FTPS virtual servers (security mode in the FTP application profile) | 7.0.0 and later | ALG `SRG-NET-000512-ALG-000065`; ALG `SRG-NET-000062-ALG-000150` | `config load-balance profile; edit <LB_PROFILE>; set type ftp; set security-mode explicit; next; end` (or implicit; with a client SSL profile that allows only TLS 1.2 and later) |
| Global load balancing | Root CA verification between GSLB and SLB (protection against MITM attacks) | 7.0.0 and later | ALG `SRG-NET-000164-ALG-000100`; ALG `SRG-NET-000062-ALG-000150` | `config global-load-balance setting; set auth-type auth_verify; set ca-verify enable; set ca-group <CA_GROUP>; end` |
| Server load balancing | Shared IP addresses for SNAT and virtual servers (different port ranges) | 7.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | `config system global; set share-ip-address disable; end` |
| User authentication | SAML enhancements (SP metadata export, signed authentication requests, signed assertions, redirect logout binding) | 7.0.0 and later | ALG `SRG-NET-000138-ALG-000063`; ALG `SRG-NET-000138-ALG-000088`; ALG `SRG-NET-000147-ALG-000095` | `config user saml-sp; edit <SAML_SP>; set assertion-require-sign enable; set authnrequest-sign-algorithm rsa-sha256; next; end` |
| Troubleshooting | Layer 4 virtual server debug (diagnose debug flow) | 7.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Web application firewall | WAF exception rule types (HTTP method, header, cookie, parameter, source IPv6) | 7.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — (keep exceptions to the minimum the application needs) |
| Network security | IP reputation with the Internet Service Database (ISDB) | 7.0.0 and later | ALG `SRG-NET-000019-ALG-000018`; ALG `SRG-NET-000392-ALG-000142` | `config load-balance profile; edit <LB_PROFILE>; set ip-reputation enable; next; end` |
| System | FortiGuard delta package downloads for the antivirus database | 7.0.0 and later | ALG `SRG-NET-000246-ALG-000132` | — |
| Certificates | FIPS support for HSM servers (FIPS-certified HSM) | 7.0.0 and later | ALG `SRG-NET-000755-ALG-000150`; ALG `SRG-NET-000575-ALG-000020` | — (HSM integration; no setting in the 8.0.3 CLI Reference) |
| Certificates | ACME certificate enrollment (for example from Let's Encrypt) | 7.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — (use only with a CA your organization approves) |
| High availability | Unicast HA (VRRP) for FortiADC-VM on KVM | 7.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| GUI | Login navigation page (set a host name and change the default password at first login) | 7.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| GUI | GUI enhancements (dashboard and FortiView charts) | 7.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Platform | FortiADC-VM support for VMware hardware version 13 | 7.0.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Logging and alerts | OFTP log transport to FortiAnalyzer | 7.0.1 and later | NDM `SRG-APP-000515-NDM-000325`; ALG `SRG-NET-000334-ALG-000050` | `config log setting fortianalyzer; set status enable; set server <FAZ_SERVER>; set event-log-status enable; set attack-log-status enable; end` |
| Logging and alerts | System and security event automation for specific virtual or real servers | 7.0.1 and later | NDM `SRG-APP-000360-NDM-000295`; ALG `SRG-NET-000392-ALG-000141` | GUI: Security Fabric > Automation |
| Web application firewall | WAF exceptions created from WAF logs | 7.0.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Management access | REST API administrator accounts (authorization token) | 7.0.1 and later | NDM `SRG-APP-000408-NDM-000314`; NDM `SRG-APP-000153-NDM-000249` | GUI: System > Administrator (create only the REST API administrators that are needed, with trusted hosts) |
| ZTNA | Zero Trust Network Access (FortiClient EMS tags and client certificates for Layer 7 HTTPS and TCPS virtual servers) | 7.0.2 and later | ALG `SRG-NET-000015-ALG-000016`; ALG `SRG-NET-000164-ALG-000100`; VPN `SRG-NET-000343-VPN-001370`; VPN `SRG-NET-000148-VPN-000540` | `config endpoint-control fctems; edit <EMS>; set server <EMS_SERVER>; next; end`; `config load-balance virtual-server; edit <VS>; set ztna-profile <ZTNA_PROFILE>; next; end` |
| Logging and alerts | Device host name in SNMP traps and syslog messages | 7.0.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Server load balancing | RFC 7919 compliance in client and real server SSL profiles | 7.1.0 and later | ALG `SRG-NET-000062-ALG-000150` | `config load-balance client-ssl-profile; edit <CLIENT_SSL_PROFILE>; set rfc7919-comply enable; next; end` |
| Server load balancing | Cookie hash and insert cookie persistence enhancements | 7.1.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Server load balancing | IPv6 for Layer 2 TCP, UDP, and IP virtual servers | 7.1.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Server load balancing | WAF deny error page (message ID, signature ID, and client IP) | 7.1.0 and later | ALG `SRG-NET-000273-ALG-000129` | — |
| Server load balancing | Real server pool and pool member availability status | 7.1.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Global load balancing | BIND 9.18.0 upgrade (DNSSEC on by default) | 7.1.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Web application firewall | View and release WAF blocked IP addresses (FortiView) | 7.1.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Network security | External IP lists in firewall policies (IP address external connector) | 7.1.0 and later | ALG `SRG-NET-000364-ALG-000122`; ALG `SRG-NET-000202-ALG-000124` | `config firewall policy; config rule; edit <RULE_ID>; set source-type external-resource; set source-external-resource-address <EXTERNAL_LIST>; set action deny; next; end; end` |
| Web application firewall | OWASP Top 10 2021 update (wizard and FortiView) | 7.1.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Web application firewall | SAP web server signature type | 7.1.0 and later | ALG `SRG-NET-000318-ALG-000151`; ALG `SRG-NET-000319-ALG-000153` | — |
| Logging and alerts | FortiAnalyzer OFTP connectivity status and test | 7.1.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Management access | Declarative REST API | 7.1.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Certificates | ACME automatic renewal through the TLS-ALPN-01 challenge | 7.1.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| GUI | Child configuration created on the parent configuration page | 7.1.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| System | Administrative domains (ADOMs: VDOM mode share-network) | 7.1.1 and later | NDM `SRG-APP-000033-NDM-000212`; ALG `SRG-NET-000715-ALG-000120` | `config system global; set vdom-admin enable; set vdom-mode share-network; end` (where administrators must be limited to some virtual servers) |
| Logging and alerts | Automation egress VDOM for syslog, SNMP trap, and webhook actions | 7.1.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Network security | Geo IP block lists and allowlists for SMTP, FTP, RADIUS, MSSQL, and ISO8583 profiles | 7.1.1 and later | ALG `SRG-NET-000364-ALG-000122`; ALG `SRG-NET-000019-ALG-000018` | `config load-balance profile; edit <LB_PROFILE>; set geoip-list <GEOIP_LIST>; next; end` |
| Server load balancing | NAT source pools for Layer 7 SMTP, MSSQL, and ISO8583 virtual servers | 7.1.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Server load balancing | Error page customization in the web UI (LB_ERROR_PAGE_DEFAULT) | 7.1.1 and later | ALG `SRG-NET-000273-ALG-000129`; ALG `SRG-NET-000402-ALG-000130` | GUI: Server Load Balance > Advanced Profiles |
| User authentication | Error message for failed form-based authentication | 7.1.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Global load balancing | DNS over HTTP, HTTPS, and TLS (DoH and DoT) | 7.2.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | `config global-dns-server general; set dns-over-http disable; set dns-over-https disable; set dns-over-tls disable; end` |
| Scripting | AUTH class Lua function (BEFORE_AUTH) | 7.2.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Scripting | HTTP persistence Lua functions | 7.2.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Global load balancing | Address book check for the named default port 53 | 7.2.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Troubleshooting | Layer 4 server load balance debug flow enhancements | 7.2.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Server load balancing | Layer 4 FTP profile listening ports | 7.2.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Web application firewall | Bot mitigation: threshold-based and biometrics-based detection | 7.2.0 and later | ALG `SRG-NET-000362-ALG-000112`; ALG `SRG-NET-000390-ALG-000139` | `config security waf profile; edit <WAF_PROFILE>; set threshold-based-detection <THRESHOLD_POLICY>; set biometrics-based-detection <BIOMETRICS_POLICY>; next; end` |
| ZTNA | ZTNA columns in FortiView (public IP, tags, MAC, OS) | 7.2.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Platform | AWS Auto Scaling | 7.2.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Logging and alerts | Automation workflow redesign (separate triggers and actions) | 7.2.0 and later | NDM `SRG-APP-000360-NDM-000295`; ALG `SRG-NET-000392-ALG-000141` | GUI: Security Fabric > Automation |
| Administrator accounts | TACACS+ remote authentication | 7.2.0 and later | NDM `SRG-APP-000516-NDM-000336`; NDM `SRG-APP-000153-NDM-000249` | `config user tacacs+; edit <TACACS>; set server <TACACS_SERVER>; set secret <SECRET>; set auth-type auto; next; end`; `config system admin; edit <ADMIN>; set auth-strategy tacacs_plus; set tacacs-plus-server <TACACS>; next; end` |
| Management access | Declarative REST API enhancements | 7.2.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| SSL inspection | Source IP in the L2 exception list and SSLi bypass rules | 7.2.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Troubleshooting | Debug file download enhancements | 7.2.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Platform | FortiADC-VM on IBM Cloud | 7.2.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Server load balancing | Auto-populated real servers from an FQDN | 7.2.3+; 7.4.3+ | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Administrator accounts | System backup restricted to global administrators | 7.2.3 and later | NDM `SRG-APP-000516-NDM-000340`; NDM `SRG-APP-000033-NDM-000212` | `config system admin; edit <ADMIN>; set is-system-admin no; next; end` (for administrators who must not back up the configuration) |
| Scripting | HTTP:Respond in HTTP response events | 7.2.4 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| High availability | Unicast and broadcast heartbeats for active-active-VRRP HA on hardware | 7.2.7+; 7.4.4+ | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Scripting | SSL session ID persistence in Layer 7 TCP (LB:set_peer) | 7.2.7+; 7.4.5+ | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Global load balancing | DNSSEC signing with 1024, 2048, and 4096-bit keys and new algorithms | 7.4.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Global load balancing | Minimal responses option | 7.4.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Global load balancing | Sync list for all GLB objects | 7.4.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Platform | FortiADC Ingress Controller 2.0 (Kubernetes) | 7.4.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Platform | Red Hat OpenShift 4 support for the Ingress Controller | 7.4.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Server load balancing | HTTP/3 over QUIC (client side, experimental in 7.4.0) | 7.4.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Server load balancing | TCP RST to client and real server on session timeout (Layer 4 and Layer 2) | 7.4.0 and later | ALG `SRG-NET-000213-ALG-000107` | `config load-balance profile; edit <LB_PROFILE>; set timeout_send_rst enable; next; end` |
| Server load balancing | Persistent cookie domain attribute | 7.4.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Server load balancing | Session cookies for persistent and insert cookie persistence | 7.4.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Server load balancing | IP pool persistence for Layer 4 source IP persistence | 7.4.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Server load balancing | Source address and port persistence for Layer 4 and Layer 2 | 7.4.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Scripting | HTTP Lua functions for unique session and transaction IDs | 7.4.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Web application firewall | API discovery and fingerprint-based bot detection | 7.4.0 and later | ALG `SRG-NET-000401-ALG-000127`; ALG `SRG-NET-000390-ALG-000139`; ALG `SRG-NET-000362-ALG-000112` | `config security waf profile; edit <WAF_PROFILE>; set api-discovery <API_DISCOVERY>; set fingerprint-based-detection <FINGERPRINT_POLICY>; next; end` |
| Network security | Firewall connection tracking session timeouts | 7.4.0 and later | ALG `SRG-NET-000213-ALG-000107` | `config firewall global; edit 1; set tcp-established-timeout <SECONDS>; set udp-timeout <SECONDS>; next; end` |
| Network security | Antivirus engine update | 7.4.0 and later | ALG `SRG-NET-000246-ALG-000132` | — |
| Network security | CVE references in IPS signatures | 7.4.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Management access | Terraform FortiADC provider | 7.4.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Platform | FortiFlex licensing for FortiADC-VM | 7.4.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| High availability | Unicast HA (VRRP) on Hyper-V | 7.4.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| High availability | Active-active-VRRP unicast HA in Alibaba Cloud | 7.4.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Logging and alerts | Automation trigger for failed administrator logins and blocked IP addresses | 7.4.0 and later | NDM `SRG-APP-000360-NDM-000295` | GUI: Security Fabric > Automation |
| Logging and alerts | Certificate validation for webhook automation actions | 7.4.0 and later | ALG `SRG-NET-000164-ALG-000100` | GUI: Security Fabric > Automation |
| Global load balancing | Public SDN connector as a GSLB server | 7.4.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Global load balancing | User-defined certificate for GSLB | 7.4.1 and later | ALG `SRG-NET-000164-ALG-000100`; ALG `SRG-NET-000166-ALG-000101` | `config global-load-balance servers; edit <SERVER>; set user-defined-certificate enable; set cert <LOCAL_CERT>; next; end` |
| Server load balancing | Predefined client SSL profiles updated with OpenSSL 3.1.1 (LB_CLIENT_SSL_PROF_MODERN) | 7.4.1 and later | ALG `SRG-NET-000062-ALG-000150`; ALG `SRG-NET-000510-ALG-000111` | `config load-balance virtual-server; edit <VS>; set client-ssl-profile LB_CLIENT_SSL_PROF_MODERN; next; end` |
| Server load balancing | Packet forwarding method and IP pools for Layer 4 content routing | 7.4.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Server load balancing | Multiple processes for HTTP/3 virtual servers | 7.4.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Scripting | TCP Lua timer and close functions | 7.4.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Web application firewall | FortiGuard Advanced Bot Protection (cloud service) | 7.4.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | `config system global; set advanced-bot-status disable; end` |
| Logging and alerts | Automation stitches and log-based automation triggers | 7.4.1 and later | NDM `SRG-APP-000360-NDM-000295`; ALG `SRG-NET-000392-ALG-000141`; ALG `SRG-NET-000088-ALG-000054` | GUI: Security Fabric > Automation |
| System | Global Resources page | 7.4.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Network | BFD for BGP | 7.4.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Network | DNS override per VDOM | 7.4.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Network | IPv6 reverse route cache | 7.4.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| High availability | HA firmware upgrade from an FTP server | 7.4.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| System | Firmware maturity levels (Feature and Mature tags) | 7.4.1 and later | NDM `SRG-APP-001035-NDM-000340` | — (prefer Mature releases that are vendor-supported) |
| Platform | AWS IMDSv2 | 7.4.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Platform | Certificate validation of public SDN connectors | 7.4.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Troubleshooting | Debug filters for fnginx modules | 7.4.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Troubleshooting | Debug module for the named daemon | 7.4.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Platform | License bundles (Network Security, Application Security, AI Security) | 7.4.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Web application firewall | AI Threat Analytics (cloud service) | 7.4.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | `config system global; set threat-analytics disable; end` |
| Web application firewall | Data loss prevention with FortiGuard DLP signatures | 7.4.2 and later | ALG `SRG-NET-000391-ALG-000140` | `config security waf profile; edit <WAF_PROFILE>; set data-leak-prevention <DLP_POLICY>; next; end` |
| Network security | DNS DDoS protection (DNS query rate limit) | 7.4.2 and later | ALG `SRG-NET-000362-ALG-000112`; ALG `SRG-NET-000705-ALG-000110` | `config security dos dns-query-flood-protection; edit <DNS_FLOOD>; set status enable; set dns-query-rate-limit <RATE>; set action deny; set log enable; next; end` |
| SSL inspection | SSL forward proxy certificates re-signed to match the SNI | 7.4.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| GUI | Feature tour | 7.4.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| System | FortiGuard DLP signature downloads | 7.4.2 and later | ALG `SRG-NET-000019-ALG-000019` | GUI: System > FortiGuard |
| Logging and alerts | FQDN address type for remote syslog servers | 7.4.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Server load balancing | LDAPS health check | 7.4.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Management access | Trusted IP addresses for the management interface | 7.4.2 and later | NDM `SRG-APP-000408-NDM-000314`; NDM `SRG-APP-000038-NDM-000213` | `config system interface; edit <MGMT_PORT>; set trust-ip enable; config trust-ip-list; edit 1; set type ip-netmask; set ip-network <MGMT_SUBNET>; next; end; next; end` |
| Scripting | Shared Lua table | 7.4.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Platform | FortiADC 320F and 420F | 7.4.3 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Scripting | LB:set_real_server command | 7.4.3 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Scripting | SSL:disable command | 7.4.3 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Scripting | TCP:sockopt type option | 7.4.3 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Troubleshooting | curl in the CLI (execute curl) | 7.4.3 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Logging and alerts | 64-bit SNMP ifXTable counters | 7.4.3 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Server load balancing | Client IP address in a TCP option for Layer 4 TCP virtual servers | 7.4.4 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Global load balancing | Increased GSLB capacity | 7.4.5 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| SSL inspection | SSL forward proxy re-signing key type and size | 7.4.5 and later | ALG `SRG-NET-000062-ALG-000150`; ALG `SRG-NET-000062-ALG-000092` | `config load-balance client-ssl-profile; edit <CLIENT_SSL_PROFILE>; set forward-proxy-resign-cert-type rsa; set forward-proxy-resign-cert-rsa-key-size 2048bit; next; end` |
| Web application firewall | WAF adaptive learning | 7.6.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Web application firewall | Bot detection enhancement | 7.6.0 and later | ALG `SRG-NET-000362-ALG-000112`; ALG `SRG-NET-000390-ALG-000139` | `config security waf profile; edit <WAF_PROFILE>; set bot-detection <BOT_DETECTION>; next; end` |
| Security Fabric | FortiGate Security Fabric connector | 7.6.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | `config system csf; set status disable; end` |
| Web application firewall | OWASP Top 10 compliance dashboard (FortiView) | 7.6.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | `config system global; set owasp-compliance disable; end` |
| Administrator accounts | Administrator lockout controls in the CLI | 7.6.0 and later | NDM `SRG-APP-000065-NDM-000214` | `config system global; set admin-lockout-threshold 3; set admin-lockout-duration 900; end` |
| Administrator accounts | Direct VDOM access for administrators through the root VDOM interface | 7.6.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | `config system global; set admin-bypass-vdom-check disable; end` |
| High availability | HA clusters of up to eight nodes | 7.6.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| High availability | HA management interface network options | 7.6.0 and later | NDM `SRG-APP-000408-NDM-000314`; NDM `SRG-APP-000880-NDM-000290` | `config system ha; set mgmt-status enable; set mgmt-interface <MGMT_PORT>; set mgmt-ip <MGMT_IP>; set mgmt-ip-allowaccess https ssh; end` |
| High availability | Virtual MAC address in active-passive HA | 7.6.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| High availability | CLI commands to force HA nodes into standby | 7.6.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Certificates | ACME TLS-ALPN-01 enhancements | 7.6.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Scripting | Waiting room (virtual queuing) through HTTP scripting | 7.6.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Platform | AWS autoscaling group discovery | 7.6.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Server load balancing | Health check down actions (drop, none, reject) | 7.6.0 and later | ALG `SRG-NET-000365-ALG-000123` | `config load-balance pool; edit <POOL>; set health-check-down-action reject; next; end` |
| Server load balancing | HTTP/3 in HTTP-to-HTTPS redirection | 7.6.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Link load balancing | SLB local traffic in link load balancing | 7.6.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Global load balancing | Multiple global DNS policies in FQDN zones | 7.6.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Global load balancing | Zone-level DNS forwarding with no matching host name | 7.6.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Troubleshooting | DNS forwarding log debug | 7.6.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Platform | FortiFlex with cloud-init in Proxmox (KVM) | 7.6.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Troubleshooting | Health check debug log | 7.6.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Web application firewall | Enhanced file type detection | 7.6.1 and later | ALG `SRG-NET-000019-ALG-000018`; ALG `SRG-NET-000289-ALG-000110` | — |
| Web application firewall | Original client IP for attack source identification (X-Forwarded-For) | 7.6.1 and later | ALG `SRG-NET-000077-ALG-000046` | `config security waf profile; edit <WAF_PROFILE>; set use-original-ip enable; next; end` (only behind a trusted proxy) |
| Network | OSPF version 3 (OSPFv3) | 7.6.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Server load balancing | Server-side HTTP/2 connections | 7.6.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Server load balancing | Client address option for HTTP/3 virtual servers | 7.6.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Scripting | Scripting groups for predefined HTTP scripts | 7.6.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Scripting | HTTP script for error handling | 7.6.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| System | Threat telemetry to FortiGuard (IPS and antivirus statistics) | 7.6.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | `config system global; set fds-statistics disable; end` |
| Time and SNMP | NTP authentication | 7.6.1 and later | NDM `SRG-APP-000395-NDM-000347`; NDM `SRG-APP-000920-NDM-000320` | `config system time ntp; set ntpsync enable; config ntp-server; edit 1; set server <NTP_SERVER>; set authentication enable; set key-type sha256; set key <NTP_KEY>; set key-id <KEY_ID>; next; end; end` |
| Platform | Azure autoscaling for FortiADC VMSS | 7.6.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Time and SNMP | Enhanced SNMP authentication and encryption | 7.6.1 and later | NDM `SRG-APP-000395-NDM-000310`; NDM `SRG-APP-000412-NDM-000331` | `config system snmp user; edit <SNMP_USER>; set security-level authpriv; set auth-proto sha512; set priv-proto aes256; next; end` |
| User authentication | Extended maximum authentication timeout | 7.6.1 and later | ALG `SRG-NET-000213-ALG-000107`; ALG `SRG-NET-000337-ALG-000096` | `config user user-group; edit <USER_GROUP>; set auth-session-timeout 15; next; end` (the period your organization defines) |
| Logging and alerts | Syslog encryption settings | 7.6.1 and later | NDM `SRG-APP-000515-NDM-000325`; ALG `SRG-NET-000334-ALG-000050`; NDM `SRG-APP-000412-NDM-000331` | `config log setting remote; edit <SYSLOG_ID>; set proto tcpssl; set enc-algorithm high; next; end` |
| Logging and alerts | Syslog servers with IPv6 FQDNs | 7.6.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| GUI | Firmware upgrade progress tracking | 7.6.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Platform | Instance types for AWS, Azure, and GCP | 7.6.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| High availability | Status reporting in active-passive HA | 7.6.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Network | Link Layer Discovery Protocol (LLDP) | 7.6.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | `config system global; set lldp-reception disable; set lldp-transmission disable; end` |
| Platform | Data partition expansion | 7.6.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Platform | FortiFlex token in cloud-init user data for public cloud BYOL | 7.6.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| High availability | IPv6 on the HA management interface | 7.6.3 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Network | IPv6 router advertisements | 7.6.3 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Network | IPsec authentication and encryption for OSPFv3 | 7.6.3 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Server load balancing | ESP packets in Layer 4 virtual servers (IPsec VPN without NAT-T) | 7.6.3 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Platform | FortiADC-VMUL license and more VDOMs on virtual appliances | 7.6.3 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Administrator accounts | Access profile from RADIUS or TACACS+ (access profile override) | 7.6.4 and later | NDM `SRG-APP-000153-NDM-000249`; NDM `SRG-APP-000033-NDM-000212` | `config system admin; edit <ADMIN>; set accprofile-override enable; next; end` (only when the server returns the access profile) |
| Logging and alerts | Log export to Apache Kafka | 7.6.4 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Certificates | Local certificate groups of up to 1024 members | 7.6.4+; 8.0.1+ | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Platform | OpenSSL 3.1.8 | 7.6.4 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Platform | OCI Dedicated Region Cloud@Customer (DRCC) | 7.6.4+; 8.0.1+ | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Troubleshooting | CLI commands for virtual server and pool statistics | 7.6.4 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Administrator accounts | VDOM from RADIUS or TACACS+ (VDOM override) | 7.6.5 and later | NDM `SRG-APP-000153-NDM-000249`; NDM `SRG-APP-000033-NDM-000212` | `config system admin; edit <ADMIN>; set vdom-override enable; next; end` (only when the server returns the VDOM) |
| User authentication | Match conditions for user group members | 7.6.5 and later | ALG `SRG-NET-000138-ALG-000089` | — |
| User authentication | Strip the domain prefix from user names | 7.6.6 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Certificates | ACME External Account Binding (EAB) | 7.6.7 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Scripting | Stream scripting with session persistence | 7.6.7 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Global load balancing | GLB object limits of 4096 on all platforms | 7.6.7 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Platform | OpenSSL 3.3.7 | 7.6.7 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Application Access Manager | Application Access Manager menu (authentication modules) | 8.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Application Access Manager | Unified access policy for application access control | 8.0.0 and later | ALG `SRG-NET-000015-ALG-000016`; VPN `SRG-NET-000015-VPN-000010`; VPN `SRG-NET-000019-VPN-000040` | `config load-balance auth-policy; edit <AUTH_POLICY>; set app-access enable; set user-group <USER_GROUP>; set app-portal <APP_PORTAL>; next; end` |
| Application Access Manager | Agentless Application Gateway (AAG: web portal for RDP, VDI, SSH, and web applications for remote users) | 8.0.0 and later | VPN `SRG-NET-000062-VPN-000200`; VPN `SRG-NET-000138-VPN-000490`; VPN `SRG-NET-000166-VPN-000580`; VPN `SRG-NET-000213-VPN-000721`; VPN `SRG-NET-000213-VPN-000720` | `config user app-portal; edit <APP_PORTAL>; set app-group <APP_GROUP>; set user-lifetime <SECONDS>; next; end`; `config load-balance virtual-server; edit <VS>; set auth-policy <AUTH_POLICY>; set client-ssl-profile <CLIENT_SSL_PROFILE>; next; end` |
| Web application firewall | WAF adaptive learning 2.0 | 8.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| GUI | Feature visibility (hide unused features in the web UI) | 8.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| System | WAF signature statistics to FortiGuard | 8.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | `config system global; set fds-statistics disable; end` |
| Server load balancing | Proxy protocol for Layer 4 TCP | 8.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Troubleshooting | Clear session and persistence tables for HTTP and HTTPS virtual servers | 8.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Server load balancing | Up to 64 processes per virtual server | 8.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Scripting | Persistence functions in HTTP data events | 8.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Server load balancing | RFC 7919 compliance with TLS 1.3 in SSL profiles | 8.0.0 and later | ALG `SRG-NET-000062-ALG-000150` | `config load-balance client-ssl-profile; edit <CLIENT_SSL_PROFILE>; set ssl-allowed-versions tlsv1.2 tlsv1.3; set rfc7919-comply enable; next; end` |
| Network security | Source IP exceptions for network DoS protections | 8.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — (keep exceptions to trusted addresses) |
| GUI | Updated navigation menu | 8.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| System | TPM and encrypted data store (private data encryption) | 8.0.0 and later | NDM `SRG-APP-000171-NDM-000258`; ALG `SRG-NET-000755-ALG-000150` | `config system global; set private-data-encryption enable; end` |
| High availability | Azure HA with FortiFlex for up to eight nodes | 8.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Troubleshooting | Hard disk and log disk diagnostics | 8.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Application Access Manager | AAG 8.0.1 features (internal web applications, MFA at portal login, language detection, bookmark icons) | 8.0.1 and later | VPN `SRG-NET-000140-VPN-000500`; ALG `SRG-NET-000140-ALG-000094`; ALG `SRG-NET-000339-ALG-000090` | GUI: Application Access Manager > Agentless Application Gateway |
| Security Fabric | Cisco ACI external connector | 8.0.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Administrator accounts | Administrator SSO through the FortiGate Security Fabric (FortiGate as SAML IdP) | 8.0.1 and later | NDM `SRG-APP-000516-NDM-000336`; NDM `SRG-APP-000153-NDM-000249` | `config system sso-admin; edit <SSO_ADMIN>; set access-profile <PROFILE>; set is-system-admin no; next; end` |
| Web application firewall | WAF signature staging | 8.0.1 and later | ALG `SRG-NET-000019-ALG-000019`; ALG `SRG-NET-000019-ALG-000018` | `config system global; set waf-staging-signature enable; end`; GUI: System > FortiGuard > WAF Signature Staging (review staged signatures promptly) |
| Administrator accounts | Disable the default admin account | 8.0.1 and later | NDM `SRG-APP-000148-NDM-000346` | `config system global; set default-admin disable; end` (after other administrator accounts exist) |
| Server load balancing | Socket selection hash control | 8.0.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Server load balancing | Advanced mutual TLS (client authentication frequency, CA advertisement, and client certificate constrained delegation) | 8.0.1 and later | ALG `SRG-NET-000140-ALG-000094`; ALG `SRG-NET-000166-ALG-000101`; ALG `SRG-NET-000164-ALG-000100` | `config system certificate certificate_verify; edit <VERIFY>; set client-authentication enable; set client-auth-frequency always; next; end` |
| Server load balancing | Transparent proxy and TCP optimization for Layer 7 TCP virtual servers | 8.0.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Server load balancing | Content rewriting for HTTP/3 and back-end HTTP/2 | 8.0.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Global load balancing | Secondary zones with AXFR and TSIG authentication | 8.0.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Global load balancing | User-defined certificates and CA verification for GSLB | 8.0.1 and later | ALG `SRG-NET-000164-ALG-000100`; ALG `SRG-NET-000062-ALG-000150`; ALG `SRG-NET-000510-ALG-000111` | `config global-load-balance servers; edit <SERVER>; set user-defined-certificate enable; set cert <LOCAL_CERT>; set ca-verify enable; set ca-group <CA_GROUP>; next; end` |
| Network security | CLI commands for the TCP DoS block list | 8.0.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Logging and alerts | Traffic log page redesign | 8.0.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Platform | OpenSSL 3.3 | 8.0.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| System | FortiAI Assistant | 8.0.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | `config system global; set fortiai-user disable; end` |
| Server load balancing | More content routing and health check objects | 8.0.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Network | VXLAN for the Kubernetes Calico CNI | 8.0.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| System | FortiAI log analysis | 8.0.3 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Application Access Manager | AAG 8.0.3 features (SLB virtual server integration, shareable bookmarks, user group matching, URL redirection) | 8.0.3 and later | VPN `SRG-NET-000015-VPN-000010`; ALG `SRG-NET-000018-ALG-000017` | GUI: Application Access Manager > Agentless Application Gateway |
| Web application firewall | Web attack signatures for HTTP/3 and HTTP/2 virtual servers | 8.0.3 and later | ALG `SRG-NET-000318-ALG-000152`; ALG `SRG-NET-000318-ALG-000014`; ALG `SRG-NET-000318-ALG-000151` | — |
| Management access | Input security check for the REST API | 8.0.3 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Network security | External ICAP servers for file inspection | 8.0.3 and later | ALG `SRG-NET-000248-ALG-000133`; ALG `SRG-NET-000765-ALG-000170` | `config security antivirus profile; edit <AV_PROFILE>; set icap-server-check enable; next; end`; `config system icapserver; set status enable; set server <ICAP_SERVER>; set ssl enable; end` |
| Network security | FortiSandbox Cloud connection | 8.0.3 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | `config system fortisandbox; set status disable; end` (unless the cloud service is authorized) |
| Server load balancing | TLS 1.3 hardening and post-quantum cryptography | 8.0.3 and later | ALG `SRG-NET-000062-ALG-000150`; ALG `SRG-NET-000510-ALG-000111`; ALG `SRG-NET-000062-ALG-000092` | `config load-balance client-ssl-profile; edit <CLIENT_SSL_PROFILE>; set supported-groups-sigalg-security-level high; next; end` |
| Server load balancing | FQDN real server DNS cache and refresh | 8.0.3 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Scripting | Load balance pools in stream scripts | 8.0.3 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Logging and alerts | Security log page redesign | 8.0.3 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Logging and alerts | Script log page redesign | 8.0.3 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| GUI | User interface reorganization | 8.0.3 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Platform | OpenSSL 3.5 | 8.0.3 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| System | FortiAI virtual server analytics | 8.0.4 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| GUI | Floating FortiAI window | 8.0.4 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Application Access Manager | AAG 8.0.4 features (portal mapping from LDAP and SAML attributes, access tags, branding, auto-launch) | 8.0.4 and later | VPN `SRG-NET-000015-VPN-000010`; ALG `SRG-NET-000015-ALG-000016` | GUI: Application Access Manager > Agentless Application Gateway |
| Web application firewall | WAF profiles in content routing rules | 8.0.4 and later | ALG `SRG-NET-000018-ALG-000017`; ALG `SRG-NET-000019-ALG-000018` | — (not in the 8.0.3 CLI Reference) |
| GUI | In-place editing of virtual server and WAF profile objects | 8.0.4 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| System | Automatic patch firmware upgrades from FortiGuard | 8.0.4 and later | NDM `SRG-APP-000457-NDM-000352`; NDM `SRG-APP-000378-NDM-000302` | — (not in the 8.0.3 CLI Reference; use only under change control) |
| System | Critical vulnerability upgrade prompt at login | 8.0.4 and later | NDM `SRG-APP-001035-NDM-000340` | — |
| Management access | Configurable TLS parameters for the web UI and REST API | 8.0.4 and later | NDM `SRG-APP-000412-NDM-000331`; NDM `SRG-APP-000411-NDM-000330`; NDM `SRG-APP-000179-NDM-000265` | — (not in the 8.0.3 CLI Reference; on 8.0.4, allow only TLS 1.2 and 1.3 and approved ciphers) |
| System | Configuration file encryption | 8.0.4 and later | NDM `SRG-APP-000231-NDM-000271`; ALG `SRG-NET-000755-ALG-000150` | — (not in the 8.0.3 CLI Reference) |
| System | Periodic checksum verification of configuration files | 8.0.4 and later | NDM `SRG-APP-000380-NDM-000304`; NDM `SRG-APP-000516-NDM-000335` | — |
| Server load balancing | Dynamic real server weights from health check scripts | 8.0.4 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Server load balancing | Real server certificate host name verification | 8.0.4 and later | ALG `SRG-NET-000164-ALG-000100`; ALG `SRG-NET-000062-ALG-000150` | — (not in the 8.0.3 CLI Reference) |
| Scripting | LB:get_real_server_weight command | 8.0.4 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Scripting | TCP and UDP payload manipulation in stream scripts | 8.0.4 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Server load balancing | Up to 32 ports or port ranges on a Layer 7 virtual server | 8.0.4 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Global load balancing | Response policy zones (RPZ) | 8.0.4 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Global load balancing | GLB service overview and onboarding page | 8.0.4 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Network security | IPS engine upgrade | 8.0.4 and later | ALG `SRG-NET-000383-ALG-000135` | — |
| Logging and alerts | Event log page redesign | 8.0.4 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Logging and alerts | GLB DNS traffic log enhancements | 8.0.4 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Logging and alerts | Full log disk encryption | 8.0.4 and later | ALG `SRG-NET-000098-ALG-000056`; NDM `SRG-APP-000119-NDM-000236` | — (not in the 8.0.3 CLI Reference) |
| Platform | FortiADC G-Series hardware | 8.0.4 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |

### Requirement reference

The requirements used in the map and in this chapter's text, with their
severity in the current SRG releases:

| SRG | Requirement | Severity | Requirement title |
| --- | --- | --- | --- |
| ALG | `SRG-NET-000015-ALG-000016` | CAT II | The ALG must enforce approved authorizations for logical access to information and system resources by employing identity-based, role-based, and/or attribute-based security policies. |
| ALG | `SRG-NET-000018-ALG-000017` | CAT II | The ALG must enforce approved authorizations for controlling the flow of information within the network based on attribute- and content-based inspection of the source, destination, headers, and/or content of the communications traffic. |
| ALG | `SRG-NET-000019-ALG-000018` | CAT II | The ALG must restrict or block harmful or suspicious communications traffic by controlling the flow of information between interconnected networks based on attribute- and content-based inspection of the source, destination, headers, and/or content of the communications traffic. |
| ALG | `SRG-NET-000019-ALG-000019` | CAT II | The ALG must immediately use updates made to policy enforcement mechanisms such as policy filters, rules, signatures, and analysis algorithms for gateway and/or intermediary functions. |
| ALG | `SRG-NET-000041-ALG-000022` | CAT II | The ALG providing user access control intermediary services must display the Standard Mandatory DoD-approved Notice and Consent Banner before granting access to the network. |
| ALG | `SRG-NET-000062-ALG-000092` | CAT II | The ALG that stores secret or private keys must use FIPS-approved key management technology and processes in the production and control of private/secret cryptographic keys. |
| ALG | `SRG-NET-000062-ALG-000150` | CAT II | The ALG that provides intermediary services for TLS must be configured to comply with the required TLS settings in NIST SP 800-52. |
| ALG | `SRG-NET-000074-ALG-000043` | CAT II | The ALG must produce audit records containing information to establish what type of events occurred. |
| ALG | `SRG-NET-000075-ALG-000044` | CAT II | The ALG must produce audit records containing information to establish when (date and time) the events occurred. |
| ALG | `SRG-NET-000076-ALG-000045` | CAT II | The ALG must produce audit records containing information to establish where the events occurred. |
| ALG | `SRG-NET-000077-ALG-000046` | CAT II | The ALG must produce audit records containing information to establish the source of the events. |
| ALG | `SRG-NET-000078-ALG-000047` | CAT II | The ALG must produce audit records containing information to establish the outcome of the events. |
| ALG | `SRG-NET-000079-ALG-000048` | CAT II | The ALG must generate audit records containing information to establish the identity of any individual or process associated with the event. |
| ALG | `SRG-NET-000088-ALG-000054` | CAT II | The ALG must send an alert to, at a minimum, the information system security officer (ISSO) and system administrator (SA) when an audit processing failure occurs. |
| ALG | `SRG-NET-000098-ALG-000056` | CAT II | The ALG must protect audit information from unauthorized read access. |
| ALG | `SRG-NET-000099-ALG-000057` | CAT II | The ALG must protect audit information from unauthorized modification. |
| ALG | `SRG-NET-000100-ALG-000058` | CAT II | The ALG must protect audit information from unauthorized deletion. |
| ALG | `SRG-NET-000131-ALG-000085` | CAT II | The ALG must not have unnecessary services and functions enabled. |
| ALG | `SRG-NET-000138-ALG-000063` | CAT II | The ALG providing user authentication intermediary services must uniquely identify and authenticate organizational users (or processes acting on behalf of organizational users). |
| ALG | `SRG-NET-000138-ALG-000088` | CAT II | The ALG providing user access control intermediary services must be configured with a pre-established trust relationship and mechanisms with appropriate authorities (e.g., Active Directory or AAA server) which validate user account access authorizations and privileges. |
| ALG | `SRG-NET-000138-ALG-000089` | CAT II | The ALG providing user authentication intermediary services must restrict user authentication traffic to specific authentication server(s). |
| ALG | `SRG-NET-000140-ALG-000094` | CAT II | The ALG providing user authentication intermediary services must use multifactor authentication for network access to non-privileged accounts. |
| ALG | `SRG-NET-000147-ALG-000095` | CAT II | The ALG providing user authentication intermediary services must implement replay-resistant authentication mechanisms for network access to nonprivileged accounts. |
| ALG | `SRG-NET-000164-ALG-000100` | CAT II | The ALG that provides intermediary services for TLS must validate certificates used for TLS functions by performing RFC 5280-compliant certification path validation. |
| ALG | `SRG-NET-000166-ALG-000101` | CAT II | The ALG providing PKI-based user authentication intermediary services must map authenticated identities to the user account. |
| ALG | `SRG-NET-000202-ALG-000124` | CAT II | The ALG must deny network communications traffic by default and allow network communications traffic by exception (i.e., deny all, permit by exception). |
| ALG | `SRG-NET-000213-ALG-000107` | CAT II | The ALG must terminate all network connections associated with a communications session at the end of the session, or as follows: for in-band management sessions (privileged sessions), the session must be terminated after 10 minutes of inactivity; and for user sessions (non-privileged session), the session must be terminated after 15 minutes of inactivity. |
| ALG | `SRG-NET-000228-ALG-000108` | CAT II | The ALG must detect, at a minimum, mobile code that is unsigned or exhibiting unusual behavior, has not undergone a risk assessment, or is prohibited for use based on a risk assessment. |
| ALG | `SRG-NET-000230-ALG-000113` | CAT II | The ALG must protect the authenticity of communications sessions. |
| ALG | `SRG-NET-000233-ALG-000115` | CAT II | The ALG must recognize only system-generated session identifiers. |
| ALG | `SRG-NET-000235-ALG-000118` | CAT II | The ALG must fail to a secure state upon failure of initialization, shutdown, or abort actions. |
| ALG | `SRG-NET-000236-ALG-000119` | CAT II | In the event of a system failure of the ALG function, the ALG must save diagnostic information, log system messages, and load the most current security policies, rules, and signatures when restarted. |
| ALG | `SRG-NET-000246-ALG-000132` | CAT II | The ALG providing content filtering must update malicious code protection mechanisms and signature definitions whenever new releases are available in accordance with organizational configuration management policy. |
| ALG | `SRG-NET-000248-ALG-000133` | CAT II | The ALG providing content filtering must be configured to perform real-time scans of files from external sources at network entry/exit points as they are downloaded and prior to being opened or executed. |
| ALG | `SRG-NET-000249-ALG-000134` | CAT II | The ALG providing content filtering must block malicious code upon detection. |
| ALG | `SRG-NET-000249-ALG-000145` | CAT II | The ALG providing content filtering must delete or quarantine malicious code in response to malicious code detection. |
| ALG | `SRG-NET-000249-ALG-000146` | CAT II | The ALG providing content filtering must send an immediate (within seconds) alert to the system administrator, at a minimum, in response to malicious code detection. |
| ALG | `SRG-NET-000251-ALG-000131` | CAT II | The ALG providing content filtering must update malicious code protection mechanisms and signature definitions whenever new releases are available in accordance with organizational configuration management procedures. |
| ALG | `SRG-NET-000273-ALG-000129` | CAT II | The ALG must generate error messages that provide the information necessary for corrective actions without revealing information that could be exploited by adversaries. |
| ALG | `SRG-NET-000288-ALG-000109` | CAT II | The ALG providing content filtering must block or restrict detected prohibited mobile code. |
| ALG | `SRG-NET-000289-ALG-000110` | CAT II | The ALG providing content filtering must prevent the download of prohibited mobile code. |
| ALG | `SRG-NET-000318-ALG-000014` | CAT II | To protect against data mining, the ALG providing content filtering must prevent code injection attacks from being launched against data storage objects, including, at a minimum, databases, database records, queries, and fields. |
| ALG | `SRG-NET-000318-ALG-000151` | CAT II | To protect against data mining, the ALG providing content filtering must prevent code injection attacks launched against application objects including, at a minimum, application URLs and application code. |
| ALG | `SRG-NET-000318-ALG-000152` | CAT II | To protect against data mining, the ALG providing content filtering must prevent SQL injection attacks launched against data storage objects, including, at a minimum, databases, database records, and database fields. |
| ALG | `SRG-NET-000319-ALG-000015` | CAT II | To protect against data mining, the ALG providing content filtering must detect code injection attacks from being launched against data storage objects, including, at a minimum, databases, database records, queries, and fields. |
| ALG | `SRG-NET-000319-ALG-000020` | CAT II | To protect against data mining, the ALG providing content filtering must detect SQL injection attacks launched against data storage objects, including, at a minimum, databases, database records, and database fields. |
| ALG | `SRG-NET-000319-ALG-000153` | CAT II | To protect against data mining, the ALG providing content filtering as part of its intermediary services must detect code injection attacks launched against application objects including, at a minimum, application URLs and application code. |
| ALG | `SRG-NET-000334-ALG-000050` | CAT II | The ALG must off-load audit records onto a centralized log server. |
| ALG | `SRG-NET-000337-ALG-000096` | CAT II | The ALG providing user authentication intermediary services must require users to reauthenticate when organization-defined circumstances or situations require reauthentication. |
| ALG | `SRG-NET-000339-ALG-000090` | CAT II | The ALG providing user authentication intermediary services must implement multifactor authentication for remote access to nonprivileged accounts such that one of the factors is provided by a device separate from the system gaining access. |
| ALG | `SRG-NET-000344-ALG-000098` | CAT II | The ALG must prohibit the use of cached authenticators after an organization-defined time period. |
| ALG | `SRG-NET-000345-ALG-000099` | CAT II | The ALG providing user authentication intermediary services using PKI-based user authentication must implement a local cache of revocation data to support path discovery and validation in case of the inability to access revocation information via the network. |
| ALG | `SRG-NET-000355-ALG-000117` | CAT II | The ALG providing user authentication intermediary services using PKI-based user authentication must only accept end entity certificates issued by DoD PKI or DoD-approved PKI Certification Authorities (CAs) for the establishment of protected sessions. |
| ALG | `SRG-NET-000362-ALG-000112` | CAT II | The ALG providing content filtering must protect against known and unknown types of Denial of Service (DoS) attacks by employing rate-based attack prevention behavior analysis. |
| ALG | `SRG-NET-000362-ALG-000120` | CAT II | The ALG must implement load balancing to limit the effects of known and unknown types of Denial of Service (DoS) attacks. |
| ALG | `SRG-NET-000362-ALG-000126` | CAT II | The ALG providing content filtering must protect against known types of Denial of Service (DoS) attacks by employing signatures. |
| ALG | `SRG-NET-000362-ALG-000155` | CAT II | The ALG providing content filtering must protect against or limit the effects of known and unknown types of Denial of Service (DoS) attacks by employing pattern recognition pre-processors. |
| ALG | `SRG-NET-000364-ALG-000122` | CAT II | The ALG must only allow incoming communications from organization-defined authorized sources routed to organization-defined authorized destinations. |
| ALG | `SRG-NET-000365-ALG-000123` | CAT II | The ALG must fail securely in the event of an operational failure. |
| ALG | `SRG-NET-000370-ALG-000125` | CAT II | The ALG must identify and log internal users associated with denied outgoing communications traffic posing a threat to external information systems. |
| ALG | `SRG-NET-000380-ALG-000128` | CAT II | The ALG must behave in a predictable and documented manner that reflects organizational and system objectives when invalid inputs are received. |
| ALG | `SRG-NET-000383-ALG-000135` | CAT II | The ALG providing content filtering must be configured to integrate with a system-wide intrusion detection system. |
| ALG | `SRG-NET-000390-ALG-000139` | CAT II | The ALG providing content filtering must continuously monitor inbound communications traffic crossing internal security boundaries for unusual or unauthorized activities or conditions. |
| ALG | `SRG-NET-000391-ALG-000140` | CAT II | The ALG providing content filtering must continuously monitor outbound communications traffic crossing internal security boundaries for unusual/unauthorized activities or conditions. |
| ALG | `SRG-NET-000392-ALG-000141` | CAT II | The ALG providing content filtering must send an alert to, at a minimum, the ISSO and ISSM when detection events occur. |
| ALG | `SRG-NET-000392-ALG-000142` | CAT II | The ALG providing content filtering must generate an alert to, at a minimum, the ISSO and ISSM when threats identified by authoritative sources (e.g., IAVMs or CTOs) are detected. |
| ALG | `SRG-NET-000392-ALG-000148` | CAT II | The ALG providing content filtering must generate an alert to, at a minimum, the ISSO and ISSM when denial of service incidents are detected. |
| ALG | `SRG-NET-000401-ALG-000127` | CAT II | The ALG must check the validity of all data inputs except those specifically identified by the organization. |
| ALG | `SRG-NET-000402-ALG-000130` | CAT II | The ALG must reveal error messages only to the ISSO, ISSM, and SCA. |
| ALG | `SRG-NET-000503-ALG-000038` | CAT II | The ALG providing user access control intermediary services must generate audit records when successful/unsuccessful logon attempts occur. |
| ALG | `SRG-NET-000505-ALG-000039` | CAT II | The ALG providing user access control intermediary services must generate audit records showing starting and ending time for user access to the system. |
| ALG | `SRG-NET-000510-ALG-000111` | CAT II | The ALG providing encryption intermediary services must use NIST FIPS-validated cryptography to implement encryption services. |
| ALG | `SRG-NET-000511-ALG-000051` | CAT II | The ALG must off-load audit records onto a centralized log server in real time. |
| ALG | `SRG-NET-000512-ALG-000062` | CAT II | The ALG must be configured in accordance with the security configuration settings based on DoD security policy and technology-specific security best practices. |
| ALG | `SRG-NET-000512-ALG-000065` | CAT II | The ALG that provides intermediary services for FTP must inspect inbound and outbound FTP communications traffic for protocol compliance and protocol anomalies. |
| ALG | `SRG-NET-000512-ALG-000066` | CAT II | The ALG that provides intermediary services for HTTP must inspect inbound and outbound HTTP traffic for protocol compliance and protocol anomalies. |
| ALG | `SRG-NET-000517-ALG-000006` | CAT II | The ALG providing user access control intermediary services must automatically terminate a user session when organization-defined conditions or trigger events that require a session disconnect occur. |
| ALG | `SRG-NET-000575-ALG-000020` | CAT II | The ALG must use a FIPS-validated cryptographic module to implement encryption services for unclassified information requiring confidentiality. |
| ALG | `SRG-NET-000705-ALG-000110` | CAT II | The ALG must employ organization-defined controls by type of denial of service (DoS) to achieve the DoS objective. |
| ALG | `SRG-NET-000715-ALG-000120` | CAT II | The ALG must implement physically or logically separate subnetworks to isolate organization-defined critical system components and functions. |
| ALG | `SRG-NET-000750-ALG-000140` | CAT II | The ALG must include only approved trust anchors in trust stores or certificate stores managed by the organization. |
| ALG | `SRG-NET-000755-ALG-000150` | CAT II | The ALG must provide protected storage for cryptographic keys with organization-defined safeguards and/or hardware protected key store. |
| ALG | `SRG-NET-000765-ALG-000170` | CAT II | The ALG must implement signature based and/or nonsignature based malicious code protection mechanisms at system entry and exit points to detect and eradicate malicious code. |
| NDM | `SRG-APP-000001-NDM-000200` | CAT II | The network device must limit the number of concurrent sessions to an organization-defined number for each administrator account and/or administrator account type. |
| NDM | `SRG-APP-000026-NDM-000208` | CAT II | The network device must automatically audit account creation. |
| NDM | `SRG-APP-000027-NDM-000209` | CAT II | The network device must automatically audit account modification. |
| NDM | `SRG-APP-000033-NDM-000212` | CAT I | The network device must be configured to assign appropriate user roles or access levels to authenticated users. |
| NDM | `SRG-APP-000038-NDM-000213` | CAT II | The network device must enforce approved authorizations for controlling the flow of management information within the network device based on information flow control policies. |
| NDM | `SRG-APP-000065-NDM-000214` | CAT II | The network device must be configured to enforce the limit of three consecutive invalid logon attempts, after which time it must block any login attempt for 15 minutes. |
| NDM | `SRG-APP-000068-NDM-000215` | CAT II | The network device must display the Standard Mandatory DoD Notice and Consent Banner before granting access to the device. |
| NDM | `SRG-APP-000095-NDM-000225` | CAT II | The network device must produce audit log records containing sufficient information to establish what type of event occurred. |
| NDM | `SRG-APP-000096-NDM-000226` | CAT II | The network device must produce audit records containing information to establish when (date and time) the events occurred. |
| NDM | `SRG-APP-000119-NDM-000236` | CAT II | The network device must protect audit information from unauthorized modification. |
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
| NDM | `SRG-APP-000175-NDM-000262` | CAT I | The network device must be configured to use DoD approved OCSP responders or CRLs to validate certificates used for PKI-based authentication. |
| NDM | `SRG-APP-000179-NDM-000265` | CAT I | The network device must use FIPS 140-2 approved algorithms for authentication to a cryptographic module. |
| NDM | `SRG-APP-000190-NDM-000267` | CAT I | The network device must terminate all network connections associated with a device management session at the end of the session, or the session must be terminated after five minutes of inactivity except to fulfill documented and validated mission requirements. |
| NDM | `SRG-APP-000231-NDM-000271` | CAT I | The network device must only allow authorized administrators to view or change the device configuration, system files, and other files stored either in the device or on removable media (such as a flash drive). |
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
| NDM | `SRG-APP-000457-NDM-000352` | CAT II | The network device must install security-relevant firmware updates within 30 days unless the time period is directed by an authoritative source (e.g., IAVM, CTOs, DTMs, STIGs). |
| NDM | `SRG-APP-000503-NDM-000320` | CAT II | The network device must generate audit records when successful/unsuccessful logon attempts occur. |
| NDM | `SRG-APP-000505-NDM-000322` | CAT II | The network device must generate audit records showing starting and ending time for administrator access to the system. |
| NDM | `SRG-APP-000515-NDM-000325` | CAT II | The network device must off-load audit records onto a different system or media than the system being audited. |
| NDM | `SRG-APP-000516-NDM-000335` | CAT II | The network device must enforce access restrictions associated with changes to the system components. |
| NDM | `SRG-APP-000516-NDM-000336` | CAT I | The network device must be configured to use at least one authentication server for the purpose of authenticating users prior to granting administrative access. For boundary devices, two authentication servers are required. |
| NDM | `SRG-APP-000516-NDM-000340` | CAT II | The network device must be configured to conduct backups of system level information contained in the information system when changes occur. |
| NDM | `SRG-APP-000516-NDM-000344` | CAT II | The network device must obtain its public key certificates from an appropriate certificate policy through an approved service provider. |
| NDM | `SRG-APP-000516-NDM-000350` | CAT I | The network device must be configured to send log data to at least one central log server for the purpose of forwarding alerts to the administrators and the information system security officer (ISSO). For boundary devices, two log servers are required. |
| NDM | `SRG-APP-000820-NDM-000170` | CAT II | The network device must be configured to implement multifactor authentication for local; network; and/or remote access to privileged accounts; and/or nonprivileged accounts such that one of the factors is provided by a device separate from the system gaining access. |
| NDM | `SRG-APP-000825-NDM-000180` | CAT II | The network device must be configured to implement multifactor authentication for local; network; and/or remote access to privileged accounts; and/or nonprivileged accounts such that the device meets organization-defined strength of mechanism requirements. |
| NDM | `SRG-APP-000845-NDM-000220` | CAT II | The network device must be configured to verify, when users create or update passwords, the passwords are not found on the list of commonly used, expected, or compromised passwords in IA-5 (1) (a) for password-based authentication. |
| NDM | `SRG-APP-000875-NDM-000280` | CAT II | The network device must be configured to implement certificate revocation checking to support path discovery and validation for public key-based authentication. |
| NDM | `SRG-APP-000880-NDM-000290` | CAT II | The network device must be configured to protect nonlocal maintenance sessions by separating the maintenance session from other network sessions with the system by logically separated communications paths. |
| NDM | `SRG-APP-000910-NDM-000300` | CAT II | The network device must be configured to include only approved trust anchors in trust stores or certificate stores managed by the organization. |
| NDM | `SRG-APP-000920-NDM-000320` | CAT II | The network device must be configured to synchronize system clocks within and between systems or system components. |
| NDM | `SRG-APP-001035-NDM-000340` | CAT I | The network device hardware and software must be a version supported by the vendor. |
| VPN | `SRG-NET-000015-VPN-000010` | CAT II | The VPN Gateway must enforce approved authorizations for logical access to information and system resources in accordance with applicable access control policies. |
| VPN | `SRG-NET-000019-VPN-000040` | CAT II | The VPN Gateway must ensure inbound and outbound traffic is configured with a security policy in compliance with information flow control policies. |
| VPN | `SRG-NET-000041-VPN-000110` | CAT II | The Remote Access VPN Gateway and/or client must display the Standard Mandatory DOD Notice and Consent Banner before granting remote access to the network. |
| VPN | `SRG-NET-000062-VPN-000200` | CAT I | The TLS VPN Gateway must use TLS 1.2, at a minimum, to protect the confidentiality of sensitive data during transmission for remote access connections. |
| VPN | `SRG-NET-000138-VPN-000490` | CAT II | The VPN Gateway must uniquely identify and authenticate organizational users (or processes acting on behalf of organizational users). |
| VPN | `SRG-NET-000140-VPN-000500` | CAT I | The VPN Gateway must use multifactor authentication (e.g., DoD PKI) for network access to non-privileged accounts. |
| VPN | `SRG-NET-000148-VPN-000540` | CAT II | The VPN Gateway must uniquely identify all network-connected endpoint devices before establishing a connection. |
| VPN | `SRG-NET-000166-VPN-000580` | CAT II | The Remote Access VPN Gateway must use a separate authentication server (e.g., LDAP, RADIUS, TACACS+) to perform user authentication. |
| VPN | `SRG-NET-000213-VPN-000720` | CAT III | The VPN Gateway must terminate all network connections associated with a communications session at the end of the session. |
| VPN | `SRG-NET-000213-VPN-000721` | CAT II | The Remote Access VPN Gateway must terminate remote access network connections after an organization-defined time period. |
| VPN | `SRG-NET-000343-VPN-001370` | CAT II | The VPN Gateway must authenticate all network-connected endpoint devices before establishing a connection. |

### Collecting evidence

Enter `show` in each configuration section that the map cites, at least
`config system global`, `config system admin`, `config system accprofile`,
`config system password-policy`, `config system interface`,
`config system time ntp`, `config system snmp user`,
`config log setting local`, `config log setting remote`,
`config load-balance virtual-server`, `config load-balance profile`,
`config load-balance client-ssl-profile`,
`config load-balance real-server-ssl-profile`,
`config security waf profile`, `config user user-group`, and the IPS,
antivirus, and DoS profiles, and run `get system status` for the release.
Export the event, security, and traffic logs from the central log server,
and keep the FortiGuard update status and the firmware upgrade record with
the checklist.

## Validation and Troubleshooting

- **A feature in the map is missing on your FortiADC.** Check the version
  column against the FortiADC release, and check whether the feature
  depends on the platform, a license, or VDOM mode.
- **A command is rejected.** The command was checked against the 8.0.3 CLI
  Reference. Older releases may lack the option or spell it differently;
  check the CLI Reference of your release, and enter `config global` or
  `config vdom` first when VDOMs are enabled.
- **A profile has no effect.** Profiles apply only through a virtual
  server. Check which virtual server receives the traffic, its type, and
  the profiles it references.
- **Clients fail the TLS handshake after hardening.** Check the allowed
  versions and ciphers in the client SSL profile, the certificate chain,
  and, for mutual TLS, the certificate verify object and its CA group,
  OCSP, and CRL settings.
- **The WAF blocks legitimate requests.** Check the security log for the
  signature or rule that matched, then narrow it with an exception for that
  host or URL rather than lowering the whole profile.
- **A requirement has no matching feature.** Some requirements are met by
  procedure (password changes), by another system (the authentication
  server, the central log server, the time servers), or not at all. Record
  how each requirement is met, not just which feature covers it.

## Security and Best Practices

- Keep FortiADC on a vendor-supported release and install patches
  promptly, after checking the image checksum.
- Set administrator passwords of at least 15 characters, authenticate
  administrators against a remote server that enforces DoD PKI, keep one
  local account of last resort, and disable the default admin account.
- Allow only HTTPS and SSH on the management interface, with trusted
  hosts, the pre-login banner, a 10-minute idle timeout, and lockout after
  three failed logins.
- Send event, security, and traffic logs to a central log server over TLS,
  and use SNMPv3 with SHA-2 authentication and AES privacy only.
- Keep FortiGuard WAF, IPS, antivirus, and IP reputation services current,
  and review this map each time Fortinet publishes a FortiADC release or
  DISA updates the ALG, NDM, or VPN SRG.

## References and Knowledge Checks

**References:**

- Fortinet, *FortiADC Release Notes*, page "What's new", releases 7.0.0 to
  7.0.6, 7.1.0 to 7.1.5, 7.2.0 to 7.2.8, 7.4.0 to 7.4.11, 7.6.0 to 7.6.7,
  and 8.0.0 to 8.0.4 (docs.fortinet.com, FortiADC documentation).
- Fortinet, *FortiADC New Features* guides for 7.6.0 (covering 7.6.0 to
  7.6.7) and 8.0.0 (covering 8.0.0 to 8.0.4).
- Fortinet, *FortiADC 8.0.3 CLI Reference* and *FortiADC 8.0.3
  Administration Guide*.
- DISA Application Layer Gateway SRG V2R4, Network Device Management SRG
  V5R5, and Virtual Private Network SRG V3R5, from the October 2026 STIG
  Library Compilation.
- [Chapter 03](03-the-srg-catalog-how-stigs-are-built-and-what-to-do-without-one.md)
  (SRG-based assessment),
  [Chapter 10](10-fortinet-products-stigs-and-srg-mapping.md) (Fortinet
  products),
  [Chapter 11](11-fortiswitch-feature-version-and-srg-map.md) (the
  FortiSwitch map), and
  [Chapter 12](12-fortianalyzer-feature-version-and-srg-map.md) (the
  FortiAnalyzer map, the model for this chapter).

**Knowledge checks:**

1. Which three SRGs apply to FortiADC, and which part of the appliance or
   which deployment does each one cover?
2. Where does the version data come from for the 7.0 to 7.4 trains, and
   where for the 7.6 and 8.0 trains?
3. Which ALG requirement covers the TLS settings of a client SSL profile,
   and which FortiADC settings help meet it?
4. When does the VPN SRG apply to FortiADC, and which of its requirements
   do not?
5. Which requirements can FortiADC not meet exactly, and how do you handle
   them?
6. What applies to a feature marked "No direct requirement"?

## Summary and Completion Checklist

FortiADC has no STIG, so it is assessed against the ALG SRG for its
application delivery and WAF functions, the NDM SRG for its management
plane, and the VPN SRG where it gives remote users access to internal
applications. This chapter maps 327 features to the FortiADC release
that introduced them, to 150 SRG requirements, and to the FortiADC
command that configures them: 80 core platform features, and
247 features from the FortiADC 7.0.0 through 8.0.4 release notes and
New Features guides. Operational features with no direct requirement fall
under the requirement to disable unnecessary functions when unused.

- [ ] Can find the release that introduced a FortiADC feature.
- [ ] Can map a FortiADC feature to its ALG, NDM, or VPN SRG requirement.
- [ ] Can find the FortiADC command that meets the requirement.
- [ ] Can decide when the VPN SRG applies to FortiADC.
- [ ] Can collect FortiADC evidence and record the requirements FortiADC
  cannot meet exactly.
