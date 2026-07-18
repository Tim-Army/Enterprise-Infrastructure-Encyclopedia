# Volume XIII Glossary

Definitions for terms introduced in **Volume XIII — Integrated Enterprise
Labs**, alphabetized. See also the [volume index](INDEX.md) for pointers
back to the chapter section each term is drawn from, and the
[master glossary](../../GLOSSARY.md) for cross-volume terminology.

**802.1X** — An IEEE port-based network access control standard requiring
a device to authenticate before a switch port grants it more than
authentication traffic, enforced in this volume against the directory
built in Chapter 02. Introduced in Chapter 07.

**Active Directory forest** — The single-domain Active Directory Domain
Services deployment (`corp.meridian.example`) that anchors identity, DNS,
Kerberos, and Group Policy for the rest of the reference lab. Introduced
in Chapter 02.

**Admission control (HA)** — A vSphere High Availability setting that
reserves enough spare cluster capacity to restart every VM from a failed
host, distinct from HA itself, which only performs the restart. Introduced
in Chapter 04.

**Blameless postmortem** — An incident review that reconstructs a timeline
and root cause from telemetry and evidence rather than participant
recollection, without assigning individual fault. Introduced in Chapter
08.

**Burn-rate alert** — An alert that fires based on how quickly a Service
Level Objective's error budget is being consumed, evaluated across
multiple time windows so it is sensitive to both sudden and slow
degradations. Introduced in Chapter 08.

**Business Impact Analysis (BIA)** — A structured assessment that assigns
each service a criticality tier and translates it into Recovery Time
Objective and Recovery Point Objective targets, performed before the
resilience exercise it informs. Introduced in Chapter 09.

**Chain of custody** — A documented, timestamped record of who captured a
piece of evidence, when, and its checksum, establishing that it has not
been altered since capture. Introduced in Chapter 07.

**Chaos engineering** — Deliberately injecting a real failure into a
system to test whether its designed resilience actually holds, run with a
bounded, reversible blast radius. Introduced in Chapter 09.

**Control Plane Policing (CoPP)** — A Cisco IOS XE feature that
rate-limits traffic destined for a device's own route processor,
protecting it from being overwhelmed by a flood or misconfiguration.
Introduced in Chapter 03.

**Default-deny VLAN ACL** — An access control list applied to a VLAN's
interface that denies all traffic except an explicit allow-list,
replacing implicit inter-VLAN trust with zero-trust segmentation.
Introduced in Chapter 07.

**DHCP failover** — A Windows Server DHCP feature allowing two servers to
share scope state, configured in this volume as load-balance (both
servers active) for one VLAN and hot-standby (one active, one idle) for
another. Introduced in Chapter 02.

**DHCP relay** — A router or switch feature (`ip helper-address`) that
forwards DHCP broadcast traffic from a client subnet to a DHCP server on a
different subnet, used to centralize DHCP administration for the BR1
site. Introduced in Chapter 03.

**Disaster recovery (DR) failover** — The process of shifting a critical
service's operation to a secondary site or system after its primary
location becomes unavailable, exercised in this volume against a full HQ
site outage. Introduced in Chapter 09.

**Error budget** — The quantity of unreliability a Service Level Objective
permits over a defined window, treated as a resource that can be
deliberately spent rather than minimized to zero. Introduced in Chapter
08.

**Evidence bundle** — The complete, checksummed set of timestamped
command transcripts a lab exercise produces, assembled from `evidence.sh`
output and intended to satisfy an external technical reviewer. Introduced
in Chapter 01.

**FSMO roles** — The five Flexible Single Master Operations roles in
Active Directory (schema master, domain naming master, PDC emulator, RID
master, infrastructure master) that must be held by exactly one domain
controller each, seized onto a recovered replica during this volume's
disaster-recovery exercise. Introduced in Chapter 09.

**HSRP (Hot Standby Router Protocol)** — A Cisco first-hop redundancy
protocol allowing two routers or Layer 3 switches to share a virtual
gateway IP address, with one active and one standby, so endpoint devices
experience no configuration change during a failover. Introduced in
Chapter 03.

**Hybrid Kubernetes cluster** — A single Kubernetes cluster with a control
plane and workers split across more than one infrastructure location —
on-premises and cloud, in this volume — connected by a hybrid network
link. Introduced in Chapter 05.

**Idempotency (automation)** — The property that re-running an automation
task produces the same end state as running it once, verified in this
volume by running the same Ansible playbook twice and confirming zero
changes on the second run. Introduced in Chapter 06.

**Incident containment** — The incident-response phase in which a
compromised or suspect system is isolated from the rest of the network, in
this volume performed by administratively shutting its switch port so
containment does not depend on the host's cooperation. Introduced in
Chapter 07.

