# Chapter 08: Lifecycle, Security, and Tanzu

## Learning Objectives

- Use vSphere Lifecycle Manager (vLCM) for image-based host lifecycle.
- Harden ESXi and vCenter (lockdown mode, certificates, roles).
- Standardize hosts with host profiles.
- Understand vSphere with Tanzu (Kubernetes on vSphere).
- Complete a walkthrough for each lifecycle/security topic.

## Theory and Architecture

vSphere 7 introduced **vSphere Lifecycle Manager (vLCM)** — managing a cluster to a **desired-state
image** (ESXi version + vendor add-ons + firmware) so every host is identical and remediation is
consistent, alongside the legacy **baseline** model (VUM). **Security** spans the stack: **lockdown
mode** restricts direct host access to vCenter only; the **VMCA** issues and manages certificates;
**roles/permissions** (Chapter 3) enforce least privilege; and hardening follows the vSphere
Security Configuration Guide (disable unused services, secure boot, encryption). **Host profiles**
capture a reference host's configuration and apply/check it across the cluster for compliance.
Finally, **vSphere with Tanzu** turns a cluster into a **Kubernetes** platform: enabling the
**Supervisor** lets vSphere run Kubernetes workloads (vSphere Pods, Tanzu Kubernetes clusters)
alongside VMs, managed through the same vCenter — the platform runs both VMs and containers.

## Design Considerations

Adopt **vLCM image-based** lifecycle for consistency and firmware coordination. Enable **lockdown
mode**, manage **certificates**, and follow the **hardening guide**. Enforce configuration with
**host profiles**. Where you need Kubernetes, enable **vSphere with Tanzu** rather than standing up
a separate stack. Patch on a schedule via vLCM.

## Implementation and Automation

The labs inspect vLCM, check lockdown mode, and reason about host profiles and Tanzu.

## Validation and Troubleshooting

Confirm the lifecycle/security model:

```text
vLCM: desired-state IMAGE (ESXi + add-ons + firmware) per cluster (+ legacy baselines/VUM).
Security: lockdown mode (host access via vCenter only), VMCA certs, least-privilege roles, hardening guide.
Host profiles: apply/check reference config for compliance. vSphere with Tanzu: Supervisor -> K8s + VMs on one platform.
```

Common pitfalls: mixing **baseline and image** management inconsistently; and leaving hosts out of
**lockdown**/hardening.

## Security and Best Practices

Standardize with **vLCM images** and **host profiles**, enable **lockdown mode**, manage
**certificates**, and follow the **Security Configuration Guide**. Patch regularly. Use **Tanzu** to
run Kubernetes on the same governed platform. Consistency and hardening reduce risk.

## Hands-On Lab

Lifecycle/security walkthroughs. **Shared prerequisites** — vCenter 7 with a cluster and hosts,
PowerCLI/esxcli, in a lab. **Cost:** none.

### Lab 8.1 — Inspect vLCM image management

**Objective:** Review the cluster's desired-state image.

```powershell
# vLCM manages a cluster to a desired image (ESXi version + components).
Get-Cluster Cluster1 | Get-LcmImage -ErrorAction SilentlyContinue
# Or check baseline compliance (legacy) / image compliance in the UI.
Get-Cluster Cluster1 | Select Name
```

**Expected result:** the cluster's **image/lifecycle** configuration — the basis for consistent
remediation.

**Negative test:** patch hosts individually with ad-hoc bundles; **vLCM images** keep the cluster
identical — manage centrally.

**Rollback:** none (read-only).

### Lab 8.2 — Enable lockdown mode

**Objective:** Restrict direct host access.

```powershell
$h = (Get-VMHost)[0]
$h | Get-VMHostAuthentication | Out-Null
(Get-View $h.ExtensionData.ConfigManager.HostAccessManager).ChangeLockdownMode("lockdownNormal")
Get-VMHost $h | Select Name, @{N='Lockdown';E={$_.ExtensionData.Config.LockdownMode}}
```

**Expected result:** the host in **lockdown mode** — direct access restricted to vCenter, reducing
exposure.

**Negative test:** leave hosts with open direct root access; **lockdown mode** funnels access through
vCenter — enable it.

**Rollback:** set lockdown mode back to `lockdownDisabled` in a lab.

### Lab 8.3 — Host profile compliance

**Objective:** Standardize and check host configuration.

```powershell
$profile = New-VMHostProfile -Name "gold" -ReferenceHost (Get-VMHost)[0]
Test-VMHostProfileCompliance -VMHost (Get-VMHost) -Profile $profile
```

**Host setup — deploying this image on your hypervisor.** The create/import and interface-mapping steps are the same for every appliance and are collected once in the Master Appendices: [Deploying Lab Appliance Images on Each Hypervisor](../../volume-997-master-appendices/chapters/73-appendix-deploying-lab-appliance-images-on-each-hypervisor.md) — Proxmox, KVM, ESXi/vSphere, Workstation/Fusion, VirtualBox, Hyper-V, EVE-NG, GNS3, containerlab, Nutanix AHV, and Xen.

**Expected result:** a **host profile** capturing a reference config and a **compliance check**
across hosts — configuration drift caught.

**Negative test:** assume hosts are identical without checking; **host profiles** verify compliance —
test it.

**Rollback:** `Remove-VMHostProfile gold -Confirm:$false`.

### Lab 8.4 — vSphere with Tanzu concept

**Objective:** Understand Kubernetes on vSphere.

```text
# Enabling the Supervisor on a cluster turns vSphere into a Kubernetes platform: run vSphere Pods and
#   Tanzu Kubernetes clusters alongside VMs, managed via vCenter with the same networking/storage/policy.
"vSphere with Tanzu: Supervisor -> K8s workloads + VMs on one vSphere platform"
```

**Expected result:** the **vSphere with Tanzu** model — Kubernetes and VMs on one governed platform.

**Negative test:** stand up a separate, ungoverned Kubernetes stack beside vSphere; **Tanzu** runs
K8s on the same platform — use it where it fits.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

vSphere 7 lifecycle and security cover vLCM image-based host management, lockdown mode and
certificate/role hardening, host-profile compliance, and vSphere with Tanzu for Kubernetes on the
platform. Standardize with images and profiles, harden with lockdown and the config guide, and run
Kubernetes via Tanzu.

- [ ] I can inspect vLCM lifecycle management.
- [ ] I can enable lockdown mode.
- [ ] I can check host-profile compliance.
- [ ] I can explain vSphere with Tanzu.
- [ ] I completed Labs 8.1–8.4 including each negative test.
