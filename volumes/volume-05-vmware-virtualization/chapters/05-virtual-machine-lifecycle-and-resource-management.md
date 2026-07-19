# Chapter 5: Virtual Machine Lifecycle and Resource Management

## Learning Objectives

- Explain virtual machine hardware versions and identify compatibility
  constraints when moving VMs between ESXi hosts of different release levels.
- Choose the correct VM provisioning method — new VM wizard, template
  deployment, Content Library, cloning, or OVF/OVA import — for a given
  operational scenario.
- Build a guest OS customization specification and explain how it drives
  automated personalization on first boot for Windows and Linux guests.
- Apply shares, reservations, and limits correctly at both the VM and
  resource pool level, and avoid the resource pool "sibling" sizing pitfall.
- Configure DRS automation levels, migration thresholds, and VM/host
  affinity rules, and interpret a DRS cluster's VM DRS score.
- Describe how ESXi manages host memory under contention (TPS, ballooning,
  compression, host swap, and NVMe memory tiering) and how NUMA/vNUMA
  placement interacts with CPU Hot Add.
- Describe the delta-disk architecture behind VM snapshots and apply
  lifecycle practices that avoid snapshot-related outages.

## Theory and Architecture

A virtual machine in vSphere is not simply "a VM" — it is a versioned
contract between a set of virtual hardware definitions, a guest operating
system, and the ESXi host that must present that hardware faithfully. This
chapter covers the operational lifecycle of that contract: how a VM is
created, how it is personalized, how ESXi and DRS decide where its CPU and
memory demands are satisfied, and how point-in-time state (snapshots) is
managed without becoming a liability. Storage placement is introduced only
at the concept level here; the full mechanics of Storage Policy-Based
Management (SPBM) and vSAN are covered in [Chapter 6](06-vsphere-storage-and-vsan.md).

### VM hardware versions

