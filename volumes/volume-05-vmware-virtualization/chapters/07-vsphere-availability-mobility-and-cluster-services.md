# Chapter 7: vSphere Availability, Mobility, and Cluster Services

## Learning Objectives

- Explain vSphere HA's Fault Domain Manager (FDM) architecture, including
  master/agent election, heartbeating, and isolation response behavior.
- Configure HA admission control policy correctly, including cluster
  resource percentage and slot-based policies, and reason about their
  capacity trade-offs.
- Describe compute vMotion and Storage vMotion mechanics, including
  encrypted vMotion and long-distance/cross-vCenter vMotion constraints.
- Explain vSphere Fault Tolerance's lockstep execution model and its
  current vCPU/VM scaling limits.
- Describe how DRS and HA integrate operationally, including restart
  priority, orchestrated restart dependencies, and Proactive HA.
- Explain why vSphere Cluster Services (vCLS) agent VMs exist even on
  clusters without DRS or HA actively licensed or enabled.
- Compare stretched-cluster and multi-site availability design patterns
  at a conceptual level.
- Describe, at a conceptual level, VMware's current disaster-recovery and
  replication tooling positioning.

## Theory and Architecture

Availability and mobility in vSphere rest on two distinct but tightly
coupled cluster services: **vSphere HA**, which restarts VMs elsewhere in
the cluster after a host failure, and **DRS**, introduced in Chapter 5 for
its resource-balancing role, which also governs where HA restarts land and
cooperates with HA on maintenance and hardware-health events. Layered above
both is **vMotion**, the live-migration mechanism that makes both planned
maintenance and DRS rebalancing non-disruptive. This chapter covers each of
these in turn, plus the lightweight infrastructure VMs — vCLS — that keep
cluster services functioning even in unlicensed or transiently degraded
states, and closes with a conceptual look at multi-site and
disaster-recovery patterns.

### vSphere HA architecture: FDM, master/agent election, and heartbeating

**vSphere HA** protects against host failure by restarting affected VMs on
surviving cluster hosts. Its agent, the **Fault Domain Manager (FDM)**, runs
on every HA-enabled host and replaced the older AAM (Legacy HA) agent many
releases ago; FDM is the only HA architecture relevant at the vSphere 9.x
baseline.

When HA is enabled on a cluster, the member hosts elect one **master** host;
every other host becomes a **agent** (subordinate) host. The master is
responsible for:

- Monitoring the health of all agent hosts (via network heartbeats and, as
  a secondary signal, datastore heartbeating).
- Deciding which VMs need to be restarted after a detected host failure,
  and on which surviving hosts, in coordination with DRS placement logic.
- Tracking the protected VM inventory and reporting cluster HA status to
  vCenter Server.

Election happens automatically whenever a cluster lacks a master (initial
HA enablement, or the prior master becomes unreachable), using a simple
comparison algorithm (hosts compare identifiers, and the host owning the
greatest number of connected datastores wins ties) that resolves in
seconds without administrator involvement. If vCenter Server itself is
unreachable, the existing master continues operating and can still
orchestrate restarts — HA is deliberately designed to function without a
live vCenter Server, since vCenter's own availability may depend on the
same cluster being protected.

**Network heartbeating** is the primary failure-detection mechanism: agent
hosts exchange heartbeats with the master over the management network. When
a host stops sending heartbeats, the master must distinguish between three
distinct failure modes before deciding how to respond:

- **Host failure** — the host is genuinely down (power loss, hardware
  fault). The master confirms this using additional signals (datastore
  heartbeating and network liveness checks against the isolation address)
  before triggering VM restarts elsewhere.
- **Host network isolation** — the host is still running, and the VMs on it
  are still running, but it has lost all management network connectivity to
  the rest of the cluster. The isolated host cannot reach the master or any
  peer, but its VMs may still be reachable on other networks (VM traffic
  isolated from management).
- **Network partition** — a subset of hosts can reach each other but not
  the rest of the cluster (a split cluster), distinct from a single host's
  total isolation.

**Datastore heartbeating** exists specifically to disambiguate "host
failure" from "host network isolation": the master designates a small
number of heartbeat datastores (2 by default, configurable), and an agent
host that has stopped sending network heartbeats but is still writing
liveness heartbeats to a shared datastore is classified as isolated rather
than failed — a materially different situation, since an isolated-but-alive
host is still running its VMs, and restarting them elsewhere risks running
the same VM twice (a "split-brain" condition) unless the isolation response
is configured correctly.

### Isolation response and isolation address

When a host determines it is isolated (it can no longer reach the master
or any heartbeat datastore signal path indicates isolation), it applies its
configured **host isolation response**:

- **Disabled** — leave VMs running on the isolated host. This is often
  correct if the isolation event is likely management-network-only and the
  VMs remain reachable on separate VM networks.
- **Power off and restart VMs** — hard power-off (not graceful) any running
  VMs on the isolated host, so HA on a surviving host can safely restart
  them without risking a duplicate running instance.
