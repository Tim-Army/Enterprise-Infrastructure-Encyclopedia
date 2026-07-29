# Volume V Glossary

Definitions for terms introduced in **Volume V — VMware Virtualization**,
alphabetized. See also the [volume index](INDEX.md) for pointers back to
the chapter section each term is drawn from, and the
[master glossary](../../GLOSSARY.md) for cross-volume terminology.

**Acceptance level** — The trust classification (VMwareCertified,
VMwareAccepted, PartnerSupported, CommunitySupported) assigned to a VIB,
enforced against a host's configured minimum acceptance level at install
time. Introduced in Chapter 02.

**ALUA (Asymmetric Logical Unit Access)** — A SCSI standard letting a
storage array expose a LUN through multiple controllers while marking
some paths as optimized and others as non-optimized, commonly paired with
the Round Robin Path Selection Policy. Introduced in Chapter 06.

**Answer file** — A per-host set of values (such as a management IP
address) collected the first time a Host Profile is applied to a given
host, used automatically on subsequent compliance checks and
remediations. Introduced in Chapter 02.

**Auto Deploy** — A network-boot mechanism through which ESXi hosts
PXE-boot directly into a vSphere Lifecycle Manager desired-state image
supplied by vCenter Server, rather than installing to local disk in the
stateless case. Introduced in Chapter 02.

**Avi Load Balancer** — VMware's software-defined, scale-out application
delivery controller (formerly Avi Networks / NSX Advanced Load Balancer),
providing load balancing, WAF, and GSLB under centralized policy. The
subject of the VCP-AVI specialist exam (6V0-22.25). Introduced in
Chapter 17.

**BGP (Border Gateway Protocol)** — The dynamic routing protocol an NSX
Tier-0 gateway uses to peer with upstream physical routers and exchange
routes. Introduced in Chapter 11.

**Boot bank** — One of two partitions holding a complete, bootable copy of
the ESXi image, used to make upgrades and rollbacks low-risk by writing
to the inactive bank first. Introduced in Chapter 02.

**Central Control Plane (CCP)** — The NSX control-plane role, running
within the NSX Manager cluster nodes, that computes and distributes
runtime forwarding state to transport nodes and Edge nodes. Introduced in
Chapter 10.

**Cloud Builder** — The VMware Cloud Foundation appliance used for the
initial, automated bring-up of the management domain; a bring-up tool
only, not an ongoing management plane. Introduced in Chapter 01.

**Content Library** — A vCenter Server construct for publishing and
subscribing to shared VM templates, ISOs, and other content across one or
more vCenter Server instances. Introduced in Chapter 05.

**DCUI (Direct Console User Interface)** — ESXi's text-mode console used
for first-boot management network configuration and low-level recovery
when no remote management path exists. Introduced in Chapter 02.

**Distributed Firewall (DFW)** — NSX's hypervisor-kernel-enforced,
per-workload firewall, evaluated using ordered policy sections and
dynamic group membership rather than only static IP-based rules.
Introduced in Chapter 08 and extended with full rule construction in
Chapter 11.

**Distinguished Expert (VMware Certified; formerly VCDX)** — The apex of
the VMware certification hierarchy, earned by authoring a production-grade
architecture design and defending it live before a panel of existing
holders rather than by passing a written exam. There is no exam code.
Introduced in Chapter 19.

**DRS (Distributed Resource Scheduler)** — The vSphere cluster service
that balances VM placement across hosts based on resource demand,
operating at a configurable automation level and migration threshold.
Introduced in Chapter 05.

**Edge cluster (NSX)** — A pool of NSX Edge node capacity that Tier-0 and
Tier-1 gateways are deployed onto, governing gateway placement and
failover. Introduced in Chapter 10.

**Edge node (NSX)** — A VM- or bare-metal-form-factor NSX component
providing north-south connectivity and centralized services (routing
protocol peering, NAT, load balancing) between the overlay fabric and the
physical network. Introduced in Chapter 10.

**Enhanced Linked Mode (ELM)** — A vCenter Server topology joining
multiple vCenter Server instances into a shared SSO domain, licensing,
global permissions, tags, and combined inventory view. Introduced in
Chapter 03.

**ESX-OSData** — The consolidated VMFS-L partition holding scratch,
locker, and core dump data on current-generation ESXi installations,
replacing several separately sized partitions used by older releases.
Introduced in Chapter 02.

**Failures To Tolerate (FTT)** — The vSAN storage policy setting that
determines how many concurrent host, disk group, or device failures an
object can survive without data loss. Introduced in Chapter 06.

