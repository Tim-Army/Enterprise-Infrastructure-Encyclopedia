# Chapter 08: Associate Atlas Administrator

## Learning Objectives

- Explain MongoDB Atlas and cluster tiers.
- Configure network access and database users.
- Reason about backup, point-in-time recovery, and monitoring.
- Explain Atlas Search and data federation.
- Complete a walkthrough for each Atlas topic.

## Theory and Architecture

**MongoDB Atlas** is MongoDB's fully managed cloud database service (DBaaS) on AWS, Azure, and Google
Cloud — the subject of the **Associate Atlas Administrator** certification. Atlas provisions and operates
**clusters** for you: the **free M0** shared tier for learning, then dedicated tiers (M10 and up) with
choices of region, cloud, and size. Administration is done in the Atlas UI/API/CLI: **network access**
(IP access lists and VPC/private endpoints), **database users** (with roles), automated **backup** with
**point-in-time recovery (PITR)**, **monitoring** (metrics, real-time performance panel, and **alerts**),
and one-click scaling and upgrades. Atlas also adds capabilities beyond the core database — **Atlas
Search** (Lucene-based full-text search integrated with the data), **Atlas Vector Search**, **Data
Federation** (query across clusters and cloud object storage), **Charts**, and **Triggers**. This chapter
teaches Atlas administration with hands-on walkthroughs (Atlas CLI/`mongosh` plus console reasoning).

## Design Considerations

Start on the **free M0** tier to learn, and size dedicated clusters to workload. Lock down **network
access** (specific IPs or private endpoints, never `0.0.0.0/0` in production) and create **least
-privilege database users**. Enable **backup with PITR** for recovery, and set **alerts** on the metrics
that matter (connections, replication lag, disk). Use **Atlas Search** instead of bolting on a separate
search engine when full-text search is needed close to the data.

## Implementation and Automation

The labs reason about cluster tiers, configure network access and a database user, and reason about
backup/monitoring and Atlas Search — the managed-service skills the Associate Atlas Administrator exam
validates.

## Validation and Troubleshooting

Confirm Atlas administration:

```text
Atlas = managed MongoDB (AWS/Azure/GCP); M0 free tier -> dedicated M10+ (region/cloud/size)
Access: IP access list + private endpoints; database users with roles (least privilege)
Resilience: automated backup + point-in-time recovery (PITR); monitoring metrics + alerts
Beyond core: Atlas Search (full-text), Vector Search, Data Federation, Charts, Triggers
```

Common pitfalls: an Atlas cluster open to `0.0.0.0/0` with a weak user (internet-exposed database); and
no **alerts**, so problems (disk full, replication lag) surface only as outages.

## Security and Best Practices

Restrict **network access**, use **least-privilege** database users, enable **backup/PITR**, and set
**alerts** — Atlas centralizes these defensive controls for your own managed database. All work is
authorized administration.

## Hands-On Lab

Atlas walkthroughs. **Shared prerequisites** — a free Atlas M0 cluster (or the concepts, modeled), the
Atlas CLI (`atlas`) and/or `mongosh`, and `python3`. **Cost:** none (M0 is free).

### Lab 8.1 — Reason about cluster tiers

**Objective:** Match a tier to a need.

```python
python3 - <<'PY'
tiers = {
  "M0 (free/shared)": "learning, prototypes; shared, limited storage",
  "M10-M30 (dedicated)":"small/mid production; backups, scaling, VPC peering",
  "M40+":               "large production; more RAM/IOPS; analytics nodes",
}
for tier, use in tiers.items():
    print(f"{tier:20}: {use}")
print("Start on M0 to learn; size dedicated tiers to the workload")
PY
```

**Expected result:** cluster tiers matched to use — free M0 for learning, dedicated for production.

**Negative test:** run production on the free **M0** shared tier; move to a **dedicated** tier for
backups, scaling, and SLAs.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.2 — Configure network access and a database user

**Objective:** Lock down access.

```bash
# Atlas CLI — allow only the office IP, not the whole internet
atlas accessLists create 203.0.113.10/32 --type ipAddress
atlas dbusers create --username appuser --role readWrite@shop --projectId $PID
atlas accessLists list
```

```text
IP ADDRESS          TYPE
203.0.113.10/32     ipAddress
```

**Expected result:** access limited to a specific IP and a scoped `readWrite@shop` user — least-privilege
access.

**Negative test:** add `0.0.0.0/0` to the access list "to make it work"; that exposes the database to the
internet — allow only specific IPs or private endpoints.

**Rollback:**

```bash
atlas accessLists delete 203.0.113.10/32 --force
```

### Lab 8.3 — Reason about backup and PITR

**Objective:** Plan recovery.

```python
python3 - <<'PY'
plan = {
  "Backup":  "automated snapshots on a schedule (retention per policy)",
  "PITR":    "restore to any second within the window (via the oplog)",
  "Test":    "periodic restore drills prove recoverability",
}
for k, v in plan.items(): print(f"{k:8}: {v}")
print("Rule: enable backup + PITR; a backup you never restore is not proven")
PY
```

**Expected result:** backup plus PITR planned, with restore testing — a recoverable managed database.

**Negative test:** rely on a single manual snapshot; enable **automated backup with PITR** and test
restores.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.4 — Reason about Atlas Search

**Objective:** Use integrated full-text search.

```python
python3 - <<'PY'
options = {
  "External search engine": "sync data to a separate cluster; extra infra + drift risk",
  "Atlas Search":           "Lucene index ON the Atlas data; $search stage in aggregation; no sync",
}
for k, v in options.items(): print(f"{k:24}: {v}")
print("Atlas Search: full-text (and Vector Search) integrated with the data -> no separate sync")
PY
```

**Expected result:** Atlas Search as the integrated full-text option — no separate engine to sync.

**Negative test:** stand up a separate search cluster and sync data for basic full-text search; use
**Atlas Search** integrated with the data instead.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

MongoDB Atlas is the managed cloud database the Associate Atlas Administrator operates: clusters from the
free M0 tier to dedicated tiers, locked down with IP access lists/private endpoints and least-privilege
database users, protected by automated backup with point-in-time recovery and alerting, and extended by
Atlas Search, Vector Search, and Data Federation.

- [ ] I can explain Atlas and cluster tiers.
- [ ] I can configure network access and a database user.
- [ ] I can plan backup and point-in-time recovery.
- [ ] I can reason about Atlas Search.
- [ ] I completed Labs 8.1–8.4 including each negative test.
