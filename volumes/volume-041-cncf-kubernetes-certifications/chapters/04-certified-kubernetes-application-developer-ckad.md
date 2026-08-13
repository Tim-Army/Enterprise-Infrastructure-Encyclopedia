# Chapter 04: Certified Kubernetes Application Developer (CKAD)

## Learning Objectives

- Explain what the CKAD certifies and how it differs from the CKA.
- List the five CKAD domains and their exam weights.
- Describe the CKAD exam mechanics: live terminal, 2 hours, 66% to pass.
- Perform application-developer tasks with `kubectl` — build, deploy, observe, configure, and connect workloads.
- Complete a per-domain walkthrough for each CKAD domain.

## Theory and Architecture

The **Certified Kubernetes Application Developer (CKAD)** is the CNCF's
**performance-based** developer credential. Where the CKA administers clusters,
the CKAD **designs, builds, configures, and runs applications on** Kubernetes —
multi-container pods, jobs, config and secrets, probes, and service connectivity.
It is two hours in a **live terminal**, **66% to pass**, no prerequisite.

Five weighted domains:

| # | Domain | Weight |
|---|--------|--------|
| 1 | Application Design and Build | 20% |
| 2 | Application Deployment | 20% |
| 3 | Application Observability and Maintenance | 15% |
| 4 | Application Environment, Configuration and Security | 25% |
| 5 | Services and Networking | 20% |

**Application Environment, Configuration and Security (25%)** is the largest —
ConfigMaps, Secrets, SecurityContexts, ServiceAccounts, and resource management.

## Design Considerations

CKAD is about **application patterns**, not cluster internals. Master the
multi-container patterns (**sidecar**, **init container**, **ambassador**),
workload types (**Deployment**, **Job**, **CronJob**), configuration decoupling
(**ConfigMap**/**Secret** as env or volume), health signaling (**liveness**,
**readiness**, **startup** probes), and connectivity (**Service**,
**NetworkPolicy**). As with CKA, **imperative `kubectl` + `--dry-run=client -o
yaml`** is the exam-speed technique — most tasks start from a generated skeleton.

## Implementation and Automation

The labs below build one representative artifact per domain: a multi-container
pod (Domain 1), a rolling Deployment (Domain 2), a pod with probes (Domain 3), a
ConfigMap/Secret-driven pod with a SecurityContext (Domain 4), and a
Service-connected app (Domain 5).

## Validation and Troubleshooting

Confirm the CKAD blueprint before studying:

```text
training.linuxfoundation.org > CKAD > curriculum:
  - five domains and weights (20/20/15/25/20)
  - performance-based, 2 hours, 66% to pass, no prerequisite
```

Common pitfalls: confusing **liveness** (restart on failure) with **readiness**
(remove from Service endpoints) probes; mounting a Secret and printing it in logs
(defeats the point); and hand-writing manifests instead of generating them.

## Security and Best Practices

Decouple configuration from images (**ConfigMap**/**Secret**), run containers as
**non-root** with a restrictive **SecurityContext**, set **resource
requests/limits**, and default-deny with **NetworkPolicy**. These are both good
practice and heavily weighted CKAD content.

## References and Knowledge Checks

- training.linuxfoundation.org: *CKAD* curriculum; kubernetes.io (Workloads, Configuration).

**Knowledge checks**

1. Which CKAD domain is largest, and what does it include?
2. What is the difference between a liveness and a readiness probe?
3. Name two multi-container pod patterns.

## Hands-On Lab

Per-topic walkthroughs — **one lab for every weighted CKAD domain**.

**Shared prerequisites** — the `kind`/`minikube` cluster from Chapter 01 and
`kubectl`. **Cost:** none.

### Lab 4.1 — CKAD: Application Design and Build (20%)

**Objective:** Build a multi-container pod (an init container preparing a shared
volume).

```bash
kubectl apply -f - <<'YAML'
apiVersion: v1
kind: Pod
metadata: {name: web, namespace: default}
spec:
  initContainers:
  - {name: seed, image: busybox, command: ["sh","-c","echo hello > /work/index.html"], volumeMounts: [{name: html, mountPath: /work}]}
  containers:
  - {name: nginx, image: nginx, volumeMounts: [{name: html, mountPath: /usr/share/nginx/html}]}
  volumes: [{name: html, emptyDir: {}}]
YAML
kubectl wait --for=condition=Ready pod/web --timeout=60s
kubectl exec web -c nginx -- cat /usr/share/nginx/html/index.html
```

