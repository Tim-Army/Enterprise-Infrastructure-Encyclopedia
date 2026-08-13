# Chapter 08: Internal Developer Platforms and Platform Products

![Lab flow for this chapter: a WebService CustomResourceDefinition and a bash reconciliation loop stand in for a compiled operator, watching WebService objects and creating matching Deployments; a hello-service claim reconciles to status ready:true and a running 2-replica Deployment. A tenant ResourceQuota (pods: 3) is then applied. As a negative test, a second, oversized claim (replicas: 5) is accepted by the CRD but its ReplicaSet cannot bring all pods up — events show 'exceeded quota: tenant-quota' once existing plus new pods would cross the ceiling, demonstrating that tenant isolation is enforced by the shared quota regardless of what the self-service claim requested.](../../../diagrams/volume-008-containers-platform-engineering/chapter-08-platform-crd-tenant-quota-flow.svg)

*Figure 8-1. Flow used throughout this chapter's Hands-On Lab: a self-service platform claim reconciled by a minimal operator, with a tenant ResourceQuota blocking an over-limit claim.*

## Learning Objectives

- Explain platform engineering as a discipline distinct from traditional
  operations, and define an Internal Developer Platform (IDP) in terms of
  the golden paths it exposes.
- Extend the Kubernetes API with Custom Resource Definitions and the
  operator pattern to expose infrastructure as a self-service, versioned
  API rather than a ticket queue.
- Compose infrastructure resources declaratively with Crossplane and
  evaluate it against direct Terraform usage for platform teams.
- Stand up a software catalog and self-service scaffolding with Backstage,
  and connect it to the golden paths it should expose.
- Choose a multi-tenancy model — namespace-based soft tenancy, virtual
  clusters, or hard-isolated clusters — appropriate to a given isolation
  requirement.

## Theory and Architecture

Every chapter so far in this volume gave a platform team the building
blocks — workloads, networking, storage, identity, delivery. This chapter
is about the product built from those blocks: a platform that application
teams *consume* rather than assemble themselves, chapter by chapter, on
every project.

### Platform engineering as a discipline

**Platform engineering** treats internal infrastructure capability as a
product, with application developers as its customers. The deliverable is
not a runbook or a set of Terraform modules a team must know exist and
correctly invoke — it is a curated set of **golden paths**: an opinionated,
supported, self-service way to get a working, production-ready workload
from zero to running, with the platform team's operational expertise
(security defaults from [Chapter 06](06-kubernetes-identity-configuration-policy-and-security.md), delivery mechanics from [Chapter 07](07-cloud-native-delivery-gitops-and-software-supply-chains.md),
observability wiring from [Chapter 09](09-platform-observability-reliability-and-lifecycle-operations.md)) built into the path rather than
left as homework for each application team to rediscover. An **Internal
Developer Platform (IDP)** is the concrete system — often a portal, a set
of CRDs and operators, a templating and scaffolding layer, and the
underlying Kubernetes/cloud infrastructure — that implements those golden
paths.

The discipline sits deliberately between fully centralized operations
(every change goes through a platform team ticket queue, slow and
consistent) and fully decentralized "you build it, you run it" (fast, but
every team reinvents security, networking, and observability decisions
independently, with widely varying quality). A well-built IDP recovers
most of the centralized model's consistency and most of the decentralized
model's speed by making the *good* path also the *easy* path — self-service,
but self-service to a paved road, not to unrestricted raw Kubernetes API
access.

### Extending the API: CRDs and the operator pattern in depth

[Chapter 02](02-kubernetes-architecture-and-cluster-lifecycle.md) introduced Custom Resource Definitions as the mechanism that
lets a CRD-backed object receive full CRUD, watch, validation, and
(paired with a controller) reconciliation identical to a built-in object.
Platform engineering is where this mechanism becomes the product itself,
not just an implementation detail: instead of a developer filing a ticket
for "a Postgres database" or "a Kafka topic," they submit a small,
validated custom resource — `PostgresInstance`, `KafkaTopic`,
`WebService` — and an **operator** (a controller purpose-built for that
resource, commonly scaffolded with **Kubebuilder** or the **Operator
SDK**, both built on `controller-runtime`) reconciles it into the actual
underlying infrastructure, whether that infrastructure lives inside the
cluster (a StatefulSet-backed database from [Chapter 05](05-kubernetes-storage-and-stateful-platforms.md)) or outside it
entirely (a cloud-managed database instance).

