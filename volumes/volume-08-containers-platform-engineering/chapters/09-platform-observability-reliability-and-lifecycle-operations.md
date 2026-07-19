# Chapter 09: Platform Observability, Reliability, and Lifecycle Operations

![Lab topology for this chapter: demo-api runs 3 replicas with a PodDisruptionBudget requiring minAvailable 2, observed by kube-state-metrics through Prometheus. A tightly scoped Chaos Mesh experiment (mode: one) kills exactly one demo-api pod; a replacement schedules within seconds and total pod count never drops below 2. As a negative test, an over-broad experiment (mode: all) force-kills all three demo-api pods nearly simultaneously, briefly dropping available replicas to 0 despite the minAvailable 2 PDB — because PodChaos kills pods directly rather than through the eviction subresource that PDBs actually govern, and PDBs protect only voluntary, eviction-based disruption.](../../../diagrams/volume-08-containers-platform-engineering/chapter-09-chaos-mesh-pdb-scope-topology.svg)

*Figure 9-1. Topology used throughout this chapter's Hands-On Lab: a Prometheus-observed workload where a scoped chaos experiment respects the PodDisruptionBudget and an over-broad one bypasses it entirely.*

## Learning Objectives

- Assemble the Prometheus-based metrics stack (`kube-state-metrics`,
  node-exporter, metrics-server) and explain why each component covers a
  distinct signal.
- Instrument workloads for distributed tracing and log correlation using
  OpenTelemetry, and explain the collector's role as a vendor-neutral
  pipeline.
- Define platform-level SLOs and error budgets, and connect them to the
  progressive-delivery gates from [Chapter 07](07-cloud-native-delivery-gitops-and-software-supply-chains.md).
- Run a controlled chaos experiment to validate a resilience assumption,
  and plan a fleet-wide cluster upgrade using Cluster API.
- Attribute Kubernetes cost to workloads and teams, and apply the
  resulting data to a capacity-planning decision.

## Theory and Architecture

Every prior chapter in this volume built a capability: workloads,
networking, storage, identity, delivery, and a self-service platform
layer on top. This closing chapter covers the discipline that keeps all
of it observably healthy and correctly sized over time — the operational
layer a platform team owns on behalf of every tenant, whether or not any
individual tenant ever notices it is there.

### The metrics stack: three distinct signal sources

Kubernetes observability commonly gets flattened into "Prometheus," but
production clusters run at least three distinct metrics-producing
components, each answering a different question:

| Component | Answers | Consumed by |
| --- | --- | --- |
| **metrics-server** | Current CPU/memory usage per pod/node, no history | `kubectl top`, the HorizontalPodAutoscaler ([Chapter 03](03-kubernetes-workloads-scheduling-and-capacity.md)) |
| **kube-state-metrics** | The *state* of Kubernetes objects as metrics — deployment replica counts, pod phase, PVC status, node conditions — not resource usage | Prometheus scraping, dashboards, alerting on object-level conditions |
| **node-exporter** | Host-level OS metrics — disk I/O, filesystem usage, network interface counters, kernel-level statistics | Prometheus scraping, node-health alerting and capacity planning |

metrics-server deliberately holds no history and exists only to serve the
narrow, latency-sensitive `metrics.k8s.io` API the autoscaler needs;
Prometheus, scraping `kube-state-metrics` and `node-exporter` on a
schedule, is the durable, queryable time-series store everything else —
dashboards, alerting, the canary Analysis step from [Chapter 07](07-cloud-native-delivery-gitops-and-software-supply-chains.md) — is built
on. Conflating the two is a common design mistake: pointing an HPA at
Prometheus data (via the Prometheus Adapter) is reasonable for custom
metrics, but expecting metrics-server to answer a historical or
object-state question it was never built to hold is not.

### Logging and tracing

**Logging** in Kubernetes has no built-in aggregation — kubelet retains
each container's stdout/stderr locally and rotates it, full stop. A
production logging pipeline needs a node-level collector (Fluent Bit or
the Fluentd/Fluent Bit successor ecosystem, or an OpenTelemetry Collector
running in agent mode) running as a DaemonSet ([Chapter 03](03-kubernetes-workloads-scheduling-and-capacity.md)) that tails
each node's container log files, enriches each line with Kubernetes
metadata (pod, namespace, labels — read from the API server or the
kubelet), and ships to a backend such as **Loki** (label-indexed,
deliberately not full-text-indexed, for cost-efficient high-volume
storage) or a traditional Elasticsearch-backed stack.

