# Chapter 04: Deploying the Workloads

## Learning Objectives

- Enable Linkerd injection on the namespaces.
- Give each workload a distinct ServiceAccount — its identity.
- Deploy the meshed workloads and leave the PLC un-meshed.

## Hands-On Lab

### Lab 4.1 — Namespaces, injection, and identities

**Objective.** Create the namespaces with Linkerd injection annotated, and a ServiceAccount per workload.

**Walkthrough**

```bash
kubectl create namespace dc && kubectl annotate namespace dc linkerd.io/inject=enabled
kubectl create namespace ot && kubectl annotate namespace ot linkerd.io/inject=enabled
for sa in sa-web sa-api sa-db; do kubectl -n dc create serviceaccount $sa; done
kubectl -n ot create serviceaccount sa-hmi
```

**Expected result.** Both namespaces carry the `linkerd.io/inject=enabled` annotation; four ServiceAccounts exist.

**Negative test.** Forget the annotation and pods get no proxy — outside the mesh, so mTLS and policy do not apply. Confirm: `kubectl get ns dc -o jsonpath='{.metadata.annotations}'`.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.2 — Deploy the meshed services and clients

**Objective.** Deploy `db`, `api`, `web`, and `hmi`, each running as its own ServiceAccount so it gets a distinct identity.

**Walkthrough**

```bash
kubectl apply -f - <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata: { name: db, namespace: dc, labels: { app: db } }
spec:
  replicas: 1
  selector: { matchLabels: { app: db } }
  template:
    metadata: { labels: { app: db } }
    spec:
      serviceAccountName: sa-db
      containers:
        - name: db
          image: postgres:16
          env: [ { name: POSTGRES_PASSWORD, value: "LabAppPassw0rd!" }, { name: POSTGRES_DB, value: "lkdlab" } ]
          ports: [ { containerPort: 5432 } ]
---
apiVersion: v1
kind: Service
metadata: { name: db, namespace: dc }
spec: { selector: { app: db }, ports: [ { name: pg, port: 5432, targetPort: 5432 } ] }
---
apiVersion: apps/v1
kind: Deployment
metadata: { name: api, namespace: dc, labels: { app: api } }
spec:
  replicas: 1
  selector: { matchLabels: { app: api } }
  template:
    metadata: { labels: { app: api } }
    spec:
      serviceAccountName: sa-api
      containers:
        - { name: api, image: mccutchen/go-httpbin:v2.15.0, args: ["-port","8080"], ports: [ { containerPort: 8080 } ] }
---
apiVersion: v1
kind: Service
metadata: { name: api, namespace: dc }
spec: { selector: { app: api }, ports: [ { name: http, port: 8080, targetPort: 8080 } ] }
---
apiVersion: apps/v1
kind: Deployment
metadata: { name: web, namespace: dc, labels: { app: web } }
spec:
  replicas: 1
  selector: { matchLabels: { app: web } }
  template:
    metadata: { labels: { app: web } }
    spec:
      serviceAccountName: sa-web
      containers: [ { name: web, image: nicolaka/netshoot, command: ["sleep","infinity"] } ]
---
apiVersion: apps/v1
kind: Deployment
metadata: { name: hmi, namespace: ot, labels: { app: hmi } }
spec:
  replicas: 1
  selector: { matchLabels: { app: hmi } }
  template:
    metadata: { labels: { app: hmi } }
    spec:
      serviceAccountName: sa-hmi
      containers: [ { name: hmi, image: nicolaka/netshoot, command: ["sleep","infinity"] } ]
EOF
```

**Expected result.** Each pod shows **2/2** containers — the app plus the injected `linkerd-proxy`. Confirm with `kubectl get pods -n dc`.

**Negative test.** If a pod is `1/1`, the namespace annotation was missing or the pod predated it; `kubectl rollout restart` after annotating.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.3 — Deploy the un-meshed PLC

**Objective.** Deploy the PLC with injection **disabled**, modeling a device that can run no proxy.

**Walkthrough**

```bash
kubectl apply -f - <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata: { name: plc, namespace: ot, labels: { app: plc } }
spec:
  replicas: 1
  selector: { matchLabels: { app: plc } }
  template:
    metadata:
      labels: { app: plc }
      annotations: { linkerd.io/inject: disabled }
    spec:
      containers:
        - name: plc
          image: nicolaka/netshoot
          command: ["sh","-c","socat TCP-LISTEN:502,fork,reuseaddr SYSTEM:'echo modbus-ok' & sleep infinity"]
          ports: [ { containerPort: 502 } ]
---
apiVersion: v1
kind: Service
metadata: { name: plc, namespace: ot }
spec: { selector: { app: plc }, ports: [ { name: modbus, port: 502, targetPort: 502 } ] }
EOF
kubectl get pods -n ot
```

**Expected result.** `hmi` is **2/2** (meshed); `plc` is **1/1** (un-meshed). The PLC is in the cluster but outside the mesh.

**Negative test.** Remove the `linkerd.io/inject: disabled` annotation and the PLC gets a proxy — but a real PLC could not run one. The annotation models that.

**Rollback.** Keep the workloads.

## Summary and Completion Checklist

- [ ] Namespaces annotated for injection; four ServiceAccounts created.
- [ ] `web`, `api`, `db`, `hmi` meshed (2/2), each with its own ServiceAccount.
- [ ] `plc` un-meshed (1/1).
