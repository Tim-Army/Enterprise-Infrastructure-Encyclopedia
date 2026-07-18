# Chapter 07: Cloud-Native Delivery, GitOps, and Software Supply Chains

## Learning Objectives

- Package and template application manifests with Helm and Kustomize, and
  explain when to combine rather than choose between them.
- Explain the GitOps pull-based reconciliation model and configure Argo CD
  or Flux to deploy from a Git repository as the source of truth.
- Implement progressive delivery — canary and blue-green rollouts — with
  Argo Rollouts or Flagger, including automated rollback on failed
  metrics.
- Map a build pipeline to the SLSA provenance framework and enforce
  signature and attestation verification at deployment time.
- Diagnose GitOps drift, sync failures, and progressive-delivery rollback
  behavior.

## Theory and Architecture

Chapter 01 covered building, scanning, and signing an image. This chapter
picks up immediately after the registry push: how that signed artifact
becomes a running, continuously reconciled workload, and how the delivery
pipeline itself becomes a verifiable part of the supply chain rather than
a trusted black box.

### Templating and packaging: Helm and Kustomize

**Helm** packages a set of Kubernetes manifests into a versioned,
distributable **chart**: `templates/` holds Go-template YAML,
`values.yaml` holds default configuration, and a `Chart.yaml` declares
name, version, and dependencies. Helm 3 removed the server-side Tiller
component present in Helm 2, so a Helm release is tracked entirely
client-side (or by whatever CI/CD identity runs `helm upgrade`) with
release state stored as a Secret in the target namespace — there is no
separate Helm-specific privileged component running in the cluster.
Charts are the dominant distribution format for third-party software
(most vendor and open-source Kubernetes applications ship a Helm chart as
their primary install path) and are well suited to parameterizing a
single logical application across environments via different
`values-<env>.yaml` overlays.

**Kustomize** takes the opposite approach: no templating language at all.
A `base/` directory holds plain, valid Kubernetes YAML; environment-
specific `overlays/` apply structured **patches** (strategic merge patches
or JSON 6902 patches) on top of the base without ever templating a string.
Because Kustomize output is always valid, directly-`kubectl apply`-able
YAML with no template syntax to render first, it composes cleanly with
GitOps tools that want to diff the exact manifest against live cluster
state. `kubectl apply -k` and Kustomize's built-in status as a
`kubectl` subcommand also means it needs no additional binary in the
simplest cases.

In practice, the two are frequently combined rather than chosen
exclusively: consume a third-party Helm chart as-is (or with `helm
template` to render it once into plain YAML), then layer Kustomize
patches on the rendered output for environment-specific tweaks a chart's
`values.yaml` does not expose — both Argo CD and Flux support this
Helm-then-Kustomize pattern natively.

### GitOps: Git as the source of truth, reconciled by a pull-based agent

**GitOps** inverts the traditional CI/CD push model. Instead of a CI
pipeline holding cluster credentials and pushing changes with `kubectl
apply` or `helm upgrade` at the end of a build, an **in-cluster
controller** continuously pulls the desired state from a Git repository
and reconciles the live cluster toward it — the same
watch-and-reconcile pattern that underlies every Kubernetes controller
described in Chapter 02, applied to the cluster's own application
manifests.

```text
Developer            CI pipeline              Git repository         GitOps controller        Cluster
   │  commit source       │                         │                      │                     │
   ├──────────────────────►                         │                      │                     │
   │                  build, test,                  │                      │                     │
   │                  scan, sign (Ch.01)             │                      │                     │
   │                       │  update image tag/digest│                      │                     │
   │                       ├─────────────────────────►                      │                     │
   │                       │                         │  continuous pull &   │                     │
   │                       │                         │◄─────────────────────┤   diff observed     │
   │                       │                         │                      │───────────────────► │
   │                       │                         │                      │   apply to converge │
```

The CI pipeline's write access is scoped to a Git repository, never to
the cluster's API server directly — a materially smaller blast radius
than a pipeline holding a kubeconfig with cluster-admin-equivalent
access. The in-cluster controller's pull-based reconciliation also means
Git is always an accurate record of intended state, and any manual
`kubectl edit` drift against that state is detected (and, depending on
configuration, automatically reverted) on the next reconciliation pass —
this **self-healing** behavior is one of GitOps's most cited operational
benefits and one of its most surprising behaviors to an operator making
an undocumented emergency change.

