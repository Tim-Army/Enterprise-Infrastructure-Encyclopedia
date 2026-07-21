# Chapter 09: Day-2 Operations, Troubleshooting, Support, and Capstone

## Learning Objectives

- Run a day-2 operational routine for a VxRail estate on daily, weekly,
  and quarterly cadences.
- Apply a structured troubleshooting method that localizes a fault to the
  correct layer before investigating it.
- Collect the right diagnostic evidence and engage Dell support
  effectively.
- Handle drive and node failures through supported procedures.
- Exercise the whole platform through a capstone that spans every chapter
  in this volume.

## Theory and Architecture

### The day-2 routine

Most VxRail operational failures are not sudden. They are conditions that
were visible for weeks and that nobody was looking at: capacity crossing
a threshold, a failed witness, a node drifting out of validated state, a
backup that has not been restore-tested. A routine catches these; ad-hoc
attention does not.

**Daily** — automated, reviewed by exception:

- Cluster and vSAN health status
- VxRail Manager health and validated-state alignment
- Capacity utilization against the trigger threshold from
  [Chapter 05](05-cluster-expansion-scale-out-and-capacity-planning.md)
- Backup job outcomes
- Any open hardware alerts or call-home cases

**Weekly** — reviewed by a person:

- Drift detection output from
  [Chapter 08](08-vxrail-api-automation-and-ecosystem-integrations.md)
- Capacity trend, appended to the series and re-projected
- Storage policy compliance across the estate
- Resync activity that has not resolved

**Quarterly** — deliberate exercises:

- Restore validation, into isolation
  ([Chapter 07](07-availability-stretched-clusters-and-data-protection.md))
- Availability testing against the claims in the design document
- Bundle currency review against the upgrade cadence
- Support entitlement and warranty verification
- Baseline refresh and documentation reconciliation

The quarterly list is the one that gets skipped, and it is the one that
protects against the failures that actually hurt.

### Structured troubleshooting: localize before investigating

VxRail's layering is its main troubleshooting asset, provided faults are
localized before they are investigated. The sequence that works, in
order, because each step is cheaper than the next:

1. **Is it the workload?** A single VM behaving badly on a healthy
   cluster is a VM problem. Confirm the cluster is healthy before
   treating a workload symptom as a platform symptom — a substantial
   proportion of "VxRail is slow" reports resolve here.
2. **Is it vSphere?** HA, DRS, resource contention, a misconfigured
   policy. Ordinary vSphere troubleshooting from
   [Volume V, Chapter 09](../../volume-05-vmware-virtualization/chapters/09-vsphere-lifecycle-automation-observability-and-troubleshooting.md)
   applies unchanged.
3. **Is it vSAN?** Object compliance, resync, capacity, disk group
   health. Check vSAN health explicitly; it covers a lot and it is fast.
4. **Is it the network?** The prerequisites from
   [Chapter 02](02-physical-installation-network-prerequisites-and-pre-deployment-planning.md)
   do not stop mattering after deployment. An MTU change made on a
   switch months later produces a storage performance problem nobody
   connects to the switch.
5. **Is it VxRail-specific?** Validated-state drift, VxRail Manager
   health, a failed lifecycle operation.
6. **Is it the hardware?** iDRAC and the Lifecycle Log, exactly as
   [Volume XXIII, Chapter 06](../../volume-23-dell-idrac-9-10-administration/chapters/06-hardware-health-power-thermal-logs-and-support.md)
   describes. This is where the abstraction ends and a VxRail node is
   simply a PowerEdge server.

**The discipline is to not skip to step 6.** Hardware is the most
satisfying thing to suspect and among the least frequent causes. Working
the layers in order costs minutes and prevents replacing a healthy
component.

### What the layers look like from below

Worth noting the inverse: a hardware fault propagates upward and presents
at every layer above it. A failing drive appears as vSAN degraded
objects, as VM latency, and as an application complaint — in that causal
order but often in the reverse order of discovery. Recognizing that a
symptom set spans multiple layers coherently is itself the signal that
the cause is at the bottom.

### Drive and node failure

Drive failure is the most common hardware event on any HCI cluster,
because drive count is high.

vSAN handles the availability side automatically: objects rebuild using
free capacity elsewhere, provided the capacity exists — which is the
functional-slack-space point from Chapter 05 arriving in its most
concrete form. A cluster too full to rebuild converts a routine drive
failure into a data availability incident.

The replacement side is a Dell procedure. Drives are qualified parts and
replacement follows VxRail's documented process so the new drive is
brought into the vSAN configuration correctly. Where call-home is
configured, Dell frequently knows before you do and a case and a part are
already moving — this is the support model working as designed.

