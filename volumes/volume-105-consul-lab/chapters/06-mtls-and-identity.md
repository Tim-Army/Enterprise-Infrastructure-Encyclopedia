# Chapter 06: mTLS and Identity with Connect

## Learning Objectives

- Confirm that Connect secures mesh traffic with mTLS.
- See each service's SPIFFE identity.
- Understand what identity intentions will authorize on.

Consul Connect gives each meshed service a SPIFFE identity and encrypts service-to-service traffic with mTLS — the substrate the intentions in Chapter 07 build on.

## Hands-On Lab

### Lab 6.1 — Confirm the mesh secures traffic

**Objective.** See that meshed services communicate over Connect's mTLS.

**Walkthrough**

**Step 1.** Generate a little traffic, then look at the intentions/topology view in the UI (or the CLI):

```bash
kubectl exec deploy/web -c web -- curl -s -o /dev/null http://api:8080/get
# with the UI port-forward and token from Chapter 03, open the 'api' service -> Topology tab
# or from the CLI:
kubectl -n consul exec statefulset/consul-server -- consul catalog services
```

**Expected result.** The catalog lists `web`, `api`, `db`, and `hmi` (plus their `-sidecar-proxy` entries). The UI's Topology view shows connections between them, secured by Connect. Traffic between meshed services is mTLS.

**Negative test.** Look for the un-meshed `plc` in the sidecar-proxy list; it is not there — it has no proxy and no Connect identity.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 6.2 — See the SPIFFE identities

**Objective.** Inspect the identity each service carries.

**Walkthrough**

```bash
kubectl -n consul exec statefulset/consul-server -- consul catalog nodes -service=web 2>/dev/null || true
# each Connect service has a SPIFFE identity of the form:
echo "spiffe://<datacenter-domain>/ns/default/dc/dc1/svc/web"
```

**Expected result.** Each service has a SPIFFE identity encoding its name (and namespace/datacenter). Intentions authorize on this service identity — which is why the same intention governs the service whether it runs as a pod here or on a VM (Chapter 08).

**Negative test.** Note the identity is the service, not the pod IP. It is stable across pod restarts and portable across platforms.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 6.3 — Confirm encryption

**Objective.** Confirm mesh traffic is genuinely encrypted, not plaintext.

**Walkthrough**

```bash
# The app container talks to the local sidecar; the sidecar does mTLS to the peer sidecar.
# Confirm the sidecar is present and handling traffic:
kubectl get pod -l app=web -o jsonpath='{.items[0].spec.containers[*].name}{"\n"}'
```

**Expected result.** The `web` pod lists the app container plus a `consul-dataplane` sidecar; that sidecar terminates mTLS for all mesh traffic. Combined with Lab 6.1, meshed service-to-service traffic is encrypted and identity-checked — ready for authorization.

**Negative test.** There is no per-connection switch to disable Connect mTLS for meshed services; encryption is intrinsic to the mesh, as with Linkerd.

**Rollback.** Keep the mesh for Chapter 07.

## Summary and Completion Checklist

- [ ] Meshed services confirmed communicating over Connect mTLS.
- [ ] Each service's SPIFFE identity understood (portable across platforms).
- [ ] The sidecar (`consul-dataplane`) confirmed present on meshed pods.
