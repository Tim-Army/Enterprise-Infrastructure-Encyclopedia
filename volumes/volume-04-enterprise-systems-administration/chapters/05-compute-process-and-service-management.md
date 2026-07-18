# Chapter 05: Compute, Process, and Service Management

## Learning Objectives

- Explain the process lifecycle on Linux (fork/exec, process states) and
  Windows (`CreateProcess`, thread scheduling) and how each kernel
  allocates CPU time.
- Apply resource-control primitives — cgroups v2 on Linux, Job Objects on
  Windows — to bound CPU, memory, and task-count consumption per workload.
- Design `systemd` unit dependency chains and Windows service dependency
  graphs so startup and shutdown ordering is predictable rather than
  accidental.
- Schedule recurring work reliably with `systemd` timers, `cron`, and
  Windows Task Scheduler, including overlap prevention and misfire
  handling.
- Diagnose CPU, memory, and process-level contention using platform-native
  tooling on both operating systems.
- Right-size compute allocations for a workload from observed utilization
  rather than reflexive over-provisioning.

## Theory and Architecture

Chapters 02 and 03 introduced `systemd` services and the Windows Service
Control Manager (SCM) as the mechanisms that keep a workload running. This
chapter goes one layer deeper: how the operating system schedules the CPU
time and memory those processes consume, how administrators bound that
consumption so one workload cannot starve another, and how dependency and
scheduling logic keeps a fleet of services and jobs starting, stopping,
and running in the right order. Container-level compute abstraction
(namespaces, container runtimes) is covered in Volume VIII; this chapter
stays at the host operating system layer.

### The process as the unit of compute

A **process** is a running instance of a program: an address space, at
least one thread of execution, open file descriptors/handles, and
resource accounting. A **thread** is the actual unit the scheduler
dispatches onto a CPU core; a process may contain many threads sharing
its address space.

- **Linux** creates processes with `fork()` (duplicate the calling
  process) followed by `exec()` (replace the duplicate's image with a new
  program) — a two-call model that is why a Linux process briefly exists
  as a copy of its parent before becoming something new. Process states
  are `R` (running/runnable), `S`/`D` (sleeping, interruptible or
  uninterruptible — typically waiting on I/O), `T` (stopped), and `Z`
  (zombie — exited but not yet reaped by its parent).
- **Windows** creates processes with a single `CreateProcess` call that
  both allocates the new process object and loads its image, with no
  intermediate "copy of the parent" state. Threads within a process move
  through Windows' own state model (running, ready, waiting) under the
  same preemptive scheduler.

### CPU scheduling

Both platforms use preemptive, priority-influenced schedulers, but the
mechanics differ:

- **Linux** has used the Completely Fair Scheduler (CFS) as its default
  scheduling class for ordinary processes for over a decade, with EEVDF
  (Earliest Eligible Virtual Deadline First) available as the selectable
  scheduler in current kernels; both aim to give every runnable task a
  fair share of CPU time weighted by its **nice** value (-20, highest
  priority, to 19, lowest). Real-time scheduling classes (`SCHED_FIFO`,
  `SCHED_RR`) exist for latency-sensitive workloads but should be used
  deliberately — a misbehaving real-time process can starve every normal
  process on the host.
- **Windows** uses a preemptive, priority-based scheduler with six process
  priority classes (`Idle`, `BelowNormal`, `Normal`, `AboveNormal`,
  `High`, `Realtime`) further modified by each thread's relative priority
  within its process, producing 31 effective priority levels. Windows also
  applies **priority boosting** — a temporary priority increase for a
  thread that just became runnable after waiting, or for the thread
  owning the foreground window — to keep the system responsive under
  load.

### Resource control: cgroups v2 and Job Objects

Scheduling priority alone does not stop a workload from consuming all
available memory or spawning enough processes to exhaust the process
table. Both platforms provide a grouping primitive for hard resource
limits:

- **cgroups v2** (control groups) organize processes into a single
  unified hierarchy, with controllers — `cpu`, `memory`, `io`, `pids`,
  `cpuset` — attaching limits to each group. `systemd` maps its own unit
  hierarchy directly onto cgroups: every service, scope, and slice is a
  cgroup, so resource-control directives in a unit file (`CPUQuota=`,
  `MemoryMax=`, `TasksMax=`) require no separate tooling to take effect.
