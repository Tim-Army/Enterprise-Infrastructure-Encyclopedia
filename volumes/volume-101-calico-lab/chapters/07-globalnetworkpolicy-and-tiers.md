# Chapter 07: GlobalNetworkPolicy and Tiers

## Learning Objectives

- Complete the segmentation by protecting the OT namespace.
- Write a cluster-wide guardrail with a Calico `GlobalNetworkPolicy`, including an explicit `Deny`.
- Order policy with tiers so platform guardrails evaluate before app-team rules.
- Confirm that label-based policy survives pod restarts.

## Hands-On Lab

### Lab 7.1 — Segment the OT namespace

**Objective.** Default-deny ingress in `ot` and permit only `hmi → plc:502`, completing the two legitimate flows.

**Walkthrough**

```bash
kubectl apply -f - <<'EOF'
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata: { name: default-deny-ingress, namespace: ot }
spec: { podSelector: {}, policyTypes: [ Ingress ] }
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata: { name: allow-hmi-to-plc, namespace: ot }
spec:
  podSelector: { matchLabels: { app: plc } }
  policyTypes: [ Ingress ]
  ingress:
    - from: [ { podSelector: { matchLabels: { app: hmi } } } ]
      ports: [ { protocol: TCP, port: 502 } ]
EOF
```

**Step 2.** Validate both legitimate flows work and the unwanted ones do not:

```bash
kubectl exec -n dc web -- nc -z -w2 db.dc 5432 && echo "web -> db  ALLOWED"
kubectl exec -n ot hmi -- nc -z -w2 plc.ot 502 && echo "hmi -> plc ALLOWED"
kubectl exec -n ot hmi -- nc -z -w2 db.dc 5432 || echo "hmi -> db  BLOCKED"
kubectl exec -n dc web -- nc -z -w2 plc.ot 502 || echo "web -> plc BLOCKED"
```

**Expected result.** The two legitimate flows are ALLOWED; the two unwanted flows are BLOCKED.

**Negative test.** Delete `default-deny-ingress` in `ot` and re-run; `web → plc` reaches again, because without a default-deny the allow rules are additive over an allow-all base. Default-deny is the floor everything else builds on. Re-apply it.

**Cleanup.** Keep the OT policies.

### Lab 7.2 — A cluster-wide guardrail with GlobalNetworkPolicy

**Objective.** Add a Calico `GlobalNetworkPolicy` that protects the database *cluster-wide* with an explicit `Deny` — a platform guardrail independent of any namespace's own policy.

**Walkthrough**

**Step 1.** Create a `security` **tier** that evaluates before the default tier, then a guardrail in it:

```bash
calicoctl apply -f - <<'EOF'
apiVersion: projectcalico.org/v3
kind: Tier
metadata: { name: security }
spec: { order: 100 }
EOF
calicoctl apply -f - <<'EOF'
apiVersion: projectcalico.org/v3
kind: GlobalNetworkPolicy
metadata: { name: security.protect-db }
spec:
  tier: security
  order: 10
  selector: app == 'db'
  types: [ Ingress ]
  ingress:
    - action: Allow
      source: { selector: app == 'web' }
      destination: { ports: [ 5432 ] }
    - action: Deny
EOF
```

**Step 2.** Confirm the guardrail is enforced cluster-wide — even if someone later writes a permissive namespace policy, the `security` tier's explicit `Deny` wins because it evaluates first:

```bash
kubectl exec -n ot hmi -- nc -z -w2 db.dc 5432 || echo "hmi -> db DENIED by the security tier"
kubectl exec -n dc web -- nc -z -w2 db.dc 5432 && echo "web -> db still ALLOWED"
```

**Expected result.** Only `app=web` may reach `app=db:5432` anywhere in the cluster; everything else is denied by the tiered guardrail. This is the capability standard Kubernetes NetworkPolicy lacks: cluster-wide scope, explicit `Deny`, and ordered evaluation.

> **Caution.** A `GlobalNetworkPolicy` with `selector: all()` and a blanket `Deny` will also cut off DNS and the Kubernetes control plane unless you allow them; that can break the cluster. This guardrail selects only `app == 'db'`, so it is safe. When you do write an all-selecting deny, always allow `kube-system` and UDP/TCP 53 first, and rely on Calico's failsafe ports.

**Negative test.** Write a permissive namespace `NetworkPolicy` allowing everything to `db`, then re-test `hmi → db`; it stays denied, because the `security` tier is evaluated before the default tier. Tiers are how a platform team keeps guardrails an app team cannot accidentally override.

**Cleanup.** Keep the guardrail.

### Lab 7.3 — Policy survives pod restart

**Objective.** Prove that label-based policy keeps working when pods reschedule and change IP.

**Walkthrough**

**Step 1.** Delete the `db` pod so Kubernetes recreates it with a new IP:

```bash
kubectl delete pod -n dc -l app=db
kubectl rollout status -n dc deploy/db
kubectl get pod -n dc -l app=db -o wide     # note the new IP
```

**Step 2.** Re-test the flows:

```bash
kubectl exec -n dc web -- nc -z -w2 db.dc 5432 && echo "web -> db ALLOWED (new IP, same label)"
kubectl exec -n ot hmi -- nc -z -w2 db.dc 5432 || echo "hmi -> db STILL BLOCKED"
```

**Expected result.** Policy still works despite the new pod IP — because it selects on the label `app=db`, not an address. This is the property that makes label-based policy the only sane choice in Kubernetes, where pod IPs are ephemeral.

**Negative test.** Imagine you had written the rule against the old pod IP. After this restart it would either fail open (allow a new pod that reused the IP) or fail closed (block the legitimate db). Labels avoid both.

**Cleanup.** Keep everything for Chapter 08.

## Summary and Completion Checklist

- [ ] OT namespace segmented; both legitimate flows work, both unwanted flows blocked.
- [ ] A tiered `GlobalNetworkPolicy` guardrail protects the database cluster-wide with an explicit `Deny`.
- [ ] The DNS/kube-system caution for all-selecting deny understood.
- [ ] Policy shown to survive a pod restart because it is label-based.
