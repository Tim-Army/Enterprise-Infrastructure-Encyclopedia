# Chapter 09: Monitoring, Troubleshooting, and Lifecycle Operations

## Learning Objectives

- Build a host-level monitoring baseline that feeds the enterprise
  observability stack covered in depth in Volume XI.
- Use platform-native performance tools — `sar`/`vmstat`/`iostat`/
  `pidstat` on Linux, Performance Monitor/`Get-Counter` on Windows — to
  diagnose CPU, memory, disk, and I/O bottlenecks.
- Apply a structured troubleshooting methodology to cross-platform
  incidents rather than ad hoc investigation.
- Centralize logs from both platforms into a common pipeline, extending
  the `journald` forwarding introduced in Chapter 02 with Windows Event
  Forwarding.
- Operate a host through the full lifecycle model introduced in Volume I
  — build, patch, monitor, and decommission — as a closed loop rather than
  a series of disconnected tasks.

## Theory and Architecture

This closing chapter ties the volume together operationally: how
administrators know a host is healthy, how they diagnose it when it is
not, how logs and metrics leave the host to reach a central pipeline, and
how a host's operational life ends in a controlled way rather than as an
afterthought. Full observability platform architecture — metrics
pipelines, distributed tracing, dashboarding, and alerting design at
scale — is covered in Volume XI; this chapter stays at what a single host
produces and how an administrator reasons about it directly.

### The monitoring stack, from a single host's perspective

Enterprise observability is commonly described in three data types:
**metrics** (numeric time-series — CPU percent, queue depth), **logs**
(discrete structured or unstructured event records), and **traces**
(request-level causal chains through distributed systems, most relevant
to application-layer observability and covered in Volume XI). A host
participates in this stack either through an **agent** that pushes or
exposes data, or **agentlessly**, where a central collector pulls data
over an existing protocol (SSH, WinRM, SNMP). This chapter's examples use
agentless, platform-native tools first, since understanding what the host
itself can report is the foundation for evaluating any agent or platform
built on top of it.

### Platform-native performance tooling

| Purpose | Linux | Windows |
| --- | --- | --- |
| CPU utilization over time | `sar -u` (requires `sysstat`) | `Get-Counter '\Processor(_Total)\% Processor Time'` |
| Memory pressure | `sar -r`, `vmstat` | `Get-Counter '\Memory\Available MBytes'` |
| Disk I/O | `iostat -xz` | `Get-Counter '\PhysicalDisk(_Total)\Avg. Disk Queue Length'` |
| Per-process resource use over time | `pidstat` | Resource Monitor, Performance Monitor with a process-scoped counter set |
| Interactive live view | `top`/`htop` | Task Manager, Performance Monitor live graph |

The `sysstat` package (Linux) runs a `systemd` timer (`sysstat-
collect.timer`) that samples system activity every 10 minutes by default
and retains it, which is what makes `sar` useful for **retrospective**
analysis — diagnosing a spike that happened overnight — not only live
monitoring.

### A structured troubleshooting methodology

Ad hoc troubleshooting — changing things until the symptom goes away —
produces incidents that recur because the actual cause was never
identified. This chapter recommends a repeatable sequence:

1. **Define the problem and scope.** What is the observed symptom,
   which hosts/services are affected, and since when?
2. **Gather evidence before forming a hypothesis.** Pull metrics, logs,
   and recent change history (tying back to Chapter 01's change-management
   process) for the affected window.
3. **Form a specific, testable hypothesis.** "Disk I/O saturation on the
   database volume," not "something is slow."
4. **Test narrowly.** Confirm or reject the hypothesis with a targeted
   diagnostic before changing production configuration.
5. **Implement the fix, then verify it resolved the original symptom** —
   not just that the diagnostic metric improved.
6. **Document the finding** as a runbook update or a problem record
   (Chapter 01), so the next occurrence is faster to resolve.

A useful lens for step 3, borrowed from performance engineering, is the
**USE method** (Utilization, Saturation, Errors): for every resource —
CPU, memory, disk, network — check how busy it is, how much work is
queued waiting for it, and whether it is throwing errors, rather than
guessing which resource is the bottleneck.

### Log centralization