**Distributed tracing** answers a question logs and metrics cannot: which
downstream call, across how many services, made this one request slow?
**OpenTelemetry** has become the vendor-neutral standard for this signal
— an SDK instruments (or auto-instruments, via the **OpenTelemetry
Operator**'s injection of language-specific auto-instrumentation into a
pod) an application to emit spans, and an **OpenTelemetry Collector**
(deployable as a DaemonSet for node-local collection, a Deployment as a
central gateway, or both in a tiered topology) receives, batches, and
exports that telemetry — traces, metrics, and logs alike — to any
compatible backend (Jaeger, Tempo, a commercial APM vendor) without the
application ever coupling directly to a specific vendor's SDK. This
vendor-neutrality is the point: instrumentation written once against the
OpenTelemetry API survives a backend migration untouched.

### SLOs, error budgets, and the platform's reliability contract

[Volume I](../../volume-01-enterprise-engineering-foundations/README.md) introduced Service Level Objectives and error budgets as a
general reliability vocabulary; a platform team applies that vocabulary
to the platform itself, not just to individual applications. A platform
SLO answers "how reliable is the *platform surface* a tenant depends on"
— API server availability and latency, scheduling latency for a new pod,
ingress/gateway data-plane availability ([Chapter 04](04-kubernetes-networking-service-delivery-and-traffic-policy.md)), CSI provisioning
latency ([Chapter 05](05-kubernetes-storage-and-stateful-platforms.md)) — distinct from, and additive to, whatever SLOs an
individual application team defines for its own service on top of that
platform. The **error budget** this produces is what makes [Chapter 07](07-cloud-native-delivery-gitops-and-software-supply-chains.md)'s
canary Analysis gates a genuinely risk-calibrated control rather than an
arbitrary threshold: a canary's failure condition should be defined in
terms of the same SLO the on-call team is paged against, so a rollout
that is aborted automatically is aborted for exactly the reason a human
would also have rolled it back manually.

### Chaos engineering

An SLO is a claim about behavior under failure; **chaos engineering**
tests whether that claim is actually true by deliberately injecting
controlled failure — killing a pod, adding network latency, exhausting a
node's memory — into a system, typically starting in a non-production
environment and, at higher maturity, in production itself under tight
blast-radius controls. **Chaos Mesh** and **LitmusChaos** both implement
this as Kubernetes-native CRDs (`PodChaos`, `NetworkChaos`, `StressChaos`)
reconciled by an in-cluster controller, so an experiment is defined,
version-controlled, and audited the same way any other platform resource
in this volume is. The output of a chaos experiment is not "did it
break" — it is "did our monitoring detect it, did our alerting page the
right team, and did our automated remediation (a PodDisruptionBudget from
[Chapter 03](03-kubernetes-workloads-scheduling-and-capacity.md), a health-checked LoadBalancer from [Chapter 04](04-kubernetes-networking-service-delivery-and-traffic-policy.md)) behave as
designed" — validating the *system*, not just the *component*.

### Fleet-scale cluster lifecycle operations

[Chapter 02](02-kubernetes-architecture-and-cluster-lifecycle.md) covered upgrading a single cluster. A platform team operating
many clusters — per-environment, per-region, or per-tenant in a
hard-multi-tenancy model ([Chapter 08](08-internal-developer-platforms-and-platform-products.md)) — needs that same version-skew-
respecting upgrade discipline applied consistently at fleet scale.
**Cluster API (CAPI)** manages Kubernetes clusters themselves as
Kubernetes objects (`Cluster`, `MachineDeployment`, `MachineSet`) on a
management cluster, applying the same declarative, reconciled model this
entire volume has used for workloads to the clusters that host them —
a fleet-wide version bump becomes a coordinated set of object updates
rather than a per-cluster manual runbook. **Karmada** and comparable
multi-cluster orchestration projects extend workload placement itself
(not just cluster lifecycle) across a fleet, propagating a single
workload definition to a policy-selected subset of member clusters.

