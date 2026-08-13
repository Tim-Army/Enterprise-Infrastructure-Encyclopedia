# Chapter 05: The Flat Cluster and Lateral Movement

## Learning Objectives

- Establish baseline reachability, including HTTP methods on the API.
- Prove the default cluster is flat.
- Frame the legitimate flows — including the one Layer 7 constraint.

## Hands-On Lab

### Lab 5.1 — Baseline reachability

**Objective.** Measure what talks to what before policy — and note that at Layer 7, *every* HTTP method is currently allowed.

**Walkthrough**

**Step 1.** L3/L4 probes from `web` and `hmi`:

```bash
kubectl exec -n dc web -- nc -z -w2 db.dc 5432   && echo "web -> db:5432 REACH"
kubectl exec -n ot hmi -- nc -z -w2 plc.ot 502   && echo "hmi -> plc:502 REACH"
kubectl exec -n ot hmi -- nc -z -w2 db.dc 5432   && echo "hmi -> db:5432 REACH (lateral!)"
```

**Step 2.** L7 probes to the API — both a benign GET and a sensitive POST currently succeed:

```bash
kubectl exec -n dc web -- curl -s -o /dev/null -w "web -> api GET /get  : %{http_code}\n"  http://api.dc:8080/get
kubectl exec -n dc web -- curl -s -o /dev/null -w "web -> api POST /post: %{http_code}\n" -X POST http://api.dc:8080/post
```

**Expected result.** All L3/L4 probes REACH; both HTTP calls return `200`. The cluster is flat at Layer 3/4 *and* unrestricted at Layer 7 — any method, any path.

**Negative test.** There is nothing blocked to find, at any layer. That includes the sensitive `POST /post`, which no Layer 3/4 control could ever distinguish from the benign `GET /get` — they are the same 5-tuple. Only L7 policy can tell them apart.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.2 — Identify the legitimate flows

**Objective.** Write down the flows the application needs, including the L7 constraint on the API.

**Walkthrough**

| # | Source | Destination | Layer | Allowed? |
|:--|:--|:--|:--|:--|
| 1 | web (`app=web`) | db (`app=db`) :5432 | L4 | **Yes** |
| 2 | hmi (`app=hmi`) | plc (`app=plc`) :502 | L4 | **Yes** |
| 3 | web (`app=web`) | api (`app=api`) `GET /get` | L7 | **Yes** |
| 4 | web (`app=web`) | api (`app=api`) `POST /post` | L7 | **No** (read-only client) |
| 5 | hmi (`app=hmi`) | db (`app=db`) :5432 | L4 | **No** (lateral movement) |

**Expected result.** Two L4 allows, one L7 allow, and two denies — one of which (`POST /post`) is expressible *only* at Layer 7.

**Negative test.** Try to write rule 4 as an L3/L4 firewall rule. You cannot — `GET /get` and `POST /post` are identical at L4. This is the gap Cilium L7 policy fills.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.3 — Reproduce lateral movement

**Objective.** Show the compromised operator reaching the database, and abusing the API's write path.

**Walkthrough**

```bash
# lateral movement to the database:
kubectl exec -n ot hmi -- nc -z -w2 db.dc 5432 && echo "hmi reached the database (lateral)"
# API write abuse from the app tier (a read-only client should never POST):
kubectl exec -n dc web -- curl -s -o /dev/null -w "web POST /post abused: %{http_code}\n" -X POST http://api.dc:8080/post
```

**Expected result.** The operator reaches the database, and the read-only web client successfully POSTs to the API — two different attacks, one at L4 and one at L7, both currently unstopped.

**Negative test.** Re-run the legitimate `web → api GET /get`; it works too. The cluster cannot yet distinguish a read from a write, or the app from the operator, until Cilium policy gives it identity and L7 awareness.

**Rollback.** None — Chapter 06 begins visibility, Chapters 07–08 enforcement.

## Summary and Completion Checklist

- [ ] Baseline shows all L4 probes REACH and both HTTP methods returning 200.
- [ ] The legitimate flows written down, including the L7-only constraint.
- [ ] Lateral movement (hmi→db) and API write abuse (web POST) reproduced.
- [ ] You can state the goal: allow flows 1–3 by identity and L7, deny 4 and 5.
