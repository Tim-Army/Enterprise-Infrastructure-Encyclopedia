# Volume XIX Glossary

Definitions for terms introduced in **Volume XIX — Fortinet Network
Security**, alphabetized. See also the [volume index](INDEX.md) for
pointers back to the chapter section each term is drawn from, and the
[master glossary](../../GLOSSARY.md) for cross-volume terminology.

**Access proxy (ZTNA)** — The FortiOS construct (`config firewall
access-proxy`) that brokers every connection to a protected application
individually, rather than routing a client into a broadly trusted network
zone once a tunnel is established. Introduced in Chapter 06.

**ADOM (Administrative Domain)** — A logical grouping of FortiManager-
managed devices, commonly by business unit, region, or customer, with its
own policy packages and firmware version alignment. Introduced in
Chapter 08.

**Admin profile (accprofile)** — A named FortiOS object defining which
configuration areas an administrator account can view and/or modify,
enabling least-privilege operator accounts distinct from `super_admin`.
Introduced in Chapter 03.

**Antivirus (AV) profile** — A FortiGuard-backed security profile
(`config antivirus profile`) applying signature and heuristic malware
detection to file transfers matched by a firewall policy. Introduced in
Chapter 07.

**Application control** — A security profile type that identifies and
governs traffic by application signature rather than by port/protocol
alone, distinguishing sanctioned from unsanctioned use of the same
underlying transport. Introduced in Chapter 07.

**Automation stitch** — An on-box, event-driven automation construct
combining an `automation-trigger` (the firing condition), one or more
`automation-action` entries (the response), and an `automation-stitch`
binding them together, without requiring an external orchestrator.
Introduced in Chapter 08.

**Business email compromise (BEC)** — A targeted phishing variant
impersonating an executive or vendor to redirect a legitimate financial
transaction to an attacker-controlled account. Introduced in Chapter 01.

**Central NAT** — A FortiOS NAT architecture (`config firewall
central-snat-map`) that defines source NAT rules independently of firewall
policy, evaluated against a dedicated central table rather than embedded
in the matching policy itself. Introduced in Chapter 05.

**Certificate inspection** — An SSL inspection mode that reads only the
TLS handshake's certificate and SNI field to enforce category- and
domain-based policy, without decrypting session payload or requiring
client CA trust changes. Introduced in Chapter 07.

**Cyber kill chain** — A staged model (reconnaissance, weaponization,
delivery, exploitation, installation, command and control, actions on
objectives) describing attacker progression, used to map which defensive
technology category interrupts which stage. Introduced in Chapter 02.

**Deep inspection (full SSL inspection)** — An SSL inspection mode in
which FortiGate terminates and re-establishes the TLS session as an
authorized on-path party, restoring payload-level AV/IPS/DLP visibility at
the cost of requiring CA certificate trust distribution to every client.
Introduced in Chapter 07.

**Destination NAT (Virtual IP / VIP)** — FortiOS's implementation of
inbound NAT (`config firewall vip`), mapping an external IP and port to an
internal address, referenced as a destination object in a permitting
firewall policy. Introduced in Chapter 05.

**Device posture** — Endpoint health and compliance signals (patch level,
antivirus status, disk encryption, domain membership) reported by
FortiClient to FortiClient EMS and used to assign ZTNA tags that firewall
policy can match on. Introduced in Chapter 06.

**FGCP (FortiGate Clustering Protocol)** — FortiGate's native high-
availability clustering protocol, supporting active-passive and active-
active modes with heartbeat-based health exchange, configuration
synchronization, and session synchronization between cluster members.
Introduced in Chapter 05.

**Firewall policy** — The sequentially evaluated FortiOS rule set
(`config firewall policy`) matching traffic by source/destination
interface, address, service, schedule, and identity, applying the first
matching rule and falling through to an implicit deny if none matches.
Introduced in Chapter 06.

**FortiAnalyzer** — Fortinet's centralized logging and analytics platform,
receiving forwarded logs from FortiGate devices for retention,
correlation, and reporting beyond local device log storage. Introduced in
Chapter 08.

**FortiCare** — Fortinet's device registration and support portal, used to
associate a device serial number with FortiGuard subscriptions and TAC
support entitlement. Introduced in Chapter 04.

**FortiClient EMS (Endpoint Management Server)** — The fleet management
platform for FortiClient endpoint agents, responsible for issuing ZTNA
tags based on device posture and centrally managing endpoint
configuration. Introduced in Chapter 06.