**IPsec** — A suite of protocols providing authenticated, encrypted
tunnels between two network endpoints, used in this volume for both the
HQ–BR1 WAN link and the HQ–CLOUD1 hybrid connection. Introduced in
Chapter 03.

**Landing zone** — A pre-configured cloud environment with baseline
guardrails (network controls, tagging policy, identity boundaries)
established before any workload is deployed into it. Introduced in
Chapter 05.

**Load-balance DHCP failover** — A DHCP failover mode in which both
partner servers actively lease addresses from a shared scope
simultaneously, as opposed to hot-standby, where only one is active at a
time. Introduced in Chapter 02.

**Major incident** — A formally declared incident severity level that
triggers a dedicated response process — a bridge, an incident commander,
and a mandatory postmortem — distinct from routine incident handling.
Introduced in Chapter 08.

**Meridian Industrial Group** — The fictitious manufacturing and
logistics enterprise whose environment forms this volume's single,
continuous reference lab across all nine chapters. Introduced in Chapter
01.

**Microsegmentation** — Restricting network communication between hosts
or VLANs to an explicit allow-list rather than allowing broad reachability
within a perimeter, implemented in this volume through 802.1X and VLAN
ACLs together. Introduced in Chapter 07.

**NIST SP 800-88** — The NIST Special Publication defining Clear, Purge,
and Destroy media sanitization categories, applied in this volume's
capstone decommissioning to every disk that held domain, security, or
configuration data. Introduced in Chapter 09.

**OIDC federation (automation)** — Using OpenID Connect to exchange a
short-lived, pipeline-scoped identity token for cloud or vSphere
credentials at apply time, eliminating a standing stored credential.
Introduced in Chapter 06.

**OSPF (Open Shortest Path First)** — A link-state interior gateway
routing protocol used in this volume to route between the HQ core, the WAN
edge router, and the BR1 site router. Introduced in Chapter 03.

**Plan/apply separation** — Using a read-only identity for an
infrastructure pipeline's `plan` stage and a separate, more privileged
identity for its `apply` stage, gating write access behind human
approval. Introduced in Chapter 06.

**Policy as code** — Expressing compliance and security requirements
(mandatory tags, denied configurations) as automated rules evaluated
against an infrastructure change before it is applied, rather than
checked afterward. Introduced in Chapter 06.

**Read-only domain controller (RODC)** — A domain controller that can
authenticate users and serve DNS but cannot originate directory changes,
placed at the BR1 branch site to limit the impact of a compromised or
less physically secure location. Introduced in Chapter 03.

**Recovery Point Objective (RPO)** — The maximum acceptable amount of
data loss, measured in time, between the last good backup or replication
point and a failure. Introduced in Chapter 09.

**Recovery Time Objective (RTO)** — The maximum acceptable duration
between a failure and a service's restoration, used in this volume's
business impact analysis to set per-tier targets. Introduced in Chapter
09.

**Service Level Objective (SLO)** — An internal reliability target for a
service, measured by a Service Level Indicator, that defines the error
budget an alerting strategy is built around. Introduced in Chapter 08.

**Split-brain (HSRP)** — A failure condition in which two HSRP peers both
believe themselves to be the active router for the same group
simultaneously, typically caused by a failed peer link rather than a
genuine active-router failure. Introduced in Chapter 03.

**Topology manifest** — The versioned YAML file (`topology.yml`)
recording this volume's addressing, VLAN, and domain plan, treated as the
lab's equivalent of a production IP address management record. Introduced
in Chapter 01.

**Topology spread constraint** — A Kubernetes scheduling rule that limits
how unevenly a workload's replicas can be distributed across a labeled
dimension (such as a physical or cloud location), used in this volume to
guarantee a hybrid workload actually spans both locations rather than
landing on one by chance. Introduced in Chapter 05.

**USN rollback** — An Active Directory replication failure condition in
which a domain controller's update sequence number state conflicts with
what its replication partners expect, typically caused by restoring a
stale snapshot or backup without proper reintroduction; Active Directory
detects and halts replication when it occurs. Introduced in Chapter 09.

**vSAN** — VMware's hyperconverged storage technology that pools local
host storage into a shared cluster datastore, deployed in this volume as a
two-node cluster with a witness appliance. Introduced in Chapter 04.

**vSphere Replication** — A VMware hypervisor-level feature that
periodically replicates a VM's disk state to a target host at another
site, used in this volume to give the BR1 disaster-recovery exercise a
writable domain controller image to recover from. Introduced in Chapter
04.

**Zero trust** — A security model that removes implicit trust based on
network location alone, requiring explicit authentication and
authorization for every connection regardless of which segment it
originates from. Introduced in Chapter 07.