- **Shut down and restart VMs** — attempt a graceful in-guest shutdown
  (via VMware Tools) before HA restarts the VM elsewhere, falling back to a
  hard power-off if the guest does not shut down within a timeout.

The **isolation address** is the IP address (or addresses) a host pings to
confirm whether it is truly isolated versus merely disconnected from vCenter.
By default this is the management network's default gateway, but
administrators should configure one or more explicit isolation addresses
(`das.isolationaddress1`, `das.isolationaddress2`, …) whenever the default
gateway itself is not a reliable indicator of true network health — for
example, in a topology where the management VLAN's gateway is a single
device whose failure would falsely indicate every host is isolated
simultaneously.

### Admission control policies

**Admission control** reserves cluster capacity so that VMs that were
running on a failed host can actually be restarted elsewhere, preventing
the cluster from becoming so densely packed that HA promises capacity it
cannot deliver. vSphere HA supports several policy models:

- **Cluster resource percentage** — reserve a percentage of total cluster
  CPU and memory capacity, either specified manually or calculated
  automatically based on a configured number of host failures to tolerate
  (vCenter computes the percentage as if the largest N hosts failed
  simultaneously). This is the standard modern default and scales
  proportionally with cluster size and host heterogeneity far more cleanly
  than the older slot policy.
- **Slot policy** — computes a "slot" size (a unit of CPU and memory,
  historically derived from the largest reservation configured on any
  powered-on VM in the cluster, or a fixed administrator-defined slot size)
  and calculates how many slots the cluster can support after a defined
  number of host failures. Slot policy is more conservative — and often
  more confusing to reason about — than percentage-based policy, because a
  single VM with an unusually large CPU or memory reservation can inflate
  the slot size for the entire cluster, silently reducing the calculated
  number of failover slots available to every other VM.
- **Dedicated failover hosts** — reserve one or more specific hosts to
  remain empty during normal operation, used exclusively to receive
  restarted VMs after a failure. Simple to reason about but wastes standby
  capacity that cannot contribute to day-to-day DRS balancing.

| Policy | Sizing basis | Strength | Weakness |
| --- | --- | --- | --- |
| Cluster resource percentage | % of total cluster CPU/memory | Predictable, scales with heterogeneous hardware | Requires periodic re-validation as cluster grows/shrinks |
| Slot policy | Largest VM reservation → slot size | Conservative, guarantees exact restart capacity | One oversized reservation inflates slot size cluster-wide |
| Dedicated failover hosts | N hosts held empty | Simplest to explain/audit | Wastes standby capacity outside failure events |

Cluster resource percentage with automatically calculated values (based on
"host failures cluster tolerates" — commonly N+1 or N+2 depending on cluster
size and risk tolerance) is the standard recommendation for most modern
clusters; slot policy remains useful mainly for smaller, more homogeneous
clusters where its conservatism is an acceptable, well-understood cost.

```powershell
# PowerCLI: configure HA with cluster resource percentage admission control
$cluster = Get-Cluster -Name "prod-cluster-a"
Set-Cluster -Cluster $cluster -HAEnabled:$true -Confirm:$false

(Get-View $cluster.ExtensionData.MoRef).ReconfigureComputeResource_Task(
  (New-Object VMware.Vim.ClusterConfigSpecEx -Property @{
    dasConfig = New-Object VMware.Vim.ClusterDasConfigInfo -Property @{
      enabled = $true
      admissionControlPolicy = New-Object VMware.Vim.ClusterFailoverResourcesAdmissionControlPolicy -Property @{
        cpuFailoverResourcesPercent = 25
        memoryFailoverResourcesPercent = 25
      }
    }
  }), $true)
```

### vMotion architecture

**vMotion** performs a live migration of a running VM's compute state
(memory contents and execution state) from one ESXi host to another with no
guest-perceptible downtime beyond a brief final cutover. The mechanics:

1. A shadow VM is created on the destination host, and the source host
   begins iteratively copying the VM's memory pages over the vMotion
   network to the destination while the VM continues running (and being
   modified) on the source.
2. Because memory continues changing during the copy, vMotion tracks
   "dirty" pages modified since the last copy pass and re-copies just those
   pages in successive, shrinking iterations.
3. Once the remaining dirty-page set is small enough to transfer within a
   sub-second window, the source VM is briefly stunned, the final delta is
   copied, and execution resumes on the destination host. Network identity
   (MAC address) and, for shared storage, disk state require no data copy
   at this stage since both hosts already see the same datastore.

**Encrypted vMotion** protects the memory and device-state data transferred
during migration using a per-migration encryption key negotiated between
source and destination hosts, independent of whether the VM's disks are
themselves encrypted at rest. It is configurable per-VM as **Disabled**,
**Opportunistic** (encrypt if both hosts support it, proceed unencrypted if
not), or **Required** (fail the migration rather than proceed unencrypted).
Required is the correct setting for any VM where memory contents in transit
constitute a compliance concern (secrets, regulated data resident in
memory) — Opportunistic silently downgrades protection rather than failing
loudly, which is rarely the intended behavior for a compliance-driven
requirement.