```text
Developer                        Platform API (CRD)          Operator            Actual infrastructure
   │  kubectl apply -f postgres.yaml                             │                        │
   ├──────────────────────────────►                               │                        │
   │           validated by the CRD's OpenAPI schema              │                        │
   │           (and any admission policy from Chapter 06)         │                        │
   │                              │  watch/reconcile               │                        │
   │                              ├────────────────────────────────►                        │
   │                              │                                │  create/configure       │
   │                              │                                ├────────────────────────►│
   │                              │                                │◄────────────────────────┤
   │                              │◄────status written back────────┤   status report          │
   │◄──kubectl get postgresinstance shows Ready──────────────────┤                            │
```

This pattern is what makes the platform's API surface genuinely
Kubernetes-native rather than a bolt-on web form: the same `kubectl`,
RBAC, GitOps ([Chapter 07](07-cloud-native-delivery-gitops-and-software-supply-chains.md)), and policy enforcement ([Chapter 06](06-kubernetes-identity-configuration-policy-and-security.md)) tooling a
team already uses for a Deployment applies identically to a
`PostgresInstance`.

### Crossplane: infrastructure as a Kubernetes API

**Crossplane** generalizes the CRD-plus-operator pattern specifically for
external cloud infrastructure. A **provider** (AWS, Azure, GCP, and many
others) installs CRDs representing individual cloud resources
(`RDSInstance`, `Bucket`, `VPC`). A platform team composes those
primitives into a higher-level, developer-facing abstraction using a
**Composite Resource Definition (XRD)** — which defines the schema of a
new custom API, such as `DatabaseClaim` — and one or more
**Compositions**, which map that claim onto a concrete set of
provider-level resources (an `RDSInstance` plus its security group,
subnet group, and parameter group, for example), entirely as Kubernetes
objects reconciled the same way any other controller reconciles. The
platform team designs and owns the Composition (and its guardrails —
instance sizes, encryption defaults, allowed regions); the application
team only ever sees and submits the narrow, validated `DatabaseClaim`.

This is a genuinely different architecture from a Terraform module
library invoked by CI: Terraform state lives outside Kubernetes, applied
by a pipeline run; a Crossplane claim is a live, continuously reconciled
Kubernetes object, drift-corrected the same way any controller
drift-corrects, and inspectable with the same `kubectl get`/`describe`
muscle memory as everything else in the cluster. It is not a universal
replacement for Terraform — Terraform's ecosystem breadth and maturity
for less-Kubernetes-centric infrastructure (networking backbones, IAM at
the organization level) remains a legitimate reason to keep it for
infrastructure outside the platform's Kubernetes-native surface — but for
infrastructure a platform wants to expose as a first-class, self-service,
continuously reconciled API to application teams, Crossplane closes a gap
Terraform's plan/apply, run-triggered model does not.

### The developer portal: Backstage

**Backstage** (a CNCF graduated project, originated at Spotify) provides
the human-facing layer over everything above: a **software catalog**
cataloging every service, its owner, its dependencies, and its links to
runtime dashboards; **TechDocs** for documentation that lives beside the
code it describes and renders into the same portal; and a **scaffolder**
that turns a golden path into a self-service form — "create a new Go
microservice" — that generates a populated repository, a CI pipeline, and
the platform CRDs (a `WebService`, a `DatabaseClaim`) needed to run it,
all wired together and already compliant with platform defaults on day
one. Backstage's catalog and scaffolder are extensible via plugins,
which is how it integrates with whatever CI/CD, GitOps ([Chapter 07](07-cloud-native-delivery-gitops-and-software-supply-chains.md)), and
observability ([Chapter 09](09-platform-observability-reliability-and-lifecycle-operations.md)) tooling a given organization already runs
rather than replacing any of it.

