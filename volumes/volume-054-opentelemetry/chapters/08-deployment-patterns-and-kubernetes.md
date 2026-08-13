# Chapter 08: Deployment Patterns and Kubernetes

## Learning Objectives

- Compare agent and gateway Collector deployment patterns.
- Deploy the OpenTelemetry Operator on Kubernetes.
- Use auto-instrumentation injection.
- Scale the gateway tier.
- Complete a walkthrough for each deployment pattern.

## Theory and Architecture

Collectors deploy in two roles. An **agent** runs close to the workload (as a
DaemonSet/sidecar) to collect local telemetry and host metrics with low latency. A
**gateway** is a centralized, horizontally scaled Collector tier that agents forward to
for heavy processing (tail sampling, redaction) before export. On Kubernetes the
**OpenTelemetry Operator** manages Collectors via the `OpenTelemetryCollector` CRD and
provides **auto-instrumentation injection** via the `Instrumentation` CRD (annotate a
pod, get zero-code instrumentation). The pattern: **agents → gateway → backend**.

## Design Considerations

Use **agents** for local collection/host metrics and a **gateway** for centralized,
stateful processing (tail sampling needs a whole trace in one place). Scale the
**gateway** horizontally; keep agents light. Manage it all with the **Operator** on
Kubernetes.

## Implementation and Automation

The labs deploy the Operator, a Collector CR, and instrumentation injection.

## Validation and Troubleshooting

Confirm the patterns:

```text
Agent (DaemonSet/sidecar): local collection. Gateway (Deployment): central processing.
Operator: OpenTelemetryCollector CRD + Instrumentation CRD (auto-inject).
Flow: app -> agent -> gateway -> backend.
```

Common pitfalls: tail sampling on load-balanced gateways without trace affinity (split
traces); and agents doing heavy processing (resource contention).

## Security and Best Practices

Keep **agents lightweight**, centralize heavy processing on a **scalable gateway**, use
the **Operator** for lifecycle, ensure **trace affinity** to a single gateway instance
for tail sampling, and secure agent→gateway with TLS.

## Hands-On Lab

Deployment walkthroughs. **Shared prerequisites** — a Kubernetes cluster (kind/minikube)
and `kubectl`. **Cost:** none.

### Lab 8.1 — Install the Operator

**Objective:** Deploy the OpenTelemetry Operator.

```bash
kubectl apply -f https://github.com/open-telemetry/opentelemetry-operator/releases/latest/download/opentelemetry-operator.yaml
kubectl -n opentelemetry-operator-system get deploy
```

**Expected result:** the **operator deployment** running — CRDs available to manage
Collectors.

**Negative test:** create an `OpenTelemetryCollector` CR before the operator is ready;
the CR is **unhandled** — install the operator first.

**Rollback:** delete the operator manifest.

### Lab 8.2 — Deploy a gateway Collector

**Objective:** Create a gateway Collector via the CRD.

```yaml
apiVersion: opentelemetry.io/v1beta1
kind: OpenTelemetryCollector
metadata: { name: gateway }
spec:
  mode: deployment
  config:
    receivers: { otlp: { protocols: { grpc: {}, http: {} } } }
    processors: { batch: {} }
    exporters: { debug: {} }
    service: { pipelines: { traces: { receivers: [otlp], processors: [batch], exporters: [debug] } } }
```

**Expected result:** a **gateway Collector Deployment** managed by the operator — the
central tier.

**Negative test:** set `mode: daemonset` for the central gateway; a **deployment** scales
horizontally — daemonset is for agents.

**Rollback:** `kubectl delete opentelemetrycollector gateway`.

### Lab 8.3 — Auto-instrumentation injection

**Objective:** Inject zero-code instrumentation via the CRD.

```yaml
apiVersion: opentelemetry.io/v1alpha1
kind: Instrumentation
metadata: { name: python-instr }
spec: { exporter: { endpoint: http://gateway-collector:4318 }, python: {} }
# then annotate the pod: instrumentation.opentelemetry.io/inject-python: "true"
```

**Expected result:** annotated pods **auto-instrumented** with no image changes — the
Operator injection.

**Negative test:** rebuild every image to add the SDK; **annotation-based injection**
avoids that — use the Operator.

**Rollback:** delete the Instrumentation CR and annotation.

### Lab 8.4 — Scale the gateway

**Objective:** Horizontally scale the gateway tier.

```bash
kubectl scale deployment gateway-collector --replicas=3
kubectl get deploy gateway-collector -o jsonpath='{.status.readyReplicas}'
```

**Expected result:** **3 gateway replicas** ready — horizontal scale for the processing
tier.

**Negative test:** vertically scale one gateway forever; **scale out** replicas for
throughput and resilience.

**Rollback:** `kubectl scale deployment gateway-collector --replicas=1`.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Collectors deploy as lightweight agents (local collection) forwarding to a scalable
gateway (central processing), managed on Kubernetes by the Operator with
annotation-based auto-instrumentation injection. This chapter installed the Operator,
deployed a gateway, injected instrumentation, and scaled out.

- [ ] I can compare agent and gateway roles.
- [ ] I can install the Operator and deploy a Collector CR.
- [ ] I can inject auto-instrumentation via annotations.
- [ ] I can scale the gateway horizontally.
- [ ] I completed Labs 8.1–8.4 including each negative test.
