# Chapter 07: Rancher and Kubernetes

## Learning Objectives

- Describe Rancher and the RKE2/K3s distributions.
- Manage clusters centrally with Rancher.
- Deploy and operate workloads with kubectl and Helm.
- Apply cluster access control and policy.
- Complete a walkthrough for each Rancher/Kubernetes topic.

## Theory and Architecture

**Rancher** is SUSE's **Kubernetes management platform** — a single control plane to provision,
manage, and secure many Kubernetes clusters across data centers and clouds. SUSE ships two Kubernetes
distributions: **RKE2** (a security-focused, government-grade distribution for servers) and **K3s** (a
lightweight distribution for edge and IoT). Rancher provides **centralized authentication and RBAC**
(map enterprise identities to cluster roles), a **catalog** of applications, monitoring, and policy
across all managed clusters. Day-to-day cluster operation uses the standard Kubernetes tools:
**kubectl** (deploy and inspect workloads — Pods, Deployments, Services), **Helm** (package and
release applications as charts), and Kubernetes objects (namespaces, ConfigMaps, Secrets). The value
is **consistent Kubernetes at scale** — provision RKE2/K3s clusters, govern them centrally through
Rancher, and operate workloads with familiar tools. This chapter teaches each with a hands-on
walkthrough (distribution choice, kubectl/Helm operation, and Rancher RBAC).

## Design Considerations

Choose **RKE2** for secure server clusters, **K3s** for edge/lightweight. Govern all clusters
centrally with **Rancher** (auth + RBAC + policy). Operate with **kubectl** and **Helm**. Use
**namespaces** for isolation and **RBAC** for least privilege. Apply monitoring and policy uniformly.

## Implementation and Automation

The labs choose a distribution, deploy with kubectl/Helm, and apply RBAC.

## Validation and Troubleshooting

Confirm the Rancher/Kubernetes model:

```text
Rancher = central control plane for many K8s clusters (provision + auth/RBAC + catalog + policy). Distributions: RKE2 (secure server), K3s (lightweight edge). Operate: kubectl (workloads) + Helm (packages) + namespaces/RBAC.
Value: consistent Kubernetes governed centrally.
```

Common pitfalls: managing each cluster in isolation (no central **RBAC/policy** — use Rancher); and
running everything in the **default** namespace.

## Security and Best Practices

Govern clusters centrally with **Rancher** (RBAC + policy), pick the right **distribution**, isolate
with **namespaces**, and enforce **least-privilege RBAC**. Operate with kubectl/Helm. All work is
authorized administration.

## Hands-On Lab

Rancher/Kubernetes walkthroughs. **Shared prerequisites** — a K3s/RKE2 lab cluster (or `kubectl` with
any cluster), `python3`. **Cost:** none (K3s is free and lightweight).

### Lab 7.1 — Choose a distribution

**Objective:** Match distribution to use case.

```python
python3 - <<'PY'
choices={"data-center servers (secure, compliant)":"RKE2","edge/IoT/small footprint":"K3s",
         "CI test cluster on a laptop":"K3s","government/FIPS workloads":"RKE2"}
for use,dist in choices.items(): print(f"{use:38}: {dist}")
PY
```

**Expected result:** each use case matched to **RKE2 or K3s** — SUSE Kubernetes distribution choice.

**Negative test:** run heavyweight full Kubernetes on an edge device; **K3s** is built for that — use
it.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.2 — Deploy a workload with kubectl

**Objective:** Run an application.

```bash
kubectl create namespace demo 2>/dev/null || echo "kubectl create namespace demo"
kubectl -n demo create deployment web --image=nginx --replicas=2 2>/dev/null || echo "kubectl create deployment web --image=nginx --replicas=2"
kubectl -n demo get pods 2>/dev/null || echo "kubectl get pods: 2 nginx pods Running"
```

**Expected result:** a **Deployment** with 2 pods running in the `demo` namespace — Kubernetes
operation.

**Negative test:** deploy into the **default** namespace with no isolation; use a **namespace** per
app/team.

**Rollback:** `kubectl delete namespace demo`.

### Lab 7.3 — Package with Helm

**Objective:** Release applications as charts.

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami 2>/dev/null || echo "helm repo add <name> <url>"
helm search repo nginx 2>/dev/null | head || echo "helm install my-web bitnami/nginx -n demo"
echo "Helm: package + version + release Kubernetes apps as charts (repeatable installs/upgrades)"
```

**Expected result:** **Helm** managing an application as a versioned chart — repeatable K8s releases.

**Negative test:** apply dozens of raw YAML files by hand for one app; **Helm** packages them — use a
chart.

**Rollback:** `helm uninstall my-web -n demo` (if installed).

### Lab 7.4 — Apply Rancher RBAC

**Objective:** Least-privilege cluster access.

```python
python3 - <<'PY'
rbac={"dev-team":"namespace 'demo': edit (deploy/manage workloads)","auditors":"cluster: view (read-only)",
      "platform":"cluster: admin"}
for role,access in rbac.items(): print(f"{role:10}: {access}")
print("Rancher: map enterprise identities to scoped cluster/namespace roles (least privilege)")
PY
```

**Expected result:** identities mapped to **scoped RBAC** roles — governed cluster access.

**Negative test:** give every developer **cluster-admin**; one mistake affects everything — scope with
**RBAC**.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Rancher governs many Kubernetes clusters centrally with auth, RBAC, and policy; SUSE's RKE2 (secure)
and K3s (lightweight) distributions run the workloads, operated with kubectl and Helm — consistent
Kubernetes at scale.

- [ ] I can choose RKE2 vs K3s.
- [ ] I can deploy a workload with kubectl.
- [ ] I can package with Helm.
- [ ] I can apply Rancher RBAC.
- [ ] I completed Labs 7.1–7.4 including each negative test.
