# Chapter 07: Availability, Stretched Clusters, and Data Protection

## Learning Objectives

- Distinguish availability, replication, and backup, and explain why one
  never substitutes for another.
- Design a two-node cluster with a witness and identify its failure
  modes.
- Explain stretched cluster architecture, its latency and bandwidth
  requirements, and what it does and does not protect against.
- Select fault domain configuration appropriate to a cluster's physical
  layout.
- Design a backup approach for VxRail workloads and validate that it
  recovers.

## Theory and Architecture

### Three different problems, routinely confused

This confusion causes more real data loss than any technical failure in
this volume, so it is worth being blunt about.

| Mechanism | Protects against | Does not protect against |
| --- | --- | --- |
| **Availability** (HA, vSAN failure tolerance, stretched clusters) | Hardware failure — a drive, a host, a rack, a site | Anything that corrupts or deletes data, because the corruption is replicated faithfully |
| **Replication** | Site loss, with a recovery point measured in minutes | The same — replication copies deletion and ransomware encryption as diligently as it copies legitimate writes |
| **Backup** | Corruption, deletion, ransomware, and operator error | Nothing, if it is not tested |

A stretched cluster across two sites, with synchronous mirroring and a
witness, provides no protection whatsoever against a ransomware event or
an accidental deletion. Both are written to both sites, immediately and
correctly. This is not a shortcoming of the design; it is what
availability means. But it is regularly sold and bought as though it were
backup, and clusters exist today whose owners believe they are protected
against something they are not.

**A VxRail cluster needs a backup strategy that is separate from its
availability design.** The rest of this chapter covers both, in that
order, and the separation is deliberate.

### Standard cluster availability

The mechanics are vSAN's and vSphere HA's, covered in
[Volume V, Chapter 07](../../volume-05-vmware-virtualization/chapters/07-vsphere-availability-mobility-and-cluster-services.md).
The layers stack:

- **Drive failure** — absorbed by vSAN's failure tolerance; the object
  rebuilds using free capacity elsewhere. This is why the slack space
  from [Chapter 05](05-cluster-expansion-scale-out-and-capacity-planning.md)
  is functional.
- **Host failure** — absorbed by both vSAN (data remains available from
  other copies) and HA (VMs restart on surviving hosts).
- **Multiple simultaneous failures** — absorbed only to the extent the
  applied storage policy allows, which is a decision, not a property.

The layer people forget is the second failure during a rebuild. A cluster
tolerating one failure that loses a host is not protected while it
rebuilds, and rebuild time is proportional to data volume. Tolerating two
failures is expensive; knowing whether you have chosen to tolerate one is
essential.

### Fault domains

By default, vSAN treats each host as its own fault domain and will place
the copies of an object on different hosts. If those hosts share a rack,
and the rack loses power, the object is unavailable despite the policy
having been satisfied.

Fault domains fix this by telling vSAN which hosts share fate. Configure
them to match physical reality — one fault domain per rack, typically —
and vSAN places copies across domains rather than merely across hosts.

The cost is a higher host-count requirement: satisfying a policy across
fault domains needs enough domains, not merely enough hosts. A cluster
spanning three racks with unequal host counts also places uneven demand
on the largest domain.

**Configure fault domains if the cluster spans racks, and do not if it
does not.** A single-rack cluster with fault domains configured gains
nothing and constrains placement.

### Two-node clusters and the witness

For small and edge sites, a two-node cluster provides host-failure
tolerance with two nodes rather than three. It works by placing the two
data copies on the two nodes and the witness component — the tie-breaker
that determines which node holds the valid copy after a partition — on a
third entity outside both.

The witness is a lightweight virtual appliance. Its placement is the
whole design:

- **It must not run on either of the two nodes.** A witness hosted on a
  node it arbitrates cannot arbitrate that node's failure.
- **It must not share a failure domain with either node.** A witness at a
  site whose network path fails together with a node's produces the
  split-brain scenario it exists to prevent.
- **It commonly lives at a central site**, arbitrating for several
  two-node edge clusters — though each cluster needs its own witness
  appliance.

The failure modes to reason through:

| Failure | Outcome |
| --- | --- |
| One node fails | Surviving node plus witness form a quorum; workloads restart there |
| Witness fails | Both nodes remain, cluster continues, but a subsequent node failure has no arbiter — replace the witness promptly |
| Link between nodes fails, both reach witness | Witness decides; one node's copy becomes authoritative |
| Node loses connectivity to both peer and witness | That node is isolated and its copy is not authoritative |

The third row is the reason the witness matters. Without an arbiter, both
nodes would believe themselves survivors, and both would continue writing.

