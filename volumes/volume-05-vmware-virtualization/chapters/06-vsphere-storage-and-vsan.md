# Chapter 6: vSphere Storage and vSAN

## Learning Objectives

- Compare VMFS6, NFS (v3 and v4.1), iSCSI, Fibre Channel/FCoE, and NVMe over
  Fabrics as vSphere datastore transports, and select correctly among them.
- Explain the Pluggable Storage Architecture (PSA), the Native Multipathing
  Plugin (NMP), and how SATP/PSP selection — including Round Robin with
  ALUA — governs multipathing behavior.
- Describe how VASA and Storage Policy-Based Management (SPBM) decouple VM
  storage requirements from manual datastore selection, and how vVols
  extends that model to array-native per-VM objects.
- Explain vSAN's disk group architecture under the Original Storage
  Architecture (OSA) and contrast it with the per-disk log-structured
  design of the vSAN Express Storage Architecture (ESA).
- Configure and reason about vSAN storage policies, including Failures To
  Tolerate (FTT) and the capacity/performance trade-offs of RAID-1 mirroring
  versus RAID-5/6 erasure coding.
- Design vSAN networking correctly, including dedicated VMkernel adapters
  and unicast cluster communication requirements.
- Choose an appropriate vSAN cluster topology — standard, stretched with a
  witness host, or 2-node ROBO — for a given availability requirement.
- Apply vSAN capacity management practices, including deduplication and
  compression trade-offs, and configure data-at-rest encryption.

## Theory and Architecture

vSphere storage falls into two broad architectural families: **traditional
shared storage**, where an external array or NAS presents block or file
storage that ESXi hosts consume as a shared datastore, and **vSAN**, where
ESXi hosts pool their own local storage devices into a single distributed
datastore with no external array required. Both remain fully supported and
common in production at the vSphere 9.x baseline; the correct choice (or
combination) depends on existing storage investment, scale, and operational
model. This chapter covers both, along with the policy-driven abstraction
layer — SPBM — that sits above either.

### Traditional datastore transports

| Transport | Protocol type | Typical use case | Notable characteristic |
| --- | --- | --- | --- |
| VMFS6 | Block, VMware clustered file system | FC/iSCSI/local block LUNs | ESXi-native file system with clustered locking |
| NFS v3 | File, IP-based | Simpler deployments, array-side dedupe/compression | No native multipathing session trunking; relies on network-layer redundancy |
| NFS v4.1 | File, IP-based | Same as v3 plus stronger security options | Supports Kerberos (`krb5`, `krb5i`) authentication and native multipathing/session trunking |
| iSCSI | Block, IP-based | Cost-effective block storage without FC fabric | Software or hardware (dependent/independent) initiator options |
| Fibre Channel / FCoE | Block, dedicated fabric or converged Ethernet | High-throughput, low-latency enterprise SAN | Requires FC HBAs/switches (or FCoE-capable CNAs and DCB-enabled switches) |
| NVMe over Fabrics (NVMe-oF) | Block, NVMe command set over RDMA/TCP/FC | Latency-sensitive, high-IOPS workloads | Transports include NVMe/FC, NVMe/RoCE v2, NVMe/TCP |

**VMFS6** is VMware's purpose-built clustered file system for block storage.
Multiple ESXi hosts can mount the same VMFS volume concurrently and safely
coordinate access through on-disk locking primitives (ATS — Atomic Test and
Set — offloaded to array hardware where supported, falling back to SCSI
reservations otherwise). VMFS6 supports automatic space reclamation
(unmap) on thin-provisioned backing LUNs, 512e/4Kn physical sector
formats, and a default block size that eliminates the block-size tiers
earlier VMFS versions required administrators to plan around.

**NFS** datastores mount as network file shares rather than block LUNs; ESXi
is an NFS client, and the array or NAS head is the NFS server. NFS v3 is
simple and broadly compatible but has no notion of multiple TCP sessions
per mount for a single datastore — path redundancy is handled at the
network layer (NIC teaming, LACP) rather than through storage-stack
multipathing. **NFS v4.1** adds session trunking (true multiple-connection
use of a single mount) and optional Kerberos-based authentication and
in-transit integrity/encryption (`krb5`/`krb5i`/`krb5p` security flavors),
making it the stronger choice where either performance scaling across
multiple network paths or authenticated/encrypted mounts are requirements.

**iSCSI** carries SCSI commands over IP. ESXi supports a software iSCSI
initiator (implemented entirely by the VMkernel networking stack),
dependent hardware iSCSI adapters (offload with configuration still bound
to a normal NIC), and independent hardware iSCSI adapters (a full HBA that
handles both networking and iSCSI processing). Software iSCSI is the most
common deployment given commodity Ethernet economics; it requires correct
VMkernel port binding to the iSCSI initiator for multipathing to function.

**Fibre Channel** remains the traditional enterprise SAN transport,
dedicated fabric switches and HBAs providing predictable, isolated,
low-latency block connectivity. **FCoE** converges FC frames onto
Data Center Bridging (DCB)-enabled Ethernet, reducing cabling but requiring
DCB-capable switching end to end; FCoE deployments have generally declined
in new-build enterprise environments in favor of either native FC (for
maximum SAN isolation) or NVMe/TCP (for converged Ethernet without DCB
complexity).

