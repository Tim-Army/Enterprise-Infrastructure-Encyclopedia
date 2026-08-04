# Chapter 06: The OpenShift Track — Administration (EX280)

## Learning Objectives

- Map the OpenShift track: Technologist → EX280 (Administrator) → EX380 → Specialists → RHCA.
- Cover the EX280 objectives: projects, workloads, networking, storage, and RBAC on OpenShift.
- Drill each against a local single-node OpenShift/Kubernetes.

## The track

| Level | Credential | Exam |
|:---|:---|:---|
| L1 | Technologist (containers/OpenShift foundations) | EX180 |
| L2 | RHCS in OpenShift Administration | **EX280** (OCP 4.18) |
| L3 | Advanced OpenShift Administrator | EX380 |
| L4 | Specialists — MultiCluster Mgmt (EX480), OpenShift Virtualization (EX316), etc. | various |
| L5 | RHCA in OpenShift | EX280 + three same-track Specialists |

**EX280** is 100% hands-on (10–17 real tasks on OCP 4.18) and counts toward RHCA in OpenShift. It also mirrors the Red Hat half of the IBM Cloud Pak "PLUS" combos ([Volume CXXIII](../../volume-123-ibm-certifications/README.md)).

## Hands-On Lab

A local OpenShift practice cluster: **CRC (CodeReady Containers / OpenShift Local)**, or plain Kubernetes (`kind`/`minikube`) for the portable pieces — `oc` and `kubectl` share most verbs. **Cost:** none.

### Lab 6.1 — Projects and workloads

**Objective (task):** "Create a project, deploy an app, and expose it."

```bash
# oc on OpenShift; kubectl equivalents shown for kind/minikube
oc new-project lab 2>/dev/null || kubectl create namespace lab
oc create deployment web --image=registry.access.redhat.com/ubi9/httpd-24 2>/dev/null \
  || kubectl -n lab create deployment web --image=httpd
oc -n lab get pods 2>/dev/null || kubectl -n lab get pods
oc expose deployment web --port=8080 2>/dev/null || kubectl -n lab expose deployment web --port=80
```

**Expected result:** A project/namespace, a running deployment, and a service — projects (OpenShift's namespaces-with-policy), deployments, and services/routes are EX280's core. `oc get pods` showing `Running` is the checkpoint.

**Negative test:** `oc new-app` with an image the cluster can't pull (no pull secret) — pods stick in `ImagePullBackOff`; reading pod status is the primary EX280 debugging skill.

**Cleanup:** `oc delete project lab` / `kubectl delete namespace lab`.

### Lab 6.2 — Scaling, health, and updates

**Objective (task):** "Scale a deployment, add probes, and roll an update."

```bash
kubectl -n lab create deployment api --image=httpd 2>/dev/null
kubectl -n lab scale deployment api --replicas=3
kubectl -n lab set image deployment/api httpd=httpd:2.4
kubectl -n lab rollout status deployment/api --timeout=60s
kubectl -n lab get deployment api -o wide
```

**Expected result:** Three replicas, an image update rolled out with `rollout status` confirming — scaling, rolling updates/rollback, and readiness/liveness probes are EX280 objectives; the rollout is declarative and self-healing.

**Negative test:** Set an image tag that doesn't exist — the rollout stalls and `rollout status` times out; new pods `ImagePullBackOff` while old ones keep serving (rolling-update safety), which the exam expects you to recognize and roll back.

**Cleanup:** Namespace removed above.

### Lab 6.3 — Storage: persistent volumes

**Objective (task):** "Attach persistent storage to a workload via a claim."

```bash
kubectl -n lab apply -f - <<'EOF'
apiVersion: v1
kind: PersistentVolumeClaim
metadata: { name: data, namespace: lab }
spec: { accessModes: ["ReadWriteOnce"], resources: { requests: { storage: 1Gi } } }
EOF
kubectl -n lab get pvc data
```

**Expected result:** A PVC (`Bound` if a default StorageClass provisions it, else `Pending` awaiting a PV) — persistent storage via PVC/PV/StorageClass is an EX280 objective; the claim/volume/class triangle is the model.

**Negative test:** A PVC with no matching StorageClass or PV stays `Pending` forever — "storage attached but pod won't start" traces to an unbound claim, the exam's storage-debugging path.

**Cleanup:** `kubectl -n lab delete pvc data`.

### Lab 6.4 — RBAC and security context

**Objective (task):** "Grant a user view access to one project and understand SCCs."

```bash
kubectl -n lab create serviceaccount viewer 2>/dev/null
kubectl -n lab create rolebinding view-binding --clusterrole=view --serviceaccount=lab:viewer
kubectl -n lab get rolebinding view-binding -o wide
echo "OpenShift adds Security Context Constraints (SCC): restricted-v2 by default forbids running as root"
```

**Expected result:** A rolebinding granting `view` to a service account — RBAC (roles, cluster roles, bindings) plus OpenShift's **Security Context Constraints** (the `restricted-v2` SCC that blocks root containers by default) are EX280 security objectives.

**Negative test:** Deploy an image that insists on running as UID 0 under the default SCC — OpenShift refuses it; the SCC model (unlike vanilla Kubernetes) is a defining EX280 topic.

**Cleanup:** Namespace removed.

### Lab 6.5 — The Specialist path and RHCA in OpenShift

**Objective:** Understand the OpenShift RHCA assembly and its specialists.

```text
RHCA (OpenShift) = EX280/L2 + EX380/L3-adjacent + THREE OpenShift Specialists, e.g.:
  EX480 MultiCluster Management (ACM + ACS)
  EX316 OpenShift Virtualization (replaces the retired EX318 KVM specialist)
  EX288 Cloud-Native Developer / others in-track
```

**Expected result:** The OpenShift RHCA formula and its flagship specialists — **EX316 (OpenShift Virtualization)** is where Red Hat now directs virtualization candidates after retiring EX318, and **EX480 (MultiCluster Management)** covers Advanced Cluster Management and Advanced Cluster Security.

**Negative test:** Chasing the retired EX318 (RHV virtualization) — gone; EX316 on OpenShift Virtualization is the current path.

**Cleanup:** None (design).

## Summary and Completion Checklist

- [ ] Projects, workloads, scaling, and rolling updates drilled on a local cluster.
- [ ] PVC storage and RBAC + SCC security modeled.
- [ ] OpenShift RHCA formula and the EX318→EX316 shift understood.