- **Argo CD** models each deployed unit as an `Application` custom
  resource, provides a web UI and CLI for visualizing sync status and
  diffs, and supports **App of Apps** and **ApplicationSet** patterns for
  managing many applications or many clusters from a single Git
  structure.
- **Flux** is built as a more composable set of Kubernetes controllers
  (source-controller, kustomize-controller, helm-controller,
  notification-controller) with no separate UI by default, favoring a
  toolkit approach that integrates into existing GitOps-adjacent tooling
  rather than presenting its own dashboard.

Both support **multi-cluster** fan-out from one or a small number of Git
repositories, and both distinguish a Git-repository-level reconciliation
interval from an immediate webhook-triggered sync, trading a small amount
of reconciliation latency for resilience against a missed webhook.

### Progressive delivery

A GitOps controller answers "does the cluster match Git." **Progressive
delivery** tools answer a narrower, riskier question: given a new version
is being rolled out, is it actually healthy, and should the rollout
continue automatically? **Argo Rollouts** and **Flagger** both replace (or
sit alongside) a Deployment with a custom resource that drives a
**canary** (a small percentage of traffic shifted to the new version,
increased in steps) or **blue-green** (a full parallel environment,
cut over atomically) rollout, gated by an **Analysis** step that queries a
metrics provider — typically Prometheus — for error rate, latency, or a
custom business metric, and automatically **aborts and rolls back** if
the new version's metrics breach a defined threshold before traffic
shifts further. This closes the loop between deployment and the
observability stack covered in depth in Chapter 09: a rollout is not
"successful" merely because pods reached `Running`, it is successful
because the metrics that matter stayed within bounds while real traffic
hit the new version.

### Software supply chain security: from provenance to enforcement

Chapter 01 covered signing an individual image digest with cosign.
Enterprise supply chain security extends that single control into a
framework:

- **SLSA (Supply-chain Levels for Software Artifacts)** defines a ladder
  of increasing build integrity guarantees, from SLSA 1 (a documented
  build process exists) through SLSA 3 (a hardened, tamper-resistant
  build platform generates non-forgeable provenance). Higher levels
  progressively reduce the ability of a compromised build input or a
  malicious insider to produce an artifact that appears legitimate.
- **In-toto attestations** are signed, structured statements about a
  step in the software supply chain — "this specific source commit was
  built by this specific CI job, producing this specific digest" — that
  a consumer (a policy engine, an admission controller) can verify
  cryptographically rather than trust by convention.
- **SBOM (Software Bill of Materials)** generation, covered in Chapter
  01's implementation, becomes a supply-chain input here: a policy can
  require an SBOM exists and reference it during admission, not merely
  generate one as a build-time artifact nobody consults.

The chain closes at deployment time: Chapter 06's Kyverno `verifyImages`
rule (or an equivalent Gatekeeper/OPA policy, or Sigstore's dedicated
`policy-controller`) enforces that only images carrying a valid signature
— and, at higher maturity, a valid provenance attestation matching an
expected builder identity — are ever admitted to the cluster, turning the
supply chain from a set of independently useful build-time practices into
an end-to-end enforced property.

## Design Considerations

**Helm vs. Kustomize is a distribution-vs-composition decision, not a
maturity ranking.** Publishing software for others to consume across
many unrelated environments favors Helm's templating and versioned
packaging. Managing an organization's own applications across a known,
finite set of environments (dev/staging/prod, or per-region clusters)
often favors Kustomize's patch model, since there is no need to
parameterize for unknown consumers and plain YAML is easier to review as
a diff in a pull request than a rendered template.