**NVMe over Fabrics** extends the low-latency, high-queue-depth NVMe command
set across a fabric rather than confining it to a local PCIe device. ESXi
supports NVMe/FC (over existing FC fabrics), NVMe/RoCE v2 (RDMA over
Converged Ethernet, requiring lossless/DCB-configured Ethernet), and
NVMe/TCP (standard IP networking, no RDMA or DCB requirement). NVMe/TCP in
particular has become the practical entry point for enterprises adopting
NVMe-oF without existing RDMA-capable network fabric, trading some latency
headroom compared to NVMe/RoCE v2 for far simpler network requirements.

### Pluggable Storage Architecture, NMP, SATP, and PSP

The **Pluggable Storage Architecture (PSA)** is the VMkernel framework that
manages I/O path selection and failover for block storage devices,
structured so third-party storage vendors can plug in their own
multipathing logic without modifying VMkernel core code. Most environments
use VMware's own **Native Multipathing Plugin (NMP)**, which itself
delegates two decisions to sub-plugins:

- **SATP (Storage Array Type Plugin)** — understands the specific
  array's failover behavior and characteristics (active/active,
  active/passive, ALUA-compliant). ESXi selects a default SATP
  automatically based on array identification strings, but a vendor's
  installation guide may call for a specific SATP override.
- **PSP (Path Selection Policy)** — decides which physical path an I/O
  travels on, given a device's SATP-reported characteristics. Three
  standard PSPs ship with ESXi: **Fixed** (always use a designated
  preferred path, failing over only on path loss), **Most Recently Used
  (MRU)** (use the last-working path, common for active/passive arrays
  without ALUA), and **Round Robin (RR)** (cycle I/O across all active
  paths in batches, the standard recommendation for modern arrays that
  support active/active or ALUA-based access).

**ALUA (Asymmetric Logical Unit Access)** is a SCSI standard letting an
array expose a LUN through multiple controllers/ports while marking some
paths as "optimized" (direct to the owning controller, lower latency) and
others as "non-optimized" (proxied through another controller). Round Robin
combined with ALUA awareness (an ALUA-aware SATP) is the standard modern
configuration: RR uses all optimized paths for load distribution while
correctly deprioritizing non-optimized paths rather than treating every
path as equal.

```bash
# esxcli: inspect current multipathing configuration for a device
esxcli storage nmp device list -d naa.<DEVICE_ID>

# esxcli: set Round Robin as the default PSP for a specific SATP class
esxcli storage nmp satp set -s VMW_SATP_ALUA -P VMW_PSP_RR

# esxcli: set the I/O operation limit (path-switch frequency) for Round Robin
esxcli storage nmp psp roundrobin deviceconfig set -d naa.<DEVICE_ID> -I 1 -t iops
```

Reducing the Round Robin I/O operation limit (`-I`) from its default of
1000 down to a smaller value such as 1 is a common, vendor-recommended
tuning step on all-flash arrays, since flash-backed paths have low enough
per-I/O latency that switching paths more frequently improves aggregate
throughput distribution — always confirm against the specific array
vendor's current guidance before changing this cluster-wide.

### VASA, SPBM, and vVols

