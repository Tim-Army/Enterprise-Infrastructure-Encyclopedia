# Chapter 29: FortiSASE Feature, Version, and SRG Map

## Learning Objectives

- Find the FortiSASE release that introduced a given feature, and read
  FortiSASE's year-based release names.
- Explain how the Cloud Computing SRG is built (a Cloud Service Provider
  document and Mission Owner requirements), which identifiers it uses, and
  which of its requirements apply to a software-as-a-service offering such
  as FortiSASE.
- Separate what Fortinet operates in FortiSASE from what the tenant
  configures, and assess only the tenant's part against settings.
- Map each FortiSASE feature to the Cloud Computing (CC), Application Layer
  Gateway (ALG), Virtual Private Network (VPN), or Network Device
  Management (NDM) SRG requirement it helps satisfy.
- Find the FortiSASE portal pane that configures each tenant feature to
  meet its requirement.
- Record the requirements that FortiSASE cannot meet with tenant settings,
  and the mitigations.

## Theory and Architecture

FortiSASE is Fortinet's cloud-delivered secure access service edge (SASE)
service. Fortinet runs the service in its own and public cloud data
centers, called **security points of presence (PoPs)**, and each customer
gets an **instance** that is managed in the FortiSASE portal. The FortiSASE
7.4 Administration Guide describes these ways of connecting users and sites
to the PoPs:

- **FortiClient agent-based mode.** FortiClient on the endpoint, managed by
  the FortiSASE endpoint management service, builds the *FortiSASE Cloud
  Security tunnel* (SSL, or IPsec on newer instances) to the nearest PoP
  for secure internet access (SIA), and custom tunnels to other gateways.
  Endpoint profiles set the connection, protection, ZTNA, and FortiClient
  GUI settings.
- **Proxy agentless mode** (formerly SWG, secure web gateway). Browsers use
  an explicit proxy at the PoP, configured through a PAC file, with no
  agent.
- **Site-based access.** FortiExtender, FortiGate, and FortiAP edge devices
  (and FortiBranchSASE devices) send branch traffic to the PoPs, and
  branch FortiGates and third-party IPsec devices connect through
  **Branch On-ramp** (formerly SD-WAN On-Ramp) tunnels.
- **Secure private access (SPA).** PoPs connect over IPsec to FortiGate
  SD-WAN or SPA hubs in front of private applications. **Agent-based
  ZTNA** sends FortiClient traffic to FortiGate ZTNA application gateways
  using security posture tags, and **agentless ZTNA** publishes private web
  applications in a bookmark portal.
- **Inspection at the PoP.** Internet Access and Private Access policies
  and proxy policies apply security profile groups: SSL inspection,
  AntiVirus, intrusion prevention, File Filter, data loss prevention (DLP),
  Web Filter, DNS Filter, Application Control With Inline-CASB, and Video
  Filter. API-based CASB (FortiCASB) and SaaS security posture management
  (FortiCASB-SSPM) inspect SaaS applications out of band.

The portal is reached through FortiCloud: administrators sign in with the
primary FortiCloud account, as FortiCloud Identity & Access Management
(IAM) users with FortiSASE access (FortiCloud subuser accounts were
discontinued in 24.3.b), or through an external SAML identity provider.
Logs are kept in Fortinet's logging PoPs for a fixed retention period and
can be forwarded to FortiAnalyzer, a syslog or CEF server, FortiAnalyzer
Cloud, or FortiGuard SOCaaS.

**Who is responsible for what.** FortiSASE is software as a service. The
Cloud Computing Mission Owner SRG Overview says that for SaaS the cloud
service provider is responsible for the security of the software service
and the entire security stack, while the Mission Owner (the DoD customer)
remains responsible for its data, identity management, and the
configuration settings within its control (sections 3.1.3 and 3.3.1). For
FortiSASE that divides as follows:

| Fortinet operates (provider responsibility) | The tenant configures (customer responsibility) |
| --- | --- |
| The PoPs, logging PoPs, and endpoint management service, their hosts, operating systems, and network | Policies, proxy policies, and security profile groups |
| The tunnel settings of the Cloud Security tunnel (IKE version, proposals, Diffie-Hellman groups, key lifetimes) | Endpoint profiles: autoconnect, split tunneling, network lockdown, posture checks, timeouts |
| FortiGuard signatures and databases, and the service upgrades in the monthly maintenance window | Authentication sources (SAML SSO, LDAP, RADIUS, FSSO), users, and groups |
| The portal platform and the FortiCloud sign-in | Who may administer the instance (IAM users, external IdP roles), the portal session timeout, and configuration audit logs |
| Log storage and its retention limits | Log forwarding, retention within the allowed range, and anonymization |
| The authorization of the offering (FedRAMP, DoD provisional authorization) | Selecting an authorized offering at the right impact level, AO authorization, and the contract |

This map assigns requirements to tenant settings only. A row for a
Fortinet-operated capability says so in the Feature column, and its
command entry says that there is no tenant setting.

FortiSASE has **no DISA STIG** (Chapter 10). Chapter 10 assigns it the
**Cloud Computing SRG**, and says to confirm the offering's authorization
status and impact level before use, as described in Chapter 08. For every
FortiSASE feature this chapter gives **which FortiSASE release introduced
it**, **which requirement it relates to**, and **which portal pane
configures it to meet that requirement**.

### Where the version data comes from

FortiSASE has no Feature Matrix and no New Features Guide. FortiSASE
releases are named by year and quarter rather than by firmware train: in
2024 and 2025 a quarter's releases are lettered (24.3.b, 25.2.c), with
maintenance releases numbered under them (25.3.a.1), and from 2026 they are
numbered (26.1.1, 26.2.2.a). The 24.x release notes also give the build
number (24.3.42 is 24.3.b). Since 26.2.1 Fortinet calls the two kinds of
instance **FortiSASE v7.4** (formerly *Feature*) and **FortiSASE v7.2**
(formerly *Mature*); instances created after 25.2.c are v7.4 instances,
and v7.2 instances move to v7.4 through a best practice upgrade.

The best available source is the **release notes**, and two documents were
used:

- The **FortiSASE 7.4 Release Notes** (docs.fortinet.com, and the PDF
  with change log through the initial release of 26.3.1.a on 29 September
  2026). Its *What's new* page lists every release from **25.1.a through
  26.3.1.a**: 41 releases, of which 18 are maintenance releases with no new
  features (25.1.a.1, 25.1.a.2, 25.2.a.1, 25.2.b.1, 25.2.b.2, 25.2.c.1,
  25.2.c.2, 25.3.a.1 to 25.3.a.3, 25.3.b.1, 25.3.c.1, 25.4.b.1, 25.4.b.2,
  25.4.c.1, 26.1.2.1.1, 26.2.1.a, and 26.2.2.b). This is the only FortiSASE
  documentation Fortinet still publishes: the 26.3.1.a page says that the
  v7.2 documentation has been removed from the Document Library, and
  links to older versions (24.4.0, 23.1.0, and so on) now redirect to the
  7.4 release notes.
- The **FortiSASE 24.4.87 Release Notes** (PDF, initial release 21 January
  2025), retrieved from the Internet Archive copy of Fortinet's document
  server because Fortinet no longer publishes it. Its *What's new* section
  covers **24.3.b (24.3.42) through 24.4.c (24.4.87)**: 24.3.b, 24.3.c
  (24.3.56), 24.4.a (24.4.32), 24.4.b (24.4.60), 24.4.b.1 (24.4.75), and
  24.4.c. Its *What's new preview for 25.1.a* was not used, because the
  7.4 release notes list 25.1.a itself.

Releases before 24.3.b are not covered: their release notes are no longer
published, and the Internet Archive holds only some of the earlier ones
(there are no 24.2 release notes, for example). The version column was built with these rules:

- Each feature bullet of a *What's new* list is one entry; sub-bullets are
  folded into their entry.
- The same feature is sometimes listed twice, first for new instances and
  in a later release for existing instances (the endpoint vulnerability,
  SPA, and Cloud Security Usage reports in 25.3.c and 25.4.b, and the
  Automation page). Each listing is its own entry, and the map merges them
  into one row with both releases.
- New PoP, data center, and endpoint management locations (20 entries)
  are merged into one row, and so are new recommended or supported
  FortiClient versions and installers (16 entries).
- The 7.4 Administration Guide has a **New features** table of the
  capabilities available only in FortiSASE v7.4 (80 features, enabled by
  default on new instances created after 25.2.c). Twelve of them are not
  listed on any *What's new* page; they are entered as **v7.4 (release not
  listed)**, because Fortinet does not say which release added them.

That gives 248 entries: 40 from the 24.4.87 release notes,
196 from the 7.4 release notes, and 12 from the v7.4 New
features table. Each entry title was taken from the source and shortened
where needed.

The table has two groups of rows:

- **Core platform features** (categories starting with *Core:*) are the
  long-standing capabilities that the requirements depend on: the cloud
  service and its locations, administration through FortiCloud, logging,
  the access modes and edge devices, policies and security profiles,
  remote access and authentication, SPA and ZTNA, and the endpoint
  service. Each one is described in the **FortiSASE 24.4.87 Administration
  Guide** (retrieved from the Internet Archive, like the 24.4.87 release
  notes) and is not on a *What's new* list, so it existed by 24.4.87; the
  build script checks a phrase of each core row against that guide.
- **New features** are the 248 entries, merged into 102
  rows. The categories were assigned for this chapter.