Every VM is built against a **virtual hardware version** (sometimes called
the VM's "compatibility level"), which determines the feature set exposed to
the guest: number of virtual CPUs, maximum memory, virtual PCIe slot count,
NVMe controller support, virtual TPM availability, and more. Each ESXi
release introduces a new hardware version and continues to support running
older versions for backward compatibility. On a vSphere 9.x host, newly
created VMs default to the current hardware version tied to that release,
but a VM authored years earlier on an ESXi 7.x or 8.x host can continue
running unmodified as long as the host it lands on supports that version.

The compatibility rule that matters operationally: **a VM's hardware version
sets the ceiling on which ESXi hosts can run it.** A VM upgraded to the
latest hardware version tied to vSphere 9.x cannot be powered on by an older
host that does not understand that version — this is a one-way door in
mixed-version environments. Practical implications:

- During a phased ESXi upgrade (some hosts still on an older release, some
  freshly upgraded), do not upgrade VM hardware version until every host the
  VM might vMotion to has been upgraded.
- VM hardware version upgrades require the VM to be powered off in most
  cases, or can be scheduled for the next reboot — check the compatibility
  matrix before scripting a fleet-wide bump.
- Compatibility is set per-VM (`vSphere Client > select VM > Summary >
  VM Hardware Compatibility`, or the **Upgrade VM Compatibility** action) and
  can also be set as a cluster-wide default so newly created VMs pick up a
  target version automatically without forcing existing VMs to change.

Treat hardware version upgrades as a change-managed activity, not a
default "always latest" setting, particularly in clusters that mix hardware
generations or are mid-upgrade.

### VM creation methods

vSphere supports several provisioning paths, each suited to a different
operational pattern:

| Method | Best fit | Key characteristic |
| --- | --- | --- |
| New VM wizard | One-off VMs, lab builds, troubleshooting | Full manual control over every hardware parameter |
| VM template | Standardized golden images within one vCenter | Template is a non-power-able master copy; deploy creates independent clones |
| Content Library | Multi-site or multi-vCenter template distribution | Subscribed libraries sync templates, ISOs, and OVF items across sites |
| Cloning (VM or template) | Rapid duplication of a known-good running VM | Can clone a live VM or convert a VM directly to a template |
| OVF/OVA import | Vendor virtual appliances, cross-platform portability | Self-describing package (OVF descriptor + VMDK + manifest) |
| OVF/OVA export | Appliance distribution, backup of a VM's definition | Produces a portable package independent of the source vCenter |

A **VM template** is the traditional building block for standardized
deployment: an administrator builds a VM, installs and patches the guest OS,
strips machine-specific identifiers, and converts it to a template object,
which cannot be powered on directly. Deploying from a template creates a new
VM with its own VMDKs (full clone by default), decoupling the new VM's disk
lifecycle from the template's.

**Content Library** solves the problem of keeping templates, ISO images, and
OVF/OVA items consistent across multiple vCenter Server instances or
geographically distributed sites. A **published library** lives on one
vCenter and exposes its contents over HTTPS; **subscribed libraries** on
other vCenter instances pull (sync) that content either on a schedule or
on-demand, with an option to download content immediately or only when an
item is first deployed (thin provisioning of the sync itself). This is the
standard mechanism for distributing a validated golden image to every site
in a multi-vCenter enterprise deployment without manual file copying.

**Cloning** duplicates an existing VM (powered on or off) into a new,
independent VM. Cloning a live VM triggers a memory and disk copy comparable
in mechanism to vMotion plus a full disk copy, and is disruptive to the
source VM's I/O during the operation on busy systems — schedule accordingly.

**OVF/OVA import and export** use the Open Virtualization Format, an
industry-standard packaging format consisting of an XML descriptor (`.ovf`),
one or more virtual disk files, and a manifest for integrity verification.
An **OVA** is the same content packaged as a single tar archive. OVF/OVA is
the interchange format for third-party virtual appliances (NSX Manager
appliances themselves ship this way) and for exporting a VM's definition
independent of any specific vCenter's database.

### Guest OS customization specifications

Deploying ten VMs from the same template produces ten VMs with identical
guest identifiers — hostname, SID (Windows), machine ID, and often
IP configuration — unless something personalizes each one. A **customization
specification** in vCenter Server automates this personalization at first
boot:

- For Windows guests, the specification drives **Sysprep** (Microsoft's
  System Preparation tool), regenerating the security identifier (SID),
  setting hostname, joining a domain, and applying license/product-key
  data.
- For Linux guests, VMware Tools (or open-vm-tools) applies customization
  directly — setting hostname, network configuration, and DNS — without a
  Sysprep-equivalent step, since Linux does not carry an SID-style identity
  problem.

A customization specification is built once (`vSphere Client > Policies and
Profiles > VM Customization Specifications`) and referenced by name during
template deployment or scripted through PowerCLI. It typically defines
computer name generation (fixed, prefix-plus-clone-index, or a custom script
callback), network settings (DHCP or static with an IP pool integration),
time zone, and domain-join credentials.

```powershell
# PowerCLI: deploy a VM from a template using an existing customization spec
Connect-VIServer -Server vcenter01.corp.example

New-VM -Name "app-web-03" `
  -Template (Get-Template -Name "tmpl-rhel10-base") `
  -OSCustomizationSpec (Get-OSCustomizationSpec -Name "spec-rhel10-dhcp") `
  -ResourcePool (Get-Cluster -Name "prod-cluster-a") `
  -Datastore (Get-Datastore -Name "vsan-datastore-01")
```

This pattern is the foundation most enterprises build on before layering a
full infrastructure-as-code tool (Terraform's vSphere provider, or
Packer-built templates feeding Ansible) on top — the customization spec
handles day-zero identity, while configuration management handles everything
after first boot. Cloud-init-style personalization is standard for
Linux distributions that ship it by default (Ubuntu, and increasingly
RHEL-family images); where a guest OS supports cloud-init, it can replace or
supplement the vCenter customization specification, particularly for VMs
provisioned through Content Library OVF templates carrying a cloud-init
data source.

### Resource management fundamentals: shares, reservations, and limits

Every VM (and every resource pool) exposes three controls for CPU and memory
resource allocation:

- **Shares** — a relative priority weight (Low/Normal/High, or a custom
  numeric value) that only matters when the underlying resource is
  contended. Shares determine how contested capacity is divided
  proportionally; when no contention exists, a VM at Low shares gets exactly
  as much CPU or memory as one at High shares.
- **Reservation** — a guaranteed minimum amount of the resource, expressed
  in MHz/GHz for CPU or MB/GB for memory. A reservation is set aside for the
  VM whether or not it is actively using it, and vCenter's admission control
  will refuse to power on a VM if its reservation cannot be guaranteed from
  unreserved cluster capacity.
- **Limit** — a hard ceiling on the resource, regardless of shares or
  available capacity. A CPU limit forces the hypervisor to actively throttle
  the VM's scheduling even when the host is otherwise idle — a common,
  self-inflicted "why is this VM slow on an idle host" support case.

Setting a limit is rarely correct in production capacity planning; it
converts idle host capacity that could have helped a VM into artificially
wasted headroom. Reservations, by contrast, are the correct tool for
guaranteeing latency-sensitive or SLA-bound workloads (a database VM, or a
VM running vCLS-adjacent infrastructure) real capacity during contention.

### The resource pool sibling pitfall

Resource pools let administrators group VMs and sub-pools under an
aggregate share, reservation, and limit — visually resembling a folder
structure in the vSphere Client. This visual resemblance is the source of
the single most common resource-pool misconfiguration in the field: **shares
assigned to a resource pool are divided only among that pool's immediate
siblings** — the other resource pools and VMs at the same level directly
under the same parent — not among all VMs contained within it.

Consider a cluster with two resource pools directly under the cluster root:
`Pool-Production` (High shares, containing 40 VMs) and `Pool-Test`
(Normal shares, containing 2 VMs). During CPU contention, the 40 VMs inside
`Pool-Production` collectively receive the CPU allocation implied by "High"
— they do not each individually receive High-share treatment. If a VM is
moved directly under the cluster root (outside any pool), it competes as a
sibling against each resource pool as a single entity, which is almost
never the intended outcome. This is sometimes called the **VM-vs-pool
sibling problem**: a lone VM's shares are compared against an entire pool's
aggregate shares, not against the individual VMs inside that pool.

Design guidance that avoids this trap:

- Do not build deep, nested resource pool hierarchies to mirror
  organizational charts (a common and regretted pattern). Keep pool depth
  shallow and pool count low.
- Never place a standalone VM as a sibling of a resource pool at the cluster
  root; either give every top-level workload its own pool or avoid pools
  entirely and rely on VM-level shares plus DRS.
- Reservations set on a parent pool are shared among children by default
  (expandable reservations) unless explicitly fixed — understand which mode
  is active before assuming a child pool's reservation is hard-guaranteed
  independent of siblings.
- Prefer VM-level shares/reservations over resource pools unless there is a
  genuine need to sub-allocate capacity to a delegated team or tenant —
  resource pools exist primarily as a delegation and isolation boundary, not
  as a folder-organization convenience.

### DRS: automation levels, migration thresholds, and the DRS score

The **Distributed Resource Scheduler (DRS)** is a cluster-level feature that
continuously evaluates CPU and memory load across member hosts and uses
vMotion to rebalance VMs toward a more even distribution. DRS operates in
one of three automation levels, configured per-cluster (and overridable
per-VM):

| Automation level | Initial placement | Ongoing balancing | Operator involvement |
| --- | --- | --- | --- |
| Manual | Recommends placement | Recommends moves | Operator applies every recommendation |
| Partially Automated | Automatic | Recommends moves | Operator applies ongoing balancing moves |
| Fully Automated | Automatic | Automatic | None, subject to migration threshold |

The **migration threshold** (a five-step slider from "Conservative" to
"Aggressive") controls how large an imbalance, or how much a VM's DRS score
would improve, before DRS acts. A conservative threshold only applies moves
that are effectively mandatory (host entering maintenance mode, or affinity
rule violations); an aggressive threshold applies moves for comparatively
small predicted improvements, trading additional vMotion overhead for
tighter balance.

Modern DRS (post vSphere 7.0 Update 1 logic, retained through the 9.x
baseline) is **workload-centric**: rather than only equalizing
host-level CPU/memory utilization percentages, DRS computes a per-VM **DRS
score** (0–100%) representing how close that VM is to its ideal resource
availability, factoring in CPU readiness, memory contention (ballooning,
swapping), and cache locality effects. A cluster-wide histogram of VM DRS
scores (`vSphere Client > select cluster > Monitor > vSphere DRS > VM DRS
Score`) is the primary tool for judging whether the cluster is well-balanced
— a cluster full of hosts at even CPU utilization can still contain VMs with
poor DRS scores if that "even" utilization is itself contended.

**Predictive DRS** extends this by consuming forecast metrics from vRealize
Operations / Aria Operations (workload demand trend data) so DRS can
pre-emptively move VMs ahead of a predictable load spike (e.g., a
batch job that runs at the same time nightly) rather than reacting only
after contention is already measured.

### VM/host affinity and anti-affinity rules

DRS supports constraint rules that shape where VMs can land:

- **VM/VM affinity** — keep listed VMs together on the same host (useful for
  chatty multi-tier application pairs where inter-VM latency dominates).
- **VM/VM anti-affinity** — keep listed VMs apart on different hosts (the
  standard pattern for clustered application nodes, such as a
  three-node database cluster, so a single host failure cannot take down a
  quorum).
- **VM/Host affinity (required or preferred)** — bind VMs to a defined host
  group, commonly used for license-boundary enforcement (per-core licensed
  software restricted to specific hosts) or physical/regulatory placement
  requirements.

```powershell
# PowerCLI: create a VM/VM anti-affinity rule across three database nodes
$cluster = Get-Cluster -Name "prod-cluster-a"
$vms = Get-VM -Name "db-node-1", "db-node-2", "db-node-3"

New-DrsRule -Cluster $cluster -Name "anti-affinity-db-nodes" `
  -VM $vms -KeepTogether $false -Enabled $true
```

A **required** affinity rule is a hard constraint — DRS and even HA will not
violate it, which can prevent a VM from powering back on at all if the rule
cannot be satisfied during a host outage. A **preferred** rule is a
best-effort constraint DRS will violate rather than leave a VM unplaceable.
Understand which mode is configured before relying on a rule for a
regulatory or licensing requirement, and audit required rules whenever
cluster capacity shrinks (maintenance mode, host failure) since they can
silently prevent HA restarts.

### Memory management techniques

ESXi employs several complementary techniques to reclaim and manage host
memory, applied roughly in the order below as contention increases:

1. **Transparent Page Sharing (TPS)** — identifies memory pages with
   identical content across VMs and collapses them to a single physical
   copy, backed by copy-on-write. Since the 2014-era security disclosures
   around cross-VM information disclosure through TPS, ESXi restricts TPS
   to **intra-VM** sharing by default, with **inter-VM salting** available as
   an explicit opt-in: administrators can assign a shared `Mem.ShareForceSalting`
   salt value to a defined group of mutually trusting VMs so pages are only
   shared among VMs carrying the same salt, preserving most of TPS's memory
   savings for genuinely trusted VM groups (e.g., VMs belonging to the same
   tenant or the same golden-image fleet) without exposing the broader
   host to the original cross-tenant information-disclosure class of issue.
2. **Ballooning (vmmemctl)** — the VMware Tools balloon driver running
   inside the guest is inflated by the hypervisor, forcing the guest's own
   memory manager to page out what it considers its least-needed pages to
   its own swap/pagefile. This is the preferred first reclamation technique
   under mild contention because the guest OS chooses which pages to
   surrender, generally producing a better outcome than the hypervisor
   guessing.
3. **Memory compression** — pages that would otherwise be swapped to disk
   are first tested for compressibility and stored in a per-VM compression
   cache in host RAM if they compress well, avoiding the higher latency of a
   disk round-trip for those pages.
4. **Host swap to disk** — as a last resort under sustained, severe
   contention, ESXi swaps guest physical pages out to a `.vswp` file on
   datastore. This is the slowest and least desirable technique and its
   presence in performance data (`esxtop`, field `SWW/s`, `SWR/s`) is a clear
   signal of undersized host memory relative to committed workload.
5. **Memory tiering using NVMe** — ESXi can extend the effective memory tier
   of a host by using local NVMe capacity as a second-tier memory pool
   below DRAM, transparently to the guest, distinct from and faster than
   traditional host swap. This lets a host support a larger active memory
   footprint than its installed DRAM alone would allow, at a
   latency cost between DRAM and legacy swap, and is a capacity-planning
   lever for memory-dense consolidation ratios rather than a substitute for
   adequately sizing DRAM on latency-sensitive hosts.

Operationally, seeing ballooning activity alone is not necessarily alarming
— it indicates the reclamation system is working as designed under mild
pressure. Sustained host swapping (`.vswp` activity) or compression cache
growth trending upward over time indicates real memory undersizing that
capacity planning needs to address, not just a scheduling quirk.

### CPU scheduling and NUMA/vNUMA

Modern multi-socket hosts are **NUMA (Non-Uniform Memory Access)** systems:
each physical CPU socket has directly attached "local" memory that it can
access faster than memory attached to another socket ("remote" memory). The
ESXi CPU scheduler is NUMA-aware and tries to keep a VM's vCPUs and memory
allocation within a single NUMA node (a **wide VM** that must span multiple
nodes to fit its configured vCPU/memory size is unavoidable for
large VMs, but should be sized deliberately with node boundaries in mind
when possible).

**vNUMA** exposes the underlying physical NUMA topology to the guest OS for
VMs above a vCPU count threshold, so a NUMA-aware guest OS and application
(major RDBMS platforms, JVMs configured for NUMA affinity) can make its own
locality-aware memory allocation decisions rather than being an opaque flat
memory space to the guest kernel. vNUMA topology is computed and presented
to the guest **at boot time** based on the VM's configured vCPU count and
the host's physical topology at that moment.

This creates a well-known operational gotcha with **CPU Hot Add**: enabling
CPU Hot Add on a VM (`Edit Settings > CPU > CPU Hot Plug`) disables vNUMA
for that VM entirely, because the hypervisor cannot know in advance what
NUMA topology to present to the guest when the final vCPU count is unknown
at boot. A VM with CPU Hot Add enabled instead presents a single flat
UMA-like topology to the guest regardless of the actual physical NUMA
boundaries, which can silently degrade performance for large, NUMA-sensitive
workloads (typically large database VMs) that were assumed to be
NUMA-optimized. Do not enable CPU Hot Add on large, performance-sensitive
VMs as a matter of default convenience — treat it as a deliberate trade-off
between operational flexibility (adding vCPUs without downtime) and memory
locality performance, and prefer scheduled maintenance-window vCPU changes
for genuinely NUMA-sensitive workloads instead.

### Storage-aware placement (preview)

VM placement also has a storage dimension: which datastore, and under what
data-service guarantees (replica count, failure tolerance, encryption), a
VM's disks land on. This chapter treats storage placement only at the
concept level — a **VM storage policy** expresses the desired storage
capabilities declaratively (rather than picking a specific datastore
manually), and SPBM evaluates candidate datastores against that policy at
provisioning time. The mechanics of storage policies, vSAN's Failures To
Tolerate (FTT) settings, RAID-1 versus erasure-coded protection, and VASA
provider architecture are covered in full in Chapter 6.

### Snapshot architecture

A vSphere **snapshot** captures VM state (disk contents at a point in time,
and optionally memory state) without a full copy of the underlying virtual
disks. When a snapshot is taken, ESXi freezes the base VMDK as read-only and
creates a new **delta disk** (a sparse, redo-log-style file, historically
extension `-000001.vmdk`) that captures all writes occurring after the
snapshot point. Every subsequent snapshot adds another delta disk layered on
top of the previous one, forming a **snapshot chain**. Reads must potentially
traverse the entire chain to locate the most recent version of a given
block, so chain depth has a direct, cumulative performance cost — a VM
running on a long snapshot chain shows measurably higher read latency and
consumes more datastore I/O than the same VM with no active snapshots.

Key architectural points:

- A snapshot is **not** a backup. It has no independent existence away from
  the base disk it is chained to; if the base disk is lost or corrupted, the
  snapshot chain is lost with it.
- Snapshot memory state, when captured, is written to a `.vmsn` file and
  allows a "revert" to restore the VM to a running state matching the
  moment the snapshot was taken, rather than only a crash-consistent
  power-off state.
- **Consolidation** is the process of merging delta disks back into the base
  disk after a snapshot is deleted. Consolidation is triggered automatically
  by "Delete" and "Delete All" operations, but can fail to complete silently
  in some interrupted scenarios, leaving orphaned delta disks consuming
  datastore capacity — the vSphere Client surfaces this as a **"Consolidation
  Needed"** VM status flag that should be treated as an active alert, not
  background noise.
- Snapshots left active for extended periods are the single most common
  cause of unplanned datastore-full incidents in vSphere environments,
  because delta disk growth is driven by guest write volume and is easy to
  underestimate, especially on databases or logging-heavy VMs.

### Snapshot lifecycle best practices

- Treat snapshots as a short-lived operational tool (pre-change rollback
  point during a patch window, typically hours) rather than a
  long-term retention mechanism — backup products that use the VMware
  snapshot API create and remove their working snapshot automatically per
  backup job and should not be confused with a manually-retained snapshot.
- Avoid taking snapshots of VMs running write-intensive database workloads
  without understanding the application's own consistency requirements;
  quiesced snapshots (VSS-integrated on Windows guests) are safer for
  transactional workloads than a crash-consistent snapshot.
- Alert on snapshot age (commonly 24–72 hours as a warning threshold) and on
  snapshot chain depth, not just on datastore free space — by the time free
  space alarms fire, remediation options are already narrower.
- Never manually delete or edit `.vmdk`/`-delta.vmdk`/`.vmsn` files at the
  datastore/file-system level to "clean up" a snapshot; always use **Delete**
  or **Delete All** from the Snapshot Manager (or the equivalent API call) so
  vCenter and the VM's descriptor files remain consistent.
- Before deleting a large or old snapshot, confirm free space on the
  datastore is sufficient for consolidation — merging a delta disk
  temporarily requires additional space and can itself trigger a
  datastore-full condition if capacity is already tight.

```bash
# esxcli: inspect VM snapshot-related disk consumption from the ESXi shell
esxcli storage vmfs extent list
vmkfstools -D /vmfs/volumes/<DATASTORE>/<VM_NAME>/<VM_NAME>.vmdk
```

```powershell
# PowerCLI: report all VMs with snapshots older than 3 days
Get-VM | Get-Snapshot | Where-Object { $_.Created -lt (Get-Date).AddDays(-3) } |
  Select-Object VM, Name, Created, SizeGB | Sort-Object Created
```

## Design Considerations

- **Template strategy.** Decide between a small number of minimal,
  frequently-patched "base OS" templates (composed further by configuration
  management) versus a larger number of role-specific templates baked with
  application binaries. Minimal templates reduce patch/rebuild overhead;
  role-specific templates reduce time-to-deploy for a specific workload
  class. Most enterprises converge on minimal base templates plus
  configuration-management-driven role application.
- **Content Library sync topology.** For multi-site deployments, decide
  whether every site subscribes directly to one published library (simple,
  but WAN-dependent for sync) or whether a hub-and-spoke tier of intermediate
  publishers reduces cross-region bandwidth. Also decide sync mode
  (immediate download versus on-demand) based on site bandwidth and how
  urgently a new template version must be available at every site.
- **Resource pool usage.** Only introduce resource pools where there is a
  genuine delegation boundary (a business unit or tenant that should be
  capped or guaranteed a slice of cluster capacity independent of other
  tenants). If the goal is purely organizational grouping in the UI, use
  vSphere folders instead — folders carry no resource-allocation semantics
  and cannot trigger the sibling pitfall.
- **DRS automation level per workload class.** Fully Automated is the
  correct default for most stateless and horizontally-scaled workloads.
  Consider Partially Automated or per-VM DRS automation-level overrides for
  VMs sensitive to vMotion-induced latency blips (some real-time or
  latency-sensitive workloads) so migrations happen only with human review.
- **Affinity rule scope.** Required affinity/anti-affinity rules interact
  directly with HA admission control and maintenance-mode host evacuation.
  Before adding a required rule, model what happens to cluster capacity
  during an N-1 host-failure scenario — a required rule can turn a
  survivable failure into VMs that cannot restart.
- **Reservations versus overall cluster headroom.** Aggressive use of
  memory/CPU reservations for "important" VMs reduces the pool of
  unreserved capacity DRS and HA can use for everything else. Reserve
  deliberately and track total reserved capacity against total cluster
  capacity as a standing operational metric, not just at initial sizing
  time.
- **Snapshot retention policy as an explicit standard.** Publish and enforce
  a maximum snapshot age/count policy organization-wide (commonly enforced
  by an automated alert-and-report job) rather than relying on individual
  engineers to remember to clean up.
- **CPU Hot Add trade-off.** Decide per workload class whether operational
  flexibility (no-downtime vCPU increases) outweighs the vNUMA-disabling
  performance cost, and document the decision so it is not silently applied
  cluster-wide as a template default.

## Implementation and Automation

### Creating and deploying a template

```powershell
# PowerCLI: convert an existing, patched VM into a template
Connect-VIServer -Server vcenter01.corp.example

$vm = Get-VM -Name "golden-rhel10-master"
Stop-VM -VM $vm -Confirm:$false          # graceful guest shutdown first
Set-VM -VM $vm -ToTemplate -Confirm:$false
```

```powershell
# PowerCLI: deploy 5 VMs from the template with sequential names and a customization spec
1..5 | ForEach-Object {
  $name = "app-node-{0:D2}" -f $_
  New-VM -Name $name `
    -Template (Get-Template -Name "golden-rhel10-master") `
    -OSCustomizationSpec (Get-OSCustomizationSpec -Name "spec-rhel10-static") `
    -ResourcePool (Get-Cluster -Name "prod-cluster-a") `
    -Datastore (Get-Datastore -Name "vsan-datastore-01")
}
```

### Publishing and subscribing a Content Library

```powershell
# PowerCLI: create a published Content Library backed by a vSAN datastore
New-ContentLibrary -Name "corp-golden-images" `
  -Datastore (Get-Datastore -Name "vsan-datastore-01") `
  -Published -PublishContentOnDemand:$false
```

```powershell
# PowerCLI: subscribe a remote site's vCenter to the published library
New-ContentLibrary -Name "corp-golden-images-sub" `
  -SubscriptionUrl "https://vcenter01.corp.example/cls/vcsp/lib/<LIBRARY_ID>/lib.json" `
  -Datastore (Get-Datastore -Name "site2-vsan-datastore-01") `
  -AutomaticSync:$true
```

### Setting shares, reservations, and limits

```powershell
# PowerCLI: guarantee 4 GHz / 8 GB to a latency-sensitive VM without capping it
Get-VM -Name "db-primary-01" | Get-VMResourceConfiguration |
  Set-VMResourceConfiguration -CpuReservationMhz 4000 -MemReservationMB 8192 `
    -CpuSharesLevel High -MemSharesLevel High
```

```powershell
# PowerCLI: create a resource pool with an expandable reservation for a tenant
New-ResourcePool -Location (Get-Cluster -Name "prod-cluster-a") `
  -Name "tenant-finance" `
  -CpuSharesLevel Normal -CpuReservationMhz 8000 -CpuExpandableReservation:$true `
  -MemSharesLevel Normal -MemReservationMB 16384 -MemExpandableReservation:$true
```

### Configuring DRS automation level and migration threshold

```powershell
# PowerCLI: set a cluster to Fully Automated with a moderate migration threshold
Set-Cluster -Cluster (Get-Cluster -Name "prod-cluster-a") `
  -DrsEnabled:$true -DrsAutomationLevel FullyAutomated -Confirm:$false
```

DRS migration threshold (the 1–5 aggressiveness slider) is set through
`vSphere Client > select cluster > Configure > vSphere DRS > Edit`, and is
not exposed as a simple `Set-Cluster` parameter — script it via the
`Set-View` / `ReconfigureComputeResource_Task` API method against the
cluster's `DrsConfig.VmotionRate` property when full automation is required.

### Building a VM/Host affinity rule with host groups

```powershell
# PowerCLI: pin licensed-software VMs to a defined host group (required rule)
$cluster = Get-Cluster -Name "prod-cluster-a"
New-DrsClusterGroup -Cluster $cluster -Name "hg-oracle-licensed-hosts" `
  -VMHost (Get-VMHost -Name "esxi01.corp.example", "esxi02.corp.example")
New-DrsClusterGroup -Cluster $cluster -Name "vg-oracle-vms" `
  -VM (Get-VM -Name "ora-db-01", "ora-db-02")

New-DrsVMHostRule -Cluster $cluster -Name "rule-oracle-host-affinity" `
  -VMGroup "vg-oracle-vms" -VMHostGroup "hg-oracle-licensed-hosts" `
  -Type MustRunOn
```

### Salting Transparent Page Sharing for a trusted VM group

```bash
# ESXi advanced setting via esxcli — set a shared salt for a group of mutually trusting VMs
esxcli system settings advanced set -o /Mem/ShareForceSalting -i 2
```

```text
# In the VM's .vmx file (or via VM Advanced Configuration Parameters in the
# vSphere Client), assign the same salt value to every VM permitted to share
# pages with each other:
sched.mem.pshare.salt = "tenant-a-shared-salt-001"
```

Apply the same `sched.mem.pshare.salt` value only to VMs that share a trust
boundary (for example, VMs belonging to the same tenant, deployed from the
same golden image); never set a common salt across VMs from different
security domains.

### Reporting NUMA and CPU Hot Add status

```powershell
# PowerCLI: audit VMs with CPU Hot Add enabled (candidates for vNUMA review)
Get-VM | Where-Object { $_.ExtensionData.Config.CpuHotAddEnabled -eq $true } |
  Select-Object Name, NumCpu, MemoryGB
```

## Validation and Troubleshooting

- **Template deployment validates as unique identity.** After deploying from
  a template with a customization spec, confirm the resulting VM's guest
  hostname and (Windows) SID differ from the template and from sibling
  clones — `Get-VM -Name <NAME> | Get-VMGuest` reports hostname and IP once
  VMware Tools reports in. A stalled customization typically shows the VM
  still carrying the template's original hostname well after boot;
  check `/var/log/vmware-imc/toolsDeployPkg.log` (Linux) or
  `%WINDIR%\Panther\UnattendGC\setupact.log` (Windows) on the guest.
- **DRS score review.** `vSphere Client > select cluster > Monitor >
  vSphere DRS > VM DRS Score` should show the large majority of VMs in the
  "good" band (typically defined as 80% and above). A cluster with even
  host-level CPU/memory utilization but many VMs in a low DRS score band
  points to per-host contention DRS cannot resolve through balancing alone
  (often a single oversized "noisy neighbor" VM) rather than a DRS
  misconfiguration.
- **Affinity rule violations.** `vSphere Client > select cluster > Monitor >
  vSphere DRS > Faults` surfaces rules DRS could not satisfy, commonly
  during host maintenance-mode evacuation when a required rule's target
  host group has insufficient remaining capacity.
- **Memory reclamation diagnosis.** Use `esxtop` (press `m` for the memory
  view) and check `MCTLSZ` (balloon-driver reclaimed memory), `SWCUR`/`SWR/s`/`SWW/s`
  (host swap activity), and `ZIP/UNZIP` fields (compression activity) per
  VM. Sustained non-zero `SWR/s`/`SWW/s` values indicate genuine host memory
  undersizing, not a transient condition to ignore.
- **NUMA locality check.** `esxtop`'s memory view also exposes `NHN` (Home
  Node) and `NMIG` (NUMA migrations) columns; a VM with a rapidly changing
  home node or a home node count greater than one for a VM sized to fit a
  single node indicates the scheduler is fighting for placement, often due
  to host memory fragmentation or an oversubscribed NUMA node.
- **Snapshot consolidation check.** A VM flagged **"Consolidation Needed"**
  in the vSphere Client summary should be resolved via `right-click VM >
  Snapshots > Consolidate`, not by manually deleting delta-disk files. If
  consolidation repeatedly fails, check datastore free space first — it is
  the most common root cause.
- **Snapshot chain audit.** `Get-VM | Get-Snapshot` in PowerCLI enumerates
  all active snapshots cluster-wide; cross-reference `SizeGB` growth over
  time against expected guest write volume to catch runaway delta disks
  before a datastore-full event.

```bash
# esxcli: confirm current host memory state summary from the ESXi shell
esxcli system settings advanced list -o /Mem/ShareForceSalting
vsish -e get /memory/comprehensive
```

## Security and Best Practices

- Strip machine-specific secrets (local admin passwords, SSH host keys, API
  tokens) from golden-image templates before conversion; regenerate SSH host
  keys and any embedded credentials during first-boot customization rather
  than shipping a common key pair to every clone.
- Restrict who can edit or deploy from Content Library items using
  role-based access control — a compromised or careless Content Library
  publisher can push a backdoored golden image to every subscribed site.
- Use inter-VM TPS salting deliberately and narrowly; do not disable the
  post-2014 default protections or apply a shared salt across VMs that do
  not share a trust boundary, since doing so re-introduces the cross-VM
  memory-disclosure exposure TPS salting was designed to close.
- Avoid required VM/Host affinity rules as a substitute for proper per-core
  or per-socket licensing controls unless the rule's failure-mode impact on
  HA restart capacity has been explicitly modeled and accepted.
- Treat active snapshots as an expanded attack/exposure surface for
  data-at-rest concerns: a delta disk on an encrypted VM's datastore is
  still governed by the VM's encryption policy, but a snapshot's `.vmsn`
  memory-state file can contain sensitive in-memory data (unencrypted
  secrets, keys) if snapshot memory capture is used carelessly on
  security-sensitive VMs — restrict snapshot-with-memory operations on such
  VMs through role-based permissions.
- Set and enforce organization-wide guest customization standards (unique
  SSH host keys, unique machine SIDs, disabled default/service accounts) as
  a checklist item in the template-approval process, not an assumption.
- Audit resource pool reservations quarterly against actual cluster
  capacity; stale, oversized reservations from decommissioned tenants
  silently starve unreserved capacity available to everyone else.

## References and Knowledge Checks

**References**

- [VMware vSphere 9.x Documentation](https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/9-0.html) — *Virtual Machine Administration*
  (hardware versions, cloning, templates, Content Library).
- [VMware vSphere 9.x Documentation](https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/9-0.html) — *Resource Management* (shares,
  reservations, limits, resource pools, DRS).
- [VMware vSphere 9.x Documentation](https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/9-0.html) — *vCenter Server and Host Management*
  (guest OS customization specifications).
- [VMware Knowledge Base](https://knowledge.broadcom.com/) — Transparent Page Sharing and inter-VM salting
  guidance.
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — dated vSphere 9.x /
  NSX 4.x baseline referenced throughout this volume.
- See [Chapter 6](06-vsphere-storage-and-vsan.md) for full SPBM, vSAN, and VASA storage-policy detail.
- See [Chapter 7](07-vsphere-availability-mobility-and-cluster-services.md) for vMotion mechanics, HA admission control, and vCLS.

**Knowledge checks**

1. Why can a VM's hardware version become a blocker during a phased,
   mixed-version ESXi upgrade, and what mitigates the risk?
2. Explain, using a concrete numeric example, why a standalone VM placed as
   a sibling of a large resource pool at the cluster root produces an
   unintended share allocation.
3. What is the practical difference between how DRS responds to a
   "Conservative" versus an "Aggressive" migration threshold?
4. Why does enabling CPU Hot Add disable vNUMA for a VM, and what workload
   types are most affected by that trade-off?
5. Why is a snapshot not a substitute for a backup, architecturally?

## Hands-On Lab

**Objective:** Build a VM template, deploy a customized clone from it, apply
resource controls including a deliberately misconfigured resource pool
sibling scenario, and observe delta-disk growth through a snapshot lifecycle
— all in a nested-ESXi lab.

**Prerequisites**

- A vSphere 9.x lab environment: one vCenter Server instance managing at
  least one ESXi 9.x host (nested ESXi-in-a-VM is sufficient), with at least
  one shared or local VMFS/vSAN datastore and 16+ GB free capacity.
- PowerCLI installed and connected (`Connect-VIServer`) with a role that
  has VM creation, template, and resource-pool privileges.
- A small Linux guest ISO or an existing minimal VM to serve as the
  template source (a 2 vCPU / 2 GB RAM VM is sufficient for this lab).

**Steps**

1. Build the template source VM and confirm it boots cleanly, then shut it
   down and convert it to a template:

   ```powershell
   Connect-VIServer -Server vcenter01.lab.example
   Get-VM -Name "lab-src-01" | Stop-VM -Confirm:$false
   Get-VM -Name "lab-src-01" | Set-VM -ToTemplate -Confirm:$false
   ```

   **Expected result:** `Get-Template -Name "lab-src-01"` returns the new
   template object; the original VM object no longer appears in
   `Get-VM`.

2. Create a minimal customization specification for Linux guests with DHCP
   networking:

   ```powershell
   New-OSCustomizationSpec -Name "lab-spec-dhcp" -OSType Linux `
     -Domain "lab.example" -NamingScheme Fixed -NamingPrefix "lab-clone" `
     -Type NonPersistent
   ```

3. Deploy two clones from the template using the customization spec:

   ```powershell
   1..2 | ForEach-Object {
     New-VM -Name "lab-clone-0$_" -Template (Get-Template -Name "lab-src-01") `
       -OSCustomizationSpec (Get-OSCustomizationSpec -Name "lab-spec-dhcp") `
       -Datastore (Get-Datastore | Select-Object -First 1) `
       -ResourcePool (Get-Cluster | Select-Object -First 1) `
       -RunAsync
   }
   ```

   **Expected result:** After both tasks complete and the VMs boot,
   `Get-VM -Name "lab-clone-0*" | Get-VMGuest` reports two distinct
   hostnames (`lab-clone-01`, `lab-clone-02`), confirming customization ran.

4. Reproduce the resource pool sibling pitfall deliberately. Create one
   resource pool with High CPU shares containing both clones, then move a
   third standalone VM to be a sibling of that pool:

   ```powershell
   $cluster = Get-Cluster | Select-Object -First 1
   New-ResourcePool -Location $cluster -Name "lab-pool-high" `
     -CpuSharesLevel High
   Get-VM -Name "lab-clone-01", "lab-clone-02" |
     Move-VM -Destination (Get-ResourcePool -Name "lab-pool-high")
   ```

   **Negative test:** Generate CPU load inside `lab-clone-01`,
   `lab-clone-02`, and a third standalone VM left at the cluster root
   (e.g., `stress-ng --cpu 2 --timeout 120s` inside each guest, or any
   available CPU-load tool) simultaneously on an intentionally
   CPU-constrained lab host (reduce vCPU allocation or run this on a
   resource-limited nested host to force contention). **Expected
   result:** the standalone VM at the cluster root receives CPU
   scheduling roughly proportional to a single High-share entity
   competing against the *entire pool* as one entity — observable in
   `esxtop`'s CPU view (`%RDY` climbing disproportionately on the two
   pooled VMs relative to what their individual "High" pool-inherited
   shares would suggest) — demonstrating that the two pooled VMs are
   sharing one pool-level allocation rather than each independently
   receiving High-share treatment.

