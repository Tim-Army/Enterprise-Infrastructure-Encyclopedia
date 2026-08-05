# Chapter 02: The Intelligent Edge — DNS, GTM, and Delivery

## Learning Objectives

- Explain how Akamai's edge platform maps users to servers, and how it differs from anycast.
- Use Edge DNS and Global Traffic Management for resilience and steering.
- Understand the Property Manager configuration model — rules, behaviors, and activation.
- Reason about staging-versus-production activation as a change-safety mechanism.

*Course relevance: the delivery substrate beneath every Akamai University course; **Edge DNS and GTM** is one of the twelve Certified Partner Solutions Architect specializations.*

## Mapping, not anycast

[Volume CXLII](../../volume-142-cloudflare-certifications/chapters/02-the-edge-network-dns-and-caching.md) built its edge chapter on anycast: same IPs everywhere, BGP chooses. Akamai's classic approach is different and worth understanding precisely *because* the two produce similar outcomes by different means:

| | **Anycast** (Cloudflare-style) | **DNS mapping** (Akamai-style) |
|:---|:---|:---|
| The user reaches an edge because… | BGP routed them to the nearest announcement | DNS **answered** with servers chosen for them |
| The choosing happens | In routing, continuously | At resolution time, per lookup |
| Granularity | Whatever BGP sees | Whatever the mapping system knows — load, health, network distance |
| Failure response | Routing reconverges | The next DNS answer simply names different servers |

Akamai's mapping system answers each DNS lookup with edge servers selected for that resolver at that moment. The practical consequence for operators: **TTLs are short and answers vary** — two users, or one user twice, may legitimately receive different edge IPs. Hard-coding an Akamai edge IP anywhere is wrong by design.

## Edge DNS and GTM

Two distinct DNS products that get conflated:

- **Edge DNS** is authoritative DNS hosting — your zones served from the edge platform, built for volume and DDoS resistance.
- **Global Traffic Management (GTM)** is *intelligent* DNS answering — load-balancing and failover across your data centers by liveness, load, geography, and performance. GTM answers the question "which of my origins should this user reach?", which is a different question from "where is my zone hosted?"

The GTM design discipline mirrors every load-balancer chapter on this shelf: **failover tested is failover owned.** A GTM policy that has never had its primary marked down in a controlled test is a hypothesis, and the lab models the arithmetic of what liveness-test intervals and TTLs mean for real failover time.

## Property Manager

Akamai delivery configuration lives in **properties** — per-site (or per-group-of-sites) configurations built from **rules** containing **criteria** (when does this rule match?) and **behaviors** (what happens — caching, origin selection, header manipulation, redirects). Rules nest; children refine parents.

Two properties of the model shape daily work:

1. **Versioning is native.** Properties have numbered versions; you edit a new version while the old serves traffic.
2. **Activation is staged.** A version activates to the **staging network** first — real Akamai edges, not receiving production traffic, testable by pointing your client at staging hostnames — then to **production**. The staging step is the platform's built-in "try it on real infrastructure before users see it," and skipping it is the local variant of the drift sins Chapter 08 of Volume CXLII cataloged.

## Hands-On Lab

Python models edge behavior. **Cost:** none.

### Lab 2.1 — Mapping versus anycast, observed from a resolver

**Objective:** Model why Akamai answers differ per resolver and per moment.

```bash
python3 - <<'EOF'
import random
random.seed(43)
EDGES = {
  "frankfurt": {"load": 0.42, "healthy": True},
  "warsaw":    {"load": 0.71, "healthy": True},
  "vienna":    {"load": 0.30, "healthy": True},
  "prague":    {"load": 0.55, "healthy": False},   # maintenance
}
def map_answer(resolver_region, t):
    # score = proximity (fixed per resolver) + live load + health gate
    proximity = {"frankfurt": 8, "warsaw": 3, "vienna": 6, "prague": 4}
    scored = []
    for name, e in EDGES.items():
        if not e["healthy"]: continue
        load_now = min(0.95, e["load"] + 0.15*random.random())    # load moves
        scored.append((proximity[name] + (1-load_now)*10, name, load_now))
    scored.sort(reverse=True)
    return scored[:2]

print("Resolver in Poland, five lookups over ten minutes (TTL ~20s):\n")
for t in range(5):
    ans = map_answer("pl", t)
    names = ", ".join(f"{n} (load {l:.0%})" for _, n, l in ans)
    print(f"   t+{t*2}min  -> {names}")
print("\nThree observations:")
print("  1. prague never appears — unhealthy edges are simply not answered.")
print("  2. the answer CHANGES as load moves; two lookups differ legitimately.")
print("  3. nothing about this is visible in traceroute — the intelligence is in")
print("     the ANSWER, not the route. (Anycast puts it in the route instead.)")
print("\nOperator consequences:")
print("  - never hard-code an edge IP; it is valid for one answer's TTL")
print("  - monitoring must resolve like a USER (through DNS), not ping a pet IP")
print("  - 'the site is slow from my office' starts with WHICH edge your office")
print("    resolver was mapped to — capture the answer, not just the symptom")
EOF
```

