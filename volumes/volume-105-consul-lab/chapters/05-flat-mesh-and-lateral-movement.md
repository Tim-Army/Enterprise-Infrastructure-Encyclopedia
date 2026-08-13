# Chapter 05: The Flat Mesh and Lateral Movement

## Learning Objectives

- Establish baseline reachability inside the mesh.
- Prove that Consul allows service-to-service traffic until intentions deny it.
- Frame the legitimate flows as intentions.

## Hands-On Lab

### Lab 5.1 — Baseline reachability

**Objective.** Measure what talks to what. With Connect's mTLS in place but no restrictive intentions, services can still reach each other.

**Walkthrough**

```bash
kubectl exec deploy/web -c web -- curl -s -o /dev/null -w "web -> api GET /get : %{http_code}\n" http://api:8080/get
kubectl exec deploy/web -c web -- nc -z -w2 db 5432 && echo "web -> db:5432 REACH"
kubectl exec deploy/hmi -c hmi -- nc -z -w2 db 5432 && echo "hmi -> db:5432 REACH (lateral!)"
```

**Expected result.** Everything REACHes and the API returns `200`. The mesh secured the transport with mTLS, but authorization comes from **intentions**, which you have not written yet — so, depending on the mesh's default intention policy, service-to-service traffic is permitted.

**Negative test.** Assume Connect's mTLS blocks the operator. It does not — mTLS authenticates identity; **intentions** decide who may talk. Encryption is not authorization.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.2 — Identify the legitimate flows as intentions

**Objective.** Write the flows as Consul intentions — source service, destination service, allow.

**Walkthrough**

| # | Source service | Destination service | Intention |
|:--|:--|:--|:--|
| 1 | web | db | **allow** |
| 2 | web | api | **allow** |
| 3 | hmi | db | **deny** (lateral movement) |
| 4 | *(everything else)* | any | **deny** (default) |

**Expected result.** A short intention list — the whole segmentation, expressed as "who may call whom" by service name. The same list would govern these services whether they run on Kubernetes or a VM.

**Negative test.** Express intention 3 by pod IP. Consul intentions are between service *identities*, which is what makes them portable across platforms and stable across restarts. Use service names.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.3 — Reproduce lateral movement

**Objective.** Show the compromised operator reaching the database.

**Walkthrough**

```bash
kubectl exec deploy/hmi -c hmi -- nc -z -w2 db 5432 && echo "hmi reached the database (lateral)"
```

**Expected result.** The operator reaches the database over the (mTLS-secured) mesh — encrypted, but unauthorized, because no intention denies it yet.

**Negative test.** Re-run the legitimate `web → db`; it works too. Until intentions exist, Consul does not distinguish the app from the operator; the encryption is identical for both.

**Rollback.** None — Chapter 06 confirms mTLS, Chapter 07 writes the intentions.

## Summary and Completion Checklist

- [ ] Baseline shows all flows REACH; intentions not yet written.
- [ ] The legitimate flows written as intentions (by service name).
- [ ] Lateral movement (hmi→db) reproduced.
- [ ] You can state the goal: default-deny intentions, allow web→db and web→api, deny hmi→db.