**FortiGuard** — Fortinet's cloud-delivered threat intelligence and
content service, supplying the signature, category, and reputation data
enforced by FortiGate's antivirus, IPS, web filtering, application
control, DNS filter, and sandbox-integrated security profiles. Introduced
in Chapter 02 and detailed in Chapter 07.

**FortiManager** — Fortinet's centralized configuration and policy
management platform for a fleet of FortiGate devices, organized into
ADOMs and using reviewable policy package installation. Introduced in
Chapter 08.

**FortiSandbox** — Fortinet's file detonation and behavioral analysis
service (cloud or on-premises appliance) that analyzes unknown files and
feeds verdicts back into FortiGuard antivirus signature updates fleet-
wide. Introduced in Chapter 07.

**FortiTelemetry** — The protocol Security Fabric components use to
exchange identity, health, and configuration status with a root FortiGate,
underlying the fabric's topology and Security Rating views. Introduced in
Chapter 03.

**FortiToken** — Fortinet's hardware or mobile-app-based one-time
password token used as a phishing-resistant second factor for
administrator and VPN authentication. Introduced in Chapter 04.

**Health-check (SD-WAN Performance SLA)** — Active probing (ICMP, HTTP,
TCP, DNS, or application-aware) against defined targets that continuously
measures latency, jitter, and packet loss per SD-WAN member, driving
SLA-based path selection. Introduced in Chapter 08.

**Heartbeat interface (hbdev)** — A dedicated FGCP interface exchanging
cluster health and synchronization traffic between HA members; loss of
all heartbeat links without a corresponding data-plane loss is the classic
cause of a split-brain condition. Introduced in Chapter 05.

**Implicit deny** — The default, unconditional final rule in FortiGate's
firewall policy evaluation order that blocks any traffic no explicit
policy matched, enforcing a default-deny security posture. Introduced in
Chapter 06.

**Inter-VDOM link** — A pair of virtual interfaces, one assigned to each
of two VDOMs, functioning as the only deliberate communication path
between otherwise isolated virtual firewalls on the same physical device.
Introduced in Chapter 05.

**IP pool** — A defined address range (`config firewall ippool`) used for
policy-based source NAT, either as a shared overload (PAT) pool or a
one-to-one mapping. Introduced in Chapter 05.

**IPsec phase1/phase2** — The two negotiation stages of an IPsec tunnel:
phase1 establishes the secure management channel and peer authentication;
phase2 negotiates the security association actually protecting traffic
between defined subnets. Introduced in Chapter 06.

**IPS sensor** — A security profile (`config ips sensor`) applying
signature- and behavior-based intrusion prevention against known exploit
patterns, evaluated by severity and configurable block/monitor action.
Introduced in Chapter 07.

**Kill chain** — See *Cyber kill chain*.

**MFA fatigue (push bombing)** — An attack technique that sends repeated
multi-factor push approval requests until a target approves one out of
distraction or annoyance, distinct from a direct credential compromise.
Introduced in Chapter 01.

**NAT traversal (NAT-T)** — A mechanism (typically over UDP 4500) allowing
IPsec traffic to pass correctly through an intermediate NAT device between
VPN peers. Introduced in Chapter 06.

**NSE Training Institute** — Fortinet's eight-level (NSE 1–8) training
and certification program, spanning free awareness-level content (NSE
1–3) through hands-on administrator (NSE 4) and expert-level practical
tracks (NSE 5–8). Introduced in Chapter 01.

**Password policy** — A FortiOS configuration object (`config system
password-policy`) enforcing minimum length, character composition, and
expiration requirements on administrator account passwords. Introduced in
Chapter 04.

**Performance SLA** — See *Health-check*.

**Phishing** — A social-engineering attack delivered through a message
impersonating a trusted brand or contact, with named variants including
spear phishing (targeted), whaling (executive-targeted), smishing (SMS),
vishing (voice), business email compromise, and quishing (QR code-based).
Introduced in Chapter 01.

**Policy-based NAT** — The traditional FortiGate NAT model enabling
source NAT directly on a firewall policy (`set nat enable`), optionally
drawing from a defined IP pool. Introduced in Chapter 05.

**Policy route** — A FortiOS routing construct (`config router policy`)
that matches traffic on richer criteria than destination alone (source
address, incoming interface, protocol, port) and overrides standard
routing-table selection for matching traffic. Introduced in Chapter 05.