**Long-distance vMotion** and **cross-vCenter vMotion** extend live
migration beyond a single cluster or even a single vCenter Server instance
(including across vCenter instances joined only by a common SSO domain, or
in more recent capability, across independent vCenter instances via
Enhanced Linked Mode connectivity). These extended forms have explicit
latency and bandwidth requirements — historically up to 150 ms RTT is
supported (versus roughly 10 ms for standard same-datacenter vMotion),
which is materially more permissive than vSAN stretched-cluster latency
requirements — but still require enough sustained bandwidth to complete the
memory-copy convergence within a practical time window, and require Layer 2
network connectivity (or an equivalent that preserves the VM's IP without a
guest-visible network change) between source and destination for the VM's
network identity to remain valid post-migration.

**Storage vMotion** is the storage-side counterpart: it relocates a VM's
disk files between datastores (or changes disk format/provisioning type)
while the VM continues running, using a mirror-driver mechanism that
mirrors in-flight writes to both the source and destination disk copies
during the migration, then cuts over once the bulk copy completes. Compute
vMotion and Storage vMotion can run simultaneously as a single combined
operation (relocating both the running state and the disk to a new host
and new datastore at once).

```powershell
# PowerCLI: perform a combined compute + storage vMotion with encryption required
Move-VM -VM (Get-VM -Name "app-web-03") `
  -Destination (Get-VMHost -Name "esxi04.corp.example") `
  -Datastore (Get-Datastore -Name "vsan-datastore-02") `
  -VMotionPriority High

Get-VM -Name "app-web-03" | Get-View |
  Select-Object -ExpandProperty Config |
  Select-Object -ExpandProperty MigrateEncryption