**FDM (Fault Domain Manager)** — The vSphere HA agent architecture
responsible for master/agent election and host heartbeating within an
HA-enabled cluster. Introduced in Chapter 07.

**Gateway Firewall (NSX)** — A stateful firewall enforced at an NSX
Tier-0 or Tier-1 gateway, complementing the workload-level Distributed
Firewall at the north-south boundary. Introduced in Chapter 08.

**Geneve encapsulation** — The overlay encapsulation protocol NSX uses to
carry Layer 2 traffic between Tunnel Endpoints across the physical
underlay network, independent of physical VLAN structure. Introduced in
Chapter 10.

**Hardware Support Manager** — A server vendor-supplied plugin that
integrates firmware and driver management into a vSphere Lifecycle
Manager cluster image alongside ESXi software. Introduced in Chapter 09.

**Host Profile** — A reusable configuration template extracted from a
reference ESXi host, used both to provision new hosts and to
continuously audit configuration compliance across a cluster. Introduced
in Chapter 02.

**Identity federation** — Delegating vCenter Server (or VCF-wide)
authentication entirely to an external OpenID Connect identity provider,
centralizing MFA and conditional-access policy outside the platform
itself. Introduced in Chapter 03.

**Identity source** — A configured origin (local SSO, Active Directory
over LDAPS, or identity federation) vCenter Single Sign-On authenticates
users against. Introduced in Chapter 03.

**Image profile** — A named, ordered collection of VIBs forming a
bootable ESXi image, authored with Image Builder or as a vSphere
Lifecycle Manager cluster image. Introduced in Chapter 02.

**Isolation response** — The vSphere HA setting governing what a host
does with its running VMs when it determines it is network-isolated from
the rest of the cluster. Introduced in Chapter 07.

**LACP LAG (Link Aggregation Group)** — A distributed-vSwitch-only
feature bonding multiple physical uplinks into a single logical channel
using IEEE 802.3ad/802.1AX, dynamically negotiated with a matching
physical switch configuration. Introduced in Chapter 04.

**Management domain (VCF)** — The mandatory VMware Cloud Foundation
workload domain hosting SDDC Manager, the initial vCenter Server, and the
NSX Manager cluster for the environment. Introduced in Chapter 01.

**Micro-segmentation** — Using NSX's Distributed Firewall and dynamic
security groups to enforce fine-grained, workload-level network policy
independent of physical or VLAN topology. Introduced in Chapter 08.

**N-VDS** — The legacy, separately managed NSX virtual distributed
switch used by NSX releases prior to convergence with the standard
vSphere distributed switch. Introduced in Chapter 10.

**NAT (NSX)** — Source, destination, or reflexive network address
translation configurable at an NSX Tier-0 or Tier-1 gateway. Introduced
in Chapter 11.

**Network I/O Control (NIOC)** — The distributed-vSwitch feature
governing bandwidth allocation (shares, reservations, limits) across
traffic types sharing physical uplinks. Introduced in Chapter 04.

**NFV (Network Functions Virtualization)** — The service-provider
practice of running virtualized network functions (a 4G/5G core, RAN
workloads) on a telco-grade platform built from vSphere and NSX; the
subject of the VMware Telco Cloud specialist exams. Introduced in
Chapter 20.

**NSX Group** — A dynamically populated object (by VM tag, segment
membership, or other criteria) used as the source, destination, or
Applied To scope of a Distributed Firewall rule. Introduced in Chapter 11.

**NSX Manager** — The NSX management-plane component, deployed as a
resilient three-node cluster with a virtual IP, that also hosts the
Central Control Plane role. Introduced in Chapter 10.

**PSA (Pluggable Storage Architecture)** — The VMkernel framework
managing block storage I/O path selection and failover, delegating
array-specific behavior to SATP and path selection to PSP. Introduced in
Chapter 06.

**Private Cloud Security (VCP-PCS)** — The VMware private-cloud security
discipline — vDefend Distributed Firewall and Advanced Threat Prevention,
micro-segmentation, and platform hardening — assessed by the VCP-PCS
specialist exam (6V0-21.25). Introduced in Chapter 17.

**Private VLAN (PVLAN)** — A VLAN subdivision using promiscuous,
isolated, and community port types to prevent lateral communication
between VMs that must still reach a shared gateway. Introduced in
Chapter 04.

**Proactive HA** — A vSphere HA capability that quarantines or evacuates
a host based on hardware health degradation signals, before an actual
failure occurs. Introduced in Chapter 07.

