# Chapter 07: L3/L4 CiliumNetworkPolicy

## Learning Objectives

- Segment the database and PLC with identity-based `CiliumNetworkPolicy`.
- Confirm drops in Hubble.
- Add a cluster-wide guardrail and confirm policy follows identity.

Start at Layer 3/4 — the same job Calico does — then Chapter 08 goes where only Cilium can, to Layer 7.

## Hands-On Lab

### Lab 7.1 — Segment the database and the PLC

**Objective.** Permit only `web → db:5432` and `hmi → plc:502`; deny everything else into those endpoints.

**Walkthrough**

**Step 1.** Apply the two ingress policies. In Cilium, once a policy selects an endpoint for ingress, that endpoint **default-denies** all other ingress — so these two rules both allow the legitimate flow and deny the rest:

```bash
kubectl apply -f - <<'EOF'
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata: { name: allow-web-to-db, namespace: dc }
spec:
  endpointSelector: { matchLabels: { app: db } }
  ingress:
    - fromEndpoints: [ { matchLabels: { app: web } } ]
      toPorts: [ { ports: [ { port: "5432", protocol: TCP } ] } ]
---
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata: { name: allow-hmi-to-plc, namespace: ot }
spec:
  endpointSelector: { matchLabels: { app: plc } }
  ingress:
    - fromEndpoints: [ { matchLabels: { app: hmi } } ]
      toPorts: [ { ports: [ { port: "502", protocol: TCP } ] } ]
EOF
```

**Step 2.** Validate, and watch the drop in Hubble:

```bash
kubectl exec -n dc web -- nc -z -w2 db.dc 5432 && echo "web -> db  ALLOWED"
kubectl exec -n ot hmi -- nc -z -w2 plc.ot 502 && echo "hmi -> plc ALLOWED"
kubectl exec -n ot hmi -- nc -z -w2 db.dc 5432 || echo "hmi -> db  BLOCKED"
hubble observe --to-pod dc/db --verdict DROPPED | tail -3
```

**Expected result.** The two legitimate flows are ALLOWED; `hmi → db` is BLOCKED, and Hubble shows the DROPPED verdict with the `ot/hmi → dc/db` identities. The Chapter 05 lateral movement is dead, and you can *see* it being denied.

**Negative test.** Change `fromEndpoints` on the db policy to `matchLabels: {}` ("any endpoint"); the app works but so would the operator. Least privilege names the source identity. Revert to `app: web`.

**Cleanup.** Keep the policies.

### Lab 7.2 — Policy follows identity across a restart

**Objective.** Prove label-derived identity survives a pod IP change.

**Walkthrough**

```bash
kubectl delete pod -n dc -l app=db
kubectl rollout status -n dc deploy/db
kubectl exec -n dc web -- nc -z -w2 db.dc 5432 && echo "web -> db ALLOWED (new IP, same identity)"
kubectl exec -n ot hmi -- nc -z -w2 db.dc 5432 || echo "hmi -> db STILL BLOCKED"
```

**Expected result.** Policy still works after the db pod's IP changed, because Cilium enforces on the label-derived identity, not the address.

**Negative test.** An IP-based rule would have broken here. Identity avoids that entirely.

**Cleanup.** Keep everything.

### Lab 7.3 — A cluster-wide guardrail

**Objective.** Add a `CiliumClusterwideNetworkPolicy` — a guardrail not scoped to any namespace.

**Walkthrough**

```bash
kubectl apply -f - <<'EOF'
apiVersion: cilium.io/v2
kind: CiliumClusterwideNetworkPolicy
metadata: { name: protect-db-clusterwide }
spec:
  endpointSelector:
    matchLabels: { app: db, k8s:io.kubernetes.pod.namespace: dc }
  ingress:
    - fromEndpoints: [ { matchLabels: { app: web, k8s:io.kubernetes.pod.namespace: dc } } ]
      toPorts: [ { ports: [ { port: "5432", protocol: TCP } ] } ]
EOF
kubectl exec -n ot hmi -- nc -z -w2 db.dc 5432 || echo "hmi -> db DENIED cluster-wide"
```

**Expected result.** The database is protected cluster-wide by identity — a platform guardrail independent of the namespace policy. Two independent controls now guard it.

> **Note.** `CiliumClusterwideNetworkPolicy` is not namespaced, so its selectors must include the namespace label (`k8s:io.kubernetes.pod.namespace`) to be precise. A cluster-wide *default-deny* would also need to allow DNS and kube-system; this guardrail selects only `app=db`, so it is safe.

**Negative test.** Write a permissive namespace policy allowing everything to `db`; the cluster-wide guardrail still denies the operator, because both must allow for traffic to pass. Defense in depth.

**Cleanup.** Keep the guardrail for Chapter 08.

## Summary and Completion Checklist

- [ ] `web → db` and `hmi → plc` allowed by identity; `hmi → db` blocked and seen DROPPED in Hubble.
- [ ] Policy shown to follow identity across a pod restart.
- [ ] A `CiliumClusterwideNetworkPolicy` guardrail protects the database.