```

```powershell
# PowerCLI: set a VM's vMotion encryption policy to Required
$vm = Get-VM -Name "app-secure-01"
$spec = New-Object VMware.Vim.VirtualMachineConfigSpec
$spec.MigrateEncryption = "opportunistic"  # or "required" / "disabled"
$vm.ExtensionData.ReconfigVM_Task($spec)
```

### vSphere Fault Tolerance (FT)

**vSphere Fault Tolerance** goes beyond HA's restart-after-failure model to
provide continuous availability with zero downtime and zero data loss for a
protected VM. FT maintains a live secondary VM on a different host, kept in
**lockstep** with the primary using **Fast Checkpointing** — a technique
that streams the primary VM's execution deltas to the secondary at very
high frequency (far more granular than vMotion's memory-copy model),
allowing the secondary to take over instantaneously and transparently
(without a guest-visible restart) if the primary's host fails. Unlike
older FT implementations that required true vLockstep (identical
instruction-for-instruction record/replay), Fast Checkpointing–based FT
tolerates some divergence between primary and secondary execution and
periodically resynchronizes state, which is what enables current FT to
support multiple vCPUs per protected VM.

FT's scaling limits are the most operationally important fact about it: at
the vSphere 9.x baseline, FT-protected VMs are limited to a maximum of 8
vCPUs, and a single ESXi host has an overall cap on the number of
FT-protected VMs and vCPUs it can host concurrently (a per-host limit,
independent of the per-VM vCPU cap, intended to bound the sustained network
and CPU overhead FT imposes on the host). FT also carries specific
prerequisites and restrictions: it requires a dedicated, low-latency FT
logging network between hosts, does not support certain features
simultaneously (historically including some snapshot and Storage vMotion
interactions, which vary by release — verify current-release compatibility
before designing around FT), and imposes real CPU and network overhead on
every protected VM whether or not a failure ever occurs. FT is therefore
reserved for a narrow set of genuinely zero-RPO/zero-RTO-critical
workloads, not applied broadly as a default HA enhancement — HA's
restart-based recovery (measured in a small number of minutes) is
sufficient and far less resource-expensive for the overwhelming majority of
production VMs.

### DRS and HA integration

DRS and HA are architecturally separate cluster services but cooperate
closely in practice:

- **VM restart priority.** HA restart order is influenced by a per-VM
  restart priority setting (Lowest through Highest, plus Disabled), so
  infrastructure-tier VMs (domain controllers, DNS, the VM hosting a
  storage array's management appliance) can be configured to restart ahead
  of less critical application VMs after a multi-VM host failure.
- **Orchestrated restart / VM dependencies.** Beyond simple priority
  ordering, HA supports explicit VM-to-VM restart dependencies (a defined
  VM group must reach a running, and optionally VMware-Tools-reporting,
  state before a dependent VM group begins restarting), which matters for
  multi-tier applications where the database tier must be up before the
  application tier attempts to reconnect.
- **VM/VM affinity rule interaction.** HA respects DRS-defined VM/VM
  affinity and anti-affinity rules when choosing restart placement where
  possible, but a required anti-affinity rule can reduce the set of viable
  restart targets during a multi-host failure — the same failure-scenario
  modeling discussed in Chapter 5 for affinity rules applies directly to
  HA restart planning.
- **Proactive HA.** Distinct from reactive HA (which responds to an
  already-failed host), Proactive HA consumes hardware health signals from
  a supported hardware-monitoring integration (server vendor health
  providers reporting component degradation — failing power supply, memory
  ECC error trends, fan failure) and preemptively evacuates VMs from a
  degrading-but-not-yet-failed host, placing that host into quarantine mode
  (DRS avoids placing new VMs there but existing VMs are not force-evacuated)
  or maintenance mode (full evacuation), configurable per the
  administrator's tolerance for proactive disruption versus risk.

### vSphere Cluster Services (vCLS)

**vSphere Cluster Services (vCLS)** are lightweight agent VMs — typically
one to three per cluster depending on cluster size — that vCenter Server
deploys and maintains automatically on every cluster, independent of
whether DRS or HA is actually licensed or enabled on that cluster. This
surprises administrators who disable DRS and HA on a cluster expecting no
VMware-owned infrastructure VMs to appear, and then find vCLS agent VMs
present anyway.

The reason vCLS exists is architectural: starting with the release that
introduced it, VMware decoupled cluster services (DRS, HA) from a
permanently-connected vCenter Server dependency by giving each cluster its
own always-on, lightweight compute substrate (the vCLS VMs) that cluster
services can rely on for quorum and control-plane continuity even during a
vCenter Server outage or upgrade. In other words, vCLS exists to make DRS
and HA themselves more resilient to vCenter unavailability — the agent VMs
are the infrastructure that cluster services run on top of, not a feature
administrators opt into directly.

Operational guidance for vCLS:

- Do not manually delete, modify, or manage vCLS agent VMs directly; they
  are lifecycle-managed automatically by vCenter Server and will be
  recreated if removed.
- vCLS VMs consume minimal resources (a small vCPU/memory footprint per
  VM) but do count as VMs on their host for licensing and inventory
  purposes in some counting contexts — factor a small number of additional
  always-present VMs into capacity planning at the margins.
- If vCLS VMs must be temporarily excluded from a specific datastore or
  host (a maintenance activity, a storage migration), use the supported
  vCLS VM placement/anti-affinity configuration options rather than
  attempting to move or delete the VMs directly.
- A cluster showing "vCLS VMs are being deployed/retreated" health warnings
  during a vCenter upgrade or cluster-membership change is normal transient
  behavior, not necessarily an error condition, but should resolve within
  a reasonably short window — persistent failure to deploy vCLS VMs
  (commonly due to no eligible datastore or no DRS-automation-eligible
  host) is worth investigating as it can degrade DRS/HA reliability.

### Stretched-cluster and multi-site availability design patterns

Beyond the single-cluster HA/DRS/vMotion model covered above, enterprises
commonly extend availability across sites using one of several patterns,
each with different RPO/RTO and complexity trade-offs:

- **A single stretched cluster across two sites** (using vSAN stretched
  cluster, introduced in Chapter 6, or an equivalent stretched-storage
  array configuration) with vSphere HA/DRS operating across both sites as
  one logical cluster. This gives the tightest RPO (effectively zero, since
  storage is synchronously mirrored) and fast automatic HA-driven failover,
  at the cost of the strict inter-site latency requirement that makes this
  pattern only viable at true metro distance.
- **Independent clusters per site with orchestrated cross-site
  recovery**, where each site runs its own self-contained vSphere cluster
  (no stretched storage, no cross-site vMotion in normal operation) and a
  separate orchestration/replication layer handles failover between sites.
  This tolerates much greater distance and latency between sites than a
  stretched cluster, at the cost of a non-zero RPO (determined by
  replication frequency) and a failover process that is orchestrated
  (automated by DR tooling) rather than instantaneous like HA.
- **Active-active multi-site with independent workloads**, where each site
  runs production workloads independently and the "availability" pattern
  is workload-level redundancy (application-layer clustering, global load
  balancing) rather than infrastructure-layer VM failover at all. This
  pattern sidesteps vSphere-level stretched-cluster/replication complexity
  entirely but pushes availability responsibility onto the application
  architecture.

Choosing among these depends primarily on achievable inter-site latency,
required RPO/RTO, and whether the organization is willing to operate a
single logical cluster spanning two physical locations (with the shared
blast-radius implications that implies) versus accepting orchestrated,
non-instantaneous recovery in exchange for looser distance constraints.

### Disaster recovery and replication tooling (conceptual overview)

vSphere's native availability tools (HA, FT, vMotion) address host- and
compute-level failures within reach of live migration or automatic restart.
Site-level disaster recovery — where an entire site becomes unavailable —
is the domain of dedicated DR orchestration tooling, which this chapter
introduces only at a conceptual level since deep DR tooling implementation
is out of scope here:

- **Orchestrated failover tooling** (in VMware's historical product line,
  Site Recovery Manager–style orchestration) automates the sequenced
  failover of many VMs between a protected site and a recovery site
  according to predefined recovery plans — including boot order, IP
  re-mapping, and pre/post-failover scripted steps — rather than requiring
  an administrator to manually power on and reconfigure each VM in the
  correct order during an actual disaster.
- **vSphere Replication** provides VM-level, storage-agnostic (does not
  require the same array or replication technology on both ends)
  asynchronous replication of VM disk state to a recovery site or a
  secondary datastore, with a configurable recovery point objective per VM,
  independent of whether the underlying storage is vSAN or a traditional
  array.
- **Current positioning (VMware Live Recovery / Cloud DR).** VMware's
  current disaster-recovery and ransomware-recovery product positioning
  under Broadcom continues to build on this same conceptual
  foundation — orchestrated recovery plans plus flexible, VM-level
  replication — extended with cloud-hosted recovery targets and
  ransomware-focused recovery workflows (isolated recovery environments for
  validating backups/replicas are not themselves compromised before
  full failback). Treat the specific current product name and packaging as
  a detail to confirm against current VMware/Broadcom documentation at
  implementation time rather than a fixed fact to memorize — the
  underlying architectural concepts (orchestrated recovery plans,
  VM-level asynchronous replication, RPO/RTO-driven design) are stable
  even as product branding evolves.

## Design Considerations

- **Admission control percentage versus real headroom.** A cluster resource
  percentage set once at initial build time does not automatically track
  cluster growth or shrinkage — recalculate and validate the percentage
  whenever hosts are added or removed, and prefer the automatically
  calculated "host failures cluster tolerates" mode over a manually fixed
  percentage so the reserved capacity scales with the cluster.
- **Isolation address selection in non-default topologies.** In any
  network design where the management network's default gateway is not a
  reliable arbiter of true isolation (redundant gateways via VRRP/HSRP,
  or a management network with no gateway dependency for local VM
  reachability), configure explicit `das.isolationaddress` values rather
  than relying on the default-gateway assumption.
- **Encrypted vMotion policy by data sensitivity.** Set Required, not just
  Opportunistic, for any VM where in-transit memory exposure is a genuine
  compliance concern — Opportunistic's silent fallback to unencrypted
  migration is easy to overlook during an audit.
- **FT is a narrow tool, not a general HA upgrade.** Given its 8-vCPU
  ceiling, per-host concurrent-FT-VM limits, and continuous resource
  overhead, reserve FT for a short, deliberately curated list of workloads
  where the business genuinely cannot tolerate an HA-driven restart's few
  minutes of downtime — not as a default "more available than HA" setting
  applied broadly.
- **vCLS placement and datastore eligibility.** Ensure every cluster has at
  least one datastore and one host eligible for vCLS VM placement at all
  times (including during maintenance windows), since a cluster that
  cannot place its vCLS VMs anywhere degrades DRS/HA reliability in ways
  that are easy to misattribute to an unrelated cause.
- **Stretched cluster versus orchestrated DR trade-off.** A stretched
  cluster is not automatically the "better" availability pattern — it
  concentrates operational and blast-radius risk into a single logical
  cluster spanning two sites (a cluster-wide misconfiguration or a
  version/patch issue now affects both sites simultaneously) in exchange
  for near-zero RPO. Evaluate this trade-off explicitly against the
  organization's actual RPO/RTO requirement rather than defaulting to the
  most technically impressive option.
- **DR recovery plan testing cadence.** Whatever orchestrated DR tooling is
  in use, non-disruptive recovery-plan testing (most tooling in this space
  supports an isolated test-bubble network for exactly this purpose) should
  be scheduled on a recurring basis — an untested recovery plan is a
  liability that looks identical to a working one until the day it is
  actually needed.

## Implementation and Automation

### Configuring HA isolation response and isolation addresses

```powershell
# PowerCLI: set host isolation response and add explicit isolation addresses
$cluster = Get-Cluster -Name "prod-cluster-a"