**GitOps repository structure determines blast radius.** A single
monorepo holding every application and every environment gives strong
cross-cutting visibility and atomic multi-app changes, at the cost of
broad access if repository-level permissions are not further scoped. Splitting
by environment (a `production` repo separate from `staging`) or by team
gives narrower blast radius and clearer ownership at the cost of
coordinating changes that must land consistently across repos. Most
platform teams land on a hybrid: an `apps` repo per team or service, and a
separate, more tightly access-controlled `platform`/`fleet` repo the
platform team owns, referenced by ApplicationSet/Flux Kustomization
generators rather than manually enumerated.

**Self-healing GitOps needs an explicit break-glass path.** Automatic
drift reversion is a feature until an incident genuinely requires an
immediate manual change faster than a commit-review-merge-sync cycle
allows. Both Argo CD and Flux support a temporary sync-pause or
manual-override annotation for exactly this scenario — document and
rehearse that path before an incident, not during one, since discovering
it live during an outage costs time the incident does not have.

**Canary analysis is only as good as the metric it queries.** A canary
gated on request-count-derived error rate will happily promote a version
that silently degrades a metric it was never told to check — a
business-logic correctness bug that returns `200` with wrong data, for
example. Progressive delivery reduces blast radius for the failure modes
its Analysis step actually measures; it does not substitute for adequate
pre-production testing, and the Analysis metrics chosen deserve the same
design scrutiny as an SLO (Chapter 09).

**Supply chain enforcement should ratchet up, not appear fully-formed.**
Requiring valid signatures on every image is a reasonable starting
enforcement point with low false-positive risk once Chapter 01's signing
step is already in every pipeline. Requiring a specific provenance
attestation and matching builder identity is a stronger control but a
larger lift — every existing pipeline needs a compliant attestation
step before enforcement can flip from `audit` to `enforce`, mirroring the
Pod Security admission rollout pattern from Chapter 06 exactly.

## Implementation and Automation

### A Helm chart consumed with environment-specific values

```bash
helm repo add platform-charts https://charts.example.internal
helm repo update

# Render only, for review — no cluster access required.
helm template checkout-api platform-charts/web-service \
  --values values-production.yaml > rendered-production.yaml

# Actual install/upgrade, tracked as a Helm release.
helm upgrade --install checkout-api platform-charts/web-service \
  --namespace payments --create-namespace \
  --values values-production.yaml \
  --set image.tag=2.3.1
```

### Kustomize base and overlay

```yaml
# base/kustomization.yaml
resources:
  - deployment.yaml
  - service.yaml
---
# overlays/production/kustomization.yaml
resources:
  - ../../base
patches:
  - target: { kind: Deployment, name: checkout-api }
    patch: |-
      - op: replace
        path: /spec/replicas
        value: 5
images:
  - name: checkout-api
    newName: registry.example.internal/payments/checkout-api
    newTag: "2.3.1"
```

```bash
kubectl kustomize overlays/production | kubectl diff -f -
kubectl apply -k overlays/production
```

### Argo CD Application pointing at Git as source of truth

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: checkout-api
  namespace: argocd
spec:
  project: payments
  source:
    repoURL: https://git.example.internal/platform/payments-apps.git
    targetRevision: main
    path: checkout-api/overlays/production
  destination:
    server: https://kubernetes.default.svc
    namespace: payments
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
```

```bash
argocd app sync checkout-api
argocd app get checkout-api

# Confirm no manual drift exists against Git's declared state.
argocd app diff checkout-api
```

### Canary rollout with Argo Rollouts, gated on Prometheus error rate

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: checkout-api
  namespace: payments
spec:
  replicas: 5
  strategy:
    canary:
      steps:
        - setWeight: 20
        - pause: { duration: 5m }
        - analysis:
            templates:
              - templateName: error-rate-check
        - setWeight: 50
        - pause: { duration: 5m }
        - setWeight: 100
  selector:
    matchLabels: { app: checkout-api }
  template:
    metadata:
      labels: { app: checkout-api }
    spec:
      containers:
        - name: checkout-api
          image: registry.example.internal/payments/checkout-api:2.3.1
---
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: error-rate-check
  namespace: payments
spec:
  metrics:
    - name: error-rate
      interval: 1m
      successCondition: result[0] < 0.01
      failureLimit: 2
      provider:
        prometheus:
          address: http://prometheus.monitoring.svc:9090
          query: |
            sum(rate(http_requests_total{app="checkout-api",status=~"5.."}[2m]))
            /
            sum(rate(http_requests_total{app="checkout-api"}[2m]))
```

