# Chapter 07: Resource Management and Availability

## Learning Objectives

- Configure DRS and vSphere HA in vSphere 8.
- Explain vMotion unified data transport for large VMs.
- Use resource pools, reservations, limits, and shares.
- Apply EVC and admission control.
- Complete a walkthrough for each resource/availability topic.

## Theory and Architecture

vSphere 8 keeps the cluster availability model — **DRS** (per-VM workload-centric balancing via
vMotion), **vSphere HA** (VM restart on host failure), **resource pools/reservations/limits/
shares**, **EVC**, and **admission control** — and refines the migration engine. **vMotion unified
data transport** streamlines the copy of very large, memory-heavy VMs (and improves live migration
for some GPU/DPU-backed configurations), reducing migration time and stun. DRS and HA continue to
be enhanced (better initial placement, faster restarts). The design guidance is unchanged: run
**DRS + HA** on production clusters with **admission control** sized for failures, set **EVC** to a
common CPU baseline so hosts of different generations coexist, keep **vMotion networking** fast and
dedicated, and use resource controls deliberately. vSphere 8 makes the same features faster and more
capable, especially for large and accelerated workloads.

## Design Considerations

Enable **DRS (fully automated) + HA** on production clusters and size **admission control** for the
failures you must tolerate. Set **EVC** early. Keep **vMotion networking** fast — unified data
transport benefits large VMs most on good networking. Use **shares** for priority, reservations
sparingly. Test failover.

## Implementation and Automation

The labs enable DRS/HA, perform a vMotion, set EVC, and configure resource controls with PowerCLI.

## Validation and Troubleshooting

Confirm the cluster model:

```text
DRS (per-VM scoring) + HA (restart on failure, admission control) + resource pools/shares + EVC (as in 7).
vMotion unified data transport: faster migration of large/memory-heavy VMs (+ improved live ops for some accel VMs).
Keep vMotion networking fast/dedicated. Size admission control for host failures.
```

Common pitfalls: **no HA/DRS** on production; and mixed CPU generations with **no EVC**.

## Security and Best Practices

Run **DRS + HA** with **admission control**, set **EVC** early, dedicate fast **vMotion**
networking, and use resource controls **deliberately**. Test failover regularly. Mobility and
resilience justify the platform; vSphere 8 makes them faster.

## Hands-On Lab

Resource/availability walkthroughs. **Shared prerequisites** — a vCenter 8 cluster with 2+ hosts,
shared storage, PowerCLI, in a lab. **Cost:** none.

### Lab 7.1 — Enable DRS and HA

**Objective:** Turn on load balancing and failover.

```powershell
Set-Cluster Cluster1 -DRSEnabled $true -DRSAutomationLevel FullyAutomated `
  -HAEnabled $true -HAAdmissionControlEnabled $true -Confirm:$false
Get-Cluster Cluster1 | Select Name, DrsEnabled, DrsAutomationLevel, HAEnabled
```

**Expected result:** the cluster with **fully automated DRS** and **HA + admission control** —
balancing and failover.

**Negative test:** run production with **HA disabled**; a host failure drops its VMs — enable HA.

**Rollback:** leave enabled (production) or revert in a lab.

### Lab 7.2 — Live-migrate a large VM (vMotion)

**Objective:** Migrate with unified data transport.

```powershell
$vm = Get-VM app01
Move-VM -VM $vm -Destination (Get-VMHost | Where {$_.Name -ne $vm.VMHost.Name})[0]
Get-VM app01 | Select Name, VMHost
```

**Expected result:** the running VM **migrated live** — vSphere 8's unified data transport speeds
this for large VMs.

**Negative test:** power off a large VM to move it; **vMotion** migrates it live — use it.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.3 — Set EVC

**Objective:** Enable cross-generation CPU compatibility.

```powershell
Set-Cluster Cluster1 -EVCMode "intel-icelake" -Confirm:$false
Get-Cluster Cluster1 | Select Name, EVCMode
```

**Expected result:** an **EVC baseline** so VMs vMotion across mixed CPU generations — fleet
flexibility.

**Negative test:** add a newer-CPU host with **no EVC**; vMotion may fail — set a common baseline.

**Rollback:** revert EVC in a lab if needed.

### Lab 7.4 — Resource pools and shares

**Objective:** Prioritize under contention.

```powershell
$rp = New-ResourcePool -Name "prod8" -Location (Get-Cluster Cluster1) -CpuSharesLevel High -MemSharesLevel High
Move-VM -VM app01 -Destination $rp
Get-ResourcePool prod8 | Select Name, CpuSharesLevel, MemSharesLevel
```

**Expected result:** a **resource pool** with high shares holding the VM — prioritized under
contention.

**Negative test:** over-reserve everywhere; that fragments capacity — use **shares** for priority.

**Rollback:** `Get-VM app01 | Move-VM -Destination (Get-Cluster Cluster1); Remove-ResourcePool prod8 -Confirm:$false`.

### Lab 7.5 — Verify HA readiness

**Objective:** Confirm the cluster can absorb a failure.

```powershell
Get-Cluster Cluster1 | Select Name, HAEnabled,
  @{N='FailoverLevel';E={$_.ExtensionData.Configuration.DasConfig.AdmissionControlPolicy.FailoverLevel}}
```

**Expected result:** HA with an **admission-control failover level** reserving capacity — ready to
recover.

**Negative test:** run at full utilization with no reserved capacity; failover has nowhere to
restart VMs — size admission control.

**Rollback:** none (read-only).

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

vSphere 8 keeps DRS, HA, resource controls, and EVC, and speeds migration with vMotion unified data
transport for large and accelerated VMs. Run DRS+HA with admission control, set EVC early, keep
vMotion networking fast, and use resource controls deliberately.

- [ ] I can enable DRS and HA with admission control.
- [ ] I can live-migrate a VM (unified data transport).
- [ ] I can set an EVC baseline.
- [ ] I can configure resource pools/shares and verify HA readiness.
- [ ] I completed Labs 7.1–7.5 including each negative test.
