# Chapter 06: Lifecycle Management and the Continuously Validated State

## Learning Objectives

- Explain what a VxRail lifecycle bundle contains and why it is applied
  as a unit.
- Plan and execute a cluster upgrade, including pre-checks, sequencing,
  and duration estimation.
- Choose between connected and offline upgrade paths and prepare for
  each.
- Diagnose an upgrade that stalls, and know which failures are yours to
  resolve and which are support cases.
- Maintain validated-state alignment as an ongoing operational practice
  rather than an upgrade-day activity.

## Theory and Architecture

### What the bundle contains

Everything that Chapter 01 identified as jointly certified travels
together in a single release:

- Node BIOS and firmware, including drives, controllers, and network
  adapters
- Device drivers matched to that firmware
- The ESXi build
- The vSAN version carried by that ESXi build
- VxRail Manager itself
- vCenter, where the cluster uses VxRail-managed vCenter

The reason for bundling is not packaging convenience. Each of these
components has compatibility relationships with the others, and the
number of possible combinations is large enough that testing them
individually is not feasible. Dell tests specific combinations and ships
those. **The bundle is the unit of testing, so it is the unit of
application.**

This is the same argument that makes the validated state binding rather
than advisory. Applying half a bundle produces a combination nobody
tested, which is indistinguishable in principle from the self-built
cluster VxRail exists to replace.

### The upgrade sequence

A cluster upgrade is a rolling operation. VxRail Manager, for each host
in turn:

1. Places the host into maintenance mode, evacuating workloads via DRS
   and handling the vSAN data decision automatically.
2. Applies firmware and driver updates, which typically requires reboots
   — sometimes more than one, because firmware components have their own
   ordering.
3. Applies the hypervisor update.
4. Brings the host out of maintenance mode and waits for the cluster to
   return to a healthy state before proceeding.

Before the host loop, VxRail Manager and (where applicable) vCenter are
updated. After it, the cluster's validated state is recorded as the new
bundle's.

**The sequencing is the product.** Getting firmware, drivers, and
hypervisor applied in a correct order across a cluster that must stay
available throughout is genuinely hard to do by hand, and doing it by
hand is the thing VxRail customers are paying not to do.

### Duration, honestly

Upgrade duration is the single most under-estimated aspect of VxRail
operations, and under-estimating it produces change windows that
overrun.

The dominant factor is not the software; it is the per-host loop. Each
host must be evacuated, updated with multiple reboots, and returned to
service, and the cluster must be healthy before the next host begins. On
a cluster with substantial workloads, evacuation alone is significant,
and firmware reboots on enterprise hardware are not fast.

The practical guidance is to derive an estimate rather than assume one:
upgrade a single host — or observe the first host of the run — and
multiply, adding the pre-upgrade and appliance-update time. That produces
a defensible window. A cluster of a dozen nodes is comfortably an
overnight operation and frequently longer.

Two things follow. **Fully automated DRS is not optional in practice**,
for the reason [Chapter 04](04-vsphere-and-vsan-integration-and-the-division-of-management.md)
gave — a manual-DRS cluster requires a human present for every host
transition. And **the cluster must have capacity to run with one host
out** for the entire duration, which is the admission control
conversation from Chapter 05 arriving in operational form.

### Connected versus offline upgrade paths

Two ways of getting the bundle to the cluster:

| Path | How it works | Suits |
| --- | --- | --- |
| Connected | VxRail Manager reaches Dell's repository over the internet, sees available bundles, and downloads directly | Clusters with outbound connectivity; lowest friction |
| Offline | The bundle is downloaded separately and uploaded to VxRail Manager | Air-gapped or restricted environments |

The offline path is the same idea as the air-gapped repository workflow
in [Volume XXII, Chapter 07](../../volume-022-dell-openmanage-enterprise/chapters/07-isolated-offline-repositories-and-air-gapped-updates.md),
and the operational lessons transfer: the bundle is large, the transfer
must be planned, and its integrity must be verified before it is applied
rather than after.

For the connected path, note that outbound connectivity is a security
decision as well as a convenience one. A cluster permitted to reach the
internet directly is a different risk posture from one that is not, and
the proxy arrangements that mediate it are worth designing rather than
improvising.

