# Chapter 08: CCSC and Distributed Deployment

## Learning Objectives

- Explain the CCSC (partner) certification and its prerequisites.
- Describe the distributed leader/worker architecture.
- Manage worker groups and commit/deploy.
- Plan a production deployment.
- Complete a walkthrough for each deployment topic.

## Theory and Architecture

The **Cribl Certified Service Consultant (CCSC)** is the **partner-only** top credential —
it validates **deployment readiness** across the whole portfolio and requires all prior
certs (CC User, both Admin, CC Engineer). Its practical foundation is the **distributed
deployment**: a **Leader** node manages configuration and distributes it to **Worker
Groups** (clusters of Worker Processes that do the actual data processing), with Edge
**Fleets** managed the same way. Config changes are **committed** (versioned, Git-backed)
and **deployed** to worker groups. Deployment planning covers sizing (workers per
throughput), high availability, and upgrade strategy.

## Design Considerations

Run a **Leader + Worker Groups** for production, separate groups by function/environment,
**commit** changes (Git-backed versioning) and **deploy** deliberately, and size worker
processes to data throughput. Plan HA for the Leader and rolling upgrades.

## Implementation and Automation

The labs cover worker groups, commit/deploy, and deployment sizing.

## Validation and Troubleshooting

Confirm the model:

```text
Distributed: Leader (config mgmt) -> Worker Groups (Worker Processes process data). Edge Fleets similar.
Commit (Git-backed versioning) -> Deploy to groups. Size workers to throughput; plan HA + upgrades.
```

Common pitfalls: editing worker config directly instead of via the **Leader**; and deploying
without a **commit**.

## Security and Best Practices

Manage via the **Leader**, **commit** (versioned) before **deploy**, size **worker groups**
to throughput, plan **Leader HA** and rolling upgrades, and secure Leader↔worker with TLS.
Test config on a group before fleet-wide deploy.

## Hands-On Lab

Deployment walkthroughs. **Shared prerequisites** — a distributed Cribl (Leader + workers)
or the patterns; `$CRIBL`/`$CRIBL_TOKEN`. **Cost:** none.

### Lab 8.1 — List worker groups

**Objective:** Enumerate worker groups.

```bash
curl -sS -H "Authorization: Bearer $CRIBL_TOKEN" "$CRIBL/api/v1/master/groups" \
  | python3 -c "import sys,json;print('worker groups:',[g.get('id') for g in json.load(sys.stdin).get('items',[])])" 2>/dev/null \
  || echo "list groups via the Leader / Manage Worker Groups"
```

**Expected result:** the **worker groups** managed by the Leader — the distributed topology.

**Negative test:** run one big group for all workloads; **separate groups** by function/
environment for isolation.

**Rollback:** none (read-only).

### Lab 8.2 — Commit configuration

**Objective:** Version a config change.

```bash
curl -sS -H "Authorization: Bearer $CRIBL_TOKEN" -H "Content-Type: application/json" \
  -X POST "$CRIBL/api/v1/version/commit" -d '{"message":"add errors pipeline","group":"default"}' 2>/dev/null \
  | python3 -c "import sys,json;print('commit:',json.load(sys.stdin).get('items',[{}])[0].get('commit','ok'))" 2>/dev/null \
  || echo "commit via the UI (Git-backed versioning)"
```

**Expected result:** a **commit** recorded (Git-backed) — versioned config.

**Negative test:** deploy without committing; **commit first** so changes are versioned and
reversible.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.3 — Deploy to a group

**Objective:** Push committed config to workers.

```text
# Deploy the committed config to the worker group; workers pull and apply it.
# POST /api/v1/master/groups/<group>/deploy (or Deploy in the UI).
"deploy: committed config -> worker group -> workers apply"
```

**Expected result:** the committed config **deployed** to the group's workers — the change
goes live.

**Negative test:** edit a worker's config directly on the box; changes are **overwritten**
by the next deploy — manage via the Leader.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.4 — Size the deployment

**Objective:** Plan worker capacity.

```text
# Sizing: worker processes ~ (data throughput / per-process capacity); add headroom + HA.
# e.g., 2 TB/day at ~X GB/process/day -> N processes across worker nodes; Leader HA pair.
"sizing: workers to throughput + headroom; Leader HA; rolling upgrades"
```

**Expected result:** a **sizing plan** (workers to throughput, HA, upgrades) — deployment
readiness (the CCSC focus).

**Negative test:** deploy without capacity planning; **size to throughput** or workers
saturate.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The CCSC (partner) validates deployment readiness on the distributed Leader/Worker-Group
architecture: manage via the Leader, commit (Git-backed) and deploy to worker groups, and
size for throughput/HA/upgrades. This chapter listed groups, committed, deployed, and
sized.

- [ ] I can describe the CCSC and its prerequisites.
- [ ] I can explain the Leader/Worker-Group model.
- [ ] I can commit and deploy configuration.
- [ ] I can size a distributed deployment.
- [ ] I completed Labs 8.1–8.4 including each negative test.
