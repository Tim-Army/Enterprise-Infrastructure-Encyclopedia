# Chapter 12: Service Mesh and Workload-Identity Segmentation

## Learning Objectives

- Explain why a service mesh is a distinct enforcement layer above L3/L4 network policy.
- Describe Istio, Linkerd, and HashiCorp Consul as segmentation mechanisms.
- Explain SPIFFE/SPIRE workload identity and why cryptographic identity beats IP-based policy.
- Record cost model, implementation effort, FIPS, FedRAMP, and air-gap posture.
- Complete a walkthrough for each topic.

## Theory and Architecture

Chapter 08 covered Kubernetes NetworkPolicy with Calico and Cilium, which enforce at L3/L4 — addresses,
ports, and labels. A service mesh enforces one layer higher, on **cryptographic workload identity and
L7 semantics**.

The mechanism is mutual TLS between workloads, where each workload holds a short-lived certificate
naming *what it is* rather than *where it is*. **SPIFFE** defines that identity format (a SPIFFE ID such
as `spiffe://cluster.local/ns/prod/sa/orders`) and **SPIRE** is its reference issuing system. Policy is
then written against identity: "the `orders` service account may call `POST /charge` on the `payments`
service" — a statement no IP-based firewall can express.

**Istio** is the most feature-complete implementation, historically deploying an Envoy sidecar beside
every workload and more recently offering an *ambient* mode that removes the per-pod sidecar in favor of
a per-node component, reducing overhead. **Linkerd** takes the opposite design stance: a purpose-built
lightweight Rust proxy, far fewer knobs, mTLS on by default. **HashiCorp Consul** provides a service
mesh whose *intentions* are explicitly service-to-service authorization rules, and — unlike the other
two — it spans virtual machines as well as containers, which matters for estates mid-migration.

The critical property is that identity is issued and rotated automatically and is verified
cryptographically on every connection. An attacker who steals an IP address, spoofs a MAC, or lands on
the right subnet gains nothing, because none of those are the credential.

## Pros, Cons, Compatibility, and Requirements

- **Pros:** identity is cryptographic, not positional; policy expresses L7 intent (method, path) that
  L3/L4 cannot; mTLS gives encryption in transit as a side effect; certificates rotate automatically;
  all three options are **open source with no license cost**.
- **Cons:** covers only workloads *in the mesh* — the unmanaged printer, the PLC, and the legacy VM are
  outside it entirely, so a mesh is never a whole-estate answer; sidecars add latency and resource
  overhead (ambient and Linkerd mitigate, not eliminate); it is a substantial operational commitment,
  and a mesh adopted solely for segmentation is usually the wrong tool.
- **Compatibility:** Istio and Linkerd target Kubernetes; Consul spans Kubernetes and VMs. All integrate
  with L3/L4 policy rather than replacing it — mesh and NetworkPolicy are complementary layers.
- **Requirements:** a Kubernetes platform (or Consul agents on VMs); a certificate authority, either the
  mesh's built-in CA or SPIRE; a control plane sized for the workload count; and a team that will own
  it.

**Cost model.** Istio, Linkerd, and Consul are **open source and free to run**; the cost is operational
plus optional commercial support — Buoyant for Linkerd, HashiCorp/IBM for Consul Enterprise, and various
vendors for Istio. That makes this the only tier in this volume with a genuine zero-license entry point,
and the one where the true cost is entirely staff time.

**Implementation time (estimate, not a vendor commitment).** A mesh on an existing, healthy Kubernetes
platform reaches mTLS-everywhere in **4–10 weeks**; adding meaningful L7 authorization policy is a
continuing program, not a project, because it requires per-service knowledge. Retrofitting a mesh onto
an unhealthy platform takes far longer and should not be attempted for segmentation reasons alone.