### Pre-checks, and why they are the important part

VxRail runs a health and readiness check before an upgrade. It is
tempting to treat this as a formality; it is the opposite. The pre-check
is where an upgrade that would have failed at 3 a.m. on host seven fails
instead at 8 p.m. before anything has changed.

Pre-checks cover cluster health, vSAN health, capacity sufficient to run
with a host out, node state, certificate validity, connectivity to
required services, and validated-state consistency. A failing pre-check
should be resolved rather than overridden, and the reflex to look for an
override is worth resisting — the check is protecting the change window,
not obstructing it.

**Run the pre-check days before the window, not at the start of it.**
This is the single highest-value operational habit in this chapter.
Pre-check findings frequently require work — a certificate to replace,
capacity to free, a health issue to resolve — and discovering them at the
start of the change window means the window is spent on remediation
rather than on the upgrade.

### Drift, and staying aligned between upgrades

The validated state is a continuous property, not a state achieved at
upgrade time. Between upgrades, drift arrives from:

- A node replaced or added at a different version
  ([Chapter 05](05-cluster-expansion-scale-out-and-capacity-planning.md))
- Someone applying a hypervisor patch through vSphere tooling
- Someone applying firmware through iDRAC or OpenManage
- A configuration change to a VxRail-owned object
  ([Chapter 04](04-vsphere-and-vsan-integration-and-the-division-of-management.md))

Only the first is a legitimate operation with a known remedy. The other
three are the unsupported changes, and detecting them promptly matters
because their effect compounds: an upgrade run against a drifted cluster
is more likely to fail and harder to diagnose when it does.

## Design Considerations

- **Establish an upgrade cadence and hold to it.** Clusters that fall
  several bundle versions behind become harder to upgrade, sometimes
  requiring intermediate steps. The backlog compounds; a regular cadence
  does not.
- **Confirm the upgrade path before planning the window.** Not every
  version upgrades directly to every later version. Check whether an
  intermediate bundle is required, because it doubles the window.
- **Plan the window against a measured estimate.** Derive it from the
  first host rather than from optimism, and include the appliance
  updates that precede the host loop.
- **Do not run an upgrade on a cluster that is nearly full.** It needs
  capacity to run with a host out, and the pre-check will say so, but
  planning around it beforehand avoids a cancelled window.
- **Decide the connectivity posture deliberately.** Connected upgrades
  are much lower friction; whether the cluster should reach the internet
  is a security decision that belongs with the security team, not with
  whoever is scheduling the upgrade.
- **Read the release notes, specifically for what is being removed.**
  Bundle release notes name deprecations, hardware support changes, and
  behavior changes. The one that matters most is hardware support: a
  bundle that drops support for a node generation you own is a
  procurement event, not an upgrade.

## Implementation and Automation

### 1. Establishing current state before planning

```bash
# Per-host: the hypervisor half of the current validated state.
esxcli system version get
```

```powershell
Connect-VIServer -Server vcsa-01.lab.example.com

# Build consistency across the cluster — a precondition for upgrade.
Get-VMHost | Select-Object Name, Version, Build |
  Sort-Object Build |
  Format-Table -AutoSize

# Any host reporting a different build than its peers is drift, and
# needs resolving before an upgrade rather than during one.
$builds = (Get-VMHost | Select-Object -ExpandProperty Build | Sort-Object -Unique)
if ($builds.Count -gt 1) {
  Write-Warning "Mixed builds present: $($builds -join ', ')"
} else {
  Write-Output "Uniform build: $builds"
}
```

VxRail Manager's own view in the vSphere Client is the authority on
whether that build corresponds to a validated state; the commands above
establish whether the cluster is at least internally consistent, which is
a cheaper check to run frequently.

### 2. Confirming capacity for a host-out upgrade