- **Linux**: Chapter 02 showed `journald` forwarding to syslog
  (`ForwardToSyslog=yes`). At fleet scale, hosts typically forward to a
  local `rsyslog`/`syslog-ng` relay, which batches and ships to the
  central collector, rather than every host connecting directly to a
  central system.
- **Windows**: **Windows Event Forwarding (WEF)** lets a designated
  collector pull (or sources push, depending on subscription type) event
  log data over WinRM, without installing a third-party agent. A
  **subscription**, created on the collector with `wecutil`, defines which
  event log/query to forward and from which source computers.
- Both mechanisms feed the same downstream pipeline in a mature
  environment (Volume XI); the choice of agentless-native forwarding
  versus a shipping agent (Beats, Fluent Bit, and similar) is itself an
  architectural decision made at the observability-platform layer, not
  in this chapter.

### Lifecycle operations

Volume I, Chapter 08 defined the infrastructure lifecycle: plan, build,
operate, maintain, and decommission. Applied to a single host in this
volume's scope:

```text
  Build          Patch           Monitor            Decommission
(Chapter 06) -> (Chapter 06) -> (this chapter) -> (this chapter +
 golden image     ring rollout    health checks,     Volume I Ch08
 provisioning                     alerting,           NIST 800-88)
                                   incident/problem
                                   feedback (Ch01)
```

A host is never "done" until it is decommissioned; monitoring is the
stage that occupies most of a host's operational life and is what
produces the evidence that a change (Chapter 06/08) succeeded or a
problem (Chapter 01) needs escalation.

## Design Considerations

