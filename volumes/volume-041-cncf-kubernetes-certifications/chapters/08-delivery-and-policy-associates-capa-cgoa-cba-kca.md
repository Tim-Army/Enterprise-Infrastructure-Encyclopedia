# Chapter 08: Delivery and Policy Associates — CAPA, CGOA, CBA, KCA

## Learning Objectives

- Explain the four delivery-and-policy associate credentials: CAPA (Argo), CGOA (GitOps), CBA (Backstage), and KCA (Kyverno).
- List each credential's domains and exam weights.
- Relate the four to the platform lifecycle: deliver (Argo/GitOps), catalog (Backstage), and govern (Kyverno).
- Apply Argo, GitOps, Backstage, and Kyverno skills.
- Complete a per-domain walkthrough for every domain of all four credentials.

## Theory and Architecture

Four CNCF associate exams cover how software is **delivered, catalogued, and
governed** on Kubernetes — all multiple-choice, 90 minutes, no prerequisite:

- **Certified Argo Project Associate (CAPA)** — the Argo ecosystem. Domains:
  Argo **Workflows** 36% · Argo **CD** 34% · Argo **Rollouts** 18% · Argo
  **Events** 12%.
- **Certified GitOps Associate (CGOA)** — vendor-neutral GitOps. Domains: GitOps
  **Terminology** 20% · **Principles** 30% · **Related Practices** 16% ·
  **Patterns** 20% · **Tooling** 14%.
- **Certified Backstage Associate (CBA)** — internal developer portals. Domains:
  Backstage **Development Workflow** 24% · **Infrastructure** 22% · **Catalog**
  22% · **Customizing Backstage** 32%.
- **Kyverno Certified Associate (KCA)** — Kubernetes-native policy. Domains:
  **Fundamentals** 18% · **Installation, Configuration, and Upgrades** 18% ·
  **Kyverno CLI** 12% · **Applying Policies** 10% · **Writing Policies** 32% ·
  **Policy Management** 10%.

## Design Considerations

These map onto the **platform lifecycle**: **GitOps** (CGOA) is the delivery
philosophy; **Argo CD** (CAPA) is a leading GitOps engine and Argo Workflows/
Rollouts/Events add CI-style pipelines and progressive delivery; **Backstage**
(CBA) is the developer portal and service catalog on top; and **Kyverno** (KCA)
enforces policy as admission-control guardrails. Study each project's flagship
concept: Argo's **Application** and **Workflow** CRDs, GitOps's **four
principles**, Backstage's **catalog-info.yaml**, and Kyverno's **validate/mutate/
generate** rules.

## Implementation and Automation

The labs below use each project's CRDs and CLIs (or portable manifests) so every
domain is concrete without requiring all four platforms installed at once.

## Validation and Troubleshooting

Confirm all four blueprints before studying:

```text
training.linuxfoundation.org > CAPA / CGOA / CBA / KCA > curricula:
  - CAPA (36/34/18/12), CGOA (20/30/16/20/14), CBA (24/22/22/32), KCA (18/18/12/10/32/10)
  - all multiple-choice, 90 minutes, no prerequisite
```

Common pitfalls: confusing **Argo Workflows** (pipelines) with **Argo CD**
(GitOps deployment); thinking GitOps is "just CI/CD" (it is **declarative,
Git-as-source-of-truth, continuously reconciled**); and confusing Kyverno's
**validate** (allow/deny) with **mutate** (change) and **generate** (create)
rules.

## Security and Best Practices

Make **Git the single source of truth** and let a controller **reconcile** it
(no manual `kubectl apply` to production); enforce policy with **Kyverno**
admission rules (default-deny risky configs); and expose a **golden-path**
catalog in Backstage so developers self-serve within guardrails. These reduce
drift and misconfiguration — the whole point of the four credentials.

## References and Knowledge Checks

- training.linuxfoundation.org: *CAPA*, *CGOA*, *CBA*, *KCA* curricula; argoproj.github.io; opengitops.dev; backstage.io; kyverno.io.

**Knowledge checks**

1. What is the difference between Argo Workflows and Argo CD?
2. What are the four GitOps principles?
3. What are Kyverno's three rule types?

## Hands-On Lab

Per-topic walkthroughs — **one lab for every weighted domain of all four
credentials**.

**Shared prerequisites** — the `kind`/`minikube` cluster from Chapter 01,
`kubectl`, and a Linux shell with `python3`. **Cost:** none.

### CAPA — Certified Argo Project Associate

### Lab 8.1 — CAPA: Argo Workflows (36%)

**Objective:** Read a Workflow's DAG structure (the Argo pipeline model).

