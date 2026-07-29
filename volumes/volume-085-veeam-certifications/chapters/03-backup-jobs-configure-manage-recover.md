# Chapter 03: Backup Jobs — Configure, Manage, Recover

## Learning Objectives

- Create and run a backup job.
- Apply GFS (grandfather-father-son) retention.
- Enable application-aware processing.
- Perform a file-level and full restore.
- Complete a walkthrough for each backup-and-recover topic.

## Theory and Architecture

The first VMCE+ training — **Veeam Backup & Replication: Configure, Manage, and Recover** — is the core
of the credential. A **backup job** defines what to protect (VMs, physical machines via agents, cloud
workloads), where to store it (a repository), and on what schedule. Veeam's default backup mode creates
periodic full backups with intervening **incrementals** (forever-forward or with synthetic fulls).
Retention is governed by restore points and **GFS (grandfather-father-son)** — keeping weekly, monthly,
and yearly full backups for long-term retention. **Application-aware processing** quiesces applications
(VSS on Windows; database log handling for SQL Server, Oracle, and others) so restores are
transactionally consistent, and enables transaction-log backup and truncation. Recovery is the point of
it all: **file-level recovery**, **full VM/machine restore**, **Instant Recovery** (Chapter 04), and
application item recovery. This chapter teaches configure/manage/recover with hands-on Veeam PowerShell
walkthroughs.

## Design Considerations

Group workloads into **jobs** by SLA and repository. Set **retention** (restore points) plus **GFS** to
meet compliance retention. Enable **application-aware processing** for databases and domain controllers
so backups are consistent and logs are managed. Schedule jobs within the backup window and stagger to
avoid proxy/repository contention. Test **restores** regularly — a backup is only as good as its
recovery.

## Implementation and Automation

The labs create a backup job, apply GFS retention, enable application-aware processing, and run a
restore — the lifecycle the first VMCE+ course validates.

## Validation and Troubleshooting

Confirm the backup lifecycle:

```text
Job = what (workloads) + where (repository) + when (schedule); full + incrementals
Retention = restore points + GFS (weekly/monthly/yearly) for long-term
App-aware = VSS / DB log handling -> transactionally consistent restore + log truncation
Recover = file-level / full restore / Instant Recovery / application items
```

Common pitfalls: relying on crash-consistent backups for databases (no **application-aware
processing**); and setting retention too low to meet a compliance requirement (add **GFS**).

## Security and Best Practices

Encrypt backups, keep at least one copy immutable (Chapter 08), and verify restores. Application-aware
processing and tested recovery are core to defensible data protection. All work is authorized.

## Hands-On Lab

Backup-and-recover walkthroughs. **Shared prerequisites** — a Veeam Backup & Replication Community
Edition server with a repository (`Repo-01`) and at least one protected workload; the Veeam PowerShell
module. **Cost:** none.

### Lab 3.1 — Create and run a backup job

**Objective:** Protect a workload.

```powershell
PS> $vm = Find-VBRViEntity -Name "app-vm01"
PS> $repo = Get-VBRBackupRepository -Name "Repo-01"
PS> Add-VBRViBackupJob -Name "Daily-App" -Entity $vm -BackupRepository $repo
PS> Start-VBRJob -Job (Get-VBRJob -Name "Daily-App")

PS> Get-VBRJob -Name "Daily-App" | Select-Object Name, LastResult, LastState
Name       LastResult LastState
----       ---------- ---------
Daily-App  Success    Stopped
```

**Expected result:** a backup job that runs to `Success` — a first restore point exists.

**Negative test:** create a job but never run or schedule it; there is no restore point — schedule and
run it.

**Cleanup:**

```powershell
PS> Remove-VBRJob -Job (Get-VBRJob -Name "Daily-App") -Confirm:$false
```

### Lab 3.2 — Apply GFS retention

**Objective:** Keep long-term restore points.

```powershell
PS> $job = Get-VBRJob -Name "Daily-App"
PS> Set-VBRJobAdvancedBackupOptions -Job $job -EnableGFS $true -WeeklyBackup 4 -MonthlyBackup 12 -YearlyBackup 7
PS> (Get-VBRJobObject -Job $job).Job.BackupStorageOptions | Select-Object RetainCycles

RetainCycles
------------
14
```

**Expected result:** GFS keeping 4 weekly, 12 monthly, and 7 yearly fulls — long-term retention.

**Negative test:** keep only 14 daily restore points for a 7-year compliance need; you cannot restore
last year — enable **GFS**.

**Cleanup:** none (removed with the job).

### Lab 3.3 — Enable application-aware processing

**Objective:** Make database backups consistent.

```powershell
PS> $job = Get-VBRJob -Name "Daily-App"
PS> Enable-VBRJobGuestProcessing -Job $job
PS> Set-VBRJobVSSOptions -Job $job -Type Backup -TransactionLogsProcessing TruncateLogs

PS> (Get-VBRJobVSSOptions -Job $job) | Select-Object AreApplicationsTreatedAsGuest
AreApplicationsTreatedAsGuest
-----------------------------
True
```

**Expected result:** application-aware processing on, with SQL/exchange log truncation — consistent
restores.

**Negative test:** back up a SQL Server crash-consistently; logs are never truncated and restores may
be inconsistent — enable application-aware processing.

**Cleanup:** none (removed with the job).

### Lab 3.4 — Perform a restore

**Objective:** Recover data from a restore point.

```powershell
PS> $rp = Get-VBRRestorePoint -Name "app-vm01" | Sort-Object CreationTime -Descending | Select-Object -First 1
PS> Start-VBRWindowsFileRestore -RestorePoint $rp

PS> Get-VBRRestoreSession | Select-Object JobName, State, Result | Select-Object -First 1
JobName          State   Result
-------          -----   ------
Daily-App        Working Success
```

**Expected result:** a file-level restore session recovering data from the latest restore point.

**Negative test:** assume a backup is good without ever restoring; test recovery regularly — an
untested backup is not a guarantee.

**Cleanup:**

```powershell
PS> Stop-VBRWindowsFileRestore -FileRestore (Get-VBRWindowsFileRestore)
```

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The core VMCE+ skill is the backup lifecycle: backup jobs (workloads + repository + schedule) with GFS
retention for the long term, application-aware processing for transactionally consistent database
backups, and tested recovery — file-level, full, and application-item restores.

- [ ] I can create and run a backup job.
- [ ] I can apply GFS retention.
- [ ] I can enable application-aware processing.
- [ ] I can perform a restore.
- [ ] I completed Labs 3.1–3.4 including each negative test.
