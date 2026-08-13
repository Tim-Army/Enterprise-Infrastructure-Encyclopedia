# Chapter 07: Cloud Native

## Learning Objectives

- Run containers on Container Service for Kubernetes (ACK).
- Deploy and scale workloads with kubectl.
- Build serverless functions with Function Compute.
- Design microservices patterns.
- Complete a walkthrough for each cloud-native topic.

## Theory and Architecture

Alibaba Cloud's cloud-native stack centers on **ACK (Container Service for Kubernetes)** — a managed
Kubernetes offering (standard, Pro, and serverless variants) that runs containerized workloads with
the standard Kubernetes API, integrated with Alibaba networking (VPC), storage (cloud disk/NAS/OSS via
CSI), load balancing (SLB/ALB via Ingress), and security. Operations use **kubectl** and Kubernetes
objects — Deployments, Services, Ingress, ConfigMaps, and Horizontal Pod Autoscaling. For
**serverless** event-driven code, **Function Compute** runs functions without managing servers,
triggered by events (OSS uploads, API Gateway, timers) and billed per invocation. **Microservices**
patterns — service discovery, API gateway, and messaging — are supported by ACK plus Alibaba's
Microservices Engine (MSE). The cloud-native theme is **containers and functions on managed
infrastructure**: run Kubernetes without operating the control plane, and event code without servers.
This chapter teaches each with a hands-on walkthrough (ACK deployment, autoscaling, serverless, and
microservices reasoning).

## Design Considerations

Use **ACK** for containerized/microservice workloads (managed control plane), **Function Compute** for
event-driven/bursty code. Scale with **HPA** on ACK. Expose services via **Ingress (SLB/ALB)**.
Isolate with **namespaces** and **RBAC**. Choose **serverless ACK** or **Function Compute** to avoid
node management where it fits. Design for **statelessness** and resilience.

## Implementation and Automation

The labs deploy on ACK, autoscale, and design serverless/microservices.

## Validation and Troubleshooting

Confirm the cloud-native model:

```text
ACK = managed Kubernetes (standard/Pro/serverless) integrated with VPC/storage/SLB. Operate: kubectl + Deployments/Services/Ingress/HPA. Function Compute = serverless functions (event-triggered, per-invocation billing).
Microservices: service discovery + API gateway + messaging (ACK + MSE). Theme: managed containers + serverless.
```

Common pitfalls: managing your own Kubernetes control plane (use **ACK**); and running always-on ECS
for rare event code (use **Function Compute**).

## Security and Best Practices

Run containers on **ACK** (managed), use **Function Compute** for event code, scale with **HPA**,
isolate with **namespaces/RBAC**, and expose via **Ingress**. Design stateless services. All work is
authorized administration.

## Hands-On Lab

Cloud-native walkthroughs. **Shared prerequisites** — `kubectl` (any cluster) or `python3` to model
logic. **Cost:** none.

### Lab 7.1 — Deploy a workload on ACK

**Objective:** Run containers on managed Kubernetes.

```bash
kubectl create namespace shop 2>/dev/null || echo "kubectl create namespace shop"
kubectl -n shop create deployment api --image=registry.example/api:1.0 --replicas=3 2>/dev/null || echo "kubectl create deployment api --replicas=3"
kubectl -n shop expose deployment api --port=80 --type=LoadBalancer 2>/dev/null || echo "expose via Service (SLB) / Ingress (ALB)"
```

**Expected result:** a **Deployment** exposed via a load-balanced Service on ACK — cloud-native
operation.

**Negative test:** run the app on a single pod with no Service; it's unreachable and fragile — use a
**Deployment + Service**.

**Rollback:** `kubectl delete namespace shop`.

### Lab 7.2 — Autoscale with HPA

**Objective:** Scale pods to load.

```python
python3 - <<'PY'
hpa={"target":"deployment/api","min":3,"max":20,"metric":"CPU 60%","behavior":"scale out on load, in when idle"}
for k,v in hpa.items(): print(f"{k:9}: {v}")
print("ACK HPA: automatically add/remove pods based on CPU/custom metrics")
PY
```

**Expected result:** a **Horizontal Pod Autoscaler** scaling on CPU — elastic containers.

**Negative test:** fix replicas at peak count always; you waste resources off-peak — use **HPA**.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.3 — Build a serverless function

**Objective:** Event-driven, no servers.

```python
python3 - <<'PY'
function={"runtime":"python3","trigger":"OSS object created (image uploaded)","action":"generate thumbnail -> write back to OSS",
          "billing":"per invocation + duration (no idle cost)"}
for k,v in function.items(): print(f"{k:9}: {v}")
print("Function Compute: event triggers a function; pay only when it runs")
PY
```

**Expected result:** a **Function Compute** function triggered by an OSS event — serverless processing.

**Negative test:** keep an ECS instance running 24/7 to occasionally resize images; that's wasteful —
use **Function Compute**.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.4 — Design a microservices pattern

**Objective:** Decompose and connect services.

```python
python3 - <<'PY'
services={"api-gateway":"single entry, routing + auth","order-service":"ACK deployment","payment-service":"ACK deployment",
          "messaging":"async events between services (decoupling)","discovery":"service registry (MSE)"}
for svc,role in services.items(): print(f"{svc:16}: {role}")
print("Microservices: gateway + independent services + async messaging + discovery")
PY
```

**Expected result:** a **microservices** design (gateway, services, messaging, discovery) — cloud-native
architecture.

**Negative test:** build a single monolith and call it microservices; decompose into **independent,
messaged** services.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Alibaba Cloud cloud-native runs containers on managed ACK (kubectl, HPA, Ingress) and event code on
serverless Function Compute, with microservices patterns via ACK and MSE — managed containers and
serverless without operating infrastructure.

- [ ] I can deploy a workload on ACK.
- [ ] I can autoscale with HPA.
- [ ] I can build a serverless function.
- [ ] I can design a microservices pattern.
- [ ] I completed Labs 7.1–7.4 including each negative test.