```powershell
# Can the cluster run with its largest host absent?
$hosts = Get-VMHost
$totalMem  = ($hosts | Measure-Object MemoryTotalGB -Sum).Sum
$largest   = ($hosts | Sort-Object MemoryTotalGB -Descending | Select-Object -First 1).MemoryTotalGB
$usedMem   = ($hosts | Measure-Object MemoryUsageGB -Sum).Sum

[pscustomobject]@{
  TotalGB          = [math]::Round($totalMem, 0)
  LargestHostGB    = [math]::Round($largest, 0)
  UsedGB           = [math]::Round($usedMem, 0)
  AvailableHostOut = [math]::Round($totalMem - $largest, 0)
  FitsHostOut      = ($usedMem -lt ($totalMem - $largest))
}
```

`FitsHostOut` reading false means the upgrade cannot proceed as a rolling
operation, and no amount of scheduling will change that.

### 3. Capturing pre-upgrade evidence

Whatever the outcome, the state before the change is what the
troubleshooting afterwards is measured against:

```powershell
$stamp = Get-Date -Format 'yyyy-MM-dd-HHmm'

Get-VMHost | Select-Object Name, Version, Build, ConnectionState, PowerState |
  Export-Csv "./pre-upgrade-hosts-$stamp.csv" -NoTypeInformation

Get-VM | Select-Object Name, PowerState, VMHost, ProvisionedSpaceGB |
  Export-Csv "./pre-upgrade-vms-$stamp.csv" -NoTypeInformation

Get-Cluster | Select-Object Name, HAEnabled, DrsEnabled, DrsAutomationLevel |
  Export-Csv "./pre-upgrade-cluster-$stamp.csv" -NoTypeInformation
```

```bash
# vSAN health, captured as text, before anything changes.
esxcli vsan health cluster list > "vsan-health-pre-$(date +%Y-%m-%d-%H%M).txt"
```

### 4. Verifying an offline bundle before applying it

A bundle that transferred incompletely across an air gap will fail
partway through an upgrade, which is the most expensive time to discover
it:

```bash
# Verify the downloaded bundle against Dell's published checksum before
# transferring it, and again after.
sha256sum VxRail-bundle.zip
```

Compare against the value published alongside the download. Verify on
both sides of the transfer — the point of the second check is the
transfer itself.

### 5. Monitoring the run

An upgrade in progress is observable from the outside as well as through
VxRail Manager:

```powershell
# Which host is currently out, and is the cluster otherwise healthy?
Get-VMHost | Select-Object Name, ConnectionState, Version, Build |
  Format-Table -AutoSize
```

Watching hosts change build one at a time is a useful independent
confirmation that the run is progressing, and the time between the first
and second host completing is the measurement to extrapolate the window
from.

## Validation and Troubleshooting

### Pre-check failures

| Pre-check failure | Usual resolution |
| --- | --- |
| Cluster or vSAN health not green | Resolve the underlying health issue; do not proceed |
| Insufficient capacity to run with a host out | Free capacity or add a node; scheduling cannot fix this |
| Certificate expired or expiring | Replace the certificate before the window |
| Node version inconsistency | Reconcile the drifted node first |
| Connectivity to required services unavailable | Resolve the network or proxy path |
| DRS not fully automated | Set it, or plan an attended upgrade |

Every one of these is easier to fix with days in hand than with a change
window running, which is the argument for the early pre-check.

### An upgrade that stalls on a host

The run pauses when a host does not return to a healthy state. The
diagnosis order that works:

1. **Is the host up?** A firmware update that did not complete can leave
   a host that has not booted. iDRAC is the tool here — virtual console
   and the Lifecycle Log, exactly as
   [Volume XXIII, Chapter 06](../../volume-023-dell-idrac-9-10-administration/chapters/06-hardware-health-power-thermal-logs-and-support.md)
   describes. This is the point where VxRail's hardware layer stops being
   abstracted away.
2. **Is it up but not rejoining?** Check management network reachability
   and vCenter connectivity for that host.
3. **Is it rejoined but vSAN is not healthy?** The cluster may be
   resyncing; confirm it is progressing rather than stuck.

**Do not attempt to resume the upgrade by reconfiguring the host by
hand.** A stalled upgrade is a supported condition with documented
recovery, and a hand-repaired host is a validated-state problem on top of
an upgrade problem. This is a support case, and Dell expects them.

### The upgrade completes but a host reports a different build