**VASA (vSphere APIs for Storage Awareness)** is the API framework through
which a storage array (or vSAN itself) reports its capabilities —
supported RAID/erasure-coding levels, snapshot support, encryption,
replication — directly to vCenter Server through a **VASA provider** (a
software component the array vendor supplies, or vSAN's built-in provider).
This capability data feeds **Storage Policy-Based Management (SPBM)**: an
administrator defines a VM storage policy declaratively ("this VM's disks
require RAID-1 mirroring, encryption at rest, and a minimum IOPS
guarantee") rather than manually picking a specific datastore believed to
have those properties. At provisioning or reconfiguration time, SPBM
evaluates every datastore's VASA-reported capabilities against the policy
and shows only compliant datastores, and continuously reports compliance
drift afterward if underlying array capabilities or the policy itself
change.

**vSphere Virtual Volumes (vVols)** takes this a step further for
traditional array storage: rather than a VM's disks living as files inside
a VMFS datastore built on one or more large LUNs, vVols makes each virtual
disk (and each snapshot, each swap file) a native, individually addressable
object on the array itself. The architecture has three components:

- **VASA provider** — the array's control-plane API endpoint, through which
  vCenter creates, manages, and queries vVol objects.
- **Protocol Endpoint (PE)** — a small logical I/O proxy (a special LUN for
  block arrays, or a mount point for NFS-based arrays) that ESXi uses as
  the data path to reach any vVol on that array; ESXi does not mount each
  vVol individually at the protocol level.
- **Storage Container** — the array-side capacity pool a vVol datastore maps
  to, analogous to a traditional LUN/volume but sized to hold many
  individually managed vVol objects rather than one large shared file
  system.

The practical benefit of vVols is that array-native data services
(snapshots, replication, QoS) apply per-VM-disk rather than per-datastore,
and SPBM policy compliance is enforced at that same per-VM-disk granularity
— eliminating the older pattern of grouping VMs onto separate datastores
purely to segregate them by required service level.

### vSAN architecture: OSA versus ESA

**vSAN** aggregates local storage devices — SSDs, NVMe devices, and in
hybrid configurations magnetic disks — from each ESXi host in a cluster
into a single distributed, software-defined datastore, using a dedicated
cluster network for the replication and metadata traffic between hosts. Two
architectural generations exist at the vSphere 9.x baseline, and clusters
choose one at creation time (a cluster is homogeneously OSA or ESA — the
two are not intermixed within one vSAN cluster):

**Original Storage Architecture (OSA)** organizes each host's local devices
into one or more **disk groups**, each disk group consisting of exactly one
cache-tier device and one or more capacity-tier devices:

- The **cache tier** device (always flash, even in "all-flash" nomenclature
  where the capacity tier is also flash) serves as a write buffer and read
  cache. In hybrid configurations (magnetic capacity tier), the cache
  device also holds a large read cache; in all-flash configurations, the
  cache device is dedicated almost entirely to write buffering since flash
  capacity-tier read latency is already low.
- The **capacity tier** devices hold the durable data (flash in all-flash
  configurations, magnetic disks in hybrid configurations).
- Losing the cache-tier device takes the entire disk group offline (all
  capacity devices in that group become inaccessible until the group is
  rebuilt), making cache-device reliability and disk group count per host a
  deliberate failure-domain design decision, not an afterthought.

**vSAN Express Storage Architecture (ESA)** removes the cache/capacity tier
split entirely. ESA requires an all-NVMe device configuration and treats
every device as a single-tier, individually contributing storage unit using
a **log-structured file system** design: writes land in an efficient
log-structured layout across devices rather than a dedicated cache device
absorbing writes before destaging to a separate capacity tier. This
eliminates the "losing the cache device takes down the whole group" failure
mode inherent to OSA, generally improves native support for space-efficient
RAID-5/6 erasure coding performance (ESA is designed to make erasure coding
performant enough to be a default recommendation rather than a
capacity-motivated compromise), and simplifies capacity planning since
there is no separate cache-tier sizing ratio to calculate. ESA requires
compatible all-NVMe hardware and a vSAN-certified HCL configuration; OSA
remains fully supported for hybrid and existing all-flash SAS/SATA
deployments that do not meet ESA's all-NVMe hardware requirement.

| Characteristic | OSA | ESA |
| --- | --- | --- |
| Tiering model | Cache tier + capacity tier per disk group | Single tier, log-structured, per device |
| Device requirement | Hybrid (flash + magnetic) or all-flash | All-NVMe only |
| Cache device failure impact | Entire disk group offline | No single-device group dependency |
| Erasure coding performance | Usable, historically favored RAID-1 for performance-sensitive workloads | Designed to make RAID-5/6 broadly performant by default |
| Typical adoption path | Existing hardware, hybrid economics, upgraded legacy vSAN clusters | New hardware refresh cycles standardizing on all-NVMe |

### vSAN storage policies: FTT and protection levels

vSAN enforces data protection and placement through **vSAN storage
policies**, evaluated through the same SPBM framework used for traditional
array policies, with vSAN's own VASA provider reporting vSAN-specific
capabilities. The central setting is **Failures To Tolerate (FTT)**, which
determines how many concurrent host, disk group, or device failures the
object can survive without data loss, combined with a protection method:

- **RAID-1 (mirroring)** — full replica copies of data on separate hosts.
  FTT=1 with RAID-1 requires 2x raw capacity (one full mirror); FTT=2
  requires 3x. Mirroring has the lowest read/write amplification and
  the lowest rebuild-time complexity, at the cost of the highest raw
  capacity consumption.
- **RAID-5 erasure coding** — requires a minimum of 4 fault domains
  (hosts), stripes data plus parity so FTT=1 protection costs only 1.33x
  raw capacity rather than 2x.
- **RAID-6 erasure coding** — requires a minimum of 6 fault domains,
  provides FTT=2 protection at 1.5x raw capacity rather than RAID-1's 3x.

| Protection | Minimum hosts | FTT | Capacity overhead | Typical fit |
| --- | --- | --- | --- | --- |
| RAID-1 | 3 | 1 | 2.0x | Performance-sensitive workloads, smaller clusters |
| RAID-1 | 5 | 2 | 3.0x | High-availability performance-sensitive workloads |
| RAID-5 | 4 | 1 | 1.33x | Capacity-sensitive workloads, all-flash/ESA clusters |
| RAID-6 | 6 | 2 | 1.5x | Capacity-sensitive workloads needing FTT=2 |

Erasure coding trades additional write amplification and parity-calculation
overhead for substantially reduced capacity consumption. On OSA all-flash
clusters this trade-off is usually acceptable for general workloads but
still meaningfully more expensive in write I/O than mirroring for
write-intensive, latency-sensitive workloads (databases with heavy
transaction logs, for instance). On ESA clusters, the erasure-coding
performance penalty is substantially reduced by design, making RAID-5/6 a
reasonable default even for workloads that would previously have been
steered toward RAID-1 under OSA.

```powershell
# PowerCLI: create a vSAN storage policy requiring RAID-1 FTT=1
$rule = New-SpbmRuleFtt -FttType RAID-1 -FttValue 1
$ruleset = New-SpbmRuleSet -AllOfRules $rule
New-SpbmStoragePolicy -Name "vsan-raid1-ftt1" -AnyOfRuleSets $ruleset
```

```powershell
# PowerCLI: apply a storage policy to a VM's existing disks
Get-VM -Name "app-db-01" | Get-HardDisk |
  Set-SpbmEntityConfiguration -StoragePolicy (Get-SpbmStoragePolicy -Name "vsan-raid1-ftt1")
```

### vSAN networking requirements

vSAN relies entirely on the inter-host network for replica writes, witness
component traffic, and cluster metadata, making network design a first-class
part of vSAN architecture rather than an afterthought:

- Each ESXi host participating in vSAN requires a **dedicated VMkernel
  adapter** tagged for vSAN traffic (`vSphere Client > Hosts and Clusters >
  select host > Configure > VMkernel adapters > Add Networking`, enabling
  the **vSAN** traffic service on that adapter). This is distinct from the
  vMotion and management VMkernel adapters, and should ride its own
  physical uplinks or a properly bandwidth-reserved shared uplink using
  Network I/O Control, not share unmanaged bandwidth with vMotion or
  management traffic.
- vSAN cluster communication uses **unicast** (since the removal of the
  older multicast requirement several major releases ago); every host
  maintains direct unicast connections to every other host's vSAN VMkernel
  adapter rather than relying on IGMP-managed multicast groups, removing an
  entire class of multicast-misconfiguration-related vSAN partition issues
  that affected earlier vSAN deployments.
- 10 GbE is the practical minimum for all-flash OSA and any ESA
  deployment; hybrid OSA deployments can function on lower bandwidth but
  will bottleneck rebuild and resync operations. Stretched-cluster
  deployments add explicit latency requirements between sites (discussed
  below) on top of the base bandwidth requirement.
- Jumbo frames (MTU 9000) are supported and can reduce CPU overhead for
  vSAN traffic, but must be configured consistently end-to-end (VMkernel
  adapter, vSwitch/distributed switch port group, and every physical
  switch port in the path) — a single MTU mismatch anywhere in that path
  causes silent packet fragmentation or loss rather than an obvious error.

```powershell
# PowerCLI: create a dedicated vSAN VMkernel adapter on a distributed switch port group
$vmhost = Get-VMHost -Name "esxi01.corp.example"
$vds = Get-VDSwitch -Name "dvs-cluster-a"
$pg = Get-VDPortgroup -VDSwitch $vds -Name "pg-vsan"

New-VMHostNetworkAdapter -VMHost $vmhost -PortGroup $pg -VirtualSwitch $vds `
  -IP "10.10.30.11" -SubnetMask "255.255.255.0" -VsanTrafficEnabled:$true
```

### vSAN cluster topologies

- **Standard cluster** — all hosts in a single site/rack sharing one
  network fault domain, the default topology and the right fit for the
  large majority of deployments. Fault domains can optionally be defined
  manually (rack awareness) so vSAN spreads replicas across defined
  physical racks rather than assuming any host is an equally independent
  failure domain.
- **Stretched cluster** — a single vSAN cluster split across two physical
  sites (data sites), each holding a mirrored copy of every object, plus a
  third, lightweight **witness host** (a dedicated ESXi instance, commonly
  virtual, hosted at a third independent location) that holds only witness
  components — metadata used to establish quorum, not full data replicas.
  A stretched cluster tolerates the loss of an entire site without data
  loss, provided the witness site remains reachable to break the tie.
  Stretched clusters have explicit round-trip latency requirements between
  the two data sites (commonly 5 ms RTT or better for the data-site
  link, with a much more relaxed bandwidth/latency requirement to the
  witness site since it carries only metadata) — this is a network design
  constraint that must be validated before committing to a stretched
  topology, not assumed.
- **2-node ROBO (Remote Office/Branch Office)** — a compact topology for
  edge or branch sites: exactly two data hosts at the remote site plus a
  witness host (typically hosted centrally, shared potentially across many
  ROBO sites from a central hub) providing quorum. This delivers
  local-site host-failure protection with minimal remote hardware, at the
  cost of the same witness-reachability dependency a stretched cluster
  has, scaled down to a single-site pair.

| Topology | Sites | Data replicas | Witness | Typical use |
| --- | --- | --- | --- | --- |
| Standard | 1 | Within-cluster per policy | Not required | Primary datacenter clusters |
| Stretched | 2 data + 1 witness | Full copy per data site | Required, third location | Metro-distance active-active DR |
| 2-node ROBO | 1 data + 1 witness | Full copy per host | Required, often centralized | Branch/edge sites |

### Capacity management, deduplication/compression, and encryption

vSAN capacity planning must account for the chosen FTT/protection overhead
(above), plus a reserved operations threshold (commonly recommending free
capacity be kept well below 100% utilization to leave room for
rebuild/resync operations following a failure or maintenance evacuation),
plus any snapshot or swap-file overhead. vSAN's capacity view
(`vSphere Client > select cluster > Configure > vSAN > vSAN Capacity`)
reports both raw and usable capacity accounting for the active policy set
across all objects.

**Deduplication and compression** are cluster-wide (all-flash-only, on both
OSA and ESA, though implemented differently) space-efficiency features:
deduplication identifies and eliminates duplicate blocks, compression
reduces the storage footprint of unique blocks. Under OSA, deduplication
operates at the disk-group level (a disk group is the dedup domain,
meaning identical blocks are only deduplicated against each other if they
land in the same disk group), which caps effective dedup ratios compared to
a cluster-wide dedup domain. ESA implements space efficiency differently,
consistent with its log-structured, per-device design, generally achieving
better efficiency without the disk-group-scoped limitation OSA has.
Enabling deduplication/compression trades some additional CPU and, on OSA,
some write-latency overhead for reduced capacity consumption — validate the
trade-off against workload I/O profile rather than enabling it universally
as a default.

**Data-at-rest encryption** for vSAN encrypts data as it is written to
capacity-tier devices, using keys sourced from either the built-in vSphere
Native Key Provider or an external KMIP-compliant key management server
(full key-management architecture is covered in Chapter 8). vSAN encryption
is configured cluster-wide (`vSphere Client > select cluster > Configure >
vSAN > Services > Data Services > Edit`) and operates below the
deduplication/compression layer in the I/O path in a way that preserves
space-efficiency benefits rather than defeating them — encrypting
already-deduplicated/compressed data, not encrypting first and then losing
dedup effectiveness against now-unique ciphertext.

## Design Considerations

- **Traditional array versus vSAN versus hybrid.** Existing enterprise SAN
  investment, storage team skill sets, and the need for advanced array-side
  data services (array-native replication products, certain third-party
  data-protection integrations) can favor keeping traditional shared
  storage, sometimes exposed through vVols for policy-driven per-VM
  service levels. vSAN favors organizations standardizing on
  hyperconverged, HCL-validated server hardware and wanting a single
  compute-and-storage lifecycle. Many enterprises run both concurrently for
  different cluster tiers rather than treating the decision as
  all-or-nothing.
- **OSA versus ESA at hardware-refresh time.** ESA is the forward-looking
  architecture and the natural choice for new all-NVMe hardware purchases,
  but requires validating every host against the vSAN ESA-specific HCL
  entry, not just a general vSAN HCL entry — ESA hardware qualification is
  stricter. OSA remains the correct choice where existing hybrid or
  non-NVMe all-flash hardware is still in its depreciation/support
  lifecycle.
- **Multipathing policy by array class.** Confirm the array vendor's
  current PSP/SATP recommendation before deploying — while Round Robin plus
  an ALUA-aware SATP is the common modern default, some arrays or specific
  firmware versions call for Fixed or MRU, and blindly applying Round Robin
  cluster-wide without vendor confirmation can produce non-optimized-path
  thrashing on ALUA arrays that do not tolerate it well.
- **FTT sizing against real fault-domain count.** FTT=2 with RAID-6 needs a
  minimum of 6 fault domains just to be legal, and meaningfully more to
  leave rebuild headroom after a failure — undersized clusters (exactly
  the policy's stated minimum host count) leave no room for a host to be in
  maintenance mode and a second host to fail simultaneously. Size cluster
  host count with the maintenance-mode-plus-failure scenario in mind, not
  just the bare policy minimum.
- **Stretched cluster site latency validation.** Do not commit to a
  stretched-cluster design before an actual RTT and packet-loss
  measurement between candidate sites over the intended link — marketing or
  planning-assumed metro-distance latency figures frequently do not match
  measured reality, and a stretched cluster deployed on a link that
  intermittently exceeds the supported RTT threshold produces recurring,
  hard-to-diagnose resync storms.
- **Witness host placement independence.** The witness host (stretched
  cluster or 2-node ROBO) must be genuinely independent of both data
  sites' failure domains — placing it in the same power/network failure
  domain as one of the two data sites defeats its quorum purpose entirely.
- **Deduplication ratio expectations by workload.** Homogeneous VM fleets
  built from common golden images (VDI, standardized application tiers)
  see meaningfully higher dedup ratios than heterogeneous database or
  file-server workloads; do not assume a uniform dedup ratio across a mixed
  cluster when sizing usable capacity.
- **vVols versus vSAN policy model parity.** Both use SPBM, but vVols
  policy capabilities are bounded by what the specific array's VASA
  provider actually exposes — confirm the array vendor's VASA provider
  supports the specific capability (encryption, specific RAID/erasure
  levels, replication) before designing a policy around it.

## Implementation and Automation

### Creating a VMFS6 datastore

```powershell
# PowerCLI: create a VMFS6 datastore on a presented block LUN
$vmhost = Get-VMHost -Name "esxi01.corp.example"
New-Datastore -VMHost $vmhost -Name "ds-vmfs6-tier1" `
  -Path "naa.<DEVICE_ID>" -Vmfs -FileSystemVersion 6
```

### Mounting an NFS v4.1 datastore with Kerberos

```powershell
# PowerCLI: mount an NFS v4.1 datastore using Kerberos authentication
New-Datastore -VMHost $vmhost -Name "ds-nfs41-tier2" `
  -Nfs -NfsHost "nas01.corp.example" -Path "/export/vsphere-tier2" `
  -KerberosAuthentication:$true -FileSystemVersion "4.1"
```

### Configuring the software iSCSI initiator with port binding

```bash
# esxcli: enable the software iSCSI adapter and bind a VMkernel port for multipathing
esxcli iscsi software set --enabled=true
esxcli iscsi networkportal add -A vmhba65 -n vmk1
esxcli iscsi adapter discovery sendtarget add -A vmhba65 -a 10.10.20.50:3260
esxcli storage core adapter rescan -A vmhba65
```

### Enabling vSAN on a cluster (OSA example)

```powershell
# PowerCLI: enable vSAN on an existing cluster and claim disks for a disk group
$cluster = Get-Cluster -Name "prod-cluster-vsan"
Set-Cluster -Cluster $cluster -VsanEnabled:$true -Confirm:$false

$vmhost = Get-VMHost -Location $cluster | Select-Object -First 1
New-VsanDiskGroup -VMHost $vmhost `
  -SsdCanonicalName "naa.<CACHE_DEVICE_ID>" `
  -DataDiskCanonicalName "naa.<CAPACITY_DEVICE_ID_1>", "naa.<CAPACITY_DEVICE_ID_2>"
```

### Creating and applying a vSAN RAID-5 erasure-coded policy

```powershell
# PowerCLI: create a RAID-5 FTT=1 policy for capacity-sensitive workloads
$rule = New-SpbmRuleFtt -FttType RAID-5 -FttValue 1
$ruleset = New-SpbmRuleSet -AllOfRules $rule
New-SpbmStoragePolicy -Name "vsan-raid5-ftt1" -AnyOfRuleSets $ruleset

Get-VM -Name "app-file-01" | Get-HardDisk |
  Set-SpbmEntityConfiguration -StoragePolicy (Get-SpbmStoragePolicy -Name "vsan-raid5-ftt1")
```

### Enabling deduplication, compression, and encryption

```powershell
# PowerCLI: enable dedup/compression and encryption using the vSphere Native Key Provider
Set-VsanClusterConfiguration -Cluster $cluster `
  -SpaceEfficiencyEnabled:$true -DedupCompressionState "DedupAndCompression"

Set-VsanClusterConfiguration -Cluster $cluster `
  -DataInTransitEncryption:$true `
  -KmsProviderId (Get-KmsCluster -Name "native-key-provider-01").Id
```

### Configuring a stretched cluster witness host

```powershell
# PowerCLI: configure a stretched cluster with a defined witness host
Set-VsanClusterConfiguration -Cluster $cluster -StretchedClusterEnabled:$true `
  -PreferredFaultDomain "site-a" `
  -SecondaryFaultDomain "site-b" `
  -WitnessHost (Get-VMHost -Name "witness01.corp.example")
```

## Validation and Troubleshooting

- **Multipathing state.** `esxcli storage nmp device list -d
  naa.<DEVICE_ID>` reports the active PSP, working paths, and path state
  (`active`, `active (I/O)`, `standby`, `dead`). A device showing all paths
  as `standby` except one, with frequent path-switch log entries in
  `/var/log/vmkernel.log`, indicates an ALUA misclassification or a PSP
  mismatched against the array's actual failover behavior — verify SATP
  assignment against vendor documentation.
- **VMFS heartbeat/locking issues.** Repeated
  "Lost access to volume" events with subsequent recovery in
  `/var/log/vmkernel.log` point to transient path loss or array-side
  latency spikes rather than a VMFS corruption issue in most cases; sustained
  loss instead requires a full storage-path audit (HBA firmware, switch
  zoning, array controller health) before assuming a file system problem.
- **vSAN health service.** `vSphere Client > select cluster > Monitor >
  vSAN > Skyline Health` is the first stop for any vSAN issue — it runs a
  structured battery of checks (network, physical disk, cluster,
  data) and should be clear of red/yellow findings before troubleshooting
  further at a lower level.
- **vSAN network partition diagnosis.** `esxcli vsan cluster get` on each
  host reports the cluster UUID and member count that host currently sees;
  a host reporting a different member count or a different cluster UUID
  than its peers indicates a network partition, most commonly caused by an
  MTU mismatch or a firewall/VLAN misconfiguration on the vSAN VMkernel
  network specifically.

  ```bash
  # esxcli: verify vSAN cluster membership and network health per host
  esxcli vsan cluster get
  esxcli vsan network list
  vmkping -I vmk1 -d -s 8972 <PEER_VSAN_VMKERNEL_IP>
  ```

  The `vmkping` command with `-d` (don't fragment) and `-s 8972` (a
  payload size that only succeeds end-to-end at MTU 9000) is the standard
  jumbo-frame path-MTU validation test; a failure here with success at a
  smaller size pinpoints an MTU mismatch somewhere in the path.
- **vSAN resync/rebuild monitoring.** `vSphere Client > select cluster >
  Monitor > vSAN > Resyncing Objects` shows active data movement following
  a failure, maintenance-mode evacuation, or policy change; extended
  resync duration against expected network bandwidth suggests either
  network undersizing or unexpectedly high concurrent workload I/O
  competing with resync traffic.
- **SPBM compliance drift.** `Get-VM | Get-SpbmEntityConfiguration | Where-Object
  { $_.ComplianceStatus -ne "compliant" }` in PowerCLI surfaces any VM
  object no longer meeting its assigned policy — commonly following a host
  or disk group failure that has not yet fully resynced, or a policy
  edited after initial assignment without a corresponding re-application.
- **vVols connectivity.** A vVols datastore showing as inaccessible while
  the array itself is reachable usually traces to the Protocol Endpoint
  (PE) specifically, not the storage container — confirm PE path status
  with `esxcli storage core device list` filtered to the PE device, since a
  PE outage takes down access to every vVol behind it even if the
  underlying array volumes are healthy.

## Security and Best Practices

- Enable vSAN data-at-rest encryption (and data-in-transit encryption for
  the inter-host vSAN network where supported) on any cluster handling
  regulated or sensitive data; because encryption sits below
  dedup/compression in the I/O path, enabling it after the fact does not
  require disabling space efficiency.
- Prefer the vSphere Native Key Provider only where its trust model (keys
  held within the vSphere/vCenter trust boundary) meets policy; regulated
  environments requiring separation of duties between infrastructure
  administrators and key custodians should use an external KMIP-compliant
  KMS instead — this decision is covered in depth in [Chapter 8](08-vsphere-and-nsx-security-architecture.md).
- Restrict iSCSI target and NFS export access with array-side or NAS-side
  IP/initiator allow-lists in addition to VMkernel network segmentation;
  do not rely on network segmentation alone as the only access control
  layer for storage traffic.
- Use NFS v4.1 with Kerberos (`krb5i`/`krb5p`) rather than NFS v3's
  IP-only trust model wherever the NAS platform supports it, particularly
  for datastores reachable from any network segment beyond a fully
  isolated storage VLAN.
- Segment vSAN, vMotion, iSCSI/NFS, and management traffic onto separate
  VLANs and, where practical, separate physical uplinks — do not run vSAN
  traffic across the same unmanaged uplinks as general VM traffic without
  Network I/O Control bandwidth reservations protecting it.
- Audit SPBM/vSAN storage policy compliance on a recurring schedule, not
  only after an incident; silent compliance drift (a VM running at a lower
  effective FTT than intended following an unresolved resync) is a
  data-loss-risk condition that produces no user-visible symptom until a
  second failure occurs.
- Validate array firmware and ESXi driver/firmware combinations against
  the VMware Compatibility Guide before any storage-stack change,
  particularly PSP/SATP changes — an unsupported combination can produce
  path-thrashing or data-unavailability conditions that are difficult to
  distinguish from a genuine array fault.

## References and Knowledge Checks

**References**

- [VMware vSphere 9.x Documentation](https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/9-0.html) — *Storage* (VMFS6, NFS, iSCSI, FC,
  NVMe-oF, PSA/NMP/SATP/PSP).
- [VMware vSAN 9.x (aligned to the vSphere 9.x / NSX 4.x baseline)
  Documentation](https://techdocs.broadcom.com/us/en/vmware-cis/vsan/vsan/9-0.html) — *vSAN Planning and Deployment*, *vSAN Administration*
  (OSA, ESA, storage policies, stretched clusters, 2-node ROBO).
- [VMware vSphere 9.x Documentation](https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/9-0.html) — *Storage Policy Based Management* and
  *vSphere Virtual Volumes*.
- [VMware Compatibility Guide](https://compatibilityguide.broadcom.com/) — vSAN OSA and ESA hardware qualification.
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — dated vSphere
  9.x / NSX 4.x baseline referenced throughout this volume.
- See [Chapter 5](05-virtual-machine-lifecycle-and-resource-management.md) for the conceptual introduction to VM storage policy
  placement.
- See [Chapter 8](08-vsphere-and-nsx-security-architecture.md) for full key-management-server architecture (Native Key
  Provider versus external KMIP KMS).

**Knowledge checks**

1. Why does NFS v4.1 offer a multipathing advantage NFS v3 fundamentally
   cannot, independent of network-layer redundancy?
2. Explain what ALUA describes and why Round Robin plus an ALUA-aware SATP
   is the common modern PSP/SATP pairing.
3. What single architectural change does vSAN ESA make relative to OSA
   that eliminates the "cache device failure takes down the disk group"
   failure mode?
4. Given a 4-host vSAN cluster, is RAID-6 FTT=2 legal to configure? Why or
   why not, and what does that imply about minimum viable cluster sizing
   for that protection level in practice?
5. What specific network requirement distinguishes a stretched cluster's
   data-site link from its witness-site link?

## Hands-On Lab

**Objective:** Enable vSAN on a nested-ESXi lab cluster, create and apply a
RAID-1 storage policy, deliberately violate policy compliance through a
simulated host failure, and observe resync behavior — then clean up back to
a non-vSAN state.

**Prerequisites**

- A vSphere 9.x lab with at least 3 nested ESXi hosts in one cluster, each
  presenting at least two unused virtual disks (one to serve as a cache
  device, one or more as capacity devices) not already consumed by another
  datastore. Nested ESXi VMs must have hardware virtualization exposed and
  the virtual disks marked as SSD/flash at the VM's virtual disk controller
  settings for a clean vSAN all-flash claim.
- A dedicated, routable VMkernel network (a lab VLAN or isolated
  port group) available for vSAN traffic on each host.
- PowerCLI connected to the lab vCenter with cluster-modify privileges.

**Steps**

1. Create a dedicated vSAN VMkernel adapter on each of the 3 hosts:

   ```powershell
   Connect-VIServer -Server vcenter01.lab.example
   $cluster = Get-Cluster -Name "lab-vsan-cluster"
   foreach ($vmhost in (Get-VMHost -Location $cluster)) {
     New-VMHostNetworkAdapter -VMHost $vmhost -PortGroup "pg-vsan-lab" `
       -VirtualSwitch (Get-VirtualSwitch -VMHost $vmhost -Name "vSwitch0") `
       -IP "10.10.30.1$($vmhost.Name.Substring($vmhost.Name.Length-1))" `
       -SubnetMask "255.255.255.0" -VsanTrafficEnabled:$true
   }
   ```

   **Expected result:** each host shows a new VMkernel adapter with the
   vSAN traffic service enabled under
   `vSphere Client > select host > Configure > VMkernel adapters`.

2. Enable vSAN on the cluster:

   ```powershell
   Set-Cluster -Cluster $cluster -VsanEnabled:$true -Confirm:$false
   ```

3. Claim disks and create a disk group on each host (adjust device
   identifiers to the lab's actual virtual disk `naa.` or `mpx.` identifiers,
   found via `Get-VMHostDisk` or `esxcli storage core device list`):

   ```powershell
   foreach ($vmhost in (Get-VMHost -Location $cluster)) {
     New-VsanDiskGroup -VMHost $vmhost `
       -SsdCanonicalName "<CACHE_DEVICE_ID>" `
       -DataDiskCanonicalName "<CAPACITY_DEVICE_ID>"
   }
   ```

   **Expected result:** `vSphere Client > select cluster > Configure > vSAN
   > Disk Management` shows three disk groups, one per host, all in a
   healthy (green) state, and a new vSAN datastore appears under Datastores
   with usable capacity roughly matching the sum of claimed capacity
   devices.

4. Run Skyline Health and confirm no unresolved findings:

   `vSphere Client > select cluster > Monitor > vSAN > Skyline Health >
   Retest`.

   **Expected result:** all categories report green/healthy; resolve any
   network or disk findings before proceeding.

5. Create a RAID-1 FTT=1 storage policy and deploy a small test VM using it:

   ```powershell
   $rule = New-SpbmRuleFtt -FttType RAID-1 -FttValue 1
   $ruleset = New-SpbmRuleSet -AllOfRules $rule
   New-SpbmStoragePolicy -Name "lab-vsan-raid1-ftt1" -AnyOfRuleSets $ruleset

   New-VM -Name "vsan-lab-test-vm" -ResourcePool $cluster `
     -Datastore (Get-Datastore -Name "vsanDatastore") `
     -DiskGB 10 -DiskStorageFormat Thin -NumCpu 1 -MemoryGB 1
   Get-VM -Name "vsan-lab-test-vm" | Get-HardDisk |
     Set-SpbmEntityConfiguration -StoragePolicy (Get-SpbmStoragePolicy -Name "lab-vsan-raid1-ftt1")
   ```

   **Expected result:** `Get-VM -Name "vsan-lab-test-vm" |
   Get-SpbmEntityConfiguration` reports `ComplianceStatus: compliant`.

6. **Negative test:** place one host into maintenance mode using the "No
   data migration" option (simulating an unplanned host loss rather than a
   clean evacuation) while the test VM's replica components reside partly
   on that host:

   ```powershell
   Set-VMHost -VMHost (Get-VMHost -Location $cluster | Select-Object -First 1) `
     -State Maintenance -VsanDataMigrationMode NoAction -Confirm:$false
   ```

   **Expected result:** within a few minutes, `Get-VM -Name
   "vsan-lab-test-vm" | Get-SpbmEntityConfiguration` shows
   `ComplianceStatus: nonCompliant` or `Get-VM -Name "vsan-lab-test-vm" |
   Get-VsanObject` (or the vSAN health/resyncing view in the vSphere
   Client) shows the object as reduced-redundancy, since only 2 of the
   original 3 fault domains remain reachable for a policy requiring 3.
   The VM itself should remain running and accessible (RAID-1 FTT=1
   tolerates exactly this single-host loss) — this is the expected,
   correct behavior a storage policy is designed to guarantee, but the
   compliance flag correctly signals the object is no longer protected
   against a *second* concurrent failure until the host returns.

7. Exit maintenance mode and confirm the object resyncs back to full
   compliance:

   ```powershell
   Set-VMHost -VMHost (Get-VMHost -Location $cluster | Select-Object -First 1) `
     -State Connected -Confirm:$false
   ```

   **Expected result:** `vSphere Client > select cluster > Monitor > vSAN
   > Resyncing Objects` shows active resync traffic, and
   `Get-SpbmEntityConfiguration` returns to `ComplianceStatus: compliant`
   once resync completes.

8. **Cleanup:** delete the test VM, remove the storage policy, disable
   vSAN, and remove the vSAN VMkernel adapters to return the cluster to its
   prior non-vSAN state:

   ```powershell
   Get-VM -Name "vsan-lab-test-vm" | Stop-VM -Confirm:$false
   Get-VM -Name "vsan-lab-test-vm" | Remove-VM -DeletePermanently -Confirm:$false
   Get-SpbmStoragePolicy -Name "lab-vsan-raid1-ftt1" | Remove-SpbmStoragePolicy -Confirm:$false
   Set-Cluster -Cluster $cluster -VsanEnabled:$false -Confirm:$false
   foreach ($vmhost in (Get-VMHost -Location $cluster)) {
     Get-VMHostNetworkAdapter -VMHost $vmhost -Name "vmk*" |
       Where-Object { $_.PortGroupName -eq "pg-vsan-lab" } |
       Remove-VMHostNetworkAdapter -Confirm:$false
   }
   ```

## Summary and Completion Checklist

vSphere storage spans traditional array-backed transports (VMFS6 block
storage, NFS v3/v4.1 file storage, iSCSI, Fibre Channel/FCoE, and NVMe-oF)
governed by the Pluggable Storage Architecture's NMP/SATP/PSP multipathing
model, and vSAN's hyperconverged, host-local storage pooling. VASA and SPBM
form a common policy layer above either model, letting administrators
declare required data-service capabilities rather than manually selecting
datastores, with vVols extending that per-VM-object granularity down into
traditional arrays. vSAN itself comes in two architectural generations —
OSA's cache/capacity disk-group model and ESA's simpler, all-NVMe
log-structured design — with storage policies (FTT, RAID-1 mirroring versus
RAID-5/6 erasure coding) trading capacity efficiency against write
performance and fault-domain minimums. Correct vSAN networking (a
dedicated VMkernel adapter, unicast cluster communication, validated MTU
consistency) and topology selection (standard, stretched with a witness,
or 2-node ROBO) are prerequisites for a healthy cluster, and capacity
management must account for deduplication/compression behavior and
encryption's position in the I/O path.

- [ ] Can select the correct storage transport and multipathing
      configuration (SATP/PSP) for a given array class.
- [ ] Can explain how VASA, SPBM, and vVols relate to each other and to
      traditional datastore selection.
- [ ] Can contrast vSAN OSA and ESA architecturally, including the
      cache-device failure-domain implication.
- [ ] Can size a vSAN storage policy (FTT, RAID-1/5/6) against a given
      minimum fault-domain/host-count requirement.
- [ ] Can correctly configure vSAN networking, including VMkernel adapter
      tagging and jumbo-frame validation.
- [ ] Can choose the correct vSAN cluster topology for a given
      multi-site or ROBO availability requirement.
- [ ] Completed the hands-on lab, including the maintenance-mode negative
      test and full cleanup back to a non-vSAN cluster state.
