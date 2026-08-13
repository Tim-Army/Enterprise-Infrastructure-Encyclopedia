# Chapter 09: Operations, Troubleshooting, and Teardown

## Learning Objectives

- Work a structured troubleshooting playbook for Linkerd policy.
- Rehearse a safe rollback.
- Tear the cluster down cleanly.

## Hands-On Lab

### Lab 9.1 — Troubleshooting playbook

**Objective.** Diagnose the three failure modes you are most likely to hit.

**Walkthrough.**

**Symptom 1 — a pod is not in the mesh.** It shows `1/1`. Confirm the namespace annotation and recreate the pod:

```bash
kubectl get ns dc -o jsonpath='{.metadata.annotations.linkerd\.io/inject}{"\n"}'
kubectl get pods -n dc            # 2/2 = meshed
linkerd check --proxy -n dc
```

**Symptom 2 — a legitimate flow is denied.** A `Server` exists but the identity is not authorized. Check the policy and the identity string:

```bash
kubectl get server,authorizationpolicy,meshtlsauthentication -n dc
linkerd viz authz -n dc deploy/db 2>/dev/null || linkerd viz stat -n dc deploy/db
```

The usual cause is a wrong identity string (ServiceAccount or namespace) in the `MeshTLSAuthentication`, or a `Server` with no matching `AuthorizationPolicy`.

**Symptom 3 — probes fail after default-deny.** `default-inbound-policy=deny` also denies kubelet health probes. Allow them (a `NetworkAuthentication` for the node/probe source) or use `all-authenticated` with explicit `Server` rules.

**Expected result.** Each symptom maps to a first check: injection, identity/authorization, or the probe caveat.

**Negative test.** "Fix" a denied flow by deleting the `Server`. You removed the deny-by-default that protects the port. Fix the identity or add the `AuthorizationPolicy` instead.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 9.2 — Safe rollback

**Objective.** Restore connectivity fast.

**Walkthrough.**

- **Undo one Server (re-open a port):** `kubectl delete server -n dc db` (the port returns to the namespace default policy).
- **Loosen the namespace default:** `kubectl annotate ns dc config.linkerd.io/default-inbound-policy=all-authenticated --overwrite && kubectl rollout restart deploy -n dc`.
- **Inspect before removing:** `linkerd viz authz` and `linkerd viz tap` show what is being allowed/denied live, so you rarely need to delete blindly.

**Step 1.** Practice loosening the namespace default and confirming the explicit rules still hold:

```bash
kubectl annotate ns dc config.linkerd.io/default-inbound-policy=all-authenticated --overwrite
kubectl exec -n ot deploy/hmi -c hmi -- nc -z -w2 db.dc 5432 || echo "hmi -> db STILL denied by the db Server + AuthorizationPolicy"
```

**Expected result.** Even with the namespace loosened, the per-`Server` authorization still denies the operator — two layers of control. Restore `deny` when done.

**Negative test.** Delete the `Server`, the `AuthorizationPolicy`, *and* set the default to `all-unauthenticated`; the lateral movement returns. Re-apply the controls.

**Rollback.** Restore the intended policy state.

### Lab 9.3 — Teardown

**Objective.** Remove the cluster.

**Walkthrough.**

```bash
kind delete cluster --name linkerd-lab
docker ps -a | grep linkerd-lab || echo "no lab containers remain"
```

Optionally remove the `kind`, `kubectl`, and `linkerd` binaries.

**Expected result.** The cluster and its containers are gone.

**Negative test.** Deleting the kind containers by hand leaves metadata behind; a later recreate may conflict. Use `kind delete cluster`.

**Rollback.** Host restored.

## Summary and Completion Checklist

- [ ] Troubleshooting playbook worked against a real symptom.
- [ ] Safe rollback rehearsed; layered controls confirmed.
- [ ] Cluster deleted with `kind delete cluster`.

## Where to go next

This lab built service-mesh segmentation with Linkerd — automatic mTLS, ServiceAccount identity, and Server/AuthorizationPolicy — entirely from open source. To place it among the alternatives, including the heavier Istio and the multi-platform Consul, see [Volume LXXXVII, Microsegmentation Options](../../volume-087-microsegmentation-options/README.md), whose Chapter 15 comparison matrix links each option to its own build-it-yourself lab in this series.