5. Take a snapshot of `lab-clone-01`, generate write activity inside the
   guest, and observe delta-disk growth:

   ```powershell
   New-Snapshot -VM "lab-clone-01" -Name "pre-change-snapshot" -Memory:$false
   ```

   Inside the guest: `dd if=/dev/urandom of=/tmp/fill.img bs=1M count=500`
   (adjust size to available lab disk space).

   ```powershell
   Get-VM -Name "lab-clone-01" | Get-Snapshot | Select-Object Name, SizeGB, Created
   ```

   **Expected result:** the snapshot's reported `SizeGB` grows to reflect
   the ~500 MB of new guest writes, confirming the delta disk — not the
   base disk — absorbed the change.

6. Consolidate and remove the snapshot:

   ```powershell
   Get-VM -Name "lab-clone-01" | Get-Snapshot -Name "pre-change-snapshot" |
     Remove-Snapshot -Confirm:$false
   ```

   **Expected result:** `Get-VM -Name "lab-clone-01" | Get-Snapshot` returns
   no results, and the VM's summary in the vSphere Client shows no
   "Consolidation Needed" flag.

7. **Cleanup:** remove the lab pool, move any remaining VMs back to the
   cluster root, delete the clones, and delete the template so the lab
   environment returns to its prior state:

   ```powershell
   Get-VM -Name "lab-clone-01", "lab-clone-02" | Stop-VM -Confirm:$false
   Get-VM -Name "lab-clone-01", "lab-clone-02" | Remove-VM -DeletePermanently -Confirm:$false
   Remove-ResourcePool -ResourcePool "lab-pool-high" -Confirm:$false
   Get-Template -Name "lab-src-01" | Remove-Template -DeletePermanently -Confirm:$false
   Get-OSCustomizationSpec -Name "lab-spec-dhcp" | Remove-OSCustomizationSpec -Confirm:$false
   ```