### Multi-tenancy models

A platform serving many application teams on shared infrastructure has to
choose an isolation model, and different teams or workloads can
legitimately warrant different points on this spectrum:

| Model | Isolation boundary | Trade-off |
| --- | --- | --- |
| **Namespace-based soft multi-tenancy** | Kubernetes namespace, enforced by RBAC + NetworkPolicy + resource quotas | Cheapest, highest density; a control-plane or kernel-level vulnerability can still cross tenants |
| **Virtual clusters (vcluster)** | A control-plane-per-tenant running inside a namespace of a shared host cluster | Each tenant gets its own API server and object namespace (even cluster-scoped resources feel dedicated) without a dedicated set of nodes |
| **Hierarchical namespaces / Capsule-style tenancy** | Namespace, with policy inherited down a namespace hierarchy and self-service sub-namespace creation | Improves on flat soft multi-tenancy's admin burden without the overhead of a virtual or dedicated cluster |
| **Dedicated (hard) cluster per tenant** | Full cluster — separate control plane, separate nodes | Strongest isolation, including kernel-level; highest cost and operational overhead, multiplied by tenant count |

## Design Considerations

**A platform is only as good as its opinionation, and over-flexibility is
a design failure, not a feature.** A golden path that exposes every
possible Kubernetes knob "for flexibility" reproduces the cognitive load
the platform was built to remove — an application team back to making
security and reliability decisions it has neither the context nor the
mandate to make well. The discipline is choosing *which* decisions the
platform makes unilaterally (base image hardening, default resource
requests, mandatory PodDisruptionBudgets, signature enforcement) versus
which remain genuinely a per-application choice (replica count within a
bounded range, environment variables, feature flags) — and resisting
pressure to expand the second category just because one team requests an
exception.

**CRDs-as-a-product require the same versioning discipline as a public
API.** A platform CRD consumed by dozens of application teams cannot make
a breaking schema change the way an internal implementation detail could;
Kubernetes' built-in CRD versioning (multiple served versions with a
conversion webhook, or a coordinated deprecation window) is not optional
tooling here — it is the mechanism that keeps a platform's evolution from
becoming a synchronized, all-teams-at-once migration event every time the
platform improves.

**Crossplane concentrates cloud provisioning power in the platform
team's Compositions, which is the point, but demands the same admission
and RBAC rigor as anything else with that reach.** A Composition that
lets an application team's `DatabaseClaim` implicitly provision an
unencrypted, publicly-reachable database because a guardrail was left out
of the Composition is a platform-caused incident, not an application-team
mistake — the entire value proposition is that the guardrail is enforced
centrally and correctly once, rather than left to be reproduced correctly
by every consuming team.

**Choose multi-tenancy isolation strength per actual risk, not
uniformly.** Namespace-based soft multi-tenancy, correctly combined with
the RBAC ([Chapter 06](06-kubernetes-identity-configuration-policy-and-security.md)), NetworkPolicy ([Chapter 04](04-kubernetes-networking-service-delivery-and-traffic-policy.md)), and resource-quota
controls already covered in this volume, is entirely adequate for
internal teams operating under a shared trust boundary and shared
compliance posture. A tenant with a materially different compliance
requirement (regulatory data residency, a customer-facing multi-tenant
SaaS boundary where one tenant is literally an external, mutually
distrusting customer) justifies the added cost of virtual or dedicated
clusters. Applying dedicated-cluster isolation everywhere "to be safe"
mostly just multiplies the platform team's operational surface — patching,
upgrades ([Chapter 02](02-kubernetes-architecture-and-cluster-lifecycle.md)), and observability ([Chapter 09](09-platform-observability-reliability-and-lifecycle-operations.md)) — by the tenant
count without a corresponding security benefit for tenants that did not
need that boundary.

**A developer portal is a symptom of platform maturity, not a
starting point.** Standing up Backstage before the underlying golden
paths, CRDs, and operators it is meant to surface actually exist produces
an empty catalog and an impressive-looking scaffolder that generates
services with nowhere well-defined to land. Build the golden path first
— even manually documented — validate it with a handful of real teams,
then invest in the self-service portal layer once there is a genuine
paved road worth automating access to.

