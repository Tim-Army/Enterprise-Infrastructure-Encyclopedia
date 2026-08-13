# Chapter 08: L7-Aware Policy

## Learning Objectives

- Enforce Layer 7 **HTTP** policy: which methods and paths a client may use.
- Enforce **DNS/FQDN** egress: which names a workload may reach.
- Observe Layer 7 verdicts in Hubble.

This is where Cilium goes beyond every Layer 3/4 tool in this series. A 5-tuple firewall cannot tell `GET /get` from `POST /post`, or `example.com` from `evil.example`. Cilium can, because its eBPF dataplane can redirect selected traffic through an in-kernel L7 proxy.

## Hands-On Lab

### Lab 8.1 — Restrict the API to specific HTTP methods and paths

**Objective.** Allow the read-only web client to call only `GET /get` on the API; deny `POST /post` and every other path — at Layer 7.

**Walkthrough**

**Step 1.** Apply an L7 HTTP policy:

```bash
kubectl apply -f - <<'EOF'
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata: { name: web-to-api-l7, namespace: dc }
spec:
  endpointSelector: { matchLabels: { app: api } }
  ingress:
    - fromEndpoints: [ { matchLabels: { app: web } } ]
      toPorts:
        - ports: [ { port: "8080", protocol: TCP } ]
          rules:
            http:
              - { method: "GET", path: "/get" }
EOF
```

**Step 2.** Validate: the allowed call succeeds; the forbidden method and path are denied *by Cilium's L7 proxy* with a `403`:

```bash
kubectl exec -n dc web -- curl -s -o /dev/null -w "GET /get   : %{http_code}\n"  http://api.dc:8080/get
kubectl exec -n dc web -- curl -s -o /dev/null -w "POST /post : %{http_code}\n" -X POST http://api.dc:8080/post
kubectl exec -n dc web -- curl -s -o /dev/null -w "GET /admin : %{http_code}\n"  http://api.dc:8080/admin
hubble observe --to-pod dc/api --protocol http | tail -5
```

**Expected result.** `GET /get` returns `200`; `POST /post` and `GET /admin` return `403` — denied at Layer 7, not Layer 4. Hubble shows each HTTP request with its method, path, and verdict. The API write-abuse from Chapter 05 is now impossible even though the TCP connection to `:8080` is permitted.

**Negative test.** Delete the L7 policy and re-run the POST; it returns `200` again. Only the L7 rule distinguishes the read from the write — no L3/L4 control can. Re-apply it.

**Rollback.** Keep the L7 policy.

### Lab 8.2 — Restrict egress by DNS name (FQDN policy)

**Objective.** Allow the web client to reach only a named external destination, and deny all other egress — enforced on the **DNS name**, not an IP.

**Walkthrough**

**Step 1.** Apply an egress policy that permits DNS resolution and then only `example.com:443`:

```bash
kubectl apply -f - <<'EOF'
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata: { name: web-egress-fqdn, namespace: dc }
spec:
  endpointSelector: { matchLabels: { app: web } }
  egress:
    - toEndpoints:
        - matchLabels:
            k8s:io.kubernetes.pod.namespace: kube-system
            k8s:k8s-app: kube-dns
      toPorts:
        - ports: [ { port: "53", protocol: ANY } ]
          rules:
            dns: [ { matchPattern: "*" } ]
    - toFQDNs: [ { matchName: "example.com" } ]
      toPorts: [ { ports: [ { port: "443", protocol: TCP } ] } ]
EOF
```

**Step 2.** Validate: the allowed name works; another name is denied (Cilium learns the IP from the DNS reply it proxied and only permits that name's addresses):

```bash
kubectl exec -n dc web -- curl -s -o /dev/null -w "example.com : %{http_code}\n" --max-time 8 https://example.com
kubectl exec -n dc web -- curl -s -o /dev/null -w "cloudflare  : %{http_code}\n" --max-time 8 https://www.cloudflare.com || echo "other FQDN DENIED"
```

**Expected result.** `example.com` succeeds (a 2xx/3xx code); the other name is denied. Egress is now governed by *name*, which is how you allow "our payment provider" without hard-coding a fragile list of IPs.

> **Note.** FQDN policy depends on Cilium proxying the pod's DNS, which the first `toEndpoints` DNS rule enables. Without allowing DNS, the pod cannot resolve anything and even the allowed name fails.

**Negative test.** Remove the DNS `toEndpoints` rule; now even `example.com` fails, because the pod cannot resolve it. DNS visibility is the prerequisite for name-based egress. Restore it.

**Rollback.** Keep the egress policy, or delete it if you have no outbound internet from the pod.

### Lab 8.3 — Validate the whole segmentation

**Objective.** Confirm the end state across L4 and L7.

**Walkthrough**

```bash
kubectl exec -n dc web -- nc -z -w2 db.dc 5432 && echo "web -> db  L4 ALLOWED"
kubectl exec -n ot hmi -- nc -z -w2 plc.ot 502 && echo "hmi -> plc L4 ALLOWED"
kubectl exec -n ot hmi -- nc -z -w2 db.dc 5432 || echo "hmi -> db  L4 BLOCKED"
kubectl exec -n dc web -- curl -s -o /dev/null -w "GET /get 200? %{http_code}\n"  http://api.dc:8080/get
kubectl exec -n dc web -- curl -s -o /dev/null -w "POST /post 403? %{http_code}\n" -X POST http://api.dc:8080/post
```

**Expected result.**

| Flow | Layer | Before | After |
|:---|:---|:---|:---|
| web→db 5432 | L4 | REACH | **ALLOWED** |
| hmi→plc 502 | L4 | REACH | **ALLOWED** |
| hmi→db 5432 | L4 | REACH | **BLOCKED** |
| web→api GET /get | L7 | 200 | **200 (allowed)** |
| web→api POST /post | L7 | 200 | **403 (denied)** |

Both L4 flows are correct; the API is restricted to a single method and path at Layer 7; egress is governed by name — none of which a Layer 3/4-only tool could express.

**Negative test.** Remove every policy and re-run; the cluster returns to flat and the POST abuse returns. Cilium enforces only what you declare. Re-apply.

**Rollback.** Leave the policies for Chapter 09.

## Summary and Completion Checklist

- [ ] The API restricted to `GET /get` at Layer 7; `POST`/other paths return 403.
- [ ] Egress restricted by DNS name with an FQDN policy.
- [ ] L7 verdicts observed in Hubble.
- [ ] End-to-end validation table (L4 + L7) reproduced.
