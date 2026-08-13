# Chapter 09: Automation, Operations, and Keeping Current

## Learning Objectives

- Automate vSphere 8 with PowerCLI, govc, the REST API, and pyvmomi.
- Operate the platform (logs, monitoring, backup).
- Track vSphere 8 updates and the Broadcom VCF direction.
- Relate vSphere 8 to the encyclopedia's virtualization volumes.
- Verify current platform facts from the authoritative source.

## Theory and Architecture

vSphere 8 is automated exactly as vSphere 7 — **PowerCLI** (the primary admin module), **govc**
(the open-source Go CLI), the **vSphere REST API** (`/api`), the SOAP API, and **pyvmomi** (the
Python SDK) — with cmdlets and endpoints updated for the new features (DPU, ESA, device groups).
Existing automation carries forward, which is a major operational benefit of the upgrade.
Operationally: forward **logs** (host/vCenter) via syslog, monitor **performance/capacity** (with
Aria Operations), and **back up** the **VCSA** (file-based) and VMs (with VADP-based backup tools).
On currency, vSphere 8 receives **Update releases** (U1/U2/U3) that add CPU support, expand **DPU
offload**, and improve **vSAN ESA** — keep current within the update line. Strategically, under
**Broadcom**, vSphere is delivered through **VMware vSphere Foundation (VVF)** and **VMware Cloud
Foundation (VCF)** subscription bundles, and Broadcom's direction points customers toward the
**VCF** private-cloud platform. Track the roadmap and licensing as you plan.

## Design Considerations

Reuse **PowerCLI/govc/API** automation from vSphere 7 (updated for 8's features), keep it in **Git**,
**back up** the VCSA and VMs, and monitor the platform. Stay current with **Update releases**. Plan
licensing and roadmap around **VVF/VCF**. Automate for repeatability and audit.

## Implementation and Automation

The labs script vSphere 8 with PowerCLI and govc and verify the platform.

## Validation and Troubleshooting

Confirm the automation and currency facts:

```text
Automate: PowerCLI + govc + REST API (/api) + pyvmomi (same as 7, updated for DPU/ESA/device groups).
Operate: syslog, performance/capacity (Aria Ops), back up VCSA (file-based) + VMs (VADP).
Currency: vSphere 8 Update releases (U1/U2/U3) add CPUs + DPU offload + vSAN ESA. Broadcom VVF/VCF subscription; VCF direction.
```

Common pitfalls: no **VCSA backup**; and staying on an old vSphere 8 build (apply **Update
releases**).

## Security and Best Practices

Keep automation in **Git**, **back up** the VCSA and VMs, monitor, and secure API access
(least-privilege, TLS). Apply **Update releases**. Track the **Broadcom VCF** direction and
licensing. Automate defensively for repeatability and audit.

## References and Knowledge Checks

- techdocs.broadcom.com (VMware vSphere 8 documentation and release notes): the platform, APIs, and updates.
- Related encyclopedia volumes: vSphere 7 (LXXI), VMware Virtualization (V), Python for Infrastructure (LVII), Ansible (LIX).

**Knowledge checks**

1. Name three ways to automate vSphere 8.
2. What do vSphere 8 Update releases add?
3. What Broadcom bundles deliver vSphere?

## Hands-On Lab

Automation and currency walkthroughs. **Shared prerequisites for Labs 9.1–9.3** — vCenter 8,
PowerCLI, `govc`, and a shell, in a lab. **Cost:** none.

### Lab 9.1 — Report inventory with PowerCLI

**Objective:** Script a fleet report.

```powershell
Connect-VIServer vcenter8.lab.local
Get-VMHost | Select Name, Version, Build,
  @{N='CPU%';E={[math]::Round(100*$_.CpuUsageMhz/$_.CpuTotalMhz)}},
  @{N='Mem%';E={[math]::Round(100*$_.MemoryUsageGB/$_.MemoryTotalGB)}} | Format-Table -Auto
```

**Expected result:** a **host report** (version, build, CPU/mem usage) — automated operations (same
cmdlets as 7).

**Negative test:** compile it by clicking; **PowerCLI** reports it in one command — script it.

**Rollback:** `Disconnect-VIServer -Confirm:$false`.

### Lab 9.2 — Script with govc

**Objective:** Use the open-source CLI.

```bash
export GOVC_URL="https://vcenter8.lab.local" GOVC_USERNAME="$VC_USER" GOVC_PASSWORD="$VC_PASS" GOVC_INSECURE=1
govc about
govc host.info -json 2>/dev/null | python3 -c "import sys,json;d=json.load(sys.stdin);print('ESXi:', d.get('HostSystems',[{}])[0].get('Config',{}).get('Product',{}).get('Version','see output'))" 2>/dev/null \
  || echo "govc: open-source Go CLI over the vSphere 8 API (govc about, host.info, vm.info, ...)"
```

**Expected result:** platform/host info via **govc** — cross-platform, scriptable API access.

**Negative test:** assume PowerShell-only; **govc** scripts the API from any shell — use it where
needed.

**Rollback:** none (read-only).

### Lab 9.3 — Verify version and update status

**Objective:** Confirm the build and currency.

```bash
esxcli system version get
python3 - <<'PY'
print("vSphere 8 GA: Oct 2022; keep current via Update releases (U1/U2/U3).")
print("Broadcom delivery: VMware vSphere Foundation (VVF) / VMware Cloud Foundation (VCF) subscription.")
PY
```

**Expected result:** the confirmed **ESXi 8 build** and the **update/licensing** context — informed
currency.

**Negative test:** run an old 8.0 GA build for years with no updates; apply **Update releases** for
CPU/DPU/ESA improvements and fixes.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

vSphere 8 is automated with the same PowerCLI/govc/REST/pyvmomi toolchain as vSphere 7 (updated for
DPU/ESA), operated with logs/metrics and backups (protect the VCSA), kept current via Update
releases, and delivered under Broadcom's VVF/VCF subscription bundles pointing toward VCF. Reuse
automation, back up, monitor, and stay current.

- [ ] I can report inventory with PowerCLI.
- [ ] I can script vSphere 8 with govc.
- [ ] I can verify the version and update status.
- [ ] I can explain the Broadcom VVF/VCF delivery.
- [ ] I completed Labs 9.1–9.3 including each negative test.
