# Chapter 17: FortiMail Feature, Version, and SRG Map

## Learning Objectives

- Find the FortiMail release that introduced a given feature.
- Map each FortiMail feature to the Application Layer Gateway (ALG) or
  Network Device Management (NDM) SRG requirement it helps satisfy.
- Find the FortiMail CLI command that configures each feature to meet its
  requirement.
- Use the map to scope an SRG-based assessment of FortiMail, which has no
  STIG of its own.
- Decide which ALG requirements apply to an email security gateway and
  which do not.
- Record the requirements that FortiMail cannot meet exactly, with their
  mitigations.

## Theory and Architecture

FortiMail is Fortinet's email security gateway. It has **no DISA STIG**
(Chapter 10), so it is assessed against SRGs, as described in Chapter 03.
Chapter 10 assigns it two: the **Application Layer Gateway (ALG) SRG** for
the mail-filtering gateway, the SMTP proxy or relay that inspects inbound
and outbound email and blocks spam, malware, spoofing, and data leaks, and
the **Network Device Management (NDM) SRG** for the management plane, the
way administrators log in to and configure the appliance. For every
FortiMail feature the chapter gives **which FortiMail release introduced
it**, **which requirement it relates to**, and **which command configures
it to meet that requirement**.

FortiMail runs in one of three **operation modes**, set with
`operation-mode` in `config system global` (the 8.0.0 CLI Reference):

- **Gateway** (the default): FortiMail is an SMTP relay (MTA) in front of
  the mail servers. It receives mail for the protected domains, scans it,
  and delivers it to the protected mail server, but hosts no mailboxes.
- **Transparent**: FortiMail is an SMTP proxy or implicit relay in the
  network path, so in most cases the DNS records of the protected domains
  do not change.
- **Server**: FortiMail is a standalone mail server that also hosts the
  mailboxes, with webmail, POP3, and IMAP.

Mail processing is built from a few objects. **Protected domains** name the
domains FortiMail receives mail for. **Access control rules** decide which
SMTP clients may relay (receiving rules) and how mail leaves (delivery
rules). **IP-based policies** and **recipient-based policies** then select
the **profiles** to apply: a session profile (SMTP protocol checks,
connection limits, sender reputation), an antispam profile, an antivirus
profile, a content profile (attachments, archives, content disarm and
reconstruction), a DLP profile, and, for authenticated users, an
authentication profile. Action profiles decide what happens to a detected
message: reject, discard, quarantine, tag, or encrypt.

FortiMail also serves users directly through **webmail**, the **personal
quarantine**, and the **identity-based encryption (IBE)** portal, where
external recipients read encrypted mail. Those pages are where the ALG
requirements for user access control and user authentication apply.

Several FortiMail features use Fortinet or Microsoft cloud services
(FortiGuard antispam and antivirus, FortiSandbox Cloud, FortiIdentity
Cloud, FortiAnalyzer Cloud, and the Microsoft 365 and Google Workspace API
modes); those services are outside the enclave and are not assessed here,
so use them only if they are authorized for your environment. FortiMail
Cloud (the SaaS service) is a separate product and is not covered.

### Where the version data comes from

Fortinet does not publish a feature matrix, a New Features Guide, or a
"What's new" chapter in the Administration Guide for FortiMail. The
authoritative per-release list is the **"What's new" section of the
FortiMail Release Notes**, which Fortinet publishes for every release on
docs.fortinet.com as a table of features with a description of each. The
version column was built from the release notes of all 38 releases Fortinet
publishes for the 7.0 to 8.0 trains:

- **7.0 train:** 7.0.0 through 7.0.9.
- **7.2 train:** 7.2.0 through 7.2.9.
- **7.4 train:** 7.4.0 through 7.4.7, and 7.4.9.
- **7.6 train:** 7.6.0 through 7.6.5, and 7.6.7.
- **8.0 train:** 8.0.0 and 8.0.2.

There are no release notes for 7.4.8, 7.6.6, or 8.0.1; their addresses on
docs.fortinet.com open the previous release. In 7.4.7 and 7.4.9 the section
is "What's New and What's Changed", and both entries (time zone updates)
were kept. Fourteen releases (7.0.4, 7.0.5, 7.0.7 through 7.0.9, 7.2.4,
7.2.6 through 7.2.9, 7.4.5, 7.4.6, 7.6.1, and 7.6.7) are patch releases
with no new features: their release notes have no "What's new" section or
say that none were added.

The table has two groups of rows:

- **Core platform features** (categories starting with *Core:*) are the
  long-standing capabilities that the requirements depend on: management
  access, administrator accounts and authentication, password and lockout
  policy, the login disclaimer, logging, time, SNMP, FIPS-CC mode, firmware
  and backups, high availability, and the mail gateway itself (protected
  domains, access control rules, policies, and the session, antispam,
  antivirus, content, and encryption profiles). They existed before
  FortiMail 7.0.0 and are not in any of these "What's new" lists; they were
  taken from the FortiMail 8.0.0 CLI Reference and 8.0.2 Administration
  Guide, and their commands were checked against the 7.0.0 CLI Reference
  table of contents.
- **New features** are the 257 entries of the "What's new" tables.
  The 7.0 to 7.2 tables and several later ones have no categories, and the
  others are broad, so the categories were assigned for this chapter, and
  some titles were lightly edited for clarity. An entry listed again in a
  later release or train is one row with both versions: Microsoft OneNote
  virus detection, for example, is listed in 7.0.6 and 7.2.3, and SNMPv3
  SHA-2 authentication and AES-256 privacy in 7.6.5 and 8.0.0.

| Version entry | Meaning |
| --- | --- |
| `7.0.0 or earlier` | A core feature that predates the oldest release notes used (FortiMail 7.0.0) |
| `7.4.0 and later` | Introduced in FortiMail 7.4.0 |
| `7.0.6+; 7.2.3+` | Listed in two trains: from 7.0.6 in the 7.0 train and from 7.2.3 in the 7.2 train |

Three cautions apply. First, a feature introduced in a patch release of an
older train may reach a newer train only in a later patch, so "and later"
means later in the same train and, usually, in later trains. Second, many
features apply only to some operation modes (server mode, Microsoft 365 and
Google API mode), platforms, or licenses (Advanced Management, MSSP, email
continuity, OCR). Third, a core row records a FortiMail capability, but its
command was checked against the 8.0.0 CLI Reference and may differ on an
older release: `config system fips-cc` and `config system web-service` are
not in the 7.0.0 CLI Reference, and several settings arrived later, as the
new-feature rows say (for example SNMPv3 SHA-2 and AES-256 in 7.6.5,
secure RADIUS and administrator MFA with FortiIdentity Cloud in 8.0.0).

### Where the SRG data comes from

The SRG column uses requirement IDs from the October 2026 DISA library:

| SRG column | SRG | Release | Applies to |
| --- | --- | --- | --- |
| **ALG** | Application Layer Gateway SRG | V2R4, benchmark date 01 Jul 2026 | The mail-filtering gateway: SMTP inspection, spam, malware, and content filtering, quarantine, TLS and encryption of mail, user access to webmail, quarantine, and IBE, and the mail logs (assigned by Chapter 10) |
| **NDM** | Network Device Management SRG | V5R5, benchmark date 01 Jul 2026 | The management plane: administrator access, authentication, logging, time, SNMP, firmware, and backups (assigned by Chapter 10) |

The ALG SRG is written for every kind of application layer gateway, so not
all of it applies. The requirements for an ALG that is part of a
cross-domain solution (CDS), for remote access, and for HTTP and FTP
intermediary services do not apply to FortiMail, and neither do the SQL and
code injection requirements written for web applications. The SMTP
requirement (ALG `SRG-NET-000512-ALG-000064`), the spam protection update
requirement (ALG `SRG-NET-000393-ALG-000144`), and the malicious code
requirements are the core of an email gateway assessment. The requirements
for "user access control" and "user authentication intermediary services"
apply to the pages FortiMail serves to users: webmail, the personal
quarantine, and the IBE portal.

The requirement IDs are the **rule version IDs** from the XCCDF files, and
the severity is the rule's severity (high = CAT I, medium = CAT II, low =
CAT III). Each feature maps to one of three kinds of relationship:

- **Implements a requirement.** The feature is how FortiMail meets a
  requirement. Antivirus scanning implements the requirement to scan files
  from external sources in real time (ALG `SRG-NET-000248-ALG-000133`), for
  example.
- **Must be configured to meet a requirement.** The feature is in scope of
  a requirement and has to be set up correctly. TLS profiles must require
  TLS 1.2 or later (ALG `SRG-NET-000062-ALG-000150`), for example.
- **No direct requirement.** The feature is operational, such as a cloud
  platform, a license, a dashboard, a webmail convenience, or a disclaimer
  option. It has no requirement of its own, but if it is not needed it
  falls under the ALG requirement not to have unnecessary services and
  functions enabled (ALG `SRG-NET-000131-ALG-000085`); for a
  management-plane function the NDM equivalent is NDM
  `SRG-APP-000142-NDM-000245`.

The mapping is a starting point for an assessment, not a ruling. Confirm it
with your assessor, especially where a requirement is organization-defined
or depends on the operation mode.

### Where the commands come from

Every command was checked against the **FortiMail 8.0.0 CLI Reference**,
the newest CLI Reference Fortinet publishes for FortiMail (there is no
8.0.2 CLI Reference), and every web UI pane named in the table against the
**FortiMail 8.0.2 Administration Guide**. The check was automatic: each
`config` path and nested table, each `set` option against the syntax and
examples of the command it is entered under, each listed option value
against the documented values, each `execute` and `diagnose` command, and
each GUI pane name. Read the column this way:

- Commands run on the FortiMail CLI, over SSH, the console, or the CLI
  Console in the web UI. Most mail settings live in profiles, such as
  `config profile antispam`, `config profile antivirus`,
  `config profile content`, and `config profile session`; `<AS_PROFILE>`,
  `<AV_PROFILE>`, `<CONTENT_PROFILE>`, and `<SESSION_PROFILE>` are their
  names, and the profiles take effect only when a policy uses them.
- **GUI:** entries name the FortiMail web UI pane.
- Statements are separated by `;` to fit in a table cell; on the CLI, enter
  each one on its own line. Values in `<ANGLE_BRACKETS>` are placeholders
  for your own names, addresses, and keys.
- For **"No direct requirement"** rows, the command shown is the one that
  disables the feature when it is unused. A dash (**—**) means there is
  nothing to change: the feature is a platform, a license, a GUI change, or
  a capability that is off unless configured.

Some requirements cannot be met exactly with FortiMail settings. Record them
on the checklist as open findings with mitigations, or meet them another way:

- **Concurrent sessions.** There is no per-account session limit (NDM
  `SRG-APP-000001-NDM-000200`). The 8.0.0 CLI Reference has only a
  system-wide limit, `max-active-session-admin` under
  `config system web-service`. Define the limit as one session per
  administrator through procedure and the remote authentication server.
- **Password rules.** The password policy sets the minimum length and the
  character types, but there is no rule that a new password must change at
  least eight characters (NDM `SRG-APP-000170-NDM-000329`) and no check
  against a list of compromised passwords (NDM
  `SRG-APP-000845-NDM-000220`), and the CLI Reference says an administrator
  password can contain any character except spaces (NDM
  `SRG-APP-000860-NDM-000250`). Record the findings, and prefer PKI or
  remote authentication for administrators.
- **NTP authentication.** `config system time ntp` accepts up to ten NTP
  servers but has no authentication setting (NDM
  `SRG-APP-000395-NDM-000347`). Use internal time sources on a protected
  management path and record the finding.
- **SNMPv3 algorithms.** SHA-2 authentication and AES-256 privacy arrive in
  7.6.5 and 8.0.0 (NDM `SRG-APP-000395-NDM-000310`). On older releases use
  SHA-1 with AES, or disable SNMP.
- **Firmware signatures.** The Administration Guide says to verify the hash
  of a downloaded image before installing it, and the image is checked for
  integrity when it boots; there is no setting that requires a signed image
  before installation (NDM `SRG-APP-000131-NDM-000243`). Verify the hash by
  procedure before every upgrade.