| Version entry | Meaning |
| --- | --- |
| `24.4.87 or earlier` | A core feature described in the FortiSASE 24.4.87 Administration Guide |
| `25.3.a and later` | Introduced in that release (listed on its *What's new* page); later releases include it |
| `24.3.c+; 25.1.b+; 25.3.a+` | Listed in each of those quarters (or, for 2026, in each numbered release series such as 26.1 and 26.2); the first release listed in each is shown |
| `v7.4 (release not listed)` | Listed only in the v7.4 New features table of the 7.4 Administration Guide |
| `25.1.b+; v7.4 New features` | A merged row: one entry from a release, and another listed only in the v7.4 New features table |

Four cautions apply. First, Fortinet upgrades every instance in the
monthly maintenance window, so the tenant does not choose a release; the
version column says when a feature became available in the service.
Second, many features apply only to new instances, to v7.4 instances, to
instances with IPsec remote agent support, or to a minimum FortiClient
version, and *select availability* features (central management, SCIM,
backup and restore, the Secure Browser, and others) must be enabled
through a FortiCare Support ticket. Third, a row records when Fortinet
first listed a feature, which is not always when it first existed: the
FortiPAM agent in the FortiClient installer is listed in 26.2.1, but
FortiPAM integration itself is only in the New features table. Fourth,
panes were checked against the 7.4 Administration Guide; earlier releases
used other names (*Configuration > Profiles* before *Endpoint management >
Configuration*, *SWG* before *Proxy*, *Network > Infrastructure* before
*Operations > Infrastructure*).

### Where the SRG data comes from

The October 2026 DISA library holds the Cloud Computing SRG as
`U_Cloud_Computing_Y26M06_SRG.zip`. It is not one XCCDF checklist. As the
release memo (21 June 2024) explains, the Cloud Computing SRG has two
parts, a **Cloud Service Provider (CSP)** document and a **Mission Owner
(MO)** part made of an overview PDF and STIG-format requirements. The zip
holds:

| File | Kind | What it contains |
| --- | --- | --- |
| Cloud Service Provider SRG, V1R7, 30 June 2026 | PDF document | Requirements for providers who want a DoD provisional authorization: impact levels (section 3.7), the provisional authorization (3.6), authorization boundaries (4.3.1), the customer responsibility matrix (5.1.4), PKI (5.4), data protection, and the SaaS architecture (5.9.3.1). It has numbered sections and CAT definitions, but **no requirement IDs** |
| Cloud Computing Mission Owner SRG Overview, 30 June 2026 | PDF document | The Mission Owner's responsibilities for each service model (section 3.3), choosing the impact level, and contract and SLA requirements |
| Cloud Computing Mission Owner Operating System SRG, V1R3, benchmark date 13 Aug 2025 | XCCDF | 17 requirements for the Mission Owner, with IDs such as `SRG-OS-000480-CLD-000031` |
| Cloud Computing Mission Owner Network SRG, V1R2, benchmark date 30 Jan 2025 | XCCDF | 9 requirements, all written for infrastructure or platform as a service (IaaS/PaaS) |

The two XCCDF files use the naming standard that the Overview describes
(section 1.3), *core SRG value - technology SRG - sequence number*, so
`SRG-OS-000480-CLD-000031` is a requirement built on the Operating System
core SRG for the cloud (`CLD`) technology area; its Group ID (here
V-259885) identifies the same rule in a checklist, as in other SRGs. The
**impact levels** are DoD categories, not FedRAMP ones (CSP SRG 3.7):
Impact Level 2 for public or non-controlled unclassified information,
Impact Level 4 for Controlled Unclassified Information (CUI), Impact Level
5 for CUI that needs more protection and for unclassified National Security
Systems, and Impact Level 6 for classified information up to SECRET. A
**DoD provisional authorization (PA)** is granted to one cloud service
offering, not to the provider, and a SaaS offering needs its own PA even
when it runs on an authorized IaaS (CSP SRG 3.6); the offerings with a PA
are listed in the DoD Cloud Service Catalog.

The SRG column uses these abbreviations:

| SRG column | SRG | Release | Applies to |
| --- | --- | --- | --- |
| **CC** | Cloud Computing Mission Owner Operating System SRG (part of the Cloud Computing SRG) | V1R3, benchmark date 13 Aug 2025 | The customer's decisions about the offering: authorization, impact level, the contract, registration of ports and connections, portal credentials, the logon banner, and DoD PKI (assigned by Chapter 10) |
| **ALG** | Application Layer Gateway SRG | V2R4, benchmark date 01 Jul 2026 | The secure internet access, proxy, inline CASB, DLP, and ZTNA functions of the PoPs, as far as the tenant configures them: policies, security profiles, authentication of users, and log forwarding |
| **VPN** | Virtual Private Network SRG | V3R5, benchmark date 01 Jul 2026 | Remote access through FortiClient tunnels to the PoPs, and the IPsec connections of Branch On-ramp and SPA, as far as the tenant configures them: endpoint profiles, authentication sources, and posture checks |
| **NDM** | Network Device Management SRG | V5R5, benchmark date 01 Jul 2026 | The tenant's administration of the instance in the FortiSASE portal: administrators, sessions, configuration audit logs, certificates, backups, and log forwarding |

Each SRG was chosen for one reason:

- **CC, because Chapter 10 assigns it.** The Cloud Computing SRG is the DoD
  baseline for using a cloud service. Its CSP document addresses Fortinet,
  not the customer, and has no requirement IDs, so it is cited by section.
  The map uses the Mission Owner Operating System requirements that a SaaS
  customer can act on: AO authorization of the offering
  (CC `SRG-OS-000480-CLD-000025`), selecting an offering listed at the
  right impact level (CC `SRG-OS-000480-CLD-000030`, CC
  `SRG-OS-000480-CLD-000031`, CC `SRG-OS-000480-CLD-000032`, and CC
  `SRG-OS-000480-CLD-000033`), compensating controls in the contract
  (CC `SRG-OS-000480-CLD-000035`), registering ports, the IAP allowlist, and
  SNAP (CC `SRG-OS-000096-CLD-000060`, CC `SRG-OS-000370-CLD-000050`, and CC
  `SRG-OS-000368-CLD-000040`), least privilege for portal credentials
  (CC `SRG-OS-000001-CLD-000010`), the logon banner
  (CC `SRG-OS-000023-CLD-000015`), and DoD PKI for organizational users
  (CC `SRG-OS-000104-CLD-000065`). The title of
  CC `SRG-OS-000096-CLD-000060` names IaaS and PaaS, but its fix, and
  section 3.3 of the Overview, tell the Mission Owner to register the ports
  and protocols used by a SaaS offering in the PPSM registry, which is how
  it is used here. The other Mission Owner requirements say in their check
  that they do not apply to SaaS (centralized logging
  CC `SRG-OS-000342-CLD-000020`, removing virtual machines and old software)
  or apply to storage offerings (CC `SRG-OS-000404-CLD-000080`), and the
  nine Mission Owner Network requirements are all written for IaaS and
  PaaS, so none of them is mapped.
- **ALG for the inspection functions.** A PoP is a proxy and application
  gateway for the tenant's traffic, and the ALG SRG, which Chapter 18 used
  for FortiProxy, has the requirements for what the tenant configures there:
  deny by default (ALG `SRG-NET-000202-ALG-000124`), content-based flow
  control and blocking (ALG `SRG-NET-000018-ALG-000017`,
  ALG `SRG-NET-000019-ALG-000018`), malicious code scanning and blocking,
  user authentication, and log off-loading. The ALG requirement to disable
  unnecessary functions (ALG `SRG-NET-000131-ALG-000085`) is used for rows
  about traffic functions with no direct requirement.
- **VPN for remote access.** The Cloud Security tunnel is a remote access
  VPN between FortiClient and the PoP, and the VPN SRG, which Chapters 15
  and 27 used, has the requirements that endpoint profiles address:
  always-on connections (VPN `SRG-NET-000230-VPN-002436`), no split
  tunneling (VPN `SRG-NET-000369-VPN-001620`), a separate authentication
  server and multifactor authentication, endpoint identification and
  authentication, and session time limits. Its cryptographic requirements
  are met or not met by Fortinet's fixed tunnel settings, which the tenant
  cannot change.
- **NDM for portal administration.** The FortiSASE portal is the tenant's
  management interface, so the NDM SRG covers who may administer the
  instance, the session timeout, configuration audit logs, certificates,
  and backups. Much of an administrator's identity (password, lockout, and
  multifactor authentication) is managed in FortiCloud, not in FortiSASE.
  The NDM requirement to disable unnecessary functions
  (NDM `SRG-APP-000142-NDM-000245`) is used for portal, licensing,
  reporting, and endpoint rows with no direct requirement.

Two SRGs were considered and not used. The Intrusion Detection and
Prevention Systems SRG fits an inline sensor; the PoP's intrusion
prevention profile is a content filtering function of the gateway and is
mapped to the ALG SRG. The Unified Endpoint Management SRGs fit the
FortiClient agent and its management service, which Chapter 27 maps for
FortiClient and EMS; the endpoint protection settings of FortiSASE
endpoint profiles are assessed with that chapter and the endpoint's
operating system STIG, and appear here as rows with no direct requirement.

The requirement IDs are the **rule version IDs** from the XCCDF files,
and the severity is the rule's severity (high = CAT I, medium = CAT II,
low = CAT III). Each feature maps to one of three kinds of relationship:

- **Implements a requirement.** The feature is how the tenant meets a
  requirement. Endpoint quarantine implements the requirement to
  immediately disconnect a remote endpoint (VPN `SRG-NET-000314-VPN-001060`),
  and configuration audit logs implement the requirement to audit
  privileged functions (NDM `SRG-APP-000343-NDM-000289`), for example.
- **Must be configured to meet a requirement.** The feature is in scope
  of a requirement and has to be set up correctly. The default Allow-All
  policy must be replaced by specific policies to deny by default
  (ALG `SRG-NET-000202-ALG-000124`), and the offering must be listed at the
  impact level of the data (CC `SRG-OS-000480-CLD-000031`), for example.
- **No direct requirement.** The feature is operational, such as a
  dashboard, a report, a license, a location, a GUI change, or a routing
  option. If it is not needed it falls under the requirement to disable
  unnecessary functions: ALG `SRG-NET-000131-ALG-000085` for traffic
  functions (21 rows) and NDM `SRG-APP-000142-NDM-000245` for
  portal, licensing, reporting, and endpoint functions (28 rows),
  49 rows in all.

The mapping is a starting point for an assessment, not a ruling. Confirm
it with your assessor, especially the use of the ALG, VPN, and NDM SRGs
for a cloud service whose platform the customer cannot see.

### Where the commands come from

FortiSASE is configured in the FortiSASE portal and has no command line
for the tenant. The command column was therefore built from the
**FortiSASE 7.4 Administration Guide** (PDF, 922 pages, change log through
9 October 2026), the newest guide, and its *Appendix B - REST API* for the
API. The check was automatic: each GUI pane had to appear in the guide's
text or be a heading path of its outline (chapter, section, and
subsection), each field label in parentheses had to appear in the guide,
and each literal value had to appear in the guide, be a number, or be on or
off. All 135 GUI panes and 55 field labels passed. Read the column this
way:

- **GUI:** entries name the portal pane (*menu > page > section or tab*);
  the text in parentheses names the fields to set, with the value where it
  matters. A last level such as *Endpoint management > Configuration >
  Connection* is a tab of the endpoint profile, and *Endpoint management >
  Configuration > Global* is the Global page of that menu.
- Statements in plain text are actions outside the portal (in FortiCloud,
  the contract, or a support ticket) or notes on how to set a field.
- **"(Fortinet-operated; no tenant setting)"** marks a capability that the
  tenant cannot configure. It is assessed through the offering's
  authorization package, not through tenant settings.
- For **"No direct requirement"** rows, the entry shown is where the
  feature is turned off or left unconfigured when it is unused. A dash
  (**—**) means there is nothing to change: the feature is a GUI change, a
  license, a location, a report, or a capability that does nothing until it
  is configured or licensed.

Some requirements cannot be met with FortiSASE tenant settings. Record
them on the checklist as open findings with mitigations, or meet them
another way:

- **Authorization and impact level.** Neither the 7.4 Administration Guide
  nor the release notes name a FedRAMP authorization, a DoD provisional
  authorization, or an impact level for FortiSASE; Appendix F of the guide
  refers readers to the Fortinet Trust Resource Center. Check the DoD Cloud
  Service Catalog and the FedRAMP Marketplace for the offering before use
  (CC `SRG-OS-000480-CLD-000025`). Without a listing at the impact level
  of the data, the offering cannot be used for that data
  (CC `SRG-OS-000480-CLD-000031` and CC `SRG-OS-000480-CLD-000032` are
  CAT I). Put the compensating controls of this list in the contract
  (CC `SRG-OS-000480-CLD-000035`).
- **Logon banners.** The guide documents no logon banner for the portal,
  which administrators reach through FortiCloud (CC
  `SRG-OS-000023-CLD-000015`, NDM `SRG-APP-000068-NDM-000215`), and no
  banner for FortiClient tunnels (VPN `SRG-NET-000041-VPN-000110`). For
  edge device users, the Captive Portal Login Page template can show the
  notice, but the *Captive Portal Disclaimer* template is not supported,
  so the banner cannot be kept until the user accepts it
  (ALG `SRG-NET-000042-ALG-000023`). Log administrators and users on
  through a SAML identity provider that displays the DoD notice and consent
  banner, and record the finding.
- **Administrator authentication.** Administrators sign in through
  FortiCloud, and the guide documents no FortiSASE settings for their
  password length and complexity, lockout, or multifactor authentication
  (NDM `SRG-APP-000164-NDM-000252`, NDM `SRG-APP-000065-NDM-000214`, NDM
  `SRG-APP-000149-NDM-000247`, CAT I). Use IAM users or external IdP
  administrators who authenticate with DoD PKI through the IdP (CC
  `SRG-OS-000104-CLD-000065`), keep the primary FortiCloud account as the
  account of last resort with the strongest authentication FortiCloud
  offers, and record how FortiCloud enforces the rest.
- **Portal session timeout.** The session timeout (26.3.1) is a total
  session length from sign-in (5 to 480 minutes, 30 by default), not an
  idle timer, applies to the whole instance, and does not apply to MSSP IAM
  users (NDM `SRG-APP-000190-NDM-000267`, CAT I). Set it to 5 minutes if
  administrators can work with frequent sign-ins, otherwise to the shortest
  workable value, and record the difference; before 26.3.1 there is no
  setting.
- **Tunnel cryptography.** Fortinet fixes the tunnel settings. The PoPs
  and the settings FortiClient receives use IKEv2 with Phase 1 proposals
  that include AES128 and SHA256 and Diffie-Hellman groups 5 and 15, and
  Phase 2 proposals that include SHA1 and AES128 with DH group 15 for
  perfect forward secrecy; custom and failover gateways must use the same
  settings with DH group 15. The VPN SRG requires DH
  group 16 or higher (VPN `SRG-NET-000074-VPN-000250`), SHA-384 for IKE
  (VPN `SRG-NET-000230-VPN-000780`), and AES256 for IPsec
  (VPN `SRG-NET-000525-VPN-002330`), all CAT I, and SHA-2 at 384 bits for
  IPsec integrity (VPN `SRG-NET-000063-VPN-000220`). The guide does not
  document the TLS versions of the SSL tunnel
  (VPN `SRG-NET-000062-VPN-000200`). The tenant cannot change these; ask
  Fortinet, and record them as findings against the offering.
- **FIPS-validated cryptography.** The guides document no FIPS 140
  validation for the PoPs, tunnels, portal, or FortiClient's tunnel
  (VPN `SRG-NET-000510-VPN-002170`, ALG `SRG-NET-000510-ALG-000111`,
  NDM `SRG-APP-000179-NDM-000265`), while CSP SRG section 5.9.3.1 expects
  FIPS 140-2 or 140-3 validated modules for customer data in transit and at
  rest. Ask Fortinet for the validation status, and record the finding.