```bash
kubectl argo rollouts get rollout checkout-api -n payments --watch
kubectl argo rollouts promote checkout-api -n payments   # manual promotion, if desired
kubectl argo rollouts abort checkout-api -n payments     # force rollback
```

### Enforcing signature and provenance verification at admission

```bash
# Generate SLSA-style provenance during the CI build (GitHub Actions example).
slsa-github-generator generate-provenance \
  --artifact-path registry.example.internal/payments/checkout-api@sha256:<digest>
```

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-provenance-attestation
spec:
  validationFailureAction: Enforce
  rules:
    - name: verify-slsa-provenance
      match:
        any:
          - resources: { kinds: ["Pod"] }
      verifyImages:
        - imageReferences: ["registry.example.internal/payments/*"]
          attestors:
            - entries:
                - keyless:
                    subject: "https://ci.example.internal/app-build"
                    issuer: "https://token.actions.githubusercontent.com"
          attestations:
            - predicateType: https://slsa.dev/provenance/v1
              conditions:
                - all:
                    - key: "{{ builder.id }}"
                      operator: Equals
                      value: "https://ci.example.internal/app-build"
```

## Validation and Troubleshooting

```bash
# GitOps sync and health status at a glance.
argocd app list
flux get kustomizations -A

# Why is a sync stuck OutOfSync?
argocd app diff checkout-api
flux logs --level=error --kind=Kustomization

