# Chapter 03: Building the Cluster and Installing Istio

## Learning Objectives

- Create a `kind` cluster (its default CNI is fine — Istio is an overlay on top).
- Install the Istio control plane and verify it.

Unlike Calico and Cilium, Istio is **not** the CNI. It runs on top of whatever CNI the cluster has, so you do **not** disable the default CNI here.

## Hands-On Lab

### Lab 3.1 — Create a kind cluster

**Objective.** Build a standard single-node cluster.

**Walkthrough**

```bash
kind create cluster --name istio-lab
kubectl get nodes
```

**Expected result.** One node, `Ready` (kind's default `kindnet` CNI provides networking).

**Negative test.** Disable the default CNI here as you did for Calico/Cilium and the node stays `NotReady` — Istio needs a working pod network beneath it. Leave the default CNI in place.

**Cleanup.** None yet.

### Lab 3.2 — Install the Istio control plane

**Objective.** Install `istiod` and the Istio components.

**Walkthrough**

```bash
istioctl install --set profile=default -y
kubectl -n istio-system get pods
istioctl verify-install
```

**Expected result.** `istiod` (and, with the default profile, an ingress gateway) are `Running` in `istio-system`; `verify-install` reports success. The mesh control plane is up; workloads join it by sidecar injection in Chapter 04.

**Negative test.** Deploy a workload into a namespace *before* labeling it for injection and it gets no sidecar — it is in the cluster but not in the mesh, so mTLS and AuthorizationPolicy do not apply to it. Labeling comes in Chapter 04.

**Cleanup.** Keep the cluster and Istio; Chapter 04 deploys the workloads.

## Summary and Completion Checklist

- [ ] kind cluster created with its default CNI; node Ready.
- [ ] Istio control plane installed; `istiod` Running; `verify-install` passes.