## Implementation and Automation

### A minimal platform CRD and its operator's reconciliation contract

```yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: webservices.platform.example.internal
spec:
  group: platform.example.internal
  names: { kind: WebService, plural: webservices, singular: webservice }
  scope: Namespaced
  versions:
    - name: v1alpha1
      served: true
      storage: true
      schema:
        openAPIV3Schema:
          type: object
          properties:
            spec:
              type: object
              required: ["image", "port"]
              properties:
                image: { type: string }
                port: { type: integer, minimum: 1, maximum: 65535 }
                replicas: { type: integer, default: 2, minimum: 1 }
                exposeExternally: { type: boolean, default: false }
            status:
              type: object
              properties:
                ready: { type: boolean }
                url: { type: string }
      subresources:
        status: {}
```

```yaml
apiVersion: platform.example.internal/v1alpha1
kind: WebService
metadata:
  name: checkout-api
  namespace: payments
spec:
  image: registry.example.internal/payments/checkout-api:2.3.1
  port: 8080
  replicas: 3
  exposeExternally: true
```

A `WebService` operator watches this resource and reconciles a
Deployment, Service, and (when `exposeExternally: true`) an `HTTPRoute`
against the platform's shared `Gateway` from [Chapter 04](04-kubernetes-networking-service-delivery-and-traffic-policy.md) — with the
platform's default `PodDisruptionBudget`, resource requests, and
`restricted` Pod Security context ([Chapter 06](06-kubernetes-identity-configuration-policy-and-security.md)) applied automatically,
never left to the application team to configure or forget.

### Crossplane: an XRD and Composition exposing a self-service database claim

```yaml
apiVersion: apiextensions.crossplane.io/v1
kind: CompositeResourceDefinition
metadata:
  name: xdatabaseclaims.platform.example.internal
spec:
  group: platform.example.internal
  names: { kind: XDatabaseClaim, plural: xdatabaseclaims }
  claimNames: { kind: DatabaseClaim, plural: databaseclaims }
  versions:
    - name: v1alpha1
      served: true
      referenceable: true
      schema:
        openAPIV3Schema:
          type: object
          properties:
            spec:
              type: object
              properties:
                storageGB: { type: integer, default: 20 }
                engineVersion: { type: string, default: "16" }
---
apiVersion: apiextensions.crossplane.io/v1
kind: Composition
metadata:
  name: database-claim-aws-rds
spec:
  compositeTypeRef:
    apiVersion: platform.example.internal/v1alpha1
    kind: XDatabaseClaim
  resources:
    - name: rds-instance
      base:
        apiVersion: rds.aws.upbound.io/v1beta1
        kind: Instance
        spec:
          forProvider:
            engine: postgres
            storageEncrypted: true          # platform guardrail, not developer-configurable
            publiclyAccessible: false        # platform guardrail, not developer-configurable
            region: us-east-2
```

```yaml
apiVersion: platform.example.internal/v1alpha1
kind: DatabaseClaim
metadata:
  name: order-db
  namespace: payments
spec:
  storageGB: 100
  engineVersion: "16"
```

The application team's `DatabaseClaim` never exposes
`storageEncrypted` or `publiclyAccessible` — those guardrails live only in
the platform-owned Composition, structurally unreachable from the
consuming namespace.

```bash
kubectl get databaseclaim -n payments
kubectl describe databaseclaim order-db -n payments   # status shows readiness once RDS provisioning completes
```

### Backstage scaffolder template invoking a golden path

```yaml
apiVersion: scaffolder.backstage.io/v1beta3
kind: Template
metadata:
  name: golden-path-web-service
  title: "New Web Service (Go)"
spec:
  parameters:
    - properties:
        serviceName: { type: string }
        teamOwner: { type: string }
  steps:
    - id: fetch
      name: Fetch base template
      action: fetch:template
      input:
        url: ./skeletons/go-web-service
        values:
          serviceName: "${{ parameters.serviceName }}"
    - id: publish
      name: Publish repository
      action: publish:github
      input:
        repoUrl: "github.com?owner=example-org&repo=${{ parameters.serviceName }}"
    - id: register
      name: Register in catalog
      action: catalog:register
      input:
        repoContentsUrl: "${{ steps.publish.output.repoContentsUrl }}"
        catalogInfoPath: /catalog-info.yaml
```