```bash
cat <<'YAML'
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata: {generateName: build-}
spec:
  entrypoint: main
  templates:
  - name: main
    dag:
      tasks:
      - {name: build, template: echo}
      - {name: test,  template: echo, dependencies: [build]}
      - {name: deploy, template: echo, dependencies: [test]}
  - {name: echo, container: {image: alpine, command: [echo, hi]}}
YAML
echo "DAG: build -> test -> deploy, each a containerized step. Argo's heaviest domain."
```

**Expected result:** a Workflow with a `build → test → deploy` DAG — the
container-native pipeline model of CAPA's largest domain.

**Negative test:** expect steps to run in listed order without `dependencies`; a
DAG runs tasks in parallel unless dependencies impose order — declare them.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.2 — CAPA: Argo CD (34%)

**Objective:** Read an Argo CD Application (GitOps deployment).

```bash
cat <<'YAML'
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata: {name: guestbook, namespace: argocd}
spec:
  project: default
  source: {repoURL: https://github.com/org/repo, path: manifests, targetRevision: main}
  destination: {server: https://kubernetes.default.svc, namespace: demo}
  syncPolicy: {automated: {prune: true, selfHeal: true}}
YAML
echo "Argo CD reconciles cluster state to Git; selfHeal reverts manual drift."
```

**Expected result:** an Application syncing a Git path to the cluster with
`selfHeal`/`prune` — the GitOps deployment engine of CAPA Domain 2.

**Negative test:** `kubectl edit` a resource Argo CD manages; `selfHeal` reverts
it to Git — change Git, not the cluster.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.3 — CAPA: Argo Rollouts (18%)

**Objective:** Describe a canary progressive-delivery strategy.

```bash
cat <<'YAML'
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata: {name: web}
spec:
  strategy:
    canary:
      steps: [{setWeight: 20}, {pause: {duration: 60}}, {setWeight: 50}, {pause: {}}]
YAML
echo "Canary: shift 20% -> pause/analyze -> 50% -> manual promote. Argo Rollouts."
```

**Expected result:** a canary Rollout stepping 20% → 50% with pauses — the
progressive-delivery pattern of CAPA Domain 3.

**Negative test:** flip 100% of traffic at once ("big bang"); a canary limits
blast radius by shifting gradually with analysis gates.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.4 — CAPA: Argo Events (12%)

**Objective:** Describe event-driven triggering.

```bash
python3 - <<'PY'
print("Argo Events: EventSource (e.g., webhook/S3/Kafka) -> Sensor -> trigger (e.g., a Workflow).")
print("Enables event-driven automation: a git push or message starts a pipeline.")
PY
```

**Expected result:** the EventSource → Sensor → trigger chain — the event-driven
automation of CAPA Domain 4.

**Negative test:** poll on a timer for changes; Argo Events reacts to **events**
(webhooks/messages) — push, don't poll.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### CGOA — Certified GitOps Associate

### Lab 8.5 — CGOA: GitOps Terminology (20%)

**Objective:** Define the core GitOps terms.

```bash
python3 - <<'PY'
terms = {"Desired state":"declared in Git","Actual state":"what's in the cluster",
         "Reconciliation":"agent converges actual -> desired",
         "Drift":"actual diverges from desired (auto-corrected)"}
for t,d in terms.items(): print(f"{t:16}: {d}")
PY
```

**Expected result:** the GitOps vocabulary (desired/actual state, reconciliation,
drift) — CGOA Domain 1.

**Negative test:** call any CI/CD pipeline "GitOps"; GitOps specifically means
**declarative desired state in Git, continuously reconciled** — not every
pipeline qualifies.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.6 — CGOA: GitOps Principles (30%)

**Objective:** State the four OpenGitOps principles.

```bash
python3 - <<'PY'
for i,p in enumerate(["Declarative","Versioned and immutable",
                      "Pulled automatically","Continuously reconciled"],1):
    print(f"{i}. {p}")
PY
```

**Expected result:** the four OpenGitOps principles — the heaviest CGOA domain.

**Negative test:** push changes imperatively to the cluster; GitOps is
**pull-based reconciliation** from a versioned, declarative source — the agent
pulls.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.7 — CGOA: Related Practices (16%)

**Objective:** Relate GitOps to CI/CD, IaC, and DevOps.

```bash
python3 - <<'PY'
rel = {"CI":"builds/tests + produces artifacts (before GitOps CD)",
       "CD (GitOps)":"reconciles declared state from Git",
       "IaC":"declarative infra (GitOps applies it), DevOps: the culture"}
for k,v in rel.items(): print(f"{k:12}: {v}")
PY
```

