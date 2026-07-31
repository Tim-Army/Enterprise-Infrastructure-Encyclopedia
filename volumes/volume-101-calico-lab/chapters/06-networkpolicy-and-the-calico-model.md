# Chapter 06: NetworkPolicy and the Calico Model

## Learning Objectives

- Apply a default-deny NetworkPolicy to a namespace.
- Allow a single flow by label selector.
- Understand how Calico implements and extends Kubernetes NetworkPolicy.

Calico enforces standard **Kubernetes NetworkPolicy** and its own richer **Calico policy**. Start with the standard object, because it is portable and it is where most real segmentation begins.

## Hands-On Lab

### Lab 6.1 — Default-deny ingress in the data center namespace

**Objective.** Flip namespace `dc` from allow-all to deny-all ingress, so nothing may reach `db` until explicitly permitted.

**Walkthrough**

```bash
kubectl apply -f - <<'EOF'
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata: { name: default-deny-ingress, namespace: dc }
spec:
  podSelector: {}
  policyTypes: [ Ingress ]
EOF
```

**Step 2.** Confirm the lateral-movement path is now blocked — even the app is blocked, because you have not allowed it yet. From `hmi` and from `web`:

```bash
kubectl exec -n ot hmi -- nc -z -w2 db.dc 5432 || echo "hmi -> db BLOCKED"
kubectl exec -n dc web -- nc -z -w2 db.dc 5432 || echo "web -> db BLOCKED (not yet allowed)"
```

**Expected result.** Both are **BLOCKED**. An empty `podSelector: {}` selects every pod in the namespace, and naming `Ingress` with no `ingress:` rules denies all inbound. The database is now dark to everything.

**Negative test.** Note that `web → db` is blocked too. Default-deny denies the legitimate flow along with the attack; that is why the next step *adds back* exactly what the app needs and nothing more.

**Cleanup.** Keep the default-deny.

### Lab 6.2 — Allow the app tier to reach the database

**Objective.** Permit `app=web → app=db:5432`, restoring the one legitimate flow into the database.

**Walkthrough**

```bash
kubectl apply -f - <<'EOF'
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata: { name: allow-web-to-db, namespace: dc }
spec:
  podSelector: { matchLabels: { app: db } }
  policyTypes: [ Ingress ]
  ingress:
    - from:
        - podSelector: { matchLabels: { app: web } }
      ports:
        - { protocol: TCP, port: 5432 }
EOF
```

**Step 2.** Validate: the app is restored, the attacker stays blocked:

```bash
kubectl exec -n dc web -- nc -z -w2 db.dc 5432 && echo "web -> db ALLOWED"
kubectl exec -n ot hmi -- nc -z -w2 db.dc 5432 || echo "hmi -> db STILL BLOCKED"
```

**Expected result.** `web → db` is **ALLOWED**; `hmi → db` stays **BLOCKED**. The rule selected the source by the label `app=web`; because `hmi` (in namespace `ot`) is not `app=web`, it is denied — the Chapter 05 lateral movement is dead.

**Negative test.** Change the `from` selector to `podSelector: {}` ("allow from anything in this namespace") and the app still works — but so would any compromised pod in `dc`. Least privilege names the *source label*, not "anything". Revert to `app=web`.

**Cleanup.** Keep both policies.

### Lab 6.3 — The Calico model

**Objective.** Understand what Calico added under that standard object, and what its own policy offers.

**Walkthrough**

**Step 1.** Inspect how Calico represents the policy you just wrote:

```bash
calicoctl get networkpolicy -n dc -o wide
```

Calico stores Kubernetes NetworkPolicies as its own `knp.default.*` policies and enforces them in the dataplane (iptables by default, or eBPF). The standard object is a subset of what Calico can express.

**Step 2.** Note the capabilities Calico adds beyond Kubernetes NetworkPolicy, which you use in Chapter 07:

- **GlobalNetworkPolicy** — cluster-wide, not namespaced.
- **Tiers** — ordered policy groups, so platform guardrails evaluate before app-team rules.
- **`Deny` action and rule order** — Kubernetes NetworkPolicy is allow-only; Calico can write explicit `Deny`.
- **HostEndpoints and NetworkSets** — policy for the node itself and for endpoints outside the cluster (Chapter 08).

**Expected result.** You can explain that Calico enforces the standard object and extends it with global, ordered, deny-capable policy.

**Negative test.** Assume Kubernetes NetworkPolicy alone can express "deny RDP everywhere, then let teams allow within their namespace". It cannot — it is namespaced and allow-only. That is exactly the gap Calico tiers and GlobalNetworkPolicy fill.

**Cleanup.** Keep the policies for Chapter 07.

## Summary and Completion Checklist

- [ ] Namespace `dc` default-denies ingress.
- [ ] `web → db:5432` allowed by label; `hmi → db` blocked.
- [ ] Calico's representation of the policy inspected with `calicoctl`.
- [ ] The capabilities Calico adds beyond Kubernetes NetworkPolicy understood.
