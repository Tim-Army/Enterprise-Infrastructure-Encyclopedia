# Chapter 03: The Traditional Stack vs Converged SASE

## Learning Objectives

- Describe the traditional point-product security stack.
- Understand the costs of appliance sprawl — complexity, gaps, lifecycle.
- Explain how convergence eliminates these costs.
- Recognize convergence as more than consolidation.

*Cert relevance: the stack-versus-converged comparison is core **SASE Expert** and **Business Impact** material — the "why change?" argument.*

## The traditional stack

Before SASE, securing an enterprise edge meant assembling a **stack of point products**, each from a (often different) vendor, each a separate box or virtual appliance with its own console, policy model, and lifecycle:

| Function | Point product |
|:---|:---|
| Branch connectivity | SD-WAN appliance |
| Perimeter firewall | Next-gen firewall |
| Web filtering | Secure web gateway |
| Cloud app control | CASB |
| Remote access | VPN concentrator |
| Intrusion prevention | IPS |

Each was chosen "best of breed," bought separately, and **integrated by the customer's team** — wiring them together, keeping their policies consistent, and routing traffic through each in sequence.

## The costs of sprawl

This stack has real, compounding costs that the certifications (especially **Business Impact & Strategy**) teach you to articulate:

- **Complexity** — six products means six consoles, six policy languages, six upgrade cycles, six support contracts. Operating it is a full-time burden, and expertise in all six is rare.
- **Gaps** — security lives *between* the products as much as in them. Traffic that one product doesn't inspect, a policy inconsistent across two consoles, a handoff where context is lost — these seams are where attacks slip through. **Integration is where security breaks.**
- **Latency and hair-pinning** — traffic is routed through each appliance in sequence (service chaining), each adding delay, often backhauled to where the appliances live ([Chapter 2](02-what-is-sase.md)).
- **Lifecycle pain** — each box must be sized, deployed, patched, and refreshed; a capacity limit on one becomes a bottleneck for all.

The lab quantifies the sprawl.

## Convergence eliminates the seams

**Convergence** — Cato's model — replaces the stack with **one cloud service** where all functions are *natively integrated*, share *one policy*, and inspect traffic in a *single pass* ([Chapter 4](04-single-pass-architecture-and-the-global-backbone.md)). This is **more than consolidation** (putting six products in one box). Because the functions are built as one system on one data model, there *are no seams* — no integration to break, no policy to keep consistent across consoles, no context lost at handoffs.

The distinction matters: a "platform" that is really six acquired products bolted together still has the seams internally. True convergence is one engine that does firewall *and* web-gateway *and* CASB *and* ZTNA in one pass on one policy — which is what removes the gaps, not just the console count. The lab models the difference.

## Hands-On Lab

Python models the stack-versus-converged comparison. **Cost:** none.

### Lab 3.1 — The cost of appliance sprawl

**Objective:** Quantify the operational burden and gaps of a point-product stack.

```bash
python3 - <<'EOF'
STACK = ["SD-WAN", "NGFW", "SWG", "CASB", "VPN", "IPS"]
n = len(STACK)
print(f"Traditional stack: {n} point products\n")
print("OPERATIONAL burden:")
print(f"   {n} consoles to learn + operate")
print(f"   {n} policy models to keep consistent")
print(f"   {n} upgrade/patch cycles, {n} support contracts, {n} vendors")
print(f"   seams (integration points BETWEEN products) = {n-1} handoffs where context")
print(f"      can be lost and policy can diverge")
# consistency: probability all N policies stay perfectly in sync degrades with N
p_one_consistent = 0.95
p_all_consistent = p_one_consistent ** n
print(f"\nPOLICY CONSISTENCY (if each product's policy is 95% likely to be correctly synced):")
print(f"   all {n} consistent at once: {100*p_all_consistent:.0f}%")
print(f"   -> ~{100*(1-p_all_consistent):.0f}% chance SOME policy is out of sync = a gap")
print("\nCONVERGED SASE:")
print("   1 console, 1 policy, 0 internal seams (one engine, one data model)")
print("   policy is consistent BY CONSTRUCTION (there's only one)")
print(f"\nThe sprawl tax: {n} products = {n}x the ops burden AND {n-1} seams where security")
print("breaks. And keeping 6 separate policies perfectly in sync is a losing game — the")
print("more products, the more likely SOMETHING is misaligned, and misalignment is a")
print("gap. Convergence removes both: one console (less burden) and one policy (no seams")
print("to diverge). That's the 'why change' the Business Impact cert teaches — it's not")
print("just cost, it's that INTEGRATION is where security fails.")
EOF
```

**Expected result:** A six-product stack imposing six consoles, policies, and lifecycles plus five internal seams, with policy consistency degrading as products multiply, versus converged SASE's one console and one policy consistent by construction. The sprawl lesson is that the point-product stack costs operational burden and opens seams where security breaks, and convergence removes both — the "why change" argument.

**Negative test:** Assuming best-of-breed point products are more secure than a converged platform. The seams between them — inconsistent policy, lost context at handoffs, un-inspected traffic — are where attacks slip through; convergence eliminates the seams, not just the console count.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] The traditional stack understood as separately-bought point products the customer integrates.
- [ ] The costs of sprawl understood — complexity, gaps at the seams, latency, and lifecycle pain.
- [ ] Convergence understood as one natively-integrated cloud service with one policy and single-pass inspection.
- [ ] Convergence recognized as more than consolidation — removing the internal seams, not just the console count.
