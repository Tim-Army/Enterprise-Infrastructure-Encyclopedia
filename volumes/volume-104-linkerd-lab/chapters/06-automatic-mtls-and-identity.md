# Chapter 06: Automatic mTLS and Identity

## Learning Objectives

- Confirm that mesh traffic is already mTLS — with no configuration.
- See each workload's identity, derived from its ServiceAccount.
- Watch a live request and confirm it is TLS-secured.

Istio required a `PeerAuthentication` object to enforce mTLS. Linkerd required nothing: mTLS was on the moment you meshed the workloads in Chapter 04. This chapter proves it.

## Hands-On Lab

### Lab 6.1 — Confirm mTLS is already on

**Objective.** See that mesh connections are mutually authenticated and encrypted, with no policy applied.

**Walkthrough**

**Step 1.** Generate a little traffic, then look at the edges Linkerd observed:

```bash
kubectl exec -n dc deploy/web -c web -- curl -s -o /dev/null http://api.dc:8080/get
linkerd viz edges deployment -n dc
```

**Expected result.** The `edges` output lists connections between the meshed deployments with the **SECURED** column marked (a check / `√`), meaning mTLS. You wrote no mTLS configuration — Linkerd issued each workload a certificate and encrypted the traffic automatically. This is the headline difference from Istio.

**Negative test.** Look for an edge to or from the un-meshed `plc`; it is not mTLS-secured, because the PLC has no proxy and no identity. Only meshed-to-meshed traffic is automatically mTLS.

**Cleanup.** None.

### Lab 6.2 — See the ServiceAccount identities

**Objective.** Inspect the identity each workload carries.

**Walkthrough**

```bash
linkerd viz tap -n dc deploy/api --to deploy/api 2>/dev/null &   # start a tap
kubectl exec -n dc deploy/web -c web -- curl -s -o /dev/null http://api.dc:8080/get
sleep 2; kill %1 2>/dev/null
# identities also appear in the proxy's environment:
kubectl get pod -n dc -l app=web -o jsonpath='{.items[0].spec.serviceAccountName}{"\n"}'
```

**Expected result.** The web workload runs as `sa-web`, so its mesh identity is `sa-web.dc.serviceaccount.identity.linkerd.cluster.local`. The `tap` output shows requests carrying `tls=true` and the client/server identities. This identity — not an IP — is what you authorize on.

**Negative test.** Note the identity is the ServiceAccount, not the pod. Two pods of the same Deployment share the identity, and a rescheduled pod keeps it. Identity is stable; IPs are not.

**Cleanup.** None.

### Lab 6.3 — Watch a live request

**Objective.** Confirm a real request is TLS-secured end to end.

**Walkthrough**

```bash
linkerd viz tap -n dc deploy/api 2>/dev/null &
kubectl exec -n dc deploy/web -c web -- curl -s -o /dev/null http://api.dc:8080/get
sleep 2; kill %1 2>/dev/null
```

**Expected result.** The tap shows the `GET /get` request with `tls=true` and the source identity `sa-web...`. You have live proof that mesh traffic is authenticated and encrypted — the substrate the Chapter 07 authorization builds on.

**Negative test.** There is nothing to disable to "turn off" mTLS in the mesh short of removing the proxy; Linkerd's opinion is that mesh traffic is always encrypted. That opinion is the product.

**Cleanup.** Keep the mesh for Chapter 07.

## Summary and Completion Checklist

- [ ] `linkerd viz edges` shows mesh connections SECURED (mTLS) with no configuration.
- [ ] Each workload's identity confirmed to come from its ServiceAccount.
- [ ] A live request observed with `tls=true` via `linkerd viz tap`.
