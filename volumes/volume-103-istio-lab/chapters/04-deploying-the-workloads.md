# Chapter 04: Deploying the Workloads

## Learning Objectives

- Enable sidecar injection on the namespaces.
- Give each workload a distinct **ServiceAccount** — its identity.
- Deploy the meshed workloads, and leave the PLC deliberately un-meshed.

Identity in Istio comes from the **ServiceAccount**, so each workload gets its own. The `plc` is excluded from injection to represent a device that can run no sidecar.

## Hands-On Lab

### Lab 4.1 — Namespaces, injection, and identities

**Objective.** Create the namespaces with sidecar injection, and a ServiceAccount per workload.

**Walkthrough**

```bash
kubectl create namespace dc && kubectl label namespace dc istio-injection=enabled
kubectl create namespace ot && kubectl label namespace ot istio-injection=enabled
for sa in sa-web sa-api sa-db; do kubectl -n dc create serviceaccount $sa; done
kubectl -n ot create serviceaccount sa-hmi
```

**Expected result.** Both namespaces are labeled `istio-injection=enabled`; four ServiceAccounts exist.

**Negative test.** Forget to label a namespace and its pods get no sidecar — they are outside the mesh, and mTLS/authz will not apply. Confirm the labels: `kubectl get ns -L istio-injection`.

**Cleanup.** None.

### Lab 4.2 — Deploy the meshed services (api, db) and clients (web, hmi)

**Objective.** Deploy the workloads that join the mesh, each running as its own ServiceAccount.

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
          env: [ { name: POSTGRES_PASSWORD, value: "LabAppPassw0rd!" }, { name: POSTGRES_DB, value: "istiolab" } ]
          ports: [ { containerPort: 5432 } ]
---
apiVersion: v1
kind: Service
metadata: { name: db, namespace: dc }
spec: { selector: { app: db }, ports: [ { name: tcp-pg, port: 5432, targetPort: 5432 } ] }
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
        - name: api
          image: mccutchen/go-httpbin:v2.15.0
          args: ["-port","8080"]
          ports: [ { containerPort: 8080 } ]
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

**Expected result.** Each pod shows **2/2** containers (`kubectl get pods -n dc`) — the app plus the injected `istio-proxy` sidecar. The Istio service port names (`http`, `tcp-pg`) matter: Istio uses the port name prefix to know a port is HTTP versus plain TCP.

**Negative test.** Name the API service port `api` instead of `http` and Istio treats it as plain TCP, so L7 HTTP authorization in Chapter 07 will not apply. Prefix HTTP ports with `http`.

**Cleanup.** None.

### Lab 4.3 — Deploy the un-meshed PLC

**Objective.** Deploy the PLC with sidecar injection **disabled**, representing a device that cannot join the mesh.

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
      annotations: { sidecar.istio.io/inject: "false" }
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
spec: { selector: { app: plc }, ports: [ { name: tcp-modbus, port: 502, targetPort: 502 } ] }
EOF
kubectl get pods -n ot
```

**Expected result.** `hmi` shows **2/2** (meshed); `plc` shows **1/1** (no sidecar — un-meshed). The PLC is in the cluster but outside the mesh, exactly like an OT device that can run no proxy.

**Negative test.** Remove the `sidecar.istio.io/inject: "false"` annotation and the PLC gets a sidecar — but a real PLC could not run one. The annotation models that constraint.

**Cleanup.** Keep the workloads.

## Summary and Completion Checklist

- [ ] Namespaces `dc` and `ot` labeled for injection; four ServiceAccounts created.
- [ ] `web`, `api`, `db`, `hmi` meshed (2/2 containers), each with its own ServiceAccount.
- [ ] `plc` deployed un-meshed (1/1), modeling a device that can run no sidecar.
- [ ] HTTP service ports named with an `http` prefix.
