# Chapter 18: FortiProxy Feature, Version, and SRG Map

## Learning Objectives

- Find the FortiProxy release that introduced a given feature.
- Map each FortiProxy feature to the Application Layer Gateway (ALG) or
  Network Device Management (NDM) SRG requirement it helps satisfy.
- Find the FortiProxy CLI command that configures each feature to meet its
  requirement.
- Use the map to scope an SRG-based assessment of FortiProxy, which has no
  STIG of its own.
- Decide which ALG requirements apply to a secure web gateway and which do
  not.
- Record the requirements that FortiProxy cannot meet exactly, with their
  mitigations.

## Theory and Architecture

FortiProxy is Fortinet's secure web gateway: an explicit and transparent
web proxy that inspects the web traffic of users on the way out to the
internet. It has **no DISA STIG** (Chapter 10), so it is assessed against
SRGs, as described in Chapter 03. Chapter 10 assigns it two: the
**Application Layer Gateway (ALG) SRG** for the proxy, the intermediary
that terminates user connections, authenticates users, inspects HTTP,
HTTPS, and FTP, and blocks malware, unwanted sites, and data leaks, and the
**Network Device Management (NDM) SRG** for the management plane, the way
administrators log in to and configure the appliance. For every FortiProxy
feature the chapter gives **which FortiProxy release introduced it**,
**which requirement it relates to**, and **which command configures it to
meet that requirement**.

FortiProxy runs an operating system derived from FortiOS, so its CLI looks
like a FortiGate's: `config system global`, `config system admin`,
`config firewall policy`, `config firewall ssl-ssh-profile`, and the
security profiles. The proxy itself (the WAD process) is configured through
a few objects:

- **Explicit proxies** (`config web-proxy explicit-proxy`) listen on an
  internal interface and port for clients that are configured to use the
  proxy, directly or through a PAC file. The explicit FTP proxy
  (`config ftp-proxy explicit`) and SOCKS work the same way.
- **Policies** (`config firewall policy`) carry a policy type. The
  7.6.7 CLI Reference lists `explicit-web`, `explicit-web-connect`,
  `transparent`, `transparent-connect`, `explicit-ftp`, `ssh-tunnel`,
  `ssh`, `access-proxy`, `ztna-proxy`, `wanopt`, and `llm-proxy`.
  Transparent policies intercept web traffic that is routed through
  FortiProxy, so clients need no proxy settings.
- **Authentication schemes and rules** (`config authentication scheme` and
  `config authentication rule`) decide how proxy users are identified:
  basic, digest, form, NTLM, Kerberos (negotiate), certificate, SAML,
  OpenID Connect, FSSO, or a header set by a downstream proxy.
- **Security profiles** applied in a policy do the inspection: SSL/SSH
  inspection, antivirus, web filter, DNS filter, application control, IPS,
  DLP, file filter, video filter, ICAP to an external content analysis
  server, browser isolation, inline CASB, and, from 7.6.4, the LLM
  security gateway.

FortiProxy can also cache web content, optimize WAN traffic, act as a ZTNA
access proxy, and serve WCCP. Several features use Fortinet or third-party
cloud services (FortiGuard, FortiSandbox Cloud, FortiToken Cloud, FortiCloud
single sign-on, browser isolation, and Google reCAPTCHA); those services
are outside the enclave and are not assessed here, so use them only if
they are authorized for your environment.

### Where the version data comes from

Fortinet does not publish a feature matrix or a New Features Guide for
FortiProxy, and the FortiProxy Administration Guide has no "What's new"
chapter: its contents point to the "What's new" section of the Release
Notes. That section is the authoritative per-release list, and Fortinet
publishes it on docs.fortinet.com for every release. The version column was
built from the release notes of all 64 releases Fortinet publishes for the
7.0 to 7.6 trains:

- **7.0 train:** 7.0.0 through 7.0.23.
- **7.2 train:** 7.2.0 through 7.2.16.
- **7.4 train:** 7.4.0 through 7.4.14.
- **7.6 train:** 7.6.0 through 7.6.7.

Each feature is a heading in the "What's new" section. In 7.0.0 to 7.0.2
the headings are grouped under category headings, and the last 7.0.0 group,
"Other new features, enhancements, and changes", is a bulleted list whose
items were taken as entries. In 7.4.0 and 7.6.0 the section spans several
pages, so their features were read from the release notes' table of
contents and, for the 7.4.0 "Other features and changes" page, from that
page's headings. The "CLI changes" tables that many releases add (option
changes listed by bug ID) are not feature entries.

Twelve releases add no features: 7.2.1 has no "What's new" section;
7.0.20, 7.0.23, 7.2.13, 7.2.15, 7.2.16, 7.4.10, 7.4.13, and 7.6.5 say that
they include no new features, enhancements, or changes; and 7.0.14,
7.0.16, and 7.0.18 describe only changes to diagnose commands.

The table has two groups of rows:

- **Core platform features** (categories starting with *Core:*) are the
  long-standing capabilities that the requirements depend on: management
  access, administrator accounts and authentication, password and lockout
  policy, banners, certificates and revocation checking, logging and
  alerts, time, SNMP, FIPS-CC mode, firmware and backups, high
  availability, and the proxy itself (explicit and transparent proxy,
  policies, user authentication, SSL inspection, and the security
  profiles). They existed before FortiProxy 7.0.0 and are not in any of
  these "What's new" lists; they were taken from the FortiProxy 7.6.7 CLI
  Reference and Administration Guide.
- **New features** are the 457 entries of the "What's new"
  sections. The categories of the 7.0.0 to 7.0.2, 7.4.0, and 7.6.0 release
  notes are broad and the other releases have none, so the categories were
  assigned for this chapter, and some titles were lightly edited for
  clarity. An entry listed again in a later release or train is one row
  with all its versions: many 7.0 features were listed again in a 7.2
  release (for example the explicit proxy's passive FTP mode, in 7.0.8 and
  7.2.2), and the Log HTTP Transaction options are listed in 7.0.12,
  7.2.6, 7.2.11, 7.4.0, and 7.4.5.

| Version entry | Meaning |
| --- | --- |
| `7.0.0 or earlier` | A core feature that predates the oldest release notes used (FortiProxy 7.0.0) |
| `7.4.1 and later` | Introduced in FortiProxy 7.4.1 |
| `7.0.8+; 7.2.2+` | Listed in two trains: from 7.0.8 in the 7.0 train and from 7.2.2 in the 7.2 train |

Three cautions apply. First, a feature introduced in a patch release of an
older train may reach a newer train only in a later patch, so "and later"
means later in the same train and, usually, in later trains; when a train
lists the same entry twice (7.0.9 and 7.0.10, for example), the row keeps
the first. Second, many features apply only to some platforms (hardware
models, FortiProxy-VM, or one public cloud) or licenses (license sharing,
browser isolation, DLP, content analysis). Third, a core row records a
FortiProxy capability, but its command was checked against the 7.6.7 CLI
Reference and may differ on an older release; several settings it uses
arrived later, as the new-feature rows say (for example the minimum number
of changed password characters in 7.0.0, TLS 1.3 for LDAP in 7.2.10 and
7.4.4, and RADIUS over TLS in 7.6.0). SSL VPN, which appears in the early
7.0 entries, was removed in 7.0.17, 7.2.10, and 7.4.4.

### Where the SRG data comes from

The SRG column uses requirement IDs from the October 2026 DISA library:

| SRG column | SRG | Release | Applies to |
| --- | --- | --- | --- |
| **ALG** | Application Layer Gateway SRG | V2R4, benchmark date 01 Jul 2026 | The proxy: policies, HTTP, HTTPS, and FTP inspection, SSL inspection, content filtering, malware protection, user authentication and access control for proxy users, and the traffic logs (assigned by Chapter 10) |
| **NDM** | Network Device Management SRG | V5R5, benchmark date 01 Jul 2026 | The management plane: administrator access, authentication, logging, time, SNMP, firmware, and backups (assigned by Chapter 10) |

The ALG SRG is written for every kind of application layer gateway, so not
all of it applies. A web proxy is the case it fits best: the HTTP and FTP
requirements (ALG `SRG-NET-000512-ALG-000066` and
`SRG-NET-000512-ALG-000065`), the content filtering and malicious code
requirements, and the user access control and user authentication
intermediary requirements all apply. The requirements for an ALG that is
part of a cross-domain solution (CDS) do not apply, and neither do the
remote access requirements, now that FortiProxy has no SSL VPN. The SMTP
and spam requirements apply only if the email filter is used, which is
unusual on a web proxy. The SQL and code injection requirements are written
for gateways in front of web applications; for outbound proxy traffic,
IPS signatures detect these attacks.

The requirement IDs are the **rule version IDs** from the XCCDF files, and
the severity is the rule's severity (high = CAT I, medium = CAT II, low =
CAT III). Each feature maps to one of three kinds of relationship:

- **Implements a requirement.** The feature is how FortiProxy meets a
  requirement. Antivirus scanning in proxy mode implements the requirement
  to scan files from external sources in real time (ALG
  `SRG-NET-000248-ALG-000133`), for example.
- **Must be configured to meet a requirement.** The feature is in scope of
  a requirement and has to be set up correctly. SSL deep inspection must
  require TLS 1.2 or later and block untrusted and revoked server
  certificates (ALG `SRG-NET-000062-ALG-000150`), for example.
- **No direct requirement.** The feature is operational, such as a
  dashboard widget, a diagnose command, a platform, a license, or a GUI
  change. It has no requirement of its own, but if it is not needed it
  falls under the ALG requirement not to have unnecessary services and
  functions enabled (ALG `SRG-NET-000131-ALG-000085`); for a
  management-plane function the NDM equivalent is NDM
  `SRG-APP-000142-NDM-000245`.

The mapping is a starting point for an assessment, not a ruling. Confirm it
with your assessor, especially where a requirement is organization-defined
or depends on how FortiProxy is deployed.

### Where the commands come from

Every command was checked against the **FortiProxy 7.6.7 CLI Reference**
(dated 04 September 2026), the newest CLI Reference Fortinet publishes for
FortiProxy, and every web UI pane named in the table against the
**FortiProxy 7.6.7 Administration Guide**. The check was automatic: each
`config` path and nested table, each `set` option against the syntax of the
command it is entered under, each listed option value against the
documented values, and each GUI pane name. Read the column this way:

- Commands run on the FortiProxy CLI, over SSH, the console, or the CLI
  Console in the web UI. With VDOMs enabled, enter `config global` or
  `config vdom` first, as on a FortiGate. Security profiles take effect
  only when a policy uses them; `<SSL_PROFILE>`, `<AV_PROFILE>`,
  `<WF_PROFILE>`, `<IPS_SENSOR>`, and `<APP_LIST>` are their names, and
  `<POLICY_ID>` and `<EXPLICIT_PROXY>` name the policy and the explicit
  proxy.
- **GUI:** entries name the FortiProxy web UI pane.
- Statements are separated by `;` to fit in a table cell; on the CLI, enter
  each one on its own line. Values in `<ANGLE_BRACKETS>` are placeholders
  for your own names, addresses, and keys.
- For **"No direct requirement"** rows, the command shown is the one that
  disables the feature when it is unused. A dash (**—**) means there is
  nothing to change: the feature is a platform, a license, a GUI change, a
  diagnose command, or a capability that is off unless configured.

Some requirements cannot be met exactly with FortiProxy settings. Record
them on the checklist as open findings with mitigations, or meet them
another way:

- **Password rules.** The password policy sets the minimum length (12 to
  128) and the character types, and `min-change-characters` sets the
  minimum number of characters in a new password that are not in the old
  one, which is close to, but not the same as, changing eight positions
  (NDM `SRG-APP-000170-NDM-000329`). There is no check against a list of
  commonly used or compromised passwords (NDM
  `SRG-APP-000845-NDM-000220`). Record the finding, and prefer PKI or
  remote authentication for administrators.
- **VDOM mode.** The 7.6.7 CLI Reference has no syntax entry for turning
  VDOMs on, so the VDOM row has no command. VDOMs separate proxy
  configurations (ALG `SRG-NET-000715-ALG-000120`); enable them as the
  Administration Guide for your release describes.
- **Session lock for proxy users.** A proxy has no user session to lock,
  so the session lock requirements (for example ALG
  `SRG-NET-000514-ALG-000514`) are met, if at all, on the client.
  FortiProxy ends authenticated sessions with the authentication timeout,
  the lifetime timeout, and the reauthentication mode
  (`proxy-auth-timeout`, `proxy-auth-lifetime-timeout`, and
  `proxy-keep-alive-mode`), which the map uses for ALG
  `SRG-NET-000517-ALG-000006`.
- **Cached authenticators.** The LDAP user cache and the authentication
  timeouts keep users authenticated for a time; set them to the period your
  organization defines (ALG `SRG-NET-000344-ALG-000098`).
- **Banner for proxy users.** The web proxy disclaimer (`disclaimer` in the
  policy) shows a notice that users must accept, per user, policy, or
  domain (ALG `SRG-NET-000041-ALG-000022`). It appears only on policies
  that use it, and only to browsers; record how non-browser clients are
  covered.
- **Header-based identity.** The `x-auth-user` method trusts a user name in
  an HTTP header (ALG `SRG-NET-000138-ALG-000063`). Use it only behind a
  trusted downstream proxy, and never on a policy that clients reach
  directly.
- **Settings with no command.** Several rows mapped to a requirement end in
  a dash because the feature is a GUI page, a log field, or a behavior
  change with nothing to set; the ZTNA, OCR, EDM, and HSM rows, for
  example, depend on licenses and designs that this map does not cover.
- **FIPS 140 validation.** FIPS-CC mode (`config system fips-cc`) restricts
  FortiProxy to approved algorithms (NDM `SRG-APP-000179-NDM-000265`, ALG
  `SRG-NET-000510-ALG-000111`). Check the NIST Cryptographic Module
  Validation Program for a current certificate for your FortiProxy release
  before relying on its cryptography.

## Design Considerations

- **Pick the proxy mode deliberately.** An explicit proxy gives the
  clearest user authentication and works through PAC files; a transparent
  proxy needs no client settings but needs routing or WCCP to steer the
  traffic to it. Disable SOCKS, FTP over HTTP, and the explicit
  FTP proxy unless they are required (ALG `SRG-NET-000131-ALG-000086`).
- **Pick the release first, then the features.** If your design depends on
  a feature introduced in a certain release (for example RADIUS over TLS
  in 7.6.0, OpenID Connect in 7.6.2, or post-quantum key exchange in 7.4.14
  and 7.6.7), that sets the minimum FortiProxy release, and it must be a
  vendor-supported release (NDM `SRG-APP-001035-NDM-000340`).