The generated repository ships a `WebService` manifest and a GitOps
overlay ([Chapter 07](07-cloud-native-delivery-gitops-and-software-supply-chains.md)) already wired to the platform's golden path, so a
new service reaches a running, monitored, signed-and-verified deployment
without the owning team hand-assembling any of Chapters 01 through 07's
mechanics individually.

### Namespace-based soft multi-tenancy baseline

```bash
kubectl create namespace team-payments
kubectl label namespace team-payments platform.example.internal/tenant=payments

kubectl apply -n team-payments -f - <<'EOF'
apiVersion: v1
kind: ResourceQuota
metadata:
  name: tenant-quota
spec:
  hard:
    requests.cpu: "20"
    requests.memory: 40Gi
    persistentvolumeclaims: "10"
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: payments-team-admin
subjects:
  - kind: Group
    name: payments-team
    apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: admin
  apiGroup: rbac.authorization.k8s.io
EOF
```

## Validation and Troubleshooting

```bash
# Confirm a platform CRD is installed and its operator is reconciling.
kubectl get crd webservices.platform.example.internal
kubectl get pods -n platform-system -l app=webservice-operator

# Watch a custom resource's reconciliation status directly.
kubectl get webservice checkout-api -n payments -o jsonpath='{.status}'

# Crossplane-specific reconciliation and provider health.
kubectl get providers.pkg.crossplane.io
kubectl describe databaseclaim order-db -n payments
```

| Symptom | Likely cause | Diagnostic |
| --- | --- | --- |
| A platform custom resource never leaves an empty/pending status | Operator pod is down, or the operator lacks RBAC to reconcile the resource | `kubectl get pods -n platform-system`; `kubectl auth can-i --list --as=system:serviceaccount:platform-system:<operator-sa>` |
| Crossplane claim stuck, never provisions the underlying cloud resource | Provider credentials misconfigured, or the Composition references a provider CRD version mismatch | `kubectl describe databaseclaim`; `kubectl get providerconfig`; provider pod logs |
| Backstage scaffolder template fails during `publish:github` | CI/SCM integration token expired or lacks repository-creation scope | Backstage backend logs; confirm the integration's token scope |
| Two tenants' workloads interfere despite separate namespaces | Missing NetworkPolicy default-deny ([Chapter 04](04-kubernetes-networking-service-delivery-and-traffic-policy.md)) or an overly broad ClusterRoleBinding crossing tenant boundaries | `kubectl get networkpolicy -A`; `kubectl get clusterrolebindings -o wide` and audit subjects |
| Application team requests a platform CRD field the schema does not expose | Working as intended if the field is a deliberate guardrail; otherwise a genuine platform gap | Confirm against the platform's documented golden-path scope before adding the field |

## Security and Best Practices

- Bake security and reliability defaults (Pod Security admission,
  resource requests, PodDisruptionBudgets, signature verification) into
  the platform CRD/operator layer so they are structurally present, not
  dependent on every application team remembering to configure them.
- Version platform CRDs deliberately, using Kubernetes' native
  multi-version-with-conversion mechanism for breaking changes, and
  communicate deprecation windows the same way a public API provider
  would.
- Keep guardrail-bearing fields (encryption, public accessibility,
  region restrictions) inside platform-owned Compositions or operator
  logic, never inside the schema an application team's claim can set
  directly.
- Apply the same RBAC least-privilege discipline from [Chapter 06](06-kubernetes-identity-configuration-policy-and-security.md) to
  operator ServiceAccounts themselves; an operator with cluster-admin
  "because it's easier" is a single point of compromise for every
  resource it reconciles across every tenant.
- Choose multi-tenancy isolation strength based on actual compliance and
  trust-boundary requirements per tenant, not uniformly, and document the
  reasoning so the decision can be revisited as a tenant's requirements
  change.
