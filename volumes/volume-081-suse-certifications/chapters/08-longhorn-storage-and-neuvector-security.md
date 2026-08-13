# Chapter 08: Longhorn Storage and NeuVector Security

## Learning Objectives

- Provide persistent storage to Kubernetes with Longhorn.
- Understand replication, snapshots, and backups.
- Secure containers with NeuVector.
- Apply defensive runtime and network policy.
- Complete a walkthrough for each storage/security topic.

## Theory and Architecture

Two SUSE cloud-native products complete the stack. **Longhorn** is a **cloud-native block storage**
system for Kubernetes — it provides **persistent volumes** backed by distributed, **replicated**
storage across cluster nodes, with **snapshots** and scheduled **backups** to external targets (S3/
NFS). It gives stateful workloads (databases, queues) reliable storage without a separate SAN.
**NeuVector** is SUSE's **container security** platform — a full-lifecycle, **defensive** tool that
scans images for vulnerabilities, enforces admission control, and — its signature capability —
provides **runtime protection** with automatically-learned **network segmentation** (a zero-trust
allow-list of expected container connections) plus process and file monitoring, detecting and blocking
anomalous behavior inside running containers. Together, Longhorn keeps stateful workloads durable and
NeuVector keeps them secure — the persistence and defense layers of the SUSE Kubernetes platform. This
chapter teaches each with a hands-on walkthrough (persistent-volume reasoning, replication/backup, and
defensive NeuVector policy).

> **Scope.** NeuVector is a defensive container-security platform. Every lab is **authorized
> protection** — scanning, segmenting, and monitoring your own clusters — never an attack.

## Design Considerations

Use **Longhorn** for replicated persistent volumes; schedule **snapshots and backups** offsite. Right-
size **replica count** for durability. Secure with **NeuVector**: scan images (shift-left), enforce
**admission control**, and use learned **network segmentation** (zero-trust) plus runtime monitoring.
Prioritize protecting **internet-facing** workloads.

## Implementation and Automation

The labs provision a persistent volume, plan backups, and apply NeuVector policy.

## Validation and Troubleshooting

Confirm the storage/security model:

```text
Longhorn = cloud-native replicated block storage for K8s (persistent volumes + snapshots + scheduled backups to S3/NFS). NeuVector = defensive container security: image scan + admission control + runtime protection (learned zero-trust network segmentation + process/file monitoring).
Longhorn = durable stateful workloads; NeuVector = secure them.
```

Common pitfalls: single-replica Longhorn volumes (no redundancy); and NeuVector in **discover** mode
forever (never enforcing the learned zero-trust policy).

## Security and Best Practices

Replicate and **back up** Longhorn volumes offsite, scan images and enforce **admission control** with
NeuVector, and move learned **network segmentation** to enforce. Protect internet-facing workloads
first. All work is defensive.

## Hands-On Lab

Storage/security walkthroughs. **Shared prerequisites** — a K3s/RKE2 cluster (or `python3` to model
logic). **Cost:** none.

### Lab 8.1 — Provision a persistent volume (Longhorn)

**Objective:** Durable storage for a stateful app.

```python
python3 - <<'PY'
pvc={"name":"db-data","storageClass":"longhorn","size":"20Gi","accessMode":"ReadWriteOnce","replicas":3}
for k,v in pvc.items(): print(f"{k:12}: {v}")
print("Longhorn: a PVC with storageClass=longhorn -> replicated persistent volume (3 replicas)")
PY
```

**Expected result:** a **PersistentVolumeClaim** backed by replicated Longhorn storage — durable
Kubernetes persistence.

**Negative test:** store database data on an **emptyDir**; it's lost when the pod moves — use a
**Longhorn PVC**.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.2 — Plan replication and backups

**Objective:** Survive node and cluster loss.

```python
python3 - <<'PY'
plan={"replicas":"3 (survive node failure)","snapshots":"hourly (fast local recovery)",
      "backups":"daily to S3 (survive cluster loss)","restore_test":"quarterly"}
for k,v in plan.items(): print(f"{k:13}: {v}")
print("Longhorn: replicas for node failure + offsite backups for cluster disaster; test restores")
PY
```

**Expected result:** a **replication + backup** plan — durable, recoverable storage.

**Negative test:** rely on replicas alone; a whole-cluster loss takes all replicas — add **offsite
backups**.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.3 — Apply NeuVector network segmentation

**Objective:** Zero-trust runtime protection.

```python
python3 - <<'PY'
learned_policy={"web -> app":"allow (tcp 8080, observed)","app -> db":"allow (tcp 5432, observed)",
                "web -> db":"DENY (never observed)","any -> internet:4444":"DENY (unexpected)"}
for conn,rule in learned_policy.items(): print(f"{conn:22}: {rule}")
print("NeuVector: learns expected connections -> enforces a zero-trust allow-list (blocks the rest)")
PY
```

**Expected result:** NeuVector's **learned zero-trust segmentation** allowing expected and denying
unexpected connections — defensive runtime protection.

**Negative test:** leave NeuVector in **discover** mode indefinitely; it never enforces — promote the
learned policy to **protect** mode.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.4 — Scan an image (shift-left)

**Objective:** Catch vulnerabilities before deploy.

```python
python3 - <<'PY'
image={"name":"app:2.1","base":"suse/bci-base","critical_vulns":1,"admission":"block if critical"}
decision="BLOCK (admission control: critical vuln)" if image["critical_vulns"]>0 else "allow"
print("image:", image["name"], "->", decision)
print("NeuVector: scan images + admission control -> stop vulnerable images at deploy")
PY
```

**Expected result:** a vulnerable image **blocked** by admission control — NeuVector shift-left
security.

**Negative test:** scan only running containers; the vulnerable image already deployed — scan and gate
at **admission**.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Longhorn provides replicated, backed-up persistent storage for stateful Kubernetes workloads, and
NeuVector secures them defensively with image scanning, admission control, and learned zero-trust
runtime segmentation — persistence and defense for the SUSE Kubernetes platform.

- [ ] I can provision a Longhorn persistent volume.
- [ ] I can plan replication and backups.
- [ ] I can apply NeuVector network segmentation.
- [ ] I can scan an image and gate at admission.
- [ ] I completed Labs 8.1–8.4 including each negative test.