Get-AdvancedSetting -Entity $cluster -Name "das.isolationaddress1" -ErrorAction SilentlyContinue |
  Remove-AdvancedSetting -Confirm:$false

New-AdvancedSetting -Entity $cluster -Name "das.isolationaddress1" `
  -Value "10.10.10.1" -Confirm:$false
New-AdvancedSetting -Entity $cluster -Name "das.isolationaddress2" `
  -Value "10.10.10.2" -Confirm:$false
New-AdvancedSetting -Entity $cluster -Name "das.usedefaultisolationaddress" `
  -Value "false" -Confirm:$false
```

```powershell
# PowerCLI: set per-VM restart priority and isolation response override
Get-VM -Name "dc-01" | Get-View |
  ForEach-Object {
    $spec = New-Object VMware.Vim.ClusterConfigSpecEx
    $vmOverride = New-Object VMware.Vim.ClusterDasVmConfigSpec
    $vmOverride.operation = "add"
    $vmOverride.info = New-Object VMware.Vim.ClusterDasVmConfigInfo
    $vmOverride.info.key = $_.MoRef
    $vmOverride.info.restartPriority = "highest"
    $spec.dasVmConfigSpec = @($vmOverride)
    (Get-View $cluster.ExtensionData.MoRef).ReconfigureComputeResource_Task($spec, $true)
  }
```

### Configuring orchestrated restart dependencies

