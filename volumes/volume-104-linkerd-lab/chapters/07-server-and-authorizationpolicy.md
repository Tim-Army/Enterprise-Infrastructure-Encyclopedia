# Chapter 07: Server and AuthorizationPolicy

## Learning Objectives

- Define a `Server` for a port and understand that it flips the port to deny-by-default.
- Authorize an identity with `MeshTLSAuthentication` + `AuthorizationPolicy`.
- Confirm the lateral movement is denied.

Linkerd's policy is three small resources: a **`Server`** (a port on some pods), a **`MeshTLSAuthentication`** (a set of authorized identities), and an **`AuthorizationPolicy`** binding them. Creating a `Server` denies the port until an `AuthorizationPolicy` opens it.

## Hands-On Lab

### Lab 7.1 — Define a Server for the database (deny-by-default)

**Objective.** Declare the database's 5432 as a `Server`, which makes it reject all clients until authorized.

**Walkthrough**

```bash
kubectl apply -f - <<'EOF'
apiVersion: policy.linkerd.io/v1beta1
kind: Server
metadata: { name: db, namespace: dc }
spec:
  podSelector: { matchLabels: { app: db } }
  port: 5432
  proxyProtocol: opaque
EOF
```

**Step 2.** Confirm the port is now denied — even for the app, which you have not authorized yet:

```bash
kubectl exec -n dc deploy/web -c web -- nc -z -w2 db.dc 5432 || echo "web -> db BLOCKED (Server exists, no authz yet)"
kubectl exec -n ot deploy/hmi -c hmi -- nc -z -w2 db.dc 5432 || echo "hmi -> db BLOCKED"
```

**Expected result.** Both are BLOCKED. Declaring a `Server` for the port makes it deny-by-default; nothing reaches it until you add authorization. (`proxyProtocol: opaque` tells Linkerd 5432 is not HTTP.)

**Negative test.** Note the app is blocked too — deny-by-default denies the legitimate flow along with the attack, which is why the next step authorizes exactly the app identity.

**Rollback.** Keep the Server.

### Lab 7.2 — Authorize the app identity

**Objective.** Permit only `sa-web`'s identity to reach the database `Server`.

**Walkthrough**

```bash
kubectl apply -f - <<'EOF'
apiVersion: policy.linkerd.io/v1alpha1
kind: MeshTLSAuthentication
metadata: { name: web-identity, namespace: dc }
spec:
  identities: [ "sa-web.dc.serviceaccount.identity.linkerd.cluster.local" ]
---
apiVersion: policy.linkerd.io/v1alpha1
kind: AuthorizationPolicy
metadata: { name: db-allow-web, namespace: dc }
spec:
  targetRef: { group: policy.linkerd.io, kind: Server, name: db }
  requiredAuthenticationRefs:
    - { group: policy.linkerd.io, kind: MeshTLSAuthentication, name: web-identity }
EOF
```

**Step 2.** Validate — the app works, the operator's lateral movement stays denied:

```bash
kubectl exec -n dc deploy/web -c web -- nc -z -w2 db.dc 5432 && echo "web -> db  ALLOWED (sa-web identity)"
kubectl exec -n ot deploy/hmi -c hmi -- nc -z -w2 db.dc 5432 || echo "hmi -> db  DENIED (sa-hmi not authorized)"
```

**Expected result.** `web → db` is ALLOWED; `hmi → db` is DENIED — by **mTLS-verified identity**. The HMI is refused because it cannot present the `sa-web` identity, not because of any IP rule.

**Negative test.** Point the `MeshTLSAuthentication` at `sa-hmi...` and the operator gets in while the app is denied — you authorized the wrong identity. Revert to `sa-web`.

**Rollback.** Keep the policy.

### Lab 7.3 — Protect the API and validate end to end

**Objective.** Do the same for the API, and confirm the full segmentation.

**Walkthrough**

```bash
kubectl apply -f - <<'EOF'
apiVersion: policy.linkerd.io/v1beta1
kind: Server
metadata: { name: api, namespace: dc }
spec: { podSelector: { matchLabels: { app: api } }, port: 8080 }
---
apiVersion: policy.linkerd.io/v1alpha1
kind: AuthorizationPolicy
metadata: { name: api-allow-web, namespace: dc }
spec:
  targetRef: { group: policy.linkerd.io, kind: Server, name: api }
  requiredAuthenticationRefs:
    - { group: policy.linkerd.io, kind: MeshTLSAuthentication, name: web-identity }
EOF
kubectl exec -n dc deploy/web -c web -- curl -s -o /dev/null -w "web -> api GET /get : %{http_code}\n" http://api.dc:8080/get
kubectl exec -n ot deploy/hmi -c hmi -- curl -s -o /dev/null -w "hmi -> api (should fail): %{http_code}\n" --max-time 5 http://api.dc:8080/get || echo "hmi -> api DENIED"
```

**Expected result.**

| Flow | Basis | Before | After |
|:---|:---|:---|:---|
| web→db 5432 | identity `sa-web` | REACH | **ALLOWED** |
| hmi→db 5432 | identity `sa-hmi` | REACH | **DENIED** |
| web→api 8080 | identity `sa-web` | REACH | **ALLOWED** |
| hmi→api 8080 | identity `sa-hmi` | REACH | **DENIED** |

Every allow and deny is by mTLS-verified identity. (For per-HTTP-route authorization — allowing `GET` but not `POST` — Linkerd uses the Gateway API `HTTPRoute` with an `AuthorizationPolicy` targeting the route; that L7 refinement layers on top of this identity foundation.)

**Negative test.** Delete the `db` Server and the port returns to the namespace's default policy (allow), so `hmi → db` reaches again. The `Server` is what makes the port deny-by-default. Re-apply it.

**Rollback.** Leave the policies for Chapter 08.

## Summary and Completion Checklist

- [ ] A `Server` for the database made 5432 deny-by-default.
- [ ] `sa-web` authorized via `MeshTLSAuthentication` + `AuthorizationPolicy`; app works, operator denied.
- [ ] The API protected the same way; end-to-end table reproduced.
- [ ] The `HTTPRoute`-based L7 refinement understood.