- **Certificate revocation and CAC.** The guide documents no OCSP or CRL
  checking for PKI users or imported certificates
  (VPN `SRG-NET-000580-VPN-002431`, ALG `SRG-NET-000345-ALG-000099`), and
  no direct CAC authentication of users. Authenticate users through a SAML
  identity provider that accepts and validates the CAC
  (VPN `SRG-NET-000341-VPN-001350`, VPN `SRG-NET-000140-VPN-000500`).
- **Disconnecting a user.** The Connected users page documents no
  disconnect action. Manual endpoint quarantine (26.3.1) blocks a managed
  endpoint's network access (VPN `SRG-NET-000314-VPN-001060`); before that,
  or for proxy users, remove the user from the groups the policies allow.
- **Log storage.** Logs are kept by Fortinet for 2 to 7 days on instances
  provisioned after 25.3.a (2 to 30 days before), administrator event logs
  appear after a delay, and the guide documents no customer-managed
  encryption keys for stored logs. Forward all logs in real time to a log
  server in your boundary over TLS (ALG `SRG-NET-000511-ALG-000051`, NDM
  `SRG-APP-000516-NDM-000350`). Log anonymization replaces user names, which
  conflicts with identifying the user in each record
  (ALG `SRG-NET-000079-ALG-000048`); leave it off unless the privacy officer
  requires it. Once enabled, SOCaaS log forwarding can be turned off only
  through a FortiCare ticket.
- **Backups.** Backup and restore of selected configuration settings is a
  select availability feature (26.3.1) that keeps up to 10 backups; there
  is no other tenant backup (NDM `SRG-APP-000516-NDM-000340`). Enable it
  through FortiCare, or keep the configuration in FortiManager through
  central management, and record the settings it does not cover.
- **Settings the guide does not name.** The 25.1.a personal VPN setting is
  not described in the 7.4 guide; check the endpoint profile, keep users
  from adding personal VPN connections (VPN `SRG-NET-000132-VPN-000450`),
  and record what you find.
- **No STIG.** Without a STIG there is no DoD baseline for FortiSASE; use
  this map, the Cloud Computing SRG, and the ALG, VPN, and NDM SRGs as the
  baseline, and record the settings that differ from it.

## Design Considerations

- **Decide authorization first.** Confirm the offering's DoD provisional
  authorization and impact level, obtain the AO's authorization, register
  the connection, ports, and egress addresses (SNAP, PPSM, the DoD
  DMZ/IAP allowlist), and put Fortinet's responsibilities and the open
  findings of this map in the contract before any design work.
- **Choose PoP locations deliberately.** PoP and logging locations decide
  where traffic is inspected and logs are kept. Select only approved
  locations at provisioning, and review every location change, migration
  best practice, and geofencing rule.
- **Deny by default.** Replace the default Allow-All policies with
  policies for approved users, destinations, and services, apply a
  security profile group with deep inspection, AntiVirus, intrusion
  prevention, and Web Filter to every Accept policy, and log all sessions.
- **Keep users in the tunnel.** Set endpoint profiles to connect
  automatically, hide the disconnect option, enable network lockdown when
  off-net, and leave steering bypass destinations and local LAN access
  empty unless the AO approves split tunneling.
- **Authenticate through an identity provider.** Use SAML SSO with an IdP
  that enforces CAC for users and administrators, use LDAP or RADIUS only
  as a separate authentication server, keep local users to the minimum,
  and set the authentication and idle timeouts.
- **Move to IPsec, but record the cryptography.** IPsec remote agent
  support is the direction of the service (SSL tunnels are to be migrated
  in 2027), but its fixed proposals do not meet the VPN SRG; record that
  as a provider finding.
- **Send logs out.** Forward traffic, security, and event logs in real
  time to FortiAnalyzer or a syslog server over TLS, and alert the ISSO on
  detections there.
- **Turn off what is not used.** Leave proxy mode, agentless ZTNA, RBI,
  edge devices, Branch On-ramp, the Secure Browser, and API-based CASB
  disabled unless they are needed, and remove unused custom tunnels,
  access keys, and FortiManager keys.

## Implementation and Automation

### The FortiSASE feature map

The SRG column uses the abbreviations defined in *Where the SRG data comes
from*: **CC** is the Cloud Computing Mission Owner Operating System SRG,
**ALG** the Application Layer Gateway SRG, **VPN** the Virtual Private
Network SRG, and **NDM** the Network Device Management SRG. The requirement
titles are listed in the next table. The command column follows the
conventions in *Where the commands come from*.

[Download the feature map as CSV](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/data/volume-172-disa-srgs-and-stigs/29-fortisase-feature-version-and-srg-map-feature-map.csv) (168 rows).

