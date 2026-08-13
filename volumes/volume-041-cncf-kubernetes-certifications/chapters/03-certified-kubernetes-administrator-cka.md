# Chapter 03: Certified Kubernetes Administrator (CKA)

## Learning Objectives

- Explain what the CKA certifies and why it is performance-based.
- List the five CKA domains and their exam weights.
- Describe the CKA exam mechanics: live terminal, 2 hours, 66% to pass, killer.sh.
- Perform core administrator tasks with `kubectl` and `kubeadm`.
- Complete a per-domain walkthrough for each CKA domain.

## Theory and Architecture

The **Certified Kubernetes Administrator (CKA)** is the CNCF's flagship
operations credential. It is **performance-based**: two hours in a **live
terminal** solving real cluster tasks — installing and configuring clusters,
managing workloads, storage, and networking, and above all **troubleshooting**.
It is the anchor of the Kubernetes core and the **prerequisite for CKS**.

The exam is **2 hours, performance-based, 66% to pass**, and (with CKAD/CKS)
includes **killer.sh** simulator sessions. It is pinned to a current Kubernetes
version (v1.35). Five weighted domains:

| # | Domain | Weight |
|---|--------|--------|
| 1 | Cluster Architecture, Installation & Configuration | 25% |
| 2 | Workloads & Scheduling | 15% |
| 3 | Storage | 10% |
| 4 | Services & Networking | 20% |
| 5 | Troubleshooting | 30% |

**Troubleshooting (30%)** is the largest domain — the CKA is fundamentally about
diagnosing and fixing broken clusters under time pressure.

## Design Considerations

CKA rewards **speed and diagnosis** over recall. The winning strategy is
imperative `kubectl` (`--dry-run=client -o yaml` to scaffold, then edit),
fluent context/namespace switching, and a systematic troubleshooting method:
check the object, its events, its logs, and the node/kubelet. Domain 1 includes
**RBAC**, **kubeadm** cluster lifecycle (init, join, **upgrade**), **Helm** and
**Kustomize**, and **CRDs/operators**; Domain 4 covers **NetworkPolicies**,
**Ingress/Gateway API**, and **CoreDNS**. Practice each until it is muscle memory.

## Implementation and Automation

The labs below exercise one representative, real task per domain: an RBAC role
(Domain 1), a scheduled/constrained workload (Domain 2), a PVC bound to a
PersistentVolume (Domain 3), a Service resolving via DNS (Domain 4), and a
guided troubleshooting flow (Domain 5) — the exact `kubectl` patterns the timed
exam demands.

## Validation and Troubleshooting

Confirm the CKA blueprint before studying:

```text
training.linuxfoundation.org > CKA > curriculum:
  - five domains and weights (25/15/10/20/30)
  - performance-based, 2 hours, 66% to pass, Kubernetes v1.35
  - includes two attempts + killer.sh
```

Common pitfalls: hand-writing YAML instead of generating it; forgetting to set
the right **namespace/context** for a task (points lost on the wrong cluster);
and under-practicing **troubleshooting**, the largest domain — drill broken-pod,
broken-node, and broken-networking scenarios.

## Security and Best Practices

Administer with least privilege: scope **RBAC** to namespaces and verbs, use
**NetworkPolicies** to default-deny, and keep the cluster **current** (kubeadm
upgrades). Back up **etcd** (a classic CKA task) before disruptive changes.
Practice against the **exact Kubernetes version** in the curriculum.

## References and Knowledge Checks

- training.linuxfoundation.org: *CKA* curriculum; kubernetes.io (Tasks, Concepts); github.com/cncf/curriculum.

**Knowledge checks**

1. Which CKA domain is largest, and what does it demand?
2. Why is imperative `kubectl` the exam-speed technique?
3. What are two Domain 1 lifecycle tasks that use `kubeadm`?

## Hands-On Lab

Per-topic walkthroughs — **one lab for every weighted CKA domain**.

**Shared prerequisites** — the `kind`/`minikube` cluster from Chapter 01 and
`kubectl`. **Cost:** none.

### Lab 3.1 — CKA: Cluster Architecture, Installation & Configuration (25%)

**Objective:** Create and verify an RBAC role binding (a core Domain 1 task).