- **Job Objects** are the Windows equivalent grouping primitive: a
  collection of processes that share CPU rate limits, memory limits, and
  a process-count limit, and that can be terminated as a single unit.
  Unlike `systemd`, ordinary Windows services are **not** automatically
  placed in a resource-limited Job Object; IIS application pools and
  container runtimes use Job Objects internally, but a service
  administrators create through the SCM has no CPU/memory ceiling unless
  something explicitly assigns one (IIS's per-application-pool CPU limit
  being the most common enterprise example).

### Service dependency model

`systemd` expresses startup/shutdown ordering and requirement strength
separately, which is a common source of confusion:

| Directive | Meaning |
| --- | --- |
| `Wants=` | Weak dependency: try to start the target unit, but do not fail this unit if it fails |
| `Requires=` | Strong dependency: this unit fails if the required unit fails |
| `After=` / `Before=` | Ordering only — does **not** imply a requirement; a unit can be ordered `After=` another without `Wants=`/`Requires=` it |
| `Conflicts=` | Mutual exclusion: starting this unit stops the conflicting unit |

The Windows SCM expresses only ordering/requirement, combined into a
single `DependOnService` (and `DependOnGroup`) list per service: a
dependent service will not start until every service it depends on has
reported `RUNNING`, and stopping a depended-upon service stops its
dependents first.

### Job scheduling architecture

- **`cron`** reads per-user and system crontabs (`crontab -e`,
  `/etc/cron.d/*`) on a five-field schedule (`minute hour day month
  weekday`). `anacron` supplements `cron` on hosts that are not always
  powered on, running missed jobs once the system is back up.
  **`systemd` timers** (introduced in Chapter 02) are the modern
  replacement: `OnCalendar=` expressions, `Persistent=true` to catch up a
  missed run, and — critically — activation of a `.service` unit rather
  than a raw command line, which brings the full `systemd` sandboxing and
  resource-control surface to scheduled work.
- **Windows Task Scheduler** triggers on time, logon, system event, or
  idle state, and exposes a **multiple-instance policy**
  (`IgnoreNew`, `Parallel`, `Queue`, `StopExisting`) that directly answers
  the overlap question `cron` leaves to the administrator.

## Design Considerations

- **Size from measurement, not convention.** Doubling a requested vCPU or
  memory allocation "to be safe" produces fleet-wide overcommitment that
  a hypervisor or cloud billing model eventually surfaces as cost. Baseline
  actual utilization (Implementation and Automation, below) before sizing
  a new workload's request.
- **Resource limits are a fairness control, not only a performance one.**
  A `CPUQuota=`/memory ceiling on a multi-tenant host protects every other
  workload from one runaway process — treat it as a standing control on
  shared hosts, not an optional tuning exercise.
- **Ordering (`After=`) is not a substitute for requirement
  (`Requires=`).** A unit ordered after a database but not requiring it
  will still start — and likely fail at runtime — if the database unit
  itself failed. Decide explicitly which failures should cascade.
- **Overlap prevention must be designed, not assumed.** A `systemd` timer
  will not start a second instance of a service that is still running by
  default (`RemainAfterExit`/activation semantics), Task Scheduler's
  `IgnoreNew` policy does the same explicitly, but a raw `cron` entry has
  no built-in protection — a slow job and a tight schedule will eventually
  overlap unless the job locks itself.
- **NUMA awareness on large hosts.** On multi-socket compute hosts,
  processes and their memory should stay pinned to the same NUMA node
  where the workload is sensitive to memory latency; `numactl` (Linux) and
  `Set-VMProcessor`/NUMA topology settings (Windows/Hyper-V hosts) are the
  relevant controls — deep coverage of virtualization-layer NUMA sizing is
  in Volume V.