| Category | Feature | Introduced (FortiSASE) | SRG requirement(s) | Command to satisfy the requirement |
| --- | --- | --- | --- | --- |
| Core: Cloud service | FortiSASE cloud service offering: security PoPs, logging PoPs, and the endpoint management service (Fortinet-operated) | 24.4.87 or earlier | CC `SRG-OS-000480-CLD-000025`; CC `SRG-OS-000480-CLD-000035` | Confirm the offering's DoD provisional authorization and impact level, obtain AO authorization, and record Fortinet's responsibilities in the contract (Fortinet-operated; no tenant setting) |
| Core: Cloud service | Impact level of the information processed (DoD Cloud Service Catalog listing at that level) | 24.4.87 or earlier | CC `SRG-OS-000480-CLD-000030`; CC `SRG-OS-000480-CLD-000031`; CC `SRG-OS-000480-CLD-000032`; CC `SRG-OS-000480-CLD-000033` | Select an offering listed at the impact level of the data; FortiSASE has no setting for this |
| Core: Cloud service | Security PoP locations selected at provisioning (where traffic is inspected and logs are kept) | 24.4.87 or earlier | CC `SRG-OS-000480-CLD-000035` | GUI: Operations > Infrastructure (choose only locations the authorizing official approves) |
| Core: Cloud service | Required services and ports, and the egress IP addresses feed | 24.4.87 or earlier | CC `SRG-OS-000096-CLD-000060`; CC `SRG-OS-000370-CLD-000050`; CC `SRG-OS-000368-CLD-000040` | Register the ports, egress addresses, and connection method in PPSM, the DoD DMZ/IAP allowlist, and SNAP (see Required services and ports and Egress IP addresses feed) |
| Core: Cloud service | Monthly maintenance and service upgrades (Fortinet-operated) | 24.4.87 or earlier | NDM `SRG-APP-000457-NDM-000352`; NDM `SRG-APP-001035-NDM-000340` | Fortinet upgrades the service in the monthly maintenance window; subscribe to status notifications and review each release |
| Core: Cloud service | FortiGuard signature and database updates for the security profiles (Fortinet-operated) | 24.4.87 or earlier | ALG `SRG-NET-000019-ALG-000019`; ALG `SRG-NET-000246-ALG-000132`; ALG `SRG-NET-000251-ALG-000131` | — (Fortinet-operated; no tenant setting) |
| Core: Cloud service | System status notifications from the FortiSASE status page | 24.4.87 or earlier | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | GUI: Monitoring > Dashboards > Status (Subscribe) |
| Core: Cloud service | Subscriptions and licenses (Standard, Advanced, Comprehensive, and add-ons) | 24.4.87 or earlier | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Core: Administration | Portal sign-in with the primary FortiCloud account | 24.4.87 or earlier | CC `SRG-OS-000001-CLD-000010`; NDM `SRG-APP-000148-NDM-000346` | Keep the primary FortiCloud account as the account of last resort; it is required for software audit and version settings |
| Core: Administration | Administrators as FortiCloud Identity & Access Management (IAM) users with FortiSASE access | 24.4.87 or earlier | CC `SRG-OS-000001-CLD-000010`; NDM `SRG-APP-000033-NDM-000212`; NDM `SRG-APP-000153-NDM-000249` | Create an IAM user for each administrator and add FortiSASE to the services the user can access (see Signing in as an IAM user) |
| Core: Administration | External IdP administrators (SAML IdP roles for cloud products) | 24.4.87 or earlier | CC `SRG-OS-000104-CLD-000065`; NDM `SRG-APP-000149-NDM-000247`; NDM `SRG-APP-000516-NDM-000336` | Log administrators on through an external SAML IdP that enforces CAC (see Supporting external IdP users) |
| Core: Administration | MSSP portal with resource-based permissions | 24.4.87 or earlier | NDM `SRG-APP-000329-NDM-000287`; NDM `SRG-APP-000033-NDM-000212` | Grant MSSP administrators only the tenants and resources they manage (MSSP portal, Resource-based permissions) |
| Core: Administration | Administrator Events log (logins, MSSP portal access, and configuration changes) | 24.4.87 or earlier | NDM `SRG-APP-000503-NDM-000320`; NDM `SRG-APP-000343-NDM-000289`; NDM `SRG-APP-000100-NDM-000230` | GUI: Operations > Logs > Events (Administrator Events) |
| Core: Administration | Certificates for SSL deep inspection, SAML SSO, and LDAPS (local and remote CA certificates) | 24.4.87 or earlier | NDM `SRG-APP-000910-NDM-000300`; ALG `SRG-NET-000750-ALG-000140` | GUI: System > Certificates (import only DoD-approved CA certificates) |
| Core: Administration | HTML templates for block pages, captive portal pages, and the invitation email | 24.4.87 or earlier | ALG `SRG-NET-000041-ALG-000022` | GUI: System > HTML templates (Captive Portal Login Page) (add the DoD notice and consent text) |
| Core: Administration | REST API (Appendix B) | 24.4.87 or earlier | NDM `SRG-APP-000033-NDM-000212` | Give API users only the permissions they need (see Appendix B - REST API) |
| Core: Logging | Traffic, security, and event logs in the portal | 24.4.87 or earlier | ALG `SRG-NET-000074-ALG-000043`; ALG `SRG-NET-000077-ALG-000046`; ALG `SRG-NET-000079-ALG-000048`; VPN `SRG-NET-000492-VPN-001980` | GUI: Operations > Logs > Traffic; GUI: Operations > Logs > Events |
| Core: Logging | Policy logging of allowed traffic | 24.4.87 or earlier | ALG `SRG-NET-000074-ALG-000043`; ALG `SRG-NET-000503-ALG-000038` | GUI: Security > Traffic > Policies (Log Allowed Traffic: All Sessions) |
| Core: Logging | Log forwarding to an external server (FortiAnalyzer, Syslog, or CEF) | 24.4.87 or earlier | ALG `SRG-NET-000334-ALG-000050`; ALG `SRG-NET-000511-ALG-000051`; NDM `SRG-APP-000515-NDM-000325`; NDM `SRG-APP-000516-NDM-000350`; VPN `SRG-NET-000334-VPN-001260` | GUI: Operations > Logs > Settings (Log Forwarding to Self-Managed Service, Reliable connection, Secure Connection, Forwarding frequency: Real Time) |
| Core: Logging | Log forwarding to SOCaaS | 24.4.87 or earlier | ALG `SRG-NET-000383-ALG-000135` | GUI: Operations > Logs > Settings (Log Forwarding to SOCaaS 24x7 managed security event monitoring) |
| Core: Logging | Log retention policy | 24.4.87 or earlier | NDM `SRG-APP-000515-NDM-000325` | GUI: Operations > Logs > Settings (Log Retention (days)) (keep the long-term copy on the external server) |
| Core: Logging | Log anonymization | 24.4.87 or earlier | ALG `SRG-NET-000079-ALG-000048`; NDM `SRG-APP-000100-NDM-000230` | GUI: Operations > Logs > Settings (leave Anonymization disabled unless the privacy officer requires it) |
| Core: Logging | Dashboards and FortiView monitors | 24.4.87 or earlier | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Core: Logging | Reports (scheduled and on demand) | 24.4.87 or earlier | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Core: Secure internet access | FortiClient agent-based mode (SIA for remote users through the Cloud Security tunnel) | 24.4.87 or earlier | VPN `SRG-NET-000371-VPN-001650`; ALG `SRG-NET-000313-ALG-000010` | GUI: Endpoint management > Configuration > Connection |
| Core: Secure internet access | Agentless proxy mode (formerly SWG) with PAC files | 24.4.87 or earlier | ALG `SRG-NET-000018-ALG-000017`; ALG `SRG-NET-000131-ALG-000086` | GUI: Network > Proxy configuration (disable proxy if unused) |
| Core: Secure internet access | FortiExtender edge devices (site-based SIA and LAN extension) | 24.4.87 or earlier | ALG `SRG-NET-000018-ALG-000017` | GUI: Operations > Connectivity > Edge devices > FortiExtenders |
| Core: Secure internet access | FortiGate edge devices (LAN extension) | 24.4.87 or earlier | ALG `SRG-NET-000018-ALG-000017` | GUI: Operations > Connectivity > Edge devices > FortiGates |
| Core: Secure internet access | FortiAP edge devices and SSIDs (site-based SIA) | 24.4.87 or earlier | ALG `SRG-NET-000018-ALG-000017` | GUI: Operations > Connectivity > Edge devices > FortiAPs |
| Core: Secure internet access | Captive portal for edge device users | 24.4.87 or earlier | ALG `SRG-NET-000138-ALG-000063`; ALG `SRG-NET-000041-ALG-000022` | GUI: Security > Traffic > Policies (do not set Captive Portal Exempt except for documented devices) |
| Core: Secure internet access | SD-WAN On-Ramp (Branch On-ramp) IPsec connections from branch FortiGate devices | 24.4.87 or earlier | VPN `SRG-NET-000512-VPN-002220`; ALG `SRG-NET-000018-ALG-000017` | GUI: Operations > Connectivity > On-ramp tunnel |
| Core: Secure internet access | Internet Access and Private Access policies (default Allow-All and Implicit Deny) | 24.4.87 or earlier | ALG `SRG-NET-000202-ALG-000124`; ALG `SRG-NET-000018-ALG-000017`; VPN `SRG-NET-000019-VPN-000040`; VPN `SRG-NET-000015-VPN-000010` | GUI: Security > Traffic > Policies (replace the Allow-All policy with policies for approved users, destinations, and services) |
| Core: Secure internet access | Proxy policies for agentless proxy users | 24.4.87 or earlier | ALG `SRG-NET-000202-ALG-000124`; ALG `SRG-NET-000018-ALG-000017` | GUI: Security > Traffic > Proxy policies |
| Core: Secure internet access | Security profile groups | 24.4.87 or earlier | ALG `SRG-NET-000019-ALG-000018` | GUI: Security > Traffic > Security profiles (apply a profile group to every Accept policy) |
| Core: Secure internet access | SSL inspection (certificate and deep inspection) | 24.4.87 or earlier | ALG `SRG-NET-000019-ALG-000018`; ALG `SRG-NET-000164-ALG-000100`; ALG `SRG-NET-000062-ALG-000150` | GUI: Security > Traffic > Security profiles (Deep Inspection) |
| Core: Secure internet access | AntiVirus profile | 24.4.87 or earlier | ALG `SRG-NET-000248-ALG-000133`; ALG `SRG-NET-000249-ALG-000134`; ALG `SRG-NET-000249-ALG-000145`; ALG `SRG-NET-000765-ALG-000170` | GUI: Security > Traffic > Security profiles (enable AntiVirus in the profile group) |
| Core: Secure internet access | Intrusion prevention profile | 24.4.87 or earlier | ALG `SRG-NET-000390-ALG-000139`; ALG `SRG-NET-000391-ALG-000140`; ALG `SRG-NET-000318-ALG-000151` | GUI: Security > Traffic > Security profiles (enable Intrusion prevention in the profile group) |
| Core: Secure internet access | File Filter profile | 24.4.87 or earlier | ALG `SRG-NET-000289-ALG-000110`; ALG `SRG-NET-000018-ALG-000017` | GUI: Security > Traffic > Security profiles (enable File Filter in the profile group) |
| Core: Secure internet access | Data loss prevention (DLP) profile | 24.4.87 or earlier | ALG `SRG-NET-000018-ALG-000017` | GUI: Security > Traffic > Security profiles (enable DLP in the profile group) |
| Core: Secure internet access | Web Filter profile with FortiGuard categories | 24.4.87 or earlier | ALG `SRG-NET-000019-ALG-000018`; ALG `SRG-NET-000288-ALG-000109` | GUI: Security > Traffic > Security profiles (enable Web Filter in the profile group) |
| Core: Secure internet access | DNS Filter profile | 24.4.87 or earlier | ALG `SRG-NET-000019-ALG-000018` | GUI: Security > Traffic > Security profiles (enable DNS Filter in the profile group) |
| Core: Secure internet access | Application Control With Inline-CASB | 24.4.87 or earlier | ALG `SRG-NET-000384-ALG-000136`; ALG `SRG-NET-000385-ALG-000137`; ALG `SRG-NET-000132-ALG-000087` | GUI: Security > Traffic > Security profiles (enable Application Control With Inline-CASB in the profile group) |
| Core: Secure internet access | External feeds (threat feeds) for Web Filter, DNS Filter, and policies | 24.4.87 or earlier | ALG `SRG-NET-000019-ALG-000018` | GUI: Security > External feeds |
| Core: Secure internet access | DNS settings and split DNS rules | 24.4.87 or earlier | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | GUI: Network > DNS |
| Core: Secure internet access | Geofencing (regional access and connection priority by country or region) | 24.4.87 or earlier | ALG `SRG-NET-000364-ALG-000122` | GUI: Network > Geofencing |
| Core: Secure internet access | Dedicated public IP addresses and source IP anchoring | 24.4.87 or earlier | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | GUI: Network > IP management |
| Core: Remote access | FortiSASE Cloud Security tunnel (SSL or IPsec) and its tunnel settings (Fortinet-operated) | 24.4.87 or earlier | VPN `SRG-NET-000371-VPN-001650`; VPN `SRG-NET-000062-VPN-000200`; VPN `SRG-NET-000512-VPN-002220` | — (Fortinet-operated; tunnel settings are fixed; see Tunnel settings) |
| Core: Remote access | Autoconnect to the Cloud Security tunnel, without a disconnect option | 24.4.87 or earlier | VPN `SRG-NET-000230-VPN-002436`; ALG `SRG-NET-000313-ALG-000010` | GUI: Endpoint management > Configuration > Connection (Endpoint connects to FortiSASE Cloud Security: Automatically, Show option to disconnect from security PoP: off) |
| Core: Remote access | Split tunneling (steering bypass destinations) | 24.4.87 or earlier | VPN `SRG-NET-000369-VPN-001620` | GUI: Endpoint management > Configuration > Connection (Steering bypass destinations) (leave empty unless the AO approves split tunneling) |
| Core: Remote access | Custom tunnels and on-premise gateways in endpoint profiles | 24.4.87 or earlier | VPN `SRG-NET-000132-VPN-000460`; VPN `SRG-NET-000132-VPN-000450` | GUI: Endpoint management > Configuration > Connection (Custom tunnels; remove unused tunnels) |
| Core: Remote access | Local users and user groups (invitation by email) | 24.4.87 or earlier | VPN `SRG-NET-000138-VPN-000490`; ALG `SRG-NET-000138-ALG-000063`; NDM `SRG-APP-000148-NDM-000346` | GUI: Access & authentication > Access > Users and groups (prefer SSO, LDAP, or RADIUS users to local users) |
| Core: Remote access | LDAP authentication source | 24.4.87 or earlier | VPN `SRG-NET-000166-VPN-000580`; ALG `SRG-NET-000138-ALG-000088` | GUI: Access & authentication > Authentication Sources > LDAP |
| Core: Remote access | RADIUS authentication source | 24.4.87 or earlier | VPN `SRG-NET-000166-VPN-000580`; VPN `SRG-NET-000140-VPN-000500` | GUI: Access & authentication > Authentication Sources > RADIUS |
| Core: Remote access | SAML SSO for agents and proxy users (Entra ID, AD FS, Okta, FortiAuthenticator) | 24.4.87 or earlier | VPN `SRG-NET-000140-VPN-000500`; VPN `SRG-NET-000341-VPN-001350`; ALG `SRG-NET-000140-ALG-000094`; CC `SRG-OS-000104-CLD-000065` | GUI: Access & authentication > Authentication Sources > SSO (use an IdP that enforces CAC) |
| Core: Remote access | PKI users for SPA service connections | 24.4.87 or earlier | VPN `SRG-NET-000166-VPN-000590`; VPN `SRG-NET-000164-VPN-000560` | GUI: Access & authentication > Access > PKI (Subject, CA) |
| Core: Remote access | Connected Users monitor | 24.4.87 or earlier | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | GUI: Operations > Connectivity > Connected users |
| Core: Secure private access | Secure private access (SPA) service connections to FortiGate SD-WAN hubs and SPA hubs | 24.4.87 or earlier | VPN `SRG-NET-000371-VPN-001650`; VPN `SRG-NET-000132-VPN-000460` | GUI: Operations > Connectivity > Secure private access (configure the hub side to the FortiGate STIG) |
| Core: Secure private access | Agent-based ZTNA with ZTNA tags and access proxies (FortiGate application gateways) | 24.4.87 or earlier | ALG `SRG-NET-000015-ALG-000016`; VPN `SRG-NET-000148-VPN-000540`; VPN `SRG-NET-000343-VPN-001370` | GUI: Security > Traffic > ZTNA > Agent-based |
| Core: Endpoint | FortiClient endpoint onboarding with invitation codes | 24.4.87 or earlier | VPN `SRG-NET-000148-VPN-000540` | GUI: Endpoint management > Configuration > Invitation codes |
| Core: Endpoint | Endpoint profiles and profile assignment (groups and AD users) | 24.4.87 or earlier | VPN `SRG-NET-000148-VPN-000540` | GUI: Endpoint management > Configuration > Groups & AD Users |
| Core: Endpoint | Endpoint protection settings (malware protection, vulnerability scan, and removable media) assessed with FortiClient (Chapter 27) | 24.4.87 or earlier | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | GUI: Endpoint management > Configuration > Protection |
| Core: Endpoint | FortiSASE Sandbox for endpoints | 24.4.87 or earlier | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | GUI: Endpoint management > Configuration > Sandbox (Sandbox mode) |
| Core: Endpoint | ZTNA tagging rules (security posture tags) | 24.4.87 or earlier | VPN `SRG-NET-000148-VPN-000540`; VPN `SRG-NET-000343-VPN-001370` | GUI: Endpoint management > Security posture tags |
| Core: Endpoint | Managed endpoints list and FortiClient diagnostic logs | 24.4.87 or earlier | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | GUI: Operations > Connectivity > Endpoints |
| Core: Endpoint | Enterprise mobility management (Intune and Jamf deployment of FortiClient) | 24.4.87 or earlier | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Core: Endpoint | Digital experience monitoring (DEM) | 24.4.87 or earlier | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Central management | Central management using FortiManager (select availability): objects, security profiles, users, authentication sources, threat feeds, service groups, policy packages, schedules, and SSO settings | 24.3.b+; 24.4.c+; 25.1.a+; 25.3.b+; 26.1.2+ | NDM `SRG-APP-000380-NDM-000304`; NDM `SRG-APP-000153-NDM-000249` | GUI: System > Central management (if used, restrict the FortiManager administrators and ADOM that manage FortiSASE; check Operations > Logs > Central management synchronizations) |
| Authentication | Fortinet single sign-on: FortiClient SSO mobility agent to FortiAuthenticator, multiple FortiAuthenticator addresses, and the FSSO collector agent | 24.3.b+; 26.3.1+; v7.4 New features | ALG `SRG-NET-000138-ALG-000088`; ALG `SRG-NET-000138-ALG-000063` | GUI: Endpoint management > Configuration > FSSO; GUI: Access & authentication > Authentication Sources > Fortinet Single Sign On (FSSO) |
| Network | Remote user identification by default on new instances (unique address ranges per PoP, no source NAT to SPA hubs) | 24.3.b and later | ALG `SRG-NET-000077-ALG-000046`; ALG `SRG-NET-000079-ALG-000048` | GUI: Network > IP management > IPAM |
| Edge devices | Edge device support: more FortiAP F, G, and K models, 6 GHz and LAN port profiles, and higher FortiExtender and FortiAP limits | 24.3.b+; 24.4.c+; 25.1.b+; v7.4 New features | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | GUI: Operations > Connectivity > Edge devices > FortiAPs |
| Portal | Portal GUI changes: themes, reorganized navigation, PoP map, URL without UI version, French and Japanese, and PoP icons, names, and region IDs | 24.3.b+; 25.2.c+; 25.3.b+; 25.4.b+; 26.2.1+; 26.3.1+ | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Licensing | Licensing: renewal notifications, License overview page, location add-on licenses, FortiFlex entitlements, SASE and SD-WAN bundles, Global Region and Global PoP add-ons, and FortiCASB data protection add-ons | 24.3.b+; 24.4.c+; 25.2.a+; 26.1.1+; 26.3.1+ | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Secure private access | SPA scale and routing: 12 service connections, easy configuration key, BGP MED, hub priority advertisement, eBGP with multiple AS, and external feeds and FSSO with BGP on loopback | 24.3.b+; 24.4.b+; 25.1.c+; 25.3.a+; 26.1.2.2+; v7.4 New features | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | GUI: Network > BGP |
| Endpoint | Endpoint upgrade: recommended FortiClient version notices, scheduled rollout per endpoint profile, deferred installation, and upgrade rules disabled for each new version | 24.3.b+; 25.4.b+; 26.2.2.a+ | NDM `SRG-APP-001035-NDM-000340` | GUI: Endpoint management > Endpoint upgrade (re-enable the upgrade rules after each new recommended version) |
| Locations | New Fortinet Cloud and Public Cloud security PoP, data center, and endpoint management locations | 24.3.b+; 24.4.c+; 25.1.c+; 25.3.a+; 25.4.a+; 26.1.1+; 26.2.1+; 26.3.1+ | CC `SRG-OS-000480-CLD-000035` | GUI: Operations > Infrastructure (add only locations the authorizing official approves) |
| Agentless ZTNA | Agentless ZTNA to private web applications for contractors and temporary workers | 24.3.c and later | ALG `SRG-NET-000015-ALG-000016`; ALG `SRG-NET-000169-ALG-000102` | GUI: Security > Traffic > ZTNA > Agentless (disable if unused) |
| Agentless ZTNA | Agentless ZTNA bookmark portal with per-user bookmark policies (up to 200 applications per policy) | 24.3.c+; 25.1.b+; 25.2.a+ | ALG `SRG-NET-000015-ALG-000016` | GUI: Security > Traffic > ZTNA > Agentless |
| Policies | Geography-based access: agentless ZTNA by geography, and geography addresses as policy source | 24.3.c+; 25.4.c+ | ALG `SRG-NET-000364-ALG-000122` | GUI: Network > Geofencing; GUI: Security > Traffic > Policies |
| Remote browser isolation | Remote browser isolation (beta in 24.3.c, limited categories in 25.2.c, tenant-based yearly data limit in 25.3.a, select availability in 26.1.2.1) | 24.3.c+; 25.2.c+; 25.3.a+; 26.1.2.1+ | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | GUI: System > Remote Browser Isolation (Enable: off) |
| Geofencing | Geofencing for regional compliance: PoP or on-premise device per country or region, with priority and failover | 24.3.c+; 25.1.b+ | CC `SRG-OS-000480-CLD-000035` | GUI: Network > Geofencing |
| Digital experience | DEM trials, TCP latency (beta), traceroute path diagram, and SaaS monitoring enhancements | 24.3.c+; 25.1.b+; 25.3.a+; 26.1.1+ | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Security profiles | Video filter profiles | 24.3.c and later | ALG `SRG-NET-000019-ALG-000018` | GUI: Security > Traffic > Security profiles (Video Filter) |
| Monitoring | Connected Users and endpoint details: group membership, tunnel IP address, agent session, and last seen time | 24.3.c+; 25.1.c+ | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Remote access | Authentication timeout and idle timeout for agent-based remote users (120 to 172800 seconds from 26.3.1) | 24.3.c+; 26.3.1+ | VPN `SRG-NET-000213-VPN-000721`; ALG `SRG-NET-000337-ALG-000096` | GUI: Endpoint management > Configuration > Global (Authentication timeout, Idle timeout) |
| Network | IP address management: IP pools and excluded subnets, edge device ranges per PoP, IPAM usage chart, and a custom management subnet | 24.4.a+; 25.3.b+; 26.1.1+ | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Edge devices | Wi-Fi client monitoring for FortiAP edge devices | 24.4.a and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Secure private access | SPA monitoring: SLA thresholds per PoP, application monitoring, and hub monitoring | 24.4.a+; 25.3.a+; v7.4 New features | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Security profiles | Application control network protocol enforcement | 24.4.a and later | ALG `SRG-NET-000132-ALG-000087`; ALG `SRG-NET-000384-ALG-000136` | GUI: Security > Traffic > Security profiles (Application Control With Inline-CASB) |
| Diagnostics | Real-time packet capture on security PoPs | 24.4.a and later | NDM `SRG-APP-000408-NDM-000314` | GUI: Operations > Connectivity > Connected users (Packet capture; restrict to authorized administrators) |
| Posture | Security posture tagging rules: negated domain, FortiClient version, security status, CVEs, AND and OR logic, combined Tagging rules tab, and CrowdStrike ZTA scores | 24.4.a+; 25.3.a+; 25.4.c+ | VPN `SRG-NET-000148-VPN-000540`; VPN `SRG-NET-000343-VPN-001370` | GUI: Endpoint management > Security posture tags > Tagging rules |
| Logging | FortiClient event logs from endpoints (select availability) | 24.4.b and later | ALG `SRG-NET-000074-ALG-000043`; VPN `SRG-NET-000492-VPN-001980` | GUI: Operations > Logs > Events |
| Remote access | Network lockdown of off-net FortiClient endpoints, strict lockdown, exempt destinations, and captive portal handling | 24.4.b+; 25.1.b+; 25.4.b+; 26.2.1+ | VPN `SRG-NET-000230-VPN-002436` | GUI: Endpoint management > Configuration > Connection (Lockdown endpoint when off-net: on, Grace period, Exempt destinations) |
| Edge devices | FortiBranchSASE device integration | 24.4.b and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Agentless ZTNA | SSO authentication before the agentless ZTNA bookmark portal | 24.4.b and later | ALG `SRG-NET-000138-ALG-000063`; ALG `SRG-NET-000140-ALG-000094` | GUI: Access & authentication > Authentication Sources > SSO > Proxy |
| Remote access | Split tunneling by on-net status, and the All traffic option for Bypass FortiSASE | 24.4.b+; 26.2.2.a+ | VPN `SRG-NET-000369-VPN-001620` | GUI: Endpoint management > Configuration > Connection (Steering bypass destinations) (do not use All traffic unless the AO approves split tunneling) |
| Remote access | IPsec remote user connectivity: default on new instances (24.4.b.1), hybrid IPsec and SSL mode (25.4.b), and SSL to IPsec transition mode for all SSL instances (26.3.1) | 24.4.b.1+; 25.4.b+; 26.3.1+ | VPN `SRG-NET-000512-VPN-002220`; VPN `SRG-NET-000132-VPN-000460`; VPN `SRG-NET-000530-VPN-002340` | GUI: Operations > Software audit & version (complete the migration to IPsec) |
| Endpoint | New recommended and supported FortiClient versions and installers (7.2.6 to 7.4.8, Linux, Android, iOS, Windows ARM, and MSI) | 24.4.c+; 25.1.a+; 25.2.a+; 25.3.a+; 25.4.c+; 26.1.1.2+; 26.2.1+ | NDM `SRG-APP-001035-NDM-000340` | GUI: Endpoint management > Endpoint upgrade |
| Endpoint | Endpoint vulnerability scanning and automatic patching (profiles, Vulnerability Summary widget, Endpoint details pane, scan on software change) | 25.1.a+; 26.1.2.1+; 26.2.1+ | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | GUI: Endpoint management > Configuration > Protection (Trigger vulnerability scan on software change: on) |
| Policies | Schedules, service groups, and one-time schedules in policies and proxy policies | 25.1.a+; 25.4.b+ | ALG `SRG-NET-000018-ALG-000017` | GUI: Security > Resources > Schedules; GUI: Security > Traffic > Policies (Schedule) |
| Policies | Policy comments and sequence numbers | 25.1.a+; 25.3.a+ | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | GUI: Security > Traffic > Policies (Comments, Sequence Number) |
| Remote access | Personal VPN settings on FortiClient per endpoint profile | 25.1.a and later | VPN `SRG-NET-000132-VPN-000450` | Do not allow personal VPN settings on endpoint profiles for users; the 7.4 Administration Guide does not name this setting |
| Remote access | Local network access while connected to SIA | 25.1.a and later | VPN `SRG-NET-000369-VPN-001620` | GUI: Endpoint management > Configuration > Connection (Allow local LAN access: off) |
| API | REST API extensions: security profiles, user groups, authentication sources, data transfer statistics, and posture tag references | 25.1.a+; 25.4.c+; 26.2.2+ | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Onboarding | Authenticated onboarding: SAML SSO before onboarding with an invitation code (select availability), and Entra ID onboarding | 25.1.a+; 25.4.b+ | ALG `SRG-NET-000138-ALG-000063`; VPN `SRG-NET-000148-VPN-000540` | GUI: Access & authentication > Authentication Sources > SSO > Authenticated onboarding |
| Locations | Adding, changing, disabling, decommissioning, and migrating security PoPs | 25.1.a+; 26.2.1+ | CC `SRG-OS-000480-CLD-000035` | GUI: Operations > Infrastructure |
| Branch On-ramp | Branch On-ramp licensing and scale: connection add-on, up to 20 PoPs, Standard subscription, simplified licensing, and location licenses | 25.1.b+; 25.2.b+; 25.3.b+; 26.1.2.1+ | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Endpoint | Cloning endpoint profiles | 25.1.b and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Agent-based ZTNA | ZTNA application gateways and destinations under Agent-based ZTNA, with destinations as IP ranges or subnets | 25.1.b+; v7.4 New features | ALG `SRG-NET-000015-ALG-000016` | GUI: Security > Traffic > ZTNA > Agent-based |
| Endpoint | Signing the preconfigured FortiClient installer with your own CA certificate | 25.1.b and later | NDM `SRG-APP-000131-NDM-000243` | Request signing with your CA certificate through a FortiCare Support ticket |
| Remote access | Pre-logon tunnels: IKEv2 with SHA256 and DH group 15 (25.2.a), certificate-based tunnels to the nearest PoP (25.4.b), and pre-logon SPA and SIA policies (26.2.1) | 25.2.a+; 25.4.b+; 26.2.1+ | VPN `SRG-NET-000132-VPN-000460`; VPN `SRG-NET-000019-VPN-000040` | GUI: Endpoint management > Configuration > Pre-logon tunnel |
| Provisioning | Improved site provisioning with recovery | 25.2.b and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Administration | Software audit best practices: audit page, login prompt, Secure Proxy migration, and SOCaaS log forwarding | 25.2.c+; 25.3.b+ | NDM `SRG-APP-000516-NDM-000317` | GUI: Operations > Software audit & version |
| Network | Dedicated public IP addresses with the Standard subscription | 25.2.c and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Portal | FortiSASE v7.4 capabilities on new instances, and the v7.4 or v7.2 version tag | 25.2.c+; 25.3.b+ | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| CASB | Integrated FortiCASB API-based CASB | 25.2.c and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | GUI: System > API-based CASB |
| Security profiles | DLP enhancements: Exact Data Matching, IDM fingerprinting, and FortiGuard DLP service sensors and dictionaries | 25.2.c+; 25.3.b+ | ALG `SRG-NET-000018-ALG-000017` | GUI: Security > Traffic > Security profiles (DLP, Profile resources) |
| Branch On-ramp | Branch On-ramp IPsec connections from third-party devices, with the Local ID type for custom devices | 25.2.c+; 26.2.2+ | VPN `SRG-NET-000512-VPN-002220`; VPN `SRG-NET-000132-VPN-000460` | GUI: Operations > Connectivity > On-ramp tunnel |
| DNS | DNS handling: transparent DNS redirection, DNS suffixes and DNS resolution for IPsec tunnels, and registering addresses in DNS | 25.2.c+; 25.4.c+; 26.3.1+ | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | GUI: Network > DNS |
| Logging | Seven-day log retention for newly provisioned instances | 25.3.a and later | NDM `SRG-APP-000515-NDM-000325`; ALG `SRG-NET-000334-ALG-000050` | GUI: Operations > Logs > Settings (Log Retention (days)) (forward logs to an external server) |
| Proxy | Secure explicit proxy, and the hosted PAC file editor | 25.3.a and later | ALG `SRG-NET-000062-ALG-000150` | GUI: Network > Proxy configuration > Hosted PAC files |
| Security profiles | Inspecting or blocking QUIC (HTTP/3) traffic | 25.3.a and later | ALG `SRG-NET-000019-ALG-000018` | GUI: Security > Traffic > Security profiles (QUIC) |
| Remote access | Additional trusted remote gateways as failover for the Cloud Security tunnel | 25.3.a and later | VPN `SRG-NET-000132-VPN-000460` | GUI: Endpoint management > Configuration > Connection (Failover sequence) (configure each gateway with the FortiClient tunnel settings) |
| Policies | Endpoint-to-endpoint communication through an SPA hub | 25.3.a and later | ALG `SRG-NET-000202-ALG-000124` | GUI: Security > Traffic > Policies (allow only the required endpoint-to-endpoint traffic) |
| Maintenance | Preferred maintenance window slots, including a Japan window | 25.3.a+; 26.1.1+ | NDM `SRG-APP-000457-NDM-000352` | GUI: Operations > Software audit & version |
| Network | IP anchoring: public IP by user group, country or region, and destination, source IP anchoring for Public Cloud locations, on-ramp IP anchoring, and editing PoP public IP addresses | 25.3.a+; 26.1.1+; 26.3.1+; v7.4 New features | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | GUI: Network > IP management > Public IP |
| Posture | Pre-connection posture checks for the Cloud Security tunnel and custom IPsec tunnels | 25.3.a and later | VPN `SRG-NET-000343-VPN-001370`; VPN `SRG-NET-000148-VPN-000540` | GUI: Endpoint management > Configuration > Connection (Run posture check before initiating FortiSASE Cloud Security tunnel: on) |
| Edge devices | Captive portal replacement message for edge devices | 25.3.a and later | ALG `SRG-NET-000041-ALG-000022` | GUI: System > HTML templates (Captive Portal Login Page) |
| Authentication | FIDO2 authentication for agent tunnels, and the FortiClient built-in browser for SAML SSO | 25.3.b+; 25.4.b+ | VPN `SRG-NET-000140-VPN-000500`; ALG `SRG-NET-000140-ALG-000094` | GUI: Endpoint management > Configuration > Connection (Use FortiClient built-in browser for SAML authentication: on, Allow FIDO authentication) |
| Security profiles | Content disarm and reconstruction (CDR) in the AntiVirus profile | 25.3.b and later | ALG `SRG-NET-000765-ALG-000170`; ALG `SRG-NET-000249-ALG-000134` | GUI: Security > Traffic > Security profiles (AntiVirus) |
| Agentless ZTNA | Custom domain and certificate for ZTNA private applications | 25.3.c and later | ALG `SRG-NET-000062-ALG-000150`; NDM `SRG-APP-000910-NDM-000300` | GUI: Security > Traffic > ZTNA > Agentless (use a certificate from a DoD-approved CA) |
| Security profiles | Web Filter URL filter priority, search keyword logging, and category tooltips | 25.3.c and later | ALG `SRG-NET-000019-ALG-000018`; ALG `SRG-NET-000074-ALG-000043` | GUI: Security > Traffic > Security profiles (Web Filter) |
| Security profiles | Application control filter overrides, custom application and IPS signatures, and IPS custom filters | 25.3.c+; v7.4 New features | ALG `SRG-NET-000384-ALG-000136`; ALG `SRG-NET-000390-ALG-000139` | GUI: Security > Traffic > Security profiles (Application Control With Inline-CASB, Intrusion prevention) |
| Reports | Endpoint vulnerability, SPA, and Cloud Security Usage reports | 25.3.c+; 25.4.b+ | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Administration | Administrator logins, configuration audit logs, and user audit logs, with a required change summary | 25.3.c and later | NDM `SRG-APP-000343-NDM-000289`; NDM `SRG-APP-000380-NDM-000304`; NDM `SRG-APP-000503-NDM-000320` | GUI: System > Administration (Require comments for configuration audit log: on) |
| Administration | Automation page for alert emails on unstable SPA connections | 25.3.c+; 25.4.b+ | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | GUI: Operations > Administration > Automation |
| Agentless ZTNA | SAML single sign-out in the agentless ZTNA bookmark portal | 25.4.b and later | ALG `SRG-NET-000518-ALG-000007` | GUI: Security > Traffic > ZTNA > Agentless |
| Administration | Factory reset of an instance (principal FortiCloud account only) | 25.4.b and later | NDM `SRG-APP-000408-NDM-000314` | GUI: System > Backup and restore > Factory Reset (keep the principal account restricted) |
| Provisioning | Simplified security PoP selection | 25.4.b and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Remote access | IPsec over TCP port 443, and a per-profile override to TCP | 25.4.c+; 26.2.1+ | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | GUI: Endpoint management > Configuration > Global (FortiSASE Cloud Security Tunnel encapsulation) |
| Agent-based ZTNA | ZTNA automatic login using OAuth with Entra ID | 25.4.c and later | ALG `SRG-NET-000138-ALG-000063` | GUI: Endpoint management > Configuration > ZTNA |
| Posture | Sharing posture with ZTNA application gateways: learned tags (Record client tags and information) and endpoint host tags | 25.4.c+; v7.4 New features | ALG `SRG-NET-000015-ALG-000016`; VPN `SRG-NET-000148-VPN-000540` | GUI: Endpoint management > Security posture tags (Record client tags and information) |
| Authentication | SCIM user provisioning from Entra ID, FortiAuthenticator, and Okta (select availability) | 25.4.c+; 26.2.2+ | ALG `SRG-NET-000138-ALG-000088` | GUI: Access & authentication > Access > Users and groups > SCIM users and groups |
| Central management | Central management for MSSP tenants with a FortiManager key | 25.4.c and later | NDM `SRG-APP-000380-NDM-000304` | GUI: System > Central management (revoke the FortiManager key when parent OU management is not approved) |
| Agent-based ZTNA | Disabling agent-based ZTNA on FortiClient per endpoint profile | 26.1.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | GUI: Endpoint management > Configuration > ZTNA |
| Endpoint | FortiClient GUI and control settings: selected tabs, debug log level, shutdown, inventory, DNS bypass, and certificate warnings | 26.1.1+; 26.3.1+ | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | GUI: Endpoint management > Configuration > FortiClient GUI Settings |
| Logging | Additional log forwarding server | 26.1.1 and later | NDM `SRG-APP-000516-NDM-000350`; ALG `SRG-NET-000334-ALG-000050` | GUI: Operations > Logs > Settings (Log Forwarding to Self-Managed Service) |
| Logging | Log forwarding to FortiAnalyzer Cloud | 26.1.1 and later | ALG `SRG-NET-000334-ALG-000050`; NDM `SRG-APP-000515-NDM-000325` | GUI: Operations > Logs > Settings (Log forwarding to FortiAnalyzer Cloud) |
| Remote access | Updating the IPsec pre-shared key of the Cloud Security tunnel | 26.1.1.1 and later | VPN `SRG-NET-000343-VPN-001370` | GUI: Endpoint management > Configuration > Global (Pre-shared key) |
| Remote access | Autoconnect using the session resumption timeout, and the internet check before autoconnect | 26.1.1.1 and later | VPN `SRG-NET-000230-VPN-002436` | GUI: Endpoint management > Configuration > Global (Session resumption timeout) |
| Policies | Bandwidth control policies and profiles | 26.1.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | GUI: Security > Traffic > Bandwidth control |
| Secure Browser | FortiSASE Secure Browser extension for unmanaged devices (select availability), with SSO domain integration | 26.1.2.1+; 26.2.2+ | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | GUI: Security > Browser |
| Remote access | IPsec dead peer detection customization (select availability) | 26.1.2.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | GUI: Endpoint management > Configuration > Connection (Dead peer detection) |
| CASB | FortiCASB-SSPM integration (SaaS security posture management) | 26.2.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Authentication | LDAP authentication for IPsec agent tunnels (EAP for LDAP authentication), and the RADIUS server timeout | 26.2.1 and later | VPN `SRG-NET-000166-VPN-000580` | GUI: Endpoint management > Configuration > Global (EAP for LDAP authentication); GUI: Access & authentication > Authentication Sources > RADIUS |
| Endpoint | On connect and on disconnect scripts | 26.2.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | GUI: Endpoint management > Configuration > Connection (On connect script) (leave empty unless reviewed) |
| Agent-based ZTNA | BYOD enrollment through MDM with ZTNA client certificates (iOS, Intune and Jamf) | 26.2.1 and later | VPN `SRG-NET-000343-VPN-001370` | GUI: System > UEM integration |
| Endpoint | FortiPAM integration, and the FortiPAM agent in the FortiClient installer | 26.2.1+; v7.4 New features | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Endpoint | Endpoint management navigation renamed, and endpoint inactivity disable and delete settings | 26.2.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | GUI: Endpoint management > Configuration > Global (Endpoint inactivity) |
| Authentication | Active Directory connector API key for a private AD server | 26.2.2 and later | ALG `SRG-NET-000138-ALG-000088` | GUI: Access & authentication > Authentication Sources > Domains |
| Agent-based ZTNA | ZTNA UDP traffic forwarding | 26.2.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Locations | Best practice and notices to migrate to newer, faster security PoPs (including Branch On-ramp PoPs) | 26.2.2+; 26.3.1.a+ | CC `SRG-OS-000480-CLD-000035` | GUI: Operations > Software audit & version (migrate only to approved locations) |
| Diagnostics | Network Tools speed test page | 26.2.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Authentication | SAML IdP metadata import | 26.3.1 and later | ALG `SRG-NET-000138-ALG-000088` | GUI: Access & authentication > Authentication Sources > SSO |
| Remote access | Manual quarantine of managed FortiClient endpoints | 26.3.1 and later | VPN `SRG-NET-000314-VPN-001060`; ALG `SRG-NET-000314-ALG-000013` | GUI: Operations > Connectivity > Endpoints (Quarantine endpoint) |
| Agent-based ZTNA | FortiGate access keys for ZTNA application gateways in other FortiCloud accounts | 26.3.1 and later | ALG `SRG-NET-000015-ALG-000016` | GUI: Security > Traffic > ZTNA > Agent-based > Access keys (revoke unused keys) |
| Administration | Portal session timeout (5 to 480 minutes) | 26.3.1 and later | NDM `SRG-APP-000190-NDM-000267` | GUI: System > Administration (Session timeout: 5) |
| Administration | Backup and restore of selected configuration settings (select availability, up to 10 backups) | 26.3.1 and later | NDM `SRG-APP-000516-NDM-000340` | GUI: System > Backup and restore > Configuration revisions |
| Security profiles | File Filter blocking of password-protected files, and profile group protocol options for unknown content and oversized files | v7.4 (release not listed) and later | ALG `SRG-NET-000019-ALG-000018` | GUI: Security > Traffic > Security profiles (File Filter) |

