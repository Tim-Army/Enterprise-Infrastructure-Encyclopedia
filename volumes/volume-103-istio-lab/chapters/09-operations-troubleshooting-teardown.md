# Chapter 09: Operations, Troubleshooting, and Teardown

## Learning Objectives

- Work a structured troubleshooting playbook for Istio policy.
- Rehearse a safe rollback.
- Tear the cluster down cleanly.

## Hands-On Lab

### Lab 9.1 — Troubleshooting playbook

**Objective.** Diagnose the three failure modes you are most likely to hit.

**Walkthrough.**

**Symptom 1 — a pod is not in the mesh.** It shows `1/1` instead of `2/2`. Confirm the namespace label and that the pod was created *after* labeling:

```bash
kubectl get ns -L istio-injection
kubectl get pods -n dc -o wide          # 2/2 = meshed; 1/1 = no sidecar
```

Recreate pods (`kubectl rollout restart deploy -n dc`) after labeling a namespace.

**Symptom 2 — a legitimate call returns 403.** The AuthorizationPolicy denied it. Check the principal and the L7 operation:

```bash
istioctl x describe pod -n dc "$(kubectl get pod -n dc -l app=api -o jsonpath='{.items[0].metadata.name}')"
kubectl get authorizationpolicy -A
```

A `403` from the sidecar is policy working; the usual cause is the wrong principal string (namespace or ServiceAccount) or an unmatched method/path.

**Symptom 3 — mesh traffic broke after STRICT mTLS.** Something is talking plaintext to a meshed service (often a non-injected client, or a probe). Confirm and, for a genuinely un-meshed destination like the PLC, add a `DestinationRule` with `tls.mode: DISABLE`.

**Expected result.** Each symptom maps to a first check: injection, principal/operation, or an mTLS mismatch.

**Negative test.** "Fix" a 403 by deleting the AuthorizationPolicy. You removed the authorization to make a denied request pass — which was the abuse. Fix the principal or the operation instead.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 9.2 — Safe rollback

**Objective.** Restore connectivity fast.

**Walkthrough.**

- **Undo one authorization:** `kubectl delete authorizationpolicy -n <ns> <name>`.
- **Back to permissive mTLS:** set the `PeerAuthentication` mode to `PERMISSIVE` (mesh accepts plaintext again) — a quick way to rule out mTLS as the cause.
- **Undo egress confinement:** `kubectl delete sidecar -n ot hmi-egress`.

**Step 1.** Practice loosening mTLS to isolate a problem, then restore STRICT:

```bash
kubectl patch peerauthentication default -n istio-system --type merge -p '{"spec":{"mtls":{"mode":"PERMISSIVE"}}}'
# ...test...
kubectl patch peerauthentication default -n istio-system --type merge -p '{"spec":{"mtls":{"mode":"STRICT"}}}'
```

**Expected result.** You can toggle enforcement without deleting your identity or policy model.

**Negative test.** Leaving the mesh in PERMISSIVE "to be safe" removes the mTLS guarantee — plaintext to meshed services is accepted again. Restore STRICT when done.

**Rollback.** Ensure STRICT mTLS is restored.

### Lab 9.3 — Teardown

**Objective.** Remove the cluster.

**Walkthrough.**

```bash
kind delete cluster --name istio-lab
docker ps -a | grep istio-lab || echo "no lab containers remain"
```

Optionally remove the `kind`, `kubectl`, and `istioctl` binaries.

**Expected result.** The cluster and its containers are gone.

**Negative test.** Deleting the kind containers by hand leaves metadata behind; a later recreate may conflict. Use `kind delete cluster`.

**Rollback.** Host restored.

## Summary and Completion Checklist

- [ ] Troubleshooting playbook worked against a real symptom.
- [ ] Safe rollback rehearsed (mTLS toggle, policy delete).
- [ ] Cluster deleted with `kind delete cluster`.

## Where to go next

This lab built service-mesh segmentation with Istio — mTLS, SPIFFE identity, and L7 AuthorizationPolicy — entirely from open source, and showed the mesh's boundary. To place it among the alternatives, including the lighter-weight mesh Linkerd and the multi-platform Consul, see [Volume LXXXVII, Microsegmentation Options](../../volume-087-microsegmentation-options/README.md), whose Chapter 15 comparison matrix links each option to its own build-it-yourself lab in this series.
