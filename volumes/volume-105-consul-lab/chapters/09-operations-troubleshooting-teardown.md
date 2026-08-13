# Chapter 09: Operations, Troubleshooting, and Teardown

## Learning Objectives

- Work a structured troubleshooting playbook for Consul intentions.
- Rehearse a safe rollback.
- Tear the cluster down cleanly.

## Hands-On Lab

### Lab 9.1 — Troubleshooting playbook

**Objective.** Diagnose the three failure modes you are most likely to hit.

**Walkthrough.**

**Symptom 1 — a service is not in the mesh.** It has no `consul-dataplane` sidecar. Confirm the connect-inject annotation and that the injector is healthy:

```bash
kubectl get pod -l app=web -o jsonpath='{.items[0].spec.containers[*].name}{"\n"}'
kubectl -n consul get pods | grep connect-injector
```

**Symptom 2 — a legitimate flow is denied.** An intention is missing or a wildcard deny shadows it. List and check precedence (specific beats wildcard):

```bash
kubectl get serviceintentions
kubectl describe serviceintentions db
```

**Symptom 3 — an L7 intention does nothing.** The destination protocol is not `http`. Confirm the `ServiceDefaults`:

```bash
kubectl get servicedefaults api -o jsonpath='{.spec.protocol}{"\n"}'
```

**Expected result.** Each symptom maps to a first check: injection, intention precedence, or the protocol declaration for L7.

**Negative test.** "Fix" a denied flow by deleting the `deny-all`. You removed default-deny for the whole mesh. Add the specific allowing intention instead.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 9.2 — Safe rollback

**Objective.** Restore connectivity fast.

**Walkthrough.**

- **Undo one intention:** `kubectl delete serviceintentions <name>`.
- **Loosen the mesh:** delete the `deny-all` intention to return to allow-first (lab only) — but prefer adding the specific allow.
- **Inspect first:** the Consul UI's Intentions and Topology tabs show what is allowed/denied before you change anything.

**Step 1.** Practice removing one allow and confirming the default-deny still protects the rest:

```bash
kubectl delete serviceintentions db
kubectl exec deploy/web -c web -- nc -z -w2 db 5432 || echo "web -> db now DENIED (deny-all governs it again)"
kubectl apply -f - <<'EOF'
apiVersion: consul.hashicorp.com/v1alpha1
kind: ServiceIntentions
metadata: { name: db }
spec: { destination: { name: db }, sources: [ { name: web, action: allow } ] }
EOF
```

**Expected result.** Removing the `db` allow re-denies `web → db` (the wildcard deny governs it), proving default-deny is the floor. Re-applying restores the app.

**Negative test.** Delete every intention including `deny-all`; the mesh returns to flat. Keep `deny-all` plus the specific allows.

**Rollback.** Ensure the intended intentions are back.

### Lab 9.3 — Teardown

**Objective.** Remove the cluster.

**Walkthrough.**

```bash
helm uninstall consul -n consul 2>/dev/null || true
kind delete cluster --name consul-lab
docker ps -a | grep consul-lab || echo "no lab containers remain"
```

Optionally remove the `kind`, `kubectl`, `helm`, and `consul` binaries.

**Expected result.** The cluster and its containers are gone.

**Negative test.** Deleting the kind containers by hand leaves metadata behind; a later recreate may conflict. Use `kind delete cluster`.

**Rollback.** Host restored.

## Summary and Completion Checklist

- [ ] Troubleshooting playbook worked against a real symptom.
- [ ] Safe rollback rehearsed; default-deny confirmed as the floor.
- [ ] Cluster deleted with `kind delete cluster`.

## Where to go next

This lab built multi-platform mesh segmentation with Consul — Connect mTLS, service intentions, and one mesh across Kubernetes and VMs — entirely from open source, completing the open-source tier of this series. To place it among all the alternatives, see [Volume LXXXVII, Microsegmentation Options](../../volume-087-microsegmentation-options/README.md), whose Chapter 15 comparison matrix links each option to its own build-it-yourself lab.
