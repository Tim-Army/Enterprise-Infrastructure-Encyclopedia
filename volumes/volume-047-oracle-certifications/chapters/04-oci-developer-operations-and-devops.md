# Chapter 04: OCI Developer, Operations, and DevOps

## Learning Objectives

- Explain the OCI Developer, Operations, and DevOps professional credentials.
- Summarize their exam topics.
- Apply cloud-native development on OCI: Functions, API Gateway, OKE, events.
- Apply observability and DevOps automation (Resource Manager, pipelines).
- Complete a per-topic walkthrough for each area.

## Theory and Architecture

Three professional credentials cover building and running applications on OCI:

- **OCI Developer Professional (1Z0-1084)** — cloud-native development: **OCI
  Functions** (serverless), **API Gateway**, **Container Engine for Kubernetes
  (OKE)**, **Container Registry**, **Events/Streaming/Notifications**, and the
  **SDK/CLI** with **resource principals**.
- **OCI Operations / Observability Professional** — **Monitoring**, **Logging**,
  **Events**, **Alarms**, and OS management for running workloads.
- **OCI DevOps Professional** — the **DevOps service** (build and deploy
  pipelines), **Resource Manager** (managed Terraform / infrastructure as code),
  and automation.

## Design Considerations

The Developer credential is about **cloud-native patterns** (serverless,
containers, events, APIs); Operations is about **observing and running** workloads;
DevOps is about **automating** delivery and infrastructure. Learn how OCI's
services map to the patterns you know from other clouds — Functions ≈ serverless,
OKE ≈ managed Kubernetes, Resource Manager ≈ managed Terraform — and use
**resource principals** so code authenticates without stored keys.

## Implementation and Automation

The labs below use OCI CLI/service patterns and IaC (Resource Manager/Terraform)
to cover development, observability, and DevOps automation.

## Validation and Troubleshooting

Confirm the blueprints before studying:

```text
education.oracle.com > OCI Developer (1Z0-1084) / Operations / DevOps Professional:
  - Developer: Functions, API Gateway, OKE, Container Registry, events/streaming, SDK/CLI
  - Operations: Monitoring, Logging, Events, Alarms
  - DevOps: DevOps pipelines, Resource Manager (Terraform)
```

Common pitfalls: storing API keys in code (use **resource principals**); confusing
**Events** (react to resource changes) with **Streaming** (Kafka-like ingest); and
hand-provisioning instead of **Resource Manager** IaC.

## Security and Best Practices

Authenticate services with **resource/instance principals** (no stored keys);
build **serverless/containerized** apps that scale to zero/out; instrument with
**Monitoring/Logging** and alarm on SLOs; and manage infrastructure as code with
**Resource Manager (Terraform)** through **DevOps pipelines**.

## References and Knowledge Checks

- education.oracle.com: OCI Developer, Operations, and DevOps exam topics; OCI Functions, OKE, Resource Manager, and Observability docs.

**Knowledge checks**

1. How should OCI code authenticate to OCI services without stored keys?
2. What is the difference between OCI Events and OCI Streaming?
3. What does Resource Manager provide for infrastructure as code?

## Hands-On Lab

Per-topic walkthroughs — Developer, Operations, and DevOps areas. OCI CLI/IaC
patterns are illustrative.

**Shared prerequisites** — a shell; an OCI account for execution; `python3`.
**Cost:** none (Always Free where possible).

### Lab 4.1 — Developer: serverless Functions

**Objective:** Describe an OCI Function and its trigger.

```bash
python3 - <<'PY'
print("OCI Functions: Fn-based serverless; deploy a function, invoke via API Gateway or Events.")
print("Scales to zero; pay per invocation; uses resource principals for OCI access.")
PY
```

**Expected result:** the serverless model (Functions + triggers + resource
principals) — a Developer topic.

**Negative test:** run an always-on VM for an occasional task; **Functions** scale
to zero — use serverless for event-driven work.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.2 — Developer: API Gateway

**Objective:** Front a backend with API Gateway.

