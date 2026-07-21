# Volume XVI Glossary

Definitions for terms introduced in **Volume XVI — Palo Alto Networks
Security**, alphabetized. See also the [volume index](INDEX.md) for
pointers back to the chapter section each term is drawn from, and the
[master glossary](../../GLOSSARY.md) for cross-volume terminology.

**Active/active HA** — A high availability mode in which both firewalls in
a pair actively forward traffic simultaneously, requiring HA3
packet-forwarding logic to handle asymmetric routing. Introduced in
Chapter 04.

**Active/passive HA** — A high availability mode in which one firewall
actively forwards traffic while its peer remains synchronized in standby,
taking over automatically on a monitored failure. Introduced in Chapter 04.

**Agentless scanning** — Cortex Cloud visibility gained through a
cloud provider's API and a read-only cross-account role, without
installing software inside the workload. Introduced in Chapter 09.

**App-ID** — PAN-OS's application classification engine, identifying the
actual application in a traffic flow using signatures, protocol decoding,
and heuristics, independent of port or encryption. Introduced in
Chapter 01; extended in Chapter 05.

**Application override** — A PAN-OS policy mechanism that forces a session
to a specific application/port pairing, bypassing further App-ID and
Content-ID inspection for that session. Introduced in Chapter 05.

**Bootstrap package** — A structured set of files (`init-cfg.txt`,
`bootstrap.xml`, content, license, and software) presented to a VM-Series
instance at first boot to fully configure, license, and register it
without manual console interaction. Introduced in Chapter 03.

**BYOL (bring-your-own-license)** — A VM-Series licensing model using a
term or perpetual license activated with an auth code against a specific
serial number. Introduced in Chapter 03.

**CDSS (cloud-delivered security services)** — The family of subscription
licenses (Threat Prevention, WildFire, Advanced URL Filtering, DNS
Security, and others) that extend Content-ID's signature and
machine-learning coverage beyond the base PAN-OS license. Introduced in
Chapter 02.

**CIEM (Cloud Infrastructure Entitlement Management)** — A CNAPP
discipline that analyzes cloud IAM policy against actual permission usage
to identify unused, excessive, or toxic-combination entitlements.
Introduced in Chapter 09.

**CNAPP (cloud-native application protection platform)** — A unified
platform architecture converging CSPM, CWPP, CIEM, IaC security, API
security, and container security into a single data model and finding
set. Introduced in Chapter 09.

**Collector Group** — A Panorama construct grouping one or more Log
Collectors for redundant, load-distributed log storage independent of the
management plane's own sizing. Introduced in Chapter 06.

**Content-ID** — PAN-OS's stream-based payload inspection engine, covering
threat prevention, URL categorization, file-type control, and data
filtering as content crosses the dataplane. Introduced in Chapter 01;
extended in Chapter 05.

**Cortex Cloud** — Palo Alto Networks' cloud-native application protection
platform, the 2025 rebrand and evolution of the former standalone Prisma
Cloud product, integrated with the Cortex XSIAM/XDR data model.
Introduced in Chapter 02; covered in depth in Chapter 09.

**Cortex XDR** — A detection and response platform correlating endpoint,
network, and cloud telemetry into a single investigation timeline.
Introduced in Chapter 02.

**Cortex Xpanse** — A continuous external attack surface management (ASM)
product discovering internet-exposed assets an organization may not know
it owns. Introduced in Chapter 02.

**Cortex XSIAM** — An AI-driven security operations platform ingesting
high-volume telemetry and automating tier-1 triage, positioned to replace
a traditional SIEM-plus-SOAR stack. Introduced in Chapter 02.

**Cortex XSOAR** — A security orchestration, automation, and response
(SOAR) platform executing playbooks across third-party tools. Introduced
in Chapter 02.

**CSPM (Cloud Security Posture Management)** — A CNAPP discipline that
continuously evaluates cloud resource configuration against best-practice
and compliance frameworks. Introduced in Chapter 09.