- **Secure RADIUS and administrator MFA.** RADIUS over TLS arrives in 8.0.0
  (NDM `SRG-APP-000172-NDM-000259`), and token-based MFA for administrators
  uses FortiIdentity Cloud, a cloud service (NDM
  `SRG-APP-000820-NDM-000170`). On older releases, or where the cloud
  service is not authorized, use DoD PKI login (`pki-mode` with
  `pki-certificate-req yes`) for MFA, and protect the RADIUS path.
- **Banner for users.** The pre-login banner (`pre-login-banner`) covers
  administrators only. For webmail, quarantine, and IBE users FortiMail can
  show the disclaimer only after login (`post-login-banner`), not before
  access is granted (ALG `SRG-NET-000041-ALG-000022`). Record the finding,
  or put the banner on a portal in front of webmail.
- **Webmail session timeout.** Webmail idle sessions are ended through the
  resource profile `idle-timeout` and `webmail-session-ttl`, which accepts
  0 to 600 seconds (ALG `SRG-NET-000213-ALG-000107`); confirm the behavior
  meets your organization's user session timeout.
- **TLS with external mail servers.** SMTP TLS with other domains is off
  (level `none`, the default) or opportunistic (`preferred`) unless a TLS
  profile with level `secure` is applied to the rule; requiring TLS for every external domain will block mail from
  servers that do not support it (ALG `SRG-NET-000062-ALG-000150`). Require
  TLS for the domains you exchange sensitive mail with, and use IBE or
  S/MIME where TLS cannot be guaranteed.
- **Settings missing from the CLI Reference.** The certificate SSH key of
  7.4.0 and the DNS cache maximum TTL of 8.0.2 have no syntax entry in the
  8.0.0 CLI Reference; their rows say so. Check for them on your release.
- **FIPS 140 validation.** FIPS-CC mode (`fips-ciphers`) restricts the
  ciphers and disallows less secure protocols such as Telnet and TFTP (NDM
  `SRG-APP-000179-NDM-000265`, ALG `SRG-NET-000510-ALG-000111`). Check the
  NIST Cryptographic Module Validation Program for a current certificate
  for your FortiMail release before relying on its cryptography.

## Design Considerations

- **Pick the operation mode deliberately.** Gateway mode is the usual
  choice; transparent mode avoids DNS and addressing changes; server mode
  adds mailboxes, webmail, POP3, and IMAP, and with them the ALG user
  access and authentication requirements. Disable POP3 and IMAP when
  FortiMail does not host mailboxes.
- **Pick the release first, then the features.** If your design depends on
  a feature introduced in a certain release (for example SNMPv3 SHA-2 in
  7.6.5, bare line feed handling against SMTP smuggling in 7.6.2, or secure
  RADIUS in 8.0.0), that sets the minimum FortiMail release, and it must be
  a vendor-supported release (NDM `SRG-APP-001035-NDM-000340`).
- **Separate management from mail.** Allow HTTPS and SSH only on a
  dedicated management interface, never on the interfaces that receive
  SMTP from the internet, restrict administrators with trusted hosts, and
  keep HTTP and Telnet off.
- **Use DoD PKI for administrators.** Use certificate-based login with OCSP
  checking or a remote authentication server, with one local account of
  last resort, and disable the maintainer account once a tested backup and
  recovery procedure exists.
- **Deny relay by default.** Receive mail only for protected domains, allow
  relay only from the internal mail servers and authenticated users, and
  apply session profiles with SMTP command checking, open relay
  prevention, and connection limits to every policy.
- **Layer the content defenses.** Combine FortiGuard antispam, SPF, DKIM,
  and DMARC checks, antivirus with outbreak protection, attachment and
  archive inspection, and content disarm and reconstruction, and quarantine
  rather than deliver what is detected.
- **Turn off what is not used.** Cloud services that are not authorized,
  email continuity, archiving, the Security Fabric connection, REST API
  access, and SNMP v1 and v2c are all functions that need a reason to stay
  on.

## Implementation and Automation

### The FortiMail feature map

The SRG column uses the abbreviations defined in *Where the SRG data comes
from*. The requirement titles are listed in the next table. The command
column follows the conventions in *Where the commands come from*.

[Download the feature map as CSV](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/data/volume-172-disa-srgs-and-stigs/17-fortimail-feature-version-and-srg-map-feature-map.csv) (331 rows).