### Stretched clusters

A stretched cluster extends the same idea to two full sites: hosts at
site A, hosts at site B, and a witness at a third location. Data is
mirrored synchronously across sites, so a site loss is absorbed with no
data loss.

The requirements are demanding and non-negotiable, because synchronous
mirroring means every write waits for both sites:

- **Latency between data sites** must be low — single-digit milliseconds
  round trip. This is a hard physical constraint on how far apart the
  sites can be.
- **Bandwidth between data sites** must carry all write traffic plus
  resynchronization. Under-provisioning shows up as application latency,
  not as a network alarm.
- **Latency to the witness** may be much higher, because the witness
  carries metadata rather than data.
- **The witness must be at a third location** that does not fail with
  either site.

Confirm the current specific figures against the vSAN stretched cluster
requirements rather than from memory — they are version-dependent and
they are the kind of number that must be right.

**What a stretched cluster costs.** Synchronous mirroring across sites
means every write pays the inter-site round trip. It also means the
capacity requirement doubles, since the data exists in full at both
sites, before local failure tolerance is considered at all. Site-local
protection policies mitigate this partially and add capacity of their
own.

**What it buys, precisely:** continued operation through the loss of an
entire site, with no data loss and no recovery procedure. That is a
genuinely strong guarantee and it is expensive. Whether it is warranted
is a business continuity question — the analysis in
[Volume XII, Chapter 02](../../volume-12-resilience-lifecycle-management/chapters/02-business-impact-analysis-and-continuity-planning.md)
is what answers it, not a technical preference.

### Backup, which is the part that gets neglected

Because VxRail is highly available, backup is easy to under-prioritize.
Resist this. Every threat in the "does not protect against" column above
is addressed by backup and by nothing else in this chapter.

Backing up VxRail workloads is ordinary vSphere backup: image-level
backups through the vSphere APIs for Data Protection, application-aware
quiescing where the workload needs it, and retention matched to recovery
requirements. The architecture and policy considerations are covered in
[Volume VI, Chapter 05](../../volume-06-enterprise-storage-data-protection/chapters/05-backup-architecture-and-data-protection-policy.md).

Two VxRail-specific points:

**Do not store backups on the cluster being backed up.** Obvious when
stated, and it happens anyway because the vSAN datastore is the
convenient large datastore. A backup that shares fate with its source is
not a backup.

**Back up the management plane too.** vCenter and VxRail Manager hold
configuration that a rebuild would otherwise reconstruct by hand. vCenter
has a native file-based backup mechanism; use it, and store the output
off-cluster.

## Design Considerations

- **State the recovery objectives before choosing a mechanism.** Recovery
  time and recovery point objectives determine whether a stretched
  cluster is warranted or whether backup and restore suffices. Choosing
  the mechanism first and deriving the objectives from it is backwards
  and expensive.
- **Do not let a stretched cluster substitute for backup in the
  design document.** If the document does not have both, it is incomplete
  regardless of how strong the availability design is.
- **Match fault domains to physical layout, and only if there is one.**
  Racks, power feeds, and cooling zones are real fault domains; arbitrary
  groupings are not.
- **Place two-node witnesses with genuine independence.** The
  cheapest-looking option — a VM at one of the two sites — defeats the
  design.
- **Size the inter-site link for resynchronization, not steady state.**
  After a site outage, the recovering site must catch up, and that
  traffic dwarfs normal write traffic. A link sized for steady state
  turns a brief outage into a long recovery.
- **Consider whether one site can carry the whole workload.** A stretched
  cluster that fails over to a site with insufficient capacity has
  survived the failure and not the consequences.

## Implementation and Automation

### 1. Auditing the current availability position

```powershell
Connect-VIServer -Server vcsa-01.lab.example.com

# Is this a stretched cluster, and what fault domains exist?
Get-VsanClusterConfiguration |
  Select-Object Cluster, VsanEnabled, StretchedClusterEnabled, WitnessHost

Get-VsanFaultDomain |
  Select-Object Name, Cluster,
    @{N='Hosts'; E={($_.VMHost | Select-Object -ExpandProperty Name) -join ', '}}

# What failure tolerance is actually applied, by capacity.
Get-VM | ForEach-Object {
  [pscustomobject]@{
    VM     = $_.Name
    Policy = (Get-SpbmEntityConfiguration $_).StoragePolicy.Name
    UsedGB = [math]::Round($_.UsedSpaceGB, 1)
  }
} | Group-Object Policy |
    Select-Object Name, Count,
      @{N='TotalGB'; E={[math]::Round(($_.Group.UsedGB | Measure-Object -Sum).Sum, 1)}}
```