- **Separate management from proxy traffic.** Allow HTTPS and SSH only on a
  dedicated management interface, never on the interfaces where the proxy
  listens, restrict administrators with trusted hosts, and keep HTTP,
  Telnet, and the FortiManager port off where they are not needed.
- **Inspect HTTPS, with care.** SSL deep inspection is what lets the
  security profiles see HTTPS. Re-sign with a DoD-issued subordinate CA
  that the clients trust, block untrusted, expired, and revoked server
  certificates, and exempt only the categories your policy requires.
- **Authenticate every user.** Use DoD PKI certificates, Kerberos, or SAML
  rather than basic authentication, send any password only over TLS, and
  log the user name with every transaction.
- **Deny by default.** Set the explicit proxy's default action to deny,
  write policies that allow by exception, and apply antivirus, web filter,
  application control, and IPS to every allow policy.
- **Turn off what is not used.** Cloud services that are not authorized,
  web caching, WAN optimization, browser isolation, the Security Fabric
  connection, REST API access, and SNMP v1 and v2c are all functions that
  need a reason to stay on.

## Implementation and Automation

### The FortiProxy feature map

The SRG column uses the abbreviations defined in *Where the SRG data comes
from*. The requirement titles are listed in the next table. The command
column follows the conventions in *Where the commands come from*.