**Expected result:** GitOps situated against CI, CD, IaC, and DevOps — the
related-practices context of CGOA Domain 3.

**Negative test:** treat GitOps as a replacement for CI; CI still builds/tests —
GitOps handles the **CD/reconcile** half.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.8 — CGOA: GitOps Patterns (20%)

**Objective:** Contrast repository and deployment patterns.

```bash
python3 - <<'PY'
patterns = {"Monorepo vs polyrepo":"one repo vs per-app repos",
            "App-of-apps":"a root app that manages child apps",
            "Environment promotion":"promote via branch/dir/overlay per env",
            "Pull vs push delivery":"GitOps prefers pull (agent in cluster)"}
for k,v in patterns.items(): print(f"{k:24}: {v}")
PY
```

**Expected result:** common GitOps patterns (repo layout, app-of-apps, env
promotion, pull delivery) — CGOA Domain 4.

**Negative test:** hard-code environment differences into one manifest; use
**overlays/branches** to promote across environments.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.9 — CGOA: Tooling (14%)

**Objective:** Identify GitOps engines and their model.

```bash
python3 - <<'PY'
tools = {"Argo CD":"pull-based reconciler (Application CRD)",
         "Flux":"pull-based GitOps toolkit (controllers)",
         "Common":"both watch Git and reconcile the cluster"}
for k,v in tools.items(): print(f"{k:8}: {v}")
PY
```

**Expected result:** the leading GitOps tools (Argo CD, Flux) and their shared
pull-reconcile model — CGOA Domain 5.

**Negative test:** assume a CI runner doing `kubectl apply` is a GitOps tool; a
GitOps engine **continuously reconciles** from Git in-cluster.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### CBA — Certified Backstage Associate

### Lab 8.10 — CBA: Backstage Development Workflow (24%)

**Objective:** Describe running Backstage locally and its stack.

```bash
python3 - <<'PY'
print("Backstage: a TypeScript/React app (frontend) + Node backend.")
print("Dev loop: `yarn install` -> `yarn dev` (or `yarn start`) -> local portal at :3000.")
print("Package as a container for production deployment.")
PY
```

**Expected result:** the Backstage local dev workflow and stack — CBA Domain 1.

**Negative test:** expect a no-code product; Backstage is a **framework** you
build and extend in TypeScript — code is involved.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.11 — CBA: Backstage Infrastructure (22%)

**Objective:** Describe the client-server architecture and config.

```bash
python3 - <<'PY'
print("Frontend (React) <-> Backend (Node plugins) <-> databases + integrations (GitHub, k8s).")
print("Config via app-config.yaml (+ app-config.production.yaml) — env-specific overrides.")
PY
```

**Expected result:** the Backstage client-server architecture and `app-config`
model — CBA Domain 2.

**Negative test:** put production secrets in `app-config.yaml`; use environment
variables / a secrets store referenced from config.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.12 — CBA: Backstage Catalog (22%)

**Objective:** Register a component with a catalog-info descriptor.

```bash
cat <<'YAML'
apiVersion: backstage.io/v1alpha1
kind: Component
metadata: {name: payments-api, annotations: {github.com/project-slug: org/payments}}
spec: {type: service, lifecycle: production, owner: team-payments}
YAML
echo "catalog-info.yaml registers a software entity; the catalog is Backstage's core."
```

**Expected result:** a `catalog-info.yaml` describing a service entity (owner,
lifecycle, type) — the Software Catalog that anchors CBA Domain 3.

**Negative test:** track services in a spreadsheet; the **catalog** ingests
descriptors from source repos and stays current — register entities in code.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.13 — CBA: Customizing Backstage (32%)

**Objective:** Describe extending Backstage with plugins.

```bash
python3 - <<'PY'
print("Frontend plugins: add pages/tabs (React); Backend plugins: add APIs/processors (Node).")
print("Customize: Material UI theming, add a plugin (e.g., Kubernetes, TechDocs), wire routes.")
print("This is Backstage's heaviest domain — the portal is meant to be extended.")
PY
```

**Expected result:** how Backstage is extended (frontend/backend plugins,
theming, routes) — CBA's largest domain (Domain 4).

**Negative test:** fork core to add a feature; write a **plugin** instead so
upgrades stay clean.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### KCA — Kyverno Certified Associate

### Lab 8.14 — KCA: Fundamentals of Kyverno (18%)

**Objective:** Explain Kyverno as a Kubernetes-native policy engine.