| Category | Feature | Introduced (FortiMail) | SRG requirement(s) | Command to satisfy the requirement |
| --- | --- | --- | --- | --- |
| Core: Management access | Administrative access per interface (HTTPS, SSH, ping, SNMP, HTTP, Telnet) | 7.0.0 or earlier | NDM `SRG-APP-000142-NDM-000245`; NDM `SRG-APP-000412-NDM-000331`; NDM `SRG-APP-000408-NDM-000314`; NDM `SRG-APP-000172-NDM-000259` | `config system interface; edit <MGMT_PORT>; set allowaccess https ssh; next; end` (management interface only; leave out HTTP and Telnet) |
| Core: Management access | TLS versions and strong ciphers for HTTPS, SSH, and syslog over TLS | 7.0.0 or earlier | NDM `SRG-APP-000412-NDM-000331`; NDM `SRG-APP-000411-NDM-000330`; NDM `SRG-APP-000179-NDM-000265` | `config system global; set strong-crypto enable; set ssl-versions tls1_2 tls1_3; end`; `config system security crypto; edit http; set status enable; set ssl-versions tls1_2 tls1_3; set strong-crypto enable; next; end` |
| Core: Management access | Default local certificate for the web UI and secure connections | 7.0.0 or earlier | NDM `SRG-APP-000516-NDM-000344`; NDM `SRG-APP-000910-NDM-000300` | `config system global; set default-certificate <DOD_ISSUED_CERT>; end` |
| Core: Management access | Administrative HTTP, HTTPS, SSH, and Telnet port numbers | 7.0.0 or earlier | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Core: Management access | Trusted hosts for each administrator | 7.0.0 or earlier | NDM `SRG-APP-000408-NDM-000314`; NDM `SRG-APP-000038-NDM-000213` | `config system admin; edit <ADMIN>; set trusted-hosts <MGMT_SUBNET>; next; end` |
| Core: Management access | Console port | 7.0.0 or earlier | NDM `SRG-APP-000408-NDM-000314` | — (physical access control; the console requires an administrator login) |
| Core: Management access | LCD panel PIN protection (models with an LCD panel) | 7.0.0 or earlier | NDM `SRG-APP-000408-NDM-000314` | `config system global; set lcd-protection enable; set lcd-pin <PIN>; end` |
| Core: Management access | Idle timeout for administrator sessions | 7.0.0 or earlier | NDM `SRG-APP-000190-NDM-000267` | `config system global; set admin-idle-timeout 5; end` |
| Core: Management access | Login disclaimer before administrator login (pre-login banner) | 7.0.0 or earlier | NDM `SRG-APP-000068-NDM-000215` | `config system global; set pre-login-banner admin; end` (banner text under System > Configuration > Option, Login Disclaimer Setting) |
| Core: Management access | Maintainer account (console password recovery) | 7.0.0 or earlier | NDM `SRG-APP-000148-NDM-000346`; NDM `SRG-APP-000142-NDM-000245` | `config system global; set admin-maintainer disable; end` (only with a tested configuration and data backup for recovery) |
| Core: Administrator accounts | Local administrator accounts | 7.0.0 or earlier | NDM `SRG-APP-000148-NDM-000346`; NDM `SRG-APP-000153-NDM-000249` | `config system admin; edit <ADMIN>; set auth-strategy local; set access-profile <PROFILE>; set password <PASSWORD_15_CHARS_MIN>; next; end` |
| Core: Administrator accounts | Access profiles (none, read, read-update, read-write per functional area) | 7.0.0 or earlier | NDM `SRG-APP-000033-NDM-000212`; NDM `SRG-APP-000231-NDM-000271`; NDM `SRG-APP-000380-NDM-000304` | `config system accprofile; edit <PROFILE>; config menuitem; edit system_grp; set permission read; next; edit log_grp; set permission read; next; end; next; end` |
| Core: Administrator accounts | Administrator domain scope (system, domain, domain group) | 7.0.0 or earlier | NDM `SRG-APP-000033-NDM-000212`; ALG `SRG-NET-000015-ALG-000016` | `config system admin; edit <ADMIN>; set level domain; set domain <PROTECTED_DOMAIN>; next; end` |
| Core: Administrator accounts | Administrator access methods (CLI, GUI, REST API) | 7.0.0 or earlier | NDM `SRG-APP-000408-NDM-000314`; NDM `SRG-APP-000142-NDM-000245` | `config system admin; edit <ADMIN>; set access cli gui; next; end` |
| Core: Administrator accounts | Password policy (length and character types) | 7.0.0 or earlier | NDM `SRG-APP-000164-NDM-000252`; NDM `SRG-APP-000166-NDM-000254`; NDM `SRG-APP-000167-NDM-000255`; NDM `SRG-APP-000168-NDM-000256`; NDM `SRG-APP-000169-NDM-000257` | `config system password-policy; set status enable; set apply-to admin-user ibe-user local-mail-user; set allow-admin-empty-password disable; set minimum-length 15; set must-contain upper-case-letter lower-case-letter number non-alphanumeric; end` |
| Core: Administrator accounts | Administrator login lockout | 7.0.0 or earlier | NDM `SRG-APP-000065-NDM-000214` | `config system global; set admin-lockout-threshold 3; set admin-lockout-duration 15; end` |
| Core: Administrator accounts | Authentication reputation (block client IP addresses after failed logins) | 7.0.0 or earlier | NDM `SRG-APP-000065-NDM-000214`; NDM `SRG-APP-000435-NDM-000315`; ALG `SRG-NET-000705-ALG-000110` | `config system security authserver; set status enable; set access-group cli mail web; set block-period 15; end` |
| Core: Administrator accounts | Remote administrator authentication with RADIUS | 7.0.0 or earlier | NDM `SRG-APP-000516-NDM-000336`; NDM `SRG-APP-000153-NDM-000249`; NDM `SRG-APP-000148-NDM-000346` | `config profile authentication radius; edit <RADIUS>; set server <RADIUS_SERVER>; set secret <SECRET>; next; end`; `config system admin; edit <ADMIN>; set auth-strategy radius; set radius-profile <RADIUS>; next; end` |
| Core: Administrator accounts | Remote administrator authentication with LDAP | 7.0.0 or earlier | NDM `SRG-APP-000516-NDM-000336`; NDM `SRG-APP-000153-NDM-000249`; NDM `SRG-APP-000172-NDM-000259` | `config profile ldap; edit <LDAP>; set server <LDAP_SERVER>; set secure ssl; set authstate enable; next; end`; `config system admin; edit <ADMIN>; set auth-strategy ldap; set ldap-profile <LDAP>; next; end` |
| Core: Administrator accounts | Certificate-based (PKI) administrator login | 7.0.0 or earlier | NDM `SRG-APP-000149-NDM-000247`; NDM `SRG-APP-000177-NDM-000263`; NDM `SRG-APP-000175-NDM-000262`; NDM `SRG-APP-000875-NDM-000280` | `config user pki; edit <PKI_USER>; set ca <DOD_CA_CERT>; set subject <SUBJECT>; set ocsp-check enable; set ocsp-URL <OCSP_URL>; set ocsp-ca <OCSP_CERT>; set ocsp-unavailable-action revoke; next; end`; `config system global; set pki-mode enable; set pki-certificate-req yes; end`; `config system admin; edit <ADMIN>; set auth-strategy pki; set pkiuser <PKI_USER>; next; end` |
| Core: Administrator accounts | SSH public key login for administrators | 7.0.0 or earlier | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Core: Logging | Local logging and log levels | 7.0.0 or earlier | NDM `SRG-APP-000095-NDM-000225`; NDM `SRG-APP-000357-NDM-000293`; ALG `SRG-NET-000074-ALG-000043` | `config log setting local; set status enable; set loglevel information; set event-log-status enable; set history-log-status enable; end` |
| Core: Logging | Event log categories (administrator, configuration, HA, system, update) | 7.0.0 or earlier | NDM `SRG-APP-000026-NDM-000208`; NDM `SRG-APP-000503-NDM-000320`; NDM `SRG-APP-000505-NDM-000322`; NDM `SRG-APP-000380-NDM-000304`; NDM `SRG-APP-000343-NDM-000289`; NDM `SRG-APP-000095-NDM-000225` | `config log setting local; set syseventlog-category admin configuration configuration-user dns ha system update; end` |
| Core: Logging | History log (one record per mail transaction, with sender, recipient, client, policy, and disposition) | 7.0.0 or earlier | ALG `SRG-NET-000074-ALG-000043`; ALG `SRG-NET-000075-ALG-000044`; ALG `SRG-NET-000077-ALG-000046`; ALG `SRG-NET-000079-ALG-000048`; ALG `SRG-NET-000078-ALG-000047` | `config log setting local; set history-log-status enable; end` |
| Core: Logging | AntiVirus, AntiSpam, and encryption logs | 7.0.0 or earlier | ALG `SRG-NET-000074-ALG-000043`; ALG `SRG-NET-000249-ALG-000146`; ALG `SRG-NET-000370-ALG-000125` | `config log setting local; set antivirus-log-status enable; set antispam-log-status enable; set encryption-log-status enable; end` |
| Core: Logging | Remote syslog servers (TCP over TLS) | 7.0.0 or earlier | NDM `SRG-APP-000515-NDM-000325`; NDM `SRG-APP-000516-NDM-000350`; ALG `SRG-NET-000334-ALG-000050`; ALG `SRG-NET-000511-ALG-000051` | `config log setting remote; edit <SYSLOG>; set status enable; set server <SYSLOG_SERVER>; set protocol syslog; set syslog-mode tcp-tls; set loglevel information; set event-log-status enable; set history-log-status enable; set virus-log-status enable; set spam-log-status enable; next; end` |
| Core: Logging | Logging to FortiAnalyzer (OFTPS) | 7.0.0 or earlier | NDM `SRG-APP-000515-NDM-000325`; ALG `SRG-NET-000334-ALG-000050` | `config log setting remote; edit <FAZ>; set status enable; set server <FAZ_IP>; set protocol oftps; next; end` |
| Core: Logging | Log access restricted by access profile (log functional area) | 7.0.0 or earlier | NDM `SRG-APP-000231-NDM-000271`; ALG `SRG-NET-000098-ALG-000056`; ALG `SRG-NET-000099-ALG-000057`; ALG `SRG-NET-000100-ALG-000058` | `config system accprofile; edit <PROFILE>; config menuitem; edit log_grp; set permission read; next; end; next; end` |
| Core: Logging | Alert email (disk full, HA, system, virus, remote storage failure) | 7.0.0 or earlier | NDM `SRG-APP-000360-NDM-000295`; ALG `SRG-NET-000088-ALG-000054`; ALG `SRG-NET-000335-ALG-000053`; ALG `SRG-NET-000249-ALG-000146`; ALG `SRG-NET-000392-ALG-000141` | `config log alertemail recipient; edit <ISSO_EMAIL>; next; end`; `config log alertemail setting; set categories diskfull ha remote-storage-failure system virus; end` |
| Core: Logging | Hard disk monitoring with alert email | 7.0.0 or earlier | NDM `SRG-APP-000360-NDM-000295`; ALG `SRG-NET-000335-ALG-000053` | `config system global; set disk-monitor enable; end` |
| Core: Time | System time and NTP synchronization | 7.0.0 or earlier | NDM `SRG-APP-000920-NDM-000320`; NDM `SRG-APP-000374-NDM-000299` | `config system time ntp; set ntpsync enable; set ntpserver <NTP_SERVER>; end` |
| Core: SNMP | SNMP v1 and v2c communities | 7.0.0 or earlier | NDM `SRG-APP-000142-NDM-000245`; NDM `SRG-APP-000395-NDM-000310` | `config system snmp community; edit <ID>; set status disable; next; end` |
| Core: SNMP | SNMPv3 users and traps | 7.0.0 or earlier | NDM `SRG-APP-000395-NDM-000310` | `config system snmp user; edit <SNMP_USER>; set status enable; set security-level authpriv; set auth-proto sha256; set auth-pwd <AUTH_PASSWORD>; set priv-proto aes256; set priv-pwd <PRIV_PASSWORD>; next; end` |
| Core: Cryptography | FIPS-CC mode | 7.0.0 or earlier | NDM `SRG-APP-000179-NDM-000265`; NDM `SRG-APP-000412-NDM-000331`; NDM `SRG-APP-000411-NDM-000330`; ALG `SRG-NET-000510-ALG-000111`; ALG `SRG-NET-000510-ALG-000025`; ALG `SRG-NET-000575-ALG-000020` | `config system fips-cc; set status fips-ciphers; end` |
| Core: Cryptography | FIPS known-answer self-tests | 7.0.0 or earlier | NDM `SRG-APP-000179-NDM-000265`; ALG `SRG-NET-000235-ALG-000118` | `execute fips kat all` |
| Core: Firmware and configuration | Firmware upgrade (web UI, FTP, SCP, or TFTP) | 7.0.0 or earlier | NDM `SRG-APP-000457-NDM-000352`; NDM `SRG-APP-001035-NDM-000340`; NDM `SRG-APP-000131-NDM-000243` | `execute restore image scp <IMAGE> <SERVER>` (after checking the image hash against the Fortinet support site) |
| Core: Firmware and configuration | Configuration backup (manual and scheduled) | 7.0.0 or earlier | NDM `SRG-APP-000516-NDM-000340` | `execute backup full-config scp <FILE> <SERVER>`; `config system scheduled-backup; set destination remote; set remote-protocol sftp; set remote-host <SERVER>; set remote-username <USER>; set remote-password <PASSWORD>; set schedule daily; end` |
| Core: Firmware and configuration | FortiGuard antivirus updates | 7.0.0 or earlier | ALG `SRG-NET-000019-ALG-000019`; ALG `SRG-NET-000246-ALG-000132`; ALG `SRG-NET-000251-ALG-000131` | `config system fortiguard antivirus; set scheduled-update-status enable; set scheduled-update-frequency every; end`; `execute update now` |
| Core: Firmware and configuration | FortiGuard antispam service (real-time queries) | 7.0.0 or earlier | ALG `SRG-NET-000393-ALG-000144`; ALG `SRG-NET-000019-ALG-000019` | `config system fortiguard antispam; set status enable; end` |
| Core: Certificates | Local certificates and certificate requests | 7.0.0 or earlier | NDM `SRG-APP-000516-NDM-000344`; ALG `SRG-NET-000755-ALG-000150` | GUI: System > Certificate > Local Certificate |
| Core: Certificates | CA certificates and certificate revocation lists | 7.0.0 or earlier | NDM `SRG-APP-000910-NDM-000300`; ALG `SRG-NET-000750-ALG-000140`; ALG `SRG-NET-000164-ALG-000100`; NDM `SRG-APP-000875-NDM-000280` | GUI: System > Certificate > CA Certificate; GUI: System > Certificate > Certificate Revocation List |
| Core: High availability | HA clusters (active-passive and active-active) | 7.0.0 or earlier | ALG `SRG-NET-000365-ALG-000123`; ALG `SRG-NET-000236-ALG-000119` | `config system ha; set mode active-passive; set password <HA_PASSWORD>; end` |
| Core: High availability | RAID (hardware models) | 7.0.0 or earlier | ALG `SRG-NET-000365-ALG-000123` | — |
| Core: Deployment | Operation modes (gateway, transparent, server) | 7.0.0 or earlier | ALG `SRG-NET-000018-ALG-000017`; ALG `SRG-NET-000019-ALG-000018` | `config system global; set operation-mode gateway; end` |
| Core: Deployment | Protected domains | 7.0.0 or earlier | ALG `SRG-NET-000364-ALG-000122`; ALG `SRG-NET-000202-ALG-000124` | GUI: Domain & User > Domain > Domain |
| Core: Mail policies | Access control receive rules (relay control; unauthenticated mail to unprotected domains rejected by default) | 7.0.0 or earlier | ALG `SRG-NET-000202-ALG-000124`; ALG `SRG-NET-000364-ALG-000122`; ALG `SRG-NET-000018-ALG-000017` | `config policy access-control receive; edit <RULE>; set status enable; set sender-ip-type ip-mask; set sender-ip-mask <INTERNAL_SUBNET>; set action relay; next; end` |
| Core: Mail policies | Access control delivery rules (TLS and encryption for outgoing mail) | 7.0.0 or earlier | ALG `SRG-NET-000062-ALG-000150`; ALG `SRG-NET-000510-ALG-000111` | `config policy access-control delivery; edit <RULE>; set status enable; set tls-profile <TLS_PROFILE>; next; end` |
| Core: Mail policies | IP-based policies | 7.0.0 or earlier | ALG `SRG-NET-000018-ALG-000017`; ALG `SRG-NET-000364-ALG-000122` | `config policy ip; edit <ID>; set status enable; set source-ip <CLIENT_SUBNET>; set action scan; set profile-session <SESSION_PROFILE>; set profile-antispam <AS_PROFILE>; set profile-antivirus <AV_PROFILE>; set profile-content <CONTENT_PROFILE>; next; end` |
| Core: Mail policies | Recipient-based policies | 7.0.0 or earlier | ALG `SRG-NET-000018-ALG-000017` | `config policy recipient; edit <ID>; set status enable; set direction incoming; set profile-antispam <AS_PROFILE>; set profile-antivirus <AV_PROFILE>; set profile-content <CONTENT_PROFILE>; set profile-dlp <DLP_PROFILE>; next; end` |
| Core: Mail policies | Recipient address verification | 7.0.0 or earlier | ALG `SRG-NET-000364-ALG-000122`; ALG `SRG-NET-000401-ALG-000127` | GUI: Domain & User > Domain > Domain |
| Core: Session profiles | SMTP protocol and command checks | 7.0.0 or earlier | ALG `SRG-NET-000512-ALG-000064`; ALG `SRG-NET-000380-ALG-000128`; ALG `SRG-NET-000401-ALG-000127` | `config profile session; edit <SESSION_PROFILE>; set session-command-checking enable; set session-helo-char-validation enable; set session-helo-domain-check enable; set session-sender-domain-check enable; set session-recipient-domain-check enable; set session-reject-empty-domain enable; set session-prevent-open-relay enable; next; end` |
| Core: Session profiles | Connection and message limits (rate, concurrency, recipients, size) | 7.0.0 or earlier | ALG `SRG-NET-000362-ALG-000112`; ALG `SRG-NET-000705-ALG-000110`; ALG `SRG-NET-000213-ALG-000107` | `config profile session; edit <SESSION_PROFILE>; set conn-rate-number <LIMIT>; set conn-concurrent <LIMIT>; set number-of-messages <LIMIT>; set number-of-recipients <LIMIT>; set conn-idle-timeout <SECONDS>; set limit-max-message-size <LIMIT>; next; end` |
| Core: Session profiles | Sender reputation | 7.0.0 or earlier | ALG `SRG-NET-000362-ALG-000112`; ALG `SRG-NET-000019-ALG-000018` | `config profile session; edit <SESSION_PROFILE>; set sender-reputation-status enable; next; end` |
| Core: Session profiles | Endpoint reputation (carrier networks) | 7.0.0 or earlier | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | `config profile session; edit <SESSION_PROFILE>; set endpoint-reputation disable; next; end` |
| Core: Session profiles | Session safe and block lists | 7.0.0 or earlier | ALG `SRG-NET-000019-ALG-000018` | `config profile session; edit <SESSION_PROFILE>; set sender-blocklist-status enable; set recipient-blocklist-status enable; next; end` |
| Core: Session profiles | DKIM signing of outgoing mail | 7.0.0 or earlier | ALG `SRG-NET-000735-ALG-000130`; ALG `SRG-NET-000510-ALG-000040` | `config profile session; edit <SESSION_PROFILE>; set dkim-signing enable; next; end` |
| Core: Antispam | FortiGuard antispam, IP reputation, and spam outbreak protection | 7.0.0 or earlier | ALG `SRG-NET-000019-ALG-000018`; ALG `SRG-NET-000390-ALG-000139`; ALG `SRG-NET-000393-ALG-000144` | `config profile antispam; edit <AS_PROFILE>; set fortiguard-antispam enable; set fortiguard-check-ip enable; set spam-outbreak-protection enable; next; end` |
| Core: Antispam | SPF, DKIM, and DMARC checks | 7.0.0 or earlier | ALG `SRG-NET-000735-ALG-000130` | `config profile antispam; edit <AS_PROFILE>; set spf-checking enable; set dkim-checking enable; set dmarc-checking enable; next; end` |
| Core: Antispam | Greylisting | 7.0.0 or earlier | ALG `SRG-NET-000019-ALG-000018`; ALG `SRG-NET-000362-ALG-000112` | `config profile antispam; edit <AS_PROFILE>; set greylist enable; next; end` |
| Core: Antispam | Heuristic, DNSBL, and SURBL scans | 7.0.0 or earlier | ALG `SRG-NET-000019-ALG-000018`; ALG `SRG-NET-000390-ALG-000139` | `config profile antispam; edit <AS_PROFILE>; set heuristic enable; set dnsbl enable; set surbl enable; next; end` |
| Core: Antispam | Impersonation analysis | 7.0.0 or earlier | ALG `SRG-NET-000735-ALG-000130`; ALG `SRG-NET-000019-ALG-000018` | `config profile antispam; edit <AS_PROFILE>; set impersonation-analysis enable; set impersonation <IMPERSONATION_PROFILE>; next; end` |
| Core: Antispam | Bounce address tag verification | 7.0.0 or earlier | ALG `SRG-NET-000735-ALG-000130`; ALG `SRG-NET-000019-ALG-000018` | `config antispam settings; set bounce-verification-status enable; end` |
| Core: Antispam | System block and safe lists | 7.0.0 or earlier | ALG `SRG-NET-000019-ALG-000018` | `config antispam settings; set blocklist-action reject; end` |
| Core: Antivirus | Antivirus scanning (signatures, heuristics, grayware) | 7.0.0 or earlier | ALG `SRG-NET-000248-ALG-000133`; ALG `SRG-NET-000249-ALG-000134`; ALG `SRG-NET-000765-ALG-000170` | `config profile antivirus; edit <AV_PROFILE>; set scanner enable; set heuristic enable; set grayware-scan enable; set action-default predefined_av_reject; next; end` |
| Core: Antivirus | Antivirus action profiles (quarantine and notification) | 7.0.0 or earlier | ALG `SRG-NET-000249-ALG-000145`; ALG `SRG-NET-000249-ALG-000146`; ALG `SRG-NET-000770-ALG-000180` | `config profile antivirus-action; edit <AV_ACTION>; set action system-quarantine; set notification-status enable; set notification-profile <NOTIFY_PROFILE>; next; end` |
| Core: Antivirus | Virus outbreak protection | 7.0.0 or earlier | ALG `SRG-NET-000765-ALG-000170`; ALG `SRG-NET-000019-ALG-000019` | `config system fortiguard antivirus; set virus-outbreak enable-with-defer; end`; `config profile antivirus; edit <AV_PROFILE>; set malware-outbreak-protection enable; next; end` |
| Core: Antivirus | FortiSandbox inspection of attachments and URLs | 7.0.0 or earlier | ALG `SRG-NET-000765-ALG-000170`; ALG `SRG-NET-000248-ALG-000133` | `config system fortisandbox; set status enable; set service-type appliance; set host <FSA_FQDN>; end`; `config profile antivirus; edit <AV_PROFILE>; set sandbox-analysis enable; next; end` |
| Core: Content | Attachment filtering by file type | 7.0.0 or earlier | ALG `SRG-NET-000228-ALG-000108`; ALG `SRG-NET-000288-ALG-000109`; ALG `SRG-NET-000289-ALG-000110`; ALG `SRG-NET-000249-ALG-000134` | `config profile content; edit <CONTENT_PROFILE>; config attachment-scan; edit 1; set status enable; set operator is; set patterns <FILE_TYPES>; set action <CONTENT_ACTION>; next; end; next; end` |
| Core: Content | Archive and Microsoft Office file inspection (password-protected, embedded content) | 7.0.0 or earlier | ALG `SRG-NET-000248-ALG-000133`; ALG `SRG-NET-000380-ALG-000128` | `config profile content; edit <CONTENT_PROFILE>; set detect-archive-status enable; set archive-scan-option detect-password-protected block-on-failure-to-decompress; set detect-office-status enable; set office-scan-option detect-password-protected detect-embedded-component; next; end` |
| Core: Content | Content disarm and reconstruction (HTML active content) | 7.0.0 or earlier | ALG `SRG-NET-000288-ALG-000109`; ALG `SRG-NET-000228-ALG-000108` | `config profile content; edit <CONTENT_PROFILE>; set html-content-action modify-content; set html-active-content-action remove; next; end` |
| Core: Content | Data loss prevention profiles | 7.0.0 or earlier | ALG `SRG-NET-000391-ALG-000140` | `config profile dlp; edit <DLP_PROFILE>; set action-default SystemQuarantine; next; end` |
| Core: Encryption | TLS profiles for SMTP sessions | 7.0.0 or earlier | ALG `SRG-NET-000062-ALG-000150`; ALG `SRG-NET-000510-ALG-000111` | `config profile tls; edit <TLS_PROFILE>; set level secure; set check-ssl-version enable; set min-ssl-version tls1_2; next; end` |
| Core: Encryption | TLS versions and ciphers for mail protocols (SMTPS, STARTTLS, IMAPS, POP3S) | 7.0.0 or earlier | ALG `SRG-NET-000062-ALG-000150`; ALG `SRG-NET-000510-ALG-000111` | `config system security crypto; edit mail; set status enable; set ssl-versions tls1_2 tls1_3; set strong-crypto enable; next; end` |
| Core: Encryption | Identity-based encryption (IBE) for external recipients | 7.0.0 or earlier | ALG `SRG-NET-000510-ALG-000111`; ALG `SRG-NET-000169-ALG-000102` | `config profile encryption; edit <ENC_PROFILE>; set protocol ibe; set encryption-algorithm aes256; next; end` |
| Core: Encryption | S/MIME encryption and signing | 7.0.0 or earlier | ALG `SRG-NET-000510-ALG-000111`; ALG `SRG-NET-000510-ALG-000040` | `config profile encryption; edit <ENC_PROFILE>; set protocol smime; set encryption-algorithm aes256; set action encryptandsign; next; end` |
| Core: Quarantine | System quarantine | 7.0.0 or earlier | ALG `SRG-NET-000249-ALG-000145` | `config mailsetting systemquarantine; config folders; edit <FOLDER>; set retention-period <DAYS>; next; end; end` |
| Core: Users | SMTP authentication of email users | 7.0.0 or earlier | ALG `SRG-NET-000138-ALG-000063`; ALG `SRG-NET-000138-ALG-000088`; ALG `SRG-NET-000400-ALG-000097` | `config profile authentication smtp; edit <AUTH_PROFILE>; set server <MAIL_SERVER>; set option ssl secure; next; end`; `config system mailserver; set smtp-auth-over-tls enable; end` |
| Core: Users | Webmail and quarantine access for users | 7.0.0 or earlier | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | `config profile resource; edit <RESOURCE_PROFILE>; set webmail-access disable; next; end` |
| Core: Users | Webmail idle timeout | 7.0.0 or earlier | ALG `SRG-NET-000213-ALG-000107` | `config profile resource; edit <RESOURCE_PROFILE>; set idle-timeout enable; next; end` |
| Core: Users | Login disclaimer after webmail and IBE login (post-login banner) | 7.0.0 or earlier | ALG `SRG-NET-000041-ALG-000022` | `config system global; set post-login-banner admin ibe webmail; end` |
| Core: Mail server | POP3 and IMAP services (server mode) | 7.0.0 or earlier | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | `config system mailserver; set pop3-service disable; set imap-service disable; end` |
| Core: Mail server | Email archiving | 7.0.0 or earlier | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | `config archive account; edit <ARCHIVE>; set status disable; next; end` |
| Core: Mail server | Disclaimers in email | 7.0.0 or earlier | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | `config system disclaimer; set disclaimer-status disable; end` |
| Core: Mail server | Security Fabric connection | 7.0.0 or earlier | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | `config system csf; set status disable; end` |
| Email continuity | Email continuity (users reach incoming mail while the protected mail server is down) | 7.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | `config mailsetting email-continuity; set status disable; end` |
| Users and directories | User account synchronization from LDAP and Microsoft 365 | 7.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| High availability | HA synchronization control (settings excluded from synchronization) | 7.0.0 and later | ALG `SRG-NET-000365-ALG-000123` | — (review the excluded settings with `diagnose system ha show-sync-disable-cfg`) |
| High availability | HA synchronization status on the dashboard and HA pages | 7.0.0 and later | ALG `SRG-NET-000365-ALG-000123` | — |
| Antispam | Cousin domain detection | 7.0.0 and later | ALG `SRG-NET-000735-ALG-000130`; ALG `SRG-NET-000019-ALG-000018` | `config profile antispam; edit <AS_PROFILE>; set cousin-domain enable; set cousin-domain-profile <COUSIN_PROFILE>; next; end` |
| Administrator accounts | More detailed controls in administrator access profiles | 7.0.0 and later | NDM `SRG-APP-000033-NDM-000212`; NDM `SRG-APP-000231-NDM-000271` | `config system accprofile; edit <PROFILE>; config menuitem; edit system_grp; set permission read; next; end; next; end` |
| Encryption | DANE support in TLS profiles | 7.0.0 and later | ALG `SRG-NET-000062-ALG-000150`; ALG `SRG-NET-000164-ALG-000100` | `config profile tls; edit <TLS_PROFILE>; set dane-support opportunistic; next; end` |
| Mail delivery | Sender Rewriting Scheme (SRS) for forwarded mail | 7.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | `config mailsetting sender-rewriting-scheme; set domain-for-rewrite none; end` |
| Platform | Larger maximum values (MSSP license) | 7.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Quarantine | Domain quarantine (MSSP license) | 7.0.0 and later | ALG `SRG-NET-000249-ALG-000145` | — |
| Mail policies | TLS profile enforcement in access control receive rules | 7.0.0 and later | ALG `SRG-NET-000062-ALG-000150`; ALG `SRG-NET-000202-ALG-000124` | `config policy access-control receive; edit <RULE>; set tls-profile <TLS_PROFILE>; next; end` |
| Disclaimers and messages | IP addresses in disclaimer exclusion lists | 7.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Antispam | Block and safe list enhancements (statistics; email, IP/netmask, and reverse DNS entries) | 7.0.0 and later | ALG `SRG-NET-000019-ALG-000018` | — |
| Antispam | Safe list bypass control for SPF, DKIM, and DMARC failures | 7.0.0 and later | ALG `SRG-NET-000735-ALG-000130` | `config antispam settings; set safelist-bypass-sender-auth disable; end` |
| Encryption | TLS versions in TLS profiles | 7.0.0 and later | ALG `SRG-NET-000062-ALG-000150` | `config profile tls; edit <TLS_PROFILE>; set check-ssl-version enable; set min-ssl-version tls1_2; next; end` |
| Disclaimers and messages | Message-ID variable in disclaimer and attachment filtering messages | 7.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Certificates | Trusted CA certificates downloaded from FortiGuard | 7.0.0 and later | ALG `SRG-NET-000750-ALG-000140`; NDM `SRG-APP-000910-NDM-000300` | — (review System > Certificate > Trusted CA against the DoD trust anchors) |
| Content | FortiSandbox and CDR workflow controls | 7.0.0 and later | ALG `SRG-NET-000765-ALG-000170`; ALG `SRG-NET-000288-ALG-000109` | `config file content-disarm-reconstruct; set continue-sandbox-on-cdr enable; end` |
| Antivirus | Archive of email deferred by spam outbreak, virus outbreak, and FortiSandbox | 7.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Monitoring | Deferred email statistics on the dashboard | 7.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Mail server | Oldest email archive command for user mailboxes (server mode) | 7.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Logging | Log search criteria and background log search tasks | 7.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Quarantine | Quarantine search criteria | 7.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Antispam | DKIM failure action in antispam profiles | 7.0.0 and later | ALG `SRG-NET-000735-ALG-000130` | `config profile antispam; edit <AS_PROFILE>; set dkim-checking enable; set dkim-fail-status enable; set action-dkim-fail <ACTION_PROFILE>; next; end` |
| Session profiles | SMTP pipelining control | 7.0.0 and later | ALG `SRG-NET-000512-ALG-000064` | `config profile session; edit <SESSION_PROFILE>; set session-allow-pipelining no; next; end` |
| Platform | Oracle Cloud Infrastructure (OCI) support | 7.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Antivirus | FortiSandbox Cloud regions | 7.0.0 and later | ALG `SRG-NET-000765-ALG-000170` | `config system fortisandbox; set service-type cloud; set region <REGION>; end` |
| Monitoring | Queue history dashboard widget | 7.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Antispam | Sender alignment check of Header From against Reply-To | 7.0.0 and later | ALG `SRG-NET-000735-ALG-000130` | `config profile antispam; edit <AS_PROFILE>; set sender-alignment-status enable; set action-sender-alignment <ACTION_PROFILE>; next; end` |
| Data loss prevention | Text file fingerprints in DLP | 7.0.0 and later | ALG `SRG-NET-000391-ALG-000140` | — |
| Platform | Subscription-based FortiMail VM (S-Series) | 7.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Antispam | Spam submission plugin for Microsoft Outlook | 7.0.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Monitoring | Status monitor of backend mail servers | 7.0.1 and later | ALG `SRG-NET-000365-ALG-000123` | — |
| Email continuity | Smart SMTP recipient verification (queue mail while the mail server is unreachable) | 7.0.1 and later | ALG `SRG-NET-000365-ALG-000123` | `config mailsetting smtp-rcpt-verification; set mode fail-open; end` |
| Cryptography | FIPS mode for cloud VM platforms | 7.0.1 and later | NDM `SRG-APP-000179-NDM-000265`; ALG `SRG-NET-000510-ALG-000111`; ALG `SRG-NET-000575-ALG-000020` | `config system fips-cc; set status fips-ciphers; end` |
| Antispam | DMARC reports (system and domain level) | 7.0.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | `config antispam dmarc-report-generation; set status disable; end` |
| Users and directories | Authentication failover to the second server address (SMTP, IMAP, POP3, RADIUS) | 7.0.1 and later | NDM `SRG-APP-000516-NDM-000336`; ALG `SRG-NET-000138-ALG-000088` | — |
| Platform | FortiMail 2000F and 3000F | 7.0.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Users and directories | User account import for recipient verification (Advanced Management license) | 7.0.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Administrator accounts | Cloning system-level profiles to domain level | 7.0.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Cloud email (Microsoft 365 and Google) | Microsoft 365 Graph API national cloud endpoints | 7.0.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | `config cloud-api setting; set service-endpoint us-dod; end` (when Microsoft 365 API mode is used in a DoD tenant) |
| Encryption | Self-reactivation link in IBE account expiration email | 7.0.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Antispam | Extreme URI checking strictness | 7.0.3 and later | ALG `SRG-NET-000019-ALG-000018` | `config antispam settings; set url-checking <LEVEL>; end` |
| Mail delivery | DSN EHLO/HELO argument customization | 7.0.3+; 7.2.0+ | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Mail delivery | IP pool behavior control for internal-to-internal mail | 7.0.3+; 7.2.0+ | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Antivirus | Microsoft OneNote virus detection | 7.0.6+; 7.2.3+ | ALG `SRG-NET-000248-ALG-000133`; ALG `SRG-NET-000765-ALG-000170` | — |
| Content | Disarmed attachments in deferred scan notifications | 7.0.6+; 7.2.3+ | ALG `SRG-NET-000288-ALG-000109` | — |
| Antivirus | FortiNDR (formerly FortiAI) malware detection in antivirus profiles | 7.2.0 and later | ALG `SRG-NET-000765-ALG-000170` | — |
| Logging | FortiAnalyzer Cloud as a log destination | 7.2.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | `config log setting cloud; set status disable; end` |
| Email continuity | Email continuity enhancements (internal mail, BCC self, address book synchronization, authentication cache) | 7.2.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | `config mailsetting email-continuity; set auth-cache-status disable; end` |
| Mail delivery | Mail queue search actions (send, delete, deliver to alternative host) | 7.2.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Quarantine | Control of quarantined attachment downloads by webmail users | 7.2.0 and later | ALG `SRG-NET-000289-ALG-000110` | — |
| Antispam | Authenticated Received Chain (ARC) validation and sealing | 7.2.0 and later | ALG `SRG-NET-000735-ALG-000130` | `config profile antispam; edit <AS_PROFILE>; set arc-status enable; set action-arc <ACTION_PROFILE>; next; end` |
| Content | Header removal in content and DLP action profiles | 7.2.0 and later | ALG `SRG-NET-000391-ALG-000140` | `config profile content-action; edit <CONTENT_ACTION>; set remove-header enable; next; end` |
| Administrator accounts | Configuration control (restrict domain administrators) | 7.2.0 and later | NDM `SRG-APP-000380-NDM-000304`; ALG `SRG-NET-000700-ALG-000100` | `config system config-control; set domain-admin-restriction enable; end` |
| Antispam | Redirector URL resolution | 7.2.0 and later | ALG `SRG-NET-000019-ALG-000018` | — |
| Disclaimers and messages | Classifier variables in notification templates | 7.2.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Mail delivery | Mail host relay type in mail routing | 7.2.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Antispam | DMARC record policy actions | 7.2.0 and later | ALG `SRG-NET-000735-ALG-000130` | `config profile antispam; edit <AS_PROFILE>; set dmarc-checking enable; set dmarc-policy-reject-status enable; set dmarc-policy-quarantine-status enable; set action-dmarc-policy-reject <ACTION_PROFILE>; set action-dmarc-policy-quarantine <ACTION_PROFILE>; next; end` |
| Encryption | MTA-STS domain checking | 7.2.0 and later | ALG `SRG-NET-000062-ALG-000150`; ALG `SRG-NET-000164-ALG-000100` | `config system mailserver; set smtp-mtasts-status check-external-domain; end` |
| Platform | MSSP advanced management (per-domain statistics, intra-domain protection) | 7.2.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Mail policies | Discard action for recipient verification failures | 7.2.0 and later | ALG `SRG-NET-000364-ALG-000122` | — |
| Content | Local categories in web filtering | 7.2.0 and later | ALG `SRG-NET-000019-ALG-000018` | `config system webfilter local-rating; edit <ID>; set status enable; set pattern-type wildcard; set url-pattern <URL_PATTERN>; set category <CATEGORY>; next; end` |
| Platform | Maturity and feature release tags for GA releases | 7.2.0 and later | NDM `SRG-APP-001035-NDM-000340` | — |
| Quarantine | New variables in quarantine summaries | 7.2.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Disclaimers and messages | Incoming disclaimer for external email only | 7.2.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| System | Description and comment fields | 7.2.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Management access | REST API rate limit | 7.2.0 and later | NDM `SRG-APP-000435-NDM-000315`; ALG `SRG-NET-000705-ALG-000110` | `config system web-service; set max-request-rate-restful <LIMIT>; end` |
| Administrator accounts | CLI privilege levels in administrator profiles | 7.2.0 and later | NDM `SRG-APP-000033-NDM-000212`; NDM `SRG-APP-000340-NDM-000288` | `config system accprofile; edit <PROFILE>; set privilege-level low; set system-diagnostics disable; next; end` |
| System | Utility menu (.msg to .eml converter, regular expression validator) | 7.2.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Mail policies | MAIL FROM customization for SMTP recipient address verification | 7.2.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | `config mailsetting smtp-rcpt-verification; set mail-from-addr <SENDER_EMAIL>; end` |
| Antispam | Automatic aging and retention of block and safe list entries | 7.2.0 and later | ALG `SRG-NET-000019-ALG-000018` | `config antispam settings; set safe-block-list-tracking-status enable; end` |
| Disclaimers and messages | Separate replacement messages for body and attachments | 7.2.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Content | URL neutralization action in CDR and content action profiles | 7.2.0 and later | ALG `SRG-NET-000019-ALG-000018`; ALG `SRG-NET-000288-ALG-000109` | `config profile content; edit <CONTENT_PROFILE>; set html-content-url-action neutralize; set text-content-action neutralize; next; end` |
| Antivirus | FortiSandbox exception for one-time URLs | 7.2.0 and later | ALG `SRG-NET-000765-ALG-000170` | `config system fortisandbox; set bypass-one-time-url disable; end` |
| Antispam | URL resolution before FortiGuard queries | 7.2.0 and later | ALG `SRG-NET-000019-ALG-000018` | — |
| Firmware and configuration | Factory reset that keeps network settings (`execute factoryreset2`) | 7.2.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Cloud email (Microsoft 365 and Google) | Microsoft 365 protection (IP reputation actions, sender and recipient filtering, logging on policy match) | 7.2.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | `config cloud-api setting; set realtime-scan-log all; end` |
| Platform | Load balancers on Microsoft Azure and Oracle Cloud | 7.2.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Authentication | SSO workflow enhancements | 7.2.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Antispam | Business email compromise (BEC) check and action | 7.2.1 and later | ALG `SRG-NET-000735-ALG-000130`; ALG `SRG-NET-000019-ALG-000018` | `config profile antispam; edit <AS_PROFILE>; set bec-scan-status enable; next; end` |
| Antispam | Separate actions for DMARC and DKIM results | 7.2.1 and later | ALG `SRG-NET-000735-ALG-000130` | `config profile antispam; edit <AS_PROFILE>; set dmarc-fail-status enable; set action-dmarc-fail <ACTION_PROFILE>; next; end` |
| Antispam | QR code URL scan in the message body | 7.2.1 and later | ALG `SRG-NET-000019-ALG-000018`; ALG `SRG-NET-000765-ALG-000170` | `config antispam settings; set qr-code-url-scan-status enable; end` |
| Content | Malformed HTML tag handling for URL click protection | 7.2.1 and later | ALG `SRG-NET-000380-ALG-000128` | `config system fortiguard url-protection; set malformed-html-tag-content-action remove; end` |
| Mail policies | Internet Service Database (ISDB) source in ACL rules | 7.2.1 and later | ALG `SRG-NET-000364-ALG-000122` | — |
| Antivirus | FortiSandbox Cloud EMEA region | 7.2.1 and later | ALG `SRG-NET-000765-ALG-000170` | — |
| Antispam | Combined DMARC record and antispam profile actions | 7.2.1 and later | ALG `SRG-NET-000735-ALG-000130` | — |
| Quarantine | Quarantine search by release status | 7.2.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Archiving | Scan of incoming journaled email | 7.2.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Platform | AWS Snowball for FortiMail KVM | 7.2.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Session profiles | FortiGuard IP reputation check granular control | 7.2.2 and later | ALG `SRG-NET-000019-ALG-000018`; ALG `SRG-NET-000138-ALG-000063` | `config profile session; edit <SESSION_PROFILE>; set fortiguard-ip-check-mode as-profile-no-auth; next; end` |
| Disclaimers and messages | Tag Subject option in disclaimer settings | 7.2.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Management access | Repeat offender control for the web service (block IP addresses sending bad HTTP requests) | 7.2.2 and later | NDM `SRG-APP-000435-NDM-000315`; ALG `SRG-NET-000705-ALG-000110` | `config system web-service; set repeat-offender-status enable; set repeat-offender-count <LIMIT>; set repeat-offender-period <MINUTES>; end` |
| Platform | AWS and Azure on-demand licenses | 7.2.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Antispam | Impersonation analysis levels | 7.2.3 and later | ALG `SRG-NET-000735-ALG-000130` | `config antispam settings; set impersonation-analysis-level strict; end` |
| Platform | AWS on-demand VM | 7.2.3 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Content | New FortiGuard web filter categories (AI technology, cryptocurrency) | 7.2.5+; 7.4.1+ | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Logging | IP pool information in logs | 7.2.5+; 7.4.1+ | ALG `SRG-NET-000077-ALG-000046` | — |
| Antispam | BEC weighted analysis, intelligent analysis rule, and action keyword dictionaries | 7.4.0 and later | ALG `SRG-NET-000735-ALG-000130` | `config profile antispam; edit <AS_PROFILE>; set weighted-analysis-status enable; set weighted-analysis-profile <WEIGHTED_PROFILE>; next; end` |
| Antispam | QR code URL scan in attachments | 7.4.0 and later | ALG `SRG-NET-000019-ALG-000018`; ALG `SRG-NET-000765-ALG-000170` | `config antispam settings; set qr-code-url-scan-option attachment-image inline-image; end` |
| Antivirus | Candidate passwords sent to FortiSandbox for password-protected files | 7.4.0 and later | ALG `SRG-NET-000765-ALG-000170` | — |
| Cloud email (Microsoft 365 and Google) | Google Workspace email scan and clawback | 7.4.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Antispam | FortiGuard outbreak deferral as an antispam or content action | 7.4.0 and later | ALG `SRG-NET-000765-ALG-000170`; ALG `SRG-NET-000019-ALG-000018` | `config profile antispam-action; edit <ACTION_PROFILE>; set fortiguard-antispam-outbreak enable; next; end` |
| Antivirus | Zip bomb compression ratio limit | 7.4.0 and later | ALG `SRG-NET-000380-ALG-000128`; ALG `SRG-NET-000705-ALG-000110` | `config mailsetting mail-scan-option; set decompress-max-ratio <RATIO>; end` |
| Antispam | Cousin domain scan of outbound email and look-alike type | 7.4.0 and later | ALG `SRG-NET-000735-ALG-000130` | — |
| Cloud email (Microsoft 365 and Google) | Microsoft 365 per-account scan control | 7.4.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| High availability | HA configuration enhancements (active-passive and active-active, service monitor) | 7.4.0 and later | ALG `SRG-NET-000365-ALG-000123` | — |
| High availability | Active-active HA primary backup and service monitor | 7.4.0 and later | ALG `SRG-NET-000365-ALG-000123`; ALG `SRG-NET-000362-ALG-000120` | — |
| Authentication | Multiple identity providers for SAML SSO | 7.4.0 and later | NDM `SRG-APP-000516-NDM-000336` | — |
| Mail policies | ISDB source type in IP-based policies | 7.4.0 and later | ALG `SRG-NET-000364-ALG-000122` | `config policy ip; edit <ID>; set source-type isdb; next; end` |
| Mail delivery | SMTPUTF8 support (RFC 6530 to 6533) | 7.4.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | `config system mailserver; set smtp-smtputf8 disable; end` |
| Encryption | Fallback to IBE when TLS fails | 7.4.0 and later | ALG `SRG-NET-000510-ALG-000111` | `config profile encryption; edit <ENC_PROFILE>; set protocol ibe-on-tls-failure; next; end` |
| Cloud email (Microsoft 365 and Google) | Microsoft 365 system quarantine release enhancement | 7.4.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Cloud email (Microsoft 365 and Google) | Azure AD group membership for Microsoft 365 users | 7.4.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Disclaimers and messages | Customized messages in domain disclaimers | 7.4.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Mail delivery | Customized bounce (DSN) email | 7.4.0 and later | ALG `SRG-NET-000273-ALG-000129` | `config system mailserver; set dsn-email-customization-status enable; end` |
| Firmware and configuration | Web proxy for FortiGuard antivirus updates and antispam queries | 7.4.0 and later | ALG `SRG-NET-000019-ALG-000019` | `config system fortiguard antivirus; set tunneling-status enable; set tunneling-address <PROXY>; set tunneling-port <PORT>; end` |
| Content | Web proxy for the shortened URL service | 7.4.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Platform | Alibaba Cloud | 7.4.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Users and directories | Automatic removal of inactive accounts | 7.4.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Mail server | Domain-level disk quota (server mode) | 7.4.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Antispam | Defer delivery action in antispam and content action profiles | 7.4.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Administrator accounts | Read-update permission in administrator profiles | 7.4.0 and later | NDM `SRG-APP-000033-NDM-000212`; NDM `SRG-APP-000380-NDM-000304` | `config system accprofile; edit <PROFILE>; config menuitem; edit policy_grp; set permission read-update; next; end; next; end` |
| Certificates | Elliptic curve keys in certificate signing requests | 7.4.0 and later | NDM `SRG-APP-000516-NDM-000344` | — |
| Logging | Access control delivery rule ID in event logs | 7.4.0 and later | ALG `SRG-NET-000074-ALG-000043` | — |
| Administrator accounts | Certificate-based SSH key for administrators | 7.4.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — (no setting found in the 8.0.0 CLI Reference syntax for `config system admin`) |
| Disclaimers and messages | Disclaimers in Outlook appointment email | 7.4.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Antispam | DKIM signing of DSNs and system notifications | 7.4.0 and later | ALG `SRG-NET-000735-ALG-000130` | — |
| High availability | Block and safe list synchronization in active-active HA | 7.4.0 and later | ALG `SRG-NET-000365-ALG-000123` | — |
| Management access | Exempt IP list for web service repeat offender control | 7.4.0 and later | NDM `SRG-APP-000435-NDM-000315` | — |
| Users and directories | User preference enhancements | 7.4.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Administrator accounts | Automatic FortiToken push after login credentials | 7.4.0 and later | NDM `SRG-APP-000820-NDM-000170` | — |
| Management access | New CLI console in the administrator GUI | 7.4.0 and later | NDM `SRG-APP-000408-NDM-000314` | — |
| Disclaimers and messages | Inline attachment replacement message | 7.4.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Disclaimers and messages | Message-ID in notification email | 7.4.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Mail policies | Recipient policy move action in all display modes | 7.4.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Webmail | Email address auto completion | 7.4.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Webmail | Address book search enhancement | 7.4.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Webmail | Display columns | 7.4.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Webmail | Email tags | 7.4.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Webmail | Mobile device view | 7.4.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Antispam | Outlook spam submission for macOS, OWA, and Microsoft 365 | 7.4.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Antispam | Archive files and QR code URLs embedded in images | 7.4.1 and later | ALG `SRG-NET-000248-ALG-000133`; ALG `SRG-NET-000019-ALG-000018` | — |
| Logging | HA cluster log search for domain administrators | 7.4.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| System | CLI command to retrieve default values (`get default-value`) | 7.4.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Cloud email (Microsoft 365 and Google) | Read or unread status as a clawback condition | 7.4.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Cloud email (Microsoft 365 and Google) | Microsoft 365 and Google Workspace information on the dashboard | 7.4.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Disclaimers and messages | Attachment replacement message location | 7.4.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Mail policies | Email and IP group import and export | 7.4.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Users and directories | Client certificate authentication in LDAP profiles | 7.4.2 and later | NDM `SRG-APP-000516-NDM-000336`; ALG `SRG-NET-000138-ALG-000088` | `config profile ldap; edit <LDAP>; set secure ssl; set client-cert-auth enable; set client-cert <CLIENT_CERT>; next; end` |
| Antispam | Per-domain DMARC failure actions | 7.4.2 and later | ALG `SRG-NET-000735-ALG-000130` | — |
| Content | Image source exemption from URL neutralization | 7.4.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Disclaimers and messages | Sender domain variable in disclaimers | 7.4.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Webmail | Sending from a webmail secondary account | 7.4.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Authentication | Dynamic IP addresses within a SAML session | 7.4.3+; 7.6.0+ | ALG `SRG-NET-000230-ALG-000113` | `config system saml; set dynamic-ip-status disable; end` (unless clients change addresses during a session) |
| Encryption | UAE local SMS gateway (Etisalat) for IBE two-factor authentication | 7.4.3 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Logging | Logs of user mail moves in the Microsoft 365 and Google API views | 7.4.4 and later | ALG `SRG-NET-000079-ALG-000048` | — |
| Time | British Columbia permanent DST time zone | 7.4.7 and later | NDM `SRG-APP-000374-NDM-000299` | — |
| Time | Alberta and Manitoba permanent DST time zones | 7.4.9 and later | NDM `SRG-APP-000374-NDM-000299` | — |
| Cloud email (Microsoft 365 and Google) | On-premises Microsoft Exchange email scan | 7.6.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Antispam | FortiGuard sender and recipient relation (SRR) scoring for BEC | 7.6.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Antispam | Spam submissions visible per domain to domain administrators | 7.6.0 and later | NDM `SRG-APP-000033-NDM-000212` | `config system fortiguard antispam; set submission-per-domain enable; end` |
| Antispam | QR code URL scan in PDF attachments | 7.6.0 and later | ALG `SRG-NET-000019-ALG-000018`; ALG `SRG-NET-000765-ALG-000170` | `config antispam settings; set qr-code-url-scan-pdf enable; end` |
| Antispam | STIX/TAXII threat feeds | 7.6.0 and later | ALG `SRG-NET-000019-ALG-000019`; ALG `SRG-NET-000019-ALG-000018` | `config system threat-feed; edit <FEED>; set status enable; set server-identity-check full; next; end` |
| Quarantine | System and domain quarantine notifications with release requests | 7.6.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Antispam | DMARC result overriding SPF and DKIM | 7.6.0 and later | ALG `SRG-NET-000735-ALG-000130` | `config profile antispam; edit <AS_PROFILE>; set dmarc-override-option override-dkim override-spf; next; end` |
| Antispam | Sender alignment bypass of Reply-To and display name checks | 7.6.0 and later | ALG `SRG-NET-000735-ALG-000130` | `config profile antispam; edit <AS_PROFILE>; set sender-alignment-option display-name reply-to; next; end` (keep both checks selected) |
| Antivirus | LZH and LHA archive scan | 7.6.0 and later | ALG `SRG-NET-000248-ALG-000133` | — |
| Antispam | DKIM signing of mail within the same protected domain | 7.6.0 and later | ALG `SRG-NET-000735-ALG-000130` | — |
| Content | Exempt image URLs from rewriting, removal, and isolation | 7.6.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Logging | Delivery status of outgoing email in history logs | 7.6.0 and later | ALG `SRG-NET-000078-ALG-000047` | `config system mailserver; set delivery-tracking-status enable; end` |
| Mail policies | LDAP groups and IP groups in access control delivery rules | 7.6.0 and later | ALG `SRG-NET-000018-ALG-000017` | — |
| High availability | Group HA | 7.6.0 and later | ALG `SRG-NET-000365-ALG-000123` | — |
| Encryption | Per-domain IBE URL in IBE notifications | 7.6.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Mail policies | Recipient exclusions in recipient policies | 7.6.0 and later | ALG `SRG-NET-000018-ALG-000017` | — |
| Firmware and configuration | Configuration download prompt before upgrading | 7.6.0 and later | NDM `SRG-APP-000516-NDM-000340` | — |
| Platform | HVM on XenServer | 7.6.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Mail policies | Reverse DNS pattern in IP-based policies | 7.6.0 and later | ALG `SRG-NET-000364-ALG-000122` | — |
| Antispam | DMARC report collector and statistics | 7.6.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Users and directories | Global editing of user preferences | 7.6.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Quarantine | Web release page customization | 7.6.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Logging | Syslog message delimiter option for TCP | 7.6.0 and later | ALG `SRG-NET-000334-ALG-000050` | — |
| Logging | Time zone in raw logs | 7.6.0 and later | NDM `SRG-APP-000374-NDM-000299`; ALG `SRG-NET-000075-ALG-000044` | — |
| Webmail | Calendar and CalDAV tasks | 7.6.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Encryption | Dedicated IBE portal URL | 7.6.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Webmail | LDAP display name for webmail users | 7.6.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Platform | FortiFlex on VM platforms | 7.6.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Monitoring | Click protection statistics in FortiView | 7.6.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Session profiles | Bare line feed handling (SMTP smuggling) | 7.6.2 and later | ALG `SRG-NET-000512-ALG-000064`; ALG `SRG-NET-000380-ALG-000128` | `config system mailserver; set smtp-eom-bare-lf-handling disallow; end` |
| Mail delivery | Mail queue delivery attempt controls | 7.6.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Logging | Reliable logging to FortiAnalyzer | 7.6.2 and later | NDM `SRG-APP-000515-NDM-000325`; ALG `SRG-NET-000334-ALG-000050`; ALG `SRG-NET-000511-ALG-000051` | `config log setting remote; edit <FAZ>; set reliable enable; next; end` |
| Users and directories | Sender identity check for authenticated users against LDAP | 7.6.2 and later | ALG `SRG-NET-000735-ALG-000130`; ALG `SRG-NET-000138-ALG-000063` | `config policy recipient; edit <ID>; set smtp-diff-identity enable; set smtp-diff-identity-ldap enable; set smtp-diff-identity-ldap-profile <LDAP>; next; end` |
| Mail policies | Recipient policy search and display | 7.6.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Firmware and configuration | FQDN for the FortiGuard HTTP proxy | 7.6.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Logging | Log level filter in log search | 7.6.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Email continuity | Per-domain recipient verification mode for email continuity recipients | 7.6.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Encryption | IBE user password reset by administrators | 7.6.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Mail policies | Member search in group profiles | 7.6.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Webmail | Drag and drop attachment upload | 7.6.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Mail policies | LDAP source and forged IP check in receiving ACL rules | 7.6.3 and later | ALG `SRG-NET-000364-ALG-000122`; ALG `SRG-NET-000735-ALG-000130` | `config policy access-control receive; edit <RULE>; set forged-ip-check fail; next; end` |
| Mail delivery | Mail host port LDAP attribute in mail routing | 7.6.3 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| System | Diagnose command reorganization (`diagnose debug setting`) | 7.6.3 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Antispam | Individual actions for each DMARC policy (p=) value | 7.6.3 and later | ALG `SRG-NET-000735-ALG-000130` | `config profile antispam; edit <AS_PROFILE>; set dmarc-policy-none-status enable; set action-dmarc-policy-none <ACTION_PROFILE>; next; end` |
| Content | XML attachment exemption from click protection URL rewrite | 7.6.3 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| System | GUI enhancements (resizable windows, comment columns, LDAP browse search) | 7.6.3 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Mail delivery | Enhanced queue runner | 7.6.4 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Mail policies | Envelope From or Header From as the sender in recipient policies | 7.6.4 and later | ALG `SRG-NET-000735-ALG-000130` | `config system advanced-management; set recipient-policy-sender-option envelope-or-header-from; end` |
| Authentication | Separate SAML service providers for the administrator GUI and webmail | 7.6.4+; 8.0.0+ | NDM `SRG-APP-000516-NDM-000336` | `config system saml; set second-sp-status enable; set second-sp-entity-id <ENTITY_ID>; set second-hostname <FQDN>; end` |
| SNMP | SNMPv3 SHA-2 authentication and AES-256 privacy | 7.6.5+; 8.0.0+ | NDM `SRG-APP-000395-NDM-000310` | `config system snmp user; edit <SNMP_USER>; set security-level authpriv; set auth-proto sha256; set priv-proto aes256; next; end` |
| Cloud email (Microsoft 365 and Google) | Microsoft 365 inline scan through Exchange Online connectors | 8.0.0 and later | ALG `SRG-NET-000018-ALG-000017` | `config mailsetting ms365-inline-setting; set cert <LOCAL_CERT>; set trusted-ip <IP_GROUP>; end` |
| Cloud email (Microsoft 365 and Google) | Microsoft 365 shared mailbox scan | 8.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Cloud email (Microsoft 365 and Google) | Notifications sent by the FortiMail MTA in Microsoft and Google API mode | 8.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Content | Password prompt for scanning password-protected attachments | 8.0.0 and later | ALG `SRG-NET-000248-ALG-000133` | `config profile content; edit <CONTENT_PROFILE>; set decrypt-password-method prompt-user-input; next; end` |
| Antispam | QR code URL scan in PDF archives | 8.0.0 and later | ALG `SRG-NET-000019-ALG-000018`; ALG `SRG-NET-000765-ALG-000170` | — |
| Quarantine | Rescan of email released from quarantine | 8.0.0 and later | ALG `SRG-NET-000248-ALG-000133`; ALG `SRG-NET-000765-ALG-000170` | `config mailsetting quarantine-release-rescan-setting; set status enable; set type antispam antivirus content dlp fortisandbox; end` |
| Content | Office file metadata and HTML hidden content handling | 8.0.0 and later | ALG `SRG-NET-000391-ALG-000140`; ALG `SRG-NET-000288-ALG-000109` | `config profile content; edit <CONTENT_PROFILE>; set cdr-office-metadata-action remove; set html-hidden-content-action remove; next; end` |
| Mail policies | Sender match on envelope, header From, or both in access control receive rules | 8.0.0 and later | ALG `SRG-NET-000735-ALG-000130` | `config policy access-control receive; edit <RULE>; set sender-option envelope-or-header-from; next; end` |
| Antispam | Reply-To header in safe list checks | 8.0.0 and later | ALG `SRG-NET-000735-ALG-000130` | `config antispam settings; set safelist-check-header-reply-to enable; end` |
| Management access | New administrator GUI framework | 8.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Administrator accounts | Administrator MFA with FortiIdentity Cloud | 8.0.0 and later | NDM `SRG-APP-000820-NDM-000170`; NDM `SRG-APP-000825-NDM-000180` | `config system global; set fortiidentity-cloud-status enable; end`; `config system admin; edit <ADMIN>; set tfa-status enable; set tfa-type fortiidentity-cloud; next; end` |
| Management access | Client IP address from an HTTP X-header | 8.0.0 and later | NDM `SRG-APP-000038-NDM-000213` | `config system web-service; set client-ip-x-header-status disable; end` (unless a trusted proxy or load balancer sets the header) |
| Monitoring | Released and unreleased quarantine counts | 8.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Monitoring | Disk usage history widget | 8.0.0 and later | NDM `SRG-APP-000357-NDM-000293` | — |
| Monitoring | TLS connection statistics in FortiView | 8.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Antispam | Personal block and safe list size limit and tracking | 8.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Mail policies | Sender exclusions in recipient policies | 8.0.0 and later | ALG `SRG-NET-000018-ALG-000017` | — |
| Administrator accounts | Secure (TLS) RADIUS | 8.0.0 and later | NDM `SRG-APP-000516-NDM-000336`; NDM `SRG-APP-000172-NDM-000259`; ALG `SRG-NET-000400-ALG-000097` | `config profile authentication radius; edit <RADIUS>; set transport-protocol tls; set ca-cert <CA_CERT>; next; end` |
| Cloud email (Microsoft 365 and Google) | Archive action in Microsoft and Google API mode | 8.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Disclaimers and messages | Disclaimer handling in mobile notification previews | 8.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Session profiles | Regular expressions in session profile header manipulation | 8.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Logging | Delivering status and failure reason in mail delivery status | 8.0.0 and later | ALG `SRG-NET-000078-ALG-000047` | — |
| Logging | Mail delivery status on FortiAnalyzer | 8.0.0 and later | ALG `SRG-NET-000334-ALG-000050` | `config system mailserver; set delivery-tracking-on-faz-status enable; end` |
| System | SED auto lock on FortiMail 900G | 8.0.0 and later | ALG `SRG-NET-000755-ALG-000150` | — |
| Archiving | Port numbers for remote email archive servers | 8.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Users and directories | FortiAuthenticator integration for user accounts (server mode) | 8.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Administrator accounts | Separate firmware upgrade permission in access profiles | 8.0.0 and later | NDM `SRG-APP-000378-NDM-000302`; NDM `SRG-APP-000033-NDM-000212` | — |
| Content | OCR scan of images (license) | 8.0.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Mail delivery | Relay host in access control delivery rules | 8.0.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| System | DNS cache maximum TTL | 8.0.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — (the cache-max-ttl option named in the 8.0.2 release notes is not in the 8.0.0 CLI Reference) |
| Encryption | AES-GCM for S/MIME | 8.0.2 and later | ALG `SRG-NET-000510-ALG-000111` | — |
| Mail policies | Country exclusions in GeoIP groups | 8.0.2 and later | ALG `SRG-NET-000364-ALG-000122` | — |
| Archiving | Original email repackaged as an attachment in archive accounts | 8.0.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Antivirus | FortiSandbox report download from the history log | 8.0.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Administrator accounts | Firmware restore by administrators with read-write access | 8.0.2 and later | NDM `SRG-APP-000378-NDM-000302`; NDM `SRG-APP-000033-NDM-000212` | — |
| Monitoring | Recent email statistics and log dashboard | 8.0.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Logging | Display name and Reply-To in history logs | 8.0.2 and later | ALG `SRG-NET-000079-ALG-000048` | — |
| Content | CDR component types in the GUI | 8.0.2 and later | ALG `SRG-NET-000288-ALG-000109` | — |

