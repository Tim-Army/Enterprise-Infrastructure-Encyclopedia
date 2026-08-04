# Chapter 06: Recovery Orchestration and Testing

## Learning Objectives

- Cover recovery orchestration: point-in-time, mass recovery, and recovery validation.
- Understand RTO/RPO and why *tested* recovery is the only real recovery.
- Model an orchestrated recovery and RTO/RPO measurement.

## Recovery is the point

Backups exist to be **recovered** — and the ransomware-era truth is that an untested recovery is a hope, not a plan (the "0 errors" of 3-2-1-1-0). Rubrik centers **fast, orchestrated, validated recovery**: recover to any point in time, recover many systems at once (mass recovery after a ransomware event), and **test recovery regularly** so you know it works before you need it.

| Concept | Meaning |
|:---|:---|
| **RPO (Recovery Point Objective)** | How much data you can afford to lose (drives snapshot frequency) |
| **RTO (Recovery Time Objective)** | How long you can afford to be down (drives recovery speed/orchestration) |
| **Point-in-time recovery** | Restore a workload to a specific clean snapshot |
| **Mass recovery** | Orchestrate recovery of many systems at once (ransomware event) |
| **Recovery validation** | Test-recover in isolation and verify integrity — proving recoverability |

## Hands-On Lab

Python models orchestration and RTO/RPO. **Cost:** none.

### Lab 6.1 — Measure RPO and RTO

**Objective:** Compute the two numbers every recovery plan lives by.

```bash
python3 - <<'EOF'
import datetime
incident = datetime.datetime(2026,8,4,12,0)          # ransomware detected
last_clean_snap = datetime.datetime(2026,8,4,8,0)    # last clean recovery point (Ch 04)
recovery_done = datetime.datetime(2026,8,4,14,30)    # systems back online
rpo = (incident - last_clean_snap).total_seconds()/3600
rto = (recovery_done - incident).total_seconds()/3600
print(f"RPO (data lost): {rpo:.1f}h of changes since the last clean snapshot")
print(f"RTO (downtime):  {rto:.1f}h from detection to recovery")
print(f"\nGold SLA (4h snaps) caps RPO at ~4h; orchestrated mass recovery caps RTO.")
print("Tighten RPO -> more frequent snapshots; tighten RTO -> orchestration + faster recovery.")
EOF
```

**Expected result:**

```text
RPO (data lost): 4.0h of changes since the last clean snapshot
RTO (downtime):  2.5h from detection to recovery
```

RPO (4h of lost changes) is set by snapshot frequency; RTO (2.5h down) is set by recovery speed and orchestration. RCSA-level operators design SLA Domains to hit RPO targets and use orchestration to hit RTO targets. These two numbers are how recovery is measured and how business requirements translate into policy.

**Negative test:** Setting a 4-hour RPO target but assigning workloads a daily-snapshot SLA — you'd lose up to 24h; RPO and snapshot frequency must match, a common RCSA design check.

**Cleanup:** None.

### Lab 6.2 — Orchestrated mass recovery

**Objective:** Model recovering many systems in the right order after a ransomware event.

```bash
python3 - <<'EOF'
# Mass recovery: restore in dependency order (infra first), from the last clean snapshot, in parallel where possible
systems = [
  {"name":"domain-controller", "tier":0, "depends_on":[]},
  {"name":"database",          "tier":1, "depends_on":["domain-controller"]},
  {"name":"app-server",        "tier":2, "depends_on":["database"]},
  {"name":"web-frontend",      "tier":2, "depends_on":["app-server"]},
]
order = sorted(systems, key=lambda s: s["tier"])
print("Orchestrated recovery order (from last clean snapshot):")
for s in order:
    dep = f" (after {', '.join(s['depends_on'])})" if s["depends_on"] else " (first)"
    print(f"  tier {s['tier']}: recover {s['name']}{dep}")
print("\nOrchestration encodes dependencies so services come back in a working order — not alphabetically.")
EOF
```

**Expected result:** Recovery ordered by dependency tier — domain controller first, then database, then app/web — all from the last clean snapshot. Orchestration is what makes **mass recovery** work: after ransomware hits hundreds of systems, restoring them in dependency order (and in parallel within a tier) is the difference between a coordinated recovery and chaos. RCSA/recovery material tests recovery planning, not just single-VM restore.

**Negative test:** Restoring systems alphabetically or all at once without dependency order — the app server comes up before its database and fails; orchestration encodes the order that makes services actually work.

**Cleanup:** None.

### Lab 6.3 — Recovery validation (the "0" in 3-2-1-1-0)

**Objective:** Test-recover and verify — prove recoverability before you need it.

```bash
python3 - <<'EOF'
# Regularly test-recover in isolation; verify integrity; record the result. An untested backup is a hope.
def validate_recovery(system, restore_ok, integrity_ok, boots_ok):
    checks = {"restore completed": restore_ok, "data integrity (hash match)": integrity_ok, "system boots/services up": boots_ok}
    failed = [c for c, ok in checks.items() if not ok]
    return "RECOVERABLE (validated)" if not failed else f"FAILED validation: {', '.join(failed)}"
print("database:", validate_recovery("database", True, True, True))
print("legacy-app:", validate_recovery("legacy-app", True, False, False))  # restores but corrupt/won't boot
EOF
```

**Expected result:** The database validates as recoverable; the legacy app restores but fails integrity/boot — a problem you **found in a test, not during a real disaster**. Recovery validation (isolated test-recover + verify) is what turns "we have backups" into "we can recover," the "0 errors" of the modern rule. Rubrik supports isolated recovery/testing to make this routine.

**Negative test:** Never testing recovery — the first real restore reveals the backup was corrupt or the app won't come up; validation exists precisely so that discovery happens in a drill, not an outage.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] RPO/RTO measured and tied to SLA/orchestration design.
- [ ] Orchestrated mass recovery in dependency order drilled.
- [ ] Recovery validation (test-recover + verify) internalized as the "0 errors" essential.