```bash
python3 - <<'PY'
print("Kyverno: policy as Kubernetes resources (no new language) via an admission webhook.")
print("Three rule types: VALIDATE (allow/deny), MUTATE (modify), GENERATE (create resources).")
PY
```

**Expected result:** Kyverno's model (policies as CRDs, admission webhook) and the
three rule types — KCA Domain 1.

**Negative test:** assume you must learn Rego (OPA); Kyverno uses **YAML
policies**, not a separate language — that is its selling point.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.15 — KCA: Installation, Configuration, and Upgrades (18%)

**Objective:** Describe installing Kyverno and its CRDs.

```bash
python3 - <<'PY'
print("Install via Helm (kyverno/kyverno). Provides ClusterPolicy/Policy CRDs + admission webhooks.")
print("Configure failurePolicy, webhook timeouts, and resource filters; upgrade via Helm.")
PY
```

**Expected result:** the Helm-based install, CRDs, and webhook configuration —
KCA Domain 2.

**Negative test:** set `failurePolicy: Fail` on a slow webhook without tuning
timeouts; you can block all admissions — tune timeouts and scope.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.16 — KCA: Kyverno CLI (12%)

**Objective:** Test a policy offline with the Kyverno CLI.

```bash
echo "kyverno apply policy.yaml --resource pod.yaml    # test policy against a manifest"
echo "kyverno test .                                    # run a policy test suite"
echo "kyverno jp '<jmespath>'                           # evaluate JMESPath expressions"
```

**Expected result:** the `kyverno apply`/`test`/`jp` commands for offline policy
testing — KCA Domain 3.

**Negative test:** deploy a policy straight to the cluster to see if it works;
test it with the **Kyverno CLI** first to avoid blocking real workloads.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.17 — KCA: Applying Policies (10%)

**Objective:** Scope a policy with resource selection.

```bash
cat <<'YAML'
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata: {name: require-labels}
spec:
  validationFailureAction: Enforce
  rules:
  - name: check-team
    match: {any: [{resources: {kinds: [Pod]}}]}
    validate:
      message: "label 'team' is required"
      pattern: {metadata: {labels: {team: "?*"}}}
YAML
echo "Enforce mode blocks Pods lacking a 'team' label; match selects the resources."
```

**Expected result:** a ClusterPolicy in `Enforce` mode requiring a `team` label
on Pods — applying and scoping policy (KCA Domain 4).

**Negative test:** start in `Enforce` cluster-wide without testing; use **Audit**
mode first to see impact, then enforce.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.18 — KCA: Writing Policies (32%)

**Objective:** Write a mutate rule (add a default).

```bash
cat <<'YAML'
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata: {name: add-default-securitycontext}
spec:
  rules:
  - name: default-nonroot
    match: {any: [{resources: {kinds: [Pod]}}]}
    mutate:
      patchStrategicMerge:
        spec: {securityContext: {runAsNonRoot: true}}
YAML
echo "Mutate injects runAsNonRoot into Pods that omit it. Writing rules = KCA's heaviest domain."
```

**Expected result:** a mutate policy defaulting `runAsNonRoot: true` — authoring
validate/mutate/generate rules, KCA's largest domain (Domain 5).

**Negative test:** expect a `validate` rule to change resources; only **mutate**
modifies them — validate only allows/denies.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.19 — KCA: Policy Management (10%)

**Objective:** Read policy results via Policy Reports.

```bash
echo "kubectl get policyreport -A        # per-namespace pass/fail results"
echo "kubectl get clusterpolicyreport    # cluster-scoped results"
echo "PolicyException lets you grant a scoped, documented exemption."
```

**Expected result:** the PolicyReport/ClusterPolicyReport resources and
PolicyException — managing and auditing policy at scale (KCA Domain 6).

**Negative test:** disable a policy globally to unblock one workload; grant a
scoped **PolicyException** instead, keeping the policy in force elsewhere.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Four associates cover delivering, cataloguing, and governing software on
Kubernetes: **CAPA** (Argo: Workflows/CD/Rollouts/Events), **CGOA** (GitOps
terminology, the four principles, patterns, tooling), **CBA** (Backstage dev
workflow, infrastructure, catalog, customization), and **KCA** (Kyverno
fundamentals, install, CLI, applying and writing policies, management). Together
they are the platform-delivery and policy layer.

- [ ] I can list all four credentials' domains and weights.
- [ ] I can read an Argo Workflow and Application and a canary Rollout.
- [ ] I can state the four GitOps principles and register a Backstage component.
- [ ] I can write Kyverno validate and mutate rules and read Policy Reports.
- [ ] I completed Labs 8.1–8.19 including each negative test.
