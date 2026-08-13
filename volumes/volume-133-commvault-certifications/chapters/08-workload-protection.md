# Chapter 08: Workload Protection

## Learning Objectives

- Protect the workloads Readiverse certifies: Microsoft 365, Active Directory and Entra ID, VMware, Oracle, and file servers.
- Explain why SaaS data needs backup despite provider redundancy.
- Choose application-consistent protection over crash-consistent snapshots.
- Match recovery granularity to what users actually ask for.

## The third pillar

**Workload and feature expertise** is the third Readiverse learning pillar, and even the Practitioner tier requires at least one workload course. The reason is practical: the platform skills of Chapters 02–05 are common, but each workload has its own consistency requirements, recovery granularity, and failure modes.

Readiverse's "Workload Hero" courses cover **Microsoft 365**, **Active Directory and Entra ID**, **file server protection**, **VMware**, and **Oracle** — the set this chapter follows.

## Consistency: the concept that spans every workload

| Level | What it guarantees | Risk |
|:---|:---|:---|
| **Crash-consistent** | The disk image as it was at an instant — as if the power was pulled | Databases may need recovery on start; in-flight transactions lost |
| **File-system-consistent** | Buffers flushed to disk | Application-level state may still be mid-transaction |
| **Application-consistent** | The application quiesced, logs flushed, a recoverable state captured (VSS on Windows, agents/RMAN for databases) | The correct target for databases and transactional applications |

The rule: **anything with transactions needs application-consistent protection.** A crash-consistent snapshot of a busy database is a recovery gamble, and the exam expects you to know the difference.

## The workloads

### Microsoft 365 — the shared responsibility gap

The most consequential misunderstanding in modern data protection: **Microsoft replicates your data; they do not back it up for you.** Replication faithfully copies deletion and encryption. The retention/recycle-bin windows are short, and the provider's responsibility is service availability, not your data's recoverability.

What backup covers that replication does not: accidental or malicious deletion beyond the retention window, ransomware in OneDrive/SharePoint, departed-employee data, long-term compliance retention, and granular restore of a single mailbox item. The same argument applies to Salesforce, Google Workspace, and every other SaaS platform.

### Active Directory and Entra ID — identity is the first recovery

