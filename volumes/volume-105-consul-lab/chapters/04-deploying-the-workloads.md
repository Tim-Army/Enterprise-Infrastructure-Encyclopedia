# Chapter 04: Deploying the Workloads

## Learning Objectives

- Opt workloads into the Consul mesh with the connect-inject annotation.
- Deploy the meshed services and leave the PLC un-meshed.
- Confirm each meshed pod has a Consul sidecar.

Consul derives a service's identity from its name and ServiceAccount, and intentions are written between **service names**. Each workload gets its own name and ServiceAccount.

## Hands-On Lab

### Lab 4.1 — Deploy the meshed services

**Objective.** Deploy `db`, `api`, `web`, and `hmi`, each opted into Consul Connect.

**Walkthrough**

```bash
for sa in web api db hmi; do kubectl create serviceaccount $sa; done
kubectl apply -f - <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata: { name: db, labels: { app: db } }
spec:
  replicas: 1
  selector: { matchLabels: { app: db } }
  template:
    metadata:
      labels: { app: db }
      annotations: { "consul.hashicorp.com/connect-inject": "true" }
    spec:
      serviceAccountName: db
      containers:
        - name: db
          image: postgres:16
          env: [ { name: POSTGRES_PASSWORD, value: "LabAppPassw0rd!" }, { name: POSTGRES_DB, value: "consullab" } ]
          ports: [ { containerPort: 5432 } ]
---
apiVersion: v1
kind: Service
metadata: { name: db }
spec: { selector: { app: db }, ports: [ { port: 5432, targetPort: 5432 } ] }
---
apiVersion: apps/v1
kind: Deployment
metadata: { name: api, labels: { app: api } }
spec:
  replicas: 1
  selector: { matchLabels: { app: api } }
  template:
    metadata:
      labels: { app: api }
      annotations: { "consul.hashicorp.com/connect-inject": "true" }
    spec:
      serviceAccountName: api
      containers: [ { name: api, image: mccutchen/go-httpbin:v2.15.0, args: ["-port","8080"], ports: [ { containerPort: 8080 } ] } ]
---
apiVersion: v1
kind: Service
metadata: { name: api }
spec: { selector: { app: api }, ports: [ { port: 8080, targetPort: 8080 } ] }
---
apiVersion: apps/v1
kind: Deployment
metadata: { name: web, labels: { app: web } }
spec:
  replicas: 1
  selector: { matchLabels: { app: web } }
  template:
    metadata:
      labels: { app: web }
      annotations: { "consul.hashicorp.com/connect-inject": "true" }
    spec:
      serviceAccountName: web
      containers: [ { name: web, image: nicolaka/netshoot, command: ["sleep","infinity"] } ]
---
apiVersion: apps/v1
kind: Deployment
metadata: { name: hmi, labels: { app: hmi } }
spec:
  replicas: 1
  selector: { matchLabels: { app: hmi } }
  template:
    metadata:
      labels: { app: hmi }
      annotations: { "consul.hashicorp.com/connect-inject": "true" }
    spec:
      serviceAccountName: hmi
      containers: [ { name: hmi, image: nicolaka/netshoot, command: ["sleep","infinity"] } ]
EOF
```

**Expected result.** Each pod shows an extra `consul-dataplane` sidecar container (2/2 or more), and the services appear in the Consul catalog (`consul catalog services` via a port-forwarded, token-authenticated CLI, or the UI).

**Negative test.** Omit the `connect-inject` annotation and the pod runs without a sidecar — it is not in the mesh, so intentions do not apply to it. Add the annotation and restart.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.2 — Deploy the un-meshed PLC

**Objective.** Deploy the PLC without connect-inject, modeling a device that cannot join the mesh.

**Walkthrough**

```bash
kubectl apply -f - <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata: { name: plc, labels: { app: plc } }
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
metadata: { name: plc }
spec: { selector: { app: plc }, ports: [ { port: 502, targetPort: 502 } ] }
EOF
kubectl get pods
```

**Expected result.** The app services show their Consul sidecar; `plc` runs `1/1` with no sidecar — un-meshed.

**Negative test.** Add the connect-inject annotation to the PLC and it joins the mesh — but a real PLC could not run a dataplane. Omitting the annotation models that.

**Rollback.** Keep the workloads.

## Summary and Completion Checklist

- [ ] `web`, `api`, `db`, `hmi` meshed via connect-inject, each with its own ServiceAccount.
- [ ] The services appear in the Consul catalog.
- [ ] `plc` un-meshed (no sidecar).
