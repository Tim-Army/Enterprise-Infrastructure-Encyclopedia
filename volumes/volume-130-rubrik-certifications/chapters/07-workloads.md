# Chapter 07: Protecting Workloads — Cloud-Native, Database, and SaaS

## Learning Objectives

- Cover the workload breadth Rubrik protects: on-prem, cloud-native (AWS/Azure), databases, and SaaS (M365).
- Understand application-consistent protection and the Rubrik Backup Service.
- Model workload-appropriate protection choices.

## One platform, many workloads

RCSA and Rubrik University's workshops cover protecting a broad estate under one policy model: virtual machines, physical hosts, NAS, **databases**, **cloud-native** resources (AWS/Azure), and **SaaS** (Microsoft 365). The skill is choosing **workload-appropriate** protection — a database needs application-consistent, log-aware backups; a cloud object store needs native snapshots; M365 needs API-based protection.

| Workload | Protection approach |
|:---|:---|
| **VM / physical** | Snapshot via hypervisor integration or the Rubrik Backup Service (RBS) agent |
| **Database** | Application-consistent backups + transaction-log backups (point-in-time to the second); RBS / Managed Volumes |
| **Cloud-native (AWS/Azure)** | Native snapshots of instances/volumes/objects via RSC cloud integration |
| **SaaS (M365)** | API-based protection of Exchange/SharePoint/OneDrive/Teams |

## Hands-On Lab

Python models workload-appropriate protection. **Cost:** none.

### Lab 7.1 — Choose the right protection per workload

**Objective:** Match the protection method to the workload — the RCSA operational skill.

```bash
python3 - <<'EOF'
def protect(workload):
    plan = {
      "sql-database":    "application-consistent snapshot + transaction-log backup (point-in-time recovery)",
      "vmware-vm":       "hypervisor snapshot (crash/app-consistent) via RSC",
      "aws-ec2":         "native EBS snapshot via RSC cloud integration",
      "azure-blob":      "native object snapshot / immutable copy",
      "m365-mailbox":    "API-based backup (Graph) of Exchange Online",
      "physical-linux":  "RBS agent, filesystem + app-consistent where supported",
    }
    return plan.get(workload, "assess: consistency needs + native vs agent")
for w in ["sql-database","vmware-vm","aws-ec2","m365-mailbox"]:
    print(f"{w:<14} -> {protect(w)}")
EOF
```

**Expected result:** Each workload matched to its method — the SQL database gets application-consistent + log backups (point-in-time), the VM a hypervisor snapshot, EC2 a native EBS snapshot, M365 API-based backup. RCSA tests knowing that **one size does not fit all**: consistency requirements and the native vs agent decision differ per workload.

**Negative test:** Taking a crash-consistent snapshot of a busy database without quiescing/log-awareness — you may recover a database in an inconsistent state; application-consistent + transaction-log protection is what enables clean point-in-time database recovery.

**Cleanup:** None.

### Lab 7.2 — Application-consistent vs crash-consistent

**Objective:** Understand the consistency distinction that governs database recovery.

```bash
python3 - <<'EOF'
# Consistency levels and what they guarantee on recovery
levels = {
  "crash-consistent":       "like pulling the power — filesystem intact, app may need recovery/repair on start",
  "application-consistent":  "app flushed/quiesced (VSS/pre-scripts) — clean, immediately usable on restore",
  "log-aware (DB)":          "app-consistent base + transaction logs -> recover to ANY point in time",
}
for level, guarantee in levels.items():
    print(f"{level:<24}: {guarantee}")
print("\nDatabases -> app-consistent + logs; general VMs -> often crash-consistent is acceptable.")
EOF
```

**Expected result:** The three consistency levels — crash-consistent (power-pull), application-consistent (quiesced, clean), and log-aware (any point in time) — and where each applies. Databases demand application-consistent-plus-logs for point-in-time recovery; many general VMs tolerate crash-consistent. This distinction is a staple of protecting workloads correctly.

**Negative test:** Assuming all snapshots are equal — restoring a crash-consistent database snapshot may require lengthy repair or lose in-flight transactions; the consistency level determines the recovery quality.

**Cleanup:** None.

### Lab 7.3 — SaaS and the shared-responsibility gap

**Objective:** Explain why M365/SaaS still needs backup.

```bash
cat <<'EOF'
Shared responsibility (M365 and most SaaS):
  Microsoft ensures: service uptime, infrastructure resilience, geo-redundancy
  YOU are responsible for: YOUR DATA — retention beyond native limits, recovery from
    accidental/malicious deletion, ransomware in OneDrive/SharePoint, long-term compliance holds
Native "recycle bin" retention is short and not a backup. Rubrik protects M365 via API for real recovery.
EOF
```

**Expected result:** The shared-responsibility reality — Microsoft runs the service, **you own recovering your data** — so SaaS like M365 needs real backup beyond the short native recycle bin. Malicious/accidental deletion and ransomware in cloud files are recoverable only with independent backup; RCSA/workshop material covers protecting SaaS for exactly this reason.

**Negative test:** Assuming "it's in the cloud, so it's backed up" — SaaS providers guarantee *service* availability, not recovery of *your data* from deletion/ransomware; the shared-responsibility gap is what third-party SaaS backup fills.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Workload-appropriate protection (VM/DB/cloud/SaaS) matched correctly.
- [ ] Application-consistent vs crash-consistent vs log-aware distinctions internalized.
- [ ] The SaaS shared-responsibility gap (why M365 needs backup) understood.
