# Chapter 09: Platform Engineering (CNPA, CNPE) and Keeping Current

## Learning Objectives

- Explain the platform-engineering track: the CNPA associate and the performance-based CNPE.
- List the CNPA and CNPE domains and their exam weights.
- Relate platform engineering to internal developer platforms (IDPs) and golden paths.
- Track program change: new credentials, version pinning, and renewal.
- Complete a per-domain walkthrough for every CNPA and CNPE domain, plus a currency check.

## Theory and Architecture

**Platform engineering** — building an **internal developer platform (IDP)** that
gives developers self-service, paved "golden paths" on top of Kubernetes — is the
CNCF's newest certification track:

- **Cloud Native Platform Engineering Associate (CNPA)** — multiple-choice,
  knowledge-level. Six weighted domains:

  | # | Domain | Weight |
  |---|--------|--------|
  | 1 | Platform Engineering Core Fundamentals | 36% |
  | 2 | Platform Observability, Security, and Conformance | 20% |
  | 3 | Continuous Delivery & Platform Engineering | 16% |
  | 4 | Platform APIs and Provisioning Infrastructure | 12% |
  | 5 | IDPs and Developer Experience | 8% |
  | 6 | Measuring your Platform | 8% |

- **Certified Cloud Native Platform Engineer (CNPE)** — the **performance-based**
  expert credential (launched November 2025), two hours in a live terminal. Five
  weighted domains:

  | # | Domain | Weight |
  |---|--------|--------|
  | 1 | Platform Architecture and Infrastructure | 15% |
  | 2 | GitOps and Continuous Delivery | 25% |
  | 3 | Platform APIs and Self-Service Capabilities | 25% |
  | 4 | Observability and Operations | 20% |
  | 5 | Security and Policy Enforcement | 15% |

CNPA teaches the concepts; **CNPE proves you can build the platform** — CRDs and
operators for self-service, GitOps delivery, observability, and policy
enforcement, drawing on nearly every project in this volume.

## Design Considerations

Platform engineering **composes** the rest of the volume: GitOps (Argo/Flux) for
delivery, Backstage for the developer portal, Kyverno for policy guardrails,
Prometheus/OpenTelemetry for observability, and Kubernetes CRDs/operators for
self-service APIs. Take **CNPA** to frame the discipline (IDPs, golden paths,
platform-as-product, DORA/platform metrics), then **CNPE** to demonstrate it
hands-on. Because CNPE is performance-based, practice **building** self-service
abstractions, not just describing them.

## Implementation and Automation

The labs below model one representative concept or task per domain — golden
paths and platform-as-product (CNPA), and CRD-based self-service, GitOps
delivery, and policy enforcement (CNPE) — using `kubectl` and portable manifests.

## Validation and Troubleshooting

Confirm both blueprints and the program's currency:

```text
training.linuxfoundation.org > CNPA and CNPE > curricula:
  - CNPA (36/20/16/12/8/8), multiple-choice
  - CNPE (15/25/25/20/15), performance-based, 2 hours
Watch cncf.io for new project associates and version bumps.
```

Common pitfalls: treating a platform as a **project** rather than a **product**
(no lifecycle, no user feedback); building self-service that **bypasses**
guardrails; and studying **CNPE** as theory — it is hands-on.

## Security and Best Practices

Design the platform as a **product** with golden paths that are **secure by
default** (policy-enforced, observable, GitOps-delivered). Measure it with
**platform and DORA metrics** (lead time, deployment frequency, MTTR, adoption).
Keep every underlying project current — the curricula are version-pinned and the
program adds credentials regularly (KCA, CNPA, and CNPE are all recent).

## References and Knowledge Checks

- training.linuxfoundation.org: *CNPA* and *CNPE* curricula; the CNCF Platforms working group; platformengineering.org.

**Knowledge checks**

1. What is an internal developer platform, and what is a "golden path"?
2. How does CNPE differ from CNPA in format and intent?
3. Which projects from earlier chapters does a platform compose?

## Hands-On Lab

Per-topic walkthroughs — **one lab for every weighted CNPA and CNPE domain**,
plus a currency check.

**Shared prerequisites** — the `kind`/`minikube` cluster from Chapter 01,
`kubectl`, `curl`, and a Linux shell with `python3`. **Cost:** none.

### CNPA — Cloud Native Platform Engineering Associate

### Lab 9.1 — CNPA: Platform Engineering Core Fundamentals (36%)

