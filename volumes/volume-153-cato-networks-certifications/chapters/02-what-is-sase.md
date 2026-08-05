# Chapter 02: What Is SASE?

## Learning Objectives

- Define SASE and the problem it solves.
- Understand why the network perimeter dissolved.
- Explain the convergence of networking and security.
- Place SASE as a cloud-delivered, identity-driven model.

*Cert relevance: this is the heart of **SASE Expert Level 1** — the concept the entire program builds on.*

## The problem: the perimeter dissolved

For decades, enterprise security assumed a **perimeter**: everything important was inside the corporate network (in a data center), users worked from offices *inside* that network, and security was a **stack of appliances at the edge** — firewall, web gateway, VPN concentrator — guarding the boundary between the trusted inside and the untrusted internet.

Then the perimeter **dissolved**. Applications moved to the **cloud and SaaS** (they are no longer inside your data center). Users moved to **remote and hybrid work** (they are no longer inside your office). Now a remote user accessing a SaaS app is *entirely outside* the traditional perimeter — and the old model of hair-pinning their traffic all the way back to a data-center appliance stack, just to send it back out to the cloud, is slow, expensive, and increasingly pointless. The world the perimeter model assumed no longer exists.

## SASE: the convergence

**SASE** (Secure Access Service Edge), coined by Gartner in 2019, is the model built for this new world. Its definition is a **convergence** of two things that used to be separate:

- **Networking** — connecting users, sites, and clouds (SD-WAN, optimized routing).
- **Network security** — protecting that connectivity (secure web gateway, CASB, firewall, zero-trust access).

...delivered as **one cloud service, at the edge, close to the user.** Instead of backhauling traffic to a central appliance stack, SASE inspects and secures it at a **cloud point-of-presence near the user**, then sends it efficiently to its destination (SaaS, internet, or another site).

Two properties define it: **cloud-delivered** (the security and networking are a service, not boxes you rack) and **identity-driven** (access decisions follow *who the user is*, not *where they are on the network* — because "on the network" no longer means anything). SASE is the perimeter reimagined as a **cloud service that follows the user**. The lab models the backhaul problem SASE solves.

## Why converge?

The convergence is the point, not an accident. Networking and security were separate stacks bought from separate vendors, and stitching them together left **gaps, complexity, and latency**. Converging them into one cloud service means: **one policy** (defined by identity and applied everywhere), **one place** traffic is processed (near the user, once), and **no gaps** between the networking and security layers. The [Cato platform (Chapter 4)](04-single-pass-architecture-and-the-global-backbone.md) is one implementation; SASE is the model. The lab is covered within the backhaul exercise.

## Hands-On Lab

Python models the SASE model. **Cost:** none.

### Lab 2.1 — Backhaul versus edge inspection

**Objective:** See why hair-pinning traffic to a central appliance stack fails the cloud/remote world.

```bash
python3 - <<'EOF'
# a remote user in London accessing a SaaS app hosted in London
# traditional: backhaul to the corporate data center (in New York) for security, then out
DIST_LONDON_NY_MS = 40    # one-way latency London <-> New York (~40ms)
DIST_LONDON_SAAS_MS = 5   # London user to London SaaS (~5ms)

print("Remote user in LONDON accessing a SaaS app also in LONDON.\n")
print("TRADITIONAL (backhaul to the data-center appliance stack in NEW YORK):")
# user -> NY (security stack) -> back to London SaaS -> NY -> user
backhaul = DIST_LONDON_NY_MS*2 + DIST_LONDON_NY_MS*2
print(f"   London user -> NY (security) -> London SaaS -> NY -> user")
print(f"   ~{backhaul}ms of latency added, just to route through a distant appliance")
print("   the traffic crossed the Atlantic FOUR times to reach an app 5ms away.")
print("   slow, expensive (backhaul bandwidth), and the appliance is a bottleneck.\n")
print("SASE (inspect at a cloud PoP NEAR the user, in London):")
sase = DIST_LONDON_SAAS_MS*2
print(f"   London user -> London PoP (security, single-pass) -> London SaaS -> user")
print(f"   ~{sase}ms — inspected locally, sent straight to the nearby app")
print(f"\n   latency: {backhaul}ms (backhaul) vs {sase}ms (SASE) — {backhaul//sase}x better")
print("\nWhy backhaul fails the modern world: when the APP is in the cloud and the USER")
print("is remote, forcing their traffic back to a data-center appliance stack (just to")
print("apply security) is absurd — it crosses the world to reach something next door.")
print("SASE moves the security to a CLOUD POP NEAR THE USER, so traffic is inspected")
print("locally and sent straight to its destination. Security follows the user to the")
print("edge, instead of dragging the user back to the security. That's the SASE model.")
EOF
```

**Expected result:** A London user reaching a London SaaS app suffering large added latency when backhauled to a New York appliance stack, versus minimal latency when inspected at a local SASE PoP. The SASE lesson is that when apps are in the cloud and users are remote, backhauling traffic to a central appliance is absurd — SASE moves security to a cloud PoP near the user so traffic is inspected locally and sent straight on.

**Negative test:** Keeping the data-center appliance stack as the security chokepoint for remote users and cloud apps. Their traffic hair-pins across the world and back to reach nearby cloud apps — SASE's edge inspection near the user eliminates the backhaul.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] The dissolved perimeter understood — cloud apps and remote users are outside the traditional boundary.
- [ ] SASE defined as the convergence of networking and security into one cloud-delivered, edge service.
- [ ] The cloud-delivered and identity-driven properties understood — security follows the user, not the network location.
- [ ] The convergence rationale internalized — one policy, one processing point near the user, no gaps.
