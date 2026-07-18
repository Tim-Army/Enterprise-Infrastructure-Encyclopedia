# Chapter 06: Kubernetes Identity, Configuration, Policy, and Security

## Learning Objectives

- Explain Kubernetes RBAC's Role/ClusterRole/RoleBinding/ClusterRoleBinding
  model and design a least-privilege binding for a workload identity.
- Differentiate ConfigMaps and Secrets from external secrets management,
  and configure the External Secrets Operator or a CSI secrets provider.
- Apply Pod Security admission at the namespace level and explain why it
  replaced PodSecurityPolicy.
- Write and enforce policy-as-code with Kyverno or Gatekeeper, and compare
  both to the native `ValidatingAdmissionPolicy` CEL-based mechanism.
- Configure workload identity federation so pods authenticate to external
  cloud services without long-lived static credentials.

## Theory and Architecture

Chapter 02 traced a request through authentication, authorization, and
admission at the API server. This chapter goes deep on the three layers
that turn that pipeline into an enforced security boundary: who a
workload *is* (identity), what it is *allowed to change* (RBAC), what
configuration and secret material it *carries*, and what *policy*
constrains every object before it is ever persisted.

### ServiceAccounts and token identity

Every pod runs as a **ServiceAccount** — the workload-identity analog of a
human user, native to Kubernetes and namespaced. Since 1.24, Kubernetes no
longer auto-mints a long-lived Secret-backed token for every
ServiceAccount; instead, kubelet requests **bound, time-limited,
audience-scoped tokens** through the `TokenRequest` API, injected into the
pod's filesystem and automatically refreshed before expiry. A bound token
is cryptographically tied to the specific pod, ServiceAccount, and (by
default) a one-hour expiry window — a token exfiltrated from a compromised
pod is far less valuable than the old indefinitely valid Secret-mounted
token, since it expires quickly and is invalidated immediately if the pod
or ServiceAccount is deleted.

### RBAC: the authorization layer

Kubernetes RBAC (`rbac.authorization.k8s.io/v1`) is the near-universal
authorization mode referenced in Chapter 02, built from four object
types:

| Object | Scope | Purpose |
| --- | --- | --- |
| `Role` | Namespaced | A set of permitted verbs (`get`, `list`, `watch`, `create`, `update`, `patch`, `delete`) on resources within one namespace |
| `ClusterRole` | Cluster-wide | Same as `Role`, but for cluster-scoped resources or to be reused across namespaces via a `RoleBinding` |
| `RoleBinding` | Namespaced | Grants a `Role` (or a `ClusterRole`, scoped down to one namespace) to a subject |
| `ClusterRoleBinding` | Cluster-wide | Grants a `ClusterRole` cluster-wide to a subject |

A **subject** is a `User`, `Group`, or `ServiceAccount`. Kubernetes has no
built-in user database — human identity is always established externally
(a client certificate's Common Name, an OIDC token's claims) and RBAC
simply authorizes whatever identity authentication already established.
`ClusterRole` objects can also be **aggregated**: a controller-managed
`ClusterRole` can accumulate rules from other ClusterRoles labeled to
match its `aggregationRule` selector, which is how built-in roles like
`view`/`edit`/`admin` automatically pick up new permissions as CRDs
(Chapter 02) are installed and label themselves for aggregation, without
anyone hand-editing the base role.

RBAC is strictly additive — there is no `deny` rule. The effective
permission set for a subject is the union of every Role/ClusterRole bound
to it; the only way to restrict access is to grant fewer, narrower roles
in the first place.

### Configuration and secret material

