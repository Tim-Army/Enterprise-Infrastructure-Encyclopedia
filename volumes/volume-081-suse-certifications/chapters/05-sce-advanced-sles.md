# Chapter 05: SCE — Advanced SLES

## Learning Objectives

- Build a high-availability cluster (Pacemaker/Corosync).
- Automate installation with AutoYaST.
- Understand transactional-update and SLE Micro.
- Apply advanced engineering practices.
- Complete a walkthrough for each SCE advanced topic.

## Theory and Architecture

The **SUSE Certified Engineer (SCE)** validates advanced SLES engineering. **High Availability** is
built with the **SUSE Linux Enterprise High Availability Extension** — **Corosync** provides cluster
membership and messaging, and **Pacemaker** is the resource manager that starts, stops, and fails over
**resources** (services, IPs, storage) across nodes with fencing (STONITH) for safety — the way SLES
runs critical services without single points of failure. **AutoYaST** automates installation: an XML
**profile** describes the entire system (partitioning, packages, network, users), enabling
**unattended, repeatable** deployments at scale. **transactional-update** and **SLE Micro** represent
SUSE's **immutable/transactional** direction: the OS is read-only, updates are applied
**atomically** into a new snapshot and activated on reboot (with easy rollback) — ideal for edge and
container hosts. These advanced capabilities — clustering, automated deployment, and transactional
updates — distinguish the SCE. This chapter teaches each with a hands-on walkthrough (cluster reasoning,
AutoYaST profiles, transactional updates).

## Design Considerations

Build **HA clusters** with Corosync/Pacemaker and **fencing** for critical services. Automate
deployment with **AutoYaST** profiles for consistency at scale. Use **transactional-update / SLE
Micro** for immutable edge/container hosts (atomic updates + rollback). Test failover. Standardize
configuration.

## Implementation and Automation

The labs reason about a cluster, outline an AutoYaST profile, and use transactional-update.

## Validation and Troubleshooting

Confirm the advanced model:

```text
HA: Corosync (membership/messaging) + Pacemaker (resource manager: start/stop/failover + STONITH fencing). AutoYaST: XML profile -> unattended repeatable install.
transactional-update / SLE Micro: read-only OS, atomic updates into a new snapshot, activate on reboot, easy rollback (edge/container hosts).
```

Common pitfalls: an HA cluster with **no fencing** (split-brain risk); and manual installs at scale
(inconsistent — use **AutoYaST**).

## Security and Best Practices

Build **HA** with fencing, automate with **AutoYaST**, and use **transactional-update** for immutable
hosts with atomic updates and rollback. Test failover. All work is authorized engineering.

## Hands-On Lab

Advanced walkthroughs. **Shared prerequisites** — a SLES VM (or read commands), `python3`. **Cost:**
none.

### Lab 5.1 — Reason about a Pacemaker cluster

**Objective:** Understand HA resource management.

```python
python3 - <<'PY'
cluster={"nodes":["node1","node2"],"corosync":"membership + messaging (heartbeat)",
         "pacemaker_resources":["virtual-ip","filesystem","service"],"fencing":"STONITH (avoid split-brain)"}
for k,v in cluster.items(): print(f"{k:20}: {v}")
print("SCE HA: Pacemaker moves resources to a healthy node on failure; STONITH prevents split-brain")
PY
```

**Expected result:** the **Corosync/Pacemaker** cluster with fencing — SLES high availability.

**Negative test:** build a 2-node cluster with **no fencing**; a network partition risks split-brain
(both active) — configure **STONITH**.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.2 — Outline an AutoYaST profile

**Objective:** Automate installation.

```python
python3 - <<'PY'
profile={"partitioning":"btrfs root + xfs /data","packages":["pattern:base","zypper","salt-minion"],
         "network":"static or DHCP","users":"admin + ssh keys","scripts":"post-install registration"}
for k,v in profile.items(): print(f"{k:13}: {v}")
print("AutoYaST: one XML profile -> identical, unattended installs across many machines")
PY
```

**Expected result:** an **AutoYaST** profile describing a full system — repeatable deployment.

**Negative test:** install 50 servers by hand; they drift — use one **AutoYaST** profile.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.3 — Use transactional-update

**Objective:** Atomic, rollback-safe updates.

```bash
transactional-update --help 2>/dev/null | head -3 || echo "transactional-update: apply updates atomically into a new snapshot; activate on reboot"
echo "SLE Micro: read-only OS; 'transactional-update pkg install' -> new snapshot -> reboot -> rollback if needed"
```

**Expected result:** the **transactional-update** model (atomic snapshot + reboot) — immutable-host
updates.

**Negative test:** patch a read-only SLE Micro host with plain `zypper`; use **transactional-update**
for the atomic/rollback workflow.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.4 — Plan a failover test

**Objective:** Validate HA works.

```python
python3 - <<'PY'
test=["cluster healthy: resources on node1","simulate: stop node1 (or fence it)",
      "Pacemaker moves virtual-ip + service to node2","verify service reachable","restore node1, rebalance"]
for i,s in enumerate(test,1): print(f"{i}. {s}")
print("SCE: test failover regularly — an untested cluster is not proven HA")
PY
```

**Expected result:** a **failover test** proving resources move to a healthy node — validated HA.

**Negative test:** assume HA works without testing; failover may be misconfigured — **test** it.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The SCE adds advanced SLES engineering — Corosync/Pacemaker high-availability clustering with fencing,
AutoYaST automated deployment, and transactional-update/SLE Micro immutable hosts — distinguishing the
engineer from the administrator.

- [ ] I can reason about a Pacemaker cluster.
- [ ] I can outline an AutoYaST profile.
- [ ] I can use transactional-update.
- [ ] I can plan a failover test.
- [ ] I completed Labs 5.1–5.4 including each negative test.
