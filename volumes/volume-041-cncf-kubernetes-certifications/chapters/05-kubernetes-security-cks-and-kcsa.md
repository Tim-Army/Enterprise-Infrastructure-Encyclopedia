# Chapter 05: Kubernetes Security — CKS and KCSA

## Learning Objectives

- Explain the two Kubernetes security credentials: the performance-based CKS and the multiple-choice KCSA.
- List the CKS and KCSA domains and their exam weights.
- Describe the CKA prerequisite for CKS and the entry-level nature of KCSA.
- Apply cluster hardening, supply-chain, and runtime-security controls.
- Complete a per-domain walkthrough for every CKS and KCSA domain.

## Theory and Architecture

The CNCF certifies Kubernetes security at two levels:

- **Certified Kubernetes Security Specialist (CKS)** — **performance-based**, two
  hours in a live terminal, **67% to pass**, and it **requires an active CKA**.
  It is the deep, hands-on security credential, pinned to Kubernetes v1.35. Six
  weighted domains:

  | # | Domain | Weight |
  |---|--------|--------|
  | 1 | Cluster Setup | 15% |
  | 2 | Cluster Hardening | 15% |
  | 3 | System Hardening | 10% |
  | 4 | Minimize Microservice Vulnerabilities | 20% |
  | 5 | Supply Chain Security | 20% |
  | 6 | Monitoring, Logging and Runtime Security | 20% |

- **Kubernetes and Cloud Native Security Associate (KCSA)** — **multiple-choice**,
  90 minutes, entry-level, no prerequisite. It validates security *knowledge* —
  the 4Cs, component security, the threat model — as a stepping stone to CKS. Six
  weighted domains:

  | # | Domain | Weight |
  |---|--------|--------|
  | 1 | Overview of Cloud Native Security | 14% |
  | 2 | Kubernetes Cluster Component Security | 22% |
  | 3 | Kubernetes Security Fundamentals | 22% |
  | 4 | Kubernetes Threat Model | 16% |
  | 5 | Platform Security | 16% |
  | 6 | Compliance and Security Frameworks | 10% |

## Design Considerations

Take **KCSA** first to build the mental model (the **4Cs** — Cloud, Cluster,
Container, Code; the component attack surface; the threat model), then **CKS** to
prove you can *implement* it. CKS's back half — **microservice vulnerabilities**,
**supply chain**, and **runtime security** (60% combined) — is where most study
time should go: Pod Security Standards, seccomp/AppArmor, image scanning and
signing, SBOMs, and runtime detection with Falco. Because CKS is performance-
based, practice the actual controls on a cluster.

## Implementation and Automation

The labs below implement one representative control per CKS domain (API/kubelet
hardening, RBAC least privilege, node hardening, Pod Security admission, image
scanning/signing, audit and runtime detection) and reason through one concept per
KCSA domain (4Cs, component security, authn/authz, threat model, platform
controls, and frameworks). CKS controls use `kubectl` and standard Linux
security tooling.

## Validation and Troubleshooting

Confirm both blueprints before studying:

```text
training.linuxfoundation.org > CKS and KCSA > curricula:
  - CKS: six domains (15/15/10/20/20/20), performance-based, 67%, requires CKA
  - KCSA: six domains (14/22/22/16/16/10), multiple-choice, 90 min
```

Common pitfalls: attempting **CKS without an active CKA** (blocked); under-
weighting CKS Domains 4–6 (60% of the exam); and confusing **KCSA** (knowledge)
with **CKS** (hands-on) — they cover the same surface at different depths.

## Security and Best Practices

Default to **least privilege** (RBAC, ServiceAccount tokens), **restricted Pod
Security Standards**, **default-deny NetworkPolicies**, **non-root** containers
with seccomp/AppArmor, **scanned and signed images** with SBOMs, and **runtime
detection** (Falco) plus **audit logging**. These are the CKS domains and sound
production practice alike.

## References and Knowledge Checks

- training.linuxfoundation.org: *CKS* and *KCSA* curricula; kubernetes.io security docs; the CNCF cloud-native security whitepaper.

**Knowledge checks**

1. What is the prerequisite for CKS, and what is its passing score?
2. What are the 4Cs of cloud-native security?
3. Which three CKS domains together make up 60% of the exam?

## Hands-On Lab

Per-topic walkthroughs — **one lab for every weighted CKS and KCSA domain**.

**Shared prerequisites** — the `kind`/`minikube` cluster from Chapter 01,
`kubectl`, and a Linux shell. **Cost:** none.

### CKS — Certified Kubernetes Security Specialist

### Lab 5.1 — CKS: Cluster Setup (15%)