### Requirement reference

The table lists every requirement used in the feature map or cited in
this chapter, with its severity and title from the XCCDF files.

[Download the requirement reference as CSV](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/data/volume-172-disa-srgs-and-stigs/29-fortisase-feature-version-and-srg-map-requirements.csv) (112 rows).

| SRG | Requirement | Severity | Requirement title |
| --- | --- | --- | --- |
| CC | `SRG-OS-000001-CLD-000010` | CAT I | The Mission Owner must configure the customer service portal credentials for least privilege. |
| CC | `SRG-OS-000023-CLD-000015` | CAT II | The Mission Owner must configure the cloud service offering (CSO)-provided customer logon banner to display the Standard Mandatory DOD Notice and Consent Banner before granting access to users that must log on. |
| CC | `SRG-OS-000096-CLD-000060` | CAT II | The Mission Owner must configure the Infrastructure as a Service (IaaS)/Platform as a Service (PaaS) to prohibit or restrict the use of functions, ports, protocols, and/or services. |
| CC | `SRG-OS-000104-CLD-000065` | CAT II | The cloud service offering (CSO) must be configured to use DOD public key infrastructure (PKI) to uniquely identify and authenticate organizational users (or processes acting on behalf of organizational users). |
| CC | `SRG-OS-000342-CLD-000020` | CAT II | The Infrastructure as a Service (IaaS)/Platform as a Service (PaaS) must perform centralized logging to capture and store log records. |
| CC | `SRG-OS-000368-CLD-000040` | CAT II | For Impact Levels 4 and 5, the Mission Owner must register all cloud-based services, their CSP/CSO, and connection method in the DISA Systems/Network Approval Process (SNAP) database Cloud Module. |
| CC | `SRG-OS-000370-CLD-000050` | CAT II | The Infrastructure as a Service (IaaS)/Platform as a Service (PaaS)/Software as a Service (SaaS) must register the service/application with the DOD DMZ/IAP allowlist for internet-facing inbound and outbound traffic. |
| CC | `SRG-OS-000404-CLD-000080` | CAT I | For storage service offerings, the Mission Owner must configure or ensure the cloud instance uses encryption to protect all DOD files housed in the cloud instance. |
| CC | `SRG-OS-000480-CLD-000025` | CAT II | The Mission owner must obtain Authorizing Official (AO) authorization for each cloud service offering (CSO) implemented in support of production or development environments prior to operational use. |
| CC | `SRG-OS-000480-CLD-000030` | CAT II | The Mission Owner must select and configure an Impact Level 2 FedRAMP authorized cloud service offering (CSO) when hosting unclassified, publicly releasable DOD information. |
| CC | `SRG-OS-000480-CLD-000031` | CAT I | The Mission Owner must select and configure an Impact Level 4/5 cloud service offering (CSO) listed in the DISA Provisional Authorization (PA) DOD Cloud Catalog when hosting Controlled Unclassified Information (CUI). |
| CC | `SRG-OS-000480-CLD-000032` | CAT I | The Mission Owner must select and configure an Impact Level 5 cloud service offering (CSO) listed in the DISA Provisional Authorization (PA) DOD Cloud Catalog when hosting Unclassified National Security Information (U-NSI). |
| CC | `SRG-OS-000480-CLD-000033` | CAT I | The Mission Owners must select and configure a cloud service offering (CSO) listed in the DISA Provisional Authorization (PA) DOD Cloud Catalog at Level 6 when hosting classified DOD information. |
| CC | `SRG-OS-000480-CLD-000035` | CAT II | The Mission Owner must add all applicable compensating controls and requirements in the Service Level Agreement (SLA)/contract with the cloud service provider (CSP) or third-party provider. |
| ALG | `SRG-NET-000015-ALG-000016` | CAT II | The ALG must enforce approved authorizations for logical access to information and system resources by employing identity-based, role-based, and/or attribute-based security policies. |
| ALG | `SRG-NET-000018-ALG-000017` | CAT II | The ALG must enforce approved authorizations for controlling the flow of information within the network based on attribute- and content-based inspection of the source, destination, headers, and/or content of the communications traffic. |
| ALG | `SRG-NET-000019-ALG-000018` | CAT II | The ALG must restrict or block harmful or suspicious communications traffic by controlling the flow of information between interconnected networks based on attribute- and content-based inspection of the source, destination, headers, and/or content of the communications traffic. |
| ALG | `SRG-NET-000019-ALG-000019` | CAT II | The ALG must immediately use updates made to policy enforcement mechanisms such as policy filters, rules, signatures, and analysis algorithms for gateway and/or intermediary functions. |
| ALG | `SRG-NET-000041-ALG-000022` | CAT II | The ALG providing user access control intermediary services must display the Standard Mandatory DoD-approved Notice and Consent Banner before granting access to the network. |
| ALG | `SRG-NET-000042-ALG-000023` | CAT II | The ALG providing user access control intermediary services must retain the Standard Mandatory DoD-approved Notice and Consent Banner on the screen until users acknowledge the usage conditions and take explicit actions to log on for further access. |
| ALG | `SRG-NET-000062-ALG-000150` | CAT II | The ALG that provides intermediary services for TLS must be configured to comply with the required TLS settings in NIST SP 800-52. |
| ALG | `SRG-NET-000074-ALG-000043` | CAT II | The ALG must produce audit records containing information to establish what type of events occurred. |
| ALG | `SRG-NET-000077-ALG-000046` | CAT II | The ALG must produce audit records containing information to establish the source of the events. |
| ALG | `SRG-NET-000079-ALG-000048` | CAT II | The ALG must generate audit records containing information to establish the identity of any individual or process associated with the event. |
| ALG | `SRG-NET-000131-ALG-000085` | CAT II | The ALG must not have unnecessary services and functions enabled. |
| ALG | `SRG-NET-000131-ALG-000086` | CAT II | The ALG must be configured to remove or disable unrelated or unneeded application proxy services. |
| ALG | `SRG-NET-000132-ALG-000087` | CAT II | The ALG must be configured to prohibit or restrict the use of functions, ports, protocols, and/or services, as defined in the PPSM CAL and vulnerability assessments. |
| ALG | `SRG-NET-000138-ALG-000063` | CAT II | The ALG providing user authentication intermediary services must uniquely identify and authenticate organizational users (or processes acting on behalf of organizational users). |
| ALG | `SRG-NET-000138-ALG-000088` | CAT II | The ALG providing user access control intermediary services must be configured with a pre-established trust relationship and mechanisms with appropriate authorities (e.g., Active Directory or AAA server) which validate user account access authorizations and privileges. |
| ALG | `SRG-NET-000140-ALG-000094` | CAT II | The ALG providing user authentication intermediary services must use multifactor authentication for network access to non-privileged accounts. |
| ALG | `SRG-NET-000164-ALG-000100` | CAT II | The ALG that provides intermediary services for TLS must validate certificates used for TLS functions by performing RFC 5280-compliant certification path validation. |
| ALG | `SRG-NET-000169-ALG-000102` | CAT II | The ALG providing user authentication intermediary services must uniquely identify and authenticate non-organizational users (or processes acting on behalf of non-organizational users). |
| ALG | `SRG-NET-000202-ALG-000124` | CAT II | The ALG must deny network communications traffic by default and allow network communications traffic by exception (i.e., deny all, permit by exception). |
| ALG | `SRG-NET-000246-ALG-000132` | CAT II | The ALG providing content filtering must update malicious code protection mechanisms and signature definitions whenever new releases are available in accordance with organizational configuration management policy. |
| ALG | `SRG-NET-000248-ALG-000133` | CAT II | The ALG providing content filtering must be configured to perform real-time scans of files from external sources at network entry/exit points as they are downloaded and prior to being opened or executed. |
| ALG | `SRG-NET-000249-ALG-000134` | CAT II | The ALG providing content filtering must block malicious code upon detection. |
| ALG | `SRG-NET-000249-ALG-000145` | CAT II | The ALG providing content filtering must delete or quarantine malicious code in response to malicious code detection. |
| ALG | `SRG-NET-000251-ALG-000131` | CAT II | The ALG providing content filtering must update malicious code protection mechanisms and signature definitions whenever new releases are available in accordance with organizational configuration management procedures. |
| ALG | `SRG-NET-000288-ALG-000109` | CAT II | The ALG providing content filtering must block or restrict detected prohibited mobile code. |
| ALG | `SRG-NET-000289-ALG-000110` | CAT II | The ALG providing content filtering must prevent the download of prohibited mobile code. |
| ALG | `SRG-NET-000313-ALG-000010` | CAT II | The ALG providing intermediary services for remote access communications traffic must control remote access methods. |
| ALG | `SRG-NET-000314-ALG-000013` | CAT II | The ALG providing intermediary services for remote access communications traffic must provide the capability to immediately disconnect or disable remote access to the information system. |
| ALG | `SRG-NET-000318-ALG-000151` | CAT II | To protect against data mining, the ALG providing content filtering must prevent code injection attacks launched against application objects including, at a minimum, application URLs and application code. |
| ALG | `SRG-NET-000334-ALG-000050` | CAT II | The ALG must off-load audit records onto a centralized log server. |
| ALG | `SRG-NET-000337-ALG-000096` | CAT II | The ALG providing user authentication intermediary services must require users to reauthenticate when organization-defined circumstances or situations require reauthentication. |
| ALG | `SRG-NET-000345-ALG-000099` | CAT II | The ALG providing user authentication intermediary services using PKI-based user authentication must implement a local cache of revocation data to support path discovery and validation in case of the inability to access revocation information via the network. |
| ALG | `SRG-NET-000364-ALG-000122` | CAT II | The ALG must only allow incoming communications from organization-defined authorized sources routed to organization-defined authorized destinations. |
| ALG | `SRG-NET-000383-ALG-000135` | CAT II | The ALG providing content filtering must be configured to integrate with a system-wide intrusion detection system. |
| ALG | `SRG-NET-000384-ALG-000136` | CAT II | The ALG providing content filtering must detect use of network services that have not been authorized or approved by the ISSM and ISSO, at a minimum. |
| ALG | `SRG-NET-000385-ALG-000137` | CAT II | The ALG providing content filtering must generate a log record when unauthorized network services are detected. |
| ALG | `SRG-NET-000390-ALG-000139` | CAT II | The ALG providing content filtering must continuously monitor inbound communications traffic crossing internal security boundaries for unusual or unauthorized activities or conditions. |
| ALG | `SRG-NET-000391-ALG-000140` | CAT II | The ALG providing content filtering must continuously monitor outbound communications traffic crossing internal security boundaries for unusual/unauthorized activities or conditions. |
| ALG | `SRG-NET-000503-ALG-000038` | CAT II | The ALG providing user access control intermediary services must generate audit records when successful/unsuccessful logon attempts occur. |
| ALG | `SRG-NET-000510-ALG-000111` | CAT II | The ALG providing encryption intermediary services must use NIST FIPS-validated cryptography to implement encryption services. |
| ALG | `SRG-NET-000511-ALG-000051` | CAT II | The ALG must off-load audit records onto a centralized log server in real time. |
| ALG | `SRG-NET-000518-ALG-000007` | CAT II | The ALG providing user access control intermediary services must provide a logoff capability for user-initiated communications sessions. |
| ALG | `SRG-NET-000750-ALG-000140` | CAT II | The ALG must include only approved trust anchors in trust stores or certificate stores managed by the organization. |
| ALG | `SRG-NET-000765-ALG-000170` | CAT II | The ALG must implement signature based and/or nonsignature based malicious code protection mechanisms at system entry and exit points to detect and eradicate malicious code. |
| VPN | `SRG-NET-000015-VPN-000010` | CAT II | The VPN Gateway must enforce approved authorizations for logical access to information and system resources in accordance with applicable access control policies. |
| VPN | `SRG-NET-000019-VPN-000040` | CAT II | The VPN Gateway must ensure inbound and outbound traffic is configured with a security policy in compliance with information flow control policies. |
| VPN | `SRG-NET-000041-VPN-000110` | CAT II | The Remote Access VPN Gateway and/or client must display the Standard Mandatory DOD Notice and Consent Banner before granting remote access to the network. |
| VPN | `SRG-NET-000062-VPN-000200` | CAT I | The TLS VPN Gateway must use TLS 1.2, at a minimum, to protect the confidentiality of sensitive data during transmission for remote access connections. |
| VPN | `SRG-NET-000063-VPN-000220` | CAT II | The VPN Gateway must be configured to use IPsec with SHA-2 at 384 bits or greater for hashing to protect the integrity of remote access sessions. |
| VPN | `SRG-NET-000074-VPN-000250` | CAT I | The IPSec VPN must be configured to use a Diffie-Hellman (DH) Group of 16 or greater for Internet Key Exchange (IKE) Phase 1. |
| VPN | `SRG-NET-000132-VPN-000450` | CAT II | The VPN Gateway must be configured to prohibit the use of all unnecessary and/or nonsecure functions, ports, protocols, and/or services, as defined in the PPSM CAL and vulnerability assessments. |
| VPN | `SRG-NET-000132-VPN-000460` | CAT II | The IPsec VPN Gateway must use IKEv2 for IPsec VPN security associations. |
| VPN | `SRG-NET-000138-VPN-000490` | CAT II | The VPN Gateway must uniquely identify and authenticate organizational users (or processes acting on behalf of organizational users). |
| VPN | `SRG-NET-000140-VPN-000500` | CAT I | The VPN Gateway must use multifactor authentication (e.g., DoD PKI) for network access to non-privileged accounts. |
| VPN | `SRG-NET-000148-VPN-000540` | CAT II | The VPN Gateway must uniquely identify all network-connected endpoint devices before establishing a connection. |
| VPN | `SRG-NET-000164-VPN-000560` | CAT II | The VPN Gateway, when utilizing PKI-based authentication, must validate certificates by constructing a certification path (which includes status information) to an accepted trust anchor. |
| VPN | `SRG-NET-000166-VPN-000580` | CAT II | The Remote Access VPN Gateway must use a separate authentication server (e.g., LDAP, RADIUS, TACACS+) to perform user authentication. |
| VPN | `SRG-NET-000166-VPN-000590` | CAT II | The VPN Gateway must map the authenticated identity to the user account for PKI-based authentication. |
| VPN | `SRG-NET-000213-VPN-000721` | CAT II | The Remote Access VPN Gateway must terminate remote access network connections after an organization-defined time period. |
| VPN | `SRG-NET-000230-VPN-000780` | CAT I | The IPSec VPN must be configured to use FIPS-validated SHA-2 at 384 bits or higher for Internet Key Exchange (IKE). |
| VPN | `SRG-NET-000230-VPN-002436` | CAT II | The VPN Gateway must use Always On VPN connections for remote computing. |
| VPN | `SRG-NET-000314-VPN-001060` | CAT II | The VPN Gateway administrator accounts or security policy must be configured to allow the system administrator to immediately disconnect or disable remote access to devices and/or users when needed. |
| VPN | `SRG-NET-000334-VPN-001260` | CAT II | The VPN Gateway must off-load audit records onto a different system or media than the system being audited. |
| VPN | `SRG-NET-000341-VPN-001350` | CAT II | The VPN Gateway must accept the Common Access Card (CAC) credential. |
| VPN | `SRG-NET-000343-VPN-001370` | CAT II | The VPN Gateway must authenticate all network-connected endpoint devices before establishing a connection. |
| VPN | `SRG-NET-000369-VPN-001620` | CAT II | The VPN Gateway must disable split-tunneling for remote clients VPNs. |
| VPN | `SRG-NET-000371-VPN-001650` | CAT I | The VPN Gateway and Client must be configured to protect the confidentiality and integrity of transmitted information. |
| VPN | `SRG-NET-000492-VPN-001980` | CAT II | The VPN Gateway must generate log records when successful and/or unsuccessful VPN connection attempts occur. |
| VPN | `SRG-NET-000510-VPN-002170` | CAT II | The VPN Gateway must use a FIPS-validated cryptographic module to implement encryption services for unclassified information requiring confidentiality. |
| VPN | `SRG-NET-000512-VPN-002220` | CAT I | The IPsec VPN Gateway must use Internet Key Exchange (IKE) for IPsec VPN Security Associations (SAs). |
| VPN | `SRG-NET-000525-VPN-002330` | CAT I | The IPsec VPN must use AES256 or greater encryption for the IPsec proposal to protect the confidentiality of remote access sessions. |
| VPN | `SRG-NET-000530-VPN-002340` | CAT II | The TLS VPN Gateway that supports Government-only services must prohibit client negotiation to TLS 1.1, TLS 1.0, SSL 2.0, or SSL 3.0. |
| VPN | `SRG-NET-000580-VPN-002431` | CAT II | The VPN Gateway must configure OCSP to ensure revoked user certificates are prohibited from establishing an allowed session. |
| NDM | `SRG-APP-000033-NDM-000212` | CAT I | The network device must be configured to assign appropriate user roles or access levels to authenticated users. |
| NDM | `SRG-APP-000065-NDM-000214` | CAT II | The network device must be configured to enforce the limit of three consecutive invalid logon attempts, after which time it must block any login attempt for 15 minutes. |
| NDM | `SRG-APP-000068-NDM-000215` | CAT II | The network device must display the Standard Mandatory DoD Notice and Consent Banner before granting access to the device. |
| NDM | `SRG-APP-000100-NDM-000230` | CAT II | The network device must generate audit records containing information that establishes the identity of any individual or process associated with the event. |
| NDM | `SRG-APP-000131-NDM-000243` | CAT II | The network device must prevent the installation of patches, service packs, or application components without verification the software component has been digitally signed using a certificate that is recognized and approved by the organization. |
| NDM | `SRG-APP-000142-NDM-000245` | CAT I | The network device must be configured to prohibit the use of all unnecessary and/or nonsecure functions, ports, protocols, and/or services |
| NDM | `SRG-APP-000148-NDM-000346` | CAT II | The network device must be configured with only one local account to be used as the account of last resort in the event the authentication server is unavailable. |
| NDM | `SRG-APP-000149-NDM-000247` | CAT I | The network device must be configured to use DoD PKI as multi-factor authentication (MFA) for interactive logins. |
| NDM | `SRG-APP-000153-NDM-000249` | CAT II | The network device must be configured to authenticate each administrator prior to authorizing privileges based on assignment of group or role. |
| NDM | `SRG-APP-000164-NDM-000252` | CAT II | The network device must enforce a minimum 15-character password length. |
| NDM | `SRG-APP-000179-NDM-000265` | CAT I | The network device must use FIPS 140-2 approved algorithms for authentication to a cryptographic module. |
| NDM | `SRG-APP-000190-NDM-000267` | CAT I | The network device must terminate all network connections associated with a device management session at the end of the session, or the session must be terminated after five minutes of inactivity except to fulfill documented and validated mission requirements. |
| NDM | `SRG-APP-000329-NDM-000287` | CAT II | If the network device uses role-based access control, the network device must enforce organization-defined role-based access control policies over defined subjects and objects. |
| NDM | `SRG-APP-000343-NDM-000289` | CAT II | The network device must audit the execution of privileged functions. |
| NDM | `SRG-APP-000380-NDM-000304` | CAT II | The network device must enforce access restrictions associated with changes to device configuration. |
| NDM | `SRG-APP-000408-NDM-000314` | CAT II | Network devices performing maintenance functions must restrict use of these functions to authorized personnel only. |
| NDM | `SRG-APP-000457-NDM-000352` | CAT II | The network device must install security-relevant firmware updates within 30 days unless the time period is directed by an authoritative source (e.g., IAVM, CTOs, DTMs, STIGs). |
| NDM | `SRG-APP-000503-NDM-000320` | CAT II | The network device must generate audit records when successful/unsuccessful logon attempts occur. |
| NDM | `SRG-APP-000515-NDM-000325` | CAT II | The network device must off-load audit records onto a different system or media than the system being audited. |
| NDM | `SRG-APP-000516-NDM-000317` | CAT II | The network device must be configured in accordance with the security configuration settings based on DoD security configuration or implementation guidance, including STIGs, NSA configuration guides, CTOs, and DTMs. |
| NDM | `SRG-APP-000516-NDM-000336` | CAT I | The network device must be configured to use at least one authentication server for the purpose of authenticating users prior to granting administrative access. For boundary devices, two authentication servers are required. |
| NDM | `SRG-APP-000516-NDM-000340` | CAT II | The network device must be configured to conduct backups of system level information contained in the information system when changes occur. |
| NDM | `SRG-APP-000516-NDM-000350` | CAT I | The network device must be configured to send log data to at least one central log server for the purpose of forwarding alerts to the administrators and the information system security officer (ISSO). For boundary devices, two log servers are required. |
| NDM | `SRG-APP-000910-NDM-000300` | CAT II | The network device must be configured to include only approved trust anchors in trust stores or certificate stores managed by the organization. |
| NDM | `SRG-APP-001035-NDM-000340` | CAT I | The network device hardware and software must be a version supported by the vendor. |