**CWPP (Cloud Workload Protection Platform)** — A CNAPP discipline
providing runtime protection and vulnerability scanning for VMs,
containers, and serverless functions. Introduced in Chapter 09.

**Decryption CA** — The firewall-issued certificate authority used by SSL
Forward Proxy to re-sign decrypted TLS sessions presented to internal
clients, which must trust it to avoid certificate warnings. Introduced in
Chapter 05.

**Destination NAT** — Network address translation applied to a session's
destination address, commonly used to publish an internal server to a
public or partner-facing IP. Introduced in Chapter 04.

**Device group** — Panorama's unit of security, NAT, and decryption policy
management, organized in a nested hierarchy with pre-rule and post-rule
scopes. Introduced in Chapter 06.

**Dynamic IP and port (DIPP)** — A source NAT mode where many internal
hosts share one or a small pool of public IP addresses via port address
translation. Introduced in Chapter 04.

**Flexible vCPU licensing** — A pool-based, credit-consuming VM-Series
licensing model allowing instances of varying size to be deployed and
resized against a shared credit pool. Introduced in Chapter 03.

**Group mapping** — The User-ID configuration that retrieves directory
group membership via LDAP so security policy can reference a group object
rather than individual usernames. Introduced in Chapter 05.

**HA1 (control link)** — The high availability link carrying heartbeats,
configuration synchronization, and state information between HA peers.
Introduced in Chapter 04.

**HA2 (data link)** — The high availability link carrying session state
synchronization (session table, NAT translations, IPsec associations)
between HA peers. Introduced in Chapter 04.

**HA3 (packet forwarding link)** — The high availability link used in
active/active deployments to forward packets between peers for
asymmetrically routed sessions. Introduced in Chapter 04.

**IaC security scanning** — Evaluating infrastructure-as-code templates
(Terraform, CloudFormation, Kubernetes manifests) for misconfiguration
before deployment, commonly called "shift-left" security. Introduced in
Chapter 09.

**Panorama** — Palo Alto Networks' centralized management platform for
PAN-OS firewalls, providing device-group policy management, template-based
network/device configuration, software/content deployment, and log
aggregation. Introduced in Chapter 06.

**Panorama access domain** — A Panorama RBAC construct restricting which
device groups and templates a given administrator can view or modify.
Introduced in Chapter 06.

**PAN-OS REST API** — A resource-oriented API covering common
configuration objects with standard HTTP verbs and JSON payloads.
Introduced in Chapter 07.

**PAN-OS XML API** — The original, comprehensive PAN-OS/Panorama API,
supporting configuration, operational commands, commit, and log retrieval
over XML. Introduced in Chapter 07.

**PAYG (pay-as-you-go)** — A VM-Series licensing model consumed directly
from a cloud marketplace with usage-based billing, requiring no separate
Palo Alto Networks auth code for the base firewall. Introduced in
Chapter 03.

**PCNSA (Certified Network Security Administrator)** — Retired 31 January
2025. Validated day-to-day PAN-OS operation and maintenance skill;
succeeded by Network Security Analyst. Existing credentials remain valid.
Introduced in Chapter 08.

**PCNSE (Certified Network Security Engineer)** — Retired 31 July 2025.
Validated design, deployment, and troubleshooting skill across PAN-OS and
Panorama at fleet scale; succeeded by Next-Generation Firewall Engineer.
Existing credentials remain valid. Introduced in Chapter 08.

**Post-rules (Panorama)** — Device-group security, NAT, or decryption
rules evaluated after any rules configured locally on the managed
firewall, typically used for a non-bypassable catch-all rule. Introduced
in Chapter 06.

**Pre-rules (Panorama)** — Device-group security, NAT, or decryption
rules evaluated before any rules configured locally on the managed
firewall, used to enforce non-negotiable global or parent-level controls.
Introduced in Chapter 06.

