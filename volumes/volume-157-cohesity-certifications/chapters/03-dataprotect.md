# Chapter 03: DataProtect — Backup, Recovery, and Archival

## Learning Objectives

- Explain DataProtect as the backup-and-recovery core of the Data Cloud.
- Describe policy-based protection, replication, and archival.
- Understand recovery — the point of backup — and instant mass restore.
- Recognize deduplication and the consolidated-storage advantage.

*Cert relevance: DataProtect is the subject of the Protection Associate (COH100) and Protection Professional certs — the platform core.*

## What DataProtect is

**DataProtect** is Cohesity's **backup and recovery** engine — the core of the [Data Cloud](01-the-cohesity-program.md) and the subject of the **Protection Associate (COH100)** and **Protection Professional** certifications. It backs up the enterprise's workloads — virtual machines, databases, physical servers, NAS, SaaS (Microsoft 365), and cloud — under **policy**, stores those backups efficiently on Cohesity's consolidated storage, and — the point of it all — **recovers** them quickly when needed. Where the earlier chapters framed *why* backup matters, DataProtect is *how* Cohesity does it. The lab models the protect-and-recover cycle.

## Policy-based protection

DataProtect is driven by **protection policies** rather than per-job scripting. A policy defines **what** to protect, **how often** (the backup frequency / RPO — recovery point objective), **how long to keep it** (retention), and **where** copies go (local, replicated, archived). You assign workloads to a policy, and the platform enforces it — consistent, auditable protection at scale, instead of a fragile mesh of individual backup jobs. Policy-based protection is what makes protecting thousands of workloads manageable and compliant. The lab models policies.

## Replication and archival

DataProtect implements the **3-2-1** discipline ([Chapter 2](02-modern-data-security-and-management.md)) through:

- **Replication** — copying backups to another Cohesity cluster (another site), so a site failure doesn't lose the backup. This provides disaster recovery and geographic redundancy.
- **Archival** — moving older backups to lower-cost storage (cloud object storage, tape) for long-term retention, freeing primary capacity while keeping data compliant and retrievable.

Together they place copies across media and locations — the "2" and "1" of 3-2-1 — under policy. The lab models the copy lifecycle.

## Recovery: the point of it all

A backup you cannot **recover** is worthless — recovery is the entire point, and it is where backup products prove themselves. DataProtect emphasizes **fast, flexible recovery**: restore a single file, an entire VM, a database, or thousands of VMs at once, to the original or an alternate location. Cohesity's architecture supports **instant mass restore** — bringing many workloads back rapidly, which is exactly what a ransomware recovery demands (you may need to restore your whole estate at once, quickly). The measure of a backup platform is not how it backs up but **how fast and reliably it recovers**, especially at scale under pressure. The lab models recovery.

## Deduplication and consolidation

Cohesity stores backups on **globally deduplicated** storage: identical data blocks are stored **once** across all workloads, dramatically reducing capacity (and cost) versus keeping full separate copies. Combined with [consolidation](02-modern-data-security-and-management.md) of backup, files, and archival onto one platform, this attacks **mass data fragmentation** — the uncontrolled proliferation of redundant data copies. Efficient, deduplicated, consolidated storage is both a cost win and the foundation that makes immutability and fast recovery practical at scale. The lab models deduplication.

## Hands-On Lab

Python models policy-based protection and recovery. **Cost:** none.

### Lab 3.1 — Policy-based protection, replication, and mass restore

**Objective:** Model protecting workloads and recovering them at scale.

```bash
python3 - <<'EOF'
# a protection policy applied to workloads, with replication + archival + mass restore
POLICY = {"name": "gold", "rpo_hours": 4, "retention_days": 30,
          "replicate_to": "site-B", "archive_after_days": 14}
WORKLOADS = ["vm-app-01","vm-app-02","vm-db-01","nas-finance","m365-mailboxes"] + [f"vm-web-0{i}" for i in range(1,6)]

print(f"Protection policy '{POLICY['name']}': every {POLICY['rpo_hours']}h, keep {POLICY['retention_days']}d,")
print(f"   replicate -> {POLICY['replicate_to']}, archive after {POLICY['archive_after_days']}d\n")
print(f"   applied to {len(WORKLOADS)} workloads (one policy, not {len(WORKLOADS)} scripts):")
for w in WORKLOADS[:4]:
    print(f"      {w}")
print(f"      ... (+{len(WORKLOADS)-4} more)\n")

# 3-2-1 realized by the policy
copies = ["local (site-A)", f"replicated ({POLICY['replicate_to']})", "archived (cloud object store)"]
print(f"   3-2-1 realized: {len(copies)} copies across media/sites -> {copies}\n")

# ransomware hits -> mass restore all workloads at once
print("Ransomware strikes -> recover the WHOLE estate:")
import time
restored = len(WORKLOADS)
print(f"   instant mass restore: {restored}/{len(WORKLOADS)} workloads recovered together")
print(f"   (single-file, single-VM, or MASS restore — to original or alternate location)\n")
print("DataProtect = POLICY-based protection (one policy governs many workloads: frequency,")
print("retention, replication, archival — not fragile per-job scripts) realizing 3-2-1, and")
print("— the whole point — fast, flexible RECOVERY. A backup you can't recover is worthless;")
print("the measure of a platform is how fast + reliably it restores, ESPECIALLY the mass")
print("restore a ransomware recovery demands. Global dedup makes storing it all affordable.")
EOF
```

**Expected result:** One "gold" policy governing many workloads (frequency, retention, replication, archival) realizing 3-2-1 across three copies, then an instant mass restore of the whole estate. The DataProtect lesson is that policy-based protection makes protecting thousands of workloads manageable, replication and archival place copies across sites and media, and fast flexible recovery — especially mass restore under ransomware — is the whole point, with global deduplication making it affordable at scale.

**Negative test:** Scripting backups per workload and measuring success by backup completion. Per-job sprawl is fragile and unauditable, and a backup that completes but cannot be recovered quickly at scale fails the only test that matters — recovery.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] DataProtect understood as the backup-and-recovery core of the Data Cloud.
- [ ] Policy-based protection understood — one policy governs frequency, retention, replication, archival at scale.
- [ ] Replication and archival understood as realizing the 3-2-1 discipline.
- [ ] Recovery recognized as the point — fast, flexible, mass restore — with deduplication and consolidation as the foundation.