### Requirement reference

The requirements used in the map and in this chapter's text, with their
severity in the current SRG releases:

[Download the requirement reference as CSV](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/data/volume-172-disa-srgs-and-stigs/17-fortimail-feature-version-and-srg-map-requirements.csv) (115 rows).

| SRG | Requirement | Severity | Requirement title |
| --- | --- | --- | --- |
| ALG | `SRG-NET-000015-ALG-000016` | CAT II | The ALG must enforce approved authorizations for logical access to information and system resources by employing identity-based, role-based, and/or attribute-based security policies. |
| ALG | `SRG-NET-000018-ALG-000017` | CAT II | The ALG must enforce approved authorizations for controlling the flow of information within the network based on attribute- and content-based inspection of the source, destination, headers, and/or content of the communications traffic. |
| ALG | `SRG-NET-000019-ALG-000018` | CAT II | The ALG must restrict or block harmful or suspicious communications traffic by controlling the flow of information between interconnected networks based on attribute- and content-based inspection of the source, destination, headers, and/or content of the communications traffic. |
| ALG | `SRG-NET-000019-ALG-000019` | CAT II | The ALG must immediately use updates made to policy enforcement mechanisms such as policy filters, rules, signatures, and analysis algorithms for gateway and/or intermediary functions. |
| ALG | `SRG-NET-000041-ALG-000022` | CAT II | The ALG providing user access control intermediary services must display the Standard Mandatory DoD-approved Notice and Consent Banner before granting access to the network. |
| ALG | `SRG-NET-000062-ALG-000150` | CAT II | The ALG that provides intermediary services for TLS must be configured to comply with the required TLS settings in NIST SP 800-52. |
| ALG | `SRG-NET-000074-ALG-000043` | CAT II | The ALG must produce audit records containing information to establish what type of events occurred. |
| ALG | `SRG-NET-000075-ALG-000044` | CAT II | The ALG must produce audit records containing information to establish when (date and time) the events occurred. |
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
| ALG | `SRG-NET-000164-ALG-000100` | CAT II | The ALG that provides intermediary services for TLS must validate certificates used for TLS functions by performing RFC 5280-compliant certification path validation. |
| ALG | `SRG-NET-000169-ALG-000102` | CAT II | The ALG providing user authentication intermediary services must uniquely identify and authenticate non-organizational users (or processes acting on behalf of non-organizational users). |
| ALG | `SRG-NET-000202-ALG-000124` | CAT II | The ALG must deny network communications traffic by default and allow network communications traffic by exception (i.e., deny all, permit by exception). |
| ALG | `SRG-NET-000213-ALG-000107` | CAT II | The ALG must terminate all network connections associated with a communications session at the end of the session, or as follows: for in-band management sessions (privileged sessions), the session must be terminated after 10 minutes of inactivity; and for user sessions (non-privileged session), the session must be terminated after 15 minutes of inactivity. |
| ALG | `SRG-NET-000228-ALG-000108` | CAT II | The ALG must detect, at a minimum, mobile code that is unsigned or exhibiting unusual behavior, has not undergone a risk assessment, or is prohibited for use based on a risk assessment. |
| ALG | `SRG-NET-000230-ALG-000113` | CAT II | The ALG must protect the authenticity of communications sessions. |
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
| ALG | `SRG-NET-000334-ALG-000050` | CAT II | The ALG must off-load audit records onto a centralized log server. |
| ALG | `SRG-NET-000335-ALG-000053` | CAT II | The ALG must provide an immediate real-time alert to, at a minimum, the SCA and ISSO, of all audit failure events where the detection and/or prevention function is unable to write events to either local storage or the centralized server. |
| ALG | `SRG-NET-000362-ALG-000112` | CAT II | The ALG providing content filtering must protect against known and unknown types of Denial of Service (DoS) attacks by employing rate-based attack prevention behavior analysis. |
| ALG | `SRG-NET-000362-ALG-000120` | CAT II | The ALG must implement load balancing to limit the effects of known and unknown types of Denial of Service (DoS) attacks. |
| ALG | `SRG-NET-000364-ALG-000122` | CAT II | The ALG must only allow incoming communications from organization-defined authorized sources routed to organization-defined authorized destinations. |
| ALG | `SRG-NET-000365-ALG-000123` | CAT II | The ALG must fail securely in the event of an operational failure. |
| ALG | `SRG-NET-000370-ALG-000125` | CAT II | The ALG must identify and log internal users associated with denied outgoing communications traffic posing a threat to external information systems. |
| ALG | `SRG-NET-000380-ALG-000128` | CAT II | The ALG must behave in a predictable and documented manner that reflects organizational and system objectives when invalid inputs are received. |
| ALG | `SRG-NET-000390-ALG-000139` | CAT II | The ALG providing content filtering must continuously monitor inbound communications traffic crossing internal security boundaries for unusual or unauthorized activities or conditions. |
| ALG | `SRG-NET-000391-ALG-000140` | CAT II | The ALG providing content filtering must continuously monitor outbound communications traffic crossing internal security boundaries for unusual/unauthorized activities or conditions. |
| ALG | `SRG-NET-000392-ALG-000141` | CAT II | The ALG providing content filtering must send an alert to, at a minimum, the ISSO and ISSM when detection events occur. |
| ALG | `SRG-NET-000393-ALG-000144` | CAT II | The ALG that implements spam protection mechanisms must be updated automatically. |
| ALG | `SRG-NET-000400-ALG-000097` | CAT I | The ALG providing user authentication intermediary services must transmit only encrypted representations of passwords. |
| ALG | `SRG-NET-000401-ALG-000127` | CAT II | The ALG must check the validity of all data inputs except those specifically identified by the organization. |
| ALG | `SRG-NET-000510-ALG-000025` | CAT II | The ALG providing encryption intermediary services must implement NIST FIPS-validated cryptography to generate cryptographic hashes. |
| ALG | `SRG-NET-000510-ALG-000040` | CAT II | The ALG providing encryption intermediary services must implement NIST FIPS-validated cryptography for digital signatures. |
| ALG | `SRG-NET-000510-ALG-000111` | CAT II | The ALG providing encryption intermediary services must use NIST FIPS-validated cryptography to implement encryption services. |
| ALG | `SRG-NET-000511-ALG-000051` | CAT II | The ALG must off-load audit records onto a centralized log server in real time. |
| ALG | `SRG-NET-000512-ALG-000064` | CAT II | The ALG that provides intermediary services for SMTP must inspect inbound and outbound SMTP and Extended SMTP communications traffic for protocol compliance and protocol anomalies. |
| ALG | `SRG-NET-000575-ALG-000020` | CAT II | The ALG must use a FIPS-validated cryptographic module to implement encryption services for unclassified information requiring confidentiality. |
| ALG | `SRG-NET-000700-ALG-000100` | CAT II | The ALG must prevent or restrict changes to the configuration of the system under organization-defined circumstances. |
| ALG | `SRG-NET-000705-ALG-000110` | CAT II | The ALG must employ organization-defined controls by type of denial of service (DoS) to achieve the DoS objective. |
| ALG | `SRG-NET-000735-ALG-000130` | CAT II | The ALG must implement antispoofing mechanisms to prevent adversaries from falsifying the security attributes indicating the successful application of the security process. |
| ALG | `SRG-NET-000750-ALG-000140` | CAT II | The ALG must include only approved trust anchors in trust stores or certificate stores managed by the organization. |
| ALG | `SRG-NET-000755-ALG-000150` | CAT II | The ALG must provide protected storage for cryptographic keys with organization-defined safeguards and/or hardware protected key store. |
| ALG | `SRG-NET-000765-ALG-000170` | CAT II | The ALG must implement signature based and/or nonsignature based malicious code protection mechanisms at system entry and exit points to detect and eradicate malicious code. |
| ALG | `SRG-NET-000770-ALG-000180` | CAT II | The ALG must configure malicious code protection mechanisms to send alerts to organization-defined personnel in response to malicious code detection. |
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
| NDM | `SRG-APP-000149-NDM-000247` | CAT I | The network device must be configured to use DoD PKI as multi-factor authentication (MFA) for interactive logins. |
| NDM | `SRG-APP-000153-NDM-000249` | CAT II | The network device must be configured to authenticate each administrator prior to authorizing privileges based on assignment of group or role. |
| NDM | `SRG-APP-000164-NDM-000252` | CAT II | The network device must enforce a minimum 15-character password length. |
| NDM | `SRG-APP-000166-NDM-000254` | CAT II | The network device must enforce password complexity by requiring that at least one uppercase character be used. |
| NDM | `SRG-APP-000167-NDM-000255` | CAT II | The network device must enforce password complexity by requiring that at least one lowercase character be used. |
| NDM | `SRG-APP-000168-NDM-000256` | CAT II | The network device must enforce password complexity by requiring that at least one numeric character be used. |
| NDM | `SRG-APP-000169-NDM-000257` | CAT II | The network device must enforce password complexity by requiring that at least one special character be used. |
| NDM | `SRG-APP-000170-NDM-000329` | CAT II | The network device must require that when a password is changed, the characters are changed in at least eight of the positions within the password. |
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
| NDM | `SRG-APP-000435-NDM-000315` | CAT II | The network device must be configured to protect against known types of denial-of-service (DoS) attacks by employing organization-defined security safeguards. |
| NDM | `SRG-APP-000457-NDM-000352` | CAT II | The network device must install security-relevant firmware updates within 30 days unless the time period is directed by an authoritative source (e.g., IAVM, CTOs, DTMs, STIGs). |
| NDM | `SRG-APP-000503-NDM-000320` | CAT II | The network device must generate audit records when successful/unsuccessful logon attempts occur. |
| NDM | `SRG-APP-000505-NDM-000322` | CAT II | The network device must generate audit records showing starting and ending time for administrator access to the system. |
| NDM | `SRG-APP-000515-NDM-000325` | CAT II | The network device must off-load audit records onto a different system or media than the system being audited. |
| NDM | `SRG-APP-000516-NDM-000336` | CAT I | The network device must be configured to use at least one authentication server for the purpose of authenticating users prior to granting administrative access. For boundary devices, two authentication servers are required. |
| NDM | `SRG-APP-000516-NDM-000340` | CAT II | The network device must be configured to conduct backups of system level information contained in the information system when changes occur. |
| NDM | `SRG-APP-000516-NDM-000344` | CAT II | The network device must obtain its public key certificates from an appropriate certificate policy through an approved service provider. |
| NDM | `SRG-APP-000516-NDM-000350` | CAT I | The network device must be configured to send log data to at least one central log server for the purpose of forwarding alerts to the administrators and the information system security officer (ISSO). For boundary devices, two log servers are required. |
| NDM | `SRG-APP-000820-NDM-000170` | CAT II | The network device must be configured to implement multifactor authentication for local; network; and/or remote access to privileged accounts; and/or nonprivileged accounts such that one of the factors is provided by a device separate from the system gaining access. |
| NDM | `SRG-APP-000825-NDM-000180` | CAT II | The network device must be configured to implement multifactor authentication for local; network; and/or remote access to privileged accounts; and/or nonprivileged accounts such that the device meets organization-defined strength of mechanism requirements. |
| NDM | `SRG-APP-000845-NDM-000220` | CAT II | The network device must be configured to verify, when users create or update passwords, the passwords are not found on the list of commonly used, expected, or compromised passwords in IA-5 (1) (a) for password-based authentication. |
| NDM | `SRG-APP-000860-NDM-000250` | CAT II | The network device must be configured to allow user selection of long passwords and passphrases, including spaces and all printable characters for password-based authentication. |
| NDM | `SRG-APP-000875-NDM-000280` | CAT II | The network device must be configured to implement certificate revocation checking to support path discovery and validation for public key-based authentication. |
| NDM | `SRG-APP-000910-NDM-000300` | CAT II | The network device must be configured to include only approved trust anchors in trust stores or certificate stores managed by the organization. |
| NDM | `SRG-APP-000920-NDM-000320` | CAT II | The network device must be configured to synchronize system clocks within and between systems or system components. |
| NDM | `SRG-APP-001035-NDM-000340` | CAT I | The network device hardware and software must be a version supported by the vendor. |