**ConfigMaps** hold non-sensitive configuration, consumable as environment
variables, command-line arguments, or mounted files, with a mounted
ConfigMap's files updating automatically (subject to kubelet's sync
period) if the ConfigMap changes — environment-variable consumption does
not update without a pod restart. **Secrets** use the identical mechanism
but are base64-encoded (not encrypted — this is an encoding, not a
security control) and, depending on the API server's
`EncryptionConfiguration` (Chapter 02), may or may not be encrypted at
rest in etcd. Both support `immutable: true`, which prevents further
updates and lets the kubelet skip watching the object for changes — a
minor performance win at real scale and a safety win against accidental
in-place edits to config that should be versioned instead.

Native Secrets have a structural weakness for enterprise use: they still
live in etcd (even if encrypted there) and in Git if managed declaratively
without extra tooling, and native Kubernetes offers no built-in rotation,
external secret-store integration, or audit trail beyond the API server's
own. Two patterns close that gap:

- **External Secrets Operator (ESO)** watches a `SecretStore` /
  `ExternalSecret` CRD pair and syncs material from an external system
  (HashiCorp Vault, AWS Secrets Manager, Azure Key Vault, GCP Secret
  Manager) into a native Kubernetes Secret on a refresh interval — the
  workload still consumes an ordinary Secret, but the source of truth and
  rotation live outside the cluster.
- **Secrets Store CSI Driver** takes the opposite approach: it mounts
  secret material directly from the external store into the pod's
  filesystem as a volume, without ever creating a persistent Kubernetes
  Secret object at all, minimizing the material's footprint inside
  etcd.

### Pod Security admission