```text
vSphere Client navigation:
Hosts and Clusters > select cluster > Configure > VM Overrides > Add
  - Select the dependent VM group (for example, "app-tier")
  - Set "VM Restart Priority" and enable "Additional Delay" or
    configure a VM/VM dependency rule under
    Configure > VM/Host Rules > Add > "Virtual Machines to Virtual Machines"
    with the dependency direction (must-start-after) explicitly set.
```

### Enabling and validating vSphere FT on a supported VM

```powershell
# PowerCLI: enable Fault Tolerance on a 2-vCPU VM (must be powered on, well within FT limits)
$vm = Get-VM -Name "app-critical-01"
Set-VM -VM $vm -Confirm:$false  # ensure VM meets FT prerequisites first (no snapshots, eager-zeroed thick disks, etc.)

Get-VM -Name "app-critical-01" | Get-View |
  ForEach-Object { $_.ToggleFaultToleranceState($true) }
```

```bash
# esxcli: confirm a dedicated FT logging VMkernel adapter exists and is tagged correctly
esxcli network ip interface tag get -i vmk2
```

### Configuring Proactive HA

```powershell
# PowerCLI: enable Proactive HA with automated quarantine-mode response
$cluster = Get-Cluster -Name "prod-cluster-a"
Set-Cluster -Cluster $cluster -Confirm:$false

(Get-View $cluster.ExtensionData.MoRef).ReconfigureComputeResource_Task(
  (New-Object VMware.Vim.ClusterConfigSpecEx -Property @{
    infraUpdateHaConfig = New-Object VMware.Vim.ClusterInfraUpdateHaConfigInfo -Property @{
      enabled = $true
      behavior = "ModerateAutomatic"  # options include Manual, ModerateAutomatic, AggressiveAutomatic
    }
  }), $true)
```

### Migrating a running VM with Storage vMotion and priority control

```powershell
# PowerCLI: relocate a VM to a new datastore only (Storage vMotion), high priority
Move-VM -VM (Get-VM -Name "app-web-05") `
  -Datastore (Get-Datastore -Name "vsan-datastore-03") `
  -VMotionPriority High
```

## Validation and Troubleshooting

- **Confirm HA master election.** `vSphere Client > select cluster >
  Monitor > vSphere HA > Summary` reports the current master host. From the
  ESXi shell on any host, `esxcli system settings advanced list -o
  /UserVars/HostAgentDisableTime` and the FDM log
  (`/var/log/fdm.log`) show recent election and heartbeat events; a cluster
  cycling through master elections repeatedly indicates management-network
  instability, not an HA defect.
- **Verify isolation response behavior with a controlled test.** Physically
  or logically disconnect a single non-production host's management uplink
  (in a lab, not production) and confirm the configured isolation response
  fires as expected within the configured `das.config.fault
  ToleranceHeartbeatTimeout`-adjacent isolation-detection window; VMs on
  the isolated host should transition according to the configured policy
  (Disabled, Power off and restart, or Shut down and restart), and HA
  should restart them on a surviving host without a duplicate-VM
  (split-brain) condition.
- **Admission control capacity audit.** `vSphere Client > select cluster >
  Configure > vSphere Availability > Admission Control` shows current
  reserved failover capacity versus what the cluster would actually need
  under the configured failure-tolerance level; a warning here
  ("Insufficient configured resources to satisfy...") means the cluster is
  currently over-committed relative to its own HA promise and needs either
  more capacity or a relaxed failure-tolerance target.
- **vMotion compatibility check (EVC).** A vMotion failing with a CPU
  incompatibility error points to mismatched CPU generations without
  Enhanced vMotion Compatibility (EVC) masking enabled at the cluster
  level; `vSphere Client > select cluster > Configure > VMware EVC`
  confirms the current EVC baseline and whether all member hosts qualify
  for a higher baseline.
- **FT sync state.** `vSphere Client > select VM > Summary > Fault
  Tolerance` panel shows the secondary VM's sync status; a secondary stuck
  in "Not Protected" or repeatedly resynchronizing usually traces to
  insufficient network bandwidth/latency on the dedicated FT logging
  network, not a compute-resource problem on either host.
- **Proactive HA event validation.** `vSphere Client > select cluster >
  Monitor > vSphere DRS > Proactive HA` shows any host currently in
  quarantine or maintenance mode due to a hardware health signal, along
  with the reporting hardware-health provider; cross-reference against the
  server vendor's own hardware-management console (iDRAC, iLO, or
  equivalent) to confirm the underlying condition rather than treating the
  vSphere-side alert as the full diagnostic picture.
- **vCLS health check.** `vSphere Client > select cluster > Monitor >
  vSphere DRS` (or the cluster Summary panel) surfaces vCLS-related
  warnings directly; persistent "vSphere Cluster Services has retreat mode
  activated" or repeated failure to deploy vCLS VMs after several minutes
  warrants checking for an eligible datastore/host and confirming no
  storage or network policy is inadvertently blocking vCLS VM placement.

## Security and Best Practices

