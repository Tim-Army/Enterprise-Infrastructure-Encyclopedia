# Chapter 03: Building the Cluster and Installing Linkerd

## Learning Objectives

- Create a `kind` cluster (Linkerd runs on top of the default CNI).
- Install the Linkerd control plane and the `viz` observability extension.
- Verify Linkerd is healthy.

Like Istio and unlike Calico/Cilium, Linkerd is not the CNI — it runs on top of whatever CNI the cluster has. Do **not** disable the default CNI.

## Hands-On Lab

### Lab 3.1 — Create a kind cluster

**Objective.** Build a standard single-node cluster.

**Walkthrough**

```bash
kind create cluster --name linkerd-lab
kubectl get nodes
```

**Expected result.** One node, `Ready` (kind's default CNI provides networking).

**Negative test.** Disable the default CNI here and the node stays `NotReady`; Linkerd needs a working pod network beneath it. Leave the default CNI.

**Cleanup.** None yet.

### Lab 3.2 — Install the Linkerd control plane

**Objective.** Install Linkerd's CRDs and control plane, and verify.

**Walkthrough**

```bash
linkerd check --pre
linkerd install --crds | kubectl apply -f -
linkerd install | kubectl apply -f -
linkerd check
```

**Expected result.** `linkerd check` reports all checks passing; the control plane runs in the `linkerd` namespace. Notice you configured **no** mTLS settings — Linkerd issues identities and enables mTLS automatically.

**Negative test.** Skip `linkerd install --crds` and the control-plane install fails for missing CRDs. Install the CRDs first.

**Cleanup.** None.

### Lab 3.3 — Install linkerd viz (observability)

**Objective.** Install the `viz` extension for metrics and live traffic inspection.

**Walkthrough**

```bash
linkerd viz install | kubectl apply -f -
linkerd viz check
```

**Expected result.** `linkerd viz check` passes; you can now use `linkerd viz stat`, `linkerd viz edges` (to see which connections are mTLS), and `linkerd viz tap` (to watch live requests). This is Linkerd's lighter-weight equivalent of Hubble.

**Negative test.** Try `linkerd viz stat` before the extension is ready; it errors. Wait for `viz check`.

**Cleanup.** Keep the cluster and Linkerd; Chapter 04 deploys the workloads.

## Summary and Completion Checklist

- [ ] kind cluster created with its default CNI; node Ready.
- [ ] Linkerd control plane installed; `linkerd check` passes.
- [ ] `linkerd viz` installed; `viz check` passes.
