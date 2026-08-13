# Chapter 02: Kubernetes and Cloud Native Associate (KCNA)

## Learning Objectives

- Explain who the KCNA is for and its place as the entry credential.
- List the four KCNA domains and their exam weights.
- Describe the KCNA exam mechanics (multiple-choice, 90 minutes).
- Relate KCNA concepts to real `kubectl` operations against a cluster.
- Complete a per-domain walkthrough for each KCNA domain.

## Theory and Architecture

**Kubernetes and Cloud Native Associate (KCNA)** is the CNCF's **entry-level,
multiple-choice** credential. It validates foundational knowledge of Kubernetes
and the broader cloud-native ecosystem — enough to hold a conversation about
pods, deployments, orchestration, delivery, and the CNCF landscape — without the
hands-on depth of CKA/CKAD. It is the recommended first step and a gateway to the
performance-based exams.

The exam is **90 minutes, multiple-choice**, across four weighted domains:

| # | Domain | Weight |
|---|--------|--------|
| 1 | Kubernetes Fundamentals | 44% |
| 2 | Container Orchestration | 28% |
| 3 | Cloud Native Application Delivery | 16% |
| 4 | Cloud Native Architecture | 12% |

**Kubernetes Fundamentals (44%)** dominates — the core objects and `kubectl` are
nearly half the exam.

## Design Considerations

Treat KCNA as **orientation**. Because it is broad and shallow, the fastest path
is to run a local cluster and *touch* every concept once — create a pod, scale a
deployment, expose a service, read the API — so the multiple-choice questions map
to something you have actually seen. KCNA also introduces the **CNCF landscape**
(the projects the later associate exams specialize in), so it doubles as a map of
this entire volume.

## Implementation and Automation

Every KCNA concept has a one-line `kubectl` demonstration, which is how the labs
below make the vocabulary concrete: the API and core objects (Domain 1), scaling
and scheduling (Domain 2), rollouts (Domain 3), and the architecture of the
control plane (Domain 4).

## Validation and Troubleshooting

Confirm the KCNA blueprint before studying:

```text
training.linuxfoundation.org > KCNA > curriculum:
  - four domains and weights (44/28/16/12)
  - 90 minutes, multiple-choice, no prerequisites
```

Common pitfalls: over-studying niche projects when **Kubernetes Fundamentals** is
44%; and treating KCNA as hands-on — it is knowledge-based, but hands-on practice
is still the best way to learn it.

## Security and Best Practices

Even at entry level, learn the **declarative model** (desired state in YAML,
reconciled by controllers), **namespaces** for isolation, and **RBAC** as the
access model — these recur throughout the program. Practice on a throwaway `kind`
cluster so mistakes are free.

## References and Knowledge Checks

- training.linuxfoundation.org: *KCNA* curriculum; kubernetes.io documentation; the CNCF landscape.

**Knowledge checks**

1. Which KCNA domain is largest, and what does it cover?
2. What is the declarative model, and how does a controller use it?
3. How does KCNA relate to the associate exams later in this volume?

## Hands-On Lab

Per-topic walkthroughs — **one lab for every weighted KCNA domain**.

**Shared prerequisites** — the `kind`/`minikube` cluster from Chapter 01 and
`kubectl`. **Cost:** none.

### Lab 2.1 — KCNA: Kubernetes Fundamentals (44%)

**Objective:** Create and inspect the core object — a pod — declaratively.

```bash
kubectl run web --image=nginx --restart=Never
kubectl get pod web -o wide
kubectl get pod web -o jsonpath='{.status.phase}{"\n"}'
```

**Expected result:** the `web` pod listed with a node and IP, and a phase of
`Running` (after a moment) — the fundamental Kubernetes object and how `kubectl`
reads it.

**Negative test:** expect `kubectl run` to create a Deployment; with
`--restart=Never` it creates a bare Pod — know the difference.

**Rollback:** `kubectl delete pod web`

### Lab 2.2 — KCNA: Container Orchestration (28%)

**Objective:** Demonstrate orchestration — declared replicas, self-healing.

```bash
kubectl create deployment web --image=nginx --replicas=3
kubectl get deploy web
kubectl delete pod -l app=web --field-selector=status.phase=Running --wait=false | head -1
kubectl get deploy web    # replicas restored by the controller
```

**Expected result:** the Deployment shows `3/3` ready, and after deleting a pod
the controller recreates it to restore the declared count — orchestration and
self-healing.

**Negative test:** delete a pod and expect it to stay gone; the Deployment
controller reconciles back to 3 — that is orchestration working.

**Rollback:** `kubectl delete deploy web`

### Lab 2.3 — KCNA: Cloud Native Application Delivery (16%)

**Objective:** Perform a rolling update and read the rollout status.

```bash
kubectl create deployment web --image=nginx:1.25 --replicas=2
kubectl set image deployment/web nginx=nginx:1.27
kubectl rollout status deployment/web
kubectl rollout history deployment/web | head
```

**Expected result:** `deployment "web" successfully rolled out` and a revision
history — the zero-downtime delivery pattern KCNA introduces.

**Negative test:** change the image by editing pods directly; the Deployment
would revert them — update the Deployment template so the rollout is managed.

**Rollback:** `kubectl delete deploy web`

### Lab 2.4 — KCNA: Cloud Native Architecture (12%)

**Objective:** Observe the control-plane architecture — the API and components.

```bash
kubectl get componentstatuses 2>/dev/null || kubectl get --raw='/healthz?verbose' | head
kubectl -n kube-system get pods -o name | grep -E 'kube-apiserver|etcd|scheduler|controller' | head
```

**Expected result:** healthy control-plane checks and the core components
(`kube-apiserver`, `etcd`, `kube-scheduler`, `kube-controller-manager`) — the
cloud-native architecture KCNA describes.

**Negative test:** assume the scheduler places pods on itself; the API server is
the front door and the scheduler only *assigns* nodes — each component has one
job.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

KCNA is the CNCF's multiple-choice entry credential: four domains weighted
44/28/16/12, dominated by Kubernetes Fundamentals. It orients a newcomer to
pods, orchestration, delivery, and the control-plane architecture — and maps the
cloud-native landscape the later associate exams specialize in.

- [ ] I can list the four KCNA domains and their weights.
- [ ] I can create a pod and a self-healing Deployment.
- [ ] I can perform and read a rolling update.
- [ ] I can name the core control-plane components.
- [ ] I completed Labs 2.1–2.4 including each negative test.