### Collecting evidence

Enter `show` in each configuration section that the map cites, at least
`config system global`, `config system admin`, `config system accprofile`,
`config system password-policy`, `config system interface`,
`config system time ntp`, `config system snmp user`,
`config system fips-cc`, `config log setting remote`,
`config policy access-control receive`, `config policy ip`,
`config policy recipient`, and the session, antispam, antivirus, content,
and TLS profiles, and run `get system status` for the release and
operation mode. Export the event, history, antivirus, and antispam logs
from the central log server, and keep the FortiGuard update status and the
firmware hash record with the checklist.

## Validation and Troubleshooting

- **A feature in the map is missing on your FortiMail.** Check the version
  column against the FortiMail release, and check whether the feature
  depends on the operation mode, the platform, or a license.
- **A command is rejected.** The command was checked against the 8.0.0 CLI
  Reference. Older releases may lack the option or spell it differently;
  check the CLI Reference of your release.
- **A profile setting has no effect.** Profiles apply only through a
  policy. Check which IP-based or recipient-based policy matches the
  message, and its order.
- **Mail is relayed or rejected unexpectedly.** Check the access control
  receive rules, their order, and the protected domains. With no matching
  rule, FortiMail relays mail from authenticated clients and rejects mail
  from unauthenticated clients to unprotected domains.
