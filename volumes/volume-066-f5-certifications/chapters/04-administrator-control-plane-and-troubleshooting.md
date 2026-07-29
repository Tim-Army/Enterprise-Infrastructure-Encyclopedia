# Chapter 04: Administrator — Control Plane and Troubleshooting

## Learning Objectives

- Administer the BIG-IP control plane (F5CAB4): users, HA, config sync, backups.
- Build a high-availability device group with failover.
- Support and troubleshoot the platform (F5CAB5): logs, qkview, iHealth.
- Back up and restore configuration with UCS archives.
- Complete a walkthrough for each control-plane and support topic.

## Theory and Architecture

The **F5CAB4** (Control Plane Administration) and **F5CAB5** (Support and Troubleshooting) exams
cover keeping BIG-IP running. The control plane includes **user accounts and roles** (RBAC,
partitions for administrative separation), **high availability** — a **device group** of two or
more BIG-IPs with **config sync** (so configuration is consistent), **failover** (traffic groups
move to a healthy device), and connection/persistence mirroring — and **backups** via **UCS**
(User Configuration Set) archives. Troubleshooting relies on the **logs** (`/var/log/ltm`, tmsh
`show sys log`), the **qkview** diagnostic snapshot uploaded to **iHealth** (F5's automated
analysis), packet capture (`tcpdump` on TMM interfaces), and the layered health view (virtual →
pool → member → monitor). The administrator keeps the platform available and diagnosable.

## Design Considerations

Deploy BIG-IPs in an **HA device group** so a failure is transparent, with **config sync** to keep
them consistent. Take **UCS backups** before every change and upgrade. Use **RBAC and partitions**
to separate duties. Troubleshoot top-down: is the virtual server up? the pool? the member? the
monitor?

## Implementation and Automation

The labs configure HA/config sync, take a UCS backup, read logs, and generate a qkview.

## Validation and Troubleshooting

Confirm the control-plane model:

```text
Control plane: users/RBAC/partitions; HA device group (config sync + failover + mirroring); UCS backups.
Troubleshoot: logs (show sys log / /var/log/ltm); qkview -> iHealth; tcpdump; top-down health (vs->pool->member->monitor).
Exams: F5CAB4 (control plane admin), F5CAB5 (support & troubleshooting).
```

Common pitfalls: a standalone BIG-IP for a critical service (**no HA**); and changing config with
**no UCS backup**.

## Security and Best Practices

Run **HA** with config sync, **back up (UCS)** before changes, and use **RBAC/partitions** for
least privilege. Restrict management access and audit admin actions. Diagnose with **qkview/iHealth**
rather than ad-hoc guesses. Defensive operations throughout.

## Hands-On Lab

Control-plane walkthroughs. **Shared prerequisites** — two BIG-IP VEs (for HA) in an authorized
lab. **Cost:** none.

### Lab 4.1 — Configure an HA device group

**Objective:** Pair two BIG-IPs for failover.

```bash
tmsh modify cm device <self> configsync-ip 10.10.10.1
tmsh create cm device-group dg1 type sync-failover devices add { bigip-1 bigip-2 }
tmsh run cm config-sync to-group dg1
tmsh show cm sync-status
```

**Expected result:** a **sync-failover** device group with config sync — HA across the pair.

**Negative test:** run a lone BIG-IP for a critical service; a failure is an **outage** — deploy
an HA device group.

**Cleanup:** `tmsh delete cm device-group dg1` (in a lab).

### Lab 4.2 — Back up the configuration (UCS)

**Objective:** Create a restorable archive.

```bash
tmsh save sys ucs /var/local/ucs/pre-change.ucs
tmsh list sys ucs
```

**Expected result:** a **UCS archive** capturing the full configuration — a restore point before
changes.

**Negative test:** make changes with no backup; a bad change is then hard to undo — **UCS backup**
first.

**Cleanup:** none (keep the backup).

### Lab 4.3 — Read logs top-down

**Objective:** Investigate a service issue via logs and health.

```bash
tmsh show sys log ltm | tail -n 20
tmsh show ltm virtual web_vs
tmsh show ltm pool web_pool members
```

**Expected result:** the LTM log plus the **virtual → pool → member** health — a top-down
diagnosis path.

**Negative test:** restart services blindly; troubleshoot **top-down** (virtual/pool/member/
monitor) using logs first.

**Cleanup:** none (read-only).

### Lab 4.4 — Generate a qkview for iHealth

**Objective:** Capture a diagnostic snapshot.

```bash
qkview -f /var/tmp/support.qkview
# Upload the qkview to F5 iHealth (ihealth.f5.com) for automated analysis and known-issue matching.
echo "qkview created -> upload to iHealth for analysis"
```

**Expected result:** a **qkview** diagnostic bundle for **iHealth** — F5's automated
troubleshooting.

**Negative test:** open a support case with no qkview; **iHealth/qkview** speeds diagnosis —
generate it.

**Cleanup:** `rm -f /var/tmp/support.qkview` (in a lab).

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The F5CAB4/F5CAB5 exams cover the control plane — RBAC/partitions, HA device groups with config
sync and failover, and UCS backups — and troubleshooting with logs, top-down health, and
qkview/iHealth. Run HA, back up before changes, and diagnose systematically.

- [ ] I can configure an HA device group with config sync.
- [ ] I can take a UCS backup.
- [ ] I can troubleshoot top-down with logs and health.
- [ ] I can generate a qkview for iHealth.
- [ ] I completed Labs 4.1–4.4 including each negative test.