**PodSecurityPolicy** was removed in Kubernetes 1.25. Its replacement,
**Pod Security admission**, is a built-in admission controller configured
entirely through **namespace labels** — no separate policy object to
author or bind:

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: payments
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/enforce-version: v1.31
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
```

Three built-in **Pod Security Standards** define the levels:
`privileged` (unrestricted), `baseline` (blocks known privilege
escalations while remaining broadly compatible), and `restricted`
(enforces current pod hardening best practice: non-root, no privilege
escalation, seccomp `RuntimeDefault`, dropped capabilities, and more). The
`enforce` mode rejects non-compliant pods outright; `audit` and `warn`
flag violations without blocking, which is the recommended path for
raising a namespace's standard without an unannounced outage — run
`audit`/`warn` first, review the resulting audit log or `kubectl` warning
output, then flip to `enforce` once workloads are confirmed compliant.

### Policy-as-code beyond Pod Security admission

Pod Security admission only covers a fixed, opinionated set of pod-level
controls. Organization-specific rules — "every image must come from an
approved registry," "every Deployment must carry a `cost-center` label,"
"every image must carry a valid cosign signature" (tying directly back to
Chapter 01's signing workflow) — need a general-purpose policy engine:

- **Kyverno** writes policies as native-feeling Kubernetes YAML
  (`ClusterPolicy` objects) with `validate`, `mutate`, `generate`, and
  `verifyImages` rule types, requiring no new language to learn.
- **OPA Gatekeeper** wraps Open Policy Agent's Rego language in
  `ConstraintTemplate` and `Constraint` CRDs, trading a steeper authoring
  curve for a policy language shared with non-Kubernetes OPA use cases
  elsewhere in an organization.
- **`ValidatingAdmissionPolicy`** (GA as of 1.30, part of the 1.31.x
  baseline) is a native, in-process alternative using **CEL (Common
  Expression Language)** expressions directly in the API object — no
  webhook, no separate controller to run, and lower latency and failure
  surface than either Kyverno or Gatekeeper for validation-only rules. It
  does not yet cover mutation or image verification, which is why Kyverno
  or Gatekeeper remain necessary alongside it for a complete policy
  program, but `ValidatingAdmissionPolicy` is the right first choice for
  straightforward validation rules where its narrower feature set is
  sufficient.

## Design Considerations

**Bind least privilege at the ServiceAccount level, not the default
ServiceAccount.** Every namespace gets a `default` ServiceAccount
automatically; binding cluster-wide permissions to it (directly or via a
`ClusterRoleBinding`) grants those permissions to every pod in the
namespace that does not explicitly request a different identity. Create a
dedicated ServiceAccount per workload with only the verbs and resources
that workload actually needs, and set `automountServiceAccountToken:
false` on any ServiceAccount whose pods never call the Kubernetes API at
all — most application workloads fall into this category and gain nothing
from a mounted token except unnecessary attack surface.

**Choose ESO or the Secrets Store CSI Driver based on whether the
workload's consumption pattern can tolerate a native Secret object
existing at all.** ESO's synced-Secret model is simpler to adopt
incrementally (workloads keep consuming ordinary Secrets, unaware
anything changed upstream) and works with any consumer that already reads
env vars or mounted Secret volumes. The CSI driver's direct-mount model
is the stronger control for material that must never be persisted as a
cluster object — but it requires the workload to read secret material
from a file path rather than an environment variable, which is a larger
adoption lift for existing applications.

**Rolling out `restricted` Pod Security admission cluster-wide is a
migration, not a flag flip.** Namespaces running long-lived workloads
built before hardened defaults were the norm often fail `restricted`
immediately — root-requiring base images, workloads needing specific
Linux capabilities, or init containers performing privileged setup. The
`audit`/`warn` labels exist specifically to surface this gap before
`enforce` is applied, and a platform team should budget real remediation
time per namespace rather than treating the migration as a single
cluster-wide change.

**A policy engine's failure mode matters as much as its rule language.**
Kyverno and Gatekeeper both run as validating (and, for Kyverno, mutating)
admission webhooks — if the webhook is unreachable, the API server's
`failurePolicy` setting decides whether requests are blocked (`Fail`,
safer but can stall the cluster if the policy engine itself is down) or
allowed through unchecked (`Ignore`, more available but a silent policy
bypass during an outage). `ValidatingAdmissionPolicy` avoids this
failure mode entirely for the rules it covers, since it evaluates
in-process inside kube-apiserver with no external webhook round trip —
one more reason to prefer it where its CEL-only feature set is
sufficient.

**Workload identity federation should replace static cloud credentials
everywhere it is supported.** IRSA (IAM Roles for Service Accounts) on
EKS, Workload Identity on GKE, and Azure AD Workload Identity on AKS all
implement the same underlying pattern: a pod's projected, bound
ServiceAccount token (the same OIDC-compatible token described above) is
exchanged for short-lived cloud credentials via a trust relationship
between the cluster's OIDC issuer and the cloud IAM system, eliminating
any long-lived cloud access key stored as a Kubernetes Secret. Any
workload still authenticating to a cloud API with a static access key
mounted from a Secret should be migrated to workload identity federation
as a standing security backlog item, not deferred indefinitely as
low-priority hardening.

## Implementation and Automation

### Least-privilege RBAC for a workload ServiceAccount

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: checkout-api
  namespace: payments
automountServiceAccountToken: false
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: checkout-api-configreader
  namespace: payments
rules:
  - apiGroups: [""]
    resources: ["configmaps"]
    verbs: ["get", "list", "watch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: checkout-api-configreader
  namespace: payments
subjects:
  - kind: ServiceAccount
    name: checkout-api
    namespace: payments
roleRef:
  kind: Role
  name: checkout-api-configreader
  apiGroup: rbac.authorization.k8s.io
```

```bash
# Confirm exactly what a ServiceAccount can and cannot do before shipping it.
kubectl auth can-i list secrets \
  --as=system:serviceaccount:payments:checkout-api -n payments
kubectl auth can-i list configmaps \
  --as=system:serviceaccount:payments:checkout-api -n payments
```

### External Secrets Operator syncing from Vault

```yaml
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: vault-backend
  namespace: payments
spec:
  provider:
    vault:
      server: "https://vault.example.internal:8200"
      path: "secret"
      version: v2
      auth:
        kubernetes:
          mountPath: "kubernetes"
          role: "payments-checkout-api"
---
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: checkout-db-credentials
  namespace: payments
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: vault-backend
    kind: SecretStore
  target:
    name: checkout-db-credentials
  data:
    - secretKey: password
      remoteRef:
        key: payments/order-db
        property: password
```

