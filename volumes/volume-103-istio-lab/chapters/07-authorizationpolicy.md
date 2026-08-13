# Chapter 07: AuthorizationPolicy

## Learning Objectives

- Establish default-deny for the meshed workloads.
- Allow a flow by authenticated **principal** at Layer 4.
- Allow a flow by principal and Layer 7 (HTTP method and path).
- Confirm the lateral movement and the API write abuse are denied.

With mTLS establishing identity (Chapter 06), you can now authorize on that identity. Istio's `AuthorizationPolicy` denies by default once any ALLOW policy selects a workload, so these rules both permit the legitimate flow and deny the rest.

## Hands-On Lab

### Lab 7.1 — Allow only the app tier to reach the database (L4, by principal)

**Objective.** Permit only `sa-web` to reach `db:5432`; deny every other principal — including the operator.

**Walkthrough**

```bash
kubectl apply -f - <<'EOF'
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata: { name: allow-web-to-db, namespace: dc }
spec:
  selector: { matchLabels: { app: db } }
  action: ALLOW
  rules:
    - from: [ { source: { principals: [ "cluster.local/ns/dc/sa/sa-web" ] } } ]
      to:   [ { operation: { ports: [ "5432" ] } } ]
EOF
```

**Step 2.** Validate — the app works; the operator's lateral movement is denied by identity:

```bash
kubectl exec -n dc deploy/web -c web -- nc -z -w2 db.dc 5432 && echo "web -> db  ALLOWED (sa-web)"
kubectl exec -n ot deploy/hmi -c hmi -- nc -z -w2 db.dc 5432 || echo "hmi -> db  DENIED (sa-hmi not authorized)"
```

**Expected result.** `web → db` is ALLOWED; `hmi → db` is DENIED. The denial is by **principal** — the HMI is refused because it does not hold the `sa-web` identity, not because of any IP rule. Applying this ALLOW policy also made `db` default-deny for every unlisted source.

**Negative test.** Change the principal to `cluster.local/ns/ot/sa/sa-hmi` and the operator gets in while the app is denied — you authorized the wrong identity. Principals are exact; get them right. Revert to `sa-web`.

**Rollback.** Keep the policy.

### Lab 7.2 — Restrict the API to a method and path (L7, by principal)

**Objective.** Allow `sa-web` to call only `GET /get` on the API; deny `POST /post` and other paths — at Layer 7.

**Walkthrough**

```bash
kubectl apply -f - <<'EOF'
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata: { name: allow-web-to-api-l7, namespace: dc }
spec:
  selector: { matchLabels: { app: api } }
  action: ALLOW
  rules:
    - from: [ { source: { principals: [ "cluster.local/ns/dc/sa/sa-web" ] } } ]
      to:   [ { operation: { methods: [ "GET" ], paths: [ "/get" ] } } ]
EOF
```

**Step 2.** Validate the L7 authorization:

```bash
kubectl exec -n dc deploy/web -c web -- curl -s -o /dev/null -w "GET /get   : %{http_code}\n"  http://api.dc:8080/get
kubectl exec -n dc deploy/web -c web -- curl -s -o /dev/null -w "POST /post : %{http_code}\n" -X POST http://api.dc:8080/post
kubectl exec -n dc deploy/web -c web -- curl -s -o /dev/null -w "GET /admin : %{http_code}\n"  http://api.dc:8080/admin
```

**Expected result.** `GET /get` returns `200`; `POST /post` and `GET /admin` return `403` — the sidecar's L7 authorization denies them even though the caller holds a valid identity and the TCP connection is permitted. Identity *and* Layer 7: the caller must be `sa-web` **and** make an allowed request.

**Negative test.** Delete this policy and re-run the POST; it returns `200`. Only the L7 rule distinguishes the read from the write; the L4 policy from Lab 7.1 cannot. Re-apply it.

**Rollback.** Keep the policy.

### Lab 7.3 — Validate the mesh segmentation end to end

**Objective.** Confirm the end state across identity and Layer 7.

**Walkthrough**

```bash
kubectl exec -n dc deploy/web -c web -- nc -z -w2 db.dc 5432 && echo "web -> db  ALLOWED"
kubectl exec -n ot deploy/hmi -c hmi -- nc -z -w2 db.dc 5432 || echo "hmi -> db  DENIED"
kubectl exec -n dc deploy/web -c web -- curl -s -o /dev/null -w "GET /get 200? %{http_code}\n"  http://api.dc:8080/get
kubectl exec -n dc deploy/web -c web -- curl -s -o /dev/null -w "POST /post 403? %{http_code}\n" -X POST http://api.dc:8080/post
```

**Expected result.**

| Flow | Basis | Before | After |
|:---|:---|:---|:---|
| web→db 5432 | principal `sa-web` | REACH | **ALLOWED** |
| hmi→db 5432 | principal `sa-hmi` | REACH | **DENIED** |
| web→api GET /get | principal + L7 | 200 | **200** |
| web→api POST /post | principal + L7 | 200 | **403** |

Every allow and deny is by cryptographically-authenticated identity — the strongest discriminator in this series — and the API is constrained at Layer 7.

**Negative test.** Remove all AuthorizationPolicies and the mesh returns to permissive (all allowed). Istio authorizes only what you declare; mTLS alone encrypts but does not segment.

**Rollback.** Leave the policies for Chapter 08.

## Summary and Completion Checklist

- [ ] `db` reachable only by `sa-web`; `hmi` denied by principal.
- [ ] `api` restricted to `GET /get` at Layer 7 for `sa-web`; POST/other return 403.
- [ ] End-to-end validation table reproduced.
- [ ] You can explain why principal-based authorization is harder to spoof than IP or label.