### Cost attribution

Kubernetes' shared-infrastructure model — many workloads sharing nodes,
storage, and network egress — makes naive per-workload cost attribution
difficult; a cloud bill shows node-hours and storage-GB, not "team
payments spent $4,200 last month." **Kubecost** and the CNCF's
**OpenCost** specification address this by combining actual cloud pricing
data with each workload's requested (and, optionally, actually consumed)
resources to allocate a defensible cost figure per namespace, label, or
team — turning the requests set back in [Chapter 03](03-kubernetes-workloads-scheduling-and-capacity.md) into a financial input
as well as a scheduling one, and giving a platform team the data to have
a substantive capacity conversation instead of an anecdotal one.

## Design Considerations

**Alert on symptoms your SLO defines, not on every anomaly a dashboard
can show.** A metrics stack capable of producing thousands of time series
tempts teams into alerting on all of them; the result is alert fatigue
that trains on-call engineers to ignore paging, the opposite of the
reliability goal. Alert on burn rate against a defined error budget and a
small number of platform-level symptom signals (API server latency,
ingress error rate); use the broader metric surface for dashboards and
investigation, not for paging.

**Log aggregation cost scales with retention and indexing choice, not
just volume.** A full-text-indexed backend (classic Elasticsearch
patterns) gives the richest ad hoc query experience at the highest
storage and compute cost; a label-indexed backend like Loki trades some
query flexibility for an order-of-magnitude cost reduction at high
volume, which matters considerably once a platform's log volume scales
with tenant count rather than a single application's traffic. Tune
retention per namespace or log level rather than applying one blanket
retention window — a payments audit trail and a debug-level log from a
development namespace do not warrant the same retention economics.

**Distributed tracing sampling is a cost-vs-completeness trade-off, not
an afterthought.** Head-based sampling (deciding whether to keep a trace
at its start) is cheap but can discard the very trace an incident needed
if the sampling decision happened before the slow/erroring path was
known. Tail-based sampling (buffering and deciding after a trace
completes, commonly done in the OpenTelemetry Collector's tail-sampling
processor) preserves interesting traces (errors, high latency)
preferentially at the cost of buffering overhead in the collector tier —
the right default for any environment where "the trace I actually need"
and "the traces sampling kept" cannot be allowed to diverge.

**Chaos experiments need a defined, shrinking blast radius before they
need production.** Running an untested `NetworkChaos` experiment
directly against a production namespace is itself a reliability risk; the
progression from a scoped staging experiment to a tightly bounded,
opt-in production experiment (a single canary pod, a single availability
zone, an explicit time window with an automatic abort condition) is what
turns chaos engineering into a controlled validation practice rather than
a self-inflicted incident.

**Fleet cluster lifecycle management earns its complexity at a specific
scale, not from day one.** Cluster API's declarative, reconciled cluster
management is a substantial improvement over N independent `kubeadm`
runbooks once a platform operates enough clusters that manual,
per-cluster upgrade tracking becomes the actual bottleneck — but it adds
a management cluster as new infrastructure to operate and secure in its
own right. A platform running two or three clusters may reasonably defer
CAPI adoption until fleet size actually justifies it, using the
[Chapter 02](02-kubernetes-architecture-and-cluster-lifecycle.md) single-cluster upgrade discipline repeated manually in the
interim.

**Cost data changes behavior only when it reaches the team that can act
on it.** A cost dashboard visible only to the platform team documents
spend without influencing it; routing per-team cost allocation back to
the owning team — ideally alongside the same Backstage catalog entry
from [Chapter 08](08-internal-developer-platforms-and-platform-products.md) a team already checks — is what turns cost attribution
into an input the requesting team actually weighs against the resource
requests it sets in [Chapter 03](03-kubernetes-workloads-scheduling-and-capacity.md), rather than a report nobody with the
power to change anything reads.

## Implementation and Automation

### Installing the core metrics stack via the kube-prometheus-stack chart

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm upgrade --install kube-prometheus-stack prometheus-community/kube-prometheus-stack \
  --namespace monitoring --create-namespace \
  --set kube-state-metrics.enabled=true \
  --set prometheus-node-exporter.enabled=true \
  --set prometheus.prometheusSpec.retention=15d