Node failure is a larger event with the same shape: availability handled
by the cluster if policy and capacity permit, replacement handled as a
support procedure rather than a self-service one.

### Engaging support effectively

The single support boundary from Chapter 01 is real, and getting value
from it depends on what you bring:

- **The service tag** of the affected node. This is the identifier
  everything is keyed on.
- **The VxRail version** and cluster composition.
- **A log bundle**, collected through VxRail Manager, which gathers
  cluster-wide diagnostics rather than a single host's.
- **A timeline**: when it started, what changed beforehand, what has been
  tried. The "what changed beforehand" is the one most often omitted and
  most often decisive.
- **Whether the cluster is in a validated state**, stated honestly. If an
  unsupported change was made, say so at the start. Support will find it,
  and finding it late wastes the intervening time.

Dell publishes procedure-generation resources for VxRail that produce
step-by-step, version-specific instructions for hardware and maintenance
procedures. Where a procedure exists, follow it rather than improvising —
the improvised version is what produces the second problem.

## Design Considerations

- **Automate the daily checks and review by exception.** A daily routine
  that requires a human to look at green dashboards will be abandoned
  within a month. One that alerts on deviation will not.
- **Schedule the quarterly exercises as change records.** Unscheduled
  good intentions do not survive a busy quarter. A restore test with a
  date and an owner does.
- **Keep the baseline current.** Every expansion, upgrade, and
  configuration change should update the baseline from
  [Chapter 03](03-vxrail-manager-deployment-and-first-run-configuration.md),
  or drift detection compares against fiction.
- **Write down the troubleshooting sequence and put it where the on-call
  engineer will see it.** Under pressure, people skip to the layer they
  know best. A written sequence is what prevents that.
- **Record support case outcomes into your own documentation.** The
  resolution of an incident is knowledge that otherwise lives only in
  Dell's case system.
- **Track warranty and entitlement expiry as a calendar item.** The
  support model is the platform's main operational benefit and it stops
  at the entitlement date.

## Implementation and Automation

### 1. A daily health collection

```bash
#!/usr/bin/env bash
# vxrail-daily-check.sh — collect and report. Exits non-zero on finding.
set -euo pipefail

stamp="$(date +%Y-%m-%d)"
outdir="./health/${stamp}"
mkdir -p "$outdir"
findings=0

# vSAN health, per host.
for host in esxi-01 esxi-02 esxi-03; do
  ssh "root@${host}.lab.example.com" \
    'esxcli vsan health cluster list' > "${outdir}/vsan-health-${host}.txt" || {
      echo "FINDING: could not collect vSAN health from ${host}"
      findings=1
    }
done

# Any non-green result is a finding.
if grep -qiE '\b(red|yellow)\b' "${outdir}"/vsan-health-*.txt 2>/dev/null; then
  echo "FINDING: vSAN health is not green — see ${outdir}"
  findings=1
fi

exit "$findings"
```

The exit code is the point: this is designed to be scheduled and to
alert, not to be read.

### 2. Capacity against the threshold

```powershell
# Fails loudly when utilization crosses the procurement trigger.
$threshold = 70   # per Chapter 05 — set well below the danger point

$ds = Get-Datastore | Where-Object { $_.Type -eq 'vsan' }
$usedPc = [math]::Round((($ds.CapacityGB - $ds.FreeSpaceGB) / $ds.CapacityGB) * 100, 1)

if ($usedPc -ge $threshold) {
  Write-Error "Capacity at ${usedPc}% — procurement trigger ($threshold%) crossed."
} else {
  Write-Output "Capacity at ${usedPc}% — below trigger."
}
```

### 3. Weekly compliance and resync review

```powershell
# Any VM whose objects do not satisfy its policy.
Get-VM | ForEach-Object {
  $cfg = Get-SpbmEntityConfiguration $_
  if ($cfg.ComplianceStatus -ne 'compliant') {
    [pscustomobject]@{
      VM               = $_.Name
      Policy           = $cfg.StoragePolicy.Name
      ComplianceStatus = $cfg.ComplianceStatus
    }
  }
} | Format-Table -AutoSize

# Resync that is not clearing is a finding, not a status.
Get-VsanResyncingComponent -Cluster 'vxrail-lab-01' |
  Measure-Object -Property BytesLeftToResync -Sum |
  Select-Object @{N='GBRemaining'; E={[math]::Round($_.Sum / 1GB, 1)}}
```

### 4. Collecting evidence for a support case

