# Chapter 02: The Veeam Data Platform

## Learning Objectives

- Describe the Veeam Data Platform architecture (backup server, proxies, repositories).
- Distinguish the Veeam Data Platform editions.
- Add and inspect a backup repository.
- Add and inspect a backup proxy.
- Complete a walkthrough for each platform-architecture topic.

## Theory and Architecture

The **Veeam Data Platform** is built around **Veeam Backup & Replication (VBR) v13**, plus **Veeam ONE**
(monitoring), **Veeam Recovery Orchestrator** (DR automation), and **Veeam Data Cloud** (SaaS/cloud
protection). VBR's architecture separates roles: the **backup server** is the management brain (the
configuration database, job scheduler, and console); **backup proxies** do the data-mover work
(reading source data, deduplicating, compressing, and encrypting on the way to storage); and **backup
repositories** are the storage targets (a Windows/Linux server, a **hardened Linux repository**, a
deduplicating appliance, or **object storage**). The platform ships in **editions** — **Community**
(free), **Foundation**, **Advanced**, and **Premium** (the full Data Platform with security and
orchestration) — that gate features. Understanding which role does what, and which edition unlocks a
capability, is the foundation VMCE+ builds on. This chapter teaches the architecture with hands-on Veeam
PowerShell walkthroughs.

## Design Considerations

Place **proxies** close to the source data (per site/cluster) to move data efficiently, and size them
for concurrent tasks. Choose **repositories** for the recovery need — a **hardened Linux repository**
or **object storage with immutability** for ransomware resilience (Chapter 08), fast storage for
frequent restores. Match the **edition** to the requirement — **Premium** for orchestration and the full
security feature set. Keep the backup server and its configuration database protected and backed up.

## Implementation and Automation

The labs read the platform version and edition, add a backup repository, and add a proxy — the roles
VMCE+ expects you to design and operate.

## Validation and Troubleshooting

Confirm the architecture:

```text
Backup server = brain (config DB + scheduler + console)
Backup proxy  = data mover (read/dedup/compress/encrypt)
Repository    = storage target (Windows/Linux/hardened/dedup appliance/object)
Editions: Community (free) < Foundation < Advanced < Premium (full Data Platform)
Platform: VBR v13 + Veeam ONE + Recovery Orchestrator + Data Cloud
```

Common pitfalls: undersizing **proxies** so backup windows overrun; and expecting a **Community**-edition
server to unlock Premium features like orchestration.

## Security and Best Practices

Prefer a **hardened Linux repository** or **immutable object storage** as a recovery target, protect the
backup server and its database, and use role-based access. These are defensive protections for your own
backups. All work is authorized administration.

## Hands-On Lab

Platform-architecture walkthroughs. **Shared prerequisites** — a free **Veeam Backup & Replication
Community Edition** server with the Veeam PowerShell module (`Connect-VBRServer`). **Cost:** none.

### Lab 2.1 — Read the platform roles

**Objective:** See the backup server and its components.

```powershell
PS> Connect-VBRServer -Server localhost
PS> Get-VBRBackupServerInfo | Select-Object Name, Version, PatchLevel

Name       Version   PatchLevel
----       -------   ----------
localhost  13.0.0    P20260401
```

**Expected result:** the backup server identified on **v13** — the management brain of the platform.

**Negative test:** run backups directly against production with no dedicated proxy or repository plan;
design the three roles deliberately instead.

**Rollback:** none (read-only).

### Lab 2.2 — Add a backup repository

**Objective:** Provide a storage target.

```powershell
PS> $server = Get-VBRServer -Name "localhost"
PS> Add-VBRBackupRepository -Name "Repo-01" -Server $server -Folder "E:\Backups" -Type WinLocal
PS> Get-VBRBackupRepository -Name "Repo-01" | Select-Object Name, Type, Path

Name    Type      Path
----    ----      ----
Repo-01 WinLocal  E:\Backups
```

**Expected result:** a backup repository `Repo-01` ready to receive backups.

**Negative test:** target backups at the same disk as production; a failure loses both — use separate
(ideally hardened/immutable) storage.

**Rollback:**

```powershell
PS> Remove-VBRBackupRepository -Repository (Get-VBRBackupRepository -Name "Repo-01")
```

### Lab 2.3 — Add a backup proxy

**Objective:** Provide a data mover.

```powershell
PS> $srv = Get-VBRServer -Name "localhost"
PS> Add-VBRViProxy -Server $srv -MaxTasks 4
PS> Get-VBRViProxy | Select-Object Name, MaxTasksCount, TransportMode

Name       MaxTasksCount TransportMode
----       ------------- -------------
localhost  4             Auto
```

**Expected result:** a backup proxy with a task limit — the component that moves and processes data.

**Negative test:** set proxy `MaxTasks` far above the host's CPU/RAM; jobs contend and slow — size to
the hardware.

**Rollback:** none (the default proxy is left in place).

### Lab 2.4 — Reason about editions

**Objective:** Match the edition to the requirement.

```python
python3 - <<'PY'
editions = {
  "Community": "free; core backup/restore; limited scale; no orchestration",
  "Foundation": "entry paid; broader workloads",
  "Advanced":  "adds monitoring/analytics (Veeam ONE)",
  "Premium":   "full Data Platform: orchestration + security + recovery",
}
for ed, features in editions.items():
    print(f"{ed:10}: {features}")
print("Rule: orchestration + full security = Premium; free lab = Community")
PY
```

**Expected result:** the editions ranked by capability, with Premium unlocking the full platform.

**Negative test:** promise orchestrated DR on a Community edition; upgrade to **Premium** for
Recovery Orchestrator and the full security set.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Veeam Data Platform centers on Backup & Replication v13 — a backup server (brain), backup proxies
(data movers), and repositories (storage targets, ideally hardened or immutable) — with Veeam ONE,
Recovery Orchestrator, and Data Cloud, delivered in editions from free Community up to full-platform
Premium.

- [ ] I can describe the backup server, proxy, and repository roles.
- [ ] I can add a backup repository.
- [ ] I can add a backup proxy and size it.
- [ ] I can match an edition to a requirement.
- [ ] I completed Labs 2.1–2.4 including each negative test.