```

```bash
kubectl get pods -n monitoring
# Confirm kube-state-metrics is reporting object state, distinct from
# metrics-server's live resource-usage numbers.
kubectl port-forward -n monitoring svc/kube-prometheus-stack-prometheus 9090:9090 &
curl -s 'http://localhost:9090/api/v1/query?query=kube_deployment_status_replicas' | jq '.data.result[0]'
```

### OpenTelemetry Collector as a tiered pipeline with tail-based sampling

```yaml
apiVersion: opentelemetry.io/v1beta1
kind: OpenTelemetryCollector
metadata:
  name: gateway-collector
  namespace: observability
spec:
  mode: deployment
  config:
    receivers:
      otlp:
        protocols: { grpc: {}, http: {} }
    processors:
      tail_sampling:
        decision_wait: 10s
        policies:
          - name: sample-errors
            type: status_code
            status_code: { status_codes: ["ERROR"] }
          - name: sample-slow
            type: latency
            latency: { threshold_ms: 500 }
          - name: sample-baseline
            type: probabilistic
            probabilistic: { sampling_percentage: 5 }
    exporters:
      otlp/tempo:
        endpoint: tempo.observability.svc:4317
        tls: { insecure: true }
    service:
      pipelines:
        traces:
          receivers: [otlp]
          processors: [tail_sampling]
          exporters: [otlp/tempo]
```

### An SLO-driven PrometheusRule alerting on error-budget burn rate

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: checkout-api-slo
  namespace: payments
spec:
  groups:
    - name: checkout-api-availability-slo
      rules:
        - alert: CheckoutAPIErrorBudgetBurnFast
          expr: |
            (
              sum(rate(http_requests_total{app="checkout-api",status=~"5.."}[5m]))
              /
              sum(rate(http_requests_total{app="checkout-api"}[5m]))
            ) > (14.4 * 0.001)
          for: 2m
          labels: { severity: page }
          annotations:
            summary: "checkout-api burning its 99.9% availability SLO error budget fast"
```

A `14.4x` burn-rate multiplier against a 0.1% (99.9%) error budget is a
standard fast-burn detection window — it pages when the current error
rate would exhaust a full month's error budget in about two days,
distinct from a slower, non-paging burn-rate alert tuned to a longer
window.

### A scoped chaos experiment with Chaos Mesh

```yaml
apiVersion: chaos-mesh.org/v1alpha1
kind: PodChaos
metadata:
  name: checkout-api-pod-kill
  namespace: payments
spec:
  action: pod-kill
  mode: one
  selector:
    namespaces: ["payments"]
    labelSelectors: { app: checkout-api }
  scheduler:
    cron: "@every 10m"
  duration: "30s"
```

```bash
kubectl apply -f pod-kill-experiment.yaml
# Confirm the PodDisruptionBudget and alerting from Chapters 03/09
# actually behaved as designed under the injected failure.
kubectl get events -n payments --field-selector reason=Killing
kubectl get pdb -n payments checkout-api
```

### Fleet upgrade orchestration with Cluster API

```bash
clusterctl init --infrastructure aws

# A fleet-wide minor-version bump becomes a declarative object update,
# reconciled with the same rolling-replacement discipline as a
# MachineDeployment's own rollout strategy.
kubectl patch machinedeployment production-workers \
  --type merge -p '{"spec":{"template":{"spec":{"version":"v1.31.4"}}}}'
kubectl get machinedeployment production-workers -w
```

### Cost attribution with OpenCost

```bash
helm repo add opencost https://opencost.github.io/opencost-helm-chart
helm upgrade --install opencost opencost/opencost --namespace opencost --create-namespace

kubectl port-forward -n opencost svc/opencost 9003:9003 &
curl -s 'http://localhost:9003/allocation/compute?window=7d&aggregate=namespace' | \
  jq '.data[0] | to_entries | map({namespace: .key, cost: .value.totalCost}) | sort_by(-.cost)'
```

## Validation and Troubleshooting

