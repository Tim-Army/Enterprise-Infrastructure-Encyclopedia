# Chapter 05: Cluster Expansion, Scale-Out, and Capacity Planning

## Learning Objectives

- Add a node to a running VxRail cluster and explain what the operation
  does at each stage.
- Explain why a new node must be version-matched before it can join, and
  how that is achieved.
- Distinguish scaling out, scaling up, and adding capacity, and select
  the right one for a stated shortage.
- Build a capacity model that accounts for policy overhead, slack space,
  and admission control rather than raw drive totals.
- Remove or replace a node without leaving the cluster in an
  unsupported state.

## Theory and Architecture

### Node addition, stage by stage

Adding a node to a VxRail cluster is a VxRail Manager operation, not a
vCenter one. Racking the server and adding it to the cluster in the
vSphere Client is the wrong procedure and produces a host the platform
does not manage.

The supported sequence is:

1. **Rack, cable, and power the node** to the same fabric as the cluster,
   with the same VLANs — including the internal management VLAN, because
   discovery works the same way it did at deployment.
2. **VxRail Manager discovers the node** through the same IPv6 multicast
   mechanism from [Chapter 02](02-physical-installation-network-prerequisites-and-pre-deployment-planning.md).
   A node that does not appear is almost always a fabric problem, and the
   diagnosis is identical to the deployment-time one.
3. **Version reconciliation.** The node must be running the same VxRail
   version as the cluster. Where it is not — and a node shipped from
   Dell frequently is not — it must be brought to the cluster's version
   before it can join.
4. **Configuration and join.** VxRail Manager applies management
   networking, adds the host to vCenter, joins it to the cluster,
   configures VMkernel adapters on the distributed switch, and adds its
   drives to the vSAN datastore.
5. **Rebalance.** vSAN redistributes data to make use of the new
   capacity. This is background work and it takes time proportional to
   how much data exists.

### Why version matching is the awkward part

A node arriving from Dell carries whatever VxRail version was current
when it was built. The running cluster carries whatever version it was
last upgraded to. These are rarely the same, and the mismatch has to be
resolved in one direction or the other:

- **Bring the node up to the cluster's version.** The usual answer where
  the cluster is current.
- **Bring the cluster up to the node's version first.** Sometimes
  necessary where the node ships newer than the cluster, and it converts
  a node addition into a lifecycle upgrade — a much larger change window
  than expected.

The planning consequence is worth stating clearly: **check the incoming
node's version against the cluster before scheduling the expansion
window.** An expansion that quietly requires a cluster upgrade first is
the difference between a two-hour task and a two-evening one, and finding
that out on the night is avoidable.

### Scale out, scale up, and add capacity

Three different shortages have three different remedies, and conflating
them is expensive:

| Shortage | Remedy | Note |
| --- | --- | --- |
| Cores or memory exhausted, capacity fine | Add a node, or add memory to existing nodes | Memory upgrades avoid buying capacity you do not need |
| Capacity exhausted, cores fine | Add drives to existing nodes, or add a storage-dense node | Drive addition is limited by the node's remaining slots |
| Both exhausted proportionally | Add a node | The clean case, and the one HCI is designed for |
| Failure tolerance insufficient | Add a node | More fault domains, not more space |

Note the last row. A cluster that cannot satisfy a desired storage policy
needs more *hosts*, not more *drives* — adding capacity to three hosts
does not make a four-host policy satisfiable. This is the same
node-count-floor issue from
[Chapter 04](04-vsphere-and-vsan-integration-and-the-division-of-management.md),
seen from the procurement side.

### Cluster maximums and node heterogeneity

Clusters have an upper node count, set by the vSphere cluster maximum
rather than by VxRail. Approaching it is a reason to plan a second
cluster rather than to keep adding.

Nodes within a cluster need not be identical, but heterogeneity has
costs. Mixed node sizes complicate DRS balancing and admission control —
the failover capacity that must be reserved is driven by the largest
host — and mixed drive configurations complicate vSAN capacity
distribution. Some mixing is supported and normal over a cluster's life
as generations change; deliberate heterogeneity for its own sake is
rarely worth it.

### Capacity planning that survives contact with production

