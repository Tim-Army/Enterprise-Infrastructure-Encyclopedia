# Chapter 06: mTLS and Workload Identity

## Learning Objectives

- Require mutual TLS across the mesh with `PeerAuthentication`.
- See each workload's cryptographic identity (SPIFFE).
- Verify that mesh traffic is encrypted and identity-checked.

Before you authorize by identity, you must *establish* identity — that is what mTLS does. It encrypts traffic and gives each side a certificate that proves who it is.

## Hands-On Lab

### Lab 6.1 — Require strict mTLS

**Objective.** Move the mesh from permissive to **STRICT** mTLS, so meshed workloads accept only authenticated, encrypted connections.

**Walkthrough**

```bash
kubectl apply -f - <<'EOF'
apiVersion: security.istio.io/v1
kind: PeerAuthentication
metadata: { name: default, namespace: istio-system }
spec:
  mtls: { mode: STRICT }
EOF
```

**Step 2.** Confirm the legitimate meshed flows still work (both sides have sidecars, so mTLS is transparent), and that the un-meshed PLC still receives plaintext (Istio sends plaintext to destinations outside the mesh):

```bash
kubectl exec -n dc deploy/web -c web -- curl -s -o /dev/null -w "web -> api : %{http_code}\n" http://api.dc:8080/get
kubectl exec -n ot deploy/hmi -c hmi -- nc -z -w2 plc.ot 502 && echo "hmi -> plc (plaintext, un-meshed) REACH"
```

**Expected result.** Meshed traffic keeps working over mTLS; the PLC keeps receiving the HMI's connection as plaintext, because Istio knows the PLC has no sidecar. STRICT mode did not break anything here — but it now *rejects* any plaintext attempt to reach a meshed workload from outside the mesh.

> **Note.** If `hmi → plc` breaks after STRICT, add a `DestinationRule` for the `plc` host with `trafficPolicy.tls.mode: DISABLE` to tell Istio to speak plaintext to the un-meshed device explicitly.

**Negative test.** Launch a pod in a namespace *without* injection and try to reach `api.dc:8080`; STRICT mTLS refuses it — the caller has no mesh identity to present. That is the point: an un-identified caller cannot reach a meshed service.

**Cleanup.** Keep STRICT mTLS.

### Lab 6.2 — See the SPIFFE identities

**Objective.** Inspect the cryptographic identity each workload carries.

**Walkthrough**

```bash
istioctl proxy-config secret -n dc deploy/web -o json 2>/dev/null \
  | grep -o 'spiffe://[^"]*' | sort -u
istioctl x describe pod -n dc "$(kubectl get pod -n dc -l app=db -o jsonpath='{.items[0].metadata.name}')" | sed -n '1,12p'
```

**Expected result.** `web`'s certificate carries `spiffe://cluster.local/ns/dc/sa/sa-web`; the describe output shows `db` is in the mesh with mTLS. Each identity encodes the namespace and ServiceAccount — this is the principal you will authorize on in Chapter 07.

**Negative test.** Look for the identity to be the pod IP or name; it is neither. Identity is the ServiceAccount, issued as a certificate, so it cannot be spoofed by taking over an IP.

**Cleanup.** None.

### Lab 6.3 — Verify encryption and mutual authentication

**Objective.** Confirm mesh traffic is genuinely mTLS.

**Walkthrough**

```bash
istioctl x describe pod -n dc "$(kubectl get pod -n dc -l app=api -o jsonpath='{.items[0].metadata.name}')" | grep -i -E "mtls|mode"
```

**Expected result.** The output reports mTLS for the API's traffic. Combined with Lab 6.1, you have: encryption in transit, and each connection carrying a verified SPIFFE identity — the substrate identity-based authorization needs.

**Negative test.** Recall the un-meshed PLC: `istioctl x describe` shows it is *not* in the mesh, so it has no mTLS and no identity. Chapter 08 addresses what that means for protecting it.

**Cleanup.** Keep the mesh in STRICT mTLS for Chapter 07.

## Summary and Completion Checklist

- [ ] STRICT mTLS required mesh-wide; meshed flows still work, plaintext-to-mesh refused.
- [ ] SPIFFE identities inspected; each encodes namespace + ServiceAccount.
- [ ] mTLS on mesh traffic verified with `istioctl`.