- **Administrators cannot log in after hardening.** Check trusted hosts,
  the lockout and authentication reputation block, PKI mode and the PKI
  user, and the RADIUS or LDAP profile.
- **A requirement has no matching feature.** Some requirements are met by
  procedure (firmware hash, password changes), by another system (the
  authentication server, the central log server, the time servers), or not
  at all on older releases (SNMPv3 SHA-2). Record how each requirement is
  met, not just which feature covers it.

## Security and Best Practices

- Keep FortiMail on a vendor-supported release and install patches
  promptly, after checking the image hash.
- Set administrator passwords of at least 15 characters, use DoD PKI or a
  remote authentication server for administrator login, and keep one local
  account of last resort.
- Allow only HTTPS and SSH on the management interface, with TLS 1.2 or
  later, strong ciphers, trusted hosts, and the pre-login banner.
- Send event, history, antivirus, and antispam logs to a central log server
  over TLS, and use SNMPv3 with authentication and privacy only.
- Keep FortiGuard antivirus and antispam services current, and review this
  map each time Fortinet publishes a FortiMail release or DISA updates the
  ALG or NDM SRG.

## References and Knowledge Checks

**References:**

- Fortinet, *FortiMail Release Notes*, section "What's new", releases 7.0.0
  to 7.0.9, 7.2.0 to 7.2.9, 7.4.0 to 7.4.7, 7.4.9, 7.6.0 to 7.6.5, 7.6.7,
  8.0.0, and 8.0.2 (docs.fortinet.com, FortiMail documentation).
