# Chapter 02: The Edge Network, DNS, and Caching

## Learning Objectives

- Explain anycast routing and what it means for both performance and attack absorption.
- Run authoritative DNS on Cloudflare and reason about proxied versus DNS-only records.
- Control caching: what is cacheable, cache keys, TTLs, and purges.
- Measure what cache hit ratio actually buys — and what a purge actually costs.

*Exam relevance: foundational for both exams — the edge network is the substrate every Application Security and Zero Trust feature runs on, and "basic, hands-on experience" with it is the published prerequisite posture.*

## Anycast

Cloudflare announces the **same IP addresses from every data center**. Your DNS record points at one address; BGP routing delivers each user to the *nearest* location announcing it. Nobody chooses a region; the internet's routing chooses for every packet.

Two consequences carry the rest of the volume:

1. **Performance is automatic and topological.** A user in Warsaw and a user in Lima hit different data centers with the same configuration. There is no "multi-region deployment" to design — the deployment *is* multi-region by construction.
2. **Attacks distribute themselves.** A DDoS aimed at an anycast address is absorbed by the network in proportion to where its sources are. A botnet spread across ninety countries delivers its traffic to dozens of data centers, each seeing a fraction — which is the structural reason edge networks can absorb attacks that would concentrate fatally on a single origin (Chapter 04 does the arithmetic).

## DNS: proxied or not

Cloudflare is an authoritative DNS provider, and each record makes the volume's most consequential small decision — the **proxy toggle**:

| | **Proxied** (orange cloud) | **DNS-only** (gray cloud) |
|:---|:---|:---|
| The record resolves to | Cloudflare anycast IPs | Your origin's real IP |
| Traffic flows | Through the edge — cache, WAF, DDoS protection apply | Directly to origin |
| Origin IP exposure | Hidden | **Published to the world** |

The security consequence deserves plain words: **every protection in Chapters 03–04 applies only to proxied traffic.** A single DNS-only record pointing at the origin — an old `ftp.` entry, a staging subdomain, a mail record reused for a web service — publishes the address attackers need to bypass the WAF entirely and hit the origin directly. Origin exposure via forgotten DNS records is one of the most common real-world Cloudflare misconfigurations, and the lab models the audit.

## Caching

The CDN caches eligible content at the edge. The decisions that matter:

- **What is cacheable.** Static assets cache by default; HTML typically does not unless you say so. Cacheability is decided by rules and headers, not hope.
- **The cache key** — URL plus whatever you add. Every component multiplies variants: adding a query string or header to the key splits one cached object into many, and each variant misses independently. The cardinality lesson of this shelf, in CDN clothing.
- **TTL and purge.** A long TTL raises hit ratio and slows change propagation; purge is instant and *global* — and every purged object's next request hits your origin. A purge-everything on a busy site converts your entire edge hit ratio into origin load for as long as the cache takes to rewarm.

## Hands-On Lab

Python models the edge. **Cost:** none. (A free Cloudflare account with a spare domain makes all three labs real.)

### Lab 2.1 — Anycast distributes load and attacks alike

**Objective:** Model why the same property helps both.

```bash
python3 - <<'EOF'
REGIONS = {          # share of sources per region (users and, later, botnet)
  "north-america": 0.30, "europe": 0.28, "asia-pacific": 0.24,
  "south-america": 0.10, "africa-mideast": 0.08,
}
EDGE_SITES = {"north-america": 90, "europe": 80, "asia-pacific": 70,
              "south-america": 30, "africa-mideast": 30}

print("LEGITIMATE TRAFFIC — 1,000,000 requests/min, one config, no region design:")
for r, share in REGIONS.items():
    per_site = share * 1_000_000 / EDGE_SITES[r]
    print(f"   {r:16} {share*100:>4.0f}% -> {EDGE_SITES[r]:>3} sites, ~{per_site:>7,.0f} req/min/site")

print("\nATTACK — 80M req/min botnet, sources distributed like users:")
worst = 0
for r, share in REGIONS.items():
    per_site = share * 80_000_000 / EDGE_SITES[r]
    worst = max(worst, per_site)
    print(f"   {r:16} {share*100:>4.0f}% -> spread over {EDGE_SITES[r]:>3} sites, ~{per_site:>9,.0f} req/min/site")

print(f"\n   worst single site sees ~{worst:,.0f} req/min — heavy, absorbable.")
print(f"   the same 80M req/min aimed at ONE origin = 80,000,000 req/min at one place.")
print(f"   ratio: the origin scenario concentrates ~{80_000_000/worst:,.0f}x more load on its target.\n")
print("Anycast is not an anti-DDoS feature bolted on; it is routing arithmetic.")
print("Attacks arrive pre-divided because BGP delivers each source to its nearest")
print("site — the identical mechanism that gives users low latency. One property,")
print("both benefits, no configuration.")
EOF
```

**Expected result:** The worst-loaded site absorbs roughly 280,000 req/min of an 80M req/min attack — about 286x less than the single-origin scenario concentrates. The framing to keep is the last paragraph: distribution is not a defensive feature that could be misconfigured off; it is what anycast routing *is*.

**Negative test:** Concluding the origin no longer matters. Chapter 03's protections and this chapter's origin-exposure audit exist because attackers who find the real origin IP skip the entire edge.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.2 — The DNS audit: find the gray-cloud leak

