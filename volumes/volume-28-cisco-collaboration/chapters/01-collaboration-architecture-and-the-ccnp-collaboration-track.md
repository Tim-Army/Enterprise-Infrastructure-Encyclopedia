# Chapter 01: Collaboration Architecture and the CCNP Collaboration Track

## Learning Objectives

- Describe the Cisco collaboration stack — call control, applications,
  edge, endpoints, and cloud — and how the pieces interlock
- Compare deployment models: on-premises, cloud (Webex), and the
  hybrid estate most enterprises actually run
- Explain the infrastructure collaboration depends on: DNS, DHCP,
  NTP, TLS certificates, and the network services that break calls
  when they break
- Design for availability: clustering, redundancy groups, and
  survivability
- Map the CCNP Collaboration track and choose a concentration
  deliberately

## Theory and Architecture

### The stack, from wire to meeting

A collaboration estate is a layered system, and every layer appears
somewhere in this volume:

| Layer | On-premises | Cloud |
| --- | --- | --- |
| Call control | Cisco Unified CM (CUCM) | Webex Calling |
| Messaging & presence | IM and Presence Service | Webex App |
| Voicemail | Unity Connection | Webex Voicemail |
| Meetings | Meeting Server (CMS) | Webex Meetings |
| Edge | Expressway C/E pair | (built into the cloud) |
| PSTN | Voice gateways, CUBE | Cloud Connected PSTN / Local Gateway |
| Contact center | UCCX/UCCE heritage | Webex Contact Center |

