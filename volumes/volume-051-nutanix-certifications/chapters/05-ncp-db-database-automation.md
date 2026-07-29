# Chapter 05: NCP-DB — Database Automation

## Learning Objectives

- Explain what the NCP-DB certifies and its target role.
- Summarize the four blueprint sections.
- Deploy and configure Nutanix Database Service (NDB).
- Operate, maintain, monitor, and administer an NDB environment.
- Complete a per-section walkthrough for each NCP-DB domain.

## Theory and Architecture

The **Nutanix Certified Professional — Database Automation (NCP-DB)** validates
managing databases with **Nutanix Database Service (NDB)** — the DBaaS credential
(**95 questions / 180 minutes**). Its blueprint has **four sections**: **Deploy and
Configure an NDB Solution**; **Monitor Alerts and Storage Usage within an NDB
Implementation**; **Operate and Maintain an NDB Environment**; and **Administer an NDB
Environment**. NDB provisions and manages Oracle, SQL Server, PostgreSQL, MySQL, and
MariaDB.

## Design Considerations

The DBA deploys the **NDB server**, registers source databases, provisions from
**profiles** (software/compute/network/database-parameter), uses **time-machine**
snapshots and clones for copy-data management, monitors **alerts/storage**, patches
and maintains, and **administers** RBAC and multi-cluster. Time Machine (SLA-driven
snapshots) is central.

## Implementation and Automation

The labs use NDB concepts and the NDB API/CLI for each section — deploy/configure,
monitor, operate/maintain, and administer.

## Validation and Troubleshooting

Confirm the blueprint before studying:

```text
nutanix.com > NCP-DB blueprint (95 Q / 180 min):
  1 Deploy and Configure an NDB Solution
  2 Monitor Alerts and Storage Usage within an NDB Implementation
  3 Operate and Maintain an NDB Environment
  4 Administer an NDB Environment
```

Common pitfalls: cloning full copies instead of **time-machine** clones; and no SLA on
time machines (no point-in-time recovery).

## Security and Best Practices

Provision from standardized **profiles**, protect databases with **Time Machine SLAs**,
use space-efficient **clones** for dev/test, monitor **storage/alerts**, patch on a
cadence, and enforce **RBAC**. Store DB credentials in NDB's vault.

## References and Knowledge Checks

- nutanix.com: NCP-DB blueprint guide; Nutanix Database Service (NDB) docs.

**Knowledge checks**

1. What is a Time Machine, and why set an SLA?
2. How do NDB clones save space versus a full copy?
3. What do profiles standardize?

## Hands-On Lab

Per-section walkthroughs — NCP-DB. **Shared prerequisites** — an NDB deployment (or
its API); commands shown as NDB API/CLI patterns. **Cost:** none beyond a lab cluster.

### Lab 5.1 — Deploy and configure an NDB solution

**Objective:** Register a source database via the NDB API.

```bash
# NDB REST API (bearer token from NDB): register a PostgreSQL source DB server
curl -sS -X POST "https://<ndb>/era/v0.9/dbservers/register" \
  -H "Authorization: Bearer $NDB_TOKEN" -H "Content-Type: application/json" \
  -d '{"databaseType":"postgres_database","vmIp":"10.0.0.50","nxClusterId":"<id>"}'
```

**Expected result:** a registered DB server (JSON with a work ID) — the deploy/
configure section.

**Negative test:** manage the DB VM by hand; **register with NDB** so it manages
lifecycle/patching/backup.

**Cleanup:** deregister the DB server if it was for the lab.

### Lab 5.2 — Monitor alerts and storage usage

**Objective:** Query NDB alerts and storage.

```bash
curl -sS "https://<ndb>/era/v0.9/alerts" -H "Authorization: Bearer $NDB_TOKEN" \
  | python3 -c "import sys,json;print('open alerts:',len(json.load(sys.stdin)))"
```

**Expected result:** the count of NDB **alerts** (and the storage view) — the
monitoring section.

**Negative test:** watch only the guest OS; NDB **alerts/storage** track the DBaaS
layer — monitor both.

**Cleanup:** none (read-only).

### Lab 5.3 — Operate and maintain (Time Machine clone)

**Objective:** Create a point-in-time clone from a Time Machine.

```bash
# Clone a database as of a timestamp (space-efficient, from Time Machine snapshots):
curl -sS -X POST "https://<ndb>/era/v0.9/tms/<tm-id>/clones" \
  -H "Authorization: Bearer $NDB_TOKEN" -H "Content-Type: application/json" \
  -d '{"name":"dev-clone","pointInTime":"2026-07-27 09:00:00"}'
```

**Expected result:** a space-efficient **PIT clone** for dev/test — the operate/
maintain section.

**Negative test:** copy the full database for dev; a **Time Machine clone** is instant
and space-efficient — use it.

**Cleanup:** delete the clone when done.

### Lab 5.4 — Administer an NDB environment

**Objective:** Review NDB roles/access.

```bash
curl -sS "https://<ndb>/era/v0.9/users" -H "Authorization: Bearer $NDB_TOKEN" \
  | python3 -c "import sys,json;print('NDB users:',len(json.load(sys.stdin)))"
```

**Expected result:** the NDB user/role inventory — the administration section (RBAC,
multi-cluster).

**Negative test:** share one admin login; assign **scoped NDB roles** per team.

**Cleanup:** none (read-only).

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The NCP-DB certifies database automation with NDB across four sections: deploy/
configure, monitor alerts/storage, operate/maintain (Time Machine clones), and
administer (RBAC, multi-cluster) — via the NDB API/CLI.

- [ ] I can register and configure databases in NDB.
- [ ] I can monitor NDB alerts and storage.
- [ ] I can create Time Machine clones.
- [ ] I can administer NDB roles and access.
- [ ] I completed Labs 5.1–5.4 including each negative test.