**FIPS 140-3.** The mesh proxies use an underlying cryptographic library, and the FIPS question is
answered by *that module*, not by the mesh. FIPS-mode builds exist (BoringCrypto-based distributions and
vendor-supported variants); verify the specific build in the
[NIST CMVP list](https://csrc.nist.gov/projects/cryptographic-module-validation-program/validated-modules/search).
Upstream community builds are generally **not** validated — this is the single most common compliance
mistake in mesh deployments.

**FedRAMP.** Not applicable to the software itself, which you run. Where the mesh is consumed as a
managed service from a cloud provider, the *provider's* service carries the authorization; check it in
the [FedRAMP Marketplace](https://marketplace.fedramp.gov/).

**Air-gap.** Excellent, and better than most commercial options. All three are self-hosted with no
mandatory call-home; images can be mirrored to an internal registry and the built-in CA needs no
external connectivity. This is one of the few segmentation approaches that runs unchanged in a fully
disconnected environment.

## Design Considerations

Adopt a mesh when you already need what a mesh provides — traffic management, retries, observability,
mTLS — and take segmentation as a benefit. Adopt SPIFFE/SPIRE when workload identity is needed across
platforms that no single mesh covers.

Do not present a mesh as estate-wide microsegmentation. Pair it with an L3/L4 layer beneath (Chapter 08)
and a mechanism for everything outside the cluster (Chapters 10, 11, or 14). The mesh is the innermost
ring of a layered design.

## Implementation and Automation

Enable strict mTLS in permissive mode first, confirm every workload is presenting an identity, then
switch to strict. Authorization policy follows the same discipline as everywhere else in this volume:
observe, ring-fence, tighten. Keep policies in Git beside the workload manifests.

## Validation and Troubleshooting

Verify identity before debugging policy: confirm the workload's certificate and SPIFFE ID, then confirm
the policy selector matches it. A denial with no matching policy is usually an identity that was never
issued — a missing service account or an un-injected sidecar — not a bad rule.

## Security and Best Practices

Keep certificate lifetimes short and rotation automatic. Do not disable mTLS to debug; use permissive
mode. Remember that a mesh sees only mesh traffic — a workload that bypasses its proxy is unsegmented,
so enforce sidecar injection or ambient enrollment as policy.

## Hands-On Lab

### Lab 12.1 — Express a policy identity cannot be spoofed

**Objective.** Contrast address-based and identity-based authorization.

```python
request = {"src_ip": "10.10.20.11", "spiffe_id": "spiffe://cluster.local/ns/prod/sa/orders",
           "method": "POST", "path": "/charge"}
ip_rule = {"allow_src": "10.10.20.11", "port": 8080}
id_rule = {"allow_id": "spiffe://cluster.local/ns/prod/sa/orders",
           "methods": ["POST"], "paths": ["/charge"]}
print("ip rule  ->", "ALLOW" if request["src_ip"] == ip_rule["allow_src"] else "DENY")
print("id rule  ->", "ALLOW" if (request["spiffe_id"] == id_rule["allow_id"]
      and request["method"] in id_rule["methods"] and request["path"] in id_rule["paths"]) else "DENY")
```

**Expected result.** Both allow the legitimate call.

**Negative test.** An attacker takes over 10.10.20.11 and calls `POST /refund`. Set
`request["path"] = "/refund"` and re-run: the IP rule still allows it, the identity rule denies it. The
address was never a credential.

**Cleanup.** None.

### Lab 12.2 — Measure mesh coverage against the estate

**Objective.** Quantify what a mesh cannot protect.

```python
estate = {"k8s workloads": 240, "linux VMs": 85, "windows VMs": 60,
          "network appliances": 22, "OT devices": 40}
in_mesh = {"k8s workloads"}
covered = sum(v for k, v in estate.items() if k in in_mesh)
total = sum(estate.values())
print(f"mesh-covered: {covered}/{total} ({covered/total:.0%})")
print(f"requires another mechanism: {total - covered} assets")
```

**Expected result.** 240 of 447 (54%) — 207 assets need a different mechanism.

**Negative test.** Claim the mesh is the segmentation strategy. Nearly half the estate, including every
OT device, is entirely unprotected by it. A mesh is a layer, never the plan.

**Cleanup.** None.

### Lab 12.3 — Stage a permissive-to-strict mTLS rollout

**Objective.** Sequence the change so it cannot cause an outage.

```python
services = {"orders": True, "payments": True, "legacy-batch": False}   # sidecar injected?
print("PERMISSIVE mode - plaintext and mTLS both accepted:")
for s, injected in services.items():
    print(f"  {s:<14}{'mTLS' if injected else 'plaintext'} -> ACCEPTED")
print("\nSTRICT mode:")
for s, injected in services.items():
    print(f"  {s:<14}{'mTLS -> ACCEPTED' if injected else 'plaintext -> REJECTED (outage)'}")
```

**Expected result.** `legacy-batch` breaks the moment strict mode is enabled.

**Negative test.** Enable strict mode estate-wide without checking injection coverage — exactly the
outage above. Permissive mode exists to find the `legacy-batch` cases first.

**Cleanup.** Return to permissive until every workload is enrolled.

### Lab 12.4 — Score the mesh tier against the rubric

**Objective.** Score this tier on the five **constraint axes** used across Chapters 10–15 — a deliberate reduction of Chapter 02's eight-dimension rubric that promotes air-gap capability to a first-class axis, because it disqualifies options outright rather than merely scoring them.

```python
weights = {"agentless": 0.30, "granularity": 0.25, "coverage": 0.20,
           "air_gap": 0.15, "effort": 0.10}
mesh = {"agentless": 1, "granularity": 5, "coverage": 2, "air_gap": 5, "effort": 2}
print(f"weighted score: {sum(weights[k] * mesh[k] for k in weights):.2f} / 5.00")
```

**Expected result.** 2.90 — best-in-volume granularity and air-gap, worst on agentless reach and
coverage.

**Negative test.** Re-weight `granularity` to 0.60 and the mesh wins outright — which is correct for a
container-only estate and wrong for a mixed one. Score the estate you have.

**Cleanup.** None.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

A service mesh enforces on cryptographic workload identity and L7 intent — the finest granularity in
this volume, free of license cost and fully air-gap capable — but it protects only workloads inside the
mesh, which makes it the innermost layer of a design rather than the design itself.

- [ ] I can explain SPIFFE identity and why it beats address-based policy.
- [ ] I can quantify the estate a mesh cannot cover.
- [ ] I can sequence a permissive-to-strict mTLS rollout without an outage.
- [ ] I completed Labs 12.1–12.4 including each negative test.