### Collecting evidence

Keep the authorization evidence first: the DoD Cloud Service Catalog or
FedRAMP Marketplace entry for the offering and its impact level, the AO's
authorization, the SNAP, PPSM, and allowlist registrations, and the
contract clauses. Record the FortiSASE release from the version tooltip at
the bottom of the portal navigation (it also shows v7.4 or v7.2), and the
FortiClient versions in use (*Operations > Connectivity > Endpoints*).
Add screenshots or exports of the panes the map cites, above all
*Security > Traffic > Policies* and *Proxy policies* with the profile group
and logging of each policy, the security profiles,
*Endpoint management > Configuration* (the Global page and the Connection
tab of each profile), *Access & authentication* (SSO, LDAP, RADIUS, users
and groups), *Operations > Logs > Settings* (forwarding servers, secure
connection, retention, anonymization), *System > Administration* (session
timeout and configuration audit logs), *System > Certificates*, and
*Operations > Infrastructure* with the selected PoPs. Export the
Administrator Events log for the assessment period, and record which IAM
users and external IdP roles can reach the instance in FortiCloud.

## Validation and Troubleshooting

- **A feature in the map is missing.** Check whether the instance is v7.4
  or v7.2, whether it was created before or after the release that added
  the feature (many features are for new instances first), whether it has
  IPsec remote agent support, whether endpoints run the required
  FortiClient version, and whether the feature is select availability or
  needs an add-on license.
