# Chapter 08: The Mesh Boundary

## Learning Objectives

- Understand what a service mesh cannot do: enforce on a workload outside the mesh.
- Confine a compromised meshed client's egress with a `Sidecar` resource.
- Pair the mesh with a CNI NetworkPolicy to protect non-mesh endpoints.

## The problem restated

Every other lab in this series ends by protecting the agentless PLC. Istio's honest answer is different and worth stating plainly: **a service mesh secures the workloads that are in the mesh.** The PLC runs no sidecar, so Istio has no proxy to carry its identity, no mTLS to it, and no place to enforce an `AuthorizationPolicy` *on* it. This is not a flaw to hide — it is the shape of the tool, and knowing it is the point of this chapter.

## Hands-On Lab

### Lab 8.1 — The mesh does not enforce on the un-meshed PLC

**Objective.** Confirm that an `AuthorizationPolicy` selecting the PLC has no effect, because there is no sidecar to enforce it.

**Walkthrough**

```bash
kubectl apply -f - <<'EOF'
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata: { name: try-protect-plc, namespace: ot }
spec:
  selector: { matchLabels: { app: plc } }
  action: DENY
  rules: [ { from: [ { source: { namespaces: [ "*" ] } } ] } ]
EOF
kubectl exec -n dc deploy/web -c web -- nc -z -w2 plc.ot 502 && echo "web STILL reached the PLC — the policy did nothing"
```

**Expected result.** The connection to the PLC **still succeeds** despite a DENY policy — because the PLC has no sidecar to apply it. A service mesh cannot secure what it does not proxy.

**Negative test.** Assume adding the mesh protected every workload. It protected only the meshed ones; the PLC was never in the mesh. Delete the ineffective policy: `kubectl delete authorizationpolicy -n ot try-protect-plc`.

**Rollback.** Deleted above.

### Lab 8.2 — Confine the compromised client's egress with a Sidecar resource

**Objective.** Since you cannot enforce *on* the PLC, constrain what the meshed HMI may reach *from* the mesh — so a compromised HMI cannot pivot to the database even if its identity policy were misconfigured.

**Walkthrough**

```bash
kubectl apply -f - <<'EOF'
apiVersion: networking.istio.io/v1
kind: Sidecar
metadata: { name: hmi-egress, namespace: ot }
spec:
  workloadSelector: { labels: { app: hmi } }
  egress:
    - hosts:
        - "ot/plc.ot.svc.cluster.local"
        - "istio-system/*"
        - "kube-system/*"
EOF
```

**Step 2.** Validate: the HMI reaches the PLC (its one allowed egress) but its sidecar has no route to the database at all:

```bash
kubectl exec -n ot deploy/hmi -c hmi -- nc -z -w2 plc.ot 502 && echo "hmi -> plc  ALLOWED (egress host)"
kubectl exec -n ot deploy/hmi -c hmi -- nc -z -w2 db.dc 5432 || echo "hmi -> db   BLOCKED at the sidecar (not in egress hosts)"
```

**Expected result.** `hmi → plc` works; `hmi → db` is blocked *before authorization even applies*, because the HMI's sidecar is configured to know only about the PLC and system namespaces. This is defense in depth: the db AuthorizationPolicy denies by identity, and the Sidecar egress denies by reachability.

**Negative test.** Widen the egress `hosts` to `"*/*"` and the HMI can again route to the database (where the AuthorizationPolicy then denies it). The Sidecar resource is the egress half of the control; keep it tight.

**Rollback.** Keep the Sidecar resource.

### Lab 8.3 — Pair the mesh with a CNI NetworkPolicy (defense in depth)

**Objective.** Recognize that fully protecting a non-mesh endpoint like the PLC needs a control that operates below the mesh — a CNI NetworkPolicy.

**Design Exercise.** The mesh cannot enforce on the PLC. Write the Kubernetes `NetworkPolicy` (as in the Calico lab) you would apply to protect the PLC pod so that only the `hmi` pod may reach `:502` — a control that works because it operates at the network layer, beneath the mesh. Explain why running Istio *and* a CNI policy engine together (Calico or Cilium plus Istio) is the common production pattern: the mesh secures service-to-service with identity and L7, and the CNI secures everything, meshed or not, at L3/L4.

**Model answer (sketch).**

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata: { name: protect-plc, namespace: ot }
spec:
  podSelector: { matchLabels: { app: plc } }
  policyTypes: [ Ingress ]
  ingress:
    - from: [ { podSelector: { matchLabels: { app: hmi } } } ]
      ports: [ { protocol: TCP, port: 502 } ]
```

This protects the PLC at the network layer regardless of the mesh, because the CNI enforces it on the pod's traffic directly. The mesh and the CNI are complementary, not alternatives.

**Expected result.** A clear understanding of the mesh boundary and why meshes are paired with network policy.

**Negative test.** Argue the mesh alone is sufficient. It is not, for anything that cannot join the mesh — which in real estates includes OT, appliances, and legacy systems.

**Rollback.** No NetworkPolicy applied here (the CNI beneath kind may not enforce it); the exercise is the deliverable.

## Summary and Completion Checklist

- [ ] Confirmed the mesh cannot enforce on the un-meshed PLC.
- [ ] The HMI's egress confined with a `Sidecar` resource.
- [ ] The mesh-plus-CNI defense-in-depth pattern reasoned through.
- [ ] You can explain the boundary of a service mesh.