**Objective:** Define platform-as-product and the golden path.

```bash
python3 - <<'PY'
print("Platform as product: internal users are customers; the platform has a roadmap + support.")
print("Golden path: a paved, opinionated, secure-by-default way to build/ship a service.")
print("Goal: reduce cognitive load and let developers self-serve within guardrails.")
PY
```

**Expected result:** the platform-as-product and golden-path concepts — the
foundations that lead CNPA (Domain 1, 36%).

**Negative test:** mandate one rigid pipeline with no opt-out; a golden path is
**paved, not walled** — make the easy path the good one, not the only one.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 9.2 — CNPA: Platform Observability, Security, and Conformance (20%)

**Objective:** List the platform's cross-cutting guarantees.

```bash
python3 - <<'PY'
guarantees = {"Observability":"metrics/logs/traces built into golden paths",
              "Security":"policy-enforced defaults (Kyverno/OPA), signed images",
              "Conformance":"CIS/upstream conformance + drift detection"}
for k,v in guarantees.items(): print(f"{k:13}: {v}")
PY
```

**Expected result:** the observability/security/conformance guarantees a platform
provides for every workload — CNPA Domain 2.

**Negative test:** bolt observability on per team; the platform should provide it
**by default** so every service is observable.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 9.3 — CNPA: Continuous Delivery & Platform Engineering (16%)

**Objective:** Relate GitOps delivery to the platform.

```bash
python3 - <<'PY'
print("Platform provides CD as a capability: GitOps (Argo/Flux) reconciles app + infra from Git.")
print("Developers push to Git; the platform delivers — no bespoke per-team pipelines.")
PY
```

**Expected result:** CD delivered as a platform capability via GitOps — CNPA
Domain 3.

**Negative test:** have every team build its own delivery pipeline; the platform
should offer **CD as a shared, paved capability**.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 9.4 — CNPA: Platform APIs and Provisioning Infrastructure (12%)

**Objective:** Describe self-service via platform APIs (CRDs).

```bash
python3 - <<'PY'
print("Platform API: a CRD (e.g., kind: Database) developers create; an operator provisions it.")
print("Tools: Kubernetes CRDs/operators, Crossplane (compose cloud infra as Kubernetes APIs).")
PY
```

**Expected result:** self-service provisioning through CRDs/operators (and
Crossplane) — CNPA Domain 4.

**Negative test:** file a ticket for every database; a **platform API** lets
developers self-serve within guardrails — automate provisioning.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 9.5 — CNPA: IDPs and Developer Experience (8%)

**Objective:** Describe the developer portal's role.

```bash
python3 - <<'PY'
print("IDP portal (e.g., Backstage): catalog, scaffolder (templates), docs, and self-service actions.")
print("DevEx metric: time-to-first-deploy for a new service should be minutes, not weeks.")
PY
```

**Expected result:** the IDP portal (Backstage) and a developer-experience metric
— CNPA Domain 5.

**Negative test:** measure platform success by feature count; measure **developer
experience** (time-to-first-deploy, adoption) instead.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 9.6 — CNPA: Measuring your Platform (8%)

**Objective:** Choose platform and DORA metrics.

```bash
python3 - <<'PY'
metrics = {"DORA":"lead time, deploy frequency, change fail rate, MTTR",
           "Adoption":"% services on golden paths",
           "Reliability":"platform SLOs (control-plane availability)"}
for k,v in metrics.items(): print(f"{k:11}: {v}")
PY
```

**Expected result:** DORA plus adoption and reliability metrics — measuring the
platform, CNPA Domain 6.

**Negative test:** track only uptime; **DORA + adoption** show whether the
platform actually improves delivery.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### CNPE — Certified Cloud Native Platform Engineer

### Lab 9.7 — CNPE: Platform Architecture and Infrastructure (15%)

**Objective:** Apply multi-tenancy isolation with namespaces and quotas.

```bash
kubectl create namespace team-a
kubectl create quota ta --hard=pods=10,requests.cpu=2 -n team-a
kubectl get resourcequota -n team-a
```

**Expected result:** a namespace with a ResourceQuota capping pods/CPU — tenant
isolation, the architecture foundation of CNPE Domain 1.

**Negative test:** run all tenants in one unbounded namespace; a noisy tenant
starves others — isolate with namespaces and quotas.

**Rollback:** `kubectl delete namespace team-a`

### Lab 9.8 — CNPE: GitOps and Continuous Delivery (25%)