- **A setting is not where the map says.** The map uses the 7.4 pane
  names. Earlier releases used *Configuration > Profiles* for endpoint
  profiles and *SWG* for the proxy, and the navigation was reorganized in
  25.2.c and renamed again in 26.2.1.
- **Users cannot connect after hardening.** Check that the required ports
  (TCP 443, UDP 500 and 4500, and the others in *Required services and
  ports*) are open, that network lockdown exempt destinations include the
  IdP, that pre-connection posture checks match the endpoint's tags, and
  that the SAML IdP has the IPsec service provider settings (port 11443)
  after the SSL to IPsec transition.
- **Logs do not reach the log server.** Check the connection status in
  *Operations > Logs > Settings*, that the remote CA certificate of the
  syslog server is imported for a secure connection, and, for a private
  server, that SPA is configured.
- **A requirement has no matching feature.** Some requirements are met by
  procedure (account reviews, contract terms), by another system (the
  identity provider, the central log server, FortiCloud), or by Fortinet
  as the provider. Record how each requirement is met, not just which
  feature covers it.

## Security and Best Practices

- Use FortiSASE for DoD information only when the offering is authorized
  at the impact level of the data, and review the authorization and this
  map each time Fortinet publishes a FortiSASE release or DISA updates the
  Cloud Computing, ALG, VPN, or NDM SRG.