**PSP (Path Selection Policy)** — The PSA sub-plugin deciding which
physical storage path an I/O travels on; the standard options are Fixed,
Most Recently Used, and Round Robin. Introduced in Chapter 06.

**SATP (Storage Array Type Plugin)** — The PSA sub-plugin that
understands a specific storage array's failover behavior and
characteristics. Introduced in Chapter 06.

**SDDC Manager** — The VMware Cloud Foundation lifecycle-management and
orchestration layer responsible for workload domain creation, coordinated
upgrades, and day-2 fleet operations. Introduced in Chapter 01.

**Segment (NSX)** — NSX's logical switch object, backed by either an
overlay transport zone (Geneve-encapsulated) or a VLAN transport zone,
that a VM's vNIC connects to. Introduced in Chapter 11.

**Shares, reservations, and limits** — The three vSphere resource-
management controls governing relative priority under contention
(shares), guaranteed minimum allocation (reservation), and hard ceiling
(limit) for CPU and memory. Introduced in Chapter 05.

**Skyline Health Diagnostics** — A proactive vSphere/vSAN evaluation
capability, runnable connected or air-gapped, that checks an environment
against a library of known issue signatures. Introduced in Chapter 09.

**SPBM (Storage Policy-Based Management)** — The framework letting
administrators declare required storage capabilities (RAID/erasure-coding
level, encryption, IOPS) rather than manually selecting a datastore,
evaluated against VASA-reported array or vSAN capabilities. Introduced in
Chapter 06.

**SSO domain (vSphere Single Sign-On)** — The vCenter Server Appliance's
embedded identity domain issuing the SAML tokens that authenticate every
vCenter Server session. Introduced in Chapter 03.

**Standard vSwitch (VSS)** — A per-host-configured virtual switch with no
dependency on vCenter Server, contrasted with the centrally managed
distributed vSwitch (VDS). Introduced in Chapter 04.

**Support bundle** — A complete archive of relevant logs, configuration
state, and (for ESXi) an optional core dump, generated for offline
analysis or support case submission. Introduced in Chapter 09.

**Telco Cloud** — VMware's service-provider product family for running
virtualized network functions (NFV) at telco scale, covered by the 5V0
Telco Cloud specialist skills exams (Platform 5V0-36.22, NFV 5V0-37.22,
Automation 5V0-44.21). Introduced in Chapter 20.

**TEP (Tunnel Endpoint)** — The IP address a prepared NSX transport node
uses as the source or destination of Geneve-encapsulated overlay traffic
to other transport nodes. Introduced in Chapter 10.

**Tier-0 gateway (NSX)** — The top-level NSX gateway owning the boundary
between the overlay fabric and the physical network, running on Edge
nodes and peering via BGP or static routes. Introduced in Chapter 11.

**Tier-1 gateway (NSX)** — A second-tier NSX gateway beneath a Tier-0,
typically owned by a specific tenant or application, to which workload
segments attach. Introduced in Chapter 11.

**Traceflow** — An NSX diagnostic tool that injects a synthetic packet
and traces its actual path, hop by hop, through the logical topology,
including which firewall rule (if any) dropped it. Introduced in
Chapter 11.

**Transparent Page Sharing** — A memory-management technique that
deduplicates identical memory pages across VMs, salted per trust group at
current baselines rather than applied indiscriminately. Introduced in
Chapter 05.

**Transport node** — An ESXi host or NSX Edge node prepared as a
data-plane participant in the NSX overlay fabric. Introduced in
Chapter 10.

**Transport zone** — The NSX object defining which transport nodes can
participate in a given set of logical segments; overlay and VLAN
transport zone types exist. Introduced in Chapter 10.

**VAMI (vCenter Server Appliance Management Interface)** — The VCSA's own
administrative web interface (port 5480) used for appliance-level
configuration, patching, and backup/restore. Introduced in Chapter 03.

**VASA (vSphere APIs for Storage Awareness)** — The API framework through
which a storage array or vSAN reports its capabilities to vCenter Server,
feeding Storage Policy-Based Management. Introduced in Chapter 06.

**VCAP (VMware Certified Advanced Professional)** — The advanced
certification tier between VCP and Distinguished Expert, gated by a
current VCP, spanning the eight-exam VCF 9.0 role series (3V0 generation)
plus carried-over Design and Deploy exams. Introduced in Chapter 18.

