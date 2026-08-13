# Chapter 02: The SASE Accreditation — SASE Architecture

## Learning Objectives

- Cover the SASE Accreditation's agenda: SASE origin, architecture, Zero Trust, SD-WAN, and SSE.
- Understand the deployment approaches and organizational dynamics the accreditation teaches.
- Model the "backhaul vs edge" difference that motivates SASE.

## The accreditation in brief

The **SASE Accreditation** is a **free, vendor-agnostic**, on-demand course (48 hours to log in, 2 weeks to complete) with an optional online exam: **45 minutes, two attempts, 80% to pass**, yielding a certificate and LinkedIn badge. Its agenda: SASE purpose/origin, high-level architecture, Zero Trust, SD-WAN, Security Service Edge, IT-org dynamics, and deployment approaches. It is lecture-style — no software required — so this chapter's labs *illustrate* the concepts rather than reproduce a product.

## Why SASE exists

The old model backhauled branch/remote traffic to a central data-center security stack (hub-and-spoke MPLS), then out to the cloud — adding latency and cost as apps moved to SaaS. **SASE inverts this:** security and networking move to the **cloud edge**, close to users, so traffic goes **direct to cloud** through inline inspection instead of hairpinning through a data center.

## Hands-On Lab

Free primitives illustrate the architecture. **Cost:** none.

### Lab 2.1 — Backhaul vs edge latency

**Objective:** Quantify why SASE moves inspection to the edge.

```bash
python3 - <<'EOF'
# Latency: user -> app, comparing backhaul-to-datacenter vs direct-to-edge
user_to_dc = 40    # ms to the central data-center stack
dc_to_app  = 30    # ms from DC out to the SaaS app
user_to_edge = 8   # ms to a nearby SASE edge (NewEdge PoP)
edge_to_app  = 15  # ms from edge to app
backhaul = user_to_dc + dc_to_app + user_to_dc + dc_to_app   # round trip through DC
edge     = user_to_edge + edge_to_app + user_to_edge + edge_to_app
print(f"backhaul round trip: {backhaul} ms")
print(f"SASE edge round trip: {edge} ms  ({backhaul-edge} ms saved)")
EOF
```

**Expected result:**

```text
backhaul round trip: 140 ms
SASE edge round trip: 46 ms  (94 ms saved)
```

The edge model cuts latency dramatically by inspecting near the user and going direct to the app — the core SASE value the accreditation opens with. A global edge network (Netskope's **NewEdge**) is what makes "near the user" true worldwide.

**Negative test:** Deploying "cloud security" that still hairpins through one region — you keep the backhaul penalty; the edge must be distributed for SASE's latency win to be real.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.2 — Zero Trust: verify, don't assume

**Objective:** Model the Zero Trust access decision the accreditation teaches.

```bash
python3 - <<'EOF'
# Zero Trust: access decided per-request from identity + context, not network location
def allow(user, role, device_managed, app_sensitivity, location):
    if not device_managed and app_sensitivity == "high": return "DENY (unmanaged device, sensitive app)"
    if role == "contractor" and app_sensitivity == "high": return "DENY (role)"
    if location == "anomalous": return "STEP-UP (MFA challenge)"
    return "ALLOW"
print("employee/managed/high/normal:", allow("a","employee",True,"high","normal"))
print("employee/BYOD/high/normal:   ", allow("b","employee",False,"high","normal"))
print("employee/managed/high/anom:  ", allow("c","employee",True,"high","anomalous"))
EOF
```

**Expected result:**

```text
employee/managed/high/normal: ALLOW
employee/BYOD/high/normal:    DENY (unmanaged device, sensitive app)
employee/managed/high/anom:   STEP-UP (MFA challenge)
```

Zero Trust decides **per request** from identity, device posture, app sensitivity, and context — never "trusted because on the corporate network." This principle runs through every SSE control (ZTNA, CASB, SWG).

**Negative test:** Granting access by IP/network zone (the old "castle-and-moat") — a compromised device inside the perimeter has free rein; Zero Trust removes implicit network trust.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.3 — SD-WAN, the networking half

**Objective:** State what SD-WAN contributes to SASE.

```bash
cat <<'EOF'
SD-WAN (networking half of SASE):
  - policy-based path selection across multiple transports (MPLS, broadband, LTE/5G)
  - application-aware routing (send SaaS direct-to-internet, keep sensitive apps on private paths)
  - resilience (failover across links), central orchestration
SASE = SD-WAN (get traffic to the edge efficiently) + SSE (secure it there)
EOF
```

**Expected result:** SD-WAN as the transport intelligence — choosing the best path per app and steering internet-bound traffic straight to the SASE edge. The accreditation pairs it with SSE to complete the SASE definition.

**Negative test:** Treating SASE as "just cloud security" (SSE only) — it also subsumes the WAN edge; the SD-WAN half is why SASE is a *networking-and-security* convergence.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.4 — Deployment approaches

**Objective:** Understand the accreditation's deployment guidance.

```bash
cat <<'EOF'
Approaches for deployment (accreditation agenda):
  - start with visibility (see cloud/web usage before enforcing) -> then policy
  - phase controls: SWG/CASB first, DLP and ZTNA as maturity grows
  - single-vendor SASE (converged) vs best-of-breed SSE + SD-WAN (integration cost)
  - organizational dynamics: networking + security teams must converge (SASE is org change too)
EOF
```

**Expected result:** The pragmatic rollout — visibility first, phased enforcement, and the single-vendor-vs-best-of-breed choice — plus the accreditation's honest point that SASE is an **organizational** convergence (networking and security teams), not only a technology one.

**Negative test:** Enforcing blocking policy before establishing visibility — you break legitimate workflows and lose the org's trust; visibility-then-policy is the accreditation's sequencing.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] The SASE Accreditation's format (free, 45-min exam, 80%) and agenda known.
- [ ] Backhaul-vs-edge latency and the NewEdge rationale internalized.
- [ ] Zero Trust per-request decisioning and SD-WAN's role understood.
- [ ] Deployment sequencing (visibility → phased policy) and org convergence grasped.