- Set encrypted vMotion to Required, not Opportunistic, for any VM carrying
  regulated data in memory, and audit the cluster-wide default policy
  periodically since new VMs inherit whatever default is configured at
  creation time.
- Restrict who can modify HA admission control policy and isolation
  response settings through role-based access control — a well-intentioned
  but unauthorized change to admission control percentage can silently
  remove the capacity guarantee the business is relying on.
- Isolate the vMotion network (and, separately, the FT logging network
  where FT is used) on a dedicated, non-routed VLAN; vMotion traffic
  historically transmitted memory contents unencrypted by default before
  encrypted vMotion existed, and even with encryption available, network
  isolation remains a defense-in-depth control worth keeping regardless.
- Do not manually manage vCLS agent VMs (rename, move, assign to a
  different resource pool, or delete) — doing so can degrade cluster
  service resilience in ways that are hard to diagnose later, and any
  manual changes are subject to being overwritten by vCenter's own vCLS
  lifecycle management regardless.
- Apply the principle of least privilege to DR orchestration tooling
  credentials and API access; recovery-plan execution capability is
  effectively "power to fail over production," and access to trigger it
  should be as tightly controlled and audited as any other high-impact
  administrative action.
- Test isolation response and admission-control assumptions in a
  non-production environment before relying on them in production —
  the difference between "Disabled" and "Power off and restart VMs" as an
  isolation response has produced real split-brain incidents in
  environments where the setting was assumed rather than verified.
- Periodically test DR recovery plans (isolated network bubble testing
  where the tooling supports it) rather than treating an untested plan as
  equivalent to a validated one; document RPO/RTO actually observed during
  test failovers against the RPO/RTO the business believes it is getting.

## References and Knowledge Checks

**References**

- VMware vSphere 9.x Documentation — *Availability* (vSphere HA, Fault
  Domain Manager, admission control).
- VMware vSphere 9.x Documentation — *vCenter Server and Host Management*
  (vMotion, Storage vMotion, Enhanced vMotion Compatibility).
- VMware vSphere 9.x Documentation — *Fault Tolerance* (lockstep execution,
  Fast Checkpointing, current vCPU/VM limits).
- VMware vSphere 9.x Documentation — *Resource Management* (Proactive HA,
  DRS/HA integration, vSphere Cluster Services).
- VMware Knowledge Base — vSphere Cluster Services (vCLS) operational
  guidance.
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — dated vSphere
  9.x / NSX 4.x baseline referenced throughout this volume.
- See Chapter 5 for VM/Host and VM/VM affinity rule mechanics referenced
  in HA restart placement.
- See Chapter 6 for vSAN stretched-cluster witness-host architecture.

**Knowledge checks**

1. Why does vSphere HA use datastore heartbeating in addition to network
   heartbeating, and what specific ambiguity does it resolve?
2. Explain the practical difference between the "Disabled" and "Power off
   and restart VMs" isolation response settings, and why choosing wrong
   can create a split-brain condition.
3. Why is cluster resource percentage generally preferred over slot policy
   for admission control on heterogeneous clusters?
4. What architectural change let modern FT support multiple vCPUs per
   protected VM, and what limit still bounds FT's applicability at scale?
5. Why do vCLS agent VMs appear on a cluster even when DRS and HA are both
   disabled?

## Hands-On Lab

**Objective:** Configure HA admission control and isolation response on a
nested-ESXi lab cluster, perform a live vMotion, and deliberately trigger a
host isolation event to observe HA's isolation-response and restart
behavior — then restore the cluster to its prior configuration.

**Prerequisites**

- A vSphere 9.x lab with at least 3 nested ESXi hosts in an HA/DRS-enabled
  cluster, shared datastore access across all hosts, and at least one test
  VM per host with VMware Tools installed.
- PowerCLI connected to the lab vCenter with cluster-modify privileges.
- The ability to disable/re-enable a nested ESXi host's management network
  adapter from the underlying hypervisor (or nested VM) console, since the
  isolation test requires cutting management connectivity without powering
  off the host itself.

**Steps**

1. Confirm HA is enabled and set admission control to cluster resource
   percentage tolerating one host failure:

   ```powershell
   Connect-VIServer -Server vcenter01.lab.example
   $cluster = Get-Cluster -Name "lab-ha-cluster"
   Set-Cluster -Cluster $cluster -HAEnabled:$true -HAAdmissionControlEnabled:$true -Confirm:$false
   ```

   **Expected result:** `vSphere Client > select cluster > Configure >
   vSphere Availability > Admission Control` shows a calculated reserved
   percentage greater than zero.

2. Set an explicit isolation address (use the lab management gateway or
   another reliably-pingable device on the management VLAN) and set
   isolation response to "Power off and restart VMs":

   ```powershell
   New-AdvancedSetting -Entity $cluster -Name "das.isolationaddress1" `
     -Value "10.10.10.1" -Confirm:$false -Force
   New-AdvancedSetting -Entity $cluster -Name "das.usedefaultisolationaddress" `
     -Value "false" -Confirm:$false -Force
   ```

   Set the isolation response via
   `vSphere Client > select cluster > Configure > vSphere Availability >
   Edit > Host Failure Response Behavior > Response for Host Isolation >
   Power off and restart VMs`.