Raw drive capacity is the least useful number in a VxRail capacity
conversation. The chain from raw to genuinely usable removes capacity at
each step:

1. **Raw capacity** — the sum of the capacity drives.
2. **Less formatting and metadata overhead** — vSAN's own consumption.
3. **Divided by the policy multiplier** — roughly 2x for mirroring, 1.33x
   to 1.5x for erasure coding, from
   [Chapter 04](04-vsphere-and-vsan-integration-and-the-division-of-management.md).
4. **Less slack space for rebuilds and resync** — vSAN needs free
   capacity to rebuild into after a failure. A cluster at 95% cannot
   self-heal, which means it has no failure tolerance regardless of what
   its policy says.
5. **Less admission control reservation** — capacity reserved for host
   failure is capacity you cannot fill.

**Step 4 is the one that gets skipped and the one that matters most.**
Free capacity on a vSAN cluster is not spare, it is functional: it is the
space a rebuild happens in. A cluster planned to run at 90% full has,
in practical terms, traded its resilience away without anyone deciding
to.

Plan to a target utilization that leaves genuine headroom, and treat
crossing it as a procurement trigger rather than a warning to acknowledge
and dismiss.

### Node removal and replacement

Removing a node is also a VxRail Manager operation. Doing it through
vCenter leaves VxRail Manager with a cluster definition that does not
match reality.

Before removal, the cluster must be able to tolerate the loss: enough
remaining hosts to satisfy every applied storage policy, and enough
remaining capacity to hold the data currently on the departing node.
Removal evacuates that node's data across the remaining hosts, and if
they cannot hold it, the operation cannot complete.

Replacement of a *failed* node is a different procedure again, and it is
a Dell support engagement rather than a self-service operation in most
support arrangements.

## Design Considerations

- **Plan expansion at the sizing stage, not at the shortage.** Leaving
  address range headroom (Chapter 02), rack space, switch ports, and
  power for the next node costs nothing at build time and is disruptive
  to retrofit.
- **Buy the node before you need it, not when you need it.** Lead times
  plus version reconciliation plus a change window is a long path, and it
  starts from a cluster that is already short.
- **Prefer a memory upgrade to a node where the shortage is memory
  alone.** It is cheaper and it does not add capacity you have no use
  for — one of the few available escapes from coupled scaling.
- **Set the capacity trigger well below the danger point.** If the
  cluster becomes unable to self-heal at 90%, the procurement trigger
  belongs somewhere closer to 70%, because procurement takes time.
- **Reserve switch ports for growth.** A cluster that cannot expand
  because the top-of-rack switch is full is a common and entirely
  self-inflicted constraint.
- **Consider whether a second cluster is the better answer.** Beyond a
  point, a second cluster gives a separate failure domain, a separate
  maintenance window, and separate blast radius — often worth more than
  the marginal efficiency of one large cluster.

## Implementation and Automation

### 1. Establishing the real capacity position

Before deciding what to buy, measure what exists. Raw totals are not the
answer:

```powershell
Connect-VIServer -Server vcsa-01.lab.example.com

# vSAN datastore capacity and actual free space.
Get-Datastore | Where-Object { $_.Type -eq 'vsan' } |
  Select-Object Name,
    @{N='CapacityTB';  E={[math]::Round($_.CapacityGB / 1024, 2)}},
    @{N='FreeTB';      E={[math]::Round($_.FreeSpaceGB / 1024, 2)}},
    @{N='UsedPercent'; E={[math]::Round(
        (($_.CapacityGB - $_.FreeSpaceGB) / $_.CapacityGB) * 100, 1)}}

# Compute position, including what admission control has reserved.
$cluster = Get-Cluster
Get-VMHost | Measure-Object -Property NumCpu, MemoryTotalGB -Sum |
  Select-Object Property, Sum

$cluster | Select-Object Name, HAAdmissionControlEnabled, HAFailoverLevel
```

A `UsedPercent` above the threshold you set in *Design Considerations* is
the number that triggers procurement, not the free-space figure in
terabytes — percentages carry the resilience meaning that absolute
figures do not.

### 2. Projecting when capacity runs out

A point-in-time figure does not tell you when to buy. Growth rate does:

