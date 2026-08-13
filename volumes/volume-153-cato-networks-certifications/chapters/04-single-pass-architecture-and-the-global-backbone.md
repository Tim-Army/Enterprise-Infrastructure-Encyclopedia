# Chapter 04: Single-Pass Architecture and the Global Backbone

## Learning Objectives

- Explain single-pass architecture and why it beats service chaining.
- Understand the global private backbone of PoPs.
- Describe how the backbone optimizes performance versus the public internet.
- Recognize the two pillars of Cato's converged cloud.

*Cert relevance: single-pass and the backbone are core **SASE Expert Level 2** (architecture) material.*

## Single-pass architecture

The traditional stack **service-chains** traffic: a packet goes *through* the firewall, *then* the web gateway, *then* the CASB, *then* the IPS — each a separate engine that independently parses, decrypts, and re-inspects the traffic. That is four decrypt/parse cycles, four points of latency, for one packet.

**Single-pass architecture** inspects traffic **once**: a single engine decrypts and parses the packet *one time*, then applies *all* the security functions (firewall, web filtering, CASB, threat prevention, data controls) against that single parsed representation, in one pass. Because the expensive work — decryption and deep parsing — happens once rather than per-function, single-pass is **dramatically faster and more efficient**, and it enables the functions to share context (the firewall's verdict informs the web gateway's, no re-work). Single-pass is what makes converging many functions *performant* rather than the sum of their latencies. The lab quantifies it.

## The global private backbone

The second pillar is Cato's **global private backbone** — a worldwide network of **PoPs (points of presence)** connected by Cato's own optimized, SLA-backed links. This solves the **performance** problem of cloud security: to inspect traffic near the user, you need presence near users *everywhere*, and to move traffic between regions fast, you need better-than-internet routing.

When a user connects, they reach the **nearest PoP** (low latency), their traffic is inspected there (single-pass), and if it must cross the globe (to a distant SaaS or another office), it rides Cato's **private backbone** — which is faster and more reliable than the public internet, choosing optimal routes and avoiding congestion. The backbone is what lets a converged cloud service be *fast globally*, not just secure. The lab models backbone routing.

## The two pillars together

Single-pass (inspect efficiently, once) and the global backbone (be near every user, route optimally) are the **two pillars** that make Cato's converged cloud both **secure and fast** — the combination the [Chapter 3](03-traditional-stack-vs-converged-sase.md) convergence promise depends on. A converged service that was slow would not be adopted; single-pass makes the security fast, the backbone makes the network fast, and together they deliver convergence *without* a performance penalty. The lab is covered within the two exercises.

## Hands-On Lab

Python models the architecture. **Cost:** none.

### Lab 4.1 — Single-pass versus service chaining

**Objective:** See why inspecting once beats chaining separate engines.

```bash
python3 - <<'EOF'
FUNCTIONS = ["firewall", "web gateway (SWG)", "CASB", "threat prevention (IPS)", "data controls"]
DECRYPT_PARSE_MS = 4   # the expensive work: decrypt + deep-parse the traffic
APPLY_POLICY_MS = 1    # applying one function's rules to already-parsed traffic

print(f"Inspecting traffic against {len(FUNCTIONS)} security functions.\n")
print("SERVICE CHAINING (separate engines, each re-inspects):")
chain_latency = len(FUNCTIONS) * (DECRYPT_PARSE_MS + APPLY_POLICY_MS)
for f in FUNCTIONS:
    print(f"   {f:26} decrypt+parse ({DECRYPT_PARSE_MS}ms) + apply ({APPLY_POLICY_MS}ms)")
print(f"   -> each function independently decrypts + parses = {chain_latency}ms total")
print(f"      ({len(FUNCTIONS)} redundant decrypt/parse cycles for ONE packet)\n")

print("SINGLE-PASS (decrypt+parse ONCE, apply all functions to that representation):")
single_latency = DECRYPT_PARSE_MS + len(FUNCTIONS) * APPLY_POLICY_MS
print(f"   decrypt+parse ONCE ({DECRYPT_PARSE_MS}ms), then apply all {len(FUNCTIONS)} functions ({len(FUNCTIONS)}x{APPLY_POLICY_MS}ms)")
print(f"   -> {single_latency}ms total, and functions SHARE context (no re-work)\n")
print(f"   service chaining: {chain_latency}ms  vs  single-pass: {single_latency}ms  "
      f"({chain_latency/single_latency:.1f}x faster)")
print("\nThe insight: the EXPENSIVE work is decryption + deep parsing — and service")
print("chaining does it ONCE PER FUNCTION (5 times here), because each engine is")
print("separate. Single-pass parses the traffic ONCE and runs all functions against")
print("that one representation, so the cost is ~one parse + a little per function.")
print("This is what makes CONVERGENCE performant: adding a 6th security function to a")
print("single-pass engine adds ~1ms, not another full decrypt/parse. Without single-")
print("pass, 'converged' would just mean 'all the latencies added up.'")
EOF
```