**Objective:** Apply a default-deny NetworkPolicy (a canonical Cluster Setup
control).

```bash
kubectl create namespace secure
kubectl apply -n secure -f - <<'YAML'
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata: {name: default-deny}
spec: {podSelector: {}, policyTypes: [Ingress, Egress]}
YAML
kubectl get netpol -n secure
```

**Expected result:** a `default-deny` policy selecting all pods for both
Ingress and Egress — the baseline that CKS Domain 1 establishes before allowing
specific flows.

**Negative test:** rely on the cluster's open-by-default networking; without a
default-deny, any pod can reach any other — start closed.

**Rollback:** `kubectl delete namespace secure`

### Lab 5.2 — CKS: Cluster Hardening (15%)

**Objective:** Restrict RBAC and disable ServiceAccount token automounting.

```bash
kubectl create serviceaccount app
kubectl patch serviceaccount app -p '{"automountServiceAccountToken": false}'
kubectl get sa app -o jsonpath='{.automountServiceAccountToken}{"\n"}'
kubectl auth can-i '*' '*' --as=system:serviceaccount:default:app
```

**Expected result:** `false` for automount and `no` for wildcard permissions —
minimizing the credential and RBAC surface, CKS Domain 2.

**Negative test:** leave the default token automounted in every pod; a
compromised pod then holds an API credential — disable it where unused.

**Rollback:** `kubectl delete sa app`

### Lab 5.3 — CKS: System Hardening (10%)

**Objective:** Reduce the host attack surface (kernel modules / open ports).

```bash
ss -tlnp 2>/dev/null | awk 'NR==1 || /LISTEN/' | head
echo "Harden: remove unused packages, restrict kernel modules, apply seccomp/AppArmor, minimize privileges"
```

**Expected result:** the host's listening ports (the surface to minimize) and the
node-hardening checklist — CKS Domain 3 (host, not just cluster).

**Negative test:** harden only Kubernetes objects and ignore the node OS; a
compromised node undermines the whole cluster — harden the host too.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.4 — CKS: Minimize Microservice Vulnerabilities (20%)

**Objective:** Enforce the restricted Pod Security Standard via namespace labels.

```bash
kubectl create namespace restricted
kubectl label namespace restricted \
  pod-security.kubernetes.io/enforce=restricted --overwrite
kubectl -n restricted run bad --image=nginx --privileged 2>&1 | head -2
```

**Expected result:** the privileged pod is **rejected** by Pod Security
admission (`violates PodSecurity "restricted"`) — enforcing workload isolation,
a top CKS domain.

**Negative test:** run privileged pods in an unlabeled namespace and assume
they're safe; without Pod Security enforcement there is no guardrail — label the
namespace.

**Rollback:** `kubectl delete namespace restricted`

### Lab 5.5 — CKS: Supply Chain Security (20%)

**Objective:** Reason about image provenance — digest pinning and SBOM.

```bash
# Pin by immutable digest, not a mutable tag
echo "image: nginx@sha256:<digest>   # digest is immutable; 'nginx:latest' is not"
kubectl create deployment web --image=nginx --dry-run=client -o yaml \
  | grep image:
echo "Also: scan images (Trivy/Grype) + generate an SBOM (Syft) + verify signatures (cosign)"
```

**Expected result:** the manifest's image line and the supply-chain checklist
(digest pinning, scanning, SBOM, signature verification) — CKS Domain 5.

**Negative test:** deploy `:latest`; the running image can change under you and
cannot be verified — pin to a digest and verify provenance.

**Rollback:** `kubectl delete deploy web 2>/dev/null || true`

### Lab 5.6 — CKS: Monitoring, Logging and Runtime Security (20%)

**Objective:** Define an audit-policy rule and a runtime-detection concept.

```bash
cat <<'YAML'
apiVersion: audit.k8s.io/v1
kind: Policy
rules:
- level: Metadata
  resources: [{group: "", resources: ["secrets"]}]   # audit all Secret access
YAML
echo "Runtime: Falco alerts on anomalies (shell in container, unexpected exec, sensitive mount)"
```

**Expected result:** an API-server audit rule capturing Secret access plus the
runtime-detection concept (Falco) — the detect-and-respond domain of CKS.

**Negative test:** run without audit logging or runtime detection; you cannot
investigate an incident you never recorded — enable both.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### KCSA — Kubernetes and Cloud Native Security Associate

### Lab 5.7 — KCSA: Overview of Cloud Native Security (14%)

**Objective:** Map a control to each of the 4Cs.

