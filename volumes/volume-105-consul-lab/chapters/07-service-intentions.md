# Chapter 07: Service Intentions

## Learning Objectives

- Establish default-deny with a wildcard intention.
- Allow specific service-to-service flows.
- Confirm the lateral movement is denied, and reason about L7 intentions.

Intentions are Consul's authorization primitive: "source service may (or may not) reach destination service." More-specific intentions beat wildcards, so a default-deny plus exact allows gives least privilege.

## Hands-On Lab

### Lab 7.1 — Default-deny with a wildcard intention

**Objective.** Deny all service-to-service traffic unless explicitly allowed.

**Walkthrough**

```bash
kubectl apply -f - <<'EOF'
apiVersion: consul.hashicorp.com/v1alpha1
kind: ServiceIntentions
metadata: { name: deny-all }
spec:
  destination: { name: "*" }
  sources:
    - { name: "*", action: deny }
EOF
```

**Step 2.** Confirm even the app is now denied (nothing is allowed yet):

```bash
kubectl exec deploy/web -c web -- nc -z -w2 db 5432 || echo "web -> db BLOCKED (default-deny)"
kubectl exec deploy/hmi -c hmi -- nc -z -w2 db 5432 || echo "hmi -> db BLOCKED"
```

**Expected result.** Both BLOCKED. A wildcard `* -> * deny` makes the mesh default-deny; you now add back exactly the flows the app needs.

**Negative test.** The app is blocked too — default-deny denies the legitimate flow along with the attack, which is why the next step allows exactly `web → db` and nothing more.

**Cleanup.** Keep the deny-all.

### Lab 7.2 — Allow the legitimate flows

**Objective.** Permit `web → db` and `web → api`; the more-specific intentions override the wildcard deny.

**Walkthrough**

```bash
kubectl apply -f - <<'EOF'
apiVersion: consul.hashicorp.com/v1alpha1
kind: ServiceIntentions
metadata: { name: db }
spec:
  destination: { name: db }
  sources:
    - { name: web, action: allow }
---
apiVersion: consul.hashicorp.com/v1alpha1
kind: ServiceIntentions
metadata: { name: api }
spec:
  destination: { name: api }
  sources:
    - { name: web, action: allow }
EOF
```

**Step 2.** Validate — the app works, the operator's lateral movement stays denied:

```bash
kubectl exec deploy/web -c web -- nc -z -w2 db 5432 && echo "web -> db  ALLOWED"
kubectl exec deploy/web -c web -- curl -s -o /dev/null -w "web -> api : %{http_code}\n" http://api:8080/get
kubectl exec deploy/hmi -c hmi -- nc -z -w2 db 5432 || echo "hmi -> db  DENIED (no intention allows hmi->db)"
```

**Expected result.** `web → db` and `web → api` ALLOWED; `hmi → db` DENIED. The exact `web → db allow` beats the `* -> * deny`; `hmi → db` has no allowing intention, so the wildcard deny governs it. Segmentation is a readable list of service-to-service permissions.

**Negative test.** Add `{ name: hmi, action: allow }` to the `db` intention and the operator gets in. Intentions are the whole control; add only the ones a real dependency needs. Remove it.

**Cleanup.** Keep the intentions.

### Lab 7.3 — Layer 7 intentions (Design Exercise + apply)

**Objective.** Restrict `web → api` to specific HTTP methods/paths using an L7 intention.

**Walkthrough**

**Step 1.** L7 intentions require the destination's protocol to be `http`. Set it, then write a permission-based intention:

```bash
kubectl apply -f - <<'EOF'
apiVersion: consul.hashicorp.com/v1alpha1
kind: ServiceDefaults
metadata: { name: api }
spec: { protocol: http }
---
apiVersion: consul.hashicorp.com/v1alpha1
kind: ServiceIntentions
metadata: { name: api }
spec:
  destination: { name: api }
  sources:
    - name: web
      permissions:
        - action: allow
          http: { pathExact: "/get", methods: [ "GET" ] }
EOF
```

**Step 2.** Validate the L7 restriction:

```bash
kubectl exec deploy/web -c web -- curl -s -o /dev/null -w "GET /get   : %{http_code}\n"  http://api:8080/get
kubectl exec deploy/web -c web -- curl -s -o /dev/null -w "POST /post : %{http_code}\n" -X POST http://api:8080/post
```

**Expected result.** `GET /get` returns `200`; `POST /post` returns `403` — denied at Layer 7 by the intention's `permissions`. Consul, like Cilium and Istio, can authorize by HTTP method and path, not just by service.

**Negative test.** Remove the `ServiceDefaults protocol: http` and the L7 permissions are ignored (the intention falls back to L4 allow/deny), so the POST succeeds. L7 intentions need the protocol declared.

**Cleanup.** Keep the intentions.

## Summary and Completion Checklist

- [ ] A `* -> * deny` intention made the mesh default-deny.
- [ ] `web → db` and `web → api` allowed; `hmi → db` denied.
- [ ] An L7 intention restricted `web → api` to `GET /get`; POST returns 403.
- [ ] You can explain intention precedence (specific beats wildcard).
