# Chapter 05: The Flat Cluster and Lateral Movement

## Learning Objectives

- Establish and record baseline pod-to-pod reachability.
- Prove that a default Kubernetes network permits lateral movement.
- Frame the legitimate flows so later policy has a specification.

## Hands-On Lab

### Lab 5.1 — Baseline reachability

**Objective.** Measure what talks to what before any policy. In Kubernetes, the default is **allow all** — any pod may reach any other.

**Walkthrough**

**Step 1.** From `web` (in `dc`), probe the database and the PLC:

```bash
kubectl exec -n dc web -- nc -z -w2 db.dc 5432 && echo "web -> db:5432 REACH"
kubectl exec -n dc web -- nc -z -w2 plc.ot 502 && echo "web -> plc:502 REACH"
```

**Step 2.** From `hmi` (in `ot`), probe the PLC and — the lateral-movement path — the database:

```bash
kubectl exec -n ot hmi -- nc -z -w2 plc.ot 502  && echo "hmi -> plc:502 REACH"
kubectl exec -n ot hmi -- nc -z -w2 db.dc 5432  && echo "hmi -> db:5432 REACH"
```

**Expected result.** All four probes print **REACH**. The cluster is flat: namespaces are an organizational boundary, not a security boundary, until a NetworkPolicy says otherwise.

**Negative test.** Look for a namespace that blocks cross-namespace traffic by default — there is none. Kubernetes namespaces do not isolate network traffic on their own; that is a common and dangerous misconception this lab corrects.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.2 — Identify the legitimate flows

**Objective.** Write down the only two flows the application needs.

**Walkthrough**

| # | Source (label) | Destination (label) | Port | Legitimate? |
|:--|:--|:--|:--|:--|
| 1 | web (`app=web`, ns dc) | db (`app=db`, ns dc) | 5432 | **Yes** |
| 2 | hmi (`app=hmi`, ns ot) | plc (`app=plc`, ns ot) | 502 | **Yes** |
| 3 | hmi (`app=hmi`, ns ot) | db (`app=db`, ns dc) | 5432 | **No** (lateral movement) |
| 4 | web (`app=web`, ns dc) | plc (`app=plc`, ns ot) | 502 | **No** |

**Expected result.** Two legitimate flows, expressed by **label**, which is exactly how Calico policy will select them.

**Negative test.** Express the policy by pod IP instead of label. Pod IPs change on every restart in Kubernetes, so an IP-based rule breaks the first time a pod reschedules. Policy must be label-based.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.3 — Reproduce lateral movement

**Objective.** Show that a compromised operator pod can reach and read the crown-jewel database.

**Walkthrough**

**Step 1.** Treat `hmi` as compromised. It already reached `db:5432` in Lab 5.1. Now read data with the app credentials an attacker would harvest:

```bash
kubectl exec -n ot hmi -- sh -c \
  "PGPASSWORD='LabAppPassw0rd!' psql -h db.dc -U postgres -d cwlab -c 'SELECT 1;' 2>/dev/null || nc -z -w2 db.dc 5432 && echo 'hmi reached the database'"
```

**Expected result.** The operator pod reaches the database across namespaces — a full lateral-movement path that nothing currently stops.

**Negative test.** Re-run the legitimate `web → db` probe; it also works, over the same flat network. The cluster cannot tell the app tier from the operator until Calico policy gives it labels to enforce on.

**Rollback.** None — Chapter 06 begins closing this down.

## Summary and Completion Checklist

- [ ] Baseline shows all four probes REACH (Kubernetes default allow-all).
- [ ] The two legitimate flows written down by label.
- [ ] Lateral movement from `hmi` to `db` reproduced across namespaces.
- [ ] You can state the goal: allow flows 1 and 2 by label, deny the rest.
