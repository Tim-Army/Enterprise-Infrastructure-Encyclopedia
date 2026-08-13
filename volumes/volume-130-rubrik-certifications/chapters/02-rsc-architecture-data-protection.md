# Chapter 02: Rubrik Security Cloud Architecture and Data Protection (RCSA Core)

## Learning Objectives

- Cover the RCSA core: Rubrik Security Cloud architecture and policy-driven data protection.
- Understand SLA Domains — the policy engine that replaces manual backup jobs.
- Model policy-driven protection and its compliance state.

## The RCSA foundation

RCSA validates operating **Rubrik Security Cloud (RSC)**: onboarding workloads, protecting them by policy, monitoring compliance, and recovering. The architectural shift Rubrik made — and RCSA's central concept — is **policy-driven protection via SLA Domains**, replacing hand-built backup jobs and schedules.

| Concept | What it is |
|:---|:---|
| **SLA Domain** | A reusable policy: how often to snapshot, how long to retain, where to archive/replicate, whether to make it immutable |
| **Protection by assignment** | You *assign* a workload to an SLA Domain; RSC handles scheduling, retention, and expiry automatically |
| **Compliance state** | RSC continuously reports whether each object is meeting its SLA (protected/at-risk) |
| **Workload coverage** | VMs, physical hosts, NAS, databases, cloud (AWS/Azure), SaaS (M365) |

## Hands-On Lab

Python models SLA Domains and compliance. **Cost:** none.

### Lab 2.1 — Define an SLA Domain (policy, not a job)

**Objective:** Express protection as a reusable policy.

```bash
python3 - <<'EOF'
# An SLA Domain: frequency + retention + archive/replicate + immutability — assigned, not scheduled by hand
sla_domains = {
  "Gold":   {"snapshot_every_hrs": 4,  "retain_days": 90,  "archive": "cloud", "immutable": True},
  "Silver": {"snapshot_every_hrs": 24, "retain_days": 30,  "archive": "cloud", "immutable": True},
  "Bronze": {"snapshot_every_hrs": 24, "retain_days": 7,   "archive": None,    "immutable": True},
}
for name, p in sla_domains.items():
    print(f"{name:8}: every {p['snapshot_every_hrs']}h, keep {p['retain_days']}d, "
          f"archive={p['archive']}, immutable={p['immutable']}")
print("\nAssign a workload to an SLA Domain -> RSC schedules, retains, expires, and archives automatically.")
EOF
```

**Expected result:** Three tiers (Gold/Silver/Bronze) as reusable policies — the RCSA model. You don't build a backup job per server; you define SLA Domains once and **assign** workloads to them. This is the operational efficiency (and consistency) that policy-driven protection delivers, and the concept RCSA leads with.

**Negative test:** Building a bespoke schedule per workload — that is the old backup-job world RSC replaces; it doesn't scale and drifts out of consistency. SLA Domains are the answer.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.2 — Assign workloads and read compliance

**Objective:** Protect workloads by assignment and monitor SLA compliance.

```bash
python3 - <<'EOF'
import datetime
now = datetime.datetime(2026, 8, 4, 12, 0)
# Each workload assigned to an SLA; compliance = did the last snapshot meet the frequency?
workloads = [
  {"name":"db-prod",   "sla":"Gold",   "sla_hrs":4,  "last_snap": now - datetime.timedelta(hours=2)},
  {"name":"fileserver","sla":"Silver", "sla_hrs":24, "last_snap": now - datetime.timedelta(hours=30)},  # overdue
  {"name":"web-01",    "sla":"Bronze", "sla_hrs":24, "last_snap": now - datetime.timedelta(hours=6)},
  {"name":"legacy-app","sla":None,     "sla_hrs":None,"last_snap": None},                                # unprotected!
]
for w in workloads:
    if w["sla"] is None: state = "UNPROTECTED (no SLA assigned)"
    else:
        age = (now - w["last_snap"]).total_seconds()/3600
        state = "IN COMPLIANCE" if age <= w["sla_hrs"] else f"AT RISK (last snap {age:.0f}h > {w['sla_hrs']}h)"
    print(f"{w['name']:<12} SLA={str(w['sla']):<7} -> {state}")
EOF
```

**Expected result:**

```text
db-prod      SLA=Gold    -> IN COMPLIANCE
fileserver   SLA=Silver  -> AT RISK (last snap 30h > 24h)
web-01       SLA=Bronze  -> IN COMPLIANCE
legacy-app   SLA=None    -> UNPROTECTED (no SLA assigned)
```

RSC continuously reports compliance: `db-prod` and `web-01` meet their SLA, `fileserver` is at risk (overdue), and `legacy-app` is unprotected. RCSA operators live in this **compliance view** — the answer to "is everything protected as required?" is a dashboard, not a spreadsheet of jobs.

**Negative test:** A workload nobody assigned to an SLA (`legacy-app`) is silently unprotected — the compliance view surfaces it; without policy-driven protection, unprotected assets hide until a recovery is needed and isn't there.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.3 — The RSC control-plane model

**Objective:** Understand RSC as SaaS control plane + local data.

```bash
cat <<'EOF'
Rubrik Security Cloud (RSC) architecture:
  Control plane (SaaS): policy (SLA Domains), global search, compliance, analytics, orchestration
  Data plane (local):   Rubrik clusters / cloud storage hold the actual immutable snapshots
  Rubrik Backup Service (RBS): lightweight connector on hosts for application-consistent backups
Manage globally from the SaaS console; data stays on your clusters/cloud (immutable, air-gapped).
EOF
```

**Expected result:** RSC as a **SaaS control plane** (policy, search, analytics) over **local immutable data** (clusters/cloud), with RBS connectors for app-consistent backups — the architecture RCSA tests. You operate one global console; the protected data lives on your infrastructure, immutable and air-gapped ([Chapter 03](03-immutability-and-air-gap.md)).

**Negative test:** Assuming the backups live in the SaaS console — they don't; the console is control/metadata, the immutable data is on your clusters/cloud. Confusing the planes is a common RCSA misconception.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] SLA Domains (policy, not per-workload jobs) internalized.
- [ ] Workload assignment and the compliance view (protected/at-risk/unprotected) drilled.
- [ ] The RSC control-plane (SaaS) vs data-plane (local immutable) split understood.