```bash
# Is Prometheus actually scraping every expected target?
kubectl port-forward -n monitoring svc/kube-prometheus-stack-prometheus 9090:9090 &
curl -s http://localhost:9090/api/v1/targets | jq '.data.activeTargets[] | select(.health!="up")'

# Is the OpenTelemetry Collector receiving and exporting spans?
kubectl logs -n observability deploy/gateway-collector-collector --tail=50

# Current error-budget burn against a defined SLO.
curl -s 'http://localhost:9090/api/v1/query?query=ALERTS{alertname="CheckoutAPIErrorBudgetBurnFast"}'
```

| Symptom | Likely cause | Diagnostic |
| --- | --- | --- |
| Dashboards show gaps or flat lines for a workload's metrics | Prometheus scrape target down, or `ServiceMonitor`/`PodMonitor` selector mismatch | `curl .../api/v1/targets`; confirm `ServiceMonitor` label selector matches the target Service |
| Traces exist in the collector's logs but never reach the backend | Exporter endpoint misconfigured, or the backend's ingestion is rejecting due to a schema/version mismatch | Collector logs at debug level; backend ingestion logs |
| An SLO alert never fires despite a known outage | Burn-rate window too long for the outage's duration, or the underlying query's label selector no longer matches after a workload rename | Manually run the alert's PromQL expression against the outage window |
| Chaos experiment causes a wider outage than intended | `mode`/`selector` scoped too broadly, or no `duration`/`scheduler` bound limiting blast radius | `kubectl describe podchaos`; tighten `selector` and always set an explicit `duration` |
| A `MachineDeployment` fleet upgrade stalls partway | A member cluster's PodDisruptionBudgets ([Chapter 03](03-kubernetes-workloads-scheduling-and-capacity.md)) block node replacement, mirroring the single-cluster drain behavior from [Chapter 02](02-kubernetes-architecture-and-cluster-lifecycle.md) | `kubectl get machines`; `kubectl get pdb -A` on the affected member cluster |

## Security and Best Practices

- Scrape and store metrics, logs, and traces with the same RBAC and
  NetworkPolicy discipline ([Chapter 06](06-kubernetes-identity-configuration-policy-and-security.md)/04) as any other platform data —
  observability backends routinely aggregate sensitive request metadata
  and deserve access controls commensurate with that.
- Redact or avoid emitting sensitive fields (tokens, PII) into trace
  attributes and log lines at the instrumentation layer; a tracing
  backend is not an approved data store for the material [Chapter 06](06-kubernetes-identity-configuration-policy-and-security.md)
  restricts through Secrets and RBAC.
- Define platform SLOs and alert on error-budget burn rate rather than
  raw thresholds, and route paging alerts only for symptoms with a
  defined, actionable response.
- Scope every chaos experiment with an explicit `duration`, a narrow
  `selector`, and — for anything touching production — a pre-agreed abort
  condition and on-call awareness before it runs.
- Treat a management cluster running Cluster API as Tier-0
  infrastructure: it holds the credentials and reconciliation authority
  to reshape every member cluster's nodes, and should receive the
  strictest RBAC and network exposure controls in the fleet.
- Publish cost attribution data to the owning team, not only to the
  platform team, so it becomes an input to that team's own resource
  request decisions rather than a report nobody acts on.
- Rehearse fleet-wide upgrade rollback the same way [Chapter 02](02-kubernetes-architecture-and-cluster-lifecycle.md) rehearses
  etcd restore — a Cluster API `MachineDeployment` rollout that goes
  wrong at fleet scale is a materially larger incident than a single
  cluster's stalled `kubeadm upgrade`.

## References and Knowledge Checks

**Authoritative references**