```bash
python3 - <<'PY'
fourC = {"Cloud":"harden the provider account + network",
         "Cluster":"RBAC, Pod Security, NetworkPolicy",
         "Container":"non-root, seccomp, minimal image",
         "Code":"dependency scanning, secrets management"}
for layer,ctrl in fourC.items(): print(f"{layer:9} -> {ctrl}")
PY
```

**Expected result:** the 4Cs each mapped to a control — the layered model that
frames KCSA.

**Negative test:** secure only the cluster and ignore the cloud account or the
code; the 4Cs are nested — a weak outer layer exposes the inner ones.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.8 — KCSA: Kubernetes Cluster Component Security (22%)

**Objective:** Identify the sensitive control-plane components to protect.

```bash
kubectl -n kube-system get pods -o name \
  | grep -E 'apiserver|etcd|controller|scheduler|kube-proxy' | head
echo "etcd holds all cluster state (incl. Secrets) -> encrypt at rest + restrict access"
```

**Expected result:** the control-plane components and the note that **etcd**
holds all state — the component attack surface KCSA Domain 2 emphasizes.

**Negative test:** leave etcd unencrypted and broadly reachable; anyone with etcd
access reads every Secret — encrypt at rest and lock it down.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.9 — KCSA: Kubernetes Security Fundamentals (22%)

**Objective:** Distinguish authentication from authorization in the request flow.

```bash
python3 - <<'PY'
flow = ["1. Authentication: who are you? (cert/token/OIDC)",
        "2. Authorization: may you? (RBAC)",
        "3. Admission: is it allowed/mutated? (Pod Security, webhooks)"]
for s in flow: print(s)
PY
```

**Expected result:** the authn → authz → admission pipeline every API request
passes through — the security fundamentals KCSA Domain 3 tests.

**Negative test:** assume a valid token means full access; authentication only
proves identity — **authorization** (RBAC) decides what it may do.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.10 — KCSA: Kubernetes Threat Model (16%)

**Objective:** Map a threat to its mitigation (privilege escalation).

```bash
python3 - <<'PY'
threats = {"Privilege escalation":"drop capabilities, no privileged, Pod Security restricted",
           "Persistence":"scan images, restrict hostPath, admission control",
           "Lateral movement":"NetworkPolicy default-deny + segmentation"}
for t,m in threats.items(): print(f"{t:22} -> {m}")
PY
```

**Expected result:** each threat vector mapped to a mitigation — the threat-model
reasoning KCSA Domain 4 requires.

**Negative test:** defend only the perimeter; the threat model includes insider
and lateral-movement paths — mitigate each vector.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.11 — KCSA: Platform Security (16%)

**Objective:** Describe supply-chain and admission platform controls.

```bash
python3 - <<'PY'
controls = ["Admission control (validating/mutating webhooks, Kyverno/OPA)",
            "Image policy: signed + scanned images only",
            "Observability: audit logs + runtime detection"]
for c in controls: print("-", c)
PY
```

**Expected result:** the platform-level controls (admission, image policy,
observability) KCSA Domain 5 covers — the guardrails a platform enforces for all
workloads.

**Negative test:** trust every image pushed to the registry; without admission/
image policy, an untrusted image can run — enforce a policy gate.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.12 — KCSA: Compliance and Security Frameworks (10%)

**Objective:** Map Kubernetes controls to a compliance benchmark.

```bash
python3 - <<'PY'
maps = {"CIS Kubernetes Benchmark":"control-plane + node config checks (kube-bench)",
        "NSA/CISA Kubernetes Hardening Guide":"pod security, network, audit",
        "NIST 800-190":"container security guidance"}
for fw,scope in maps.items(): print(f"{fw:38} -> {scope}")
PY
```

**Expected result:** Kubernetes controls mapped to recognized frameworks (CIS,
NSA/CISA, NIST 800-190) — the compliance grounding of KCSA Domain 6.

**Negative test:** claim compliance without measuring against a benchmark; run
**kube-bench** (CIS) to produce evidence.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Kubernetes security is certified at two levels: the performance-based **CKS**
(six domains 15/15/10/20/20/20, 67% to pass, requires CKA) implements the
controls, and the multiple-choice **KCSA** (six domains 14/22/22/16/16/10)
proves the knowledge — the 4Cs, component security, the threat model, and
compliance frameworks. Together they span hardening, supply chain, and runtime
security.

- [ ] I can list the CKS and KCSA domains and their weights.
- [ ] I can apply default-deny, Pod Security restricted, and RBAC least privilege.
- [ ] I can reason about supply-chain integrity and runtime detection.
- [ ] I can map controls to the 4Cs and to CIS/NSA/NIST frameworks.
- [ ] I completed Labs 5.1–5.12 including each negative test.