```bash
kubectl create namespace dev
kubectl create role pod-reader --verb=get,list --resource=pods -n dev
kubectl create rolebinding read-pods --role=pod-reader --user=alice -n dev
kubectl auth can-i list pods --as=alice -n dev
kubectl auth can-i delete pods --as=alice -n dev
```

**Expected result:** `yes` for listing pods and `no` for deleting them as
`alice` — RBAC granting exactly the permitted verbs, the least-privilege model
CKA tests.

**Negative test:** bind a `ClusterRole` cluster-wide when only namespace access
is needed; that over-grants — scope the RoleBinding to the namespace.

**Rollback:** `kubectl delete namespace dev`

### Lab 3.2 — CKA: Workloads & Scheduling (15%)

**Objective:** Constrain scheduling with a nodeSelector and resource requests.

```bash
kubectl label node "$(kubectl get node -o name | head -1 | cut -d/ -f2)" tier=lab --overwrite
kubectl create deployment sched --image=nginx --replicas=1
kubectl patch deployment sched --type=merge -p \
  '{"spec":{"template":{"spec":{"nodeSelector":{"tier":"lab"},"containers":[{"name":"nginx","resources":{"requests":{"cpu":"50m"}}}]}}}}'
kubectl get pod -l app=sched -o wide
```

**Expected result:** the pod scheduled onto the `tier=lab` node with a CPU
request — the scheduling constraints (selectors, requests) of Domain 2.

**Negative test:** request more CPU than any node has; the pod stays `Pending`
with a `FailedScheduling` event — requests must fit a node.

**Rollback:** `kubectl delete deploy sched`

### Lab 3.3 — CKA: Storage (10%)

**Objective:** Bind a PersistentVolumeClaim to storage.

```bash
kubectl apply -f - <<'YAML'
apiVersion: v1
kind: PersistentVolumeClaim
metadata: {name: data, namespace: default}
spec:
  accessModes: [ReadWriteOnce]
  resources: {requests: {storage: 100Mi}}
YAML
kubectl get pvc data
```

**Expected result:** the PVC reaches `Bound` (kind/minikube provide a default
StorageClass that dynamically provisions a PV) — the storage lifecycle CKA
tests.

**Negative test:** request a StorageClass that does not exist; the PVC stays
`Pending` — the class must exist or a default must be set.

**Rollback:** `kubectl delete pvc data`

### Lab 3.4 — CKA: Services & Networking (20%)

**Objective:** Expose a Deployment and resolve it via cluster DNS.

```bash
kubectl create deployment web --image=nginx
kubectl expose deployment web --port=80
kubectl run probe --image=busybox --restart=Never -it --rm -- \
  nslookup web.default.svc.cluster.local 2>/dev/null | head
```

**Expected result:** `nslookup` resolves `web.default.svc.cluster.local` to the
Service's ClusterIP — Service discovery via CoreDNS, central to Domain 4.

**Negative test:** curl a pod IP directly and rely on it; pod IPs are ephemeral
— use the stable Service name/ClusterIP.

**Rollback:** `kubectl delete deploy web svc web`

### Lab 3.5 — CKA: Troubleshooting (30%)

**Objective:** Diagnose a failing pod with the standard triage flow.

```bash
kubectl run bad --image=nginx:doesnotexist --restart=Never
sleep 3
kubectl get pod bad
kubectl describe pod bad | grep -A3 Events
```

**Expected result:** the pod in `ErrImagePull`/`ImagePullBackOff` and an Events
line naming the bad image — the get → describe → events triage flow that wins the
largest CKA domain.

**Negative test:** delete and recreate the pod hoping it fixes itself; the image
tag is wrong — read the events and fix the root cause.

**Rollback:** `kubectl delete pod bad`

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

CKA is the CNCF's performance-based administrator credential: five domains
weighted 25/15/10/20/30, dominated by troubleshooting, solved live in a terminal
in two hours (66% to pass). It rewards imperative `kubectl`, RBAC and kubeadm
fluency, and a systematic diagnosis method, and it is the prerequisite for CKS.

- [ ] I can list the five CKA domains and their weights.
- [ ] I can create RBAC, constrain scheduling, and bind a PVC.
- [ ] I can expose a Service and resolve it via DNS.
- [ ] I can triage a failing pod with get/describe/events.
- [ ] I completed Labs 3.1–3.5 including each negative test.
