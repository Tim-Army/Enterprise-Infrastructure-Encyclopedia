# Chapter 06: NCP-US — Unified Storage

## Learning Objectives

- Explain what the NCP-US certifies and its target role.
- Summarize the four blueprint sections.
- Deploy, upgrade, configure, and utilize Nutanix Unified Storage.
- Analyze, monitor, and troubleshoot Files, Objects, and Volumes.
- Complete a per-section walkthrough for each NCP-US domain.

## Theory and Architecture

The **Nutanix Certified Professional — Unified Storage (NCP-US)** validates managing
**Nutanix Unified Storage (NUS)** — the storage credential (**75 questions / 120
minutes**). Its blueprint has **four sections**: **Deploy and Upgrade**, **Configure
and Utilize**, **Analyze and Monitor**, and **Troubleshoot** Nutanix Unified Storage.
NUS spans **Files** (SMB/NFS), **Objects** (S3-compatible), and **Volumes** (iSCSI
block).

## Design Considerations

The storage admin deploys **Files/Objects/Volumes**, upgrades via **LCM**, configures
shares/buckets/volume-groups with quotas and protocols, uses **Data Lens** for
analytics/ransomware detection, monitors capacity/performance, and troubleshoots. Match
the service to the workload: Files for user shares, Objects for S3 apps, Volumes for
bare-metal/iSCSI.

## Implementation and Automation

The labs use NUS (Files/Objects/Volumes) and `ncli`/API for each section — deploy/
upgrade, configure/utilize, analyze/monitor, and troubleshoot.

## Validation and Troubleshooting

Confirm the blueprint before studying:

```text
nutanix.com > NCP-US blueprint (75 Q / 120 min):
  1 Deploy and Upgrade Nutanix Unified Storage
  2 Configure and Utilize Nutanix Unified Storage
  3 Analyze and Monitor Nutanix Unified Storage
  4 Troubleshoot Nutanix Unified Storage
```

Common pitfalls: using Files where **Objects** (S3) fits; and no **quotas** leading to
runaway share growth.

## Security and Best Practices

Pick the right service (**Files/Objects/Volumes**), size the file server VMs (FSVMs),
set **quotas** and protocol permissions, use **Data Lens** for capacity + ransomware
detection, and monitor/troubleshoot with NUS analytics. Enable WORM/immutability for
Objects where required.

## References and Knowledge Checks

- nutanix.com: NCP-US blueprint guide; Nutanix Files, Objects, Volumes, and Data Lens docs.

**Knowledge checks**

1. When do you choose Objects over Files?
2. What does Data Lens add over basic monitoring?
3. What are FSVMs?

## Hands-On Lab

Per-section walkthroughs — NCP-US. **Shared prerequisites** — a cluster with Files/
Objects/Volumes (or the API). **Cost:** none beyond a lab cluster.

### Lab 6.1 — Deploy and upgrade

**Objective:** List the file server and check upgrade status.

```bash
ncli file-server list
# Upgrades for Files/Objects/Volumes are driven through LCM (Life Cycle Manager).
```

**Expected result:** the deployed **file server(s)** (and the LCM upgrade path) — the
deploy/upgrade section.

**Negative test:** upgrade FSVMs manually; **LCM** coordinates the rolling upgrade —
use it.

**Rollback:** none (read-only).

### Lab 6.2 — Configure and utilize (a share with a quota)

**Objective:** Create an SMB share with a quota.

```bash
ncli file-server list-shares
# Create a share (Prism/API): protocol=SMB, path=/projects, quota=500G
"share 'projects' SMB, quota 500G created"
```

**Expected result:** an SMB share with a **quota** — the configure/utilize section.

**Negative test:** create shares with no quota; **quotas** prevent one team from
consuming the file server.

**Rollback:** delete the share if it was for the lab.

### Lab 6.3 — Analyze and monitor (Data Lens)

**Objective:** Review storage analytics.

```bash
# Data Lens: capacity trends, file-type/age breakdown, anomaly/ransomware signals.
ncli file-server list | grep -Ei 'Name|Usage'
```

**Expected result:** file-server usage and the **Data Lens** analytics view — the
analyze/monitor section.

**Negative test:** track capacity in a spreadsheet; **Data Lens** trends and flags
anomalies automatically.

**Rollback:** none (read-only).

### Lab 6.4 — Troubleshoot

**Objective:** Diagnose a share access issue.

```bash
# Check FSVM health, protocol/DNS/AD join, and permissions:
ncli file-server list | grep -Ei 'Status'
# afs (Files CLI on FSVM): afs smb.health_check ; afs ad.check_domain
```

**Expected result:** FSVM/AD/protocol health to pinpoint the fault — the troubleshoot
section.

**Negative test:** blame the network first; check **FSVM health + AD join + share
permissions** systematically.

**Rollback:** none (read-only).

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The NCP-US certifies managing Nutanix Unified Storage across four sections: deploy/
upgrade, configure/utilize (Files/Objects/Volumes with quotas), analyze/monitor (Data
Lens), and troubleshoot — via Prism, `ncli`, and the Files CLI.

- [ ] I can deploy and upgrade NUS via LCM.
- [ ] I can configure shares/buckets/volumes with quotas.
- [ ] I can analyze and monitor with Data Lens.
- [ ] I can troubleshoot FSVM/AD/protocol issues.
- [ ] I completed Labs 6.1–6.4 including each negative test.