- Kubernetes documentation, [Tools for Monitoring Resources](https://kubernetes.io/docs/tasks/debug/debug-cluster/resource-usage-monitoring/), version 1.31.x baseline per [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md).
- Prometheus documentation, [prometheus.io/docs](https://prometheus.io/docs/); Grafana Loki documentation, [grafana.com/docs/loki](https://grafana.com/docs/loki/).
- OpenTelemetry documentation, [opentelemetry.io/docs](https://opentelemetry.io/docs/), including the [Operator](https://opentelemetry.io/docs/kubernetes/operator/) and [Collector](https://opentelemetry.io/docs/collector/).
- Google SRE Workbook, [Alerting on SLOs](https://sre.google/workbook/alerting-on-slos/).
- Chaos Mesh documentation, [chaos-mesh.org/docs](https://chaos-mesh.org/docs/); Cluster API documentation, [cluster-api.sigs.k8s.io](https://cluster-api.sigs.k8s.io/); OpenCost documentation, [opencost.io](https://www.opencost.io/docs/).

**Knowledge check**

1. Why does the HorizontalPodAutoscaler read from metrics-server rather
   than Prometheus for its default resource-based metrics, and what
   would be lost by pointing it at Prometheus for every metric type?
2. What distinct problem does distributed tracing solve that neither
   aggregated logs nor time-series metrics answer on their own?
3. What does a `14.4x` burn-rate multiplier against a monthly error
   budget actually represent, and why is it used for a fast-page alert
   rather than a fixed error-rate threshold?
4. Why must a chaos experiment define an explicit `duration` and a
   narrowly scoped `selector` before it is safe to run, even in a
   non-production environment?
5. Why does cost attribution data need to reach the owning application
   team, not just the platform team, to actually change resource-request
   behavior?

## Hands-On Lab

**Objective:** Install the Prometheus stack, deploy an instrumented
workload, define and alert on an SLO burn rate, run a scoped chaos
experiment while observing the PodDisruptionBudget respond, and confirm
an over-broad chaos selector is correctly blocked as a negative test.

### Prerequisites

- A `kind` cluster running Kubernetes 1.31.x with at least two worker
  nodes.
- `helm`, `kubectl`, and `jq` installed locally.
- Network access to pull the `kube-prometheus-stack` and `chaos-mesh`
  Helm charts on first run.

### Procedure

1. Create the cluster and install the Prometheus stack.

   ```bash
   kind create cluster --name observability-lab --image kindest/node:v1.31.4
   helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
   helm repo update
   helm upgrade --install kube-prometheus-stack prometheus-community/kube-prometheus-stack \
     --namespace monitoring --create-namespace \
     --set prometheus.prometheusSpec.retention=1d \
     --wait --timeout 5m
   ```

2. Deploy a workload with a PodDisruptionBudget, matching [Chapter 03](03-kubernetes-workloads-scheduling-and-capacity.md)'s
   pattern, that Prometheus can observe.

   ```bash
   kubectl create namespace observability-lab
   cat > app.yaml <<'EOF'
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: demo-api
     namespace: observability-lab
   spec:
     replicas: 3
     selector: { matchLabels: { app: demo-api } }
     template:
       metadata: { labels: { app: demo-api } }
       spec:
         containers:
           - name: demo-api
             image: registry.k8s.io/e2e-test-images/agnhost:2.53
             args: ["netexec", "--http-port=8080"]
   ---
   apiVersion: policy/v1
   kind: PodDisruptionBudget
   metadata:
     name: demo-api
     namespace: observability-lab
   spec:
     minAvailable: 2
     selector: { matchLabels: { app: demo-api } }
   EOF
   kubectl apply -f app.yaml
   kubectl rollout status deployment/demo-api -n observability-lab
   ```

3. Confirm `kube-state-metrics` is reporting this Deployment's state
   through Prometheus.

   ```bash
   kubectl port-forward -n monitoring svc/kube-prometheus-stack-prometheus 9090:9090 &
   sleep 3
   curl -s 'http://localhost:9090/api/v1/query?query=kube_deployment_status_replicas{namespace="observability-lab"}' | jq '.data.result'
   ```

   **Expected result:** a result showing `demo-api` with a value of `3`,
   confirming kube-state-metrics is exposing object state, not resource
   usage, for this workload.

4. Install Chaos Mesh and run a tightly scoped pod-kill experiment
   against exactly one `demo-api` pod.

   ```bash
   helm repo add chaos-mesh https://charts.chaos-mesh.org
   helm upgrade --install chaos-mesh chaos-mesh/chaos-mesh \
     --namespace chaos-mesh --create-namespace \
     --set chaosDaemon.runtime=containerd \
     --set chaosDaemon.socketPath=/run/containerd/containerd.sock \
     --wait --timeout 5m

   cat > pod-kill.yaml <<'EOF'
   apiVersion: chaos-mesh.org/v1alpha1
   kind: PodChaos
   metadata:
     name: demo-api-kill-one
     namespace: observability-lab
   spec:
     action: pod-kill
     mode: one
     duration: "10s"
     selector:
       namespaces: ["observability-lab"]
       labelSelectors: { app: demo-api }
   EOF
   kubectl apply -f pod-kill.yaml
   kubectl get pods -n observability-lab -w
   ```

   **Expected result:** exactly one `demo-api` pod terminates and a
   replacement is scheduled within seconds; total pod count never drops
   below 2 at any observed instant, consistent with the
   `minAvailable: 2` PodDisruptionBudget. Press Ctrl+C once you observe
   the replacement pod reach `Running`.

### Negative test

5. Attempt an experiment with an over-broad selector matching *all*
   `demo-api` pods simultaneously (`mode: all`) and confirm the
   PodDisruptionBudget still prevents the platform's own eviction paths
   from taking the workload fully offline, while directly observing that
   an unscoped chaos action can still momentarily violate `minAvailable`
   through force-kill (not eviction) — which is exactly why the Design
   Considerations section requires a narrow `selector`/`mode` rather than
   relying on the PDB alone.

   ```bash
   cat > pod-kill-all.yaml <<'EOF'
   apiVersion: chaos-mesh.org/v1alpha1
   kind: PodChaos
   metadata:
     name: demo-api-kill-all
     namespace: observability-lab
   spec:
     action: pod-kill
     mode: all
     duration: "10s"
     selector:
       namespaces: ["observability-lab"]
       labelSelectors: { app: demo-api }
   EOF
   kubectl apply -f pod-kill-all.yaml
   kubectl get pods -n observability-lab -w
   ```

   **Expected result:** all three `demo-api` pods are force-killed nearly
   simultaneously, briefly dropping available replicas to 0 despite the
   `minAvailable: 2` PDB — because `PodChaos` kills pods directly rather
   than going through the API server's eviction subresource that PDBs
   govern, PDBs protect against *voluntary, eviction-based* disruption
   ([Chapter 03](03-kubernetes-workloads-scheduling-and-capacity.md)) and do not protect against this kind of direct chaos
   action. This is the intended lesson: confirm it by deleting the
   overly broad experiment immediately and comparing recovery time to
   step 4's scoped version.

   ```bash
   kubectl delete -f pod-kill-all.yaml
   ```

### Cleanup

```bash
kubectl delete namespace observability-lab
helm uninstall chaos-mesh -n chaos-mesh
helm uninstall kube-prometheus-stack -n monitoring
kubectl delete namespace chaos-mesh monitoring
kill %1 2>/dev/null   # stop the port-forward background job
kind delete cluster --name observability-lab
rm -f app.yaml pod-kill.yaml pod-kill-all.yaml
```

## Summary and Completion Checklist

Platform observability rests on three distinct metrics signals
(metrics-server, kube-state-metrics, node-exporter), a log-aggregation
pipeline Kubernetes does not provide natively, and OpenTelemetry as the
vendor-neutral tracing standard — together giving a platform team the
data an SLO and its error budget are defined against. Chaos engineering
validates those reliability claims directly, and the negative test in
this chapter's lab demonstrates concretely that a PodDisruptionBudget
protects against voluntary eviction, not against every failure mode a
chaos experiment can inject — a distinction worth carrying back through
every prior chapter's availability guarantees. Cluster API extends
[Chapter 02](02-kubernetes-architecture-and-cluster-lifecycle.md)'s single-cluster upgrade discipline to fleet scale, and cost
attribution turns the resource requests set back in [Chapter 03](03-kubernetes-workloads-scheduling-and-capacity.md) into data
a team can act on.

- [ ] Can explain the distinct role of metrics-server, kube-state-metrics,
      and node-exporter.
- [ ] Can describe OpenTelemetry's collector-based, vendor-neutral
      tracing pipeline and the head-vs-tail sampling trade-off.
- [ ] Can define a platform SLO and an error-budget burn-rate alert.
- [ ] Can scope and run a chaos experiment and correctly state what a
      PodDisruptionBudget does and does not protect against.
- [ ] Can describe how Cluster API extends single-cluster upgrade
      discipline to fleet scale, and how cost attribution informs
      capacity planning.
- [ ] Completed the hands-on lab, including the unscoped chaos negative
      test, and performed cleanup.
