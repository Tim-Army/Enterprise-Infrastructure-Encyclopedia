# Chapter 03: Kubernetes Workloads, Scheduling, and Capacity

![Lab topology for this chapter: demo-api deploys 3 replicas with required pod anti-affinity spreading one pod per node and a PodDisruptionBudget requiring minAvailable 2; an HPA targeting 50% CPU confirms live metrics and scales replicas out under generated load. As a negative test, draining the node holding one demo-api pod while only 3 replicas exist is refused: the drain reports 'Cannot evict pod as it would violate the pod's disruption budget', because removing that pod would drop available replicas below minAvailable 2. Running uncordon on the node restores normal scheduling.](../../../diagrams/volume-08-containers-platform-engineering/chapter-03-hpa-pdb-drain-topology.svg)

*Figure 3-1. Topology used throughout this chapter's Hands-On Lab: an anti-affinity-spread, HPA-scaled workload whose PodDisruptionBudget correctly blocks a node drain.*

## Learning Objectives

- Select the correct workload controller — Deployment, StatefulSet,
  DaemonSet, Job, or CronJob — for a given application's identity,
  ordering, and completion requirements.
- Explain how requests and limits drive Quality of Service (QoS)
  classification, node scheduling, and eviction behavior under resource
  pressure.
- Steer scheduling outcomes with node affinity, pod affinity/anti-affinity,
  topology spread constraints, and taints/tolerations.
- Configure horizontal and cluster-level autoscaling, and explain why
  vertical autoscaling and in-place resize remain more constrained tools
  in Kubernetes 1.31.x.
- Protect availability during voluntary disruptions with
  PodDisruptionBudgets and diagnose a running pod with ephemeral debug
  containers.

## Theory and Architecture

Every Kubernetes workload ultimately reduces to Pods, but almost nothing
in production creates a Pod directly. Controllers wrap the Pod template
with a reconciliation loop that answers a question the Pod object itself
cannot: how many copies should exist, in what order should they start and
stop, and what happens when one dies.

### Workload controllers and the identity they provide

- **Deployment** manages a **ReplicaSet**, which in turn manages Pods. The
  Deployment itself owns rollout strategy (`RollingUpdate` or `Recreate`),
  revision history, and rollback. Pods under a Deployment are fungible —
  interchangeable, individually disposable, and identified only by a
  generated suffix. This is the correct default for stateless workloads.
- **StatefulSet** provides stable, ordinal pod identity
  (`web-0`, `web-1`, `web-2`), a stable DNS name per pod via a headless
  Service, and — critically — a stable PersistentVolumeClaim per ordinal
  that survives pod rescheduling. Pods are created, updated, and deleted
  in ordinal order by default (`OrderedReady`), which is what makes
  StatefulSet the correct controller for anything with per-instance state
  or peer-aware clustering ([Chapter 05](05-kubernetes-storage-and-stateful-platforms.md) covers the storage half of this
  contract in depth).
- **DaemonSet** guarantees exactly one pod copy per node (or per node
  matching a selector), growing and shrinking automatically as nodes join
  or leave. Node agents — CNI plugins, log shippers, node-level metrics
  exporters, storage drivers — are DaemonSets almost universally, and
  DaemonSet pods routinely tolerate the control-plane
  `node-role.kubernetes.io/control-plane:NoSchedule` taint so the agent
  also runs on control-plane nodes.
- **Job** runs a pod (or a set of pods, via `completions`/`parallelism`)
  to successful completion rather than indefinitely. `backoffLimit` bounds
  retry attempts; `podFailurePolicy` (stable as of the 1.31.x baseline)
  lets a Job react differently to a container exit code versus a node
  failure, avoiding wasted retries on failures that cannot succeed on
  retry. `ttlSecondsAfterFinished` garbage-collects finished Jobs
  automatically.
- **CronJob** creates Jobs on a schedule, with `concurrencyPolicy`
  (`Allow`, `Forbid`, `Replace`) governing overlapping runs and a
  `timeZone` field so schedules do not silently shift across daylight
  saving transitions.

### The scheduler's two-phase decision

The kube-scheduler (introduced architecturally in [Chapter 02](02-kubernetes-architecture-and-cluster-lifecycle.md)) makes a
binding decision for every unscheduled pod in two phases:

```text
Filtering (predicates)          Scoring (priorities)
  - node has enough allocatable    - least/most requested resources
    CPU/memory for requests        - inter-pod affinity satisfaction
  - taints the pod does not          weighted by preference
    tolerate                       - topology spread contribution
  - required node/pod affinity     - image already present locally
  - volume topology constraints    - node affinity preference weight
  - port conflicts
        │                                  │
        ▼                                  ▼
  Feasible node set    ───────────►  Highest-scoring feasible node
```

Filtering produces a candidate set of nodes where the pod *could* run;
scoring ranks that set to decide where it *should* run. A pod that fails
filtering everywhere stays `Pending` with a `FailedScheduling` event
naming the reason — this is the first place to look when a pod will not
start.

### Requests, limits, and Quality of Service

Every container can declare `resources.requests` (what the scheduler
reserves and guarantees) and `resources.limits` (the ceiling the kubelet
and container runtime enforce via cgroups, described in [Chapter 01](01-container-architecture-images-runtimes-and-registries.md)). The
combination across every container in a pod determines its **QoS class**,
which the kubelet uses to decide eviction order under node memory
pressure:

| QoS class | Condition | Eviction priority |
| --- | --- | --- |
| `Guaranteed` | Every container sets `requests == limits` for both CPU and memory | Evicted last |
| `Burstable` | At least one container sets a request, but the pod does not meet `Guaranteed` criteria | Evicted after `BestEffort`, ordered by how far usage exceeds requests |
| `BestEffort` | No container sets any request or limit | Evicted first |

CPU limits are enforced through the cgroup CFS quota (throttling, not
killing); memory limits are enforced through the cgroup's hard memory
ceiling, and exceeding it triggers an OOM kill of that container, visible
as `OOMKilled` in `kubectl describe pod`. This is a common source of
confusion: a CPU-limited container degrades in latency, while a
memory-limited container is terminated outright.

### Priority, preemption, and disruption

A `PriorityClass` assigns an integer priority to a pod. When a
higher-priority pod cannot be scheduled due to resource scarcity, the
scheduler may **preempt** (evict) lower-priority pods on a node to make
room, subject to the evicted pods' own `PodDisruptionBudget`. This is
distinct from a `PodDisruptionBudget` (PDB) itself, which constrains
*voluntary* disruptions initiated by cluster operators or automation —
`kubectl drain`, a cluster autoscaler scale-down, a rolling node upgrade —
by declaring `minAvailable` or `maxUnavailable` for a workload. A PDB has
no effect on involuntary disruption such as a node crashing.

## Design Considerations

**Deployment vs. StatefulSet is an identity question, not a durability
question.** Both can use persistent storage ([Chapter 05](05-kubernetes-storage-and-stateful-platforms.md)). The decision
turns on whether pod replacement needs to preserve *identity* — a stable
name, stable network address, and the same volume reattached to the same
ordinal — or whether any healthy replica is interchangeable. Running a
stateless API behind a StatefulSet only inherits ordered,
one-at-a-time rollout behavior for no benefit; running a clustered
database behind a Deployment risks two replicas racing for the same
volume or losing peer identity on every reschedule.

**Requests should reflect steady-state consumption, not a guess.**
Under-requesting causes node oversubscription and noisy-neighbor CPU
throttling or, worse, `Burstable`/`BestEffort` pods evicted under memory
pressure; over-requesting wastes allocatable capacity the scheduler could
otherwise pack. Vertical Pod Autoscaler (VPA) — a separate add-on, not a
built-in controller — can run in `recommendation-only` mode against
historical usage to calibrate requests before committing to
`Auto`/`Recreate` update mode, which restarts pods to apply new values.
**In-place pod resize** (the `resize` subresource, gated by
`InPlacePodVerticalScaling`) is still an alpha feature at the 1.31.x
baseline and is not yet a substitute for VPA's restart-based update modes
in most production clusters.

**Horizontal scaling needs a signal that actually reflects load.**
`HorizontalPodAutoscaler` (`autoscaling/v2`) scales replica count off
requested-resource utilization by default, but accepts custom and
external metrics (typically sourced through the Prometheus Adapter or a
cloud provider's external metrics API) for queue depth, request rate, or
any business metric — essential for workloads where CPU is a poor proxy
for load, such as a queue consumer.

**Cluster-level autoscaling has two distinct philosophies.**
Cluster Autoscaler scales predefined node groups (cloud provider ASGs,
managed node pools) up or down based on unschedulable pods and node
underutilization — it thinks in terms of groups you already defined.
Karpenter (and Karpenter-based providers on other clouds) provisions
individual nodes directly from a `NodePool`/`NodeClass` specification at
the moment a pod is unschedulable, without pre-defined groups, generally
achieving faster and tighter bin-packing at the cost of a
provider-specific controller. Both interact with PodDisruptionBudgets and
`karpenter.sh/do-not-disrupt` or cluster-autoscaler's
`safe-to-evict` annotations when consolidating nodes.

**Taints and tolerations express node-side policy; affinity expresses
pod-side preference.** A taint (`kubectl taint nodes node1
dedicated=gpu:NoSchedule`) repels pods that lack a matching toleration —
useful for reserving specialized hardware. Node affinity instead pulls a
pod toward matching nodes and, unlike a `nodeSelector`, supports
`preferredDuringSchedulingIgnoredDuringExecution` for a soft preference.
The two mechanisms are complementary and commonly combined: taint the GPU
pool so ordinary workloads are excluded by default, then require both a
toleration and a node-affinity match on the GPU workload so it lands only
where intended.

## Implementation and Automation

### Choosing requests, limits, and a PriorityClass

```yaml
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: platform-critical
value: 100000
globalDefault: false
preemptionPolicy: PreemptLowerPriority
description: "Reserved for platform-managed control workloads."
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: checkout-api
  namespace: payments
spec:
  replicas: 3
  selector:
    matchLabels: { app: checkout-api }
  template:
    metadata:
      labels: { app: checkout-api }
    spec:
      priorityClassName: platform-critical
      containers:
        - name: checkout-api
          image: registry.example.internal/payments/checkout-api:2.3.1
          resources:
            requests: { cpu: "250m", memory: "256Mi" }
            limits: { cpu: "500m", memory: "256Mi" }
```

Setting memory `requests == limits` while leaving CPU limits at roughly
double the request is a common production pattern: it prevents
memory-driven OOM surprises entirely (the request is the ceiling) while
still allowing brief CPU bursts without throttling every cycle.

### Scheduling controls: affinity, anti-affinity, and topology spread

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: checkout-api
  namespace: payments
spec:
  template:
    spec:
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            - labelSelector:
                matchLabels: { app: checkout-api }
              topologyKey: kubernetes.io/hostname
      topologySpreadConstraints:
        - maxSkew: 1
          topologyKey: topology.kubernetes.io/zone
          whenUnsatisfiable: DoNotSchedule
          labelSelector:
            matchLabels: { app: checkout-api }
      tolerations:
        - key: "dedicated"
          operator: "Equal"
          value: "payments"
          effect: "NoSchedule"
      nodeSelector:
        dedicated: payments
```

Required pod anti-affinity guarantees no two replicas share a node;
`topologySpreadConstraints` extends the same guarantee across zones with a
tunable skew tolerance rather than a hard requirement, which scales far
better than anti-affinity alone once replica counts exceed the practical
node or zone count.

### Horizontal and cluster autoscaling

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: checkout-api
  namespace: payments
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: checkout-api
  minReplicas: 3
  maxReplicas: 20
  metrics:
    - type: Resource
      resource:
        name: cpu
        target: { type: Utilization, averageUtilization: 65 }
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
```

```bash
# HPA requires the metrics.k8s.io API, served by metrics-server —
# not Prometheus — for resource-based metrics. Verify it is installed.
kubectl get apiservices v1beta1.metrics.k8s.io
kubectl top pods -n payments

# Inspect current HPA decisions and the metric driving them.
kubectl get hpa -n payments checkout-api -o wide
kubectl describe hpa -n payments checkout-api
```

### PodDisruptionBudget and safe node drains

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: checkout-api
  namespace: payments
spec:
  minAvailable: 2
  selector:
    matchLabels: { app: checkout-api }
```

```bash
# A drain that respects PDBs; it blocks rather than violates the budget.
kubectl drain <node-name> --ignore-daemonsets --delete-emptydir-data

# If the drain stalls, identify which PDB is blocking it.
kubectl get pdb -A
kubectl describe pdb -n payments checkout-api
```

### Debugging a running pod without shipping tools in the image

```bash
# Attach an ephemeral debug container to a running pod, sharing its
# process namespace, without restarting the target container.
kubectl debug -it checkout-api-6d8f9c9b7-x2k4p \
  --image=busybox:1.36 --target=checkout-api -- sh

# Debug a node directly by launching a privileged pod in the host namespaces.
kubectl debug node/<node-name> -it --image=busybox:1.36
```

## Validation and Troubleshooting

```bash
# Why is this pod not scheduled? FailedScheduling events name the reason.
kubectl describe pod <pod-name> -n <namespace>

# Which QoS class did the pod actually receive?
kubectl get pod <pod-name> -n <namespace> -o jsonpath='{.status.qosClass}'

# Allocatable vs. requested resources per node — the scheduler's view.
kubectl describe node <node-name> | grep -A5 "Allocated resources"

# Cluster Autoscaler / Karpenter decision logs (name/namespace vary by install).
kubectl logs -n kube-system deployment/cluster-autoscaler --tail=100
```

| Symptom | Likely cause | Diagnostic |
| --- | --- | --- |
| Pod stuck `Pending` indefinitely | Insufficient allocatable CPU/memory on any node, or an unmet taint/affinity/topology constraint | `kubectl describe pod` event reason; `kubectl describe node` allocated resources |
| Container repeatedly `OOMKilled` | Memory limit set below actual working-set size | `kubectl describe pod` last state reason; compare `kubectl top pod` against the configured limit |
| HPA shows `unknown` for current metrics | metrics-server not installed/reachable, or custom metrics adapter misconfigured | `kubectl get apiservices \| grep metrics`; `kubectl top pods` |
| `kubectl drain` hangs | A PodDisruptionBudget's `minAvailable` cannot be satisfied with one fewer replica | `kubectl get pdb -A`; check `ALLOWED DISRUPTIONS` column |
| CronJob silently stops running | `concurrencyPolicy: Forbid` and the previous Job never completed, or `startingDeadlineSeconds` was missed | `kubectl get jobs -n <namespace>`; `kubectl describe cronjob` |

## Security and Best Practices

- Set both requests and limits on every workload; an unbounded
  `BestEffort` pod is both the first evicted under pressure and, absent a
  limit, capable of starving neighbors before eviction occurs.
- Prefer memory `requests == limits` to make OOM behavior predictable, and
  size CPU limits with headroom above the request rather than pinning
  them equal, unless strict CPU isolation is required.
- Set a `PodDisruptionBudget` for every replicated production workload
  before it is exposed to real traffic; an absent PDB means a routine
  node drain or autoscaler consolidation can take a workload fully
  offline.
- Use required pod anti-affinity or topology spread constraints for
  anything with an availability SLO — replica count alone does not
  protect against a single node or zone failure taking every replica down
  together.
- Reserve elevated `PriorityClass` values for genuinely platform-critical
  workloads; over-assigning high priority defeats preemption's purpose and
  can starve legitimate lower-priority work.
- Avoid shipping debugging tools (shells, package managers) inside
  production images ([Chapter 01](01-container-architecture-images-runtimes-and-registries.md)); use `kubectl debug` ephemeral containers
  for interactive troubleshooting instead.
- Bound every Job and CronJob with `activeDeadlineSeconds` and a sane
  `backoffLimit` so a broken workload fails fast and visibly rather than
  retrying indefinitely and consuming cluster capacity.

## References and Knowledge Checks

**Authoritative references**

- Kubernetes documentation, [Workload Resources](https://kubernetes.io/docs/concepts/workloads/controllers/), version 1.31.x baseline per [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md).
- Kubernetes documentation, [Assigning Pods to Nodes](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/) and [Taints and Tolerations](https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/).
- Kubernetes documentation, [Horizontal Pod Autoscaling](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/) and [Pod Disruption Budgets](https://kubernetes.io/docs/tasks/run-application/configure-pdb/).
- Kubernetes Autoscaler project, [Cluster Autoscaler](https://github.com/kubernetes/autoscaler) and [Vertical Pod Autoscaler](https://github.com/kubernetes/autoscaler/tree/master/vertical-pod-autoscaler).
- Karpenter project documentation, [karpenter.sh](https://karpenter.sh/).

**Knowledge check**

1. A clustered message broker needs a stable per-instance identity and a
   dedicated volume that follows each ordinal across reschedules. Which
   controller is correct, and what would go wrong using a Deployment
   instead?
2. What determines whether a pod is classified `Guaranteed`, `Burstable`,
   or `BestEffort`, and why does that classification matter during node
   memory pressure?
3. What is the practical difference between a taint/toleration pair and
   node affinity, and why are they often used together for dedicated node
   pools?
4. Why does a `PodDisruptionBudget` have no effect when a node crashes
   unexpectedly, but a very real effect when an operator runs
   `kubectl drain`?
5. Why is `InPlacePodVerticalScaling` not yet a full substitute for the
   Vertical Pod Autoscaler's restart-based update modes at the 1.31.x
   baseline?

## Hands-On Lab

**Objective:** Deploy a workload with defined QoS, enforce anti-affinity
and a PodDisruptionBudget, drive horizontal scaling under load, and
observe a drain being correctly blocked by the PDB.

### Prerequisites

- A running Kubernetes 1.31.x cluster (`kind` is sufficient) with at least
  three worker nodes.
- `kubectl` matching the cluster's minor version, and `hey` or `curl`
  available locally to generate load.
- `metrics-server` installed in the cluster (required for HPA in this
  lab).

### Procedure

1. Create a three-worker `kind` cluster and install `metrics-server`
   (with the `--kubelet-insecure-tls` patch `kind` clusters require).

   ```bash
   cat > kind-config.yaml <<'EOF'
   kind: Cluster
   apiVersion: kind.x-k8s.io/v1alpha4
   nodes:
     - role: control-plane
     - role: worker
     - role: worker
     - role: worker
   EOF
   kind create cluster --name workloads-lab --config kind-config.yaml --image kindest/node:v1.31.4

   kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
   kubectl patch deployment metrics-server -n kube-system --type='json' \
     -p='[{"op":"add","path":"/spec/template/spec/containers/0/args/-","value":"--kubelet-insecure-tls"}]'
   kubectl wait --for=condition=available --timeout=120s deployment/metrics-server -n kube-system
   ```

2. Deploy a workload with requests/limits, required anti-affinity, and a
   PodDisruptionBudget.

   ```bash
   kubectl create namespace workloads-lab
   cat > app.yaml <<'EOF'
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: demo-api
     namespace: workloads-lab
   spec:
     replicas: 3
     selector:
       matchLabels: { app: demo-api }
     template:
       metadata:
         labels: { app: demo-api }
       spec:
         affinity:
           podAntiAffinity:
             requiredDuringSchedulingIgnoredDuringExecution:
               - labelSelector: { matchLabels: { app: demo-api } }
                 topologyKey: kubernetes.io/hostname
         containers:
           - name: demo-api
             image: registry.k8s.io/e2e-test-images/agnhost:2.53
             args: ["netexec", "--http-port=8080"]
             resources:
               requests: { cpu: "100m", memory: "64Mi" }
               limits: { cpu: "200m", memory: "64Mi" }
             ports: [{ containerPort: 8080 }]
   ---
   apiVersion: v1
   kind: Service
   metadata:
     name: demo-api
     namespace: workloads-lab
   spec:
     selector: { app: demo-api }
     ports: [{ port: 80, targetPort: 8080 }]
   ---
   apiVersion: policy/v1
   kind: PodDisruptionBudget
   metadata:
     name: demo-api
     namespace: workloads-lab
   spec:
     minAvailable: 2
     selector:
       matchLabels: { app: demo-api }
   EOF
   kubectl apply -f app.yaml
   kubectl rollout status deployment/demo-api -n workloads-lab
   ```

   **Expected result:** three `Running` pods, each on a different node
   (confirm with `kubectl get pods -n workloads-lab -o wide`), because the
   required anti-affinity rule leaves the scheduler no other option.

3. Apply an HPA and confirm it reads live metrics.

   ```bash
   kubectl autoscale deployment demo-api -n workloads-lab \
     --cpu-percent=50 --min=3 --max=8
   kubectl get hpa -n workloads-lab -w
   ```

   **Expected result:** within a minute, the HPA row shows a numeric
   `TARGETS` value (for example `1%/50%`) instead of `<unknown>`,
   confirming metrics-server is being read successfully. Press Ctrl+C once
   confirmed.

4. Generate load against the Service and observe scale-out.

   ```bash
   kubectl run load-generator -n workloads-lab --rm -it --restart=Never \
     --image=busybox:1.36 -- /bin/sh -c \
     "while true; do wget -q -O- http://demo-api.workloads-lab.svc.cluster.local/; done"
   ```

   In a second terminal, watch replica count climb:

   ```bash
   kubectl get hpa -n workloads-lab demo-api -w
   ```

   **Expected result:** `REPLICAS` increases beyond 3 as CPU utilization
   crosses the 50% target. Stop the load generator with Ctrl+C in its
   terminal once you observe at least one scale-out event, then Ctrl+C the
   watch.

### Negative test

5. Attempt to drain a node holding a `demo-api` pod while only three
   replicas exist, and observe the PDB blocking eviction below the
   `minAvailable` floor.

   ```bash
   NODE=$(kubectl get pod -n workloads-lab -l app=demo-api \
     -o jsonpath='{.items[0].spec.nodeName}')
   kubectl drain "$NODE" --ignore-daemonsets --delete-emptydir-data --timeout=30s
   ```

   **Expected result:** the drain reports an eviction error referencing
   `Cannot evict pod as it would violate the pod's disruption budget`
   once removing that pod would drop available replicas below
   `minAvailable: 2` and the deployment cannot immediately reschedule a
   replacement onto the (now cordoned) node. Confirm the node was cordoned
   but the pod remains:

   ```bash
   kubectl get nodes
   kubectl get pods -n workloads-lab -o wide
   ```

6. Uncordon the node to restore normal scheduling.

   ```bash
   kubectl uncordon "$NODE"
   ```

### Cleanup

```bash
kubectl delete namespace workloads-lab
kind delete cluster --name workloads-lab
rm -f kind-config.yaml app.yaml
```

## Summary and Completion Checklist

Workload controllers encode identity and lifecycle semantics — Deployment
for fungible replicas, StatefulSet for ordered, identity-bearing
instances, DaemonSet for one-per-node agents, Job/CronJob for
run-to-completion work. Requests and limits are not administrative
overhead; they set QoS class, drive scheduler placement, and determine
eviction order under pressure. Affinity, anti-affinity, topology spread,
and taints/tolerations give an operator direct control over placement,
while HPA, Cluster Autoscaler/Karpenter, and PodDisruptionBudgets keep
capacity matched to demand without sacrificing availability during
routine disruption.

- [ ] Can choose the correct workload controller for a given identity and
      lifecycle requirement.
- [ ] Can explain how requests/limits determine QoS class and eviction
      order.
- [ ] Can configure affinity, anti-affinity, and topology spread
      constraints to control placement.
- [ ] Can configure an HPA and explain the difference between Cluster
      Autoscaler and Karpenter's provisioning models.
- [ ] Can set a PodDisruptionBudget and explain what it does and does not
      protect against.
- [ ] Completed the hands-on lab, including the PDB-blocked drain
      negative test, and performed cleanup.
