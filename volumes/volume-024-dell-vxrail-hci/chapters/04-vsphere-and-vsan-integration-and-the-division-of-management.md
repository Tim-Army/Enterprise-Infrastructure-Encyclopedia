# Chapter 04: vSphere and vSAN Integration and the Division of Management

## Learning Objectives

- State precisely which parts of the vSphere stack VxRail owns and which
  remain the administrator's.
- Apply vSAN storage policies on VxRail and predict their capacity
  consequences.
- Use vSphere cluster services — HA, DRS, and maintenance mode — with the
  constraints VxRail imposes.
- Recognize the operations that are routine on a self-built cluster and
  unsupported on VxRail, and explain why.
- Verify that a cluster's configuration still matches what VxRail
  Manager expects.

## Theory and Architecture

### The division of management, stated plainly

This is the chapter a vSphere administrator most needs and is least
likely to be given. VxRail's documentation describes what VxRail manages;
vSphere's documentation describes what vSphere can do. The gap between
them is where administrators get into trouble.

| Domain | Owned by | Notes |
| --- | --- | --- |
| Node firmware, BIOS, drivers | **VxRail** | Delivered only through the lifecycle bundle |
| ESXi version and patching | **VxRail** | Never patched independently |
| vCenter version (VxRail-managed topology) | **VxRail** | Customer-managed vCenter moves this to you |
| VxRail-created distributed switch and its port groups | **VxRail** | Visible and editable in vCenter, but not yours to edit |
| Management VMkernel adapters (vSAN, vMotion, management) | **VxRail** | Created and tracked by VxRail Manager |
| vSAN storage policies | **You** | Ordinary vSphere administration |
| Guest VM port groups on the VxRail VDS | **You** | Adding workload port groups is expected and supported |
| Virtual machines, resource pools, folders | **You** | Entirely ordinary |
| HA and DRS settings | **You**, within limits | See below |
| Host maintenance mode | **You**, with VxRail-aware caveats | See below |

The rule that generalizes across the table: **VxRail owns the platform's
own configuration; you own what runs on it.** Where an object was created
by VxRail Manager, treat it as read-only unless documentation says
otherwise. Where you created it, it is yours.

### vSAN on VxRail: the same technology, a narrower remit

vSAN's mechanics on VxRail are the mechanics covered in
[Volume V, Chapter 06](../../volume-005-vmware-virtualization/chapters/06-vsphere-storage-and-vsan.md).
Objects, components, witness components, storage policies, and the
distinction between mirroring and erasure coding all behave identically.
This volume does not re-teach them.

What differs is the surrounding autonomy. The disk groups or storage
pools were built by VxRail to a validated configuration, the drives are
Dell-qualified parts, and drive replacement follows a VxRail procedure
rather than a vSAN one. Adding capacity is a Chapter 05 operation, not a
vSphere Client operation.

**Storage policies, however, are fully yours.** This is worth stating
explicitly because administrators arriving from Chapter 01's
validated-state material sometimes over-generalize it and become
reluctant to touch anything. Creating, assigning, and changing vSAN
storage policies is ordinary, supported, expected administration, and it
is the single most consequential lever you have over the cluster's
usable capacity and resilience.

### Storage policy consequences, concretely

The policy applied to a virtual machine determines how many copies of its
data exist and therefore how much raw capacity it consumes. The two
choices that matter most:

| Approach | Raw capacity per usable TB | Failure tolerance | Cost |
| --- | --- | --- | --- |
| Mirroring (RAID 1 style) | Roughly 2x for one failure, 3x for two | Fast rebuilds, high write performance | Capacity-expensive |
| Erasure coding (RAID 5/6 style) | Roughly 1.33x–1.5x | Same nominal tolerance, more overhead per write | CPU and write-amplification cost |

Erasure coding also carries a node-count floor — it requires more hosts
than mirroring to satisfy the same failure tolerance — which is why a
small cluster may have no choice. Confirm the current minimums for the
vSAN architecture your nodes run against the vSAN documentation rather
than from memory; they have changed across vSAN generations.

