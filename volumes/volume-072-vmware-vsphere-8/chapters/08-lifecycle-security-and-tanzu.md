# Chapter 08: Lifecycle, Security, and Tanzu

## Learning Objectives

- Use vSphere Lifecycle Manager 8, including DPU lifecycle and the end of baselines.
- Harden ESXi 8 and vCenter 8 (lockdown, config profiles, TPM).
- Understand Tanzu enhancements (workload availability zones, supervisor services).
- Plan the migration from baseline to image-based lifecycle.
- Complete a walkthrough for each lifecycle/security topic.

## Theory and Architecture

vSphere 8 advances lifecycle and security. **vSphere Lifecycle Manager (vLCM)** now manages the
**DPU firmware/software lifecycle** together with the host image, and — importantly — **vSphere 8 is
the last release to support the legacy baseline (VUM) model**, so organizations should migrate to
**image-based** cluster management. vSphere 8 U2+ also introduces **configuration profiles** — a
desired-state, cluster-wide **configuration** model (the successor direction to host profiles).
**Security** builds on vSphere 7: **lockdown mode**, the **VMCA** and certificate management,
least-privilege **roles**, **TPM 2.0** attestation and secure boot, VM encryption, and — with the
DPU/DSE — **hardware-isolated** infrastructure services. On the platform side, **vSphere with
Tanzu** gains **workload availability zones** (spreading Kubernetes workloads across failure
domains) and **supervisor services** (extending the Supervisor with additional services). Together
these make vSphere 8 more consistent to operate, more secure, and a stronger Kubernetes platform.

## Design Considerations

Adopt **image-based vLCM** now (baselines end after 8) and let vLCM manage **DPU + host** together.
Explore **configuration profiles** for desired-state config. Enable **lockdown**, **TPM/secure
boot**, and certificate hygiene. Use **workload availability zones** for resilient Tanzu workloads.
Patch on a schedule via vLCM.

## Implementation and Automation

The labs inspect vLCM/image lifecycle, enable lockdown, and reason about Tanzu availability zones.

## Validation and Troubleshooting

Confirm the lifecycle/security model:

```text
vLCM 8: desired-state IMAGE + DPU lifecycle; 8 is LAST release to support baselines (migrate to images).
Config profiles (8 U2+): desired-state cluster config (successor to host profiles).
Security: lockdown, VMCA certs, least-privilege roles, TPM 2.0 + secure boot, VM encryption, DPU isolation.
Tanzu: workload availability zones (failure-domain spread) + supervisor services.
```

Common pitfalls: staying on **baseline** lifecycle (ending after 8); and skipping **TPM/secure
boot** hardening.

## Security and Best Practices

Standardize on **vLCM images** and **configuration profiles**, enable **lockdown**, **TPM/secure
boot**, and certificate management, and use **DPU isolation** where available. Spread Tanzu
workloads across **availability zones**. Patch regularly. Consistency and hardware-rooted trust
reduce risk.

## Hands-On Lab

Lifecycle/security walkthroughs. **Shared prerequisites** — vCenter 8 with a cluster and hosts,
PowerCLI/esxcli, in a lab. **Cost:** none.

### Lab 8.1 — Inspect image-based lifecycle

**Objective:** Review the cluster's desired-state image (and DPU).

```powershell
# vLCM manages the cluster to a desired image (ESXi + components + firmware, incl. DPU).
Get-Cluster Cluster1 | Select Name
# Check image/compliance in the UI; baselines are deprecated after vSphere 8.
Write-Output "vSphere 8 is the last release to support baselines -> use images"
```

**Expected result:** the cluster's **image-based** lifecycle (with DPU) — the forward model.

**Negative test:** keep managing with **baselines**; they end after vSphere 8 — migrate to
**images** now.

**Rollback:** none (read-only).

### Lab 8.2 — Enable lockdown mode

**Objective:** Restrict direct host access.

```powershell
$h = (Get-VMHost)[0]
(Get-View $h.ExtensionData.ConfigManager.HostAccessManager).ChangeLockdownMode("lockdownNormal")
Get-VMHost $h | Select Name, @{N='Lockdown';E={$_.ExtensionData.Config.LockdownMode}}
```

**Expected result:** the host in **lockdown mode** — direct access funneled through vCenter.

**Negative test:** leave open direct root access; **lockdown mode** reduces exposure — enable it.

**Rollback:** set lockdown back to `lockdownDisabled` in a lab.

### Lab 8.3 — Verify secure boot / TPM

**Objective:** Confirm hardware-rooted trust.

```bash
esxcli system settings encryption get
# Secure Boot + TPM 2.0 provide attestation of the ESXi boot chain (host attestation in vCenter).
esxcli hardware trustedboot get 2>/dev/null || echo "TPM 2.0 + Secure Boot -> ESXi boot attestation"
```

**Expected result:** **secure boot / TPM** status — hardware-rooted boot integrity for the host.

**Negative test:** run ESXi with **no secure boot/TPM** on capable hardware; enable them for boot
attestation.

**Rollback:** none (read-only).

### Lab 8.4 — Tanzu workload availability zones

**Objective:** Understand resilient Kubernetes on vSphere 8.

```text
# Workload availability zones map Kubernetes workloads to vSphere failure domains (e.g., separate
#   clusters/racks) so a zone failure doesn't take down the whole app. Supervisor services extend the platform.
"Tanzu AZ: spread K8s workloads across vSphere failure domains -> zone-fault-tolerant apps"
```

**Expected result:** the **workload availability zone** model — resilient Kubernetes on vSphere 8.

**Negative test:** run all Tanzu workloads in one failure domain; **availability zones** spread them
— use them for resilience.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

vSphere 8 lifecycle and security advance with image-based vLCM (including DPU lifecycle; baselines
end after 8), configuration profiles, TPM/secure-boot attestation and the usual hardening, and DPU
isolation, plus Tanzu workload availability zones and supervisor services. Move to images now,
harden with TPM/lockdown, and spread Tanzu workloads across zones.

- [ ] I can inspect image-based lifecycle (and the baseline sunset).
- [ ] I can enable lockdown mode.
- [ ] I can verify secure boot / TPM.
- [ ] I can explain Tanzu workload availability zones.
- [ ] I completed Labs 8.1–8.4 including each negative test.
