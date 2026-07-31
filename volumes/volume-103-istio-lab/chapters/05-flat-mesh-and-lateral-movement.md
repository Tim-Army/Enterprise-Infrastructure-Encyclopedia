# Chapter 05: The Flat Mesh and Lateral Movement

## Learning Objectives

- Establish baseline reachability inside the mesh.
- Prove that Istio's default posture is permissive — a mesh is not a firewall until you make it one.
- Frame the legitimate flows by identity (principal).

## Hands-On Lab

### Lab 5.1 — Baseline reachability

**Objective.** Measure what talks to what. By default, Istio installs in **permissive** mode — it enables mTLS where both sides support it but does not *require* it, and it authorizes nothing by default (all traffic is allowed).

**Walkthrough**

**Step 1.** From `web` (mesh) probe api, db, and the un-meshed plc:

```bash
kubectl exec -n dc deploy/web -c web -- curl -s -o /dev/null -w "web -> api GET /get : %{http_code}\n" http://api.dc:8080/get
kubectl exec -n dc deploy/web -c web -- nc -z -w2 db.dc 5432 && echo "web -> db:5432 REACH"
```

**Step 2.** From `hmi` (mesh) probe plc and — the lateral path — db:

```bash
kubectl exec -n ot deploy/hmi -c hmi -- nc -z -w2 plc.ot 502 && echo "hmi -> plc:502 REACH"
kubectl exec -n ot deploy/hmi -c hmi -- nc -z -w2 db.dc 5432 && echo "hmi -> db:5432 REACH (lateral!)"
```

**Expected result.** Everything REACHes and the API returns `200`. Being *in the mesh* changes nothing about who may talk to whom — Istio ships permissive so that adding the mesh does not break existing traffic. Segmentation is a policy you add.

**Negative test.** Assume the mesh isolates workloads by default. It does not — a mesh with no `AuthorizationPolicy` allows all service-to-service traffic. Adding Istio without policy buys you mTLS-capable transport and observability, not segmentation.

**Cleanup.** None.

### Lab 5.2 — Identify the legitimate flows by principal

**Objective.** Write the flows in terms of the **identity** (ServiceAccount → SPIFFE principal) that will authorize them.

**Walkthrough**

| # | Source principal | Destination | Layer | Allowed? |
|:--|:--|:--|:--|:--|
| 1 | `sa-web` (dc) | api :8080 `GET /get` | L7 | **Yes** |
| 2 | `sa-web` (dc) | db :5432 | L4 | **Yes** |
| 3 | `sa-hmi` (ot) | plc :502 (un-meshed) | egress | **Yes** |
| 4 | `sa-hmi` (ot) | db :5432 | L4 | **No** (lateral movement) |
| 5 | `sa-web` (dc) | api `POST /post` | L7 | **No** (read-only) |

**Expected result.** Flows expressed by **authenticated principal** (`spiffe://cluster.local/ns/dc/sa/sa-web`, etc.), not by IP. This is what makes Istio authorization hard to spoof: the source must hold the identity's certificate.

**Negative test.** Try to express flow 4's denial by source IP. In a mesh, the sidecar re-originates traffic, and identity — not IP — is the reliable discriminator. Use principals.

**Cleanup.** None.

### Lab 5.3 — Reproduce lateral movement

**Objective.** Show the compromised operator reaching the database, and the read-only client abusing the API's write path.

**Walkthrough**

```bash
kubectl exec -n ot deploy/hmi -c hmi -- nc -z -w2 db.dc 5432 && echo "hmi reached the database (lateral)"
kubectl exec -n dc deploy/web -c web -- curl -s -o /dev/null -w "web POST /post abused: %{http_code}\n" -X POST http://api.dc:8080/post
```

**Expected result.** The operator reaches the database and the read-only web client POSTs successfully — both unstopped, because no policy exists yet.

**Negative test.** Re-run the legitimate `web → api GET /get`; it works too. Until Istio has an mTLS-verified identity *and* an AuthorizationPolicy, the mesh cannot tell the operator from the app, or a read from a write.

**Cleanup.** None — Chapter 06 turns on mTLS and identity, Chapter 07 authorization.

## Summary and Completion Checklist

- [ ] Baseline shows all flows REACH; Istio is permissive by default.
- [ ] The legitimate flows written by principal (ServiceAccount identity).
- [ ] Lateral movement (hmi→db) and API write abuse (web POST) reproduced.
- [ ] You can state the goal: require mTLS, then authorize flows 1–3 by principal and deny 4–5.
