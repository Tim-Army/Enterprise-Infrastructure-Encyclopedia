# Volume XXIV Glossary

Definitions for terms introduced in **Volume C (XXIV) — Reference
Library**, alphabetized. See also the [volume index](INDEX.md) for
pointers back to the chapter section each term is drawn from, and the
[master glossary](../../GLOSSARY.md) for cross-volume terminology.

**Acceptance** — The governance act of a named, responsible party
reviewing validation evidence and formally agreeing a change met its
stated objective, distinct from the technical act of validation itself.
Introduced in Chapter 05.

**ARN (Amazon Resource Name)** — AWS's structured identifier format
(`arn:<partition>:<service>:<region>:<account-id>:<resource>`) used to
uniquely reference a cloud resource across IAM policies and APIs.
Introduced in Chapter 03.

**Baseline** — A specific, approved, versioned instance of a
configuration — the answer to "what should this system's configuration be
right now" — distinct from the template that produces it. Introduced in
Chapter 04.

**Bottom-up troubleshooting** — A layered diagnostic methodology that
starts at the physical/link layer and works upward through the OSI stack,
preferred when a connectivity symptom's cause is unknown. Introduced in
Chapter 06.

**CIA triad** — Confidentiality, Integrity, and Availability: the three
properties nearly every security control is ultimately justified through.
Introduced in Chapter 07.

**CIDR (Classless Inter-Domain Routing)** — The prefix-length-based
addressing scheme (RFC 4632) that replaced the historical IPv4 class
system, expressed as an address followed by a slash and prefix length
(for example, `10.0.0.0/24`). Introduced in Chapter 03.

**CIS Benchmark** — A configuration hardening standard published by the
Center for Internet Security for a specific platform, offering Level 1
(broadly applicable) and Level 2 (defense-in-depth) profiles. Introduced
in Chapter 07.

**Command Tiering (Tier 0–3)** — A platform-independent risk
classification for administrative commands, from Tier 0 (read-only,
always safe) through Tier 3 (destructive or hard to reverse), used to
scale change-management rigor to actual risk. Introduced in Chapter 01.

**CVSS (Common Vulnerability Scoring System)** — A standardized scoring
system (maintained by FIRST) that rates vulnerability severity from 0.0 to
10.0, mapped to Low/Medium/High/Critical bands. Introduced in Chapter 07.

**Data classification tier** — A category (commonly Public, Internal,
Confidential, or Restricted) assigned to data to determine its required
handling, access control, and retention. Introduced in Chapter 07.

**Decision tree (troubleshooting)** — A written, repeatable sequence of
diagnostic questions, each anchored to a specific runnable check, that
guides a responder from a symptom to a specific next action. Introduced in
Chapter 06.

**Distinguished Name (DN)** — The structured identifier format used by
LDAP and Active Directory to uniquely locate an object in a directory tree
(`CN=<name>,OU=<org unit>,DC=<domain>,DC=<tld>`). Introduced in Chapter 03.

**Divide-and-conquer troubleshooting** — A diagnostic methodology that
starts at a midpoint in a path or stack and branches up or down based on
the result, minimizing checks when the failing component is unknown across
a long path. Introduced in Chapter 06.

**Drift (configuration)** — Any divergence between a system's actual,
running configuration and its declared baseline, whether from an
unauthorized change, an undocumented emergency change, or a detection
false positive. Introduced in Chapter 04.

**East-west traffic** — Server-to-server network traffic, typically
inside a data center or VPC, which benefits more from micro-segmentation
than perimeter-focused controls because a single compromised host has
lateral options. Introduced in Chapter 02.

**Ephemeral port** — A port in the IANA dynamic/private range
(49152–65535) automatically assigned by the operating system as the
source port of an outbound connection; never hard-coded as a destination
in a firewall rule. Introduced in Chapter 02.

**Escalation** — The deliberate handoff of an incident to broader
expertise, higher authority, or additional resources when the current
responder's tools, access, or knowledge are insufficient to continue
safely or quickly enough. Introduced in Chapter 06.

**Evidence (validation)** — The durable, capturable record of a
validation check — command output, a screenshot, a test report, or a log
excerpt — that lets someone other than the executor confirm what was
actually checked. Introduced in Chapter 05.

**Five-field flow statement** — A fixed template (source, destination,
port/protocol, direction, purpose) used to record a network traffic flow
precisely enough to write a firewall rule or security-group entry without
ambiguity. Introduced in Chapter 02.

**Four safe-administration gates** — Authorization, backup, dry run, and
rollback plan: the four conditions that convert an arbitrary
state-changing command into a safe production change, regardless of
platform. Introduced in Chapter 01.