# Rollout step history and why an analysis run failed.
kubectl argo rollouts get rollout checkout-api -n payments
kubectl describe analysisrun -n payments -l rollout=checkout-api
```

| Symptom | Likely cause | Diagnostic |
| --- | --- | --- |
| Argo CD/Flux shows `OutOfSync` indefinitely | A cluster-side field is mutated by another controller (HPA-managed `replicas`, a mutating webhook) not accounted for with an `ignoreDifferences` rule | `argocd app diff`; add a targeted `ignoreDifferences`/`ignore` entry rather than disabling self-heal broadly |
| Progressive delivery rollout stuck at a partial weight | An `AnalysisRun` failed and `failureLimit` was reached, halting promotion by design | `kubectl describe analysisrun`; check the underlying Prometheus query result |
| Deployment succeeds but the pod is immediately blocked at admission | Image signature/provenance policy from Chapter 06/07 rejected the digest (expected, working as intended, or a broken pipeline step) | `kubectl get events --field-selector reason=FailedCreate`; confirm the CI signing/attestation step actually ran and succeeded |
| Helm upgrade fails with `another operation (install/upgrade) in progress` | A prior Helm operation was interrupted, leaving the release lock held | `helm history <release>`; `helm rollback` to the last good revision or `--force` only after confirming no partial write is stuck |
| Self-healing GitOps reverts an emergency manual `kubectl edit` mid-incident | Working as designed — Git is the source of truth | Use the tool's documented sync-pause/override path; commit the emergency change to Git immediately afterward |

## Security and Best Practices

- Scope CI pipeline credentials to Git repository write access only;
  never grant a CI pipeline direct cluster API access under the GitOps
  model — that access belongs solely to the in-cluster controller.
- Enable `selfHeal` deliberately and document the break-glass override
  procedure before an incident forces the team to discover it live.
- Require signature verification (Chapter 01/06) as a baseline admission
  control for every production namespace before layering stronger
  provenance-attestation requirements on top.
- Pin canary/blue-green Analysis metrics to the same SLO definitions used
  for ongoing production alerting (Chapter 09) so a rollout gate and a
  production alert never disagree about what "healthy" means.
- Separate Git repository access by environment or team boundary rather
  than granting broad write access to a single monorepo covering every
  environment, unless repository-internal path-based protections
  (CODEOWNERS, branch protection) genuinely enforce the same boundary.
- Store Helm chart repositories and OCI-based chart registries behind the
  same scanning and mirroring controls established for container images
  in Chapter 01 — a chart can reference or template arbitrary manifests
  and deserves the same supply-chain scrutiny as an image.
- Version-pin chart dependencies and Kustomize remote bases to a specific
  Git ref or chart version rather than a floating branch/tag, for the
  same tag-mutability reasons discussed for images in Chapter 01.

## References and Knowledge Checks

**Authoritative references**

- Helm documentation, [helm.sh/docs](https://helm.sh/docs/), and Kustomize documentation, [kubectl.docs.kubernetes.io](https://kubectl.docs.kubernetes.io/references/kustomize/), version 1.31.x Kubernetes baseline per [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md).
- OpenGitOps / CNCF, [GitOps Principles](https://opengitops.dev/).
- Argo Project documentation, [Argo CD](https://argo-cd.readthedocs.io/) and [Argo Rollouts](https://argo-rollouts.readthedocs.io/); Flux documentation, [fluxcd.io](https://fluxcd.io/).
- SLSA project, [slsa.dev](https://slsa.dev/); in-toto project, [in-toto.io](https://in-toto.io/).
- Sigstore project, [policy-controller documentation](https://docs.sigstore.dev/policy-controller/overview/).

**Knowledge check**

1. What is the fundamental difference between a traditional push-based
   CI/CD pipeline and a GitOps pull-based reconciliation model, and what
   security benefit does the pull model provide?
2. When would you choose Kustomize's patch-based composition over Helm's
   templating, and when is combining both the right answer?
3. What does an Analysis step in a canary rollout actually gate on, and
   why is a rollout only as safe as the metrics it queries?
4. What is the practical difference between verifying an image's
   signature and verifying its SLSA provenance attestation, and why is
   the latter a stronger supply-chain guarantee?
5. Why does GitOps self-healing require a documented break-glass
   procedure, and what happens if an operator makes an emergency
   `kubectl edit` without using it?

## Hands-On Lab

**Objective:** Deploy an application through Argo CD from a local Git
repository, observe automatic sync, trigger self-healing against manual
drift, and confirm sync failure when the deployed image fails a signature
policy as a negative test.

### Prerequisites

- A `kind` cluster running Kubernetes 1.31.x with Argo CD installed.
- `git`, `kubectl`, and the `argocd` CLI installed locally.
- A local bare Git repository is sufficient — no external Git hosting
  required.

### Procedure

1. Create the cluster and install Argo CD.

   ```bash
   kind create cluster --name gitops-lab --image kindest/node:v1.31.4
   kubectl create namespace argocd
   kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/v2.13.0/manifests/install.yaml
   kubectl wait --for=condition=available --timeout=300s deployment/argocd-server -n argocd
   ```

2. Create a local Git repository holding a minimal manifest set, and
   serve it over the local filesystem (Argo CD supports `file://` for lab
   use via a lightweight local Git HTTP daemon).

   ```bash
   mkdir -p ~/labs/gitops-repo/app && cd ~/labs/gitops-repo
   cat > app/deployment.yaml <<'EOF'
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: demo-api
     namespace: gitops-lab
   spec:
     replicas: 2
     selector: { matchLabels: { app: demo-api } }
     template:
       metadata: { labels: { app: demo-api } }
       spec:
         containers:
           - name: demo-api
             image: registry.k8s.io/e2e-test-images/agnhost:2.53
             args: ["netexec", "--http-port=8080"]
   EOF
   git init -q && git add -A && git commit -q -m "initial manifest"
   git daemon --base-path=.. --export-all --reuseaddr --informative-errors --verbose &
   ```

3. Register the Application in Argo CD, pointing at the local `git://`
   repository, with automated sync and self-heal enabled.

   ```bash
   kubectl create namespace gitops-lab
   cat > application.yaml <<'EOF'
   apiVersion: argoproj.io/v1alpha1
   kind: Application
   metadata:
     name: demo-api
     namespace: argocd
   spec:
     project: default
     source:
       repoURL: git://host.docker.internal/gitops-repo
       targetRevision: HEAD
       path: app
     destination:
       server: https://kubernetes.default.svc
       namespace: gitops-lab
     syncPolicy:
       automated: { prune: true, selfHeal: true }
   EOF
   kubectl apply -f application.yaml
   kubectl get application demo-api -n argocd -w
   ```

   **Expected result:** `SYNC STATUS` reaches `Synced` and
   `HEALTH STATUS` reaches `Healthy` within about a minute. Press Ctrl+C
   once confirmed.

