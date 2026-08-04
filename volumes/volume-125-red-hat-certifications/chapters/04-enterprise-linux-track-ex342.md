# Chapter 04: The Enterprise Linux Track — Advanced Administration (EX342)

## Learning Objectives

- Map the Enterprise Linux track: RHCSA → EX342 (Engineer) → Specialist electives → RHCA.
- Cover the advanced-administration topics EX342 tests.
- Drill each as a performance task.

## The track

The **Enterprise Linux** track builds on RHCSA:

| Level | Credential | Exam |
|:---|:---|:---|
| L2 | RHCSA | EX200 |
| L3 (Engineer) | Red Hat Certified Advanced System Administrator | **EX342** |
| L4 | Specialist electives (security/hardening EX415, identity EX362, performance, storage EX436, etc.) | various |
| L5 | RHCA in Enterprise Linux | EX342 + three same-track Specialists |

EX342 (Red Hat Certified Specialist in Advanced Automation-adjacent system administration) goes past RHCSA into troubleshooting, logging/auditing, advanced storage, and automation of administration tasks — performance-based, on RHEL.

## Hands-On Lab

A RHEL-family VM. **Cost:** none.

### Lab 4.1 — Advanced troubleshooting: boot and rescue

**Objective (task):** "Diagnose a service that fails to start, using journald and systemd analysis."

```bash
sudo systemctl start nonexistent.service 2>&1 | tail -1
sudo journalctl -u chronyd --since "-10 min" -p err --no-pager | tail -3
systemd-analyze blame 2>/dev/null | head -5
systemd-analyze critical-chain 2>/dev/null | head -8
```

**Expected result:** The failed-unit message, filtered journal errors, and boot-time attribution — EX342 troubleshooting is `journalctl` fluency (`-u`, `-p`, `--since`), `systemd-analyze blame`/`critical-chain`, and reading failed units. Diagnosis speed is the skill.

**Negative test:** `journalctl` with no unit/priority filter on a busy system — thousands of lines; the exam rewards filtering to the failing unit and severity.

**Cleanup:** None.

### Lab 4.2 — Logging and auditing

**Objective (task):** "Configure persistent journald storage and add an audit rule for a sensitive file."

```bash
sudo mkdir -p /var/log/journal && sudo systemctl restart systemd-journald
journalctl --disk-usage
sudo auditctl -w /etc/shadow -p wa -k shadow-watch 2>/dev/null && sudo auditctl -l | grep shadow-watch
sudo ausearch -k shadow-watch 2>/dev/null | tail -2 || echo "no events yet (expected)"
```

**Expected result:** Persistent journal storage confirmed by `--disk-usage`, and an audit watch on `/etc/shadow` listed by `auditctl -l` — persistent logging (journald `Storage=persistent`), rsyslog routing, and the audit subsystem (`auditctl`, `ausearch`, `aureport`) are EX342 topics.

**Negative test:** Add an audit watch with `auditctl` only (runtime) and expect it after reboot — it's lost; persistent rules go in `/etc/audit/rules.d/`, the distinction the exam tests.

**Cleanup:** `sudo auditctl -W /etc/shadow -p wa -k shadow-watch 2>/dev/null`.

### Lab 4.3 — Advanced storage: Stratis and VDO

**Objective (task):** "Create a Stratis pool and filesystem (thin, snapshottable)."

```bash
sudo dnf install -y stratisd stratis-cli >/dev/null && sudo systemctl enable --now stratisd
dd if=/dev/zero of=/root/stratis.img bs=1M count=1024 status=none
LOOP=$(sudo losetup -f --show /root/stratis.img)
sudo stratis pool create labpool $LOOP && sudo stratis filesystem create labpool labfs
sudo stratis filesystem list
```

**Expected result:** A Stratis pool and filesystem created (thin-provisioned, snapshot-capable) — advanced local storage (Stratis, VDO deduplication/compression concepts) beyond RHCSA's LVM is EX342 material.

**Negative test:** Format a Stratis-managed device with `mkfs` directly — you bypass and corrupt the pool; Stratis manages the filesystem lifecycle, unlike raw LVM+mkfs.

**Cleanup:** `sudo stratis filesystem destroy labpool labfs; sudo stratis pool destroy labpool; sudo losetup -d $LOOP; rm -f /root/stratis.img`.

### Lab 4.4 — Automating administration with scripts + systemd

**Objective (task):** "Write a maintenance script and schedule it as a systemd timer (not cron)."

```bash
sudo tee /usr/local/bin/diskreport.sh >/dev/null <<'EOF'
#!/bin/bash
df -h --output=source,pcent,target | awk 'NR==1 || $2+0 > 80'
EOF
sudo chmod +x /usr/local/bin/diskreport.sh
sudo tee /etc/systemd/system/diskreport.service >/dev/null <<'EOF'
[Unit]
Description=Disk report
[Service]
Type=oneshot
ExecStart=/usr/local/bin/diskreport.sh
EOF
sudo tee /etc/systemd/system/diskreport.timer >/dev/null <<'EOF'
[Unit]
Description=Hourly disk report
[Timer]
OnCalendar=hourly
Persistent=true
[Install]
WantedBy=timers.target
EOF
sudo systemctl daemon-reload && sudo systemctl enable --now diskreport.timer
systemctl list-timers diskreport.timer --no-pager | head -3
```

**Expected result:** The timer active and scheduled hourly — EX342 favors **systemd timers** (with `OnCalendar` and `Persistent=true` for missed runs) over cron for scheduled administration; the service+timer unit pair is the pattern.

**Negative test:** Enable the `.service` instead of the `.timer` — a oneshot service runs once and stops; the **timer** is what schedules it, a distinction the exam draws.

**Cleanup:** `sudo systemctl disable --now diskreport.timer; sudo rm /etc/systemd/system/diskreport.{service,timer} /usr/local/bin/diskreport.sh; sudo systemctl daemon-reload`.

### Lab 4.5 — Toward RHCA: the Specialist electives

**Objective:** Understand how the Enterprise Linux RHCA is assembled.

```text
RHCA (Enterprise Linux) = RHCSA/L2 + EX342/L3 + THREE Specialist electives in-track, e.g.:
  EX415 Security: Securing RHEL   |   EX362 Identity Management   |   EX436 High Availability Clustering
  (choose three within the track — post-2026 rules forbid cross-track mixing)
```

**Expected result:** The track-specific RHCA formula — an Administrator exam, an Engineer exam, and **three same-track Specialists** — the 2026 rule that replaced "any five specialists." [Chapter 09](09-choosing-currency-and-career.md) plans the elective choice.

**Negative test:** Mixing an OpenShift Specialist into an Enterprise Linux RHCA — no longer allowed; electives must share the track.

**Cleanup:** None (design).

## Summary and Completion Checklist

- [ ] EX342 advanced topics (troubleshooting, audit, Stratis, systemd-timer automation) drilled.
- [ ] Persistent-vs-runtime distinctions (audit rules, journal storage) internalized.
- [ ] The track-specific RHCA (Enterprise Linux) formula understood.