```powershell
# Append a dated capacity sample. Run on a schedule; the value is in the
# series, not in any single reading.
$ds = Get-Datastore | Where-Object { $_.Type -eq 'vsan' }
[pscustomobject]@{
  Date       = (Get-Date -Format 'yyyy-MM-dd')
  CapacityGB = [math]::Round($ds.CapacityGB, 0)
  FreeGB     = [math]::Round($ds.FreeSpaceGB, 0)
  UsedGB     = [math]::Round($ds.CapacityGB - $ds.FreeSpaceGB, 0)
} | Export-Csv -Path ./vxrail-capacity-history.csv -Append -NoTypeInformation
```

With several months of samples, the growth rate and the date the trigger
threshold is crossed both fall out of simple arithmetic — and a
procurement conversation backed by a trend line is a materially different
conversation from one backed by an alarm.

### 3. Checking a candidate node before the expansion window

```bash
# On the incoming node, once it is powered and reachable: confirm the
# version against what the cluster runs.
esxcli system version get
```

Compare against the cluster's version from
[Chapter 03](03-vxrail-manager-deployment-and-first-run-configuration.md)'s
verification block. A mismatch is expected; an *unnoticed* mismatch is
what turns an expansion into an incident.

### 4. Watching the post-expansion rebalance

```bash
# vSAN rebalance and resync activity after a node joins.
esxcli vsan debug resync summary get
```

The cluster is usable during rebalance but is doing background work.
Adding a node and immediately deploying workloads onto it means competing
with that work.

## Validation and Troubleshooting

### The new node does not appear

Identical diagnosis to deployment: IPv6 multicast on the internal
management VLAN, or MLD snooping without a querier. If the node was
cabled to a switch port configured for a different purpose — the most
common cause of the "expansion-only" version of this failure — the port
is missing the discovery VLAN.

### The join fails on version mismatch

Expected and correct. The remedy is to bring the node to the cluster's
version, or the cluster to the node's, as described above. It is not to
retry.

### Removal will not complete

Almost always one of two conditions:

| Condition | Check |
| --- | --- |
| Remaining hosts cannot satisfy an applied storage policy | Count hosts against the strictest policy in use |
| Remaining capacity cannot hold the evacuated data | Compare the node's used capacity against remaining free space |

Both are arithmetic that can be done before starting the removal, and
both produce an operation that stalls partway rather than failing
cleanly if they are not.

### Capacity appears to drop after adding a node

Not a fault. A rebalance in progress temporarily consumes capacity as
objects are rebuilt in their new positions before the old copies are
removed. Confirm the resync is progressing and re-measure once it
completes.

### The cluster is full and cannot rebuild

The condition described in the theory section, now real. There is no
elegant recovery: the options are to free capacity by deleting or
migrating workloads, or to add capacity. Neither is fast. This is the
failure the procurement trigger exists to prevent, and it is worth
treating a threshold crossing as a genuine deadline for that reason.

## Security and Best Practices

- **Bring a new node under the same access controls as the cluster
  before it carries workloads.** Its iDRAC in particular is a new
  management endpoint that needs the treatment
  [Volume XXIII, Chapter 04](../../volume-23-dell-idrac-9-10-administration/chapters/04-identity-certificates-security-and-compliance.md)
  describes, not defaults.
- **Update the deployment plan and baseline after every expansion.** A
  cluster whose documented composition does not match reality is one that
  will be troubleshot against a false premise.
- **Wipe or securely handle drives from removed nodes.** A node leaving
  the cluster carries copies of workload data on its drives; removal
  evacuates the cluster's dependency on it, not the data from it.
- **Track expansion against entitlement.** Support and licensing
  positions change with node count, and discovering a gap during an
  incident is the worst time to discover it.

## References and Knowledge Checks

**References**