- **Alert on symptoms, not just raw thresholds.** An alert tied to SLO
  burn rate (Volume I's availability vocabulary) is more actionable than
  a static "CPU > 80%" threshold that fires during entirely expected
  batch-processing windows.
- **Design retention deliberately.** Balance log/metric retention cost
  against investigative and compliance need (Chapter 08's audit evidence
  requirements are a lower bound, not a target); keep high-resolution data
  for a shorter window and downsampled/aggregated data longer.
- **Design for alert fatigue explicitly.** Every alert that does not
  require action erodes trust in the alerting system; tune thresholds from
  USE-method evidence, not guesses, and remove or fix alerts that
  consistently fire without a corresponding action.
- **Runbooks over tribal knowledge.** A troubleshooting runbook committed
  to the same documentation pipeline as the rest of this encyclopedia
  (Volume I, Chapter 05) survives staff turnover; an experienced
  administrator's memory does not.
- **Decommission checklists must be complete, not just "delete the VM."**
  A rushed decommission leaves orphaned DNS records, stale AD computer
  objects (Chapter 04), monitoring targets alerting on an unreachable
  host, and CMDB entries that no longer reflect reality — each an
  operational and audit liability.
- **Edge/disconnected sites need a monitoring design decision, not a
  default.** A site with unreliable connectivity to the central collector
  needs local buffering or local-only alerting as an explicit design
  choice, not a silent gap discovered during an outage.

## Implementation and Automation

### Retrospective performance analysis on Linux

```bash
sudo dnf install -y sysstat   # Debian/Ubuntu: sudo apt install sysstat
sudo systemctl enable --now sysstat-collect.timer

# CPU utilization for today so far, sampled every 10 minutes by the
# sysstat-collect.timer.
sar -u

# Live, ad hoc sampling for an active investigation: 5 samples, 1 second
# apart, for CPU, memory, and disk I/O.
sar -u 1 5
vmstat 1 5
iostat -xz 1 5

# Per-process CPU and I/O over the same window.
pidstat 1 5
pidstat -d 1 5
```

### Retrospective and live performance analysis on Windows

```powershell
# Live sampling: CPU and available memory, 5 samples 2 seconds apart.
Get-Counter -Counter '\Processor(_Total)\% Processor Time', `
    '\Memory\Available MBytes' -SampleInterval 2 -MaxSamples 5

# Export a longer capture to CSV for offline/retrospective analysis,
# the Windows analog to sysstat's historical sar data.
Get-Counter -Counter '\PhysicalDisk(_Total)\Avg. Disk Queue Length' `
    -SampleInterval 5 -MaxSamples 60 |
    Export-Counter -Path C:\perf\disk-queue.csv -FileFormat CSV
```

### Simple health-check job

```bash
# /usr/local/bin/disk-healthcheck.sh — logs at "crit" facility/priority
# once a threshold is exceeded, so downstream forwarding rules (below)
# can filter on severity rather than parsing free-text output.
#!/bin/bash
threshold=90
usage=$(df -h /data | awk 'NR==2 {gsub("%","",$5); print $5}')

if [ "$usage" -ge "$threshold" ]; then
    logger -p local0.crit "disk-healthcheck: /data at ${usage}% (threshold ${threshold}%)"
else
    logger -p local0.info "disk-healthcheck: /data at ${usage}% (OK)"
fi
```

```ini
# /etc/systemd/system/disk-healthcheck.timer — run every 5 minutes.
[Unit]
Description=Run disk health check every 5 minutes

[Timer]
OnCalendar=*:0/5
Persistent=true

[Install]
WantedBy=timers.target
```

### Forwarding critical events with rsyslog

```bash
# /etc/rsyslog.d/60-forward-critical.conf — forward only local0.crit and
# above to a central (or, in this lab, local) collector over UDP,
# keeping routine informational health-check entries local.
sudo tee /etc/rsyslog.d/60-forward-critical.conf <<'EOF'
local0.crit    action(type="omfwd" target="127.0.0.1" port="2514" protocol="udp")
EOF
sudo systemctl restart rsyslog
```

### Windows Event Forwarding setup

```powershell
# On the collector host: enable the forwarding service and create a
# subscription pulling Security-log logon failures from named sources.
wecutil qc /q

$subscriptionXml = @'
<Subscription xmlns="http://schemas.microsoft.com/2006/03/windows/events/subscription">
  <SubscriptionId>SecurityLogonFailures</SubscriptionId>
  <SubscriptionType>SourceInitiated</SubscriptionType>
  <Query><![CDATA[<QueryList><Query Id="0"><Select Path="Security">*[System[(EventID=4625)]]</Select></Query></QueryList>]]></Query>
  <ReadExistingEvents>false</ReadExistingEvents>
  <AllowedSourceNonDomainComputers></AllowedSourceNonDomainComputers>
  <AllowedSourceDomainComputers>O:NSG:BAD:P(A;;GA;;;DC)S:</AllowedSourceDomainComputers>
</Subscription>
'@
$subscriptionXml | Out-File C:\WEF\subscription.xml -Encoding utf8
wecutil cs C:\WEF\subscription.xml

# On each source host: enable WinRM and point it at the collector via
# Group Policy ("Configure target Subscription Manager"), then confirm.
winrm quickconfig -q
wecutil gr SecurityLogonFailures
```

### Decommissioning a host

```powershell
# Reverse the identity integration from Chapter 04, then remove
# monitoring and CMDB references — a decommission runbook should chain
# all of these, not stop after the VM is powered off.
Get-ADComputer -Filter "Name -eq 'web-lnx-04'" | Remove-ADObject -Recursive -Confirm:$true
Remove-DnsServerResourceRecord -ZoneName 'example.internal' `
    -Name 'web-lnx-04' -RRType A -Force

# Deregister from a monitoring platform's API (illustrative — adapt to
# the actual platform in use) and close the CMDB configuration item.
Invoke-RestMethod -Method Delete -Uri 'https://monitoring.example.internal/api/targets/web-lnx-04'
Invoke-RestMethod -Method Patch -Uri 'https://cmdb.example.internal/api/ci/web-lnx-04' `
    -Body (@{ status = 'decommissioned' } | ConvertTo-Json) -ContentType 'application/json'
```

## Validation and Troubleshooting

- Confirm `sysstat` is actually collecting history, not just installed:
  `sar -u` with no time range should show multiple entries spanning the
  day, not a single sample.
- Confirm a health-check job fires only at the intended threshold:
  temporarily lower the threshold in a non-production copy of the script
  and confirm the `crit` log line appears; restore the threshold
  afterward.
- Confirm log forwarding actually reaches the collector, not just that
  the forwarding rule is syntactically present: generate a test event and
  watch for it on the receiving side rather than trusting the
  configuration alone.
- Confirm WEF subscription health: `wecutil gr <SubscriptionId>` on the
  collector should show `SubscriptionRuntimeStatusActive`, and the
  collector's Forwarded Events log should contain recent entries from
  each source.
- Confirm decommission completeness: search the CMDB, DNS, and monitoring
  platform for the retired hostname after the runbook completes; any
  remaining reference is an incomplete decommission.

| Symptom | Likely cause | Diagnostic step |
| --- | --- | --- |
| High load average but low per-core CPU utilization | Processes blocked on I/O wait, not CPU-bound | `vmstat 1` — check the `b` (blocked) column and `wa` (I/O wait) percentage; confirm with `iostat -xz 1` |
| `sar` reports no historical data for a known incident window | `sysstat-collect.timer` was not enabled at the time, or its data file rotated out | `systemctl status sysstat-collect.timer`; check `/var/log/sa/` retention configuration |
| Forwarded log messages never arrive at the collector | Firewall blocking the forwarding port, or the rsyslog rule scoped to the wrong facility/severity | Test connectivity to the port directly (`nc -zv` or equivalent); confirm the rule's facility/severity filter matches what `logger` actually emitted |
| WEF subscription shows sources but no events arrive | WinRM not reachable from collector to source, or the subscription's XPath query does not match any events on the source | `Test-WSMan` from collector to source; validate the query against the source's own Event Viewer filter first |
| Decommissioned host reappears in monitoring alerts | Monitoring target removal step in the runbook was skipped or failed silently | Re-run the deregistration API call; add a post-decommission verification step to the runbook itself |

## Security and Best Practices

- Use least-privilege, dedicated service accounts for monitoring
  collection and WEF, distinct from interactive administrator accounts
  (consistent with the identity separation guidance in Chapter 01/04).
- Forward security-relevant logs (audit trails from Chapter 08, failed
  logons) before local retention expires, so a compromised host cannot
  destroy the only copy of its own evidence.
- Encrypt log transport where it crosses an untrusted network segment —
  WinRM over HTTPS for WEF, TLS-wrapped syslog (`omfwd` with
  `protocol="tcp"` plus a TLS driver) rather than plaintext UDP, in
  production.
- Sanitize storage media per NIST SP 800-88 (Volume I, Chapter 08) as part
  of decommissioning, and revoke any certificates or credentials issued
  to the retired host rather than leaving them valid and unmonitored.
- Tune alert thresholds from measured evidence (the USE method) rather
  than intuition, and retire alerts that never lead to action — alert
  fatigue is itself a security risk, since it trains responders to
  dismiss notifications.
- Treat a completed decommission as requiring positive verification
  (absence confirmed in DNS, AD, monitoring, and CMDB), not merely the
  absence of an error from the removal script.

## References and Knowledge Checks

**References**

- Brendan Gregg, "Systems Performance" — the USE method and Linux
  performance tooling.
- `sar(1)`, `sysstat` package documentation, `pidstat(1)` man pages.
- Microsoft Learn: "Windows Event Forwarding" and "Get-Counter."
- Microsoft Learn: "Monitor and troubleshoot with Performance Monitor."
- NIST SP 800-88 — media sanitization guidance referenced in Volume I,
  Chapter 08.

**Knowledge Checks**

1. What does the USE method check for each resource, and why is it more
   structured than "check if CPU is high"?
2. Why does `sysstat`/`sar` matter for diagnosing an incident that
   already happened, compared to a live-only tool like `top`?
3. What is the practical difference between a source-initiated and a
   collector-initiated Windows Event Forwarding subscription?
4. Name three systems (besides the VM/host itself) that a complete
   decommission runbook must update, and what happens if each is
   skipped.
5. Why is alerting on SLO burn rate generally preferable to a static
   utilization threshold?

## Hands-On Lab

**Objective:** Build a disk-usage health-check job that logs at a
distinguishable severity, forward only that severity to a mock collector
using `rsyslog`, and prove both the positive (alert fires and is
forwarded) and negative (no alert when the threshold is not met) cases —
demonstrating the log-centralization pattern from this chapter on a
single Linux VM.

### Prerequisites

- One Linux VM (RHEL-family or Debian-family, 2 vCPU / 2 GB RAM) with
  `rsyslog` installed and running (default on most enterprise Linux
  installs) and `sudo` access.
- `nc` (netcat) available for the mock collector
  (`sudo dnf install -y nmap-ncat` or `sudo apt install -y netcat-
  openbsd`).

### Procedure

1. Start a mock collector listening on UDP 2514 in a dedicated terminal
   session (leave this running for the rest of the lab):

   ```bash
   nc -ul 2514
   ```

2. In a second session, configure `rsyslog` to forward `local0.crit`
   messages to the mock collector:

   ```bash
   sudo tee /etc/rsyslog.d/60-forward-critical.conf <<'EOF'
   local0.crit    action(type="omfwd" target="127.0.0.1" port="2514" protocol="udp")
   EOF
   sudo systemctl restart rsyslog
   ```

3. Send a manual test message and confirm it reaches the mock collector:

   ```bash
   logger -p local0.crit "lab test: manual critical message"
   ```

   **Expected result:** the message appears in the `nc` terminal from
   step 1 within a few seconds, confirming the forwarding rule works.

4. Create the health-check script with an intentionally low threshold so
   it is guaranteed to trigger, and a timer to run it:

   ```bash
   sudo tee /usr/local/bin/disk-healthcheck.sh <<'EOF'
   #!/bin/bash
   threshold=1
   usage=$(df -h / | awk 'NR==2 {gsub("%","",$5); print $5}')
   if [ "$usage" -ge "$threshold" ]; then
       logger -p local0.crit "disk-healthcheck: / at ${usage}% (threshold ${threshold}%)"
   else
       logger -p local0.info "disk-healthcheck: / at ${usage}% (OK)"
   fi
   EOF
   sudo chmod +x /usr/local/bin/disk-healthcheck.sh

   sudo tee /etc/systemd/system/disk-healthcheck.service <<'EOF'
   [Unit]
   Description=Disk health check

   [Service]
   Type=oneshot
   ExecStart=/usr/local/bin/disk-healthcheck.sh
   EOF

   sudo systemctl start disk-healthcheck.service
   ```

   **Expected result:** because the threshold (1%) is guaranteed to be
   exceeded by real disk usage, a `disk-healthcheck: / at NN% (threshold
   1%)` message appears in the `nc` terminal within a few seconds.

### Negative Test

Raise the threshold to a value real usage cannot plausibly reach, re-run
the check, and confirm no alert is forwarded — proving the forwarding
rule fires on the `crit` severity specifically, not on every invocation
of the script:

```bash
sudo sed -i 's/threshold=1/threshold=99/' /usr/local/bin/disk-healthcheck.sh
sudo systemctl start disk-healthcheck.service
sudo tail -n1 /var/log/messages 2>/dev/null || journalctl -t logger -n1
```

**Expected result:** the `nc` terminal receives no new message (the
script now logs at `local0.info`, which the forwarding rule does not
match), while the local log (via `journalctl` or `/var/log/messages`)
still shows the informational "(OK)" entry — confirming severity-based
filtering, not the absence of any logging at all.

### Cleanup

```bash
# Stop the mock collector with Ctrl+C in its terminal, then:
sudo rm -f /etc/rsyslog.d/60-forward-critical.conf
sudo systemctl restart rsyslog
sudo rm -f /etc/systemd/system/disk-healthcheck.service /usr/local/bin/disk-healthcheck.sh
sudo systemctl daemon-reload
```

## Summary and Completion Checklist

This closing chapter connected the volume's earlier automation and
configuration coverage to day-to-day operational reality: platform-native
performance tools that answer "what is actually happening on this host
right now, and what happened during the incident window," a structured
(USE-method-informed) troubleshooting methodology instead of ad hoc
guessing, log centralization patterns — `journald`/`rsyslog` forwarding
and Windows Event Forwarding — that feed the Volume XI observability
stack, and a complete decommission runbook that closes the lifecycle loop
Volume I opened.

- [ ] Can use at least two Linux and two Windows tools to diagnose CPU,
      memory, and disk contention, including retrospective analysis.
- [ ] Can apply a structured troubleshooting methodology (define, gather
      evidence, hypothesize, test narrowly, fix, verify, document) to a
      cross-platform incident.
- [ ] Can configure severity-based log forwarding on Linux and describe
      the Windows Event Forwarding subscription model.
- [ ] Can list every system a complete host decommission must update
      beyond simply deleting the VM.
- [ ] Completed the hands-on lab, including the negative test proving
      forwarding is filtered by severity rather than firing on every
      health-check run.