### Namespace-level Pod Security admission rollout

```bash
# Start in audit/warn only, generating visibility without blocking anything.
kubectl label namespace payments \
  pod-security.kubernetes.io/audit=restricted \
  pod-security.kubernetes.io/warn=restricted \
  pod-security.kubernetes.io/enforce=baseline --overwrite

# Surface violations before enforcing the stricter standard.
kubectl get events -n payments --field-selector reason=FailedCreate

# After remediation, raise enforce to match.
kubectl label namespace payments \
  pod-security.kubernetes.io/enforce=restricted --overwrite
```

### Policy-as-code with Kyverno, and the CEL-native alternative

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-signed-images
spec:
  validationFailureAction: Enforce
  rules:
    - name: verify-cosign-signature
      match:
        any:
          - resources: { kinds: ["Pod"] }
      verifyImages:
        - imageReferences: ["registry.example.internal/*"]
          attestors:
            - entries:
                - keyless:
                    subject: "https://ci.example.internal/app-build"
                    issuer: "https://token.actions.githubusercontent.com"
---
apiVersion: admissionregistration.k8s.io/v1
kind: ValidatingAdmissionPolicy
metadata:
  name: require-resource-limits
spec:
  failurePolicy: Fail
  matchConstraints:
    resourceRules:
      - apiGroups: [""]
        apiVersions: ["v1"]
        operations: ["CREATE"]
        resources: ["pods"]
  validations:
    - expression: >
        object.spec.containers.all(c, has(c.resources.limits) &&
        has(c.resources.limits.memory))
      message: "Every container must declare a memory limit."
---
apiVersion: admissionregistration.k8s.io/v1
kind: ValidatingAdmissionPolicyBinding
metadata:
  name: require-resource-limits-binding
spec:
  policyName: require-resource-limits
  validationActions: ["Deny"]
```

The Kyverno policy directly enforces Chapter 01's cosign-signing supply
chain control at admission time; the `ValidatingAdmissionPolicy` enforces
a resource-hygiene rule from Chapter 03 with no webhook in the request
path at all.

### Workload identity federation (EKS IRSA pattern)

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: checkout-api
  namespace: payments
  annotations:
    eks.amazonaws.com/role-arn: "arn:aws:iam::123456789012:role/payments-checkout-api"
```

```bash
# Confirm the pod actually received a projected, audience-scoped token
# rather than a legacy long-lived Secret-mounted one.
kubectl exec -n payments deploy/checkout-api -- \
  cat /var/run/secrets/eks.amazonaws.com/serviceaccount/token | cut -d. -f2 | base64 -d
```

## Validation and Troubleshooting

```bash
# What would this identity actually be allowed to do, resource by resource?
kubectl auth can-i --list --as=system:serviceaccount:payments:checkout-api -n payments

# Which admission webhooks are registered, and are they reachable?
kubectl get validatingwebhookconfigurations
kubectl get mutatingwebhookconfigurations

# Why did a pod get rejected by Pod Security admission or a policy engine?
kubectl get events -n payments --field-selector reason=FailedCreate -o wide
kubectl logs -n kyverno deploy/kyverno-admission-controller --tail=50
```