**Objective:** Describe the platform's GitOps delivery topology.

```bash
python3 - <<'PY'
print("App-of-apps: a root Argo CD Application manages per-team/child Applications.")
print("Progressive delivery: Argo Rollouts canary + analysis gates before full promotion.")
print("Everything (apps + platform components) reconciled from Git.")
PY
```

**Expected result:** the GitOps delivery topology (app-of-apps, progressive
delivery) a platform engineer builds — CNPE Domain 2 (tied heaviest).

**Negative test:** apply platform components manually; reconcile **them** from
Git too so the platform itself is GitOps-managed.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 9.9 — CNPE: Platform APIs and Self-Service Capabilities (25%)

**Objective:** Define a self-service API with a CRD.

```bash
kubectl apply -f - <<'YAML'
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata: {name: databases.platform.example.com}
spec:
  group: platform.example.com
  scope: Namespaced
  names: {plural: databases, singular: database, kind: Database}
  versions:
  - name: v1
    served: true
    storage: true
    schema: {openAPIV3Schema: {type: object, properties: {spec: {type: object, properties: {engine: {type: string}}}}}}
YAML
kubectl get crd databases.platform.example.com
```

**Expected result:** a `Database` CRD registered — the self-service platform API
(an operator would reconcile it) at the heart of CNPE Domain 3.

**Negative test:** expose raw cloud APIs to developers; a **platform CRD** gives
a guardrailed, self-service abstraction instead.

**Rollback:** `kubectl delete crd databases.platform.example.com`

### Lab 9.10 — CNPE: Observability and Operations (20%)

**Objective:** Wire a platform SLO/alert concept.

```bash
cat <<'EOF'
# Platform control-plane SLO alert (PromQL):
1 - (sum(rate(apiserver_request_total{code=~"5.."}[5m])) / sum(rate(apiserver_request_total[5m]))) < 0.999
EOF
echo "Operate the platform on SLOs; alert on burn, not on every blip."
```

**Expected result:** a platform SLO expression (API-server success ratio) and the
operate-on-SLOs principle — CNPE Domain 4.

**Negative test:** alert on raw error counts; use an **SLO burn** so alerts
reflect user-visible impact.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 9.11 — CNPE: Security and Policy Enforcement (15%)

**Objective:** Enforce a platform guardrail with admission policy.

```bash
kubectl label namespace default \
  pod-security.kubernetes.io/warn=restricted --overwrite
kubectl get namespace default -o jsonpath='{.metadata.labels}' | tr ',' '\n' | grep pod-security
echo "Platform default: Pod Security + Kyverno policies enforced on every tenant namespace."
```

**Expected result:** a Pod Security label applied as a platform guardrail (and the
Kyverno note) — enforcing security/policy across tenants, CNPE Domain 5.

**Negative test:** trust each tenant to secure itself; the platform enforces
**baseline guardrails** for everyone via admission policy.

**Rollback:** `kubectl label namespace default pod-security.kubernetes.io/warn- --overwrite`

### Lab 9.12 — Keeping the program current (Topic: Verify currency)

**Objective:** Detect new credentials and version bumps from the source.

```bash
curl -sSL "https://raw.githubusercontent.com/cncf/curriculum/master/README.md" \
  | grep -oiE 'v1\.[0-9]+|CK[AS]D?|KCNA|KCSA' | sort -u | head
```

**Expected result:** the current Kubernetes version and core exam list — proof of
the pinned version so you never study a stale curriculum. Check cncf.io for new
associates (KCA, CNPA, CNPE were all recent additions).

**Negative test:** trust a two-year-old course; the curriculum and Kubernetes
version have moved — confirm against the source.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Platform engineering is the CNCF's newest track: **CNPA** (six domains
36/20/16/12/8/8) teaches internal developer platforms, golden paths, and
platform-as-product, and the performance-based **CNPE** (five domains
15/25/25/20/15, launched November 2025) proves you can build one — composing
GitOps, self-service CRDs, observability, and policy from across this volume. The
program is version-pinned and grows regularly, so verify currency from the
source.

- [ ] I can list the CNPA and CNPE domains and their weights.
- [ ] I can explain golden paths, platform-as-product, and IDPs.
- [ ] I can define a self-service CRD and enforce a platform guardrail.
- [ ] I can measure a platform with DORA and adoption metrics.
- [ ] I completed Labs 9.1–9.12 including each negative test.