**Prisma Access** — A cloud-delivered SASE product providing the NGFW
security engine and CDSS subscriptions from Palo Alto Networks' global
cloud infrastructure for remote users and branch offices. Introduced in
Chapter 02.

**Security profile group** — A named bundle of Content-ID security
profiles (Antivirus, Anti-Spyware, Vulnerability Protection, URL
Filtering, WildFire Analysis, and others) attached to a security policy
rule as a single set. Introduced in Chapter 05.

**Single-pass parallel processing (SP3)** — The PAN-OS architecture that
parses a packet once and evaluates App-ID, User-ID, and Content-ID's
scanning engines in parallel on the same normalized stream, rather than
serially as in bolt-on UTM designs. Introduced in Chapter 01.

**SSL Forward Proxy** — A PAN-OS decryption mode that terminates outbound
client TLS sessions at the firewall and re-establishes a new TLS session
to the destination, enabling Content-ID inspection of the plaintext.
Introduced in Chapter 05.

**SSL Inbound Inspection** — A PAN-OS decryption mode using an
organization's own server private key to decrypt and inspect inbound TLS
sessions to a published service, without requiring client-side trust
changes. Introduced in Chapter 05.

**Static NAT** — A one-to-one, fixed network address translation mapping,
used for a predictable public source or destination IP per host.
Introduced in Chapter 04.

**Strata Cloud Manager (SCM)** — Palo Alto Networks' cloud-delivered,
SaaS management plane providing unified visibility and increasing policy
management parity across Strata NGFWs, Prisma Access, and Prisma SD-WAN.
Introduced in Chapter 02.

**Template stack** — A Panorama construct combining multiple network/device
configuration templates in a defined priority order, pushed to a managed
firewall as its complete network/device configuration. Introduced in
Chapter 06.

**twistcli** — Cortex Cloud's command-line container image scanning tool,
used to assess vulnerability and compliance findings in a built image.
Introduced in Chapter 09.

**Unknown-tcp / unknown-udp** — The App-ID classification applied to
traffic that does not match any known application signature, warranting
investigation for either a legitimate custom protocol or evasive traffic.
Introduced in Chapter 05.

**User-ID** — PAN-OS's identity-mapping technology, associating a source
IP address (or a more granular identifier in multi-user contexts) with a
directory identity so policy can be written against users and groups.
Introduced in Chapter 01; extended in Chapter 05.

**Virtual router (VR)** — An independent PAN-OS routing instance holding
its own routing table, static routes, and dynamic routing protocol
instances, distinct from a security zone. Introduced in Chapter 04.

**Virtual wire (vWire)** — A PAN-OS interface deployment mode that binds
two interfaces transparently with no MAC/IP change and no routing,
inserting inspection into an existing segment without renumbering.
Introduced in Chapter 04.

**VM-Series** — The software form factor of PAN-OS, deployable on
hypervisors (ESXi, KVM, Hyper-V) and public clouds (AWS, Azure, GCP) using
the same App-ID/User-ID/Content-ID engine as PA-Series hardware.
Introduced in Chapter 03.

**VM auth key** — A one-time key generated on Panorama that authorizes a
VM-Series instance to register itself during bootstrap. Introduced in
Chapter 03.

**WildFire** — A cloud (or on-premises appliance) sandbox detonation
service for unknown files, feeding verdicts back to global signature
updates. Introduced in Chapter 02; applied as a security profile in
Chapter 05.

**Zero Trust** — A security strategy built on verifying explicitly, using
least-privilege access, and assuming breach, operationalized on PAN-OS by
App-ID, User-ID, and Content-ID. Introduced in Chapter 01.

**Zone (security zone)** — A logical grouping of one or more PAN-OS
interfaces sharing a trust level, used as the primary scoping dimension
for security policy evaluation. Introduced in Chapter 04.

**Zone protection profile** — A PAN-OS profile applied at the zone level
to mitigate flood, reconnaissance, and packet-based attacks independent
of and prior to security policy rule evaluation. Introduced in Chapter 04.
