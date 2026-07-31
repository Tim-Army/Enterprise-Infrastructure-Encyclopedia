# Chapter 08: The Mesh Boundary

## Learning Objectives

- Confirm Linkerd cannot enforce on the un-meshed PLC.
- Set a namespace default-inbound-policy to deny by default.
- Pair the mesh with a CNI NetworkPolicy for non-mesh endpoints.

## The problem restated

As with Istio, Linkerd secures the workloads that are **in the mesh**. The PLC runs no proxy, so it has no identity, no mTLS, and no place for a `Server` or `AuthorizationPolicy` to take effect. The honest conclusion is the same: a mesh protects meshed workloads, and a device that cannot join the mesh needs a control beneath it.

## Hands-On Lab

### Lab 8.1 — The mesh does not enforce on the un-meshed PLC

**Objective.** Confirm a `Server`/`AuthorizationPolicy` for the PLC has no effect.

**Walkthrough**

```bash
kubectl apply -f - <<'EOF'
apiVersion: policy.linkerd.io/v1beta1
kind: Server
metadata: { name: plc, namespace: ot }
spec: { podSelector: { matchLabels: { app: plc } }, port: 502, proxyProtocol: opaque }
EOF
kubectl exec -n dc deploy/web -c web -- nc -z -w2 plc.ot 502 && echo "web STILL reached the PLC — the Server did nothing (no proxy on the PLC)"
```

**Expected result.** The connection still succeeds despite the `Server`, because the PLC has no proxy to enforce it. A mesh cannot secure what it does not proxy. Delete the ineffective Server: `kubectl delete server -n ot plc`.

**Negative test.** Assume meshing the namespace protected the PLC. It did not — the PLC was explicitly excluded from injection and could not run a proxy anyway.

**Cleanup.** Server deleted above.

### Lab 8.2 — Default-deny inbound for a namespace

**Objective.** Use Linkerd's `default-inbound-policy` to make meshed workloads deny by default without a `Server` per port — a broad guardrail.

**Walkthrough**

```bash
kubectl annotate namespace dc config.linkerd.io/default-inbound-policy=deny --overwrite
kubectl rollout restart deploy -n dc
kubectl -n dc rollout status deploy/db
```

**Step 2.** With `dc` denying by default, only your explicit `AuthorizationPolicy` rules (from Chapter 07) permit traffic; everything else is denied even without a per-port `Server`.

```bash
kubectl exec -n dc deploy/web -c web -- nc -z -w2 db.dc 5432 && echo "web -> db  still ALLOWED (authorized)"
kubectl exec -n ot deploy/hmi -c hmi -- nc -z -w2 db.dc 5432 || echo "hmi -> db  DENIED (namespace default-deny)"
```

**Expected result.** The namespace now denies inbound by default; only authorized identities pass. This is the mesh-wide floor, analogous to a default-deny NetworkPolicy but expressed in mesh-identity terms.

> **Note.** `default-inbound-policy=deny` denies *all* unauthorized inbound to meshed pods in the namespace, including health probes from kubelet unless allowed. If probes fail, allow them with a `NetworkAuthentication` for the node CIDR or set the policy to `all-authenticated` and keep per-`Server` rules. This is the trade-off of a broad default-deny.

**Negative test.** Set the annotation to `all-unauthenticated` and the namespace allows everything again. The default-inbound-policy is the switch between allow-first and deny-first for the whole namespace.

**Cleanup.** Keep the deny policy, or revert to `all-authenticated` if probes misbehave in your cluster.

### Lab 8.3 — Pair the mesh with a CNI NetworkPolicy (Design Exercise)

**Objective.** Recognize that protecting the un-meshed PLC needs a control below the mesh.

**Design Exercise.** Write the Kubernetes `NetworkPolicy` you would apply so that only the `hmi` pod may reach the PLC on `:502`. Explain why running Linkerd (identity + mTLS + L7 authz for meshed services) alongside a CNI policy engine (Calico or Cilium, for L3/L4 on everything including non-mesh pods) is the standard production pattern.

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

The CNI enforces this on the PLC's traffic directly, regardless of the mesh. Mesh and CNI are complementary: the mesh brings identity and encryption to meshed services; the CNI segments everything at L3/L4.

**Expected result.** A clear understanding that a mesh needs a CNI partner for non-mesh endpoints.

**Negative test.** Argue the mesh alone suffices. It cannot protect anything that cannot join it — which in real estates includes OT and legacy systems.

**Cleanup.** No NetworkPolicy applied (kind's default CNI may not enforce it); the exercise is the deliverable.

## Summary and Completion Checklist

- [ ] Confirmed the mesh cannot enforce on the un-meshed PLC.
- [ ] Namespace `default-inbound-policy=deny` set as a broad guardrail (with the probe caveat understood).
- [ ] The mesh-plus-CNI defense-in-depth pattern reasoned through.
