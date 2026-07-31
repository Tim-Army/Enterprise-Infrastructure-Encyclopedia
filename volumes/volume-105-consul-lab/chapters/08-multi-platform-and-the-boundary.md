# Chapter 08: Multi-Platform Reach and the Boundary

## Learning Objectives

- Understand Consul's defining capability: one mesh across Kubernetes and VMs.
- See how a non-Kubernetes service joins the mesh under the same intentions.
- Recognize the un-meshed PLC boundary and pair the mesh with a network policy.

## Consul's signature: one mesh, many platforms

Istio and Linkerd secured Kubernetes pods. Consul secures **services**, wherever they run. A service on a VM runs a Consul dataplane, registers into the same catalog, receives a SPIFFE identity, and is governed by the **same intentions** you wrote in Chapter 07 — no separate policy, no gateway translation. For an organization with a mix of Kubernetes and long-lived VMs, that single control plane over both is the reason to choose Consul.

## Hands-On Lab

### Lab 8.1 — Extend an intention across platforms (Design Exercise)

**Objective.** Reason about — and script — how a database on a VM would join the mesh and be governed by the same `web → db` intention.

**Design Exercise.** Suppose `db` is not the Kubernetes pod but a PostgreSQL server on a **VM**. To bring it into the mesh:

1. Run a **Consul client agent** (or `consul-dataplane`) on the VM and join it to the cluster's Consul servers (`consul agent -retry-join=<server>` with the cluster's gossip key and CA).
2. **Register the service** on the VM with a sidecar proxy:

   ```hcl
   service {
     name = "db"
     port = 5432
     connect { sidecar_service {} }
   }
   ```

3. Run the Envoy sidecar (`consul connect envoy -sidecar-for db`).

The **same** `web → db allow` intention from Chapter 07 now authorizes the Kubernetes `web` pod to reach the VM-hosted `db` — because the intention names the *service* `db`, not a pod or an IP. State why this is impossible with a Kubernetes-only mesh, and what an organization gains from expressing one policy over both platforms.

**Model answer.** A Kubernetes-only mesh (Istio, Linkerd) cannot enroll a VM service, so a hybrid estate needs two policy systems and a gateway between them, with the seam as a weak point. Consul expresses one intention set over pods and VMs alike, so `web → db` means the same thing regardless of where `db` runs — the migration-friendly, heterogeneous-estate advantage.

**Expected result.** A written (and scripted) understanding of the VM-join and why intentions are portable.

**Negative test.** Assume you must re-write the policy when `db` moves from a VM to a pod. You do not — the intention is by service name, so the move is transparent to policy. That portability is the point.

**Cleanup.** None (no VM was provisioned in this single-host lab).

### Lab 8.2 — The un-meshed PLC still needs a network policy

**Objective.** Recognize that even Consul cannot mesh a device that runs no dataplane, and pair the mesh with a CNI policy.

**Walkthrough.** The PLC runs no Consul dataplane, so it has no identity and no intention can govern it — the same boundary the Istio and Linkerd labs reached. Write the Kubernetes `NetworkPolicy` you would apply so only `hmi` may reach the PLC on `:502`:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata: { name: protect-plc }
spec:
  podSelector: { matchLabels: { app: plc } }
  policyTypes: [ Ingress ]
  ingress:
    - from: [ { podSelector: { matchLabels: { app: hmi } } } ]
      ports: [ { protocol: TCP, port: 502 } ]
```

**Expected result.** A clear plan: Consul intentions for meshed services (pods and VMs), and a CNI network policy for the un-meshed PLC — the same mesh-plus-CNI defense-in-depth as the other mesh labs.

**Negative test.** Argue the mesh alone protects the PLC. It cannot govern a service it has no dataplane for. Pair it with a network policy.

**Cleanup.** No NetworkPolicy applied (kind's default CNI may not enforce it); the plan is the deliverable.

### Lab 8.3 — Validate the mesh segmentation

**Objective.** Confirm the end state for the meshed services.

**Walkthrough**

```bash
kubectl exec deploy/web -c web -- nc -z -w2 db 5432 && echo "web -> db  ALLOWED"
kubectl exec deploy/hmi -c hmi -- nc -z -w2 db 5432 || echo "hmi -> db  DENIED"
kubectl exec deploy/web -c web -- curl -s -o /dev/null -w "GET /get 200? %{http_code}\n"  http://api:8080/get
kubectl exec deploy/web -c web -- curl -s -o /dev/null -w "POST /post 403? %{http_code}\n" -X POST http://api:8080/post
```

**Expected result.** `web → db` allowed, `hmi → db` denied, `GET /get` 200, `POST /post` 403 — the same intention set that would govern these services on a VM.

**Negative test.** Delete the `deny-all` and the specific allows; the mesh returns to flat. Intentions are the whole control. Re-apply.

**Cleanup.** Leave the intentions for Chapter 09.

## Summary and Completion Checklist

- [ ] The VM-join steps and why intentions are portable across platforms understood.
- [ ] The un-meshed PLC boundary recognized; the CNI network policy planned.
- [ ] End-to-end validation of the meshed services reproduced.