- [Dell VxRail product documentation](https://www.dell.com/support/home/en-us/product-support/product/vxrail-appliance-series/docs)
  — the administration guide is authoritative for node addition, removal,
  and cluster maximums.
- [Volume V, Chapter 06](../../volume-05-vmware-virtualization/chapters/06-vsphere-storage-and-vsan.md)
  — vSAN capacity mechanics, slack space, and rebuild behavior.
- [Chapter 02](02-physical-installation-network-prerequisites-and-pre-deployment-planning.md)
  — the discovery requirements a new node depends on, unchanged from
  deployment.
- [Chapter 04](04-vsphere-and-vsan-integration-and-the-division-of-management.md)
  — storage policies and the node-count floors that drive several
  expansion decisions.

**Knowledge checks**

1. Why is a node addition performed through VxRail Manager rather than
   through vCenter, and what is wrong with the result if it is not?
2. A new node ships at a newer VxRail version than the cluster. What does
   that turn the expansion into, and why does it matter for planning?
3. A three-host cluster is out of capacity and cannot satisfy the desired
   policy. Which of "add drives" and "add a node" fixes which problem?
4. Why is free capacity on a vSAN cluster functional rather than spare?
5. Give the two arithmetic checks that predict whether a node removal
   will complete.

## Hands-On Lab

**Objective:** Build a capacity model from measured data, project a
procurement trigger date, and observe expansion and removal behavior on a
nested cluster.

**Prerequisites:** A nested vSphere cluster with vSAN from
[Volume V](../../volume-05-vmware-virtualization/README.md) with at least
four hosts, PowerCLI, and enough test data to make capacity movement
visible.

**The expansion mechanics here are vSAN's, not VxRail's.** VxRail
Manager's orchestration of a node addition cannot be reproduced without
hardware. The capacity modelling, the rebalance behavior, and the removal
preconditions all can be, and they are the parts that determine whether
an expansion is planned correctly.

**Procedure**

1. Run the capacity position commands and record raw capacity, free
   capacity, and used percentage.
2. Compute usable capacity by hand through the five-step chain from the
   theory section, using your cluster's actual policy. Compare the result
   against the raw figure and note the ratio.
3. Take capacity samples using the history script, then generate
   artificial growth by deploying test VMs, sampling after each. Build a
   series of at least five points.
4. From the series, compute the growth rate per day and project the date
   your chosen trigger threshold would be crossed.
5. Put a host into maintenance mode with full data migration and time it.
   Record how long the cluster spent at reduced redundancy.
6. Remove a host from the vSAN cluster and observe the evacuation, then
   add it back and observe the rebalance.

**Negative test**

7. Fill the cluster to above 90% with test data, then attempt to put a
   host into maintenance mode with full data migration. Confirm it cannot
   complete because the remaining hosts have nowhere to put the data —
   the "cannot self-heal" condition made concrete. Note that the cluster
   was reporting healthy immediately beforehand.
8. Delete test data to bring utilization back below the trigger
   threshold and confirm the operation then succeeds.

**Expected results**

- A usable-to-raw capacity ratio measured on your own cluster, which will
  be substantially below one.
- A projected trigger date derived from a growth series rather than a
  guess.
- Direct observation that a nearly full vSAN cluster loses the ability to
  perform maintenance while still reporting itself healthy.

**Cleanup**

9. Remove test VMs, allow resync to complete, and retain the capacity
   history CSV — it is the input to the day-2 operations work in
   [Chapter 09](09-day-2-operations-troubleshooting-support-and-capstone.md).

## Summary and Completion Checklist

Expansion is a VxRail Manager operation whose most common planning
failure is version mismatch discovered too late, turning a node addition
into a cluster upgrade. The right remedy for a shortage depends on which
shortage it is: nodes add fault domains, drives add capacity, and memory
adds memory — and only more hosts make a stricter storage policy
satisfiable. Capacity planning must run the full chain from raw to usable
and must treat slack space as functional rather than spare, because a
cluster too full to rebuild has silently given up the resilience its
policy claims. Set the procurement trigger far enough below that point
that procurement can actually complete.

- [ ] Can describe the five stages of node addition and why each matters.
- [ ] Checks incoming node versions before scheduling an expansion.
- [ ] Can match a shortage to the correct remedy, including the
      fault-domain case.
- [ ] Can compute usable capacity through the full five-step chain.
- [ ] Maintains a capacity series and a trigger threshold rather than a
      point-in-time figure.
- [ ] Can predict whether a node removal will complete before starting
      it.
