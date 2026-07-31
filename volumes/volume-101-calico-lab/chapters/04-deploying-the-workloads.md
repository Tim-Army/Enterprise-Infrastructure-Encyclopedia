# Chapter 04: Deploying the Workloads

## Learning Objectives

- Create the two namespaces and the four labeled workloads.
- Expose the database and the PLC as services.
- Confirm every workload is running before you test connectivity.

The estate is four pods across two namespaces, each carrying an `app` label that policy will select on: `web` and `db` in namespace `dc`, `hmi` and `plc` in namespace `ot`.

## Hands-On Lab

### Lab 4.1 — Create namespaces

**Objective.** Create the `dc` (data center) and `ot` namespaces.

**Walkthrough**

```bash
kubectl create namespace dc
kubectl create namespace ot
kubectl get ns dc ot
```

**Expected result.** Both namespaces exist and are `Active`.

**Negative test.** Deploy a pod into the `default` namespace by forgetting `-n`; later namespace-scoped policy will not select it. Keep workloads in `dc`/`ot`.

**Cleanup.** None.

### Lab 4.2 — Deploy the database and the PLC (the services)

**Objective.** Stand up the two things other workloads connect to: PostgreSQL on 5432 and a Modbus listener on 502.

**Walkthrough**

**Step 1.** The database in `dc`:

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
            - { name: POSTGRES_DB, value: "cwlab" }
          ports: [ { containerPort: 5432 } ]
---
apiVersion: v1
kind: Service
metadata: { name: db, namespace: dc }
spec:
  selector: { app: db }
  ports: [ { port: 5432, targetPort: 5432 } ]
EOF
```

**Step 2.** The PLC in `ot` (a Modbus-port listener built from `netshoot`'s `socat`):

```bash
kubectl apply -f - <<'EOF'
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
spec:
  selector: { app: plc }
  ports: [ { port: 502, targetPort: 502 } ]
EOF
```

**Expected result.** `kubectl get pods -n dc` and `-n ot` show `db` and `plc` becoming `Running`.

**Negative test.** Omit the `POSTGRES_PASSWORD` env and the postgres pod crash-loops; check `kubectl logs -n dc deploy/db`. Set the password.

**Cleanup.** None.

### Lab 4.3 — Deploy the clients (web and hmi)

**Objective.** Stand up the two client workloads that initiate flows: the app tier (`web`) and the operator (`hmi`).

**Walkthrough**

```bash
kubectl apply -f - <<'EOF'
apiVersion: v1
kind: Pod
metadata: { name: web, namespace: dc, labels: { app: web } }
spec:
  containers:
    - { name: web, image: nicolaka/netshoot, command: ["sleep","infinity"] }
---
apiVersion: v1
kind: Pod
metadata: { name: hmi, namespace: ot, labels: { app: hmi } }
spec:
  containers:
    - { name: hmi, image: nicolaka/netshoot, command: ["sleep","infinity"] }
EOF
kubectl get pods -A -o wide | grep -E "web|hmi|db|plc"
```

**Expected result.** All four pods `Running`, each with a pod IP from `192.168.0.0/16`.

**Negative test.** Use an image without network tools (say `busybox`) for the clients and the `nc`-based tests in Chapter 05 fail for lack of tooling, not for lack of connectivity. `netshoot` has the tools; keep it.

**Cleanup.** Keep the workloads; Chapter 05 attacks them.

## Summary and Completion Checklist

- [ ] Namespaces `dc` and `ot` created.
- [ ] `db` (PostgreSQL :5432) and `plc` (:502) running with services.
- [ ] `web` and `hmi` client pods running.
- [ ] Every pod has an `app` label for policy to select on.