```bash
python3 - <<'PY'
print("API Gateway: routes/auth/rate-limits requests to backends (Functions, OKE, HTTP).")
print("Add: authentication (JWT/OAuth), request/response transformation, usage plans.")
PY
```

**Expected result:** the API Gateway role (routing, auth, rate limiting) — a
Developer topic.

**Negative test:** expose a Function directly to the internet unauthenticated; front
it with **API Gateway** for auth and throttling.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.3 — Developer: OKE (Kubernetes) and Container Registry

**Objective:** Describe deploying containers on OKE.

```bash
python3 - <<'PY'
print("OCIR (Container Registry): store images. OKE: managed Kubernetes to run them.")
print("Flow: build image -> push to OCIR -> deploy to OKE (Deployment/Service).")
PY
```

**Expected result:** the container workflow (OCIR → OKE) — the Kubernetes area of
the Developer exam (pairs with Volume XLI).

**Negative test:** run containers on bare VMs and hand-manage them; **OKE**
provides managed orchestration — use it.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.4 — Developer: Events, Streaming, Notifications

**Objective:** Choose the right eventing service.

```bash
python3 - <<'PY'
choose = {"React to a resource change (bucket upload)":"Events -> Function",
          "High-volume message ingest (Kafka-like)":"Streaming",
          "Send an email/alert":"Notifications (topics/subscriptions)"}
for need,svc in choose.items(): print(f"{need:44} -> {svc}")
PY
```

**Expected result:** each need mapped to Events/Streaming/Notifications — the
event-driven area of the Developer exam.

**Negative test:** use Streaming to send an admin email; **Notifications** is the
pub/sub-to-endpoint service — match the tool.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.5 — Operations: Monitoring, Logging, Alarms

**Objective:** Define an observability baseline with an alarm.

```bash
python3 - <<'PY'
print("Monitoring: metrics (CPU, memory, custom) with MQL queries.")
print("Logging: service/audit/custom logs -> Logging + Log Search.")
print("Alarm: e.g., CpuUtilization > 85% for 5m -> Notifications topic.")
PY
```

**Expected result:** the Monitoring/Logging/Alarm baseline — the Operations
credential's core.

**Negative test:** operate with no alarms; define **alarms on SLOs** routed to
Notifications — don't watch dashboards manually.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.6 — DevOps: Resource Manager (Terraform IaC)

**Objective:** Manage infrastructure as code with Resource Manager.

```hcl
# OCI Terraform (Resource Manager stack runs this)
resource "oci_core_vcn" "app" {
  compartment_id = var.compartment_ocid
  cidr_blocks    = ["10.0.0.0/16"]
  display_name   = "app-vcn"
}
```

**Expected result:** an OCI Terraform resource managed by **Resource Manager** —
the IaC area of the DevOps credential (pairs with Volume XLII HashiCorp).

**Negative test:** click-create production infrastructure; use **Resource Manager
(Terraform)** for repeatable, reviewable IaC.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.7 — DevOps: build and deploy pipelines

**Objective:** Outline an OCI DevOps CI/CD pipeline.

```bash
python3 - <<'PY'
print("DevOps service: Build pipeline (source -> build -> artifact to OCIR/Artifacts) ->")
print("Deploy pipeline (to OKE / Instance Groups / Functions) with approvals + rollback.")
PY
```

**Expected result:** a build→deploy pipeline with approvals/rollback — the DevOps
automation area.

**Negative test:** deploy manually to production; automate with a **deploy
pipeline** (approvals + rollback) for safety and repeatability.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The OCI Developer, Operations, and DevOps credentials cover building cloud-native
apps (Functions, API Gateway, OKE, events), observing them (Monitoring, Logging,
Alarms), and automating delivery and infrastructure (Resource Manager/Terraform,
DevOps pipelines). Together they cover the build–run–automate lifecycle on OCI.

- [ ] I can describe Functions, API Gateway, OKE, and eventing.
- [ ] I can authenticate code with resource principals.
- [ ] I can define a Monitoring/Logging/Alarm baseline.
- [ ] I can manage IaC with Resource Manager and build DevOps pipelines.
- [ ] I completed Labs 4.1–4.7 including each negative test.