- Fortinet, *FortiMail 8.0.0 CLI Reference*, *FortiMail 7.0.0 CLI
  Reference* (table of contents), and *FortiMail 8.0.2 Administration
  Guide*.
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

1. Which two SRGs apply to FortiMail, and which part of the appliance does
   each one cover?
2. Where does the version data come from, given that FortiMail has no
   feature matrix, New Features Guide, or "What's new" chapter in its
   Administration Guide?
3. Which ALG requirement covers SMTP protocol compliance, and which
   FortiMail profile implements it?
4. Which ALG requirements do not apply to FortiMail, and why?
5. Which requirements can FortiMail not meet exactly, and how do you handle
   them?
6. What applies to a feature marked "No direct requirement"?

## Summary and Completion Checklist

FortiMail has no STIG, so it is assessed against the ALG SRG for its email
gateway and the NDM SRG for its management plane. This chapter maps
331 features to the FortiMail release that introduced them, to
115 SRG requirements, and to the FortiMail command that configures
them: 84 core platform features, and 247 features from the
"What's new" tables of the FortiMail 7.0.0 through 8.0.2 release notes.
Operational features with no direct requirement fall under the requirement
to disable unnecessary functions when unused.

- [ ] Can find the release that introduced a FortiMail feature.
- [ ] Can map a FortiMail feature to its ALG or NDM SRG requirement.
- [ ] Can find the FortiMail command that meets the requirement.
- [ ] Can decide which ALG requirements apply to an email gateway.
- [ ] Can collect FortiMail evidence and record the requirements FortiMail
  cannot meet exactly.