| Category | Feature | Introduced (FortiProxy) | SRG requirement(s) | Command to satisfy the requirement |
| --- | --- | --- | --- | --- |
| Core: Management access | Administrative access per interface (HTTPS, SSH, ping, SNMP, HTTP, Telnet, FortiManager, Security Fabric) | 7.0.0 or earlier | NDM `SRG-APP-000142-NDM-000245`; NDM `SRG-APP-000412-NDM-000331`; NDM `SRG-APP-000408-NDM-000314`; NDM `SRG-APP-000172-NDM-000259`; NDM `SRG-APP-000880-NDM-000290` | `config system interface; edit <MGMT_PORT>; set allowaccess https ssh; next; end` (management interface only; leave out HTTP, Telnet, and the other services) |
| Core: Management access | TLS versions and ciphers for HTTPS administration | 7.0.0 or earlier | NDM `SRG-APP-000412-NDM-000331`; NDM `SRG-APP-000411-NDM-000330`; NDM `SRG-APP-000179-NDM-000265` | `config system global; set admin-https-ssl-versions tlsv1-2 tlsv1-3; set ssl-min-proto-version TLSv1-2; set strong-crypto enable; set ssl-static-key-ciphers disable; end` |
| Core: Management access | SSH ciphers, MAC, and key exchange algorithms for administration | 7.0.0 or earlier | NDM `SRG-APP-000412-NDM-000331`; NDM `SRG-APP-000411-NDM-000330`; NDM `SRG-APP-000179-NDM-000265` | `config system ssh-config; set ssh-enc-algo aes256-ctr aes256-gcm@openssh.com; set ssh-mac-algo hmac-sha2-256 hmac-sha2-512; set ssh-kex-algo diffie-hellman-group16-sha512 ecdh-sha2-nistp384; end`; `config system global; set admin-ssh-v1 disable; end` |
| Core: Management access | HTTP-to-HTTPS redirect and Telnet administration | 7.0.0 or earlier | NDM `SRG-APP-000142-NDM-000245`; NDM `SRG-APP-000172-NDM-000259` | `config system global; set admin-https-redirect enable; set admin-telnet disable; end` |
| Core: Management access | Administrative HTTP, HTTPS, SSH, and Telnet port numbers | 7.0.0 or earlier | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Core: Management access | Administration server certificate | 7.0.0 or earlier | NDM `SRG-APP-000516-NDM-000344`; NDM `SRG-APP-000910-NDM-000300` | `config system global; set admin-server-cert <DOD_ISSUED_CERT>; end` |
| Core: Management access | Trusted hosts for each administrator | 7.0.0 or earlier | NDM `SRG-APP-000408-NDM-000314`; NDM `SRG-APP-000038-NDM-000213` | `config system admin; edit <ADMIN>; set trusthost1 <MGMT_SUBNET>; next; end` |
| Core: Management access | Idle timeout for administrator sessions (GUI, SSH, and console) | 7.0.0 or earlier | NDM `SRG-APP-000190-NDM-000267` | `config system global; set admin-timeout 10; set admin-console-timeout 300; end` |
| Core: Management access | Pre-login banner for administrators | 7.0.0 or earlier | NDM `SRG-APP-000068-NDM-000215` | `config system global; set pre-login-banner enable; end` (banner text in `config system replacemsg admin`) |
| Core: Management access | Post-login banner for administrators | 7.0.0 or earlier | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | `config system global; set post-login-banner disable; end` |
| Core: Management access | Concurrent administrator logins | 7.0.0 or earlier | NDM `SRG-APP-000001-NDM-000200` | `config system global; set admin-concurrent disable; end` |
| Core: Management access | TFTP for configuration and firmware transfers | 7.0.0 or earlier | NDM `SRG-APP-000142-NDM-000245` | `config system global; set tftp disable; end` |
| Core: Management access | USB auto-install of configuration and firmware | 7.0.0 or earlier | NDM `SRG-APP-000378-NDM-000302`; NDM `SRG-APP-000516-NDM-000335` | `config system auto-install; set auto-install-config disable; set auto-install-image disable; end` |
| Core: Management access | REST API administrators (API users) | 7.0.0 or earlier | NDM `SRG-APP-000408-NDM-000314`; NDM `SRG-APP-000153-NDM-000249`; NDM `SRG-APP-000142-NDM-000245` | `config system api-user; edit <API_USER>; set accprofile <PROFILE>; config trusthost; edit 1; set ipv4-trusthost <MGMT_SUBNET>; next; end; next; end` |
| Core: Management access | FortiCloud single sign-on for administrators | 7.0.0 or earlier | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | `config system global; set admin-forticloud-sso-login disable; end` |
| Core: Administrator accounts | Local administrator accounts | 7.0.0 or earlier | NDM `SRG-APP-000148-NDM-000346`; NDM `SRG-APP-000153-NDM-000249` | `config system admin; edit <ADMIN>; set accprofile <PROFILE>; set password <PASSWORD_15_CHARS_MIN>; next; end` |
| Core: Administrator accounts | Administrator profiles (none, read, read-write per functional area) | 7.0.0 or earlier | NDM `SRG-APP-000033-NDM-000212`; NDM `SRG-APP-000231-NDM-000271`; NDM `SRG-APP-000380-NDM-000304`; NDM `SRG-APP-000340-NDM-000288` | `config system accprofile; edit <PROFILE>; set sysgrp read; set loggrp read; set fwgrp read; next; end` |
| Core: Administrator accounts | CLI command permissions in administrator profiles (diagnose, execute, config) | 7.0.0 or earlier | NDM `SRG-APP-000340-NDM-000288`; NDM `SRG-APP-000408-NDM-000314` | `config system accprofile; edit <PROFILE>; set cli-diagnose disable; set cli-exec disable; set cli-config disable; next; end` |
| Core: Administrator accounts | Password policy for administrators (length and character types) | 7.0.0 or earlier | NDM `SRG-APP-000164-NDM-000252`; NDM `SRG-APP-000166-NDM-000254`; NDM `SRG-APP-000167-NDM-000255`; NDM `SRG-APP-000168-NDM-000256`; NDM `SRG-APP-000169-NDM-000257` | `config system password-policy; set status enable; set apply-to admin-password; set minimum-length 15; set min-upper-case-letter 1; set min-lower-case-letter 1; set min-number 1; set min-non-alphanumeric 1; end` |
| Core: Administrator accounts | Administrator login lockout | 7.0.0 or earlier | NDM `SRG-APP-000065-NDM-000214` | `config system global; set admin-lockout-threshold 3; set admin-lockout-duration 900; end` |
| Core: Administrator accounts | Local administrator login only when the remote authentication server is down | 7.0.0 or earlier | NDM `SRG-APP-000148-NDM-000346`; NDM `SRG-APP-000516-NDM-000336` | `config system global; set admin-restrict-local enable; end` |
| Core: Administrator accounts | Remote administrator authentication with RADIUS | 7.0.0 or earlier | NDM `SRG-APP-000516-NDM-000336`; NDM `SRG-APP-000153-NDM-000249` | `config user radius; edit <RADIUS>; set server <RADIUS_SERVER>; set secret <SECRET>; set auth-type ms_chap_v2; next; end`; `config user group; edit <ADMIN_GROUP>; set member <RADIUS>; next; end`; `config system admin; edit <ADMIN>; set remote-auth enable; set remote-group <ADMIN_GROUP>; set accprofile <PROFILE>; next; end` |
| Core: Administrator accounts | Remote administrator authentication with LDAP | 7.0.0 or earlier | NDM `SRG-APP-000516-NDM-000336`; NDM `SRG-APP-000153-NDM-000249`; NDM `SRG-APP-000172-NDM-000259` | `config user ldap; edit <LDAP>; set server <LDAP_SERVER>; set secure ldaps; set ca-cert <CA_CERT>; set server-identity-check enable; next; end` |
| Core: Administrator accounts | Remote administrator authentication with TACACS+ | 7.0.0 or earlier | NDM `SRG-APP-000516-NDM-000336`; NDM `SRG-APP-000153-NDM-000249` | `config user tacacs+; edit <TACACS>; set server <TACACS_SERVER>; set key <KEY>; set authen-type auto; set authorization enable; next; end` |
| Core: Administrator accounts | Certificate-based (PKI) administrator login | 7.0.0 or earlier | NDM `SRG-APP-000149-NDM-000247`; NDM `SRG-APP-000177-NDM-000263`; NDM `SRG-APP-000175-NDM-000262`; NDM `SRG-APP-000875-NDM-000280` | `config user peer; edit <PKI_PEER>; set ca <DOD_CA_CERT>; set cn <ADMIN_CN>; set ocsp-override-server <OCSP_SERVER>; next; end`; `config user peergrp; edit <PKI_GROUP>; set member <PKI_PEER>; next; end`; `config system admin; edit <ADMIN>; set peer-auth enable; set peer-group <PKI_GROUP>; next; end`; `config system global; set admin-https-pki-required enable; end` |
| Core: Administrator accounts | Two-factor authentication for administrators (FortiToken, email, SMS) | 7.0.0 or earlier | NDM `SRG-APP-000820-NDM-000170`; NDM `SRG-APP-000825-NDM-000180` | `config system admin; edit <ADMIN>; set two-factor fortitoken; set fortitoken <TOKEN_SERIAL>; next; end` |
| Core: Administrator accounts | Audit of administrator account changes (system event log) | 7.0.0 or earlier | NDM `SRG-APP-000026-NDM-000208`; NDM `SRG-APP-000027-NDM-000209`; NDM `SRG-APP-000343-NDM-000289` | `config log eventfilter; set event enable; set system enable; end` |
| Core: Certificates | CA certificates (trust store) | 7.0.0 or earlier | NDM `SRG-APP-000910-NDM-000300`; ALG `SRG-NET-000750-ALG-000140` | GUI: System > Certificates (keep only DoD and organization-approved CA certificates) |
| Core: Certificates | OCSP and CRL checking for certificates | 7.0.0 or earlier | NDM `SRG-APP-000175-NDM-000262`; NDM `SRG-APP-000875-NDM-000280`; ALG `SRG-NET-000164-ALG-000100`; ALG `SRG-NET-000345-ALG-000099` | `config vpn certificate ocsp-server; edit <OCSP_SERVER>; set url <OCSP_URL>; set cert <OCSP_CERT>; set unavail-action revoke; next; end`; `config vpn certificate setting; set ocsp-status enable; set ocsp-default-server <OCSP_SERVER>; set strict-ocsp-check enable; set check-ca-chain enable; end` |
| Core: Certificates | Certificate revocation lists (CRL) with automatic update | 7.0.0 or earlier | NDM `SRG-APP-000875-NDM-000280`; ALG `SRG-NET-000345-ALG-000099` | `config vpn certificate crl; edit <CRL>; set http-url <CRL_URL>; set update-interval 86400; next; end` |
| Core: Certificates | Private data encryption (encrypt private keys and passwords in the configuration) | 7.0.0 or earlier | NDM `SRG-APP-000171-NDM-000258`; ALG `SRG-NET-000755-ALG-000150` | `config system global; set private-data-encryption enable; end` |
| Core: Logging and alerts | Event logging (system, user, web proxy) | 7.0.0 or earlier | NDM `SRG-APP-000503-NDM-000320`; NDM `SRG-APP-000505-NDM-000322`; NDM `SRG-APP-000095-NDM-000225`; NDM `SRG-APP-000096-NDM-000226`; ALG `SRG-NET-000503-ALG-000038`; ALG `SRG-NET-000505-ALG-000039` | `config log eventfilter; set event enable; set system enable; set user enable; set webproxy enable; end` |
| Core: Logging and alerts | Traffic logging in policies | 7.0.0 or earlier | ALG `SRG-NET-000074-ALG-000043`; ALG `SRG-NET-000075-ALG-000044`; ALG `SRG-NET-000076-ALG-000045`; ALG `SRG-NET-000077-ALG-000046`; ALG `SRG-NET-000078-ALG-000047`; ALG `SRG-NET-000079-ALG-000048`; ALG `SRG-NET-000370-ALG-000125` | `config firewall policy; edit <POLICY_ID>; set logtraffic all; set logtraffic-start enable; next; end` |
| Core: Logging and alerts | Remote syslog over TLS | 7.0.0 or earlier | NDM `SRG-APP-000515-NDM-000325`; NDM `SRG-APP-000516-NDM-000350`; ALG `SRG-NET-000334-ALG-000050`; ALG `SRG-NET-000511-ALG-000051` | `config log syslogd setting; set status enable; set server <SYSLOG_SERVER>; set mode reliable; set enc-algorithm high; set ssl-min-proto-version TLSv1-2; end` |
| Core: Logging and alerts | Logging to FortiAnalyzer (encrypted, reliable, real time) | 7.0.0 or earlier | NDM `SRG-APP-000515-NDM-000325`; NDM `SRG-APP-000516-NDM-000350`; ALG `SRG-NET-000334-ALG-000050`; ALG `SRG-NET-000511-ALG-000051` | `config log fortianalyzer setting; set status enable; set server <FAZ_SERVER>; set certificate-verification enable; set enc-algorithm high; set reliable enable; set upload-option realtime; end` |
| Core: Logging and alerts | Local disk logging, disk-full action, and warning thresholds | 7.0.0 or earlier | NDM `SRG-APP-000357-NDM-000293`; NDM `SRG-APP-000360-NDM-000295`; ALG `SRG-NET-000088-ALG-000054` | `config log disk setting; set status enable; set diskfull nolog; set full-first-warning-threshold 75; set full-second-warning-threshold 90; set full-final-warning-threshold 95; end` |
| Core: Logging and alerts | Alert email | 7.0.0 or earlier | NDM `SRG-APP-000360-NDM-000295`; ALG `SRG-NET-000088-ALG-000054`; ALG `SRG-NET-000249-ALG-000146`; ALG `SRG-NET-000392-ALG-000141`; ALG `SRG-NET-000770-ALG-000180` | `config alertemail setting; set mailto1 <ISSO_EMAIL>; set filter-mode category; set admin-login-logs enable; set antivirus-logs enable; set IPS-logs enable; set configuration-changes-logs enable; set log-disk-usage-warning enable; end`; `config system email-server; set server <SMTP_SERVER>; set security smtps; end` |
| Core: Logging and alerts | Protection of logs through administrator profiles | 7.0.0 or earlier | NDM `SRG-APP-000119-NDM-000236`; ALG `SRG-NET-000098-ALG-000056`; ALG `SRG-NET-000099-ALG-000057`; ALG `SRG-NET-000100-ALG-000058` | `config system accprofile; edit <PROFILE>; set loggrp read; next; end` |
| Core: Time and SNMP | NTP time synchronization with authentication | 7.0.0 or earlier | NDM `SRG-APP-000920-NDM-000320`; NDM `SRG-APP-000395-NDM-000347`; NDM `SRG-APP-000374-NDM-000299` | `config system ntp; set ntpsync enable; set type custom; config ntpserver; edit 1; set server <NTP_SERVER>; set authentication enable; set key-type SHA256; set key <NTP_KEY>; set key-id <KEY_ID>; next; end; end` |
| Core: Time and SNMP | Time zone | 7.0.0 or earlier | NDM `SRG-APP-000374-NDM-000299`; NDM `SRG-APP-000096-NDM-000226` | `config system global; set timezone <TIMEZONE>; end` |
| Core: Time and SNMP | SNMPv3 users | 7.0.0 or earlier | NDM `SRG-APP-000395-NDM-000310`; NDM `SRG-APP-000412-NDM-000331` | `config system snmp user; edit <SNMP_USER>; set security-level auth-priv; set auth-proto sha256; set auth-pwd <AUTH_KEY>; set priv-proto aes256; set priv-pwd <PRIV_KEY>; next; end` |
| Core: Time and SNMP | SNMP v1 and v2c communities | 7.0.0 or earlier | NDM `SRG-APP-000395-NDM-000310`; NDM `SRG-APP-000142-NDM-000245` | `config system snmp community; edit <ID>; set status disable; next; end` |
| Core: System integrity | FIPS-CC mode | 7.0.0 or earlier | NDM `SRG-APP-000179-NDM-000265`; NDM `SRG-APP-000412-NDM-000331`; ALG `SRG-NET-000575-ALG-000020`; ALG `SRG-NET-000510-ALG-000111`; ALG `SRG-NET-000510-ALG-000025`; ALG `SRG-NET-000510-ALG-000040` | `config system fips-cc; set status enable; end` |
| Core: System integrity | Firmware upgrades | 7.0.0 or earlier | NDM `SRG-APP-000131-NDM-000243`; NDM `SRG-APP-000378-NDM-000302`; NDM `SRG-APP-000457-NDM-000352`; NDM `SRG-APP-001035-NDM-000340` | GUI: System > Firmware (FortiProxy verifies the image signature when the image is uploaded) |
| Core: System integrity | FortiGuard connection and automatic updates of antivirus, IPS, and web filter databases | 7.0.0 or earlier | ALG `SRG-NET-000246-ALG-000132`; ALG `SRG-NET-000251-ALG-000131`; ALG `SRG-NET-000019-ALG-000019` | `config system fortiguard; set protocol https; end`; `config system autoupdate schedule; set status enable; set frequency automatic; end` |
| Core: System integrity | Configuration revisions and backups | 7.0.0 or earlier | NDM `SRG-APP-000516-NDM-000340` | `config system global; set revision-backup-on-logout enable; set revision-image-auto-backup enable; end` |
| Core: System integrity | Central management with FortiManager | 7.0.0 or earlier | NDM `SRG-APP-000516-NDM-000340`; NDM `SRG-APP-000516-NDM-000335` | `config system central-management; set type fortimanager; set fmg <FMG_SERVER>; end` |
| Core: High availability | High availability (active-passive and config-sync clusters) | 7.0.0 or earlier | ALG `SRG-NET-000365-ALG-000123`; ALG `SRG-NET-000235-ALG-000118`; ALG `SRG-NET-000236-ALG-000119` | `config system ha; set mode active-passive; set group-name <GROUP>; set password <HA_PASSWORD>; set hbdev <HB_PORT> 50; set encryption enable; set authentication enable; end` |
| Core: Security Fabric | Security Fabric connection | 7.0.0 or earlier | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | `config system csf; set status disable; end` |
| Core: Web proxy | Explicit web proxy (HTTP and HTTPS) | 7.0.0 or earlier | ALG `SRG-NET-000512-ALG-000066`; ALG `SRG-NET-000131-ALG-000086`; ALG `SRG-NET-000132-ALG-000087` | `config web-proxy explicit-proxy; edit <EXPLICIT_PROXY>; set status enable; set interface <INTERNAL_PORT>; set http-incoming-port <PROXY_PORT>; set unknown-http-version reject; set sec-default-action deny; next; end` |
| Core: Web proxy | FTP over HTTP and SOCKS on the explicit web proxy | 7.0.0 or earlier | ALG `SRG-NET-000131-ALG-000086`; ALG `SRG-NET-000132-ALG-000087` | `config web-proxy explicit-proxy; edit <EXPLICIT_PROXY>; set ftp-over-http disable; set socks disable; next; end` (unless required) |
| Core: Web proxy | Explicit FTP proxy | 7.0.0 or earlier | ALG `SRG-NET-000512-ALG-000065`; ALG `SRG-NET-000131-ALG-000086` | `config ftp-proxy explicit; set status disable; end` (unless FTP proxying is required) |
| Core: Web proxy | Transparent proxy policies | 7.0.0 or earlier | ALG `SRG-NET-000512-ALG-000066`; ALG `SRG-NET-000018-ALG-000017` | `config firewall policy; edit <POLICY_ID>; set type transparent; set srcintf <INTERNAL_PORT>; set dstintf <EXTERNAL_PORT>; set srcaddr <INTERNAL_ADDR>; set dstaddr all; set service webproxy; set action accept; next; end` |
| Core: Web proxy | Proxy policies (allow by exception, implicit deny) | 7.0.0 or earlier | ALG `SRG-NET-000202-ALG-000124`; ALG `SRG-NET-000018-ALG-000017`; ALG `SRG-NET-000015-ALG-000016`; ALG `SRG-NET-000364-ALG-000122`; ALG `SRG-NET-000132-ALG-000087` | `config firewall policy; edit <POLICY_ID>; set type explicit-web; set explicit-web-proxy <EXPLICIT_PROXY>; set srcaddr <INTERNAL_ADDR>; set dstaddr <ALLOWED_DST>; set action accept; next; end` (traffic that matches no policy is denied) |
| Core: Web proxy | Security profiles applied in policies | 7.0.0 or earlier | ALG `SRG-NET-000019-ALG-000018`; ALG `SRG-NET-000018-ALG-000017` | `config firewall policy; edit <POLICY_ID>; set utm-status enable; set ssl-ssh-profile <SSL_PROFILE>; set av-profile <AV_PROFILE>; set webfilter-profile <WF_PROFILE>; set ips-sensor <IPS_SENSOR>; set application-list <APP_LIST>; next; end` |
| Core: Web proxy | HTTP protocol options (non-compliant HTTP, oversize files) | 7.0.0 or earlier | ALG `SRG-NET-000512-ALG-000066`; ALG `SRG-NET-000380-ALG-000128`; ALG `SRG-NET-000401-ALG-000127` | `config firewall profile-protocol-options; edit <PROTOCOL_OPTIONS>; config http; set ports 80; set unknown-http-version reject; set oversize-limit <MB>; end; next; end` |
| Core: Web proxy | Web proxy global limits (request and message length, strict web check) | 7.0.0 or earlier | ALG `SRG-NET-000512-ALG-000066`; ALG `SRG-NET-000401-ALG-000127` | `config web-proxy global; set strict-web-check enable; set max-request-length <KB>; set max-message-length <KB>; end` |
| Core: Web proxy | Forwarding servers (proxy chaining) | 7.0.0 or earlier | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Core: Web proxy | Web caching | 7.0.0 or earlier | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | `config firewall policy; edit <POLICY_ID>; set webcache disable; next; end` |
| Core: Web proxy | WAN optimization | 7.0.0 or earlier | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | `config firewall policy; edit <POLICY_ID>; set wanopt disable; next; end` |
| Core: Web proxy | Traffic shaping | 7.0.0 or earlier | ALG `SRG-NET-000705-ALG-000110` | `config firewall shaping-policy; edit <ID>; set traffic-shaper <SHAPER>; next; end` |
| Core: Web proxy | Web proxy disclaimer (user must accept the notice) | 7.0.0 or earlier | ALG `SRG-NET-000041-ALG-000022`; ALG `SRG-NET-000042-ALG-000023` | `config firewall policy; edit <POLICY_ID>; set disclaimer user; next; end` (notice text in the web proxy replacement messages) |
| Core: Web proxy | Replacement messages (block and error pages) | 7.0.0 or earlier | ALG `SRG-NET-000273-ALG-000129`; ALG `SRG-NET-000402-ALG-000130` | GUI: System > Replacement Messages (remove internal details) |
| Core: User authentication | Authentication schemes and rules for proxy users | 7.0.0 or earlier | ALG `SRG-NET-000138-ALG-000063`; ALG `SRG-NET-000138-ALG-000088`; ALG `SRG-NET-000169-ALG-000102`; ALG `SRG-NET-000138-ALG-000089` | `config authentication scheme; edit <AUTH_SCHEME>; set method form; set user-database <LDAP>; next; end`; `config authentication rule; edit <AUTH_RULE>; set srcaddr <INTERNAL_ADDR>; set ip-based enable; set active-auth-method <AUTH_SCHEME>; next; end` |
| Core: User authentication | Kerberos and NTLM (negotiate) authentication | 7.0.0 or earlier | ALG `SRG-NET-000138-ALG-000063`; ALG `SRG-NET-000147-ALG-000095`; ALG `SRG-NET-000400-ALG-000097` | `config authentication scheme; edit <AUTH_SCHEME>; set method negotiate; set kerberos-keytab <KEYTAB>; next; end` |
| Core: User authentication | Client certificate authentication for proxy users | 7.0.0 or earlier | ALG `SRG-NET-000140-ALG-000094`; ALG `SRG-NET-000339-ALG-000090`; ALG `SRG-NET-000166-ALG-000101`; ALG `SRG-NET-000355-ALG-000117`; ALG `SRG-NET-000164-ALG-000100` | `config authentication scheme; edit <AUTH_SCHEME>; set method cert; set user-cert enable; next; end`; `config user peer; edit <PKI_PEER>; set ca <DOD_CA_CERT>; set mandatory-ca-verify enable; next; end` |
| Core: User authentication | SAML authentication for proxy users | 7.0.0 or earlier | ALG `SRG-NET-000138-ALG-000063`; ALG `SRG-NET-000138-ALG-000088` | `config user saml; edit <SAML_SP>; set idp-cert <IDP_CERT>; set require-signed-resp-and-asrt enable; next; end`; `config authentication scheme; edit <AUTH_SCHEME>; set method saml; set saml-server <SAML_SP>; next; end` |
| Core: User authentication | FortiToken two-factor authentication for users | 7.0.0 or earlier | ALG `SRG-NET-000140-ALG-000094`; ALG `SRG-NET-000339-ALG-000090` | `config user local; edit <USER>; set two-factor fortitoken; set fortitoken <TOKEN_SERIAL>; next; end` |
| Core: User authentication | HTTPS for user authentication and basic authentication | 7.0.0 or earlier | ALG `SRG-NET-000400-ALG-000097` | `config user setting; set auth-secure-http enable; set auth-http-basic disable; set auth-ssl-min-proto-version TLSv1-2; end` |
| Core: User authentication | User authentication lockout | 7.0.0 or earlier | ALG `SRG-NET-000138-ALG-000063` | `config user setting; set auth-lockout-threshold 3; set auth-lockout-duration 900; end` |
| Core: User authentication | Authenticated user timeout and lifetime | 7.0.0 or earlier | ALG `SRG-NET-000213-ALG-000107`; ALG `SRG-NET-000517-ALG-000006`; ALG `SRG-NET-000344-ALG-000098`; ALG `SRG-NET-000337-ALG-000096` | `config system global; set proxy-auth-timeout 15; set proxy-auth-lifetime enable; set proxy-auth-lifetime-timeout 480; end` |
| Core: User authentication | Concurrent logins per user | 7.0.0 or earlier | ALG `SRG-NET-000053-ALG-000001` | `config user group; edit <GROUP>; set auth-concurrent-override enable; set auth-concurrent-value 1; next; end` |
| Core: User authentication | Fortinet single sign-on (FSSO) | 7.0.0 or earlier | ALG `SRG-NET-000138-ALG-000063`; ALG `SRG-NET-000138-ALG-000088` | `config user fsso; edit <FSSO_AGENT>; set server <COLLECTOR>; set password <PASSWORD>; set ssl enable; next; end` |
| Core: SSL inspection | SSL deep inspection with certificate checks | 7.0.0 or earlier | ALG `SRG-NET-000062-ALG-000150`; ALG `SRG-NET-000164-ALG-000100`; ALG `SRG-NET-000019-ALG-000018`; ALG `SRG-NET-000248-ALG-000133` | `config firewall ssl-ssh-profile; edit <SSL_PROFILE>; config https; set ports 443; set status deep-inspection; set min-allowed-ssl-version tls-1.2; set unsupported-ssl-version block; set untrusted-server-cert block; set expired-server-cert block; set revoked-server-cert block; set cert-validation-failure block; set cert-validation-timeout block; end; next; end` |
| Core: SSL inspection | Inspection CA certificate (re-signing) | 7.0.0 or earlier | ALG `SRG-NET-000062-ALG-000092`; ALG `SRG-NET-000755-ALG-000150`; ALG `SRG-NET-000750-ALG-000140` | `config firewall ssl-ssh-profile; edit <SSL_PROFILE>; set caname <DOD_ISSUED_SUBCA>; set untrusted-caname <UNTRUSTED_CA>; next; end` |
| Core: SSL inspection | SSL inspection exemptions | 7.0.0 or earlier | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Core: Content filtering | Antivirus scanning in proxy mode | 7.0.0 or earlier | ALG `SRG-NET-000248-ALG-000133`; ALG `SRG-NET-000249-ALG-000134`; ALG `SRG-NET-000765-ALG-000170`; ALG `SRG-NET-000249-ALG-000145` | `config antivirus profile; edit <AV_PROFILE>; config http; set av-scan block; set outbreak-prevention block; set quarantine enable; end; config ftp; set av-scan block; end; set av-virus-log enable; next; end` |
| Core: Content filtering | Antivirus quarantine | 7.0.0 or earlier | ALG `SRG-NET-000249-ALG-000145` | `config antivirus quarantine; set destination disk; end` |
| Core: Content filtering | FortiGuard web filtering by category | 7.0.0 or earlier | ALG `SRG-NET-000019-ALG-000018`; ALG `SRG-NET-000018-ALG-000017` | `config webfilter profile; edit <WF_PROFILE>; config ftgd-wf; config filters; edit 1; set category <CATEGORY_ID>; set action block; next; end; end; next; end` |
| Core: Content filtering | Static URL filter | 7.0.0 or earlier | ALG `SRG-NET-000019-ALG-000018` | `config webfilter urlfilter; edit <ID>; set name <LIST>; config entries; edit 1; set url <URL>; set type wildcard; set action block; next; end; next; end` |
| Core: Content filtering | Web content filters for mobile code (ActiveX, Java applets, scripts) | 7.0.0 or earlier | ALG `SRG-NET-000228-ALG-000108`; ALG `SRG-NET-000288-ALG-000109`; ALG `SRG-NET-000289-ALG-000110` | `config webfilter profile; edit <WF_PROFILE>; set options activexfilter javafilter; next; end` |
| Core: Content filtering | Application control | 7.0.0 or earlier | ALG `SRG-NET-000384-ALG-000136`; ALG `SRG-NET-000385-ALG-000137`; ALG `SRG-NET-000132-ALG-000087`; ALG `SRG-NET-000019-ALG-000018` | `config application list; edit <APP_LIST>; set unknown-application-action block; set unknown-application-log enable; set other-application-log enable; config entries; edit 1; set category <CATEGORY_ID>; set action block; next; end; next; end` |
| Core: Content filtering | Intrusion prevention (IPS) | 7.0.0 or earlier | ALG `SRG-NET-000383-ALG-000135`; ALG `SRG-NET-000390-ALG-000139`; ALG `SRG-NET-000391-ALG-000140`; ALG `SRG-NET-000362-ALG-000126`; ALG `SRG-NET-000192-ALG-000121`; ALG `SRG-NET-000319-ALG-000015`; ALG `SRG-NET-000319-ALG-000153`; ALG `SRG-NET-000319-ALG-000020`; ALG `SRG-NET-000392-ALG-000141`; ALG `SRG-NET-000392-ALG-000142` | `config ips sensor; edit <IPS_SENSOR>; set block-malicious-url enable; set scan-botnet-connections block; config entries; edit 1; set severity high critical; set status enable; set action block; set log enable; next; end; next; end` |
| Core: Content filtering | IPS rate-based signatures | 7.0.0 or earlier | ALG `SRG-NET-000362-ALG-000112`; ALG `SRG-NET-000362-ALG-000155`; ALG `SRG-NET-000392-ALG-000148` | `config ips sensor; edit <IPS_SENSOR>; config entries; edit 2; set rule <RULE_ID>; set rate-count <COUNT>; set rate-duration <SECONDS>; set rate-track src-ip; set action block; next; end; next; end` |
| Core: Content filtering | Data loss prevention (DLP) | 7.0.0 or earlier | ALG `SRG-NET-000391-ALG-000140`; ALG `SRG-NET-000018-ALG-000017` | `config dlp profile; edit <DLP_PROFILE>; config rule; edit 1; set proto http-post ftp; set filter-by sensor; set sensor <DLP_SENSOR>; set action block; next; end; next; end` |
| Core: Content filtering | File filter | 7.0.0 or earlier | ALG `SRG-NET-000019-ALG-000018`; ALG `SRG-NET-000289-ALG-000110` | `config file-filter profile; edit <FF_PROFILE>; config rules; edit 1; set protocol http ftp; set file-type <FILE_TYPES>; set action block; next; end; next; end` |
| Core: Content filtering | ICAP (external content analysis), failing closed | 7.0.0 or earlier | ALG `SRG-NET-000019-ALG-000018`; ALG `SRG-NET-000248-ALG-000133`; ALG `SRG-NET-000365-ALG-000123` | `config icap profile; edit <ICAP_PROFILE>; set request enable; set response enable; set request-failure error; set response-failure error; next; end` |
| Core: Content filtering | DNS filter | 7.0.0 or earlier | ALG `SRG-NET-000019-ALG-000018`; ALG `SRG-NET-000391-ALG-000140` | `config dnsfilter profile; edit <DNS_PROFILE>; set block-botnet enable; set log-all-domain enable; next; end` |
| Core: Content filtering | Email filter | 7.0.0 or earlier | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| GUI and dashboard | GUI-based global search | 7.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| GUI and dashboard | SSL-VPN and IPsec monitor improvements | 7.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| GUI and dashboard | API Preview (REST API requests behind a GUI page) | 7.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| System | Source interface and address for Telnet and SSH client connections | 7.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Content filtering | File filter rules in one-arm sniffer policies | 7.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Network | Explicit DNS server mode with DNS over TLS (DoT) and DNS over HTTPS (DoH) | 7.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| SSL inspection | DNS inspection of DoT and DoH | 7.0.0 and later | ALG `SRG-NET-000019-ALG-000018`; ALG `SRG-NET-000391-ALG-000140` | `config firewall ssl-ssh-profile; edit <SSL_PROFILE>; config dot; set status deep-inspection; end; next; end` |
| Network | Zones | 7.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Web proxy | Selectively forward web requests to an upstream proxy from the transparent proxy | 7.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Network | IPv6 DDNS client for generic DDNS | 7.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| System | IPv6 addresses in backup and restore commands | 7.0.0 and later | NDM `SRG-APP-000516-NDM-000340` | — |
| Policy and objects | Virtual IPs | 7.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| ZTNA | Zero Trust Network Access (access proxy, TCP forwarding access proxy, ZTNA tags) | 7.0.0 and later | ALG `SRG-NET-000015-ALG-000016`; ALG `SRG-NET-000138-ALG-000063`; ALG `SRG-NET-000164-ALG-000100` | — |
| Antivirus | Stream-based antivirus scan in proxy mode for FTP, SFTP, and SCP | 7.0.0 and later | ALG `SRG-NET-000248-ALG-000133`; ALG `SRG-NET-000512-ALG-000065` | `config antivirus profile; edit <AV_PROFILE>; config ftp; set av-scan block; end; config ssh; set av-scan block; end; next; end` |
| Web proxy | TCP window size options | 7.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Antivirus | Threat feeds and outbreak prevention without an antivirus engine scan | 7.0.0 and later | ALG `SRG-NET-000765-ALG-000170`; ALG `SRG-NET-000249-ALG-000134` | `config antivirus profile; edit <AV_PROFILE>; config http; set outbreak-prevention block; set external-blocklist block; end; next; end` |
| Antivirus | Content disarm and reconstruction (CDR) | 7.0.0 and later | ALG `SRG-NET-000228-ALG-000108`; ALG `SRG-NET-000288-ALG-000109`; ALG `SRG-NET-000765-ALG-000170` | `config antivirus profile; edit <AV_PROFILE>; config http; set content-disarm enable; end; next; end` |
| Antivirus | External malware block list | 7.0.0 and later | ALG `SRG-NET-000765-ALG-000170` | `config antivirus profile; edit <AV_PROFILE>; config http; set external-blocklist block; end; next; end` |
| Antivirus | FortiGuard Outbreak Prevention | 7.0.0 and later | ALG `SRG-NET-000765-ALG-000170`; ALG `SRG-NET-000246-ALG-000132` | `config antivirus profile; edit <AV_PROFILE>; config http; set outbreak-prevention block; end; next; end` |
| Web filter | FortiGuard categories for child sexual abuse and terrorism | 7.0.0 and later | ALG `SRG-NET-000019-ALG-000018` | `config webfilter profile; edit <WF_PROFILE>; config ftgd-wf; config filters; edit 1; set category 83; set action block; next; edit 2; set category 96; set action block; next; end; end; next; end` |
| Content filtering | Video filtering | 7.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Web filter | Antiphishing profile enhancements | 7.0.0 and later | ALG `SRG-NET-000019-ALG-000018`; ALG `SRG-NET-000400-ALG-000097` | `config webfilter profile; edit <WF_PROFILE>; config antiphish; set status enable; set default-action block; end; next; end` |
| IPS and application control | Highlighting of on-hold IPS signatures | 7.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| SSL inspection | HTTP/2 support in SSL inspection | 7.0.0 and later | ALG `SRG-NET-000062-ALG-000150`; ALG `SRG-NET-000512-ALG-000066` | `config firewall ssl-ssh-profile; edit <SSL_PROFILE>; set supported-alpn all; next; end` |
| SSL inspection | Multiple certificates in an SSL profile in replace mode | 7.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| SSL inspection | Handling SSL-offloaded traffic from an external decryption device | 7.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| IPS and application control | Filters for application control groups | 7.0.0 and later | ALG `SRG-NET-000384-ALG-000136`; ALG `SRG-NET-000132-ALG-000087` | `config application group; edit <APP_GROUP>; set type filter; set category <CATEGORY_ID>; next; end` |
| Content analysis (ICAP) | Secure (TLS) connections to ICAP remote servers | 7.0.0 and later | ALG `SRG-NET-000062-ALG-000150`; ALG `SRG-NET-000164-ALG-000100` | `config icap remote-server; edit <ICAP_SERVER>; set secure enable; set ca-cert <CA_CERT>; next; end` |
| Content analysis (ICAP) | TCP connection pool for ICAP servers | 7.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Web proxy | Improved WAD traffic dispatcher | 7.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| VPN | Dual-stack IPv4 and IPv6 for SSL VPN | 7.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| VPN | Disable the clipboard in SSL-VPN web-mode RDP connections | 7.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Administrator accounts | Password policy with a minimum number of changed characters | 7.0.0 and later | NDM `SRG-APP-000170-NDM-000329` | `config system password-policy; set min-change-characters 8; end` |
| Certificates | ACME certificate support (Let's Encrypt) | 7.0.0 and later | NDM `SRG-APP-000516-NDM-000344`; NDM `SRG-APP-000910-NDM-000300` | — (use DoD-issued certificates, not public ACME certificates) |
| System | Automatic FortiGuard update schedule frequency | 7.0.0 and later | ALG `SRG-NET-000246-ALG-000132`; ALG `SRG-NET-000251-ALG-000131`; ALG `SRG-NET-000019-ALG-000019` | `config system autoupdate schedule; set status enable; set frequency automatic; end` |
| Security Fabric | Simplified FortiClient EMS pairing with silent approval | 7.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Security Fabric | External threat feed integrations | 7.0.0 and later | ALG `SRG-NET-000019-ALG-000018`; ALG `SRG-NET-000019-ALG-000019` | `config system external-resource; edit <FEED>; set type domain; set resource <FEED_URL>; next; end` |
| Security Fabric | External block list of file hashes (malware hash threat feed) | 7.0.0 and later | ALG `SRG-NET-000765-ALG-000170` | `config system external-resource; edit <FEED>; set type malware; set resource <FEED_URL>; next; end` |
| Security Fabric | External IP block list (threat feed) in policies | 7.0.0 and later | ALG `SRG-NET-000019-ALG-000018`; ALG `SRG-NET-000018-ALG-000017` | `config system external-resource; edit <FEED>; set type address; set resource <FEED_URL>; next; end` |
| Logging and monitoring | Logs for the execution of CLI commands | 7.0.0 and later | NDM `SRG-APP-000101-NDM-000231`; NDM `SRG-APP-000343-NDM-000289` | `config system global; set cli-audit-log enable; end` |
| Logging and monitoring | Real-time logging to FortiAnalyzer | 7.0.0 and later | NDM `SRG-APP-000515-NDM-000325`; ALG `SRG-NET-000334-ALG-000050`; ALG `SRG-NET-000511-ALG-000051` | `config log fortianalyzer setting; set upload-option realtime; end` |
| SSL inspection | TLS 1.3 support | 7.0.0 and later | ALG `SRG-NET-000062-ALG-000150`; NDM `SRG-APP-000412-NDM-000331` | `config system global; set admin-https-ssl-versions tlsv1-2 tlsv1-3; end` |
| Platform | Two disks (logging and web caching) for new VMware deployments | 7.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| GUI and dashboard | More FortiView dashboard widgets | 7.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Logging and monitoring | Content Analyses log in the GUI | 7.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| SSL inspection | Upload and download of the TLS fingerprint library | 7.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Policy and objects | Policy Lookup tool | 7.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| DNS filter | DNS translation | 7.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| User authentication | User name from the X-Authenticated-User HTTP header in authentication schemes | 7.0.0 and later | ALG `SRG-NET-000138-ALG-000063`; ALG `SRG-NET-000735-ALG-000130` | — (accept the header only from a trusted downstream proxy) |
| User authentication | User authentication improvements for large deployments | 7.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Management access | Dedicated management interface in NAT mode | 7.0.0 and later | NDM `SRG-APP-000880-NDM-000290`; NDM `SRG-APP-000408-NDM-000314` | `config system interface; edit <MGMT_PORT>; set dedicated-to management; next; end` |
| User authentication | RAPTOR scheme in authentication scripts | 7.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Web proxy | Forwarding server without DNS lookup | 7.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Diagnostics | CLI statistics for explicit web proxy and SSH proxy traffic | 7.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Web filter | Blocked-image cache management in the GUI | 7.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Policy and objects | FQDN destination addresses no longer cover subdomains | 7.0.0 and later | ALG `SRG-NET-000018-ALG-000017`; ALG `SRG-NET-000202-ALG-000124` | — (use wildcard FQDN addresses where subdomains must match) |
| User authentication | LDAP user cache for explicit and transparent proxy users | 7.0.1 and later | ALG `SRG-NET-000344-ALG-000098` | `config web-proxy global; set ldap-user-cache disable; end` (unless the cache is required for performance) |
| Browser isolation | Masquerade setting for the isolator server | 7.0.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Web proxy | Longer web proxy header content (512 characters) | 7.0.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Web caching and WAN optimization | Larger maximum cache object size | 7.0.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Web filter | IP-based URL rating for SSL exemptions and proxy addresses | 7.0.1 and later | ALG `SRG-NET-000019-ALG-000018` | `config firewall ssl-ssh-profile; edit <SSL_PROFILE>; set ssl-exemption-ip-rating enable; next; end` |
| Web proxy | HTTP domain fronting blocking | 7.0.1 and later | ALG `SRG-NET-000512-ALG-000066`; ALG `SRG-NET-000735-ALG-000130`; ALG `SRG-NET-000019-ALG-000018` | `config firewall profile-protocol-options; edit <PROTOCOL_OPTIONS>; config http; set domain-fronting block; end; next; end` |
| Policy and objects | Web access control based on the body of HTTP POST requests | 7.0.1 and later | ALG `SRG-NET-000018-ALG-000017` | `config firewall proxy-address; edit <PROXY_ADDRESS>; set post-arg enable; next; end` |
| Policy and objects | Pass-through policies | 7.0.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Policy and objects | Export of the policy list to CSV and JSON | 7.0.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| SSL inspection | Client certificate authentication on behalf of the original content server | 7.0.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Content analysis (ICAP) | X-Scan-Progress-Interval header in the ICAP client | 7.0.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Content analysis (ICAP) | ICAP client timeout | 7.0.1 and later | ALG `SRG-NET-000365-ALG-000123` | `config icap profile; edit <ICAP_PROFILE>; set timeout 30; next; end` |
| Content analysis (ICAP) | ICAP load balancing in the GUI | 7.0.1 and later | ALG `SRG-NET-000362-ALG-000120`; ALG `SRG-NET-000365-ALG-000123` | `config icap remote-server-group; edit <ICAP_GROUP>; set ldb-method active-passive; next; end` |
| Content analysis (ICAP) | ICAP scanning for FTP | 7.0.1 and later | ALG `SRG-NET-000512-ALG-000065`; ALG `SRG-NET-000248-ALG-000133` | `config icap profile; edit <ICAP_PROFILE>; set file-transfer ftp; next; end` |
| Web caching and WAN optimization | TLS 1.3 for WAN optimization | 7.0.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Diagnostics | Tracking WAD memory | 7.0.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| User authentication | SAML improvements (external browser, clock-skew tolerance, error messages) | 7.0.1 and later | ALG `SRG-NET-000138-ALG-000063` | `config user saml; edit <SAML_SP>; set clock-tolerance <SECONDS>; next; end` |
| Management access | TLS 1.3 cipher suites and banned ciphers for HTTPS administration | 7.0.1 and later | NDM `SRG-APP-000412-NDM-000331`; NDM `SRG-APP-000179-NDM-000265` | `config system global; set admin-https-ssl-ciphersuites TLS-AES-256-GCM-SHA384 TLS-AES-128-GCM-SHA256; set admin-https-ssl-banned-ciphers SHA1 3DES STATIC; end` |
| Security Fabric | FortiAI integration | 7.0.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Security Fabric | External URL list resources | 7.0.1 and later | ALG `SRG-NET-000019-ALG-000018` | `config system external-resource; edit <FEED>; set type url; set resource <FEED_URL>; next; end` |
| Logging and monitoring | ICAP group and user in logs | 7.0.1 and later | ALG `SRG-NET-000079-ALG-000048` | — |
| Logging and monitoring | More HTTP information in web filter logs | 7.0.1 and later | ALG `SRG-NET-000074-ALG-000043`; ALG `SRG-NET-000077-ALG-000046` | — |
| ZTNA | ZTNA access proxy connected to an SSL-VPN web portal | 7.0.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| ZTNA | UTM scanning of TCP forwarding access proxy traffic | 7.0.2 and later | ALG `SRG-NET-000248-ALG-000133`; ALG `SRG-NET-000019-ALG-000018` | — |
| ZTNA | Higher ZTNA and EMS tag limits | 7.0.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| ZTNA | FQDNs for ZTNA TCP forwarding access proxy | 7.0.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| ZTNA | EMS ZTNA and endpoint tags in user widgets and the Asset Identity Center | 7.0.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| VPN | WebSocket SSL-VPN tunnel | 7.0.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| User authentication | Azure Active Directory as an LDAP authentication source | 7.0.2 and later | ALG `SRG-NET-000138-ALG-000088` | — |
| Logging and monitoring | REST API event logging | 7.0.2 and later | NDM `SRG-APP-000343-NDM-000289`; NDM `SRG-APP-000095-NDM-000225` | `config log setting; set rest-api-set enable; set rest-api-get enable; end`; `config log eventfilter; set rest-api enable; end` |
| Security Fabric | FortiNAC tag connector through the REST API | 7.0.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| System | REST API filter standardization | 7.0.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| SSL inspection | Implicit enforcement of deep inspection for policy matching | 7.0.2 and later | ALG `SRG-NET-000062-ALG-000150`; ALG `SRG-NET-000019-ALG-000018` | — |
| Platform | Power supply (PSU) status monitoring | 7.0.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| User authentication | Limiting the access of non-domain users (negotiate without NTLM) | 7.0.2 and later | ALG `SRG-NET-000138-ALG-000063`; ALG `SRG-NET-000147-ALG-000095` | `config authentication scheme; edit <AUTH_SCHEME>; set method negotiate; set negotiate-ntlm disable; next; end` |
| User authentication | Migration of FortiToken Mobile users to FortiToken Cloud | 7.0.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Network | DNS over TLS for the default FortiGuard DNS servers | 7.0.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| GUI and dashboard | Real-time FortiView monitors for proxy traffic | 7.0.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| GUI and dashboard | Process monitor | 7.0.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Security Fabric | WebSocket for Security Fabric events | 7.0.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Diagnostics | Diagnose command for WAD user counts | 7.0.3 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Policy and objects | Reverse DNS lookup for policy matching | 7.0.4 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Web proxy | New default TCP window type (auto-tuning) in protocol options | 7.0.4 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Policy and objects | SSH policy matching | 7.0.5 and later | ALG `SRG-NET-000018-ALG-000017`; ALG `SRG-NET-000132-ALG-000087` | `config firewall policy; edit <POLICY_ID>; set ssh-policy-check enable; next; end` |
| Policy and objects | CIFS profile removed from policies (set in protocol options) | 7.0.5+; 7.2.4+ | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Security Fabric | External threat feeds through a forwarding server | 7.0.5 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| ZTNA | Device ownership enforcement in policies | 7.0.5 and later | ALG `SRG-NET-000015-ALG-000016` | `config firewall policy; edit <POLICY_ID>; set device-ownership enable; next; end` |
| ZTNA | Custom replacement message for ZTNA virtual hosts | 7.0.5 and later | ALG `SRG-NET-000273-ALG-000129` | — |
| Web proxy | FTPS handling in proxy policies | 7.0.5 and later | ALG `SRG-NET-000512-ALG-000065`; ALG `SRG-NET-000062-ALG-000150` | `config firewall profile-protocol-options; edit <PROTOCOL_OPTIONS>; config ftp; set explicit-ftp-tls enable; end; next; end` |
| Logging and monitoring | Client IP (forwardedfor) field in forward traffic and HTTP transaction logs | 7.0.5 and later | ALG `SRG-NET-000077-ALG-000046` | — |
| User authentication | Domain information for NTLM authentication | 7.0.5 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Network | Policy-based routing | 7.0.6 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| SSL inspection | Default certificate authorities for the web proxy and SSL inspection | 7.0.6 and later | ALG `SRG-NET-000755-ALG-000150`; ALG `SRG-NET-000750-ALG-000140` | `config firewall ssl default-certificate; set default-ca <DOD_ISSUED_SUBCA>; set default-untrusted-ca <UNTRUSTED_CA>; end` |
| User authentication | Reauthentication mode for proxy users | 7.0.6 and later | ALG `SRG-NET-000337-ALG-000096`; ALG `SRG-NET-000517-ALG-000006` | `config system global; set proxy-keep-alive-mode re-authentication; set proxy-re-authentication-time <SECONDS>; end` |
| Web filter | Embedded images in replacement messages | 7.0.6 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| VPN | IPsec tunnel status in the GUI | 7.0.6 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Web caching and WAN optimization | Web cache prefetch settings | 7.0.6 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Content analysis (ICAP) | ICAP server response extension headers | 7.0.6 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Diagnostics | Filtering WAD log messages by process type or ID | 7.0.6 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Security Fabric | Certificate validation for external resources | 7.0.7+; 7.2.0+ | ALG `SRG-NET-000164-ALG-000100`; ALG `SRG-NET-000062-ALG-000150` | `config system external-resource; edit <FEED>; set server-identity-check full; next; end` |
| Web proxy | Detect HTTPS in HTTP requests | 7.0.7+; 7.2.0+ | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | `config firewall policy; edit <POLICY_ID>; set detect-https-in-http-request disable; next; end` |
| System | Auto-script password encryption | 7.0.7+; 7.2.0+ | NDM `SRG-APP-000171-NDM-000258` | `config system auto-script; edit <SCRIPT>; set password <PASSWORD>; next; end` |
| Security Fabric | Quotes removed from external resource URLs | 7.0.7+; 7.2.0+ | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Web proxy | Learn the destination from the SNI in the explicit proxy | 7.0.7 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | `config web-proxy explicit-proxy; edit <EXPLICIT_PROXY>; set learn-dst-from-sni disable; next; end` |
| Logging and monitoring | Logging of pending traffic | 7.0.8+; 7.2.2+ | ALG `SRG-NET-000074-ALG-000043`; ALG `SRG-NET-000078-ALG-000047` | `config web-proxy global; set log-policy-pending enable; end` |
| Web proxy | Passive FTP mode for the explicit FTP proxy | 7.0.8+; 7.2.2+ | ALG `SRG-NET-000512-ALG-000065` | `config ftp-proxy explicit; set server-data-mode passive; end` |
| Logging and monitoring | First hard disk for logging only | 7.0.8+; 7.2.2+ | NDM `SRG-APP-000357-NDM-000293` | — |
| SSL inspection | Toggle TLS fingerprint updates | 7.0.8+; 7.2.2+ | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | `config system global; set update-tls-finger-print disable; end` |
| Platform | Alibaba Cloud (AliCloud) platform | 7.0.8+; 7.2.2+ | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Content analysis (ICAP) | Health check of ICAP remote servers | 7.0.9+; 7.2.3+ | ALG `SRG-NET-000365-ALG-000123` | `config icap remote-server; edit <ICAP_SERVER>; set healthcheck enable; set healthcheck-service <SERVICE>; next; end` |
| GUI and dashboard | Forward server status monitoring | 7.0.9+; 7.2.3+ | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Diagnostics | Diagnose commands for conntrack | 7.0.9+; 7.2.3+ | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Diagnostics | Diagnose command for IP set lists | 7.0.9+; 7.2.3+ | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| High availability | Hold the primary config-sync unit before upgrading or rebooting | 7.0.9+; 7.2.3+ | ALG `SRG-NET-000365-ALG-000123` | `config system ha; set primary-hold-before-reboot <SECONDS>; end` |
| Policy and objects | FQDNs from a domain list matched against the SNI of HTTPS requests | 7.0.9+; 7.2.3+ | ALG `SRG-NET-000018-ALG-000017` | — |
| Policy and objects | Local URL list as a policy data source | 7.0.9+; 7.2.3+ | ALG `SRG-NET-000018-ALG-000017`; ALG `SRG-NET-000019-ALG-000018` | — |
| Diagnostics | Process file access monitoring | 7.0.9+; 7.2.3+ | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| User authentication | Detection of configuration changes in Windows Active Directory | 7.0.9+; 7.2.3+ | ALG `SRG-NET-000138-ALG-000088` | `config user domain-controller; edit <DC>; set change-detection enable; next; end` |
| Diagnostics | Memory diagnosis of all WAD processes | 7.0.9+; 7.2.3+ | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Web proxy | Domain fronting action (allow, block, monitor) | 7.0.9+; 7.2.3+ | ALG `SRG-NET-000512-ALG-000066`; ALG `SRG-NET-000735-ALG-000130` | `config firewall profile-protocol-options; edit <PROTOCOL_OPTIONS>; config http; set domain-fronting block; end; next; end` |
| Security Fabric | Fabric device configuration removed | 7.0.9+; 7.2.3+ | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Content analysis (ICAP) | ICAP server scan size limit | 7.0.10+; 7.2.4+ | ALG `SRG-NET-000248-ALG-000133` | `config icap profile; edit <ICAP_PROFILE>; set scan-size-limit <MB>; next; end` |
| GUI and dashboard | Forward server monitoring enhancements (state column) | 7.0.10+; 7.2.4+ | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Diagnostics | Diagnosing interface transceivers | 7.0.10+; 7.2.4+ | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Administrator accounts | Trusted hosts table for administrators (more than ten) | 7.0.10+; 7.2.3+ | NDM `SRG-APP-000408-NDM-000314`; NDM `SRG-APP-000038-NDM-000213` | `config system admin; edit <ADMIN>; config trusthosts; edit 1; set ipv4 <MGMT_SUBNET>; next; end; next; end` |
| Content analysis (ICAP) | HTTP header content forwarded to ICAP | 7.0.10+; 7.2.3+ | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Web proxy | Forward server masquerade disabled by default | 7.0.10 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| SSL inspection | New default certificate for SSL servers | 7.0.10+; 7.2.4+ | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| SSL inspection | Minimum allowed SSL version applies only to deep inspection | 7.0.10+; 7.2.4+ | ALG `SRG-NET-000062-ALG-000150` | `config firewall ssl-ssh-profile; edit <SSL_PROFILE>; config https; set status deep-inspection; set min-allowed-ssl-version tls-1.2; end; next; end` |
| High availability | Unicast heartbeat removed from config-sync mode | 7.0.10+; 7.2.4+ | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| User authentication | User authentication timeout removed from user settings | 7.0.10+; 7.2.4+ | ALG `SRG-NET-000344-ALG-000098`; ALG `SRG-NET-000337-ALG-000096` | `config system global; set proxy-auth-timeout 15; end` |
| GUI and dashboard | Sensor status monitoring | 7.0.11+; 7.2.5+ | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| User authentication | Destination addresses in authentication rules | 7.0.11+; 7.2.5+ | ALG `SRG-NET-000138-ALG-000063` | `config authentication rule; edit <AUTH_RULE>; set dstaddr <DST_ADDR>; next; end` |
| Logging and monitoring | More details in the HTTP transaction log | 7.0.11+; 7.2.5+ | ALG `SRG-NET-000074-ALG-000043` | — |
| Security Fabric | Alibaba Cloud SDN connector | 7.0.11+; 7.2.5+ | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| GUI and dashboard | Forward Server Monitor widget column renamed | 7.0.11 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Platform | FortiProxy G-series models | 7.0.11+; 7.2.5+ | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Logging and monitoring | Log HTTP Transaction options in policies and web proxy settings | 7.0.12+; 7.2.6+; 7.4.0+ | ALG `SRG-NET-000074-ALG-000043`; ALG `SRG-NET-000079-ALG-000048` | `config firewall policy; edit <POLICY_ID>; set log-http-transaction enable; next; end` |
| System | Rating information in REST API responses | 7.0.13+; 7.2.7+; 7.4.1+ | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Logging and monitoring | Improved ICAP error logs | 7.0.15+; 7.2.7+; 7.4.1+ | ALG `SRG-NET-000074-ALG-000043` | — |
| Antivirus | ZSTD HTTP encoding in antivirus scanning | 7.0.17+; 7.2.10+; 7.4.4+ | ALG `SRG-NET-000248-ALG-000133` | — |
| Management access | FortiManager (fgfm) port disabled by default | 7.0.17+; 7.2.10+; 7.4.4+ | NDM `SRG-APP-000142-NDM-000245` | — (allow fgfm only on the interface that faces FortiManager) |
| Platform | PSU status monitoring for FPX-400G | 7.0.17+; 7.2.10+; 7.4.4+ | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| VPN | SSL VPN no longer supported | 7.0.17+; 7.2.10+; 7.4.4+ | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| User authentication | Higher limit for authentication rules | 7.0.19+; 7.2.12+; 7.4.5+ | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Web filter | FortiGuard web filter categories for AI and cryptocurrency | 7.0.21+; 7.2.14+; 7.4.1+ | ALG `SRG-NET-000019-ALG-000018` | `config webfilter profile; edit <WF_PROFILE>; config ftgd-wf; config filters; edit <ID>; set category <CATEGORY_ID>; set action block; next; end; end; next; end` |
| Browser isolation | Browser isolation (FortiNBI) | 7.2.0 and later | ALG `SRG-NET-000765-ALG-000170`; ALG `SRG-NET-000228-ALG-000108` | `config firewall policy; edit <POLICY_ID>; set isolator-profile <ISOLATOR_PROFILE>; next; end` |
| Licensing | License sharing | 7.2.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Licensing | HA license sharing behavior change | 7.2.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| System | Virtual domains (VDOMs) | 7.2.0 and later | ALG `SRG-NET-000715-ALG-000120`; NDM `SRG-APP-000038-NDM-000213` | — (no VDOM mode setting found in the 7.6.7 CLI Reference syntax) |
| Logging and monitoring | Correlation log (forward traffic and HTTP transaction logs by session) | 7.2.0 and later | ALG `SRG-NET-000074-ALG-000043` | — |
| Network | VXLAN | 7.2.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Logging and monitoring | Automation stitches | 7.2.0 and later | NDM `SRG-APP-000360-NDM-000295`; NDM `SRG-APP-000795-NDM-000130`; ALG `SRG-NET-000392-ALG-000141` | `config system automation-trigger; edit <TRIGGER>; set event-type config-change; next; end`; `config system automation-action; edit <ACTION>; set action-type email; set email-to <ISSO_EMAIL>; next; end`; `config system automation-stitch; edit <STITCH>; set trigger <TRIGGER>; config actions; edit 1; set action <ACTION>; next; end; next; end` |
| System | Inter-VDOM links | 7.2.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Network | Cross-VDOM VLANs | 7.2.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Web proxy | Reverse proxy server support (server load balancing virtual IPs) | 7.2.3 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Logging and monitoring | Event logs for source port usage | 7.2.3 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Traffic shaping | Shared and per-IP traffic shapers | 7.2.4 and later | ALG `SRG-NET-000705-ALG-000110` | `config firewall shaper per-ip-shaper; edit <SHAPER>; set max-bandwidth <KBPS>; set max-concurrent-session <SESSIONS>; next; end` |
| Licensing | License usage history | 7.2.4+; 7.4.0+ | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Logging and monitoring | Port exhaustion alerts in the GUI | 7.2.4 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Network | Forwarding domains in transparent mode | 7.2.4 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Web filter | Strict and safe search on Qwant | 7.2.4 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Licensing | License sharing enhancements | 7.2.5+; 7.4.1+; 7.6.4+ | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Logging and monitoring | JSON log format for syslog | 7.2.6+; 7.4.1+ | ALG `SRG-NET-000334-ALG-000050` | `config log syslogd setting; set format json; end` |
| Licensing | License usage history for Browser Isolation and Content Analysis licenses | 7.2.6 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Browser isolation | Browser isolation (FortiNBI) enhancements | 7.2.6+; 7.4.0+ | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Web proxy | Forwarding FTP and SOCKS traffic to a forwarding server | 7.2.7+; 7.4.1+ | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Web proxy | Reuse of the incoming port to connect to the server | 7.2.7+; 7.4.1+ | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| System | GUI support for VDOM links | 7.2.7+; 7.4.1+ | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| GUI and dashboard | Active Sessions removed from global and VDOM resources | 7.2.7+; 7.4.1+ | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Traffic shaping | Schedules for shaping policies | 7.2.8+; 7.4.2+ | ALG `SRG-NET-000705-ALG-000110` | `config firewall shaping-policy; edit <ID>; set schedule <SCHEDULE>; next; end` |
| Web proxy | SOCKS proxy enhancements (UTM scanning of HTTP and HTTPS over SOCKS) | 7.2.8+; 7.4.2+ | ALG `SRG-NET-000131-ALG-000086`; ALG `SRG-NET-000248-ALG-000133` | `config web-proxy explicit-proxy; edit <EXPLICIT_PROXY>; set socks disable; next; end` (unless required) |
| Web proxy | Option to enable the HTTP and HTTPS proxy | 7.2.8+; 7.4.2+ | ALG `SRG-NET-000131-ALG-000086` | `config web-proxy explicit-proxy; edit <EXPLICIT_PROXY>; set http enable; next; end` |
| GUI and dashboard | DNS lookup tool | 7.2.8+; 7.4.2+ | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Browser isolation | GUI support for isolator settings | 7.2.8 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| User authentication | Case sensitivity for user names | 7.2.8+; 7.4.2+ | ALG `SRG-NET-000138-ALG-000063` | `config system global; set username-case-sensitivity enable; end` |
| Diagnostics | More details for diagnosing ICAP servers | 7.2.8+; 7.4.2+ | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Security Fabric | Higher threat feed size limit | 7.2.8+; 7.4.2+ | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| GUI and dashboard | Reordering server URLs by drag and drop | 7.2.9+; 7.4.3+ | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Antivirus | Password-protected (encrypted) archive handling | 7.2.9+; 7.4.3+ | ALG `SRG-NET-000249-ALG-000134`; ALG `SRG-NET-000765-ALG-000170` | `config firewall profile-protocol-options; edit <PROTOCOL_OPTIONS>; set encrypted-file block; set encrypted-file-log enable; next; end` |
| Licensing | FortiAnalyzer or Cloud Logging optional for license sharing | 7.2.9+; 7.4.3+ | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Licensing | Manual license upload in air-gapped environments | 7.2.10 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Logging and monitoring | Shaper fields in traffic logs | 7.2.10+; 7.4.4+ | ALG `SRG-NET-000074-ALG-000043` | — |
| Traffic shaping | Names for traffic shaping policies | 7.2.10+; 7.4.4+ | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Web proxy | Forwarding server protocol in the GUI | 7.2.10+; 7.4.4+ | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Web proxy | Forwarding server for FTP policies in the GUI | 7.2.10+; 7.4.4+ | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Web proxy | Source port of the active-mode FTP data session | 7.2.10+; 7.4.4+ | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Logging and monitoring | Client IP from headers for logging only | 7.2.10+; 7.4.4+ | ALG `SRG-NET-000077-ALG-000046`; ALG `SRG-NET-000735-ALG-000130` | `config web-proxy global; set learn-client-ip log-only; end` |
| User authentication | TLS 1.3 for LDAP connections | 7.2.10+; 7.4.4+ | ALG `SRG-NET-000400-ALG-000097`; NDM `SRG-APP-000172-NDM-000259` | `config user ldap; edit <LDAP>; set secure ldaps; set ssl-min-proto-version TLSv1-2; set ssl-max-proto-version TLSv1-3; next; end` |
| Logging and monitoring | Logging behavior for HTTP CONNECT | 7.2.11+; 7.4.5+ | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Content analysis (ICAP) | "204 allow" and "Preview" headers for ICAP servers | 7.2.11+; 7.4.4+ | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| DLP and file filter | DLP profiles in the GUI | 7.4.0 and later | ALG `SRG-NET-000391-ALG-000140` | — |
| DLP and file filter | DLP backend and configuration enhancements | 7.4.0 and later | ALG `SRG-NET-000391-ALG-000140`; ALG `SRG-NET-000018-ALG-000017` | — |
| DLP and file filter | Optical character recognition (OCR) | 7.4.0 and later | ALG `SRG-NET-000391-ALG-000140` | — |
| ZTNA | ZTNA device certificate verification from EMS for SSL VPN | 7.4.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| ZTNA | Publishing ZTNA services through the ZTNA portal | 7.4.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| ZTNA | ZTNA inline CASB for SaaS application access control | 7.4.0 and later | ALG `SRG-NET-000018-ALG-000017` | — |
| ZTNA | ZTNA policy control of unmanageable and unknown devices | 7.4.0 and later | ALG `SRG-NET-000015-ALG-000016` | — |
| Web proxy | HTTP/2 connection coalescing and multiplexing (ZTNA, load balancing, explicit proxy) | 7.4.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Web proxy | Secure (HTTPS) explicit proxy | 7.4.0 and later | ALG `SRG-NET-000400-ALG-000097`; ALG `SRG-NET-000062-ALG-000150` | `config web-proxy explicit-proxy; edit <EXPLICIT_PROXY>; set secure-web-proxy enable; set secure-web-proxy-cert <CERT>; next; end` |
| Web proxy | HTTPS download of PAC files | 7.4.0 and later | ALG `SRG-NET-000062-ALG-000150` | `config web-proxy explicit-proxy; edit <EXPLICIT_PROXY>; set pac-file-through-https enable; next; end` |
| Web proxy | Implicit web proxy browser extension | 7.4.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Web proxy | Edge and Internet Explorer user agent matching for proxy addresses | 7.4.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Logging and monitoring | Updated System Events log page | 7.4.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Logging and monitoring | Security Events log page | 7.4.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Logging and monitoring | Improved FortiAnalyzer log caching | 7.4.0 and later | ALG `SRG-NET-000334-ALG-000050` | — |
| Logging and monitoring | FortiAnalyzer Reports page | 7.4.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Logging and monitoring | New and consolidated log reports and settings | 7.4.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Logging and monitoring | Logs Sent Daily chart for remote logging | 7.4.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Logging and monitoring | New fields in ZTNA traffic and HTTP transaction logs | 7.4.0 and later | ALG `SRG-NET-000074-ALG-000043` | — |
| Antivirus | FortiSandbox inline scanning | 7.4.0 and later | ALG `SRG-NET-000765-ALG-000170`; ALG `SRG-NET-000249-ALG-000134` | `config antivirus profile; edit <AV_PROFILE>; set fortisandbox-mode inline; next; end` |
| Antivirus | Antivirus exempt list by file hash | 7.4.0 and later | ALG `SRG-NET-000765-ALG-000170` | — (keep exemptions to approved files) |
| Antivirus | Automatic regional discovery for FortiSandbox Cloud | 7.4.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Browser isolation | New and consolidated isolator settings | 7.4.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Web filter | URL Lookup tab | 7.4.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| User authentication | Extra servers for domain controllers | 7.4.0 and later | ALG `SRG-NET-000138-ALG-000088` | — |
| Web filter | Image analyzer for images with unknown FortiGuard categories | 7.4.0 and later | ALG `SRG-NET-000019-ALG-000018` | `config webfilter profile; edit <WF_PROFILE>; set ia-categorization enable; next; end` |
| SSL inspection | HTTP/3 and QUIC deep and certificate inspection; DNS over QUIC and HTTP/3 | 7.4.1 and later | ALG `SRG-NET-000062-ALG-000150`; ALG `SRG-NET-000019-ALG-000018` | `config firewall ssl-ssh-profile; edit <SSL_PROFILE>; config https; set quic inspect; end; next; end` |
| CASB | Inline CASB security profile | 7.4.1 and later | ALG `SRG-NET-000018-ALG-000017`; ALG `SRG-NET-000019-ALG-000018` | `config firewall policy; edit <POLICY_ID>; set casb-profile <CASB_PROFILE>; next; end` |
| IPS and application control | Inline IPS for proxy traffic | 7.4.1 and later | ALG `SRG-NET-000383-ALG-000135`; ALG `SRG-NET-000390-ALG-000139`; ALG `SRG-NET-000391-ALG-000140` | `config firewall policy; edit <POLICY_ID>; set ips-sensor <IPS_SENSOR>; next; end` |
| Network | Internet Service Database (ISDB) policy routing | 7.4.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Licensing | DLP license for HTTP and FTP over HTTP scanning | 7.4.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| SSL inspection | Multiple server certificates for proxy servers | 7.4.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Policy and objects | IPv6 proxy addresses | 7.4.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Policy and objects | Policy matching by application and URL category | 7.4.2 and later | ALG `SRG-NET-000018-ALG-000017` | — |
| Certificates | SSL keyring encryption | 7.4.2 and later | ALG `SRG-NET-000755-ALG-000150` | — |
| Web proxy | Pre-populated list of HTTP incoming IP addresses for the explicit proxy | 7.4.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| System | Panic logging | 7.4.2 and later | ALG `SRG-NET-000236-ALG-000119` | — |
| Licensing | DLP license changes | 7.4.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Web proxy | IPv6 for the explicit FTP proxy and web proxy forwarding servers | 7.4.3 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Web proxy | Protocol detection of traffic tunneled over SOCKS | 7.4.3 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Policy and objects | URL category policy matching in the GUI | 7.4.3 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Security Fabric | Global external resource size limit | 7.4.3 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Platform | AWS ARM64 | 7.4.3 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| DLP and file filter | Exact data match (EDM) in the GUI | 7.4.4 and later | ALG `SRG-NET-000391-ALG-000140` | — |
| SSL inspection | Control of TLS connections that use Encrypted Client Hello (ECH) | 7.4.4 and later | ALG `SRG-NET-000062-ALG-000150`; ALG `SRG-NET-000019-ALG-000018` | `config firewall ssl-ssh-profile; edit <SSL_PROFILE>; config https; set encrypted-client-hello block; end; next; end` |
| User authentication | Import and export of SAML IdP metadata | 7.4.4 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| User authentication | CORS content in the explicit proxy with session-based authentication | 7.4.4 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Antivirus | Block action for FortiSandbox inline scanning in the GUI | 7.4.4 and later | ALG `SRG-NET-000249-ALG-000134` | `config antivirus profile; edit <AV_PROFILE>; config http; set fortisandbox block; end; next; end` |
| System | Panic logging for G-series models | 7.4.4 and later | ALG `SRG-NET-000236-ALG-000119` | — |
| Web filter | Policy matching and web filtering by risk level | 7.4.5 and later | ALG `SRG-NET-000019-ALG-000018` | `config firewall policy; edit <POLICY_ID>; set url-risk <RISK_LEVEL>; next; end` |
| Certificates | SNMP trap for local certificate expiration | 7.4.5 and later | NDM `SRG-APP-000516-NDM-000344` | `config system snmp user; edit <SNMP_USER>; set events cert-expiry; next; end` |
| Web proxy | Forwarding to an upstream proxy port without DNS resolution | 7.4.5 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Logging and monitoring | IP Tables Events under System Events | 7.4.5 and later | ALG `SRG-NET-000074-ALG-000043` | — |
| DLP and file filter | OCR enhancements (HTTP PUT, ICAP clients) | 7.4.5 and later | ALG `SRG-NET-000391-ALG-000140` | — |
| Web proxy | Failover between multiple proxy chain servers | 7.4.5 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| GUI and dashboard | Application and URL category columns in the policy table | 7.4.5 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Diagnostics | Packet capture enhancements | 7.4.6+; 7.6.0+ | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Platform | SR-IOV on KVM, VMware, and Azure | 7.4.6+; 7.6.0+ | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Web filter | Reputable Websites page | 7.4.6+; 7.6.0+ | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| GUI and dashboard | Web forwarding server column in the policy list | 7.4.6+; 7.6.0+ | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| User authentication | IP-based authentication through the portal without HTTP redirection | 7.4.6+; 7.6.1+ | ALG `SRG-NET-000138-ALG-000063` | `config authentication rule; edit <AUTH_RULE>; set form-auth-fallback enable; next; end` |
| Logging and monitoring | Customizable syslog format | 7.4.6+; 7.6.1+ | ALG `SRG-NET-000334-ALG-000050` | — |
| Web proxy | Header replacement in web proxy profiles | 7.4.6+; 7.6.1+ | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| SSL inspection | Static client certificate for SSL/SSH inspection | 7.4.7+; 7.6.1+ | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Certificates | Securosys Primus HSM | 7.4.7+; 7.6.3+ | ALG `SRG-NET-000755-ALG-000150`; ALG `SRG-NET-000062-ALG-000092` | — |
| System | License information in SNMP | 7.4.7+; 7.6.1+ | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Platform | SR-IOV on Hyper-V | 7.4.7+; 7.6.1+ | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Antivirus | Alternate FortiSandbox when the main FortiSandbox is unavailable | 7.4.8+; 7.6.2+ | ALG `SRG-NET-000365-ALG-000123` | `config system fortisandbox; set alt-server <ALT_FORTISANDBOX>; end` |
| Web proxy | Longer maximum HTTP header content (4000 characters) | 7.4.8+; 7.6.2+ | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Platform | UEFI on Google Cloud | 7.4.8+; 7.6.2+ | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Traffic shaping | Traffic shaping based on the HTTP response | 7.4.9+; 7.6.3+ | ALG `SRG-NET-000705-ALG-000110` | — |
| VPN | IKEv2 for IPsec VPN | 7.4.9+; 7.6.4+ | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Policy and objects | Higher proxy address configuration limit | 7.4.9+; 7.6.3+ | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Policy and objects | Explicit Web Connect and Transparent Connect policy types for HTTPS | 7.4.11+; 7.6.4+ | ALG `SRG-NET-000018-ALG-000017`; ALG `SRG-NET-000062-ALG-000150` | `config firewall policy; edit <POLICY_ID>; set type explicit-web-connect; next; end` |
| Traffic shaping | Traffic shaping based on the HTTP response: DSCP and shaping policy matching | 7.4.11+; 7.6.4+ | ALG `SRG-NET-000705-ALG-000110` | — |
| User authentication | Negated user groups as policy sources | 7.4.11+; 7.6.4+ | ALG `SRG-NET-000015-ALG-000016` | `config user group; edit <GROUP>; set negate enable; next; end` |
| User authentication | Authentication based on a custom HTTP header | 7.4.11+; 7.6.4+ | ALG `SRG-NET-000138-ALG-000063`; ALG `SRG-NET-000735-ALG-000130` | `config authentication scheme; edit <AUTH_SCHEME>; set method x-auth-user; set auth-user-header <HEADER>; next; end` (only from a trusted downstream proxy) |
| Policy and objects | Multiple conditions in proxy addresses and address groups | 7.4.12+; 7.6.4+ | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Licensing | Logging of license sharing events | 7.4.12+; 7.6.6+ | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| SSL inspection | Post-quantum cryptography (PQC) hybrid key exchange in SSL deep inspection | 7.4.14+; 7.6.7+ | ALG `SRG-NET-000062-ALG-000150` | — |
| GUI and dashboard | Updated Dashboard and FortiView | 7.6.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| GUI and dashboard | GUI enhancements for the FortiGuard DLP service | 7.6.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| GUI and dashboard | Optimized policy and object pages and dialogs | 7.6.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Web proxy | Happy Eyeballs algorithm for the explicit proxy | 7.6.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Network | Transparent conditional DNS forwarder | 7.6.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Network | Non-management VDOM interfaces as the source of DNS conditional forwarding | 7.6.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Logging and monitoring | Explicit proxy logging enhancements | 7.6.0 and later | ALG `SRG-NET-000074-ALG-000043` | — |
| ZTNA | Interface subnet list sent to EMS | 7.6.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| ZTNA | ZTNA Tag renamed Security Posture Tag in the GUI | 7.6.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Content filtering | Video filter profile customization | 7.6.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Antivirus | CDR for XLSB, OpenOffice, and RTF files | 7.6.0 and later | ALG `SRG-NET-000765-ALG-000170`; ALG `SRG-NET-000228-ALG-000108` | `config antivirus profile; edit <AV_PROFILE>; config http; set content-disarm enable; end; next; end` |
| DLP and file filter | FortiGuard managed DLP dictionaries | 7.6.0 and later | ALG `SRG-NET-000391-ALG-000140` | — |
| Antivirus | Download of quarantined files in archive format | 7.6.0 and later | ALG `SRG-NET-000249-ALG-000145` | — |
| User authentication | Windows AD cross-forest Kerberos authentication | 7.6.0 and later | ALG `SRG-NET-000138-ALG-000063` | — |
| User authentication | Certificate validation and FortiClient EMS tag matching options | 7.6.0 and later | ALG `SRG-NET-000164-ALG-000100` | — |
| User authentication | RADIUS over TLS (RadSec) client | 7.6.0 and later | ALG `SRG-NET-000400-ALG-000097`; NDM `SRG-APP-000172-NDM-000259` | `config user radius; edit <RADIUS>; set transport-protocol tls; set ca-cert <CA_CERT>; set client-cert <CLIENT_CERT>; set server-identity-check enable; next; end` |
| User authentication | Complexity options for the local user password policy | 7.6.0 and later | ALG `SRG-NET-000138-ALG-000063` | `config user password-policy; edit <POLICY>; set minimum-length 15; set min-upper-case-letter 1; set min-lower-case-letter 1; set min-number 1; set min-non-alphanumeric 1; next; end` |
| Certificates | Enrollment over Secure Transport (EST) for automatic certificate management | 7.6.0 and later | NDM `SRG-APP-000516-NDM-000344` | — |
| Network | Upper limit of the FQDN refresh timer | 7.6.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| System | SNMP trap for memory usage | 7.6.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| System | SNMP trap for PSU power restore | 7.6.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Management access | SSH host key separate from the administration server certificate | 7.6.0 and later | NDM `SRG-APP-000412-NDM-000331`; NDM `SRG-APP-000516-NDM-000344` | `config system ssh-config; set ssh-hsk-override enable; set ssh-hsk <HOST_KEY>; end` |
| Logging and monitoring | Updated default email notification server | 7.6.0 and later | NDM `SRG-APP-000360-NDM-000295` | `config system email-server; set server <SMTP_SERVER>; end` |
| Security Fabric | FortiClient EMS and EMS Cloud per VDOM | 7.6.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Platform | UEFI-Preferred boot mode on AWS | 7.6.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| ZTNA | ZTNA for UDP traffic | 7.6.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| GUI and dashboard | Policy list enhancements | 7.6.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Logging and monitoring | Log fields for long-lived sessions | 7.6.1 and later | ALG `SRG-NET-000505-ALG-000039`; ALG `SRG-NET-000074-ALG-000043` | `config log setting; set long-live-session-stat enable; end` |
| Policy and objects | Multiple explicit proxies in a policy | 7.6.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Certificates | Google Cloud HSM | 7.6.1 and later | ALG `SRG-NET-000755-ALG-000150` | — |
| Certificates | Improved certificate management in cloud infrastructure | 7.6.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| ZTNA | ZTNA agentless web-based application access (ZTNA web portal) | 7.6.2 and later | ALG `SRG-NET-000138-ALG-000063`; ALG `SRG-NET-000015-ALG-000016` | — |
| User authentication | Authentication with OpenID Connect (OIDC) | 7.6.2 and later | ALG `SRG-NET-000138-ALG-000063`; ALG `SRG-NET-000138-ALG-000088` | `config user oidc; edit <OIDC>; set verify-cert enable; set verify-issuer enable; next; end`; `config authentication scheme; edit <AUTH_SCHEME>; set method oidc; set oidc-server <OIDC>; next; end` |
| ZTNA | Policy-based service connector traffic forwarding | 7.6.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| DLP and file filter | New file types for DLP and file filter | 7.6.2 and later | ALG `SRG-NET-000019-ALG-000018`; ALG `SRG-NET-000289-ALG-000110` | — |
| User authentication | OIDC enhancements (multiple identity providers) | 7.6.3 and later | ALG `SRG-NET-000138-ALG-000063` | — |
| ZTNA | ZTNA web portal enhancements | 7.6.3 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| User authentication | SHA-256 for digest authentication | 7.6.3 and later | ALG `SRG-NET-000400-ALG-000097`; ALG `SRG-NET-000147-ALG-000095` | `config authentication scheme; edit <AUTH_SCHEME>; set method digest; set digest-algo sha-256; next; end` |
| LLM gateway | LLM security gateway on the ZTNA web portal | 7.6.4 and later | ALG `SRG-NET-000018-ALG-000017`; ALG `SRG-NET-000391-ALG-000140` | — |
| User authentication | SAML users as local users | 7.6.4 and later | ALG `SRG-NET-000138-ALG-000063` | — |
| User authentication | Chained proxy authentication with client certificates | 7.6.4 and later | ALG `SRG-NET-000138-ALG-000063`; ALG `SRG-NET-000164-ALG-000100` | — |
| User authentication | CAPTCHA in form-based authentication | 7.6.4 and later | ALG `SRG-NET-000138-ALG-000063` | `config authentication scheme; edit <AUTH_SCHEME>; set method form; set captcha enable; next; end` |
| User authentication | SSO_Guest_Users group matches authenticated users only | 7.6.4 and later | ALG `SRG-NET-000015-ALG-000016` | — |
| LLM gateway | LLM security gateway as an HTTP proxy | 7.6.6 and later | ALG `SRG-NET-000018-ALG-000017`; ALG `SRG-NET-000391-ALG-000140` | `config firewall policy; edit <POLICY_ID>; set llm-profile <LLM_PROFILE>; next; end` |
| System | Netlink replaces iptables and ipset | 7.6.6 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Web proxy | HTTP QUERY method | 7.6.6 and later | ALG `SRG-NET-000512-ALG-000066` | — |
| GUI and dashboard | ICAP Server Monitor widget | 7.6.7 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Web proxy | Tunneling UDP and TCP over HTTP/2 and HTTP/3 | 7.6.7 and later | ALG `SRG-NET-000512-ALG-000066`; ALG `SRG-NET-000131-ALG-000086` | — |
| Web caching and WAN optimization | Ports for WCCP service groups 1 to 50 | 7.6.7 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |

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
| ALG | `SRG-NET-000042-ALG-000023` | CAT II | The ALG providing user access control intermediary services must retain the Standard Mandatory DoD-approved Notice and Consent Banner on the screen until users acknowledge the usage conditions and take explicit actions to log on for further access. |
| ALG | `SRG-NET-000053-ALG-000001` | CAT II | The ALG providing user access control intermediary services must limit the number of concurrent sessions to an organization-defined number for all accounts and/or account types. |
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
| ALG | `SRG-NET-000131-ALG-000086` | CAT II | The ALG must be configured to remove or disable unrelated or unneeded application proxy services. |
| ALG | `SRG-NET-000132-ALG-000087` | CAT II | The ALG must be configured to prohibit or restrict the use of functions, ports, protocols, and/or services, as defined in the PPSM CAL and vulnerability assessments. |
| ALG | `SRG-NET-000138-ALG-000063` | CAT II | The ALG providing user authentication intermediary services must uniquely identify and authenticate organizational users (or processes acting on behalf of organizational users). |
| ALG | `SRG-NET-000138-ALG-000088` | CAT II | The ALG providing user access control intermediary services must be configured with a pre-established trust relationship and mechanisms with appropriate authorities (e.g., Active Directory or AAA server) which validate user account access authorizations and privileges. |
| ALG | `SRG-NET-000138-ALG-000089` | CAT II | The ALG providing user authentication intermediary services must restrict user authentication traffic to specific authentication server(s). |
| ALG | `SRG-NET-000140-ALG-000094` | CAT II | The ALG providing user authentication intermediary services must use multifactor authentication for network access to non-privileged accounts. |
| ALG | `SRG-NET-000147-ALG-000095` | CAT II | The ALG providing user authentication intermediary services must implement replay-resistant authentication mechanisms for network access to nonprivileged accounts. |
| ALG | `SRG-NET-000164-ALG-000100` | CAT II | The ALG that provides intermediary services for TLS must validate certificates used for TLS functions by performing RFC 5280-compliant certification path validation. |
| ALG | `SRG-NET-000166-ALG-000101` | CAT II | The ALG providing PKI-based user authentication intermediary services must map authenticated identities to the user account. |
| ALG | `SRG-NET-000169-ALG-000102` | CAT II | The ALG providing user authentication intermediary services must uniquely identify and authenticate non-organizational users (or processes acting on behalf of non-organizational users). |
| ALG | `SRG-NET-000192-ALG-000121` | CAT II | The ALG providing content filtering must block outbound traffic containing known and unknown DoS attacks to protect against the use of internal information systems to launch any Denial of Service (DoS) attacks against other networks or endpoints. |
| ALG | `SRG-NET-000202-ALG-000124` | CAT II | The ALG must deny network communications traffic by default and allow network communications traffic by exception (i.e., deny all, permit by exception). |
| ALG | `SRG-NET-000213-ALG-000107` | CAT II | The ALG must terminate all network connections associated with a communications session at the end of the session, or as follows: for in-band management sessions (privileged sessions), the session must be terminated after 10 minutes of inactivity; and for user sessions (non-privileged session), the session must be terminated after 15 minutes of inactivity. |
| ALG | `SRG-NET-000228-ALG-000108` | CAT II | The ALG must detect, at a minimum, mobile code that is unsigned or exhibiting unusual behavior, has not undergone a risk assessment, or is prohibited for use based on a risk assessment. |
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
| ALG | `SRG-NET-000384-ALG-000136` | CAT II | The ALG providing content filtering must detect use of network services that have not been authorized or approved by the ISSM and ISSO, at a minimum. |
| ALG | `SRG-NET-000385-ALG-000137` | CAT II | The ALG providing content filtering must generate a log record when unauthorized network services are detected. |
| ALG | `SRG-NET-000390-ALG-000139` | CAT II | The ALG providing content filtering must continuously monitor inbound communications traffic crossing internal security boundaries for unusual or unauthorized activities or conditions. |
| ALG | `SRG-NET-000391-ALG-000140` | CAT II | The ALG providing content filtering must continuously monitor outbound communications traffic crossing internal security boundaries for unusual/unauthorized activities or conditions. |
| ALG | `SRG-NET-000392-ALG-000141` | CAT II | The ALG providing content filtering must send an alert to, at a minimum, the ISSO and ISSM when detection events occur. |
| ALG | `SRG-NET-000392-ALG-000142` | CAT II | The ALG providing content filtering must generate an alert to, at a minimum, the ISSO and ISSM when threats identified by authoritative sources (e.g., IAVMs or CTOs) are detected. |
| ALG | `SRG-NET-000392-ALG-000148` | CAT II | The ALG providing content filtering must generate an alert to, at a minimum, the ISSO and ISSM when denial of service incidents are detected. |
| ALG | `SRG-NET-000400-ALG-000097` | CAT I | The ALG providing user authentication intermediary services must transmit only encrypted representations of passwords. |
| ALG | `SRG-NET-000401-ALG-000127` | CAT II | The ALG must check the validity of all data inputs except those specifically identified by the organization. |
| ALG | `SRG-NET-000402-ALG-000130` | CAT II | The ALG must reveal error messages only to the ISSO, ISSM, and SCA. |
| ALG | `SRG-NET-000503-ALG-000038` | CAT II | The ALG providing user access control intermediary services must generate audit records when successful/unsuccessful logon attempts occur. |
| ALG | `SRG-NET-000505-ALG-000039` | CAT II | The ALG providing user access control intermediary services must generate audit records showing starting and ending time for user access to the system. |
| ALG | `SRG-NET-000510-ALG-000025` | CAT II | The ALG providing encryption intermediary services must implement NIST FIPS-validated cryptography to generate cryptographic hashes. |
| ALG | `SRG-NET-000510-ALG-000040` | CAT II | The ALG providing encryption intermediary services must implement NIST FIPS-validated cryptography for digital signatures. |
| ALG | `SRG-NET-000510-ALG-000111` | CAT II | The ALG providing encryption intermediary services must use NIST FIPS-validated cryptography to implement encryption services. |
| ALG | `SRG-NET-000511-ALG-000051` | CAT II | The ALG must off-load audit records onto a centralized log server in real time. |
| ALG | `SRG-NET-000512-ALG-000065` | CAT II | The ALG that provides intermediary services for FTP must inspect inbound and outbound FTP communications traffic for protocol compliance and protocol anomalies. |
| ALG | `SRG-NET-000512-ALG-000066` | CAT II | The ALG that provides intermediary services for HTTP must inspect inbound and outbound HTTP traffic for protocol compliance and protocol anomalies. |
| ALG | `SRG-NET-000514-ALG-000514` | CAT II | The ALG providing user access control intermediary services must initiate a session lock after a 15-minute period of inactivity. |
| ALG | `SRG-NET-000517-ALG-000006` | CAT II | The ALG providing user access control intermediary services must automatically terminate a user session when organization-defined conditions or trigger events that require a session disconnect occur. |
| ALG | `SRG-NET-000575-ALG-000020` | CAT II | The ALG must use a FIPS-validated cryptographic module to implement encryption services for unclassified information requiring confidentiality. |
| ALG | `SRG-NET-000705-ALG-000110` | CAT II | The ALG must employ organization-defined controls by type of denial of service (DoS) to achieve the DoS objective. |
| ALG | `SRG-NET-000715-ALG-000120` | CAT II | The ALG must implement physically or logically separate subnetworks to isolate organization-defined critical system components and functions. |
| ALG | `SRG-NET-000735-ALG-000130` | CAT II | The ALG must implement antispoofing mechanisms to prevent adversaries from falsifying the security attributes indicating the successful application of the security process. |
| ALG | `SRG-NET-000750-ALG-000140` | CAT II | The ALG must include only approved trust anchors in trust stores or certificate stores managed by the organization. |
| ALG | `SRG-NET-000755-ALG-000150` | CAT II | The ALG must provide protected storage for cryptographic keys with organization-defined safeguards and/or hardware protected key store. |
| ALG | `SRG-NET-000765-ALG-000170` | CAT II | The ALG must implement signature based and/or nonsignature based malicious code protection mechanisms at system entry and exit points to detect and eradicate malicious code. |
| ALG | `SRG-NET-000770-ALG-000180` | CAT II | The ALG must configure malicious code protection mechanisms to send alerts to organization-defined personnel in response to malicious code detection. |
| NDM | `SRG-APP-000001-NDM-000200` | CAT II | The network device must limit the number of concurrent sessions to an organization-defined number for each administrator account and/or administrator account type. |
| NDM | `SRG-APP-000026-NDM-000208` | CAT II | The network device must automatically audit account creation. |
| NDM | `SRG-APP-000027-NDM-000209` | CAT II | The network device must automatically audit account modification. |
| NDM | `SRG-APP-000033-NDM-000212` | CAT I | The network device must be configured to assign appropriate user roles or access levels to authenticated users. |
| NDM | `SRG-APP-000038-NDM-000213` | CAT II | The network device must enforce approved authorizations for controlling the flow of management information within the network device based on information flow control policies. |
| NDM | `SRG-APP-000065-NDM-000214` | CAT II | The network device must be configured to enforce the limit of three consecutive invalid logon attempts, after which time it must block any login attempt for 15 minutes. |
| NDM | `SRG-APP-000068-NDM-000215` | CAT II | The network device must display the Standard Mandatory DoD Notice and Consent Banner before granting access to the device. |
| NDM | `SRG-APP-000095-NDM-000225` | CAT II | The network device must produce audit log records containing sufficient information to establish what type of event occurred. |
| NDM | `SRG-APP-000096-NDM-000226` | CAT II | The network device must produce audit records containing information to establish when (date and time) the events occurred. |
| NDM | `SRG-APP-000101-NDM-000231` | CAT II | The network device must generate audit records containing the full-text recording of privileged commands. |
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
| NDM | `SRG-APP-000177-NDM-000263` | CAT I | The network device, for PKI-based authentication, must be configured to map validated certificates to unique user accounts. |
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
| NDM | `SRG-APP-000795-NDM-000130` | CAT II | The network device must be configured to alert organization-defined personnel or roles upon detection of unauthorized access, modification, or deletion of audit information. |
| NDM | `SRG-APP-000820-NDM-000170` | CAT II | The network device must be configured to implement multifactor authentication for local; network; and/or remote access to privileged accounts; and/or nonprivileged accounts such that one of the factors is provided by a device separate from the system gaining access. |
| NDM | `SRG-APP-000825-NDM-000180` | CAT II | The network device must be configured to implement multifactor authentication for local; network; and/or remote access to privileged accounts; and/or nonprivileged accounts such that the device meets organization-defined strength of mechanism requirements. |
| NDM | `SRG-APP-000845-NDM-000220` | CAT II | The network device must be configured to verify, when users create or update passwords, the passwords are not found on the list of commonly used, expected, or compromised passwords in IA-5 (1) (a) for password-based authentication. |
| NDM | `SRG-APP-000875-NDM-000280` | CAT II | The network device must be configured to implement certificate revocation checking to support path discovery and validation for public key-based authentication. |
| NDM | `SRG-APP-000880-NDM-000290` | CAT II | The network device must be configured to protect nonlocal maintenance sessions by separating the maintenance session from other network sessions with the system by logically separated communications paths. |
| NDM | `SRG-APP-000910-NDM-000300` | CAT II | The network device must be configured to include only approved trust anchors in trust stores or certificate stores managed by the organization. |
| NDM | `SRG-APP-000920-NDM-000320` | CAT II | The network device must be configured to synchronize system clocks within and between systems or system components. |
| NDM | `SRG-APP-001035-NDM-000340` | CAT I | The network device hardware and software must be a version supported by the vendor. |

### Collecting evidence

Enter `show` in each configuration section that the map cites, at least
`config system global`, `config system admin`, `config system accprofile`,
`config system password-policy`, `config system interface`,
`config system ntp`, `config system snmp user`, `config system fips-cc`,
`config log syslogd setting`, `config log fortianalyzer setting`,
`config web-proxy explicit-proxy`, `config web-proxy global`,
`config firewall policy`, `config authentication scheme`,
`config authentication rule`, `config user setting`, and the SSL/SSH
inspection, antivirus, web filter, application control, and IPS profiles,
and run `get system status` for the release. Export the event, traffic,
HTTP transaction, antivirus, and web filter logs from the central log
server, and keep the FortiGuard update status and the firmware upgrade
record with the checklist.

## Validation and Troubleshooting

- **A feature in the map is missing on your FortiProxy.** Check the version
  column against the FortiProxy release, and check whether the feature
  depends on the platform, a license, or VDOM mode.
- **A command is rejected.** The command was checked against the 7.6.7 CLI
  Reference. Older releases may lack the option or spell it differently;
  check the CLI Reference of your release, and enter `config global` or
  `config vdom` first when VDOMs are enabled.
- **A profile has no effect.** Profiles apply only through a policy. Check
  which policy matches the traffic, its type, and its order.
- **HTTPS sites fail after deep inspection is enabled.** Check that clients
  trust the re-signing CA, and which certificate check (untrusted,
  expired, revoked, or validation failure) blocked the site in the SSL
  logs.
- **Users are not authenticated, or are prompted repeatedly.** Check the
  authentication rule that matches the source, its active scheme, the
  authentication timeouts and keep-alive mode, and the reachability of the
  LDAP, RADIUS, SAML, or Kerberos services.
- **A requirement has no matching feature.** Some requirements are met by
  procedure (password changes), by another system (the authentication
  server, the central log server, the time servers, the client's session
  lock), or not at all. Record how each requirement is met, not just which
  feature covers it.

## Security and Best Practices

- Keep FortiProxy on a vendor-supported release and install patches
  promptly; FortiProxy verifies the image signature when the firmware is
  uploaded.
- Set administrator passwords of at least 15 characters, use DoD PKI or a
  remote authentication server for administrator login, and keep one local
  account of last resort.
- Allow only HTTPS and SSH on the management interface, with TLS 1.2 or
  later, strong ciphers, trusted hosts, and the pre-login banner.
- Send event, traffic, and security logs to a central log server over TLS,
  and use SNMPv3 with SHA-2 authentication and AES privacy only.
- Keep FortiGuard antivirus, IPS, and web filter services current, and
  review this map each time Fortinet publishes a FortiProxy release or DISA
  updates the ALG or NDM SRG.

## References and Knowledge Checks

**References:**

- Fortinet, *FortiProxy Release Notes*, section "What's new", releases
  7.0.0 to 7.0.23, 7.2.0 to 7.2.16, 7.4.0 to 7.4.14, and 7.6.0 to 7.6.7
  (docs.fortinet.com, FortiProxy documentation).
- Fortinet, *FortiProxy 7.6.7 CLI Reference* and *FortiProxy 7.6.7
  Administration Guide*.
- DISA Application Layer Gateway SRG V2R4 and Network Device Management SRG
  V5R5, from the October 2026 STIG Library Compilation.
- [Chapter 03](03-the-srg-catalog-how-stigs-are-built-and-what-to-do-without-one.md)
  (SRG-based assessment),
  [Chapter 10](10-fortinet-products-stigs-and-srg-mapping.md) (Fortinet
  products),
  [Chapter 11](11-fortiswitch-feature-version-and-srg-map.md) (the
  FortiSwitch map), and
  [Chapter 12](12-fortianalyzer-feature-version-and-srg-map.md) (the
  FortiAnalyzer map, the model for this chapter).

**Knowledge checks:**

1. Which two SRGs apply to FortiProxy, and which part of the appliance does
   each one cover?
2. Where does the version data come from, given that FortiProxy has no
   feature matrix or New Features Guide?
3. Which ALG requirement covers HTTP protocol compliance, and which
   FortiProxy settings help meet it?
4. Which ALG requirements do not apply to FortiProxy, and why?
5. Which requirements can FortiProxy not meet exactly, and how do you
   handle them?
6. What applies to a feature marked "No direct requirement"?

## Summary and Completion Checklist

FortiProxy has no STIG, so it is assessed against the ALG SRG for its web
proxy and the NDM SRG for its management plane. This chapter maps
425 features to the FortiProxy release that introduced them, to
150 SRG requirements, and to the FortiProxy command that configures
them: 89 core platform features, and 336 features from the
"What's new" sections of the FortiProxy 7.0.0 through 7.6.7 release notes.
Operational features with no direct requirement fall under the requirement
to disable unnecessary functions when unused.

- [ ] Can find the release that introduced a FortiProxy feature.
- [ ] Can map a FortiProxy feature to its ALG or NDM SRG requirement.
- [ ] Can find the FortiProxy command that meets the requirement.
- [ ] Can decide which ALG requirements apply to a secure web gateway.
- [ ] Can collect FortiProxy evidence and record the requirements
  FortiProxy cannot meet exactly.