The last block answers the question that matters: not which policies
exist, but how much of the estate is protected to what level.

### 2. Verifying inter-site characteristics

For a stretched cluster, measure the link rather than trusting the
specification:

```bash
# Round-trip latency between sites, from an ESXi host at one site to a
# vSAN VMkernel address at the other. Watch the distribution, not the
# average — the tail is what applications feel.
vmkping -I vmk1 -c 100 -i 0.2 10.20.110.11

# And confirm jumbo frames survive the inter-site path, which is a
# common place for MTU to be silently reduced.
vmkping -I vmk1 -d -s 8972 10.20.110.11
```

The second command matters more than it looks. Inter-site links
frequently traverse equipment outside the virtualization team's control,
and an MTU reduction somewhere in that path is both common and invisible
until it is measured.

### 3. Confirming the witness is genuinely independent

```powershell
# Where does the witness actually run? This should not be either data
# site for a stretched cluster, nor either node for a two-node cluster.
$config = Get-VsanClusterConfiguration
$config.WitnessHost | Select-Object Name, ConnectionState,
  @{N='ManagedBy'; E={$_.Parent}}
```

Then confirm the answer physically. Where the witness runs and where the
inventory says it runs are the same thing right up until someone migrates
it, and nothing warns you.

### 4. Verifying backups recover

A backup job reporting success is a claim about the job, not about
recoverability. The check is a restore:

```powershell
# Restore a test VM from backup into an isolated port group, power it
# on, and verify its data — then remove it. Exact restore invocation
# depends on the backup product; the discipline does not.
Get-VM -Name 'restore-test-*' |
  Select-Object Name, PowerState, VMHost,
    @{N='RestoredOn'; E={(Get-Date -Format 'yyyy-MM-dd')}}
```

Restore into an isolated network. A restored production VM that boots
onto the production network with the same identity as the original
causes an incident during the test intended to prevent one.

## Validation and Troubleshooting

### Testing availability rather than assuming it

The claims in a design document are hypotheses until tested. The tests
that matter:

| Claim | Test |
| --- | --- |
| A host failure is absorbed | Power off a host abruptly; confirm VMs restart and vSAN objects remain accessible |
| A rack failure is absorbed | Where fault domains are configured, fail an entire domain |
| A site failure is absorbed | Isolate one site of a stretched cluster; confirm the other continues |
| The witness works | Isolate the witness; confirm the cluster continues, then confirm a subsequent node failure behaves as documented |
| Backups recover | Restore, boot, and verify — into isolation |

Note that graceful shutdown does not test the same thing as abrupt power
loss. Test the failure you are claiming to survive.

### Common findings

| Symptom | Cause |
| --- | --- |
| Objects inaccessible after losing one host, despite policy allowing it | A rebuild from an earlier failure was still in progress; failure tolerance was already spent |
| Stretched cluster write latency high | Inter-site latency above requirement, or bandwidth saturated by resync |
| Both sites active after a link failure | Witness unreachable from one or both sites — the split-brain condition |
| VMs do not restart after host failure | HA admission control exhausted, or HA disabled |
| Restore succeeds but application does not start | Backup was crash-consistent where the application needed quiescing |

The last row is the one that turns a successful backup programme into a
failed recovery, and it is found only by testing the restore rather than
the backup.

### Witness failure

A failed witness does not stop the cluster, which is why it can go
unnoticed. Monitor it explicitly. A two-node or stretched cluster running
without a witness has quietly lost the arbitration it was designed
around, and the loss becomes apparent only at the next failure — when it
matters most.

## Security and Best Practices

- **Keep at least one backup copy offline or immutable.** Ransomware that
  reaches the backup repository defeats every other control in this
  chapter. Immutability is what makes backup a genuine answer to
  ransomware rather than a nominal one; see
  [Volume VI, Chapter 08](../../volume-06-enterprise-storage-data-protection/chapters/08-storage-security-ransomware-resilience-and-data-governance.md).
- **Isolate restore testing.** Restores into production networks cause
  incidents; a dedicated isolated port group for restore verification is
  cheap and permanent.
- **Protect the witness like a cluster component.** It is small and easy
  to overlook, and compromising or losing it degrades the availability
  design without any visible symptom.
- **Encrypt inter-site vSAN traffic where the link is not fully
  trusted.** A stretched cluster carries all data across that link
  continuously.
- **Test the failure scenarios on a schedule, not once at
  commissioning.** Availability designs decay as clusters grow, policies
  change, and witnesses migrate. An untested claim ages badly.

## References and Knowledge Checks

**References**