- Administer the instance through IAM users or external IdP roles with
  CAC, keep the primary FortiCloud account as the account of last resort,
  enable configuration audit logs, and set the portal session timeout.
- Replace the default Allow-All policies, inspect with deep inspection and
  a full security profile group, and log all sessions.
- Keep endpoints in the tunnel with autoconnect, no disconnect option, and
  network lockdown, without split tunneling, and check posture before
  connecting.
- Authenticate users through a SAML IdP that enforces CAC, and use
  separate authentication servers rather than local users.
- Import only DoD-approved CA certificates, and use DoD-issued
  certificates for deep inspection and custom ZTNA domains.
- Forward all logs in real time over TLS to a log server in your boundary.
- Record the provider findings (tunnel cryptography, FIPS validation,
  banners, revocation checking) and track them with Fortinet.

## References and Knowledge Checks

**References:**

- Fortinet, *FortiSASE 7.4 Release Notes*, page "What's new" (releases
  25.1.a through 26.3.1.a), and *FortiSASE 24.4.87 Release Notes* (PDF,
  releases 24.3.b through 24.4.c, retrieved from the Internet Archive).
- Fortinet, *FortiSASE 7.4 Administration Guide* (including the New
  features table and Appendix B - REST API) and *FortiSASE 24.4.87
  Administration Guide* (for the core features, retrieved from the
  Internet Archive).
- DISA Cloud Computing SRG (`U_Cloud_Computing_Y26M06_SRG.zip`): Cloud
  Service Provider SRG V1R7, Cloud Computing Mission Owner SRG Overview,
  Mission Owner Operating System SRG V1R3, Mission Owner Network SRG V1R2,
  and the release memo; and the Application Layer Gateway SRG V2R4,
  Virtual Private Network SRG V3R5, and Network Device Management SRG V5R5,
  from the October 2026 STIG Library Compilation.
- [Chapter 03](03-the-srg-catalog-how-stigs-are-built-and-what-to-do-without-one.md)
  (SRG-based assessment),
  [Chapter 08](08-applications-databases-web-servers-containers-and-cloud.md)
  (cloud services and the Cloud Computing SRG),
  [Chapter 10](10-fortinet-products-stigs-and-srg-mapping.md) (Fortinet
  products),
  [Chapter 11](11-fortiswitch-feature-version-and-srg-map.md) (the
  FortiSwitch map),
  [Chapter 12](12-fortianalyzer-feature-version-and-srg-map.md) (the
  FortiAnalyzer map, the model for this one),
  [Chapter 18](18-fortiproxy-feature-version-and-srg-map.md) (the FortiProxy
  map, which uses the ALG SRG), and
  [Chapter 27](27-forticlient-and-ems-feature-version-and-srg-map.md) (the
  FortiClient and EMS map, which uses the VPN and UEM SRGs).

**Knowledge checks:**

1. What are the two parts of the Cloud Computing SRG, and which of them
   has requirement IDs?
2. Which FortiSASE capabilities does Fortinet operate, and why does the
   map assign requirements only to tenant settings?
3. Why are the ALG, VPN, and NDM SRGs used in addition to the Cloud
   Computing SRG, and which requirement is used for rows with no direct
   requirement in each case?
4. Where does the version data come from, and how do you read a release
   name such as 25.3.a or 26.2.2.a?
5. Which endpoint profile settings keep a remote user's traffic in the
   FortiSASE tunnel?
6. Which requirements can FortiSASE not meet with tenant settings, and how
   do you handle them?

## Summary and Completion Checklist

FortiSASE has no STIG. It is assessed against the Cloud Computing SRG for
the customer's use of the offering, with the ALG SRG for the inspection
functions, the VPN SRG for remote access, and the NDM SRG for portal
administration, as far as the tenant configures them; what Fortinet
operates is assessed through the offering's authorization. This chapter
maps 168 features to the FortiSASE release that introduced them, to
112 requirements (14 CC, 44 ALG, 29 VPN, and 25
NDM), and to the portal pane that configures them: 66 core platform
features, and 102 features from the FortiSASE 24.3.b through 26.3.1.a
release notes and the v7.4 New features table. Operational features with
no direct requirement fall under the requirement to disable unnecessary
functions when unused.

- [ ] Can explain the parts of the Cloud Computing SRG and the
  identifiers it uses.
- [ ] Can separate Fortinet's responsibilities from the tenant's.
- [ ] Can find the FortiSASE release that introduced a feature.
- [ ] Can map a FortiSASE feature to its CC, ALG, VPN, or NDM
  requirement.
- [ ] Can find the pane that meets the requirement.
- [ ] Can collect the evidence and record the requirements that FortiSASE
  cannot meet with tenant settings.