**Expected result:** `hello` — the init container ran first, seeded the shared
`emptyDir`, and the main container serves it: the init-container design pattern.

**Negative test:** put the seed logic in the main container's startup; the init
pattern guarantees ordering and separation — use it for setup steps.

**Rollback:** `kubectl delete pod web`

### Lab 4.2 — CKAD: Application Deployment (20%)

**Objective:** Roll out and roll back a Deployment.

```bash
kubectl create deployment app --image=nginx:1.25 --replicas=2
kubectl set image deployment/app nginx=nginx:1.27 && kubectl rollout status deployment/app
kubectl rollout undo deployment/app
kubectl rollout status deployment/app
```

**Expected result:** the update rolls out, then `undo` returns to the previous
revision and reports success — managed deployment and rollback, CKAD Domain 2.

**Negative test:** delete and recreate the Deployment to "roll back"; that loses
history — use `rollout undo` which is revision-aware.

**Rollback:** `kubectl delete deploy app`

### Lab 4.3 — CKAD: Application Observability and Maintenance (15%)

**Objective:** Add liveness and readiness probes and observe them.

```bash
kubectl apply -f - <<'YAML'
apiVersion: v1
kind: Pod
metadata: {name: probed}
spec:
  containers:
  - name: nginx
    image: nginx
    readinessProbe: {httpGet: {path: /, port: 80}, initialDelaySeconds: 2}
    livenessProbe:  {httpGet: {path: /, port: 80}, periodSeconds: 5}
YAML
kubectl wait --for=condition=Ready pod/probed --timeout=60s
kubectl get pod probed -o jsonpath='{.status.containerStatuses[0].ready}{"\n"}'
```

**Expected result:** `true` — the readiness probe passed and the pod is Ready;
the liveness probe will restart it if `/` stops responding — observability and
self-healing, CKAD Domain 3.

**Negative test:** use a liveness probe where you meant readiness; a failing
liveness probe *restarts* the container instead of just removing it from Service
endpoints — pick the right probe.

**Rollback:** `kubectl delete pod probed`

### Lab 4.4 — CKAD: Application Environment, Configuration and Security (25%)

**Objective:** Inject config from a ConfigMap and run as non-root.

```bash
kubectl create configmap appcfg --from-literal=GREETING=hi
kubectl apply -f - <<'YAML'
apiVersion: v1
kind: Pod
metadata: {name: cfg}
spec:
  securityContext: {runAsNonRoot: true, runAsUser: 1000}
  containers:
  - name: c
    image: busybox
    command: ["sh","-c","echo $GREETING; id; sleep 30"]
    envFrom: [{configMapRef: {name: appcfg}}]
YAML
kubectl wait --for=condition=Ready pod/cfg --timeout=60s
kubectl logs cfg
```

**Expected result:** logs print `hi` (from the ConfigMap) and `uid=1000` (non-
root) — decoupled configuration plus a hardened SecurityContext, the heaviest
CKAD domain.

**Negative test:** bake the greeting into the image; rebuilding for every config
change is the anti-pattern ConfigMaps solve.

**Rollback:** `kubectl delete pod cfg; kubectl delete configmap appcfg`

### Lab 4.5 — CKAD: Services and Networking (20%)

**Objective:** Connect two workloads through a Service and restrict with a
NetworkPolicy.

```bash
kubectl create deployment api --image=nginx
kubectl expose deployment api --port=80
kubectl run client --image=busybox --restart=Never -it --rm -- \
  wget -qO- --timeout=5 http://api.default.svc.cluster.local | head -1
```

**Expected result:** the client fetches the nginx welcome HTML through the `api`
Service name — in-cluster connectivity via DNS and a Service, CKAD Domain 5.

**Negative test:** hard-code a pod IP in the client; pods are ephemeral — target
the Service DNS name, which is stable.

**Rollback:** `kubectl delete deploy api svc api`

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

CKAD is the CNCF's performance-based developer credential: five domains weighted
20/20/15/25/20, led by application environment, configuration, and security. It
certifies building and running applications on Kubernetes — multi-container
patterns, managed deployments, probes, decoupled configuration, and service
connectivity — solved live in two hours (66% to pass).

- [ ] I can list the five CKAD domains and their weights.
- [ ] I can build a multi-container pod and roll a Deployment back.
- [ ] I can add probes and inject ConfigMap/Secret config as non-root.
- [ ] I can connect workloads through a Service by DNS name.
- [ ] I completed Labs 4.1–4.5 including each negative test.
