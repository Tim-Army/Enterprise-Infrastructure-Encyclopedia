# Chapter 09: Cluster Management, Security, and Career

## Learning Objectives

- Diagnose and maintain cluster health.
- Configure role-based access control (RBAC).
- Snapshot and restore a cluster.
- Plan certification prep, currency (8.15→9.3), and career.
- Complete a walkthrough for each management-security-career topic.

## Theory and Architecture

The **Certified Engineer** exam's **Cluster Management** and **Security & Access Control** domains close
the operational picture. **Cluster health** is `green`/`yellow`/`red` — you diagnose unassigned shards
with the allocation-explain API and maintain health as nodes change. **Snapshots** (to a registered
repository — shared filesystem, S3, Azure, GCS) back up indices and cluster state, and **Snapshot
Lifecycle Management (SLM)** automates them; **cross-cluster** search and replication span clusters.
**Security** — new to the 9.3 blueprint — is **RBAC**: users, **roles** with cluster/index privileges,
**API keys**, and securing a cluster for production (TLS, authentication, network hardening). On careers:
the Engineer grounds Elasticsearch skills; the Analyst, Observability Engineer, and SIEM Analyst branch
into analytics, observability, and security. Track the **8.15→9.3** transition (1 September 2026) and
re-certify against the current version. This chapter closes with management, security, prep, and career.

## Design Considerations

Keep clusters **green** with adequate replicas and balanced shards; investigate `yellow`/`red` promptly.
Automate backups with **SLM** to a durable repository, and test restores. Apply **least-privilege RBAC**
— scoped roles and API keys, TLS everywhere, no default passwords. Plan certification **currency** against
the 9.3 update, and ladder from Engineer to the Analyst/Observability/SIEM specialties.

## Implementation and Automation

The labs diagnose cluster health, create a least-privilege role and API key, register a snapshot
repository, and plan the certification path — the management, security, and career work the exam and
program validate.

## Validation and Troubleshooting

Confirm management, security, and career:

```text
Health: green/yellow/red; _cluster/allocation/explain for unassigned shards
Backup: snapshot to registered repo (fs/S3/Azure/GCS); SLM automates; test restore
Security (9.3): RBAC roles + API keys + TLS + secure for production
Currency: Engineer 8.15 -> 9.3 (1 Sep 2026); re-certify current version
Career: Engineer -> Analyst / Observability Engineer / SIEM Analyst
```

Common pitfalls: ignoring a **yellow** cluster until it goes **red**; and running a cluster with security
disabled or default credentials — enable **RBAC/TLS**.

## Security and Best Practices

Least-privilege **RBAC**, **API keys** over shared passwords, **TLS** everywhere, and tested **snapshots**
are the baseline for a production cluster — defensive protection of your own platform. All work is
authorized administration.

## Hands-On Lab

Management-security-career walkthroughs. **Shared prerequisites** — an Elasticsearch cluster at
`https://localhost:9200`, `curl`, and `python3`. **Cost:** none.

### Lab 9.1 — Diagnose cluster health

**Objective:** Find and explain unassigned shards.

```bash
curl -s -k -u elastic:$PW "https://localhost:9200/_cluster/health?pretty"
curl -s -k -u elastic:$PW "https://localhost:9200/_cluster/allocation/explain?pretty" -H 'Content-Type: application/json' -d'{}'
```

```json
{ "status": "yellow", "unassigned_shards": 1,
  "explanation": "cannot allocate replica: no other node to hold a copy (single-node cluster)" }
```

**Expected result:** the reason a shard is unassigned — the first step in restoring health.

**Negative test:** restart nodes blindly to fix `yellow`; use **allocation/explain** to find the actual
cause first.

**Cleanup:** none (read-only).

### Lab 9.2 — Create a least-privilege role and API key

**Objective:** Apply RBAC.

```bash
curl -s -k -u elastic:$PW -X POST "https://localhost:9200/_security/role/logs_reader" -H 'Content-Type: application/json' -d'
{ "indices": [ { "names": ["logs-*"], "privileges": ["read","view_index_metadata"] } ] }'
curl -s -k -u elastic:$PW -X POST "https://localhost:9200/_security/api_key" -H 'Content-Type: application/json' -d'
{ "name": "logs-dashboard", "role_descriptors": { "logs_reader": { "indices": [ { "names": ["logs-*"], "privileges": ["read"] } ] } } }'
```

```json
{ "id": "VuaC...", "name": "logs-dashboard", "api_key": "ui2l..." }
```

**Expected result:** a read-only `logs-*` role and a scoped API key — least privilege, not superuser.

**Negative test:** hand an app the `elastic` superuser credentials; issue a **scoped API key** with only
the needed index privileges instead.

**Cleanup:**

```bash
curl -s -k -u elastic:$PW -X DELETE "https://localhost:9200/_security/role/logs_reader"
```

### Lab 9.3 — Register a snapshot repository

**Objective:** Enable backups.

```bash
curl -s -k -u elastic:$PW -X PUT "https://localhost:9200/_snapshot/backup_repo" -H 'Content-Type: application/json' -d'
{ "type": "fs", "settings": { "location": "/mnt/es-backups" } }'
curl -s -k -u elastic:$PW -X PUT "https://localhost:9200/_snapshot/backup_repo/snap-1?wait_for_completion=true"
```

```json
{ "snapshot": { "snapshot": "snap-1", "state": "SUCCESS", "shards": { "failed": 0 } } }
```

**Expected result:** a registered repository and a successful snapshot — backups in place (automate with
SLM).

**Negative test:** run a cluster with no snapshot repository; a disaster loses everything — register a
repo and schedule **SLM**.

**Cleanup:**

```bash
curl -s -k -u elastic:$PW -X DELETE "https://localhost:9200/_snapshot/backup_repo/snap-1"
curl -s -k -u elastic:$PW -X DELETE "https://localhost:9200/_snapshot/backup_repo"
```

### Lab 9.4 — Plan the certification path and currency

**Objective:** Map the path and the 8.15→9.3 transition.

```python
python3 - <<'PY'
from datetime import date
switch = date(2026, 9, 1); today = date(2026, 7, 29)
ver = "9.3" if today >= switch else "8.15 (until 9.3 on 1 Sep 2026)"
print(f"Certified Engineer exam version today: {ver}")
ladder = ["Certified Engineer (Elasticsearch/search)",
          "-> Certified Analyst (Kibana)",
          "-> Certified Observability Engineer (metrics/logs/APM)",
          "-> Certified SIEM Analyst (Elastic Security)"]
for step in ladder: print(step)
print("Currency: re-certify against the current major version")
PY
```

**Expected result:** the current exam version and the certification ladder — a prep and career plan.

**Negative test:** study 8.15-only topics for an exam you will sit after 1 September 2026; prepare for
**9.3** (ES|QL, semantic search, RBAC).

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Cluster management and security close the Engineer picture: diagnosing health with allocation-explain,
automating snapshots with SLM, and securing production with least-privilege RBAC, API keys, and TLS —
while the certification path ladders from Engineer to the Analyst, Observability, and SIEM specialties,
kept current against the 8.15→9.3 transition.

- [ ] I can diagnose and maintain cluster health.
- [ ] I can configure RBAC roles and API keys.
- [ ] I can register a snapshot repository and take a snapshot.
- [ ] I can plan the certification path and currency.
- [ ] I completed Labs 9.1–9.4 including each negative test.