**VCDX (VMware Certified Design Expert)** — The former name of the
Distinguished Expert credential; a peer-juried design defense with no
written exam code. Introduced in Chapter 19.

**VCHA (vCenter High Availability)** — A three-node (active/passive/
witness) architecture providing automated failover for the vCenter
Server Appliance itself. Introduced in Chapter 03.

**VCSA (vCenter Server Appliance)** — The Photon OS-based Linux virtual
appliance, with an embedded PostgreSQL database, that is the exclusive
current deployment form of vCenter Server. Introduced in Chapter 03.

**VI workload domain (VCF)** — A VMware Cloud Foundation workload domain,
separate from the management domain, hosting tenant/application
workloads with its own vCenter Server and optionally its own NSX
instance. Introduced in Chapter 01.

**VIB (vSphere Installation Bundle)** — The unit of packaging for ESXi
software, drivers, CIM providers, and third-party agents. Introduced in
Chapter 02.

**vLCM (vSphere Lifecycle Manager)** — The vSphere subsystem managing
ESXi patching, upgrades, and driver/firmware currency, primarily through
desired-state cluster images at the current baseline. Introduced in
Chapter 09.

**VM hardware version** — The virtual hardware compatibility level
assigned to a VM, determining which virtual devices and capabilities are
available to the guest OS. Introduced in Chapter 05.

**vMotion** — Live migration of a running VM's compute (and optionally
storage) state between hosts with no perceptible workload downtime.
Introduced in Chapter 07.

**VMFS6** — VMware's clustered file system for block storage, supporting
concurrent multi-host access through on-disk locking primitives.
Introduced in Chapter 06.

**VMware Cloud Foundation (VCF)** — The full software-defined data
center stack combining vSphere, vSAN, and NSX under SDDC Manager
orchestration, organized into a management domain and one or more VI
workload domains. Introduced in Chapter 01.

**VMware vSphere Foundation (VVF)** — A lighter SDDC bundle built on the
same vSphere and vSAN foundation as VCF, without full NSX network
virtualization or SDDC Manager-driven multi-domain lifecycle automation.
Introduced in Chapter 01.

**vSAN Express Storage Architecture (ESA)** — The current-generation vSAN
architecture using an all-NVMe, single-tier, log-structured design,
eliminating the cache/capacity tier split of the Original Storage
Architecture. Introduced in Chapter 06.

**vSAN Original Storage Architecture (OSA)** — The vSAN architecture
organizing each host's local devices into disk groups with a distinct
cache tier and capacity tier. Introduced in Chapter 06.

**vSphere Cluster Services (vCLS)** — Lightweight system VMs that
maintain DRS and other cluster-service availability independent of
vCenter Server's own uptime. Introduced in Chapter 07.

**vSphere Fault Tolerance (FT)** — A vSphere availability feature running
a continuously synchronized secondary VM instance that takes over
instantly, with no dropped connections, if the primary's host fails.
Introduced in Chapter 07.

**vSphere HA (High Availability)** — The vSphere cluster service that
automatically restarts VMs on surviving hosts after a detected host
failure, governed by admission control and isolation response policy.
Introduced in Chapter 07.

**vSphere Trust Authority** — A hardware root-of-trust attestation
architecture using a dedicated, separately administered trust
authority cluster to attest host integrity before releasing encryption
keys. Introduced in Chapter 08.

**vTPM (virtual Trusted Platform Module)** — A virtual device providing
guest-OS-level TPM 2.0 functionality (BitLocker, measured boot) to a VM,
requiring the VM's virtual disks to be encrypted. Introduced in
Chapter 08.

**vVols (vSphere Virtual Volumes)** — A storage architecture making each
virtual disk, snapshot, and swap file a native, individually addressable
object on a traditional array, accessed through a Protocol Endpoint and
managed through a VASA provider. Introduced in Chapter 06.

**Witness host (vSAN)** — A lightweight ESXi instance holding only
witness (quorum) components, not full data replicas, required by
stretched-cluster and 2-node ROBO vSAN topologies. Introduced in
Chapter 06.

**Workload domain (VCF)** — A VMware Cloud Foundation unit of capacity —
either the mandatory management domain or a VI workload domain — with
its own lifecycle managed by SDDC Manager. Introduced in Chapter 01.

**x86 virtualization** — The set of CPU and platform capabilities
(hardware-assisted virtualization extensions, memory/IOMMU features) that
a Type-1 hypervisor such as ESXi relies on to run multiple isolated guest
operating systems on shared physical hardware. Introduced in Chapter 01.
