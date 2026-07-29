# Chapter 03: ACA — Storage and Database

## Learning Objectives

- Store objects with OSS and manage access.
- Choose block, object, and file storage.
- Deploy managed databases with RDS and PolarDB.
- Protect data with backups and snapshots.
- Complete a walkthrough for each storage/database topic.

## Theory and Architecture

The second ACA Cloud Computing area is storage and databases. **OSS (Object Storage Service)** stores
unstructured objects in **buckets** with policies, versioning, lifecycle rules (tiering to cheaper
storage classes), and access control — the equivalent of an object store for backups, media, and
static assets. Alongside OSS, ECS uses **block storage** (cloud disks, with **snapshots**) and there
is **NAS** for shared file storage — three storage types for different needs. Databases are managed by
**RDS (Relational Database Service)** — MySQL, PostgreSQL, SQL Server, and more, with automated
backups, high-availability replicas, and read replicas — and by **PolarDB**, Alibaba's **cloud-native**
database that separates compute and storage for elastic scaling and fast failover. Data protection
comes from **automated backups**, **disk snapshots**, and **cross-region replication**. Understanding
when to use each storage type and how managed databases provide HA and backups is core ACA knowledge.
This chapter teaches each with a hands-on walkthrough (storage selection, OSS access, and database HA).

## Design Considerations

Match storage to need: **OSS** for objects, **block/cloud disks** for ECS, **NAS** for shared files.
Use OSS **lifecycle** rules to tier cold data. Secure OSS buckets (**private by default**, least-
privilege policies). Choose **RDS** for managed relational databases with **HA replicas** and
**backups**; **PolarDB** for elastic cloud-native scale. Enable **backups/snapshots** and test
restores.

## Implementation and Automation

The labs select storage, secure an OSS bucket, and design database HA.

## Validation and Troubleshooting

Confirm the storage/database model:

```text
Storage: OSS (objects, buckets, lifecycle tiering) + block/cloud disks (ECS, snapshots) + NAS (shared files). RDS = managed relational DB (MySQL/PG/SQL Server) with HA replicas + backups; PolarDB = cloud-native (compute/storage separation, elastic).
Protect: automated backups + snapshots + cross-region replication.
```

Common pitfalls: **public** OSS buckets (data exposure); and a single database instance with no
**HA replica/backup**.

## Security and Best Practices

Match storage to need, tier with **OSS lifecycle**, keep buckets **private** with least-privilege
policies, run **RDS with HA replicas and backups**, and test restores. All work is authorized
administration.

## Hands-On Lab

Storage/database walkthroughs. **Shared prerequisites** — `python3`; aliyun CLI optional. **Cost:**
none (modeled).

### Lab 3.1 — Select the right storage

**Objective:** Match storage type to workload.

```python
python3 - <<'PY'
needs={"backups + media + static site":"OSS (object)","ECS OS/data disk":"block (cloud disk) + snapshots",
       "shared files across many ECS":"NAS (file)","cold archive":"OSS Archive storage class (lifecycle)"}
for need,storage in needs.items(): print(f"{need:30}: {storage}")
PY
```

**Expected result:** each need matched to **OSS/block/NAS** — correct storage selection.

**Negative test:** store shared files by attaching one disk to many ECS (block is single-attach); use
**NAS** for shared file access.

**Cleanup:** none.

### Lab 3.2 — Secure an OSS bucket

**Objective:** Private by default.

```python
python3 - <<'PY'
bucket={"name":"acme-backups","acl":"private","versioning":"enabled","lifecycle":"tier to Archive after 90d",
        "policy":"allow RAM role 'backup-writer' PutObject only"}
for k,v in bucket.items(): print(f"{k:11}: {v}")
print("OSS: private ACL + least-privilege policy + versioning + lifecycle tiering")
PY
```

**Expected result:** a **private**, versioned, lifecycle-tiered bucket with least-privilege access —
secure OSS.

**Negative test:** set the bucket ACL to **public-read** for convenience; data leaks — keep it
**private** with scoped policies.

**Cleanup:** none.

### Lab 3.3 — Design database high availability

**Objective:** Survive a database failure.

```python
python3 - <<'PY'
rds={"engine":"MySQL","topology":"primary (az-a) + standby replica (az-b) — automatic failover",
     "read_replicas":"2 (offload reads)","backup":"automated daily + binlog (point-in-time restore)"}
for k,v in rds.items(): print(f"{k:13}: {v}")
print("RDS: primary+standby across AZs (auto failover) + read replicas + PITR backups")
PY
```

**Expected result:** an **HA RDS** topology (multi-AZ standby, read replicas, PITR) — resilient
database.

**Negative test:** run a single RDS instance with no standby; a failure means downtime — deploy an
**HA replica**.

**Cleanup:** none.

### Lab 3.4 — Choose RDS vs PolarDB

**Objective:** Match the database service.

```python
python3 - <<'PY'
choices={"standard MySQL app, predictable load":"RDS MySQL","need elastic scale + fast failover + large storage":"PolarDB",
         "existing SQL Server workload":"RDS SQL Server","serverless-style bursty DB":"PolarDB (auto scaling)"}
for need,svc in choices.items(): print(f"{need:44}: {svc}")
PY
```

**Expected result:** each need matched to **RDS or PolarDB** — correct database service choice.

**Negative test:** force a highly elastic, huge-storage workload onto standard RDS; **PolarDB** is
built for that — use it.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

ACA storage and databases cover OSS object storage (private, tiered), block and NAS storage, and
managed RDS/PolarDB databases with multi-AZ HA and backups — choosing the right service and protecting
data.

- [ ] I can select the right storage type.
- [ ] I can secure an OSS bucket.
- [ ] I can design database high availability.
- [ ] I can choose RDS vs PolarDB.
- [ ] I completed Labs 3.1–3.4 including each negative test.