**Expected result:** Five lookups produce shifting two-edge answers with the unhealthy edge absent throughout. The three operator consequences are the practical content — every one of them is a real support-ticket pattern, and all three follow from the single fact that the intelligence lives in the DNS answer.

**Negative test:** Building a synthetic monitor against one resolved edge IP. It tests one edge's health, not your service — and outlives the answer's validity by months.

**Cleanup:** None.

### Lab 2.2 — GTM failover arithmetic

**Objective:** Compute real failover time from liveness intervals and TTL.

```bash
python3 - <<'EOF'
CONFIGS = [
  # name,                 probe_interval_s, failures_to_down, ttl_s
  ("aggressive",                       10,  2,                 30),
  ("default-ish",                      60,  3,                 60),
  ("conservative",                    120,  3,                300),
]
print("Primary data center dies at t=0. When do users actually move?\n")
print(f"{'config':16}{'detect (s)':>11}{'ttl drain (s)':>14}{'worst user moves at':>21}")
for name, probe, fails, ttl in CONFIGS:
    detect = probe * fails                # last-good to declared-down (worst case)
    worst = detect + ttl                  # + cached answers must expire
    print(f"{name:16}{detect:>11}{ttl:>14}{worst:>20}s")
print("\nThe failover time is DETECTION + TTL, and both terms are configuration:")
print("  - detection: probe interval x failures-to-declare (2m to 6m above)")
print("  - drain: every resolver holding a cached answer keeps sending users to")
print("    the dead primary until the TTL runs out")
print("\nconservative config: SEVEN MINUTES of users hitting a dead data center —")
print("after GTM did everything right. The config was the outage's second half.")
print("\nTrades to state honestly:")
print("  aggressive probing costs load on origins and risks flapping on a")
print("  brownout (add hysteresis); short TTLs cost resolver traffic. The answer")
print("  is chosen per service by RTO, not copied from a blog. And then TESTED:")
print("  mark the primary down deliberately in a window, time the real drain.")
EOF
```

**Expected result:** Failover spans 50 seconds to seven minutes across three plausible configs, decomposed into detection and TTL-drain terms. The conservative row is the argument — GTM behaving perfectly still delivers seven minutes of failed users when the configuration was chosen by copying rather than by RTO — and the closing instruction to test in a window converts the arithmetic into an owned number.

**Negative test:** Setting probes aggressive and TTL to 10 seconds everywhere. Now a thirty-second origin brownout triggers a full flap cycle, and your resolvers carry 6x the query load, for services whose RTO was "within the hour."

**Cleanup:** None.

### Lab 2.3 — Property versions and the staging gate

**Objective:** Model why staged activation catches what review does not.

```bash
python3 - <<'EOF'
VERSIONS = [
  # ver, change,                                         review_catches, staging_catches
  (41, "add caching behavior for /static/*",             True,  True),
  (42, "origin failover tweak",                          True,  True),
  (43, "redirect rule: http->https for legacy paths",    False, True),   # loop with an old rule
  (44, "header rewrite for the mobile app",              False, True),   # breaks an API client
  (45, "tighten cache key (remove a query param)",       False, False),  # only visible at prod scale
]
print(f"{'ver':>4}  {'change':46}{'review':>8}{'staging':>9}")
caught_rev = caught_stg = escaped = 0
for v, change, rev, stg in VERSIONS:
    r = "catches" if rev else "misses"
    s = "catches" if stg else "MISSES"
    if rev: caught_rev += 1
    elif stg: caught_stg += 1
    else: escaped += 1
    print(f"{v:>4}  {change:46}{r:>8}{s:>9}")
print(f"\nreview caught {caught_rev}, staging caught {caught_stg} more, {escaped} escaped to production.")
print("\nWhat staging catches that review cannot: INTERACTIONS. v43's redirect is")
print("correct alone and loops against a rule from 2023; v44's rewrite is fine for")
print("browsers and breaks one API client — both visible only when real requests")
print("hit real edge config. Staging is Akamai's built-in 'real infrastructure,")
print("no users' step; the discipline is refusing to skip it under deadline.")
print("\nAnd v45 escaped anyway: cache-key changes reveal themselves at production")
print("traffic diversity. The lesson is layered defenses, not staging worship —")
print("version 44 is one activation away, and INSTANT ROLLBACK (activate the")
print("previous version) is the recovery path the versioning model exists for.")
EOF
```

**Expected result:** Review catches two changes, staging catches two interaction bugs review structurally cannot, and one cache-key change escapes both — resolved by instant version rollback. The layering is the honest lesson: staging is not a guarantee but a filter, and the versioned-activation model makes the escape recoverable in one action.

**Negative test:** Activating straight to production "because the change is trivial." v43 was trivial; the 2023 rule it looped against was the part nobody remembered.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] DNS mapping distinguished from anycast, with its operator consequences.
- [ ] Edge DNS separated from GTM, and GTM failover computed as detection + TTL drain.
- [ ] Failover configs chosen by RTO and proven in a test window.
- [ ] Property versions activated through staging, with rollback as the recovery path.