**Expected result:** Service chaining redundantly decrypting and parsing the traffic once per function (five times) while single-pass parses once and applies all functions to that representation, several times faster. The single-pass lesson is that the expensive work is decryption and parsing, so doing it once rather than per-function is what makes converging many security functions performant rather than the sum of their latencies.

**Negative test:** Assuming a converged platform is just as slow as a chain of the same functions. Single-pass does the expensive decrypt/parse once, so each added function costs little — service chaining repeats the expensive work per engine, which single-pass avoids.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.2 — The private backbone versus the public internet

**Objective:** See why a global PoP backbone outperforms internet routing.

```bash
python3 - <<'EOF'
import random
random.seed(4)
# a user in Tokyo reaching a service in Frankfurt
print("User in TOKYO reaching a service in FRANKFURT.\n")
print("PUBLIC INTERNET (best-effort, congestion, suboptimal routing):")
# internet path: variable, congested hops
internet_latency = 240 + random.randint(30, 120)   # base + jitter/congestion
loss = random.uniform(0.5, 2.0)
print(f"   latency ~{internet_latency}ms (variable), packet loss ~{loss:.1f}%")
print("   routes chosen by BGP for reachability, NOT performance; congestion adds jitter")
print("   -> unpredictable; bad for real-time (voice/video) and large transfers\n")
print("CATO GLOBAL BACKBONE (private, optimized, SLA-backed):")
print("   Tokyo user -> nearest PoP (Tokyo, ~5ms) -> Cato private backbone -> Frankfurt PoP -> service")
backbone_latency = 180
print(f"   latency ~{backbone_latency}ms (consistent), packet loss <0.1%, SLA-backed")
print("   the backbone picks OPTIMAL routes and avoids congestion; predictable + fast")
print(f"\n   internet ~{internet_latency}ms (jittery) vs backbone ~{backbone_latency}ms (steady)")
print("\nWhy the backbone matters: to inspect traffic NEAR every user you need PoPs")
print("everywhere; to move it between regions FAST you need better-than-internet")
print("routing. Cato's private global backbone gives both — connect to the nearest PoP,")
print("get inspected there (single-pass), and if traffic must cross the world it rides")
print("an OPTIMIZED private network, not the congested public internet. The backbone is")
print("what makes a converged CLOUD security service also FAST globally — the second")
print("pillar alongside single-pass. Security AND performance, not a trade-off.")
EOF
```

**Expected result:** Public-internet routing between distant regions being slower and jittier with higher loss than Cato's optimized private backbone with consistent latency and an SLA. The backbone lesson is that delivering cloud security globally requires both presence near every user (PoPs) and better-than-internet routing between regions, which the private backbone provides — making the converged service fast, not just secure.

**Negative test:** Delivering global cloud security over the public internet alone. Routing is best-effort and congested, so performance is unpredictable — a private optimized backbone of PoPs is what makes edge inspection near users and fast inter-region transport possible.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Single-pass architecture understood as decrypting and parsing once, then applying all functions — beating service chaining.
- [ ] The global private backbone understood as worldwide PoPs connected by optimized, SLA-backed links.
- [ ] The backbone's performance advantage over the public internet (near every user, optimal routing) recognized.
- [ ] Single-pass and the backbone understood as the two pillars making convergence both secure and fast.