If AD is down, almost nothing else can authenticate — so identity recovery precedes application recovery (Chapter 07's cleanroom sequence). Two distinct scenarios:

- **Granular recovery** — restore a deleted user, group, or attribute without disrupting the directory.
- **Forest recovery** — rebuild the entire directory after compromise, which is a rehearsed procedure, not an improvisation, and which must produce a *clean* directory (a restored-but-compromised AD reinstates the attacker's persistence).

### VMware — efficient, but mind the guest

Hypervisor-level protection is efficient: one agentless job protects many VMs via snapshots and changed-block tracking. But a VM-level snapshot is **crash-consistent to the guest** unless quiescing is used — so a database inside a VM still needs application-consistent treatment.

### Oracle and databases — RMAN, logs, and point-in-time

Databases need their native integration (RMAN for Oracle), **archive/redo log** backups for point-in-time recovery, and a recovery model that lets you roll forward to a chosen moment. The log backups are what turn a nightly full into a one-hour RPO (Chapter 05's tier-1 failure).

### File servers — the granularity problem

Large file estates back up easily and restore awkwardly. The overwhelmingly common request is "restore this one file from last Tuesday," so index quality and search matter more than raw throughput.

## Hands-On Lab

Python models workload protection. **Cost:** none.

### Lab 8.1 — Consistency level per workload

**Objective:** Match the protection method to the workload's needs.

```bash
python3 - <<'EOF'
workloads = [
  {"name":"Oracle database", "transactional":True,  "method":"crash-consistent VM snapshot"},
  {"name":"Oracle database", "transactional":True,  "method":"RMAN + archive logs (app-consistent)"},
  {"name":"SQL Server",      "transactional":True,  "method":"VSS app-consistent + log backups"},
  {"name":"File server",     "transactional":False, "method":"crash-consistent VM snapshot"},
  {"name":"Web server (stateless)","transactional":False,"method":"crash-consistent VM snapshot"},
]
for w in workloads:
    app_consistent = "app-consistent" in w["method"] or "RMAN" in w["method"] or "VSS" in w["method"]
    if w["transactional"] and not app_consistent:
        verdict = "RISK — transactional workload with crash-consistent protection; restore may require recovery or lose in-flight transactions"
    elif w["transactional"]:
        verdict = "CORRECT — application quiesced, logs captured, point-in-time recovery possible"
    else:
        verdict = "ACCEPTABLE — non-transactional workload tolerates crash-consistent"
    print(f"{w['name']:24} via {w['method']:38}\n    -> {verdict}\n")
EOF
```

**Expected result:** The Oracle-via-VM-snapshot row is flagged as a risk while the RMAN row is correct; the stateless and file workloads are fine crash-consistent. The distinction is not academic — a crash-consistent copy of a transactional database can restore into a state requiring recovery, or silently lose committed transactions.

**Negative test:** Protecting every VM identically at the hypervisor layer for operational simplicity — efficient and uniform, and it quietly leaves every database in the estate on crash-consistent protection.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.2 — The SaaS shared-responsibility gap

**Objective:** Show what provider replication does not cover.

```bash
python3 - <<'EOF'
scenarios = [
  ("Datacenter failure at the provider",       "provider replication", True),
  ("User deletes a mailbox, found 6 months on","provider replication", False),
  ("Ransomware encrypts OneDrive/SharePoint",  "provider replication", False),
  ("Departed employee's data needed for legal","provider replication", False),
  ("7-year compliance retention",              "provider replication", False),
  ("Restore one email from 14 months ago",     "provider replication", False),
]
print(f"{'scenario':46}{'covered by provider?':>22}")
for desc, _, covered in scenarios:
    print(f"{desc:46}{('YES' if covered else 'NO — needs backup'):>22}")
print("\nProviders guarantee SERVICE availability, not YOUR data's recoverability.")
print("Replication is not backup: it faithfully replicates deletion and encryption too.")
EOF
```

**Expected result:** Only infrastructure failure is covered; every other scenario — deletion past retention, ransomware, departed employees, long-term compliance, granular historical restore — requires backup. The one-line summary is the argument the M365 workload course exists to make, and it is the most commercially important point in modern data protection.

**Negative test:** "Our data is in the cloud, so it is backed up" — replication copies the deletion as faithfully as it copies the data, and the recycle-bin window expires long before most organizations discover the loss.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.3 — Recovery granularity

**Objective:** Match recovery capability to what users actually request.

```bash
python3 - <<'EOF'
requests = [
  {"ask":"restore one email from 14 months ago",  "granularity":"item",        "workload":"M365"},
  {"ask":"restore a deleted AD user + group memberships","granularity":"object","workload":"Active Directory"},
  {"ask":"restore one file from last Tuesday",    "granularity":"file",        "workload":"File server"},
  {"ask":"roll the database back to 14:05 exactly","granularity":"point-in-time","workload":"Oracle"},
  {"ask":"bring back the whole VM",               "granularity":"full image",   "workload":"VMware"},
]
requires = {
  "item":"item-level indexing of mailbox/site contents",
  "object":"granular directory object restore (no forest recovery)",
  "file":"file-level index + search across restore points",
  "point-in-time":"archive/redo log backups + roll-forward",
  "full image":"image-level restore or instant VM recovery",
}
for r in requests:
    print(f"{r['workload']:17} '{r['ask']}'")
    print(f"{'':17} granularity: {r['granularity']:14} requires {requires[r['granularity']]}\n")
print("Most real requests are GRANULAR. A platform that only restores whole images fails the common case.")
EOF
```

**Expected result:** Each request maps to a granularity and the capability it requires — item-level indexing, granular object restore, file search, log roll-forward, image restore. The closing observation is the operational reality: disasters are rare, but "restore this one thing" happens weekly, so indexing and granular restore determine whether the platform feels useful day to day.

**Negative test:** Designing only for whole-system disaster recovery — you meet the rare case and fail the common one, and users conclude backups do not work.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Crash-, file-system-, and application-consistent protection distinguished and applied.
- [ ] The SaaS shared-responsibility gap articulated for Microsoft 365.
- [ ] AD/Entra granular restore vs forest recovery understood, with identity recovered first.
- [ ] VMware, Oracle, and file-server specifics covered, including log-based point-in-time recovery.
- [ ] Recovery granularity matched to real user requests.