**Unified CM** is the on-premises center of gravity: a clustered call
agent holding device registrations, the dial plan, user data, and
feature logic. Around it: **IM and Presence** federates messaging,
**Unity Connection** answers what CUCM routes to voicemail,
**Expressway** publishes services through the DMZ without VPN, and
gateways/**CUBE** connect to the PSTN and ITSPs. The **Webex** cloud
delivers the same functions as a service, and the *hybrid* estate —
cloud meetings and messaging with on-premises calling, joined by
hybrid services and the edge — is both the common reality and the
reason CLCOR v2.0 weights Cloud and Hybrid Services at 25%.

### The infrastructure underneath

Collaboration is unsparing about network services, and CLCOR's
Infrastructure and Design domain tests exactly these dependencies:

- **DNS** — SRV records drive service discovery: `_cisco-uds` for
  Jabber/Webex App on-premises discovery, `_collab-edge` for MRA,
  `_sips._tcp` for federation. Wrong or missing SRV records are the
  first suspect in every "client cannot sign in" case.
- **DHCP** — phones learn their TFTP/configuration server from
  Option 150. No Option 150, no registration.
- **NTP** — clusters replicate and certificates validate on
  synchronized time; CUCM installation refuses un-synced clocks.
- **TLS/PKI** — every modern flow is TLS: tomcat and CallManager
  certificates, trust stores, and the expiry calendar that has taken
  down more estates than any bug. Certificate discipline is a
  first-class operational duty here.

### Availability as design

CUCM availability is layered: a **publisher** holds the writable
database, **subscribers** carry registrations and call processing;
phones register against an ordered **Unified CM Group**; and **Call
Manager redundancy** moves registrations on failure in seconds. Sites
survive WAN loss with **SRST** (a router-resident minimal call agent)
— Chapter 04 configures it. Design questions the exam and the field
both ask: which subscribers serve which devices, where does the
publisher live, what fails together, and what still works when the
data center is unreachable?

### The track

CLCOR v2.0 (120 minutes) is the core; one 90-minute concentration
completes CCNP Collaboration, and CLCOR also qualifies the CCIE
Collaboration lab. The concentrations divide by role — CLACC (call
control depth, formerly CLACCM), CLHCT (hybrid and cloud, formerly
CLCEI), CLCCE (contact center, new in 2026) — with CLICA
(applications) and CLAUTO (automation) retired in February 2026 — and
the README's alignment tables map each to this volume's chapters.

## Design Considerations

- **Follow the users, not the fashion**: estates with heavy PSTN,
  compliance recording, or analog dependencies keep on-premises call
  control longer; greenfield knowledge-worker estates start in Webex
  Calling. Most enterprises are hybrid for years — design the hybrid
  deliberately rather than accreting it.
- **Cluster placement**: centralized call processing with SRST
  branches versus distributed clusters is a WAN-reliability and
  latency decision; round-trip to the subscriber is part of every
  keypress.
- **Size the certificate operation**: multi-server SAN certificates,
  a renewal calendar with owners, and automation where the platform
  allows (Chapter 09) — decided at design time, not at first expiry.
- **DNS and DHCP are part of the collaboration design**, owned in the
  design document, not assumed from the network team.

## Implementation and Automation

The volume's lab estate begins here: CUCM publisher and one
subscriber, IM&P, and Unity Connection as VMs (DevNet's collaboration
sandbox provides the same set hosted). Foundation checks before any
call flows:

```text
# DNS: the records clients will use
dig +short SRV _cisco-uds._tcp.example.lab
dig +short SRV _collab-edge._tls.example.lab

# NTP: stratum and sync on every node (CUCM CLI)
utils ntp status

# Cluster replication: 2 = good on every node
utils dbreplication runtimestate

# Certificates: what expires, and when
show cert list own
```

```text
# DHCP Option 150 on the lab's IOS XE DHCP scope
ip dhcp pool VOICE
  network 10.50.10.0 255.255.255.0
  default-router 10.50.10.1
  option 150 ip 10.50.10.20 10.50.10.21
```

Automation enters now, as in Volume XXVII: enable AXL on CUCM and
note the API base (`https://<pub>/axl/`) — Chapter 09 drives
everything built in Chapters 03–08 through it.

## Validation and Troubleshooting

Bring-up validation follows the dependency chain: NTP synced on all
nodes, replication state 2 everywhere, DNS SRV answering, DHCP
delivering Option 150, certificates valid and trusted between nodes.
The chapter's troubleshooting habit — kept for the whole volume: when
collaboration breaks, **check the infrastructure layer first**.
Registration storms, one-way audio, sign-in failures, and federation
faults trace to DNS, certificates, NTP, or network reachability far
more often than to call-processing bugs. `utils diagnose test` on
CUCM bundles the platform's own health checks; believe it before
inventing theories.

## Security and Best Practices

- Mixed-mode/secure clusters, SIP TLS, and SRTP are Chapter 03+
  material, but the prerequisite is here: a working PKI and trust
  stores maintained like the infrastructure they are.
- Separate voice VLANs and QoS trust boundaries (Chapter 08) at
  design time.
- Administrative access: LDAP-integrated authentication, role-based
  access on the platforms, OS Administration separated from
  application administration, and every default credential rotated at
  install.

## References and Knowledge Checks

- CLCOR 350-801 v2.0 exam topics (Infrastructure and Design, 15%)
- Cisco Collaboration System Solution Reference Network Designs (SRND)
  / Preferred Architecture guides
- Cisco DevNet collaboration sandboxes

Knowledge checks:

1. A branch phone boots and never registers. Walk the dependency
   chain in order and name the check at each step.
2. Which SRV records serve on-premises discovery and MRA discovery
   respectively, and what consumes each?
3. Why does certificate expiry cause outages disproportionate to its
   apparent severity in collaboration estates?
4. Name what still works — and what does not — at an SRST branch
   during a WAN outage.

## Hands-On Lab

Stand up the volume's estate: CUCM publisher + subscriber, IM&P, and
Unity Connection (local VMs or the DevNet sandbox), with the IOS XE
DHCP scope carrying Option 150 and lab DNS carrying `_cisco-uds`.
Verify: NTP status, replication runtimestate 2 on all nodes, SRV
resolution from a client subnet, and the certificate inventory
exported to a renewal calendar with dates. Register one softphone
(Webex App or Jabber) using service discovery only — no manual server
entry — and capture the discovery flow with a packet trace showing
the SRV query and the UDS request.

## Lab Verification

Verification means the estate is replicated and time-synced, service
discovery registered the client with no manual configuration, and the
trace shows the SRV-to-UDS sequence. Until then, the lab is
unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Collaboration is a layered estate — call control, applications, edge,
cloud — standing on infrastructure that tolerates no sloppiness: DNS,
DHCP, NTP, and PKI are the first mile of every call and the first
stop of every investigation. Availability is designed in clusters,
redundancy groups, and SRST, and the CCNP Collaboration track
certifies the stack core-plus-concentration, mapped through this
volume.

- [ ] I can diagram the stack and its hybrid seams
- [ ] I can name each infrastructure dependency and its failure
      symptom
- [ ] My lab estate is replicated, synced, and discovery-registered
- [ ] I know which concentration matches my role