| Symptom | Likely cause | Diagnostic |
| --- | --- | --- |
| `Forbidden` errors from a workload calling the Kubernetes API | RBAC binding missing a required verb/resource, or wrong ServiceAccount attached to the pod | `kubectl auth can-i --list --as=...`; confirm `spec.serviceAccountName` on the pod |
| Pod creation rejected at admission with a Pod Security message | Namespace `enforce` level stricter than the pod's `securityContext` satisfies | `kubectl describe namespace` labels; compare pod spec against the `restricted` requirements |
| `ExternalSecret` never populates the target Secret | `SecretStore` auth misconfigured, or the Vault/cloud role lacks read access to the path | `kubectl describe externalsecret`; ESO controller logs |
| Policy engine blocks all pod creation cluster-wide unexpectedly | `failurePolicy: Fail` on a webhook whose backing pods are down (Kyverno/Gatekeeper controller crashed or unreachable) | `kubectl get pods -n kyverno` / `-n gatekeeper-system`; consider a scoped `failurePolicy: Ignore` for non-critical rules |
| Cloud API calls from a pod fail with `AccessDenied` despite a correct IAM policy | ServiceAccount missing the workload-identity annotation, or OIDC trust relationship misconfigured on the cloud side | Decode the projected token's claims; verify the cloud IAM trust policy's `sub`/`aud` conditions match |

## Security and Best Practices

- Grant RBAC at the narrowest scope that satisfies the workload — a
  namespaced `Role`/`RoleBinding` in preference to a `ClusterRole`/
  `ClusterRoleBinding` whenever the permission does not genuinely need to
  span the cluster.
- Set `automountServiceAccountToken: false` by default and opt individual
  workloads back in only when they call the Kubernetes API.
- Never store long-lived cloud credentials as native Secrets; migrate to
  workload identity federation (IRSA, GKE Workload Identity, Azure AD
  Workload Identity) as the default authentication path to cloud
  services.
- Treat base64-encoded Secret content as encoded, not encrypted; rely on
  API server encryption-at-rest (Chapter 02) and, for stronger separation
  of duties, an external secrets store rather than the encoding alone.
- Roll out `restricted` Pod Security admission namespace by namespace
  using `audit`/`warn` before `enforce`, and treat any namespace still on
  `privileged` as a tracked security debt item, not a permanent
  exception.
- Combine `ValidatingAdmissionPolicy` for simple, high-frequency
  validation rules with Kyverno or Gatekeeper for mutation and image
  verification, rather than choosing one mechanism exclusively.
- Set an explicit, reviewed `failurePolicy` on every admission webhook;
  understand and accept the trade-off between `Fail` (safer, can stall
  admission during an outage) and `Ignore` (more available, a silent
  policy bypass) for each policy rather than leaving it at an unexamined
  default.
- Audit ClusterRoleBindings and cluster-admin-equivalent bindings on a
  recurring schedule; unused broad grants accumulate quietly and are a
  common finding in cluster security reviews.

## References and Knowledge Checks

**Authoritative references**

