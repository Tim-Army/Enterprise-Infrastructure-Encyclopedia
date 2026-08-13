# Chapter 09: Operations, Troubleshooting, and Teardown

## Learning Objectives

- Work a structured troubleshooting playbook for Cilium policy.
- Rehearse a safe rollback.
- Tear the cluster down cleanly.

## Hands-On Lab

### Lab 9.1 — Troubleshooting playbook

**Objective.** Diagnose the three failure modes you are most likely to hit.

**Walkthrough.**

**Symptom 1 — policy does not take effect.** Confirm Cilium and Hubble are healthy and the policy was accepted:

```bash
cilium status
kubectl get ciliumnetworkpolicy -A
kubectl get ciliumclusterwidenetworkpolicy
```

**Symptom 2 — a flow is dropped that should be allowed.** Let Hubble tell you why — it names the policy verdict and the identities:

```bash
hubble observe --to-pod dc/db --verdict DROPPED --last 20
kubectl -n kube-system exec ds/cilium -- cilium endpoint list | grep -E "web|db"
```

The usual cause is a label the selector does not match, or — for L7 — a method/path outside the allowed rule (a `403` is policy working, not a bug).

**Symptom 3 — an L7 (HTTP) rule seems to break the connection entirely.** Remember that L7 policy redirects traffic through Cilium's proxy; a `403` is an *allowed connection with a denied request*. If you instead see a TCP-level drop, the L4 `toPorts` is wrong (wrong port), not the L7 rule.

**Expected result.** Each symptom maps to a first check, and Hubble is your primary tool because it speaks in policy terms.

**Negative test.** "Fix" a 403 by deleting the L7 policy. You removed the L7 protection to make a POST work — which was exactly the abuse you were preventing. Adjust the rule, do not delete it.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 9.2 — Safe rollback

**Objective.** Restore connectivity fast without deleting the wrong thing.

**Walkthrough.**

- **Undo one policy:** `kubectl delete ciliumnetworkpolicy -n <ns> <name>`.
- **Undo the cluster-wide guardrail:** `kubectl delete ciliumclusterwidenetworkpolicy protect-db-clusterwide` (the namespace policy still protects the db).
- **Monitor mode:** for a quick, non-destructive check of what policy *would* drop, use `hubble observe --verdict DROPPED` while the policy is live rather than removing it.

**Step 1.** Practice removing the cluster-wide guardrail and confirm the namespace policy still holds:

```bash
kubectl delete ciliumclusterwidenetworkpolicy protect-db-clusterwide
kubectl exec -n ot hmi -- nc -z -w2 db.dc 5432 || echo "hmi -> db STILL blocked by the namespace policy"
```

**Expected result.** Removing one control does not open the hole — two independent controls guarded it. Re-apply when done.

**Negative test.** Delete both the namespace and cluster-wide policies for the db and the lateral movement returns. Re-apply both.

**Rollback.** Ensure both controls are back.

### Lab 9.3 — Teardown

**Objective.** Remove the cluster and reclaim resources.

**Walkthrough.**

```bash
kind delete cluster --name cilium-lab
docker ps -a | grep cilium-lab || echo "no lab containers remain"
```

Optionally remove the `kind`, `kubectl`, `cilium`, and `hubble` binaries from `/usr/local/bin`.

**Expected result.** The cluster and its containers are gone.

**Negative test.** Deleting the kind containers by hand leaves kind metadata behind; a later recreate may conflict. Use `kind delete cluster`.

**Rollback.** Host restored.

## Summary and Completion Checklist

- [ ] Troubleshooting playbook worked against a real symptom, using Hubble.
- [ ] Safe rollback rehearsed; defense-in-depth confirmed.
- [ ] Cluster deleted with `kind delete cluster`.

## Where to go next

This lab built Kubernetes segmentation with Cilium — eBPF, Hubble, and Layer 7 policy — entirely from open source. To place it among the alternatives, see [Volume LXXXVII, Microsegmentation Options](../../volume-087-microsegmentation-options/README.md), whose Chapter 15 comparison matrix links each option to its own build-it-yourself lab in this series.