```bash
# Per-host logs, alongside the cluster-wide bundle collected through
# VxRail Manager. Both are useful; the VxRail bundle is the one to lead
# with, because it spans the cluster.
ssh root@esxi-01.lab.example.com 'vm-support -w /vmfs/volumes/scratch'

# Hardware-layer evidence from iDRAC, per Volume XXIII: the Lifecycle
# Log is where a hardware fault is recorded with a timestamp.
racadm -r idrac-01.lab.example.com -u root -p "$IDRAC_PASS" \
  lclog view -c 20
```

Collect evidence *before* attempting remediation where the situation
permits. Remediation destroys the state that explains what happened, and
"we restarted it and it came back" closes an incident without resolving
it.

### 5. A single day-2 driver

```bash
#!/usr/bin/env bash
# vxrail-day2.sh — run the appropriate cadence. Schedule daily/weekly.
set -euo pipefail

case "${1:-daily}" in
  daily)
    ./vxrail-daily-check.sh
    pwsh -File ./capacity-threshold.ps1
    ;;
  weekly)
    ./vxrail-daily-check.sh
    python3 ./vxrail-drift-check.py          # from Chapter 08
    pwsh -File ./compliance-review.ps1
    pwsh -File ./capacity-append.ps1         # from Chapter 05
    ;;
  *)
    echo "usage: $0 {daily|weekly}" >&2
    exit 2
    ;;
esac
```

## Validation and Troubleshooting

### A worked localization

"The database is slow" arrives at 09:00. Working the layers:

| Step | Check | Outcome that moves you on |
| --- | --- | --- |
| Workload | Is only this VM affected, or others too? | Others too — not a workload problem |
| vSphere | CPU ready, memory ballooning, host contention? | Clean — not resource contention |
| vSAN | Health, resync activity, object compliance? | Resync in progress — investigate why |
| Why resync? | A drive or host failed recently? | A capacity drive failed at 03:00 |
| Hardware | iDRAC Lifecycle Log for that node | Drive predictive failure logged 03:00 |

Five steps, each cheap, arriving at a cause that explains every symptom
including the timing. Contrast the common alternative: restarting the
database VM at step one, achieving nothing, and losing an hour.

### Localization failures to recognize

- **Symptoms at one layer only** — the cause is usually at that layer.
- **Symptoms at every layer, coherent in timing** — the cause is
  underneath, and probably hardware.
- **Symptoms that started after a change** — start with the change,
  whatever the symptoms suggest. "Nothing changed" is very often wrong,
  and the drift baseline is how you check rather than ask.
- **Intermittent symptoms correlating with load** — network or capacity
  before hardware.

### When to stop and open a case

Open a case rather than continuing when: the fault is hardware, the
cluster is out of validated state, a lifecycle operation has failed
partway, or the next diagnostic step would change something you cannot
easily reverse. There is no credit for solving alone what the support
entitlement covers, and improvised repair is how a recoverable situation
becomes an unrecoverable one.

## Security and Best Practices

- **Restrict who can collect and share log bundles.** They contain
  configuration and identifiers useful to an attacker, and they routinely
  get emailed.
- **Review access to VxRail Manager and vCenter quarterly.** Access
  granted for a project outlives the project by default.
- **Include VxRail in the patch and vulnerability process even though it
  patches differently.** Bundle currency is the mechanism; excluding the
  platform because it does not fit the normal tooling produces a cluster
  nobody is tracking.
- **Keep support contacts and entitlement details somewhere reachable
  during an outage** — not solely in a system that may be affected by it.
- **Test the call-home path.** An integration that is configured and does
  not work is worse than one known to be absent, because it produces
  false confidence.

## References and Knowledge Checks

**References**