## Summary and Completion Checklist

VM lifecycle management in vSphere 9.x spans versioned virtual hardware
compatibility, several provisioning paths suited to different operational
patterns (templates, Content Library, cloning, OVF/OVA), and automated guest
personalization through customization specifications. Resource allocation
correctness depends on understanding shares, reservations, and limits
precisely — especially the resource pool sibling pitfall, a frequent source
of unexplained performance complaints. DRS automates placement and ongoing
balancing using a workload-centric DRS score, constrained by affinity rules
that must be modeled against HA failure scenarios. ESXi's layered memory
reclamation (TPS with salting, ballooning, compression, host swap, and NVMe
memory tiering) and NUMA/vNUMA-aware CPU scheduling govern per-VM
performance under contention, with CPU Hot Add's vNUMA trade-off a common
and avoidable performance regression. Snapshots are a delta-disk-based,
short-lived operational tool — not a backup — and require active lifecycle
management to avoid datastore-full incidents.

- [ ] Can explain the compatibility risk of upgrading VM hardware version in
      a mixed-ESXi-version cluster.
- [ ] Can select the correct VM provisioning method for a given operational
      scenario, including Content Library sync topology.
- [ ] Can configure a guest OS customization specification and verify it
      applied correctly to a deployed clone.
- [ ] Can correctly reason about resource pool share allocation and avoid
      the sibling pitfall.
- [ ] Can configure DRS automation level, migration threshold, and
      VM/Host affinity rules, and interpret DRS score data.
- [ ] Can identify each stage of ESXi memory reclamation from `esxtop`
      output and explain the CPU Hot Add / vNUMA trade-off.
- [ ] Can explain delta-disk snapshot architecture and completed the
      hands-on lab, including the sibling-pitfall negative test and cleanup.