**IANA (Internet Assigned Numbers Authority)** — The organization that
maintains the registry of well-known, registered, and dynamic TCP/UDP
port assignments referenced throughout this volume. Introduced in Chapter
02.

**Idempotent (HTTP method)** — An HTTP method (`GET`, `PUT`, `DELETE`)
whose repeated identical requests produce the same end state as a single
request, distinct from `POST`, which is not guaranteed idempotent.
Introduced in Chapter 08.

**Kerberos principal** — A Kerberos identity in the format
`<primary>/<instance>@<REALM>`, used to authenticate users and services
within a Kerberos realm such as an Active Directory domain. Introduced in
Chapter 03.

**North-south traffic** — Client-to-server network traffic that
typically crosses a perimeter or DMZ boundary, distinguished from
east-west traffic for segmentation design purposes. Introduced in Chapter
02.

**NTP stratum** — A numbered layer (0 through 15) in the Network Time
Protocol hierarchy indicating how many hops a time source is from a
reference clock; enterprises typically distribute time through an
internal stratum-2 layer rather than pointing every host at external
stratum-1 sources directly. Introduced in Chapter 03.

**Placeholder convention** — A documented syntax (`<UPPER_SNAKE_CASE>`,
`{{ jinja_variable }}`, `${terraform_variable}`) marking a value in a
configuration template that must be supplied before the template is
usable. Introduced in Chapter 04.

**Port-less IP protocol** — A protocol such as GRE, ESP, or OSPF that
operates directly over IP using a protocol number rather than a TCP/UDP
port, and therefore cannot be permitted by a port-only firewall rule.
Introduced in Chapter 02.

**Registered port** — A port in the IANA range 1024–49151, registered by
a vendor or project but not requiring privileged binding; common for
application and management services. Introduced in Chapter 02.

**Risk (likelihood × impact)** — The formal product of how likely an
event is and how severe its consequence would be, used to plot findings
on a risk matrix and prioritize mitigation. Introduced in Chapter 07.

**Rollback plan** — A specific, tested command or procedure to return a
system to its prior state, written down before a forward change is
executed rather than improvised afterward. Introduced in Chapter 01;
formalized as a change-record field in Chapter 04.

**Service Principal Name (SPN)** — A Kerberos identifier
(`<service class>/<host>:<port>`) that maps a network service instance to
a Kerberos account, misconfiguration of which is a documented Active
Directory privilege-escalation path. Introduced in Chapter 03.

**Severity classification** — A rating (commonly Sev 1 through Sev 4)
assigned to an incident based on observed business/user impact and scope,
independent of suspected root cause. Introduced in Chapter 06.

**Template (configuration)** — A parameterized document that produces a
concrete configuration when combined with variable values, making
configuration reproducible across hosts, devices, or environments.
Introduced in Chapter 04.

**Tiered change formality** — The design principle that a change record's
required rigor (approval, evidence, rollback testing) should scale with
the Command Tiering (Tier 0–3) or severity of the change rather than
being uniform for all changes. Introduced in Chapter 01; extended in
Chapter 04 and Chapter 05.

**Top-down troubleshooting** — A diagnostic methodology that starts at
the application/user-visible symptom and works downward, useful when a
symptom is specific to one application while other traffic on the same
path is known-good. Introduced in Chapter 06.

**Traffic flow** — A described unit of network communication fully
specified by source, destination, port/protocol, and direction of session
initiation; incompletely specifying any one of these is a common cause of
overly broad firewall rules. Introduced in Chapter 02.

**Unique Local Address (ULA)** — An IPv6 address in the `fc00::/7` block
(commonly `fd00::/8` in practice) used for site-local addressing that is
not globally routed, the IPv6 analog to RFC 1918 private IPv4 space.
Introduced in Chapter 03.

**User Principal Name (UPN)** — A user identity format
(`<user>@<UPN suffix>`) used by Active Directory for interactive and
service logon, distinct from but often aligned with the user's email
address. Introduced in Chapter 03.

**Waiver (checklist)** — A documented exception recorded against an
acceptance checklist item, requiring a stated reason, a compensating
control, and an approver distinct from the executor for Tier 1+ changes.
Introduced in Chapter 05.

**Webhook** — An event-driven integration mechanism in which a producer
system pushes data to a consumer's endpoint when a state change occurs,
typically delivered with an at-least-once guarantee that the consumer
must handle idempotently. Introduced in Chapter 08.

**Well-known port** — A port in the IANA range 0–1023, historically
requiring privileged binding, representing most classic services such as
SSH (22), DNS (53), and HTTPS (443). Introduced in Chapter 02.

**Zone transfer (DNS)** — The replication of an entire DNS zone from a
primary to a secondary name server (`AXFR`), which discloses complete
internal naming structure if left unrestricted to authorized secondaries
only. Introduced in Chapter 03.