- **Idempotent job design.** A scheduled job that partially applies its
  work and is interrupted should be safe to re-run without duplicating
  effect (recall Volume I's idempotency principle) — this matters more for
  scheduled jobs than for one-shot administrative commands, since jobs
  run unattended and failures are not immediately reviewed by a human.

## Implementation and Automation

### Inspecting and controlling processes on Linux

```bash
# Live process/resource view; sort by CPU or memory interactively with
# 'P' or 'M' inside top, or use ps for a scriptable snapshot.
ps -eo pid,ppid,ni,pri,stat,%cpu,%mem,cmd --sort=-%cpu | head -10

# Adjust a running process's scheduling priority (lower nice = higher
# priority); requires root to lower nice below 0.
sudo renice -n 5 -p 4821

# Live cgroup resource usage, grouped by systemd unit/slice — the
# resource-control analog to 'top'.
systemd-cgtop
```

### Bounding a service with cgroup resource control

```ini
# /etc/systemd/system/batch-worker.service
[Unit]
Description=Batch processing worker (resource-bounded)

[Service]
Type=simple
ExecStart=/usr/local/bin/batch-worker
Slice=batch.slice
CPUQuota=50%
MemoryMax=512M
TasksMax=100
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now batch-worker.service

# Tune a limit on a running unit without editing and reloading the file —
# useful for temporary throttling during an incident.
sudo systemctl set-property batch-worker.service CPUQuota=25%
systemctl show batch-worker.service -p CPUQuotaPerSecUSec -p MemoryMax
```

### Explicit dependency ordering

```ini
# /etc/systemd/system/report-generator.service
[Unit]
Description=Nightly report generator
Requires=postgresql.service
After=postgresql.service

[Service]
Type=oneshot
ExecStart=/usr/local/bin/generate-report.sh
```

```bash
systemctl list-dependencies report-generator.service
```

### Overlap-safe cron scheduling with `flock`

```bash
# /etc/cron.d/nightly-reconcile — flock -n exits immediately if the lock
# is already held, so a slow run never overlaps the next scheduled one.
*/15 * * * * appsvc /usr/bin/flock -n /var/lock/reconcile.lock /usr/local/bin/reconcile.sh
```

### Inspecting and controlling processes on Windows

```powershell
# Live process/resource view, sorted by CPU consumption.
Get-Process | Sort-Object CPU -Descending | Select-Object -First 10 `
    Name, Id, CPU, WorkingSet, PriorityClass

# Adjust a running process's priority class (equivalent in spirit to
# renice, though Windows expresses priority as a class rather than a
# single numeric scale).
(Get-Process -Name batch-worker).PriorityClass = 'BelowNormal'

# Query process detail via CIM/WMI, including parent process ID — useful
# for reconstructing a process tree.
Get-CimInstance Win32_Process -Filter "Name='batch-worker.exe'" |
    Select-Object ProcessId, ParentProcessId, CommandLine
```

### Bounding an application pool with a Job Object (IIS example)

```powershell
# IIS application pools run under a Job Object; CPU limiting is exposed
# directly through the application pool's recycling configuration rather
# than a general-purpose PowerShell Job Object cmdlet.
Import-Module WebAdministration
Set-ItemProperty 'IIS:\AppPools\BatchApiPool' -Name cpu.limit -Value 50000   # 50% of one core, in 1/1000ths of a percent
Set-ItemProperty 'IIS:\AppPools\BatchApiPool' -Name cpu.action -Value 'Throttle'
```

### Scheduled tasks with overlap control

```powershell
# Extends the Chapter 03 scheduled-task example with an explicit
# multiple-instance policy so a slow run cannot overlap the next trigger.
$action   = New-ScheduledTaskAction -Execute 'powershell.exe' `
    -Argument '-NoProfile -File C:\Scripts\Reconcile.ps1'
$trigger  = New-ScheduledTaskTrigger -Once -At (Get-Date) `
    -RepetitionInterval (New-TimeSpan -Minutes 15) `
    -RepetitionDuration ([TimeSpan]::MaxValue)
$settings = New-ScheduledTaskSettingsSet -MultipleInstances IgnoreNew

Register-ScheduledTask -TaskName 'NightlyReconcile' -Action $action `
    -Trigger $trigger -Settings $settings -User 'SYSTEM'
```

## Validation and Troubleshooting

- Confirm a unit's actual cgroup limits took effect:
  `systemctl show batch-worker.service -p CPUQuotaPerSecUSec -p MemoryMax`
  should match the configured values, and sustained CPU usage under load
  (`systemd-cgtop`) should plateau near the quota rather than exceed it.
- Confirm dependency enforcement: stop the required unit
  (`sudo systemctl stop postgresql.service`) and confirm the dependent
  unit refuses to start cleanly, citing the failed dependency in
  `systemctl status`.
- Confirm no overlapping executions: `journalctl -u nightly-reconcile` (or
  `Get-ScheduledTaskInfo` history) should never show two runs with
  overlapping start/end timestamps.
- Confirm Windows process priority actually changed:
  `(Get-Process -Name batch-worker).PriorityClass` should reflect the set
  value; note that some priority reductions require the process to
  briefly regain focus/activity before the OS reflects the change in
  scheduling behavior.

| Symptom | Likely cause | Diagnostic step |
| --- | --- | --- |
| Service consumes far more CPU than `CPUQuota=` allows | `CPUQuota=` set on the wrong unit, or the workload forks children outside the unit's cgroup | `systemd-cgtop`; confirm child PIDs are under the unit's cgroup with `systemctl status` |
| Zombie (`Z` state) processes accumulate | Parent process is not calling `wait()`/reaping children | `ps -eo stat,ppid,cmd \| grep '^Z'`; identify and fix/restart the parent |
| Scheduled job runs twice concurrently | `cron` entry with no lock, or Task Scheduler `MultipleInstances` left at default (`Parallel`) | Add `flock` to the cron entry; set `-MultipleInstances IgnoreNew` on the task |
| Dependent service fails at boot but starts fine manually later | `After=`/ordering present without `Requires=`, or Windows dependency list missing the actual dependency | `systemctl list-dependencies`; on Windows, `sc.exe qc <service>` to inspect `DEPENDENCIES` |
| Host is unresponsive but no single process shows high CPU | Many processes each below alerting threshold, or I/O wait masquerading as idle CPU | `vmstat 1` (watch the `wa` column); `pidstat -d 1` for per-process I/O |

## Security and Best Practices

- Treat cgroup/Job Object resource limits as a security control against
  denial-of-service, not only a performance tuning tool — a compromised or
  buggy process that can consume unbounded CPU, memory, or process-table
  slots can degrade every other workload on a shared host.
- Set `TasksMax=` on services that spawn child processes to bound
  fork-bomb-style exhaustion, whether malicious or accidental.
- Avoid granting `SCHED_FIFO`/`SCHED_RR` real-time scheduling or the
  Windows `Realtime` priority class to any workload that is not both
  trusted and genuinely latency-critical; a misbehaving real-time process
  can starve the rest of the host, including the processes administrators
  need to diagnose and fix it.
- Run scheduled jobs and services under a scoped service account
  (Chapter 02/03), never `root`/`SYSTEM`, and combine that identity
  restriction with the resource limits in this chapter rather than relying
  on either control alone.
- Version-control resource-control unit files and scheduled-task
  definitions alongside application deployment code so a limit change is
  reviewed the same way an application change is (Volume I, repository
  architecture).
- Alert on sustained throttling (a unit consistently hitting its
  `CPUQuota=`) as a capacity signal requiring a sizing decision, not as
  noise to suppress.

## References and Knowledge Checks

**References**

- `systemd.resource-control(5)`, `systemd.timer(5)`, `cgroups(7)` man
  pages.
- Microsoft Learn: "Job Objects," "Scheduling Priorities," and "Task
  Scheduler Schema."
- Brendan Gregg, "Systems Performance" — CPU scheduling and resource
  control chapters.
- IIS documentation: "Application Pool CPU Throttling."

**Knowledge Checks**

1. What is the practical difference between `After=` and `Requires=` in a
   `systemd` unit file, and why does confusing them cause boot-order
   incidents?
2. Why are ordinary Windows services not automatically confined by a
   resource-limited Job Object, unlike `systemd` services and cgroups?
3. What mechanism prevents a `systemd` timer-activated job from
   overlapping itself, and what must an administrator add to get the same
   protection for a raw `cron` entry?
4. Why should real-time scheduling classes be granted only to trusted,
   latency-critical workloads?
5. Name two Linux tools and two Windows tools for identifying which
   process is consuming the most CPU right now.

## Hands-On Lab

**Objective:** Constrain a CPU-bound workload with a `systemd`
resource-controlled service, observe the limit under load, and prevent a
scheduled job from overlapping itself with `flock` — demonstrating both
resource control and overlap prevention on a single Linux VM.

### Prerequisites

- One Linux VM (RHEL-family or Debian-family, 2 vCPU / 2 GB RAM minimum
  so throttling is observable against a real second core).
- `sudo` access.

### Procedure

1. Create a resource-bounded service that burns CPU in a tight loop:

   ```bash
   sudo tee /usr/local/bin/cpu-burn.sh <<'EOF'
   #!/bin/bash
   while :; do :; done
   EOF
   sudo chmod +x /usr/local/bin/cpu-burn.sh

   sudo tee /etc/systemd/system/cpu-burn.service <<'EOF'
   [Unit]
   Description=Lab CPU burn (resource-bounded)

   [Service]
   ExecStart=/usr/local/bin/cpu-burn.sh
   CPUQuota=50%
   EOF

   sudo systemctl daemon-reload
   sudo systemctl start cpu-burn.service
   ```

2. Observe the bounded CPU consumption for about 15 seconds:

   ```bash
   systemd-cgtop -n 3 -b | grep cpu-burn
   ```

   **Expected result:** CPU usage for `cpu-burn.service` stabilizes at
   approximately 50% of one core, not 100%.

3. Stop the bounded run:

   ```bash
   sudo systemctl stop cpu-burn.service
   ```

4. Remove the quota and confirm unbounded consumption (this is the
   negative test — proving the limit in step 2 was actually enforced, not
   coincidental):

   ```bash
   sudo systemctl set-property cpu-burn.service CPUQuota=
   sudo systemctl start cpu-burn.service
   systemd-cgtop -n 3 -b | grep cpu-burn
   sudo systemctl stop cpu-burn.service
   ```

   **Expected result:** CPU usage now approaches 100% of one core,
   confirming the earlier 50% figure came from `CPUQuota=`, not from the
   workload's own behavior.

5. Build an overlap-safe scheduled job and prove the lock works:

   ```bash
   sudo tee /usr/local/bin/slow-job.sh <<'EOF'
   #!/bin/bash
   echo "$(date): slow-job started" >> /var/log/slow-job.log
   sleep 20
   echo "$(date): slow-job finished" >> /var/log/slow-job.log
   EOF
   sudo chmod +x /usr/local/bin/slow-job.sh

   # Launch two overlapping attempts back to back, each guarded by flock.
   flock -n /var/lock/slow-job.lock /usr/local/bin/slow-job.sh &
   sleep 1
   flock -n /var/lock/slow-job.lock /usr/local/bin/slow-job.sh || \
     echo "Second invocation correctly refused: lock held"
   wait
   ```

   **Expected result:** the console prints
   `Second invocation correctly refused: lock held`, and
   `/var/log/slow-job.log` shows only one `started`/`finished` pair for
   that window.

### Negative Test

Step 4 above is this lab's primary negative test: removing `CPUQuota=`
and confirming CPU consumption rises to (approximately) 100% proves the
50% figure observed in step 2 was the result of the configured limit
rather than an unrelated ceiling (such as a single-vCPU VM).

### Cleanup

```bash
sudo systemctl disable --now cpu-burn.service
sudo rm -f /etc/systemd/system/cpu-burn.service /usr/local/bin/cpu-burn.sh
sudo systemctl daemon-reload
sudo rm -f /usr/local/bin/slow-job.sh /var/log/slow-job.log /var/lock/slow-job.lock
```

## Summary and Completion Checklist

This chapter moved from the service basics in Chapters 02 and 03 to the
compute layer underneath them: process lifecycle and scheduling on Linux
and Windows, cgroups v2 and Job Objects as resource-bounding primitives,
`systemd`'s explicit ordering-versus-requirement dependency model against
the Windows SCM's combined dependency list, and overlap-safe job
scheduling with `systemd` timers, `flock`-guarded `cron`, and Task
Scheduler's multiple-instance policy.

- [ ] Can explain the difference between process ordering (`After=`) and
      a hard requirement (`Requires=`) in `systemd`.
- [ ] Can bound a service's CPU and memory consumption with cgroup
      resource-control directives and verify the limit is enforced.
- [ ] Can prevent a scheduled job from overlapping itself on both
      `cron`/`systemd` timers and Windows Task Scheduler.
- [ ] Can identify which Linux and Windows tools show CPU, memory, and
      per-process I/O contention.
- [ ] Completed the hands-on lab, including the negative test proving
      the CPU quota — not an unrelated ceiling — caused the observed
      throttling.