4. Confirm the deployment exists in the cluster exactly as declared in
   Git.

   ```bash
   kubectl get deployment demo-api -n gitops-lab
   ```

5. Introduce manual drift directly against the cluster, bypassing Git,
   and observe self-healing revert it.

   ```bash
   kubectl scale deployment demo-api -n gitops-lab --replicas=5
   sleep 30
   kubectl get deployment demo-api -n gitops-lab
   ```

   **Expected result:** replica count returns to `2` — the value
   declared in Git — without any manual intervention, demonstrating
   self-healing reconciliation.

### Negative test

6. Apply a Kyverno signature-verification policy requiring all images in
   `gitops-lab` to carry a valid cosign signature, then push a change to
   Git referencing an unsigned image, and confirm the resulting pod is
   blocked at admission even though Argo CD reports the sync itself as
   applied.

   ```bash
   kubectl apply -f https://raw.githubusercontent.com/kyverno/kyverno/main/config/install-latest-testing.yaml
   kubectl wait --for=condition=available --timeout=180s deployment/kyverno-admission-controller -n kyverno

   cat > policy.yaml <<'EOF'
   apiVersion: kyverno.io/v1
   kind: ClusterPolicy
   metadata:
     name: require-signed-images-lab
   spec:
     validationFailureAction: Enforce
     rules:
       - name: verify-signature
         match:
           any:
             - resources: { kinds: ["Pod"], namespaces: ["gitops-lab"] }
         verifyImages:
           - imageReferences: ["registry.k8s.io/*"]
             attestors:
               - entries:
                   - keyless:
                       subject: "https://this-signer-does-not-exist.example/build"
                       issuer: "https://token.actions.githubusercontent.com"
   EOF
   kubectl apply -f policy.yaml

   kubectl rollout restart deployment/demo-api -n gitops-lab
   kubectl get events -n gitops-lab --field-selector reason=FailedCreate
   ```

   **Expected result:** the restart's new ReplicaSet fails to create pods,
   and the event log shows a Kyverno admission rejection referencing
   `image verification failed` — because the deployed image was never
   signed by the (deliberately impossible) required identity. Argo CD's
   Application still shows the manifest as synced, illustrating that
   GitOps sync success and admission-time policy enforcement are
   independent controls.

### Cleanup

```bash
kubectl delete application demo-api -n argocd
kubectl delete namespace gitops-lab
kubectl delete clusterpolicy require-signed-images-lab
kill %1 2>/dev/null   # stop the git daemon background job
kind delete cluster --name gitops-lab
rm -rf ~/labs/gitops-repo
```

## Summary and Completion Checklist

Helm and Kustomize solve packaging and composition, respectively, and are
frequently combined rather than chosen exclusively. GitOps replaces a
push-based pipeline with a pull-based, self-healing in-cluster
controller, shrinking pipeline blast radius and making Git the
continuously enforced source of truth. Progressive delivery layers
metrics-gated, automatically-rolled-back rollout strategies on top of
that reconciliation loop. Software supply chain security extends
Chapter 01's per-image signing into a full framework — SLSA provenance,
in-toto attestations, and admission-time enforcement — turning delivery
integrity from a set of independently useful practices into an
end-to-end verifiable property.

- [ ] Can package and compose manifests with Helm and Kustomize, and
      justify when to combine them.
- [ ] Can configure a GitOps Application/Kustomization with automated
      sync and self-healing.
- [ ] Can configure a metrics-gated canary rollout and explain what
      happens when the Analysis step fails.
- [ ] Can map a build pipeline to SLSA provenance concepts and enforce
      signature/attestation verification at admission.
- [ ] Can diagnose GitOps drift, stuck sync, and blocked rollout
      promotion.
- [ ] Completed the hands-on lab, including the signature-policy
      negative test, and performed cleanup.