**Ransomware-as-a-service (RaaS)** — A criminal business model in which
ransomware operators develop and lease toolkits and negotiation
infrastructure to affiliates who conduct the actual intrusion, splitting
extortion proceeds. Introduced in Chapter 02.

**REST API (FortiOS)** — FortiGate's HTTP-based configuration
(`/api/v2/cmdb`) and monitoring (`/api/v2/monitor`) interface,
authenticated via an API administrator account and token, used for
programmatic automation. Introduced in Chapter 08.

**SD-WAN member** — An individual interface (physical WAN, IPsec tunnel,
or backup circuit) assigned to an SD-WAN zone, evaluated by SD-WAN rules
for path selection. Introduced in Chapter 08.

**SD-WAN rule (service)** — A policy (`config system sdwan` `config
service`) selecting which SD-WAN member(s) carry traffic matching defined
criteria, using a strategy such as SLA-based priority, best quality, or
load balancing. Introduced in Chapter 08.

**Security Fabric** — Fortinet's architectural model connecting security
and networking products so they share telemetry and can be centrally
orchestrated, organized around five pillars: Security-Driven Networking,
Zero Trust Access, AI-driven Security Operations, Adaptive Cloud Security,
and Open Ecosystem. Introduced in Chapter 03.

**Security Rating** — A continuously evaluated Security Fabric scorecard
checking current configuration against Fortinet-maintained best-practice
rules, grouped by severity with a specific remediation linked to each
finding. Introduced in Chapter 03.

**Social engineering** — The manipulation of a person, rather than a
system, into taking an action that benefits an attacker, typically
exploiting authority, urgency, trust, or fear/scarcity. Introduced in
Chapter 01.

**Split-brain** — An FGCP failure condition in which both cluster members
believe themselves to be primary, typically caused by complete heartbeat
link loss without a corresponding loss of data-plane connectivity.
Introduced in Chapter 05.

**Split-tunneling** — An SSL VPN or IPsec configuration in which only
traffic destined for defined internal networks traverses the VPN tunnel,
while general internet traffic exits locally at the client. Introduced in
Chapter 06.

**SSL VPN** — FortiGate's remote-access VPN technology, offered in tunnel
mode (full network-layer client access) and web mode (clientless,
browser-based access to defined internal applications). Introduced in
Chapter 06.

**Trusted host (trusthost)** — A per-administrator-account restriction
limiting which source subnets are permitted to authenticate as that
account, independent of which interfaces have administrative access
enabled. Introduced in Chapter 04.

**User group** — A FortiOS object (`config user group`) combining local
and/or remote (LDAP/RADIUS) user accounts for reference in firewall
policy, authentication rules, and VPN portal mapping. Introduced in
Chapter 06.

**VDOM (Virtual Domain)** — A logical partition of a single FortiGate into
multiple independent virtual firewalls, each with its own routing table
and policy set, isolated from other VDOMs except through an explicit
inter-VDOM link. Introduced in Chapter 05.

**Virtual MAC address** — The shared MAC/IP identity an FGCP cluster
presents on each data interface regardless of which physical member is
currently primary, avoiding the need for upstream/downstream devices to
relearn addressing on failover. Introduced in Chapter 05.

**Web filter profile** — A security profile enforcing FortiGuard
category-based access control over web destinations, referenced by
category ID and configurable per-category action. Introduced in
Chapter 07.

**Zero Trust Network Access (ZTNA)** — An access model that evaluates
identity and device posture continuously and grants access to individual
applications through a broker (access proxy) rather than granting broad
network reachability after a single point-in-time authentication, as
traditional VPN does. Introduced in Chapter 06.

**FortiLink** — The protocol and mode by which a FortiGate manages
FortiSwitch and FortiAP as extensions of its own control plane.
Introduced in Chapter 11.

**FortiSASE** — Fortinet's cloud-delivered SASE service (SWG, ZTNA,
CASB, firewall-as-a-service) for users off the branch. Introduced in
Chapter 14.

**NSE 8** — The expert tier: an NSE 8 Core practical plus one NSE 8
Specialization practical (within one year of the core), valid two
years. Introduced in Chapter 15.

**Track** — One of the four NSE specializations — Secure Networking,
Security Operations, Cloud Security, SASE — that determine which exam a
given NSE level represents. Introduced in Chapter 10.