- Kubernetes documentation, [Using RBAC Authorization](https://kubernetes.io/docs/reference/access-control/rbac/), version 1.31.x baseline per [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md).
- Kubernetes documentation, [Secrets](https://kubernetes.io/docs/concepts/configuration/secret/) and [Pod Security Admission](https://kubernetes.io/docs/concepts/security/pod-security-admission/).
- Kubernetes documentation, [ValidatingAdmissionPolicy](https://kubernetes.io/docs/reference/access-control/validating-admission-policy/).
- External Secrets Operator documentation, [external-secrets.io](https://external-secrets.io/).
- Kyverno documentation, [kyverno.io](https://kyverno.io/), and Open Policy Agent Gatekeeper documentation, [open-policy-agent.github.io/gatekeeper](https://open-policy-agent.github.io/gatekeeper/).

**Knowledge check**

1. Why is Kubernetes RBAC strictly additive, and what does that imply
   about how a platform team must structure roles to achieve least
   privilege?
2. What changed about ServiceAccount tokens starting in Kubernetes 1.24,
   and why does a bound, time-limited token reduce the impact of a
   compromised pod compared to the old default?
3. What is the practical difference between the External Secrets
   Operator's synced-Secret model and the Secrets Store CSI Driver's
   direct-mount model?
4. Why does Pod Security admission provide `audit` and `warn` modes
   separate from `enforce`, and how should they be used together during a
   migration?
5. What failure-mode trade-off does `failurePolicy: Fail` versus
   `failurePolicy: Ignore` impose on a validating admission webhook, and
   how does `ValidatingAdmissionPolicy` avoid that trade-off for the rules
   it covers?

## Hands-On Lab

**Objective:** Build a least-privilege ServiceAccount, prove RBAC denies
unauthorized access, roll out Pod Security admission from audit to
enforce, and confirm a native `ValidatingAdmissionPolicy` blocks a
non-compliant pod as a negative test.

### Prerequisites

- A `kind` cluster running Kubernetes 1.31.x (`ValidatingAdmissionPolicy`
  requires 1.30+; the API is GA at the 1.31.x baseline with no feature
  gate required).
- `kubectl` matching the cluster's minor version.

### Procedure

1. Create the cluster and a lab namespace.

   ```bash
   kind create cluster --name identity-lab --image kindest/node:v1.31.4
   kubectl create namespace identity-lab
   ```

2. Create a least-privilege ServiceAccount that can only read ConfigMaps.

   ```bash
   cat > rbac.yaml <<'EOF'
   apiVersion: v1
   kind: ServiceAccount
   metadata:
     name: reader
     namespace: identity-lab
   ---
   apiVersion: rbac.authorization.k8s.io/v1
   kind: Role
   metadata:
     name: configmap-reader
     namespace: identity-lab
   rules:
     - apiGroups: [""]
       resources: ["configmaps"]
       verbs: ["get", "list", "watch"]
   ---
   apiVersion: rbac.authorization.k8s.io/v1
   kind: RoleBinding
   metadata:
     name: configmap-reader
     namespace: identity-lab
   subjects:
     - kind: ServiceAccount
       name: reader
       namespace: identity-lab
   roleRef:
     kind: Role
     name: configmap-reader
     apiGroup: rbac.authorization.k8s.io
   EOF
   kubectl apply -f rbac.yaml
   ```

3. Confirm the ServiceAccount can read ConfigMaps but not Secrets.

   ```bash
   kubectl auth can-i list configmaps --as=system:serviceaccount:identity-lab:reader -n identity-lab
   kubectl auth can-i list secrets --as=system:serviceaccount:identity-lab:reader -n identity-lab
   ```

   **Expected result:** `yes` for ConfigMaps, `no` for Secrets — RBAC is
   enforcing exactly the narrow grant defined.

4. Label the namespace for Pod Security admission in audit/warn mode
   first, deploy a deliberately non-compliant pod, and confirm it is
   created but flagged rather than blocked.

   ```bash
   kubectl label namespace identity-lab \
     pod-security.kubernetes.io/audit=restricted \
     pod-security.kubernetes.io/warn=restricted --overwrite

   kubectl run noncompliant --image=busybox:1.36 -n identity-lab \
     --command -- sleep infinity
   kubectl get pod noncompliant -n identity-lab
   ```

   **Expected result:** the `kubectl run` command prints a warning
   referencing `restricted` requirements (root user, missing seccomp
   profile), but the pod is still created because `enforce` was not set.

5. Raise `enforce` to `restricted` and confirm a new non-compliant pod is
   now rejected outright.

   ```bash
   kubectl label namespace identity-lab \
     pod-security.kubernetes.io/enforce=restricted --overwrite
   kubectl run noncompliant-2 --image=busybox:1.36 -n identity-lab \
     --command -- sleep infinity
   ```

   **Expected result:** the command fails with an error referencing the
   `restricted` Pod Security Standard, confirming `enforce` now blocks
   what `audit`/`warn` only flagged.

### Negative test

6. Apply a `ValidatingAdmissionPolicy` requiring every pod to declare a
   memory limit, then attempt to create a compliant pod that satisfies
   Pod Security admission but omits the limit, and confirm CEL-based
   admission rejects it independently of the Pod Security controls
   already in place.

   ```bash
   cat > vap.yaml <<'EOF'
   apiVersion: admissionregistration.k8s.io/v1
   kind: ValidatingAdmissionPolicy
   metadata:
     name: require-memory-limit
   spec:
     failurePolicy: Fail
     matchConstraints:
       resourceRules:
         - apiGroups: [""]
           apiVersions: ["v1"]
           operations: ["CREATE"]
           resources: ["pods"]
     validations:
       - expression: >
           object.spec.containers.all(c, has(c.resources) &&
           has(c.resources.limits) && has(c.resources.limits.memory))
         message: "Every container must declare a memory limit."
   ---
   apiVersion: admissionregistration.k8s.io/v1
   kind: ValidatingAdmissionPolicyBinding
   metadata:
     name: require-memory-limit-binding
   spec:
     policyName: require-memory-limit
     validationActions: ["Deny"]
     matchResources:
       namespaceSelector:
         matchLabels:
           kubernetes.io/metadata.name: identity-lab
   EOF
   kubectl apply -f vap.yaml

   cat > no-limit-pod.yaml <<'EOF'
   apiVersion: v1
   kind: Pod
   metadata:
     name: no-limit-pod
     namespace: identity-lab
   spec:
     securityContext:
       runAsNonRoot: true
       seccompProfile: { type: RuntimeDefault }
     containers:
       - name: app
         image: busybox:1.36
         command: ["sleep", "infinity"]
         securityContext:
           allowPrivilegeEscalation: false
           capabilities: { drop: ["ALL"] }
         resources:
           requests: { memory: "32Mi" }
   EOF
   kubectl apply -f no-limit-pod.yaml
   ```

   **Expected result:** the API server rejects the pod with a message
   citing `require-memory-limit` and "Every container must declare a
   memory limit" — the pod satisfies `restricted` Pod Security admission
   entirely (non-root, dropped capabilities, seccomp) yet is still
   blocked by the independent CEL policy, demonstrating that admission
   controls compose rather than substitute for one another.

### Cleanup

```bash
kubectl delete namespace identity-lab
kubectl delete validatingadmissionpolicybinding require-memory-limit-binding
kubectl delete validatingadmissionpolicy require-memory-limit
kind delete cluster --name identity-lab
rm -f rbac.yaml vap.yaml no-limit-pod.yaml
```

## Summary and Completion Checklist

Workload identity in Kubernetes runs on bound, short-lived
ServiceAccount tokens rather than static credentials; RBAC's strictly
additive model means least privilege has to be designed in from the
start, not layered on as a deny rule later. ConfigMaps and Secrets cover
basic configuration and secret delivery, but enterprise secret management
generally needs an external store integrated through the External
Secrets Operator or the Secrets Store CSI Driver. Pod Security admission
replaced PodSecurityPolicy with a simpler, namespace-label-driven model
with a built-in audit/warn migration path, and general-purpose policy
enforcement — Kyverno, Gatekeeper, and the newer CEL-native
`ValidatingAdmissionPolicy` — closes the gap for organization-specific
rules Pod Security admission does not cover. Workload identity federation
extends the same bound-token pattern to eliminate static cloud
credentials entirely.

- [ ] Can design a least-privilege RBAC binding for a specific workload
      identity.
- [ ] Can explain bound ServiceAccount tokens and why they replaced the
      old auto-mounted long-lived token.
- [ ] Can configure external secrets delivery via ESO or the Secrets
      Store CSI Driver.
- [ ] Can roll out Pod Security admission from audit/warn to enforce at
      the namespace level.
- [ ] Can write a validation policy in Kyverno/Gatekeeper or as a native
      `ValidatingAdmissionPolicy` and explain when each is the better
      choice.
- [ ] Completed the hands-on lab, including the CEL policy negative test,
      and performed cleanup.
