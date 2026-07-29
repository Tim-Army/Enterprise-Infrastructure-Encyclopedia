# Chapter 06: Veeam ONE — Monitor, Manage, Analyze

## Learning Objectives

- Explain the Veeam ONE role in the Data Platform.
- Configure alarms for backup and infrastructure health.
- Run reports and reason about capacity planning.
- Use analytics to catch protection gaps.
- Complete a walkthrough for each monitor-manage-analyze topic.

## Theory and Architecture

The second VMCE+ training — **Veeam Data Platform: Monitor, Manage, Analyze (Veeam ONE)** — covers
**Veeam ONE**, the monitoring, reporting, and analytics layer. Veeam ONE watches both the **backup
environment** (jobs, repositories, SLAs) and the **virtual/cloud infrastructure** (hosts, VMs, storage),
raising **alarms** on failures, capacity thresholds, and configuration drift. Its **reporting** produces
SLA compliance, protected-vs-unprotected VMs, capacity-planning forecasts, and change tracking; its
**analytics** and the **Veeam Threat Center** surface protection gaps and anomalies. Veeam ONE is how
you prove workloads are protected, catch problems before they become data loss, and forecast when
storage will run out. This chapter teaches monitor/manage/analyze with hands-on walkthroughs.

## Design Considerations

Tune **alarms** to the signals you will act on (failed jobs, missed SLAs, repository nearing full) and
route them to the right people. Schedule **reports** — protected-VMs and SLA compliance for governance,
capacity planning for procurement. Use analytics to find **unprotected** workloads and **anomalies**.
Right-size the Veeam ONE server for the environment. Avoid alarm fatigue by disabling noise.

## Implementation and Automation

The labs reason about the Veeam ONE role, configure an alarm, run a protection report, and read a
capacity-planning forecast — the observability the second VMCE+ course validates.

## Validation and Troubleshooting

Confirm Veeam ONE:

```text
Monitor: backup jobs/repositories/SLAs + infrastructure hosts/VMs/storage
Alarms: failures, capacity thresholds, config drift -> notify + act
Reports: SLA compliance, protected vs unprotected, capacity planning, change tracking
Analyze: Threat Center + anomalies -> find protection gaps early
```

Common pitfalls: monitoring only jobs (missing **unprotected** VMs that no job covers); and ignoring
**capacity-planning** forecasts until a repository fills mid-backup.

## Security and Best Practices

Alarm on failed and anomalous backups (early ransomware signal), report on unprotected workloads, and
review the Threat Center. Observability is defensive — it protects your own environment. All work is
authorized.

## Hands-On Lab

Monitor-manage-analyze walkthroughs. **Shared prerequisites** — a Veeam ONE server (or the concepts,
modeled in `python3`) against a Veeam Backup & Replication environment. **Cost:** none (Community/eval).

### Lab 6.1 — Reason about the Veeam ONE role

**Objective:** Place Veeam ONE in the platform.

```python
python3 - <<'PY'
veeam_one = {
  "Monitor":  "jobs, repositories, SLAs, hosts, VMs, storage",
  "Manage":   "alarms + notifications; act on issues before data loss",
  "Analyze":  "reports (SLA, protected/unprotected, capacity) + Threat Center anomalies",
}
for pillar, detail in veeam_one.items():
    print(f"{pillar:8}: {detail}")
print("Veeam ONE = the observability layer that proves protection and forecasts capacity")
PY
```

**Expected result:** the three Veeam ONE pillars — monitor, manage, analyze — mapped to real functions.

**Negative test:** treat Veeam ONE as optional and fly blind on SLAs and capacity; use it to prove
protection and forecast growth.

**Cleanup:** none.

### Lab 6.2 — Configure a backup-failure alarm

**Objective:** Get notified on job failures.

```text
Veeam ONE > Alarm Management > "Job state" alarm
  Rule:   Job Result = Failed  -> severity Error
  Rule:   Job Result = Warning -> severity Warning
  Notify: email backup-admins@lab.local; run remediation script (optional)
  Assign: all backup jobs
Result: any failed job raises an Error alarm and emails the team
```

**Expected result:** an alarm that fires on failed jobs and notifies the team — problems surface fast.

**Negative test:** rely on someone opening the console to notice failures; configure **alarms + email**
so failures push to you.

**Cleanup:** disable the test alarm if not needed.

### Lab 6.3 — Run a protection report

**Objective:** Prove which workloads are protected.

```python
python3 - <<'PY'
inventory = {"app-vm01": True, "db-vm02": True, "test-vm03": False, "dc-vm04": True}
protected   = [v for v, ok in inventory.items() if ok]
unprotected = [v for v, ok in inventory.items() if not ok]
print(f"Protected ({len(protected)}): {protected}")
print(f"UNPROTECTED ({len(unprotected)}): {unprotected}")
print("Action: add unprotected workloads to a backup job -> close the gap")
PY
```

**Expected result:** protected and **unprotected** VMs listed — the protection gap made visible.

**Negative test:** assume every VM is covered; the report reveals `test-vm03` is not — add it to a job.

**Cleanup:** none.

### Lab 6.4 — Read a capacity-planning forecast

**Objective:** Forecast when storage runs out.

```python
python3 - <<'PY'
used_tb, capacity_tb, daily_growth_tb = 42.0, 60.0, 0.6
days_to_full = round((capacity_tb - used_tb) / daily_growth_tb)
print(f"Used {used_tb}TB / {capacity_tb}TB; growth {daily_growth_tb}TB/day")
print(f"Repository full in ~{days_to_full} days -> plan expansion before then")
PY
```

**Expected result:** a forecast of days-to-full so you expand storage before backups fail.

**Negative test:** wait for a "repository full" error mid-backup; use the **capacity-planning** forecast
to expand ahead of time.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Veeam ONE is the Data Platform's observability layer: it monitors jobs, repositories, SLAs, and
infrastructure; raises alarms you act on; and reports on SLA compliance, protected-vs-unprotected
workloads, and capacity planning — with Threat Center analytics to surface gaps and anomalies early.

- [ ] I can explain the Veeam ONE monitor/manage/analyze role.
- [ ] I can configure a backup-failure alarm.
- [ ] I can run a protection report.
- [ ] I can read a capacity-planning forecast.
- [ ] I completed Labs 6.1–6.4 including each negative test.
