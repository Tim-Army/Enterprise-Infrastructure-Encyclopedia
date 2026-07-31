# Chapter 05: The Flat Mesh and Lateral Movement

## Learning Objectives

- Establish baseline reachability inside the mesh.
- Prove that Linkerd meshes traffic but does not restrict it by default.
- Frame the legitimate flows by identity.

## Hands-On Lab

### Lab 5.1 — Baseline reachability

**Objective.** Measure what talks to what. By default Linkerd secures mesh traffic with mTLS but **authorizes nothing** — every meshed connection is allowed.

**Walkthrough**

```bash
kubectl exec -n dc deploy/web -c web -- curl -s -o /dev/null -w "web -> api GET /get : %{http_code}\n" http://api.dc:8080/get
kubectl exec -n dc deploy/web -c web -- nc -z -w2 db.dc 5432 && echo "web -> db:5432 REACH"
kubectl exec -n ot deploy/hmi -c hmi -- nc -z -w2 plc.ot 502 && echo "hmi -> plc:502 REACH"
kubectl exec -n ot deploy/hmi -c hmi -- nc -z -w2 db.dc 5432 && echo "hmi -> db:5432 REACH (lateral!)"
```

**Expected result.** Everything REACHes and the API returns `200`. Meshing added encryption and identity, not restriction — segmentation is a policy you add.

**Negative test.** Assume meshing isolates workloads. It does not — until you define a `Server` and `AuthorizationPolicy`, the mesh allows all traffic (already mTLS-secured, but unrestricted).

**Cleanup.** None.

### Lab 5.2 — Identify the legitimate flows by identity

**Objective.** Write the flows by the identity that will authorize them.

**Walkthrough**

| # | Source identity | Destination | Allowed? |
|:--|:--|:--|:--|
| 1 | `sa-web` (dc) | db :5432 | **Yes** |
| 2 | `sa-web` (dc) | api :8080 | **Yes** |
| 3 | `sa-hmi` (ot) | plc :502 (un-meshed) | **Yes** |
| 4 | `sa-hmi` (ot) | db :5432 | **No** (lateral movement) |

**Expected result.** Flows expressed by identity (`sa-web.dc.serviceaccount.identity.linkerd.cluster.local`, etc.). Because mTLS is already on, these identities are cryptographically verified on every connection — the authorization you add in Chapter 07 rests on that.

**Negative test.** Express flow 4's denial by pod IP; pod IPs churn and, in a mesh, are not the trust anchor. Use identities.

**Cleanup.** None.

### Lab 5.3 — Reproduce lateral movement

**Objective.** Show the compromised operator reaching the database.

**Walkthrough**

```bash
kubectl exec -n ot deploy/hmi -c hmi -- nc -z -w2 db.dc 5432 && echo "hmi reached the database (lateral)"
```

**Expected result.** The operator reaches the database over the (already mTLS-secured) mesh — encrypted, but unauthorized and unstopped, because no policy exists.

**Negative test.** Re-run the legitimate `web → db`; it works too. mTLS proves *who* each party is but does not decide *whether* they may talk — that is what `AuthorizationPolicy` adds.

**Cleanup.** None — Chapter 06 confirms the automatic mTLS, Chapter 07 adds authorization.

## Summary and Completion Checklist

- [ ] Baseline shows all flows REACH; Linkerd authorizes nothing by default.
- [ ] The legitimate flows written by identity.
- [ ] Lateral movement (hmi→db) reproduced.
- [ ] You can state the goal: keep the automatic mTLS, then authorize flows 1–3 by identity and deny 4.