3. Deploy or confirm a test VM (`lab-ha-test-vm`) is running on one
   specific host, and note that host's name:

   ```powershell
   Get-VM -Name "lab-ha-test-vm" | Select-Object Name, @{N="Host";E={$_.VMHost.Name}}
   ```

4. Perform a live compute vMotion of the test VM to a different host to
   confirm baseline vMotion functions before the isolation test:

   ```powershell
   Move-VM -VM (Get-VM -Name "lab-ha-test-vm") `
     -Destination (Get-VMHost -Name "esxi02.lab.example") -VMotionPriority High
   ```

   **Expected result:** the VM shows the new host in
   `Get-VM | Select Name,VMHost` with no guest-visible interruption (a
   continuous ping to the VM's IP shows at most one or two dropped
   packets, not a sustained outage).

5. **Negative test — isolation event.** On the host now running
   `lab-ha-test-vm`, disconnect only its management network vmknic (not the
   VM network) from the nested-hypervisor console, simulating management
   isolation while VM traffic paths remain theoretically reachable:

   ```bash
   # Run directly on the isolated host's ESXi shell/console (not via vCenter,
   # since vCenter connectivity will itself be lost to this host)
   esxcli network ip interface set -e false -i vmk0
   ```

   **Expected result:** within the configured isolation-detection window,
   the master HA host detects loss of network heartbeats from this host,
   confirms isolation (rather than failure) via datastore heartbeating, and
   — per the configured "Power off and restart VMs" policy — hard-powers-off
   `lab-ha-test-vm` on the isolated host and restarts it on a surviving
   host. Confirm via `vSphere Client > select cluster > Monitor > vSphere
   HA > Summary` and by observing `lab-ha-test-vm`'s host attribute change
   without any administrator-initiated migration.

6. Restore the isolated host's management connectivity:

   ```bash
   esxcli network ip interface set -e true -i vmk0
   ```

   **Expected result:** the host reconnects to vCenter and rejoins the HA
   cluster as an agent host within a few minutes; confirm via `vSphere
   Client > Hosts and Clusters` that the host shows Connected, not
   Disconnected or Not Responding.

7. **Cleanup:** remove the explicit isolation address settings and restore
   default isolation response if the lab's baseline configuration did not
   originally specify them:

   ```powershell
   Get-AdvancedSetting -Entity $cluster -Name "das.isolationaddress1" |
     Remove-AdvancedSetting -Confirm:$false
   Get-AdvancedSetting -Entity $cluster -Name "das.usedefaultisolationaddress" |
     Remove-AdvancedSetting -Confirm:$false
   ```

   Reset isolation response to its prior value via `vSphere Client >
   select cluster > Configure > vSphere Availability > Edit`, and power off
   /remove `lab-ha-test-vm` if it was created solely for this lab.

## Summary and Completion Checklist

vSphere HA's Fault Domain Manager provides host-failure protection through
master/agent election, dual network-plus-datastore heartbeating to
distinguish true failure from isolation, and a configurable isolation
response that determines how an isolated host's VMs are handled before HA
restarts them elsewhere. Admission control — cluster resource percentage
being the standard modern choice over slot policy — reserves the capacity
that restart promise depends on. vMotion and Storage vMotion make both
planned maintenance and DRS rebalancing non-disruptive, with encrypted and
long-distance/cross-vCenter variants extending the model across security
and geographic boundaries. Fault Tolerance provides a narrower,
continuous-availability guarantee via Fast Checkpointing lockstep, bounded
by real vCPU and per-host concurrency limits that keep it a targeted tool
rather than a general HA replacement. DRS and HA integrate through restart
priority, orchestrated dependencies, affinity-rule-aware placement, and
Proactive HA's hardware-health-driven quarantine model, while vCLS agent
VMs provide the always-on infrastructure substrate cluster services depend
on regardless of DRS/HA licensing state. Multi-site availability design
trades stretched-cluster's near-zero RPO and tight blast-radius coupling
against orchestrated DR's looser distance constraints and non-zero RPO.

- [ ] Can explain FDM master/agent election and the role of datastore
      heartbeating in disambiguating failure from isolation.
- [ ] Can configure HA admission control (cluster resource percentage) and
      isolation response/isolation address correctly.
- [ ] Can explain vMotion and Storage vMotion mechanics, including when to
      require encrypted vMotion.
- [ ] Can state vSphere FT's current vCPU and per-host scaling limits and
      explain why FT is a narrow-use tool.
- [ ] Can explain how DRS and HA integrate through restart priority,
      orchestrated dependencies, and Proactive HA.
- [ ] Can explain why vCLS agent VMs exist independent of DRS/HA licensing.
- [ ] Can compare stretched-cluster versus orchestrated multi-site DR
      trade-offs at a conceptual level.
- [ ] Completed the hands-on lab, including the isolation-event negative
      test and full cleanup.