Rare, and it means a host did not receive the full bundle. Do not leave
it: a cluster with mixed builds is the drift condition this chapter's
whole argument is against. Engage support.

### Detecting drift between upgrades

Run the build-consistency check from *Implementation and Automation* on a
schedule and compare VxRail Manager's health view alongside it. The two
together catch the version half of drift. The configuration half is
caught by diffing against the baseline captured in
[Chapter 03](03-vxrail-manager-deployment-and-first-run-configuration.md).

## Security and Best Practices

- **Do not defer bundles because they are inconvenient.** Bundles carry
  security fixes for firmware and hypervisor alike, and a cluster several
  versions behind is carrying known vulnerabilities in components that
  are not individually patchable by design.
- **Resolve the patching-policy tension explicitly.** Where security
  policy requires patching on a cadence the bundle release schedule does
  not match, that is a real conflict identified in Chapter 01. The
  resolution is a documented risk acceptance or a different platform, not
  an out-of-band patch.
- **Verify bundle integrity before applying, always.** On the connected
  path this is handled; on the offline path it is yours, and it is the
  point at which a supply-chain assumption becomes a check.
- **Restrict who can initiate an upgrade.** It is a cluster-wide
  operation with a long window and real risk, and it belongs behind the
  same controls as any major change.
- **Keep pre-upgrade evidence.** The exports above are what distinguishes
  "the upgrade broke it" from "it was already like that", and that
  distinction matters in a support case.

## References and Knowledge Checks

**References**

