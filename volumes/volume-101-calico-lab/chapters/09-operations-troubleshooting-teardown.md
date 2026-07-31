# Chapter 09: Operations, Troubleshooting, and Teardown

## Learning Objectives

- Work a structured troubleshooting playbook for Calico policy.
- Rehearse a safe rollback.
- Tear the cluster down cleanly.

## Hands-On Lab

### Lab 9.1 — Troubleshooting playbook

**Objective.** Diagnose the three failure modes you are most likely to hit.

**Walkthrough.**

**Symptom 1 — policy does not block anything.** Confirm the CNI is Calico and the default-deny exists:

```bash
kubectl -n kube-system get pods -l k8s-app=calico-node        # Running?
kubectl get networkpolicy -A                                  # is default-deny present?
```

A namespace with allow rules but no default-deny stays allow-all — the allows are additive over an open base.

**Symptom 2 — a legitimate flow is blocked.** Read which policies select the destination and why the source is not matched:

```bash
kubectl describe networkpolicy -n dc allow-web-to-db
kubectl get pod -n dc --show-labels | grep -E "web|db"        # do the labels match the selectors?
calicoctl get networkpolicy -n dc -o wide
calicoctl get globalnetworkpolicy -o wide
```

The usual cause is a label mismatch (a pod not carrying `app=web`) or a `security`-tier `Deny` shadowing the allow.

**Symptom 3 — DNS or the app breaks after a global policy.** You wrote an all-selecting egress/ingress deny without allowing `kube-system` and port 53. Check:

```bash
kubectl exec -n dc web -- nslookup db.dc 2>/dev/null || kubectl exec -n dc web -- nc -zu -w2 kube-dns.kube-system 53 || echo "DNS blocked - fix the global policy"
```

**Expected result.** Each symptom maps to a first check: CNI health, label/selector match, or a too-broad global deny.

**Negative test.** "Fix" a blocked flow by deleting all NetworkPolicies. You removed the protection, not the bug. Fix the label or the tier order instead.

**Cleanup.** None.

### Lab 9.2 — Safe rollback

**Objective.** Restore connectivity fast without deleting the wrong thing.

**Walkthrough.**

- **Undo one policy:** `kubectl delete networkpolicy -n <ns> <name>` or `calicoctl delete globalnetworkpolicy <name>`.
- **Undo a tier guardrail:** `calicoctl delete globalnetworkpolicy security.protect-db` (the namespace policy still protects the db — defense in depth).
- **Back to fully open (lab only):** delete every NetworkPolicy in `dc` and `ot` and the `security`-tier policies; the cluster returns to allow-all.

**Step 1.** Practice removing just the security-tier guardrail and confirm the namespace policy still holds:

```bash
calicoctl delete globalnetworkpolicy security.protect-db
kubectl exec -n ot hmi -- nc -z -w2 db.dc 5432 || echo "hmi -> db STILL blocked by the namespace policy"
```

**Expected result.** Removing one control does not open the hole, because two independent controls guarded it. Re-apply the guardrail when done.

**Negative test.** Delete the namespace default-deny *and* the tier guardrail and the lateral movement returns. Two controls protect; removing both un-protects. Re-apply both.

**Cleanup.** Ensure both controls are back in place.

### Lab 9.3 — Teardown

**Objective.** Remove the cluster and reclaim resources.

**Walkthrough.**

```bash
kind delete cluster --name calico-lab
docker ps -a | grep calico-lab || echo "no lab containers remain"
```

Optionally remove the tools (`kind`, `kubectl`, `calicoctl`) from `/usr/local/bin` and, if you installed Docker only for this lab, uninstall it.

**Expected result.** The cluster and its containers are gone; the host is reclaimed.

**Negative test.** Delete the kind Docker containers by hand instead of `kind delete cluster`; kind's metadata is left behind and a later `kind create cluster --name calico-lab` may conflict. Use `kind delete cluster`.

**Cleanup.** Host restored.

## Summary and Completion Checklist

- [ ] Troubleshooting playbook worked against a real symptom.
- [ ] Safe rollback rehearsed; defense-in-depth confirmed (removing one control did not open the hole).
- [ ] Cluster deleted with `kind delete cluster`.

## Where to go next

This lab built Kubernetes segmentation with Calico, entirely from open source. To place it among the alternatives — including the other open-source options Cilium, Istio, Linkerd, and Consul — see [Volume LXXXVII, Microsegmentation Options](../../volume-087-microsegmentation-options/README.md), whose Chapter 15 comparison matrix links each option to its own build-it-yourself lab in this series.