- [Dell VxRail product documentation](https://www.dell.com/support/home/en-us/product-support/product/vxrail-appliance-series/docs)
  — administration guides, procedure generators, and support resources.
- [Volume V, Chapter 09](../../volume-05-vmware-virtualization/chapters/09-vsphere-lifecycle-automation-observability-and-troubleshooting.md)
  — vSphere troubleshooting, which is layers 2 and 3 of the sequence.
- [Volume XXIII, Chapter 06](../../volume-23-dell-idrac-9-10-administration/chapters/06-hardware-health-power-thermal-logs-and-support.md)
  — iDRAC diagnostics and the Lifecycle Log, which is layer 6.
- [Volume XI](../../volume-11-observability-enterprise-operations/README.md)
  — observability practice the day-2 routine implements for one platform.

**Knowledge checks**

1. Give the six troubleshooting layers in order and explain why the order
   is worth following rather than jumping to the likeliest.
2. Symptoms appear coherently at every layer with consistent timing.
   Where is the cause, and why does that pattern indicate it?
3. What five things should accompany a support case, and which is most
   often omitted?
4. Why does a drive failure on a nearly full cluster behave differently
   from one on a cluster with headroom?
5. Name the four conditions under which you should stop troubleshooting
   and open a case.

## Hands-On Lab

**Objective:** Build and run the complete day-2 operational routine, then
complete a capstone exercising every chapter in this volume.

**Prerequisites:** Everything from the preceding chapters — a nested
vSphere and vSAN cluster, PowerCLI, the drift detector from
[Chapter 08](08-vxrail-api-automation-and-ecosystem-integrations.md), the
capacity history from
[Chapter 05](05-cluster-expansion-scale-out-and-capacity-planning.md), and
the baseline from
[Chapter 03](03-vxrail-manager-deployment-and-first-run-configuration.md).

**Part A — the day-2 routine**

1. Assemble the daily and weekly scripts into `vxrail-day2.sh` and run
   both cadences. Confirm each exits zero on a healthy cluster.
2. Introduce a condition each check should catch — fill capacity past the
   threshold, change a monitored value, break a policy's satisfiability —
   and confirm the corresponding check exits non-zero and names it.
3. Schedule the daily run and confirm it produces output and alerts
   without a human present.

**Part B — capstone**

This exercises the volume end to end. Work it as a single continuous
scenario.

4. **Design** (Chapter 01). Given a workload of 200 VMs averaging 4 vCPU,
   16 GB RAM, and 200 GB used storage, produce a sizing decision record:
   binding constraint, node count under mirroring and under erasure
   coding, recommended vCenter topology, and the patching-policy
   determination.
5. **Prerequisites** (Chapter 02). Produce the complete deployment plan
   for that design, with addressing, VLANs, and services. Verify DNS both
   ways and jumbo frames on your lab fabric.
6. **Deployment verification** (Chapter 03). Run the pre-flight checks
   against your plan, then capture a baseline of the resulting cluster.
7. **Policy** (Chapter 04). Apply a storage policy appropriate to the
   design's resilience requirement and measure the capacity consequence
   against the step 4 projection. Note the error and its direction.
8. **Capacity** (Chapter 05). Build a capacity series, project the
   trigger date, and state what you would procure and when.
9. **Lifecycle** (Chapter 06). Run a rolling per-host maintenance
   operation, time it, and produce a defensible change-window estimate
   for a twelve-node cluster.
10. **Availability** (Chapter 07). Test a host failure abruptly, measure
    both the restart and the redundancy-restored durations, and validate
    a restore into isolation.
11. **Automation** (Chapter 08). Run the drift detector against the
    baseline from step 6 and confirm it reports the changes steps 7
    through 10 introduced.
12. **Operations** (Chapter 09). Produce a single operational handover
    document containing: the design decision record, the deployment plan,
    the current baseline, the capacity projection, the measured upgrade
    window, the availability test results, and the day-2 schedule.

**Negative test**

13. Give the handover document from step 12 to someone who has not
    followed the exercise and ask them to answer: what happens when a
    host fails, when must capacity be procured, and how long is the next
    upgrade window. If the document does not answer all three, it is
    incomplete — this is the actual test of the whole volume, because a
    platform whose operational knowledge lives only in one person's head
    is not operationally sound regardless of how well it is built.

**Expected results**

- A day-2 routine that runs unattended and alerts correctly on each
  condition it monitors.
- A handover document that answers the three questions in step 13 without
  its author present.
- Measured rather than assumed figures for capacity ratio, upgrade
  duration, and recovery time.

**Cleanup**

14. Return the lab cluster to its baseline state, allow all resync to
    complete, and retain the handover document — it is the template for
    the real one.

## Summary and Completion Checklist

Day-2 VxRail operations are a cadence rather than a set of skills: daily
automated checks reviewed by exception, weekly human review of drift and
trends, and quarterly exercises that validate the claims the design makes
— restore tests, failure tests, and entitlement verification. The
quarterly list is the one that gets skipped and the one that matters
most. Troubleshooting works from workload down to hardware, in that
order, because each layer is cheaper to check than the next and because
hardware is the most tempting and least frequent cause. When the fault is
hardware, the cluster is out of validated state, or a lifecycle operation
has failed partway, the correct action is a support case with a service
tag, a log bundle, a timeline, and an honest statement of the cluster's
state — the single support boundary is the platform's main operational
benefit and it works best when it is used.

- [ ] Runs an automated daily routine that alerts by exception.
- [ ] Holds quarterly restore and availability exercises as scheduled
      change records.
- [ ] Applies the six-layer troubleshooting sequence rather than jumping
      to hardware.
- [ ] Can recognize a hardware cause from coherent multi-layer symptoms.
- [ ] Collects evidence before remediating, where circumstances permit.
- [ ] Knows the four conditions that mean stop and open a case.
- [ ] Has produced an operational handover document that answers the
      three capstone questions without its author.