The practical point for VxRail specifically: a cluster sized on mirroring
and later moved to erasure coding gains substantial usable capacity
without buying hardware, and a cluster sized on erasure coding that
cannot meet its node-count floor has a capacity problem that no policy
change will fix. Both situations are common, and both are decided by the
sizing work in [Chapter 01](01-hci-architecture-vxrail-positioning-and-platform-models.md).

### Cluster services: HA, DRS, and what VxRail assumes

HA and DRS are configured through vCenter as usual, and tuning them is
yours to do. Two VxRail-specific considerations apply.

**DRS matters more on VxRail than on a self-built cluster** because
VxRail's lifecycle operations depend on it. A bundle upgrade puts each
host into maintenance mode in turn, and that requires somewhere for the
workloads to go. A cluster with DRS disabled, or set to manual, turns an
unattended overnight upgrade into an attended one. Fully automated DRS is
the configuration VxRail's lifecycle assumes.

**HA admission control has a capacity conversation attached.** Reserving
capacity for host failure is correct, and on a small cluster the reserved
fraction is large: one host of three is a third of the cluster. Sizing
that ignored admission control produces a cluster that is technically
adequate and practically full.

### Maintenance mode, and why vSAN changes it

On a cluster without vSAN, maintenance mode moves virtual machines off a
host. On vSAN, the host also holds data, and maintenance mode must decide
what happens to it. The options are the standard vSAN ones — ensure
accessibility, full data migration, or no data migration — and choosing
between them is a real decision with real duration consequences.

Full data migration on a large host is not a quick operation, and
starting one without knowing that is a recurring source of surprise.
Ensure accessibility is faster and leaves the cluster with reduced
redundancy while the host is out. Neither is universally correct.

VxRail's own lifecycle operations handle this selection themselves during
a bundle upgrade, which is one of the concrete things the orchestration
buys.

### Operations that are supported on vSphere and not on VxRail

The list is short and worth memorizing:

- Patching ESXi from a VMware bundle, vSphere Lifecycle Manager baseline,
  or `esxcli` — **not supported**; use the VxRail bundle.
- Updating node firmware through PowerEdge tooling, iDRAC, or OpenManage
  — **not supported**; use the VxRail bundle.
- Editing or deleting VxRail-created distributed switch objects,
  VMkernel adapters, or port groups — **not supported**.
- Removing a host from the cluster through vCenter — **not supported**;
  node removal is a VxRail Manager operation
  ([Chapter 05](05-cluster-expansion-scale-out-and-capacity-planning.md)).
- Renaming VxRail-managed objects — **avoid**; VxRail Manager tracks them
  by name in places.

Everything else — VMs, policies, resource pools, workload networking,
permissions, tags — is ordinary vSphere administration and should be
treated as such.

## Design Considerations

- **Choose the storage policy deliberately and revisit it.** It is the
  highest-leverage capacity decision available after purchase, and the
  default is rarely the right long-term answer for the whole estate.
- **Do not apply one policy to everything.** Different workloads warrant
  different resilience. A test estate on erasure coding and a production
  database on mirroring is a sensible outcome, not an inconsistency.
- **Set DRS to fully automated unless you have a specific reason not
  to.** VxRail lifecycle assumes it, and the reason for any deviation
  should be recorded so the next upgrade window does not rediscover it.
- **Size admission control into the capacity plan.** Reserved failover
  capacity is capacity you cannot use, and on small clusters it dominates.
- **Add workload port groups to the VxRail VDS rather than building a
  parallel switch.** Adding port groups is supported and keeps workload
  networking where the cluster's teaming and failover policy already
  applies.
- **Document the division of management for your operations team.** The
  table at the top of this chapter is the single most useful thing to put
  in front of a vSphere administrator who is new to VxRail, and its
  absence is why clusters end up out of validated state.

## Implementation and Automation

### 1. Auditing the current storage policy landscape

Before changing anything, establish what is actually applied:

```powershell
Connect-VIServer -Server vcsa-01.lab.example.com

# What policies exist, and what each one asks for.
Get-SpbmStoragePolicy |
  Select-Object Name, Description,
    @{N='Rules'; E={($_.AnyOfRuleSets.AllOfRules |
        ForEach-Object { "$($_.Capability.Name)=$($_.Value)" }) -join '; '}} |
  Format-Table -AutoSize

# Which VMs use which policy — the distribution matters more than the list.
Get-VM | ForEach-Object {
  [pscustomobject]@{
    VM     = $_.Name
    Policy = (Get-SpbmEntityConfiguration $_).StoragePolicy.Name
    UsedGB = [math]::Round($_.UsedSpaceGB, 1)
  }
} | Group-Object Policy |
    Select-Object Name, Count,
      @{N='TotalUsedGB'; E={[math]::Round(($_.Group.UsedGB | Measure-Object -Sum).Sum, 1)}}
```

The grouped output is the useful one: it shows how much capacity each
policy is responsible for, which is what a policy change will actually
move.

### 2. Creating a policy and applying it to a subset

```powershell
# An erasure-coding policy for workloads that do not need mirroring.
New-SpbmStoragePolicy -Name 'vSAN-EC-FTT1' `
  -AnyOfRuleSets (
    New-SpbmRuleSet -AllOfRules @(
      New-SpbmRule -Capability 'VSAN.hostFailuresToTolerate' -Value 1
      New-SpbmRule -Capability 'VSAN.replicaPreference' `
                   -Value 'RAID-5/6 (Erasure Coding) - Capacity'
    )
  )

# Apply to a tagged subset rather than everything at once.
Get-VM -Tag 'tier-test' |
  Set-SpbmEntityConfiguration -StoragePolicy 'vSAN-EC-FTT1'
```

Applying a policy triggers a resynchronization: vSAN rebuilds the objects
to match the new layout. On a populated cluster this generates
substantial traffic and takes time. Do it in a window and to a subset.

### 3. Watching resynchronization

```bash
# From an ESXi host — how much is left to move.
esxcli vsan debug resync summary get
```

```powershell
# Or, from PowerCLI, at the cluster level.
Get-VsanResyncingComponent -Cluster 'vxrail-lab-01' |
  Measure-Object -Property BytesLeftToResync -Sum |
  Select-Object @{N='GBRemaining'; E={[math]::Round($_.Sum / 1GB, 1)}}
```

A resync that is not shrinking over time is a problem worth
investigating before it becomes a capacity problem.

### 4. Checking DRS and admission control against VxRail's assumptions

```powershell
Get-Cluster | Select-Object Name,
  DrsEnabled, DrsAutomationLevel,
  HAEnabled, HAAdmissionControlEnabled,
  @{N='HAFailoverLevel'; E={$_.HAFailoverLevel}}
```

`DrsAutomationLevel` should read `FullyAutomated` for lifecycle
operations to run unattended.

## Validation and Troubleshooting

### Confirming the cluster is still in the state VxRail expects

Configuration drift on VxRail is not a tidiness problem, it is a
supportability problem. The check that matters is whether vSAN health and
VxRail Manager both report a clean cluster:

```bash
# vSAN's own health assessment, which covers policy compliance,
# network, and hardware compatibility.
esxcli vsan health cluster list
```

VxRail Manager's health view in the vSphere Client covers the
VxRail-specific half — node state, validated-state alignment, and
appliance health — and both need to be clean. A cluster where vSAN health
is green and VxRail Manager is not is exactly the drift condition this
chapter is written to prevent.

### Storage policy non-compliance

A VM reporting non-compliance means its objects do not currently satisfy
its policy. The causes divide cleanly:

| Cause | Resolution |
| --- | --- |
| Resync in progress after a policy change | Wait; confirm it is progressing |
| Insufficient hosts for the policy's requirements | Reduce the policy's requirements or add nodes |
| Insufficient free capacity to build the new layout | Free capacity or stage the change |
| Host or disk failure reducing available fault domains | Address the hardware fault |

The second is the one that catches people: a policy can be created and
applied on a cluster that cannot satisfy it, and the failure appears as
persistent non-compliance rather than as a rejected change.

### After an unsupported change has already been made

If a VxRail-owned object has been edited by hand — it happens, usually by
someone who did not know — do not compound it by editing further. Record
exactly what was changed, then engage Dell support. VxRail Manager may be
able to reconcile the object, and support has procedures for it. An
improvised repair frequently produces a cluster that is harder to fix
than the original mistake.

## Security and Best Practices

- **Use vCenter roles to make the division of management enforceable.**
  The table at the top of this chapter is advice until permissions make
  it structural. Restricting who can edit distributed switch objects
  turns a documented convention into a control.
- **Tag workloads by resilience tier.** Policy assignment by tag is
  auditable and repeatable; policy assignment by hand is neither, and it
  is how production workloads end up on test-grade resilience.
- **Do not disable admission control to solve a capacity problem.** It
  converts a visible capacity shortage into an invisible one that
  surfaces during a host failure.
- **Keep vSAN encryption decisions with the storage design, not as an
  afterthought.** Enabling data-at-rest encryption on a populated cluster
  is a substantial operation; the corresponding key-management
  requirements are covered in
  [Volume VI, Chapter 08](../../volume-006-enterprise-storage-data-protection/chapters/08-storage-security-ransomware-resilience-and-data-governance.md).
- **Review policy assignment periodically.** Workloads change tier over
  their lifetime and almost nobody revisits the policy when they do.

## References and Knowledge Checks

**References**

- [Volume V, Chapter 06](../../volume-005-vmware-virtualization/chapters/06-vsphere-storage-and-vsan.md)
  — vSAN architecture, objects, and storage policies in full; this
  chapter assumes rather than repeats it.
- [Volume V, Chapter 07](../../volume-005-vmware-virtualization/chapters/07-vsphere-availability-mobility-and-cluster-services.md)
  — HA, DRS, and maintenance mode mechanics.
- [Volume VI, Chapter 08](../../volume-006-enterprise-storage-data-protection/chapters/08-storage-security-ransomware-resilience-and-data-governance.md)
  — storage encryption and key management.
- [Dell VxRail product documentation](https://www.dell.com/support/home/en-us/product-support/product/vxrail-appliance-series/docs)
  — the administration guide is authoritative on which operations are
  supported.

**Knowledge checks**

1. Give the general rule that determines whether an object on a VxRail
   cluster is yours to edit, and apply it to: a guest port group, a
   VMkernel adapter, and a resource pool.
2. A three-node cluster cannot satisfy an erasure-coding policy. How does
   that failure present itself, and why is it not rejected at creation?
3. Why does VxRail's lifecycle process assume fully automated DRS, and
   what happens if it is set to manual?
4. Explain the trade between "ensure accessibility" and "full data
   migration" when entering maintenance mode.
5. Someone has edited a VxRail-created port group. What is the correct
   next action, and why is it not "change it back"?

## Hands-On Lab

This chapter carries a topic-level walkthrough lab for **each theme of vSphere/vSAN integration and
the division of management** — the vCenter/VxRail-plugin relationship, the vSAN datastore and
policies, what VxRail owns versus vCenter, and vSAN health. It builds on Volume V's vSphere/vSAN
foundation. Each ends **`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 4.1–4.4** — a deployed VxRail cluster, vSphere Client access, and
the VxRail API. **Cost:** none.

### Lab 4.1 — vCenter and the VxRail plugin (Topic: vSphere integration)

**Objective:** Locate VxRail management inside vCenter.

```text
# In the vSphere Client: open the cluster > Configure > VxRail.
#   Confirm the VxRail plugin shows: system health, hosts/chassis, and the "Add VxRail Hosts",
#   "Updates" (LCM), and support panels — VxRail management lives inside vCenter, not a separate UI.
```

**Expected result:** the VxRail management panels appear within the vSphere Client via the plugin —
VxRail integrates *into* vCenter: day-to-day VxRail operations (add hosts, LCM, health) are driven
from the vSphere Client's VxRail plugin, so operators work in one console, not two.

**Negative test:** look for a wholly separate VxRail admin console for daily operations; the primary
management surface is the vCenter plugin — knowing where VxRail functions live in vCenter is an
exam and operational essential.

**Cleanup:** none (read-only).

### Lab 4.2 — The vSAN datastore and storage policies (Topic: vSAN storage)

**Objective:** Read the vSAN datastore and apply a storage policy.

```text
# vSphere Client: Cluster > Datastores > the vSAN datastore (usable capacity, from disk groups).
#   Policies and Profiles > VM Storage Policies: review the vSAN Default Storage Policy
#   (FTT=1, RAID-1) and create a policy (e.g. FTT=1 RAID-5) for a workload; assign it to a VM.
```

**Expected result:** the single vSAN datastore spans all nodes' disk groups, and a storage policy
(FTT/RAID) governs per-VM resilience and efficiency — vSAN presents one policy-driven datastore;
the storage policy (not LUN placement) decides how many failures a VM tolerates and its space
overhead.

**Negative test:** expect to place a VM on a specific disk for performance the way you would on a
SAN; vSAN is policy-driven and object-distributed — you set intent (FTT, stripe, RAID) via policy,
not manual placement.

**Cleanup:** revert the lab VM to the default policy; delete the lab policy if unused.

### Lab 4.3 — The division of management (Topic: Management boundaries)

**Objective:** Distinguish what VxRail owns from what vCenter owns.

```text
# Classify common tasks:
#   VxRail owns  -> node add/remove, LCM (firmware+ESXi+vSAN+vCenter bundle), hardware health,
#                   support/telemetry, the Continuously Validated State
#   vCenter owns -> VMs, resource pools, DRS/HA, networking (vDS), permissions, standard vSphere ops
```

**Expected result:** a clear split — VxRail owns the *platform lifecycle and hardware*, vCenter
owns *virtualization operations* — this division is the core operating model: you never patch ESXi
or firmware by hand (that is VxRail LCM), but you run VMs/DRS/HA normally through vCenter.

**Negative test:** upgrade ESXi through the standard vSphere Lifecycle Manager on a VxRail; you
break the validated state and the supported path — ESXi/firmware updates must go through VxRail LCM
(Chapter 06), which is the boundary this lab establishes.

**Cleanup:** none.

### Lab 4.4 — vSAN health check (Topic: Storage health)

**Objective:** Confirm vSAN is healthy end to end.

```text
# vSphere Client: Cluster > Monitor > vSAN > Skyline Health.
#   Review all checks (network, physical disk, data, cluster); resolve any red/yellow.
```

Verify overall system health via the API:

```bash
curl -sk -u 'administrator@vsphere.local:<pass>' https://<vxm>/rest/vxm/v1/system | \
  python3 -c "import json,sys; print('system health:', json.load(sys.stdin).get('health'))"
```

**Expected result:** vSAN Skyline Health passes all checks and the VxRail system reports healthy —
vSAN health is the definitive storage check (network config, disk balance, object compliance), and
on VxRail it should be watched continuously because storage underpins every workload.

**Negative test:** ignore a yellow vSAN network health check (e.g. MTU mismatch); under load it
becomes packet loss and degraded VMs — Skyline Health surfaces it early, so a clean health check is
the bar before and after any change.

**Cleanup:** none (read-only).

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

VxRail owns the platform's own configuration — firmware, hypervisor
version, and the networking objects it created — while everything running
on the platform remains ordinary vSphere administration. Storage policies
sit firmly on your side of that line and are the highest-leverage lever
you have over usable capacity and resilience after purchase. The
operations that are unsupported form a short, learnable list, and every
item on it exists to protect the continuously validated state. Where a
cluster has drifted, vSAN health and VxRail Manager health must both be
clean, and an unsupported change already made is a support case rather
than a repair to improvise.

- [ ] Can state the ownership rule and apply it to an unfamiliar object.
- [ ] Can predict the capacity consequence of a mirroring-to-erasure-
      coding change and has measured one.
- [ ] Can list the operations that are unsupported on VxRail but routine
      on vSphere.
- [ ] Can explain why VxRail lifecycle assumes fully automated DRS.
- [ ] Can diagnose persistent storage policy non-compliance to its cause.
- [ ] Knows the correct response to an unsupported change already made.
