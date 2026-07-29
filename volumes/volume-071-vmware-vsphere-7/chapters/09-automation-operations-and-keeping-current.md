# Chapter 09: Automation, Operations, and Keeping Current

## Learning Objectives

- Automate vSphere 7 with PowerCLI, govc, the REST API, and pyvmomi.
- Operate the platform (logs, monitoring, backup).
- Explain the vSphere 7 support lifecycle and the upgrade to vSphere 8.
- Relate vSphere 7 to the encyclopedia's virtualization volumes.
- Verify current platform facts from the authoritative source.

## Theory and Architecture

vSphere is fully **automatable**. **PowerCLI** (the PowerShell module) is the most common admin
automation tool — thousands of cmdlets over the vSphere API. **govc** is a fast, open-source Go CLI
for scripting the API from any shell. The **vSphere REST API** (`/api`) and the SOAP API drive
everything, and **pyvmomi** is the official Python SDK. Operationally, vSphere emits **logs**
(host and vCenter, forwardable via syslog), exposes **performance metrics** (and integrates with
vRealize/Aria Operations), and must be **backed up** — protect the **VCSA** (file-based backup) and
VMs (with real backup tools using the vSphere APIs for Data Protection). On the lifecycle side,
**vSphere 7 reached end of general support on 2 April 2025** (technical guidance to April 2027), so
operations increasingly means **planning and executing the upgrade to vSphere 8**
([Volume LXXII](../../volume-072-vmware-vsphere-8/README.md)) — vCenter first, then hosts via vLCM,
respecting interoperability. Under **Broadcom**, licensing is **subscription** (VMware vSphere
Foundation / Cloud Foundation).

## Design Considerations

Automate routine operations with **PowerCLI/govc/API** from a Git source of truth. **Back up the
VCSA** and VMs, and monitor performance and capacity. Track the **support lifecycle** and plan the
**7→8 upgrade** (interoperability, backups, staged host remediation). Standardize on subscription
licensing per Broadcom's model.

## Implementation and Automation

The labs script vSphere with PowerCLI and govc, and verify the platform/lifecycle.

## Validation and Troubleshooting

Confirm the automation and currency facts:

```text
Automate: PowerCLI (PowerShell), govc (open-source Go CLI), vSphere REST API (/api), pyvmomi (Python).
Operate: logs/syslog, performance metrics (+ Aria Ops), back up the VCSA (file-based) + VMs (VADP tools).
Lifecycle: vSphere 7 EOGS 2 Apr 2025 -> upgrade to vSphere 8 (vCenter first, then hosts via vLCM). Broadcom subscription.
```

Common pitfalls: no **VCSA backup** (unrecoverable management plane); and running vSphere 7 as a
long-term platform past **general support**.

## Security and Best Practices

Keep automation in **Git**, back up the **VCSA** and VMs, monitor the platform, and secure API
access (least-privilege service accounts, TLS). Track the lifecycle and **upgrade to vSphere 8**.
Automate for repeatability and audit.

## References and Knowledge Checks

- techdocs.broadcom.com (VMware vSphere documentation): the platform, APIs, and lifecycle.
- Related encyclopedia volumes: vSphere 8 (LXXII), VMware Virtualization (V), Python for Infrastructure (LVII), Ansible (LIX).

**Knowledge checks**

1. Name three ways to automate vSphere.
2. What must you back up to protect the management plane?
3. When did vSphere 7 reach end of general support?

## Hands-On Lab

Automation and currency walkthroughs. **Shared prerequisites for Labs 9.1–9.3** — vCenter 7,
PowerCLI, `govc`, and a shell, in a lab. **Cost:** none.

### Lab 9.1 — Report inventory with PowerCLI

**Objective:** Script a fleet report.

```powershell
Connect-VIServer vcenter.lab.local
Get-VM | Select Name, PowerState, NumCpu, MemoryGB,
  @{N='Host';E={$_.VMHost.Name}}, @{N='Tools';E={$_.ExtensionData.Guest.ToolsStatus}} |
  Sort Name | Format-Table -Auto
```

**Expected result:** a **VM inventory report** (power, resources, host, Tools) — automated
operations.

**Negative test:** compile the inventory by clicking through the UI; **PowerCLI** reports it in one
command — script it.

**Cleanup:** `Disconnect-VIServer -Confirm:$false`.

### Lab 9.2 — Script with govc

**Objective:** Use the open-source CLI.

```bash
export GOVC_URL="https://vcenter.lab.local" GOVC_USERNAME="$VC_USER" GOVC_PASSWORD="$VC_PASS" GOVC_INSECURE=1
govc ls /
govc vm.info -json '*' 2>/dev/null | python3 -c "import sys,json;print('VMs via govc:', len(json.load(sys.stdin).get('virtualMachines') or []))" 2>/dev/null \
  || echo "govc: open-source Go CLI over the vSphere API (govc ls, vm.info, host.info, ...)"
```

**Expected result:** inventory listed via **govc** — cross-platform, scriptable API access.

**Negative test:** assume PowerShell is the only option; **govc** scripts the API from any shell —
use it where PowerShell isn't available.

**Cleanup:** none (read-only).

### Lab 9.3 — Verify version and plan the upgrade

**Objective:** Confirm the platform and lifecycle position.

```bash
esxcli system version get
python3 - <<'PY'
from datetime import date
print("vSphere 7 end of general support: 2025-04-02")
print("action: upgrade path -> vCenter 7->8 first, then hosts via vLCM (check interoperability + backups)")
PY
```

**Expected result:** the confirmed version and the **7→8 upgrade** plan (vCenter first) — informed
lifecycle operations.

**Negative test:** upgrade hosts before vCenter; **vCenter must be upgraded first** — follow the
supported order.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

vSphere 7 is automated with PowerCLI, govc, the REST API, and pyvmomi, operated with logs/metrics
and backups (protect the VCSA), and — being past general support (2 April 2025) — increasingly
upgraded to vSphere 8 (vCenter first, then hosts via vLCM), under Broadcom subscription licensing.
Automate, back up, monitor, and plan the upgrade.

- [ ] I can report inventory with PowerCLI.
- [ ] I can script vSphere with govc.
- [ ] I can verify the version and state the upgrade order.
- [ ] I can explain the vSphere 7 lifecycle position.
- [ ] I completed Labs 9.1–9.3 including each negative test.