- [Dell VxRail product documentation](https://www.dell.com/support/home/en-us/product-support/product/vxrail-appliance-series/docs)
  — release notes and upgrade guides, which are the authority on
  supported upgrade paths and hardware support changes.
- [Volume XXII, Chapter 07](../../volume-022-dell-openmanage-enterprise/chapters/07-isolated-offline-repositories-and-air-gapped-updates.md)
  — air-gapped update workflow patterns that transfer to the offline
  bundle path.
- [Volume XXIII, Chapter 06](../../volume-023-dell-idrac-9-10-administration/chapters/06-hardware-health-power-thermal-logs-and-support.md)
  — iDRAC diagnostics, needed when a host does not return during an
  upgrade.
- [Volume XII, Chapter 06](../../volume-012-resilience-lifecycle-management/chapters/06-maintenance-patching-and-upgrade-engineering.md)
  — maintenance and upgrade engineering practice the upgrade window sits
  inside.

**Knowledge checks**

1. Why is the bundle applied as a unit rather than component by
   component? Give the testing argument, not the packaging one.
2. Describe the per-host upgrade loop and identify which step dominates
   duration.
3. Why should the pre-check run days before the change window rather than
   at its start?
4. Name the four sources of validated-state drift and identify which one
   is a legitimate operation.
5. A host does not come back during an upgrade. Give the diagnosis order,
   and say what you must not do.

## Hands-On Lab

This chapter carries a topic-level walkthrough lab for **each theme of VxRail lifecycle management**
— the Continuously Validated State, checking for updates, running an LCM upgrade, and pre-upgrade
health. LCM is VxRail's signature capability. Each pairs the plugin with API verification. Each ends
**`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 6.1–6.4** — a deployed VxRail cluster, vSphere Client and VxRail
plugin access, connectivity (or an offline bundle) for update content, and the VxRail API. **Cost:**
none.

### Lab 6.1 — The Continuously Validated State (Topic: LCM concept)

**Objective:** Understand what a VxRail "version" actually is.

```bash
curl -sk -u 'administrator@vsphere.local:<pass>' https://<vxm>/rest/vxm/v1/system | \
  python3 -c "import json,sys; print('VxRail bundle version:', json.load(sys.stdin).get('version'))"
# The version names ONE tested combination of BIOS/firmware/drivers/ESXi/vSAN/vCenter/VxRail Manager.
```

**Expected result:** a single VxRail version string naming one Dell-tested combination of the entire
stack — VxRail's **Continuously Validated State** means every component version is validated together
as one bundle, so "what version am I on" answers for the whole stack, not per component.

**Negative test:** update one component (e.g. a NIC driver) out of band to chase a fix; the cluster
leaves the validated state and Dell support/LCM no longer guarantee compatibility — components move
together, as a bundle, through LCM.

**Rollback:** none (read-only).

### Lab 6.2 — Check for updates (Topic: Update discovery)

**Objective:** See which validated bundle you can move to.

```text
# vSphere Client: Cluster > Configure > VxRail > Updates (or Internet/Local update source).
#   VxRail lists the available target bundle(s) — a single composite update for the whole stack.
```

Verify via the API:

```bash
curl -sk -u 'administrator@vsphere.local:<pass>' https://<vxm>/rest/vxm/v1/lcm/upgrade 2>/dev/null | head
```

**Expected result:** the available target VxRail bundle(s) are listed — checking for updates surfaces
the next validated state as one composite bundle (connected via Dell, or uploaded offline), so you
plan a single stack upgrade rather than tracking dozens of component versions.

**Negative test:** track each component's latest version independently and try to assemble your own
"current" set; you recreate the compatibility problem VxRail solved — the composite bundle is the
supported update unit.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 6.3 — Pre-upgrade health check (Topic: Upgrade readiness)

**Objective:** Confirm the cluster is ready to upgrade.

```text
# Run the VxRail pre-upgrade health check (LCM precheck) from the Updates panel.
#   It validates: vSAN health, host connectivity, capacity/slack for maintenance-mode rolling,
#   password/cert validity, and network. Resolve any failures BEFORE starting.
```

**Expected result:** the precheck passes (or lists specific blockers) — VxRail runs a health
precheck before an LCM upgrade because the upgrade rolls hosts through maintenance mode one at a
time, which requires healthy vSAN and enough slack capacity to evacuate each host.

**Negative test:** start an LCM upgrade with a failing vSAN health check or insufficient slack; a
host cannot safely enter maintenance mode and the upgrade stalls or risks data — the precheck is the
gate that prevents an unsafe upgrade.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 6.4 — Run an LCM upgrade (Topic: Lifecycle upgrade)

**Objective:** Apply the validated bundle non-disruptively.

```text
# From the Updates panel, start the LCM upgrade to the target bundle. VxRail:
#   - puts each host into maintenance mode in turn (vSAN data evacuated/re-protected),
#     updates firmware + ESXi + vSAN, exits maintenance, moves to the next host
#   - updates vCenter and VxRail Manager as part of the bundle
# Monitor to completion; confirm the new version and green health afterward.
```

**Expected result:** the whole stack upgrades one host at a time with workloads migrating via DRS,
ending on the new validated version with green health — LCM is VxRail's core value: a single,
non-disruptive, Dell-tested full-stack upgrade instead of manually sequencing firmware, ESXi, vSAN,
and vCenter.

**Negative test:** manually upgrade ESXi/vCenter/firmware in your own order on a VxRail; you risk an
unsupported/untested combination and break LCM — the orchestrated bundle upgrade is what keeps the
stack validated and supported.

**Rollback:** none (leave the cluster on the upgraded version).

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The lifecycle bundle is VxRail's product. It exists because the number of
firmware, driver, hypervisor, and appliance combinations is too large to
test individually, so Dell tests specific combinations and ships them
whole — which is why applying part of one defeats the purpose. Upgrades
are rolling per-host operations whose duration is dominated by the
evacuate-reboot-rejoin loop and is routinely under-estimated; derive the
window from a measurement. The pre-check is not a formality but the
mechanism that moves failures out of the change window, which is why it
belongs days ahead of it. Between upgrades, validated-state alignment is
a continuous property, and the three illegitimate sources of drift are
all unsupported changes made with good intentions.

- [ ] Can explain the bundle's contents and the testing argument for
      applying it whole.
- [ ] Can describe the per-host loop and derive a window estimate from a
      measurement.
- [ ] Runs pre-checks days ahead and resolves rather than overrides
      findings.
- [ ] Can verify capacity for a host-out rolling operation before
      scheduling.
- [ ] Captures pre-upgrade evidence as a routine step.
- [ ] Knows the diagnosis order for a stalled host, and that hand repair
      is not part of it.
