# Chapter 04: Replication and Recovery

## Learning Objectives

- Create a replication job to a DR host.
- Perform planned and unplanned failover.
- Fail back to production.
- Perform Instant Recovery.
- Complete a walkthrough for each replication-and-recovery topic.

## Theory and Architecture

Beyond backups, Veeam provides **replication** for low-RTO disaster recovery. A **replication job**
maintains a ready-to-run **replica** of a VM at a DR site, kept current by periodic increments and a
chain of restore points. On a disaster you **fail over** to the replica (bringing it online at the DR
site); **planned failover** does this gracefully for migrations, while **unplanned failover** is for
outages. When production is restored you **fail back**, then **commit** the failback. For fast recovery
from backups, **Instant Recovery** runs a workload **directly from the backup file** (mounting it as a
datastore) so it is available in minutes while the full restore proceeds in the background —
**SureBackup** (Chapter 07) verifies recoverability without touching production. This chapter teaches
replication and rapid recovery with hands-on Veeam PowerShell walkthroughs.

## Design Considerations

Use **replication** (not just backup) for workloads needing minutes of RTO. Keep replica restore points
for failback flexibility and to recover from corruption/ransomware (fail over to a clean point). Use
**Instant Recovery** to meet aggressive RTOs from backups. Plan **failover** and **failback** runbooks,
and rehearse them (Recovery Orchestrator, Chapter 07). Watch replica seeding and WAN bandwidth for
remote DR.

## Implementation and Automation

The labs create a replication job, run a planned failover, fail back, and perform Instant Recovery — the
recovery operations VMCE+ expects.

## Validation and Troubleshooting

Confirm the recovery model:

```text
Replication = ready-to-run replica at DR (periodic increments + restore points)
Failover: planned (graceful) vs unplanned (outage); Failback -> Commit
Instant Recovery = run workload directly from the backup file (RTO minutes)
SureBackup = verify recoverability in an isolated lab (no production impact)
```

Common pitfalls: replicating with only one restore point (cannot fail over to a pre-corruption/clean
point); and forgetting to **commit** failback (leaving the replica in a temporary state).

## Security and Best Practices

Keep multiple replica restore points so you can fail over to a clean, pre-ransomware point; isolate the
DR network; and test failover. Recovery is defensive protection of your own workloads. All work is
authorized.

## Hands-On Lab

Replication-and-recovery walkthroughs. **Shared prerequisites** — a Veeam Backup & Replication Community
Edition server, a source workload with a backup, and a DR host; the Veeam PowerShell module. **Cost:**
none.

### Lab 4.1 — Create a replication job

**Objective:** Maintain a DR replica.

```powershell
PS> $vm = Find-VBRViEntity -Name "app-vm01"
PS> $host = Get-VBRServer -Name "dr-esxi01"
PS> Add-VBRViReplicaJob -Name "Repl-App" -Entity $vm -Server $host -RestorePointsToKeep 7
PS> Get-VBRJob -Name "Repl-App" | Select-Object Name, JobType, LastResult

Name      JobType     LastResult
----      -------     ----------
Repl-App  Replication Success
```

**Expected result:** a replication job keeping 7 restore points of the replica at the DR host.

**Negative test:** keep a single replica restore point; a ransomware event replicates the damage — keep
several so you can fail over to a clean point.

**Rollback:**

```powershell
PS> Remove-VBRJob -Job (Get-VBRJob -Name "Repl-App") -Confirm:$false
```

### Lab 4.2 — Perform a planned failover

**Objective:** Bring the replica online gracefully.

```powershell
PS> $replica = Get-VBRReplica -Name "app-vm01_replica"
PS> Start-VBRPlannedFailover -Replica $replica

PS> Get-VBRReplica -Name "app-vm01_replica" | Select-Object Name, State
Name              State
----              -----
app-vm01_replica  Failover
```

**Expected result:** the replica in `Failover` state — running at the DR site.

**Negative test:** use unplanned failover for a graceful migration; **planned** failover syncs final
changes first — use it when the source is healthy.

**Rollback:** (see failback in Lab 4.3).

### Lab 4.3 — Fail back and commit

**Objective:** Return to production.

```powershell
PS> $replica = Get-VBRReplica -Name "app-vm01_replica"
PS> Start-VBRFailback -Replica $replica -ToOriginalLocation
PS> Complete-VBRFailback -Replica $replica

PS> Get-VBRReplica -Name "app-vm01_replica" | Select-Object State
State
-----
Ready
```

**Expected result:** failback completed and committed — production is primary again, replica `Ready`.

**Negative test:** leave failover uncommitted indefinitely; the replica stays in a temporary state —
commit failback (or the failover) to finalize.

**Rollback:** none (state returned to `Ready`).

### Lab 4.4 — Instant Recovery from a backup

**Objective:** Meet an aggressive RTO from a backup.

```powershell
PS> $rp = Get-VBRRestorePoint -Name "app-vm01" | Sort-Object CreationTime -Descending | Select-Object -First 1
PS> Start-VBRViInstantRecovery -RestorePoint $rp -Server (Get-VBRServer -Name "prod-esxi01")

PS> Get-VBRInstantRecovery | Select-Object VMName, State
VMName    State
------    -----
app-vm01  Mounted
```

**Expected result:** the VM running directly from the backup (`Mounted`) within minutes — RTO met while
the full restore proceeds.

**Negative test:** wait for a multi-hour full restore when minutes matter; use **Instant Recovery** to
run from the backup immediately.

**Rollback:**

```powershell
PS> Stop-VBRInstantRecovery -InstantRecovery (Get-VBRInstantRecovery)
```

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Veeam recovery spans replication for low-RTO DR (planned/unplanned failover and committed failback with
multiple replica restore points) and Instant Recovery to run a workload directly from a backup in
minutes — with SureBackup verification covered later.

- [ ] I can create a replication job.
- [ ] I can perform planned failover.
- [ ] I can fail back and commit.
- [ ] I can perform Instant Recovery.
- [ ] I completed Labs 4.1–4.4 including each negative test.
