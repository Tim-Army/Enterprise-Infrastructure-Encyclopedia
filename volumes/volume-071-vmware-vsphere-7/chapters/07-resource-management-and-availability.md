# Chapter 07: Resource Management and Availability

## Learning Objectives

- Explain vMotion, DRS, and vSphere HA.
- Configure a cluster for load balancing and failover.
- Use resource pools, reservations, limits, and shares.
- Understand EVC for CPU compatibility.
- Complete a walkthrough for each resource/availability topic.

## Theory and Architecture

The features that make vSphere an enterprise platform live at the **cluster** level. **vMotion**
migrates a running VM between hosts with **no downtime** (memory and state copied live), and
**Storage vMotion** (Chapter 6) does the same for storage. **DRS (Distributed Resource
Scheduler)** — rewritten in vSphere 7 to a **per-VM, workload-centric scoring** model — uses vMotion
to **balance load** across hosts automatically (and can power hosts down with DPM). **vSphere HA
(High Availability)** restarts VMs on **surviving hosts** when a host fails, giving automatic
recovery. Resource control uses **reservations** (guaranteed minimums), **limits** (caps), and
**shares** (relative priority under contention), organized with **resource pools**. **EVC (Enhanced
vMotion Compatibility)** masks CPU features to a common baseline so vMotion works across mixed CPU
generations. Together these deliver mobility, balance, and resilience.

## Design Considerations

Enable **DRS** (fully automated in production) and **HA** on every production cluster. Set **EVC** to
the lowest common CPU so hosts can be added and VMs migrate freely. Use **reservations/shares**
sparingly and deliberately — over-reserving wastes capacity. Size the cluster to tolerate host
failures (admission control). Keep vMotion networking fast (Chapter 5).

## Implementation and Automation

The labs enable DRS/HA, perform a vMotion, set EVC, and configure resource controls — with PowerCLI.

## Validation and Troubleshooting

Confirm the cluster model:

```text
vMotion: live VM migration (no downtime). DRS (per-VM scoring in 7): auto load-balance via vMotion (+DPM).
HA: restart VMs on surviving hosts after a host failure (admission control reserves capacity).
Resource pools + reservations/limits/shares. EVC: common CPU baseline for cross-generation vMotion.
```

Common pitfalls: **no HA/DRS** on production clusters; and mixed CPU generations with **no EVC**
(vMotion fails).

## Security and Best Practices

Run **DRS + HA** on production clusters with **admission control** sized for failures, set **EVC**
early, and use resource controls **deliberately**. Keep vMotion networking dedicated and fast.
Test failover. Mobility and resilience are what justify the platform.

## Hands-On Lab

Resource/availability walkthroughs. **Shared prerequisites** — a vCenter 7 cluster with 2+ hosts,
shared storage, PowerCLI, in a lab. **Cost:** none.

### Lab 7.1 — Enable DRS and HA

**Objective:** Turn on load balancing and failover.

```powershell
Set-Cluster Cluster1 -DRSEnabled $true -DRSAutomationLevel FullyAutomated `
  -HAEnabled $true -HAAdmissionControlEnabled $true -Confirm:$false
Get-Cluster Cluster1 | Select Name, DrsEnabled, DrsAutomationLevel, HAEnabled
```

**Expected result:** the cluster with **fully automated DRS** and **HA + admission control** — load
balancing and failover.

**Negative test:** run production with **HA disabled**; a host failure then takes its VMs down —
enable HA.

**Rollback:** leave enabled (production posture) or revert in a lab.

### Lab 7.2 — Live-migrate a VM (vMotion)

**Objective:** Move a running VM with no downtime.

```powershell
$vm = Get-VM web02
Move-VM -VM $vm -Destination (Get-VMHost | Where {$_.Name -ne $vm.VMHost.Name})[0]
Get-VM web02 | Select Name, VMHost
```

**Expected result:** the running VM **migrated to another host** with no downtime — vMotion.

**Negative test:** power off a VM to move it between hosts; **vMotion** migrates it live — use it.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.3 — Set EVC

**Objective:** Enable cross-generation CPU compatibility.

```powershell
Set-Cluster Cluster1 -EVCMode "intel-skylake" -Confirm:$false
Get-Cluster Cluster1 | Select Name, EVCMode
```

**Expected result:** an **EVC baseline** set so VMs vMotion across mixed CPU generations — fleet
flexibility.

**Negative test:** add a newer-CPU host to a cluster with **no EVC**; vMotion to/from it may fail —
set EVC to a common baseline.

**Rollback:** revert EVC in a lab if needed.

### Lab 7.4 — Resource pools and shares

**Objective:** Control resources under contention.

```powershell
$rp = New-ResourcePool -Name "prod" -Location (Get-Cluster Cluster1) -CpuSharesLevel High -MemSharesLevel High
Move-VM -VM web02 -Destination $rp
Get-ResourcePool prod | Select Name, CpuSharesLevel, MemSharesLevel
```

**Expected result:** a **resource pool** with high shares holding the VM — prioritized under
contention.

**Negative test:** set large **reservations** everywhere "to be safe"; that fragments capacity —
use **shares** for priority, reservations sparingly.

**Rollback:** `Get-VM web02 | Move-VM -Destination (Get-Cluster Cluster1); Remove-ResourcePool prod -Confirm:$false`.

### Lab 7.5 — Verify HA failover readiness

**Objective:** Confirm the cluster can absorb a failure.

```powershell
Get-Cluster Cluster1 | Select Name, HAEnabled,
  @{N='FailoverLevel';E={$_.ExtensionData.Configuration.DasConfig.AdmissionControlPolicy.FailoverLevel}}
```

**Expected result:** HA with an **admission-control failover level** reserving capacity for N host
failures — ready to recover.

**Negative test:** run at 100% utilization with HA on but **no reserved capacity**; failover has
nowhere to restart VMs — size admission control.

**Rollback:** none (read-only).

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Cluster features deliver mobility and resilience: vMotion (live migration), DRS (per-VM automated
balancing), HA (automatic VM restart on failure), resource pools/shares, and EVC for CPU
compatibility. Run DRS+HA with admission control, set EVC early, and use resource controls
deliberately.

- [ ] I can enable DRS and HA with admission control.
- [ ] I can perform a live vMotion.
- [ ] I can set an EVC baseline.
- [ ] I can configure resource pools/shares and verify HA readiness.
- [ ] I completed Labs 7.1–7.5 including each negative test.
