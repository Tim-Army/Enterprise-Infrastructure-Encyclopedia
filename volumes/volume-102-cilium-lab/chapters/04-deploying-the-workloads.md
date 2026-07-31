# Chapter 04: Deploying the Workloads

## Learning Objectives

- Create the two namespaces and the five labeled workloads.
- Expose the database, the HTTP API, and the PLC as services.
- Confirm every workload is running before testing connectivity.

The estate is five pods: `web`, `db`, and `api` in namespace `dc`; `hmi` and `plc` in namespace `ot`. The `api` (an HTTP service) exists so Chapter 08 can enforce Layer 7 policy.

## Hands-On Lab

### Lab 4.1 — Create namespaces

```bash
kubectl create namespace dc
kubectl create namespace ot
```

**Expected result.** Both namespaces `Active`.

**Negative test.** Deploy into `default` by forgetting `-n`; namespace-scoped policy will not select those pods. Keep workloads in `dc`/`ot`.

**Cleanup.** None.

### Lab 4.2 — Deploy the services: db, api, and plc

**Objective.** Stand up the three things others connect to.

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
      containers:
        - name: db
          image: postgres:16
          env:
            - { name: POSTGRES_PASSWORD, value: "LabAppPassw0rd!" }
            - { name: POSTGRES_DB, value: "cilab" }
          ports: [ { containerPort: 5432 } ]
---
apiVersion: v1
kind: Service
metadata: { name: db, namespace: dc }
spec: { selector: { app: db }, ports: [ { port: 5432, targetPort: 5432 } ] }
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
      containers:
        - name: api
          image: mccutchen/go-httpbin:v2.15.0
          args: ["-port","8080"]
          ports: [ { containerPort: 8080 } ]
---
apiVersion: v1
kind: Service
metadata: { name: api, namespace: dc }
spec: { selector: { app: api }, ports: [ { port: 8080, targetPort: 8080 } ] }
---
apiVersion: apps/v1
kind: Deployment
metadata: { name: plc, namespace: ot, labels: { app: plc } }
spec:
  replicas: 1
  selector: { matchLabels: { app: plc } }
  template:
    metadata: { labels: { app: plc } }
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
spec: { selector: { app: plc }, ports: [ { port: 502, targetPort: 502 } ] }
EOF
```

**Expected result.** `db`, `api`, and `plc` become `Running`.

**Negative test.** `kubectl logs -n dc deploy/db` if postgres crash-loops — usually a missing `POSTGRES_PASSWORD`.

**Cleanup.** None.

### Lab 4.3 — Deploy the clients: web and hmi

```bash
kubectl apply -f - <<'EOF'
apiVersion: v1
kind: Pod
metadata: { name: web, namespace: dc, labels: { app: web } }
spec:
  containers: [ { name: web, image: nicolaka/netshoot, command: ["sleep","infinity"] } ]
---
apiVersion: v1
kind: Pod
metadata: { name: hmi, namespace: ot, labels: { app: hmi } }
spec:
  containers: [ { name: hmi, image: nicolaka/netshoot, command: ["sleep","infinity"] } ]
EOF
kubectl get pods -A -o wide | grep -E "web|hmi|db|api|plc"
```

**Expected result.** All five pods `Running`; `web` and `hmi` have `curl`, `nc`, and `socat` (from `netshoot`).

**Negative test.** Use `busybox` for the clients and the `curl`-based L7 tests in Chapter 08 fail for lack of `curl`. `netshoot` has it; keep it.

**Cleanup.** Keep the workloads.

## Summary and Completion Checklist

- [ ] Namespaces `dc` and `ot` created.
- [ ] `db` (:5432), `api` (HTTP :8080), and `plc` (:502) running with services.
- [ ] `web` and `hmi` client pods running.
- [ ] Every pod carries an `app` label.