- [Volume V, Chapter 07](../../volume-05-vmware-virtualization/chapters/07-vsphere-availability-mobility-and-cluster-services.md)
  — vSphere HA, DRS, and cluster services mechanics.
- [Volume VI, Chapter 05](../../volume-06-enterprise-storage-data-protection/chapters/05-backup-architecture-and-data-protection-policy.md)
  — backup architecture and retention policy.
- [Volume VI, Chapter 07](../../volume-06-enterprise-storage-data-protection/chapters/07-recovery-engineering-and-disaster-recovery-validation.md)
  — recovery engineering and validating that recovery works.
- [Volume XII, Chapter 02](../../volume-12-resilience-lifecycle-management/chapters/02-business-impact-analysis-and-continuity-planning.md)
  — business impact analysis, which is what determines whether a
  stretched cluster is warranted.

**Knowledge checks**

1. A stretched cluster with synchronous mirroring is hit by ransomware at
   one site. What happens, and why is this not a design flaw?
2. Where may a two-node cluster's witness *not* be placed, and what
   failure does each prohibited placement produce?
3. A cluster spans three racks. What does configuring fault domains
   change about vSAN's placement, and what does it cost?
4. Why must an inter-site link be sized for resynchronization rather than
   steady-state write traffic?
5. A backup job has reported success every night for a year. What have
   you established, and what have you not?

## Hands-On Lab

**Objective:** Test availability claims by causing the failures they
claim to survive, and validate a restore rather than a backup.

**Prerequisites:** A nested vSphere cluster with vSAN and at least four
hosts from [Volume V](../../volume-05-vmware-virtualization/README.md),
a backup product with a trial or community edition, PowerCLI, and an
isolated port group with no uplinks.

**Most of this lab is faithful.** Fault domains, witness behavior, HA
response, and restore validation are vSAN and vSphere mechanisms that
VxRail inherits unchanged. A nested environment can even build a
stretched cluster configuration, though its latency characteristics will
be nothing like a real inter-site link.

**Procedure**

1. Run the availability audit and record which policies protect what
   proportion of your estate by capacity.
2. Configure fault domains grouping your hosts into two or three domains.
   Observe how vSAN redistributes object components in response.
3. Abruptly power off one host — not a graceful shutdown. Time how long
   until VMs restart and until vSAN reports objects fully compliant
   again. These are two different durations and the second is longer.
4. Build a two-node cluster configuration with a witness appliance hosted
   outside both nodes.
5. Isolate the witness from both nodes and confirm the cluster continues
   operating. Then, with the witness still isolated, fail one node and
   observe the result. Restore the witness afterwards.
6. Configure a backup of several test VMs, run it, then restore one into
   the isolated port group. Power it on and verify its data is present
   and current.

**Negative test**

7. While the cluster is still rebuilding from the step 3 failure, fail a
   second host. Confirm that objects become inaccessible even though the
   applied policy nominally tolerates a failure — because that tolerance
   was already spent on the first failure and not yet restored. This is
   the first row of the troubleshooting table, and it is the single most
   important availability behavior in this chapter to have seen.
8. Restore both hosts and allow the cluster to return to full compliance.

**Expected results**

- A measured gap between "VMs restarted" and "redundancy restored", which
  is the window during which the cluster is not protected.
- Direct observation that a witness loss is silent until the next
  failure.
- A restore verified by booting and inspecting data, not by reading a job
  report.
- A demonstrated second-failure-during-rebuild data unavailability event.

**Cleanup**

9. Remove restored test VMs and the isolated port group's contents,
   return fault domain configuration to its original state, and allow all
   resync to complete before leaving the cluster.

## Summary and Completion Checklist

Availability, replication, and backup solve three different problems, and
the most consequential error in this chapter's subject matter is treating
one as a substitute for another — a stretched cluster replicates
ransomware to the second site perfectly. Availability layers stack from
drive to host to rack to site, with fault domains aligning vSAN placement
to physical reality and witnesses providing arbitration for two-node and
stretched configurations, where witness independence is the entire
design. Stretched clusters buy site-loss survival with no data loss, at
the price of synchronous write latency, doubled capacity, and demanding
link requirements. And every one of these claims is a hypothesis until it
has been tested by causing the failure it claims to survive — including
the backup, which is validated by restoring, never by reading a job
report.

- [ ] Can state what availability protects against and what it does not.
- [ ] Can place a witness correctly and enumerate the prohibited
      placements.
- [ ] Can explain stretched cluster requirements and their real costs.
- [ ] Can configure fault domains appropriately, including knowing when
      not to.
- [ ] Has tested a host failure abruptly and measured both recovery
      durations.
- [ ] Has validated a restore into isolation rather than trusting a
      backup report.