**Objective:** Catch origin exposure the way an attacker would.

```bash
python3 - <<'EOF'
ZONE = [
  # name,               type,  target,           proxied
  ("www",               "A",   "203.0.113.10",   True),
  ("api",               "A",   "203.0.113.10",   True),
  ("blog",              "CNAME","www",           True),
  ("staging",           "A",   "203.0.113.10",   False),   # <- someone's shortcut
  ("ftp",               "A",   "203.0.113.10",   False),   # <- 2019 called
  ("mail",              "A",   "203.0.113.25",   False),   # legitimately DNS-only (MX host)
  ("dev-old",           "A",   "198.51.100.7",   False),   # decommissioned? who knows
]
ORIGIN = "203.0.113.10"
print(f"{'record':12}{'type':>7}{'target':>16}{'proxied':>9}   assessment")
leaks = []
for name, t, target, prox in ZONE:
    if prox:
        a = "protected — resolves to edge IPs"
    elif target == ORIGIN:
        a = "*** ORIGIN EXPOSED — publishes the real IP the WAF is supposed to hide"
        leaks.append(name)
    elif t == "A" and name == "mail":
        a = "DNS-only by design (mail); ensure it is NOT the same box as the origin"
    else:
        a = "DNS-only; verify the host still exists and needs to be public"
    print(f"{name:12}{t:>7}{target:>16}{'yes' if prox else 'NO':>9}   {a}")

print(f"\n{len(leaks)} record(s) leak the origin IP: {', '.join(leaks)}")
print("\nWith 203.0.113.10 published, an attacker connects to it DIRECTLY:")
print("   - the WAF inspects nothing (traffic never touches the edge)")
print("   - DDoS protection absorbs nothing (the attack targets the origin)")
print("   - your cache saves nothing")
print("\nThe fixes, in order of durability:")
print("   1. proxy or delete the leaking records")
print("   2. change the origin IP afterward — the old one is already harvested")
print("   3. firewall the origin to accept traffic ONLY from Cloudflare's published")
print("      IP ranges (or better, connect it via Tunnel — Chapter 06 — and stop")
print("      having a public origin IP at all)")
EOF
```

**Expected result:** Two records leak the live origin address, and the fix list ends at the structural answer — an origin reachable only through the edge, or with no public address at all. Step 2 is the one people skip: proxying the record hides the IP *going forward*, but certificate-transparency logs and DNS history already recorded it, so rotation is part of the remediation, not paranoia.

**Negative test:** Auditing only records you remember creating. The leak is precisely the record nobody remembers — `dev-old` pointing at an address nobody can identify is a finding too.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.3 — Hit ratio, TTLs, and what a purge costs

**Objective:** Put numbers on cache decisions.

```bash
python3 - <<'EOF'
REQ_PER_MIN = 120_000
print("Steady state at three hit ratios:")
print(f"{'hit ratio':>10}{'edge-served/min':>17}{'origin load/min':>17}   origin experience")
for hr in (0.70, 0.90, 0.98):
    print(f"{hr*100:>9.0f}%{REQ_PER_MIN*hr:>17,.0f}{REQ_PER_MIN*(1-hr):>17,.0f}   {'comfortable' if hr>.95 else ('fine' if hr>.85 else 'working hard')}")
print("\n90% -> 98% cuts origin load by a factor of 5 (12,000 -> 2,400 req/min).")
print("The last few points of hit ratio are worth more than the first seventy.\n")

# The purge event
print("PURGE EVERYTHING at t=0; cache rewarms as objects are re-requested:")
import math
print(f"{'minute':>7}{'hit ratio':>11}{'origin req/min':>16}")
for minute in (0, 1, 2, 5, 10, 20):
    hr = 0.98 * (1 - math.exp(-minute/4)) if minute else 0.0
    print(f"{minute:>7}{hr*100:>10.0f}%{REQ_PER_MIN*(1-hr):>16,.0f}")
print(f"\nAt t=0 the origin takes the FULL {REQ_PER_MIN:,} req/min — a 50x surge against")
print("its steady-state 2,400. If the origin cannot survive ~50x for several minutes,")
print("'purge everything' is a self-inflicted outage with a deploy button.")
print("\nAlternatives, in order of preference:")
print("   purge by URL/tag/prefix  -> only changed objects re-fetch")
print("   versioned asset names    -> /app.3f2a1.js never needs purging at all")
print("   purge everything         -> migrations and emergencies, with the origin")
print("                               scaled for the rewarm you just scheduled")
EOF
```

**Expected result:** The 90→98% step cuts origin load fivefold, and a full purge briefly returns the origin to 100% of traffic — a 50x surge over its 98%-cached steady state. Both numbers argue the same point from opposite ends: the origin's real capacity requirement is set by the *cache-miss* scenarios you permit, not by steady state.

**Negative test:** Sizing the origin for steady-state load because "the cache handles the rest." The first full purge, cache-busting deploy, or long-tail crawl becomes an outage that the CDN gets blamed for.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Anycast understood as one mechanism producing both latency and attack distribution.
- [ ] Proxied versus DNS-only records audited, with origin-IP rotation after any leak.
- [ ] Cache keys kept low-cardinality; TTLs chosen against change-propagation needs.
- [ ] Origin sized for the miss scenarios permitted, not for steady state.