- Treat a developer portal (Backstage) as a presentation layer over
  already-secure golden paths, not a source of authorization decisions
  itself — the underlying CRDs, RBAC, and admission policy remain the
  actual enforcement points regardless of what the portal's UI allows a
  user to click.
- Audit ResourceQuota and LimitRange coverage across every tenant
  namespace; a tenant with no quota can exhaust shared cluster capacity
  and degrade every other tenant on the same cluster.

## References and Knowledge Checks

**Authoritative references**

- CNCF, [Platform Engineering Maturity Model](https://tag-app-delivery.cncf.io/whitepapers/platform-eng-maturity-model/) and [Backstage documentation](https://backstage.io/docs/), version 1.31.x Kubernetes baseline per [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md).
- Kubernetes documentation, [Custom Resources](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/) and [Operator Pattern](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/).
- Kubebuilder documentation, [book.kubebuilder.io](https://book.kubebuilder.io/).
- Crossplane documentation, [docs.crossplane.io](https://docs.crossplane.io/).
- vcluster documentation, [www.vcluster.com/docs](https://www.vcluster.com/docs/).

**Knowledge check**

1. What distinguishes an Internal Developer Platform from a documented
   set of Terraform modules and runbooks a team could, in principle, also
   use self-service?
2. Why does exposing infrastructure through a CRD and operator give an
   application team a materially different experience than a
   ticket-based request process, beyond just being faster?
3. What is the key architectural difference between a Crossplane
   Composition and a Terraform module invoked from CI, and why does that
   difference matter for guardrail enforcement?
4. When is namespace-based soft multi-tenancy insufficient, and what does
   a virtual cluster add that RBAC and NetworkPolicy alone do not
   provide?
5. Why is standing up a Backstage developer portal before the underlying
   golden paths exist a common platform-adoption mistake?

## Hands-On Lab

This chapter carries a topic-level walkthrough lab for **each platform-engineering building
block** — CRDs and the operator pattern, Crossplane composites, golden paths, and
multi-tenancy — the discipline of building a platform *product*. Every step is a runnable
command. Each ends **`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 8.1–8.4** — a cluster with `kubectl`, and Crossplane installed
for Lab 8.2. **Cost:** none beyond cloud charges if Crossplane provisions real cloud
resources.

### Lab 8.1 — Custom Resource Definitions and the operator pattern (Topic: Extending the API)

**Objective:** Add a new resource kind to the Kubernetes API.

```bash
kubectl apply -f - <<'EOF'
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata: {name: widgets.platform.example.com}
spec:
  group: platform.example.com
  scope: Namespaced
  names: {plural: widgets, singular: widget, kind: Widget}
  versions:
  - name: v1
    served: true
    storage: true
    schema: {openAPIV3Schema: {type: object, properties: {spec: {type: object,
      properties: {size: {type: string}}}}}}
EOF
kubectl apply -f - <<'EOF'
apiVersion: platform.example.com/v1
kind: Widget
metadata: {name: w1, namespace: default}
spec: {size: large}
EOF
kubectl get widgets
```

**Expected result:** `Widget` becomes a first-class API resource and `w1` is created —
CRDs extend the Kubernetes API with your own kinds, and an **operator** (a controller watching
that CRD) then reconciles the desired state, the pattern behind databases-as-a-service,
cert-manager, and most platform abstractions.

**Negative test:** create a `Widget` before applying the CRD; the API rejects an unknown kind —
the CRD must register the type before any instance can exist.

**Rollback:** `kubectl delete widget w1; kubectl delete crd widgets.platform.example.com`.

### Lab 8.2 — Crossplane composite resources (Topic: Infrastructure composition)

**Objective:** Offer a self-service cloud resource as a Kubernetes API.

```bash
# With Crossplane + a provider (e.g. provider-aws) installed and configured:
kubectl get providers
kubectl explain compositeresourcedefinition | head
# Apply an XRD + Composition (platform-authored), then a developer claims it:
kubectl apply -f claim-bucket.yaml       # kind: Bucket (your XRD), spec: {region: us-east-1}
kubectl get bucket && kubectl get managed
```

**Expected result:** a developer's simple `Bucket` claim triggers Crossplane to provision the
real cloud resource via the provider — Crossplane turns cloud infrastructure into Kubernetes
APIs, so the platform team publishes an opinionated abstraction (the Composition) and
developers self-serve without touching cloud consoles.

**Negative test:** hand developers raw cloud IAM/console access instead of a composed claim;
they provision inconsistently and off-policy — the composition is what encodes the platform's
guardrails into a self-service API.

**Rollback:** delete the claim (`kubectl delete bucket <name>`) so Crossplane deprovisions the
cloud resource.

### Lab 8.3 — Golden paths and self-service (Topic: Platform products)

**Objective:** Provide a paved-road template a developer can consume.

```text
# In a developer portal (e.g. Backstage) or a templating tool, publish a "New Service"
#   golden path that scaffolds: repo + CI pipeline + Helm chart + Argo CD Application +
#   namespace with quotas/RBAC. A developer runs the template and gets a deployable service.
# Verify the generated Argo CD Application syncs and the service comes up.
```

**Expected result:** one self-service action scaffolds a production-ready service wired to the
platform's CI/CD, security, and observability defaults — a golden path is the platform's
*product*: the fastest route to production is also the compliant, well-instrumented one.

**Negative test:** publish documentation instead of an executable template; each team
reinvents CI/security/observability differently and inconsistently — a golden path encodes the
right way as the easy way, which docs alone cannot.

**Rollback:** remove any scaffolded lab repo/resources.

### Lab 8.4 — Multi-tenancy: namespaces, quotas, and isolation (Topic: Multi-tenancy)

**Objective:** Give a tenant a bounded, isolated slice of the cluster.

```bash
kubectl create namespace tenant-a
kubectl apply -f - <<'EOF'
apiVersion: v1
kind: ResourceQuota
metadata: {name: quota, namespace: tenant-a}
spec: {hard: {requests.cpu: "4", requests.memory: 8Gi, pods: "20"}}
EOF
kubectl apply -f - <<'EOF'
apiVersion: v1
kind: LimitRange
metadata: {name: defaults, namespace: tenant-a}
spec: {limits: [{type: Container, default: {cpu: 500m, memory: 256Mi}, defaultRequest: {cpu: 100m, memory: 128Mi}}]}
EOF
kubectl describe resourcequota quota -n tenant-a
```

**Expected result:** `tenant-a` is capped at its quota and containers get default requests/
limits from the LimitRange — namespaces plus ResourceQuota, LimitRange, RBAC, and NetworkPolicy
give a tenant a bounded, isolated slice so one team cannot starve or reach into another.

**Negative test:** run tenants in a shared namespace with no quotas; one team's runaway
workload starves the others and RBAC cannot separate them — the namespace boundary plus quotas
is the unit of multi-tenant isolation.

**Rollback:** `kubectl delete namespace tenant-a`.

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Platform engineering treats infrastructure as a product with golden
paths, not a ticket queue or a library of optional modules. CRDs and the
operator pattern turn that product into a genuinely Kubernetes-native,
self-service API; Crossplane extends the same pattern to external cloud
infrastructure with platform-owned guardrails structurally separated from
what an application team's claim can configure. Backstage gives that
platform a human-facing catalog and scaffolder, but only pays off once
real golden paths exist underneath it. Multi-tenancy isolation — soft
namespace-based, virtual-cluster, or hard-dedicated — should be chosen
per tenant's actual trust and compliance boundary, not applied uniformly.

- [ ] Can define platform engineering and an IDP in terms of golden paths
      rather than available tooling.
- [ ] Can explain how a CRD and operator turn infrastructure into a
      self-service API with enforced guardrails.
- [ ] Can describe how a Crossplane XRD and Composition separate a
      developer-facing claim from platform-owned guardrails.
- [ ] Can explain what a developer portal like Backstage adds on top of
      already-existing golden paths.
- [ ] Can select an appropriate multi-tenancy isolation model for a given
      trust boundary.
- [ ] Completed the hands-on lab, including the tenant-quota negative
      test, and performed cleanup.
