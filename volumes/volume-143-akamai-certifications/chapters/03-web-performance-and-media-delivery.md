# Chapter 03: Web Performance and Media Delivery

## Learning Objectives

- Map the Web Performance portfolio: Ion, mPulse, Image & Video Manager.
- Combine edge caching with offload thinking — the course pair's actual theme.
- Use RUM (mPulse) to steer optimization where users feel it.
- Understand media delivery's different physics: sustained throughput over request latency.

*Course relevance: **Akamai Web Performance Foundations** and **Web Performance & Offload** (University courses with badges); **Media Delivery Foundations / Media Delivery Solutions**; mPulse, Ion, and Image and Video Manager are Certified Partner Solutions Architect specializations.*

## The performance portfolio

| Product | Does | The one idea |
|:---|:---|:---|
| **Ion** | Adaptive web acceleration — caching, connection optimization, adaptive delivery decisions | The edge tunes delivery per user/network rather than one-size |
| **mPulse** | Real user monitoring from the pages you serve | Measure what users *experienced*, then optimize that |
| **Image & Video Manager** | Automated media transformation at the edge — format, quality, size per device | The heaviest bytes on most pages, made someone else's problem |
| **Adaptive Media Delivery** | Streaming delivery (Chapter's second half) | Throughput held steady beats latency shaved |

The Akamai University course naming carries the operating philosophy: Foundations, then **"Web Performance & Offload."** Offload — the fraction of traffic the origin never sees — is the course-title word because it is the number that moves both performance *and* origin economics, and the labs treat it as the primary metric.

## Offload thinking

[Volume CXLII's caching lab](../../volume-142-cloudflare-certifications/chapters/02-the-edge-network-dns-and-caching.md) established hit-ratio arithmetic; this chapter's version adds the enterprise-estate angle the Akamai courses teach: **offload is a portfolio number.** HTML, APIs, static assets, images, and video have different cacheability, different hit ratios, and wildly different byte weights — and the offload a CFO sees is the byte-weighted sum. Optimizing the asset class that dominates *bytes* (almost always media) moves the number; optimizing the class that dominates *requests* may not.

## RUM steering

mPulse is the same discipline as [New Relic's browser chapter](../../volume-141-newrelic-certifications/chapters/05-browser-mobile-and-synthetics.md) and Core Web Vitals at p75: field data over lab data, distributions over averages, segments over aggregates. What the Akamai framing adds is the **steering loop**: RUM identifies which segment (geography, network type, device class) experiences the worst delivery, and edge configuration — Ion's adaptive behaviors, image policies — is then tuned *for that segment* and re-measured. Performance work without the loop is guessing with expensive tools.

## Media delivery is different physics

Web performance optimizes **time-to-interactive** — shaving hundreds of milliseconds off many small objects. Media delivery optimizes **sustained throughput** — keeping a player's buffer fed for minutes to hours. Different failure modes (rebuffering, not slow paint), different metrics (rebuffer ratio, bitrate stability, join time), different edge behavior (large-object caching, segment pre-positioning). The volume keeps them in one chapter because the courses do, but the lab's point is that their dashboards must not be merged: a media property judged by page-load metrics looks fine while streaming fails.

## Hands-On Lab

Python models performance economics. **Cost:** none.

### Lab 3.1 — Offload is byte-weighted

**Objective:** Compute portfolio offload the way the bill reads.

```bash
python3 - <<'EOF'
CLASSES = [
  # class,       req_share, avg_kb, hit_ratio
  ("HTML",           0.18,     40,   0.30),
  ("API JSON",       0.34,      8,   0.05),
  ("static assets",  0.28,     55,   0.97),
  ("images",         0.17,    280,   0.92),
  ("video segments", 0.03,   1800,   0.96),
]
total_req = 100_000  # per minute
total_bytes = sum(s*total_req*kb for _, s, kb, _ in CLASSES)
print(f"{'class':16}{'req %':>7}{'byte %':>8}{'hit %':>7}{'bytes offloaded %pt':>21}")
req_offload = bytes_offload = 0
for name, share, kb, hr in CLASSES:
    byte_share = share*total_req*kb/total_bytes
    req_offload += share*hr
    contrib = byte_share*hr
    bytes_offload += contrib
    print(f"{name:16}{share*100:>6.0f}%{byte_share*100:>7.1f}%{hr*100:>6.0f}%{contrib*100:>20.1f}")
print(f"\nrequest-weighted offload: {req_offload*100:.1f}%")
print(f"byte-weighted offload   : {bytes_offload*100:.1f}%   <- the number the origin bill sees")
print("\nNow the improvement question — one point of effort, where?")
api_gain   = 0.34*8*total_req/total_bytes * (0.35-0.05)
video_gain = 0.03*1800*total_req/total_bytes * (0.99-0.96)
print(f"  heroic API caching (5% -> 35% hit): +{api_gain*100:.2f} byte-offload points")
print(f"  modest video tuning (96% -> 99%) : +{video_gain*100:.2f} byte-offload points")
print("\n3% of requests (video) outweigh 34% of requests (API) because bytes, not")
print("requests, are what the origin serves and the network carries. 'Offload' in")
print("the course title is byte-weighted thinking — optimize where the WEIGHT is.")
EOF
```

**Expected result:** Request-weighted offload around 53% against byte-weighted offload near 89%, and the improvement comparison showing modest video tuning beating heroic API caching. The one-line discipline — optimize where the weight is — is the entire "& Offload" half of the course title.

**Negative test:** Reporting request-hit-ratio to finance as "offload." The bill disagrees, and the disagreement is the byte weighting.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 3.2 — The RUM steering loop

**Objective:** Let field data choose the optimization target.

```bash
python3 - <<'EOF'
SEGMENTS = [
  # segment,                 traffic %, p75 LCP s, dominated by
  ("EU fiber, desktop",           28,   1.7,  "server think time"),
  ("EU mobile, 4G/5G",            24,   2.9,  "images"),
  ("NA broadband",                21,   2.1,  "third-party scripts"),
  ("APAC mobile, mixed",          15,   4.8,  "images + distance"),
  ("LATAM mobile, 3G-heavy",      12,   6.1,  "images + connection setup"),
]
GOOD = 2.5
print(f"{'segment':26}{'traffic':>8}{'p75 LCP':>9}{'vs 2.5s':>9}   dominated by")
for s, t, lcp, why in SEGMENTS:
    verdict = "good" if lcp <= GOOD else "POOR" if lcp > 4 else "needs work"
    print(f"{s:26}{t:>7}%{lcp:>8.1f}s{verdict:>9}   {why}")
site_p75 = 2.6   # traffic-weighted, roughly
print(f"\nsite-wide p75 LCP: ~{site_p75}s — 'needs improvement', cause invisible.")
print("\nThe steering loop the course teaches:")
print("  1. SEGMENT the RUM data (above) — the aggregate hides three different problems")
print("  2. rank by traffic x severity: APAC+LATAM mobile = 27% of users in POOR,")
print("     both dominated by IMAGES")
print("  3. apply the EDGE fix for that cause: Image & Video Manager policies —")
print("     device-appropriate formats/quality — no app release required")
print("  4. RE-MEASURE the same segments; expect APAC/LATAM to move, EU fiber not to")
print("\nThe anti-pattern: optimizing the aggregate. Minifying JS (helps NA's")
print("third-party problem slightly) does nothing for the 27% whose problem is")
print("image bytes on slow radios — and the site-wide number barely moves either way.")
EOF
```

**Expected result:** A mediocre site-wide p75 decomposing into three unrelated segment problems, with image policies for the 27% in POOR as the ranked first move. The loop's four steps are the course content; the anti-pattern paragraph is why aggregate-driven optimization disappoints everyone equally.

**Negative test:** Shipping an optimization without re-measuring the target segment. If APAC's p75 did not move, the fix did not fix — regardless of how the aggregate wiggled.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 3.3 — Web metrics versus media metrics

**Objective:** Show why one dashboard cannot judge both.

```bash
python3 - <<'EOF'
import random
random.seed(33)
# A property serving both a storefront and live video
WEB = {"p75_lcp_s": 2.1, "p95_ttfb_ms": 420, "error_rate": 0.4}
MEDIA_SESSIONS = []
for _ in range(2000):
    join = random.uniform(0.8, 3.0)
    rebuf = max(0, random.gauss(0.012, 0.02))     # rebuffer ratio
    MEDIA_SESSIONS.append((join, min(rebuf, 0.2)))

avg_rebuf = sum(r for _, r in MEDIA_SESSIONS)/len(MEDIA_SESSIONS)
bad_sessions = sum(1 for _, r in MEDIA_SESSIONS if r > 0.02)
print("WEB dashboard (storefront):")
print(f"   p75 LCP {WEB['p75_lcp_s']}s (good) · p95 TTFB {WEB['p95_ttfb_ms']}ms · errors {WEB['error_rate']}%")
print("   verdict: healthy\n")
print("MEDIA reality (live stream), invisible to every metric above:")
print(f"   mean rebuffer ratio : {avg_rebuf*100:.2f}% of watch time")
print(f"   sessions >2% rebuffering: {bad_sessions} of {len(MEDIA_SESSIONS)} ({bad_sessions/len(MEDIA_SESSIONS)*100:.0f}%)")
print("   join time p75       : ~2.4s")
print(f"\n{bad_sessions/len(MEDIA_SESSIONS)*100:.0f}% of viewers have a degraded stream while the property's")
print("web dashboard is entirely green — because REBUFFERING IS NOT A PAGE METRIC.")
print("Media failure is sustained-throughput failure: the buffer drains over 30s,")
print("no request errors, no slow TTFB, nothing a web SLO watches.")
print("\nThe course split (Web Performance vs Media Delivery Foundations) is the")
print("dashboard split: judge each workload by its own physics —")
print("   web   : LCP/INP, TTFB, error rate")
print("   media : join time, REBUFFER RATIO, bitrate stability")
EOF
```

**Expected result:** A green web dashboard over a stream where about a third of sessions (here 36%) rebuffer above 2%. The physics point carries the chapter — media failure produces no request errors and no slow paints, so web metrics stay green while viewers churn, and the course catalog's split into two foundations is the correct monitoring architecture, not marketing taxonomy.

**Negative test:** Adding the stream to the web SLO "for coverage." It contributes nothing but false confidence; every media failure mode passes it.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] The performance portfolio mapped: Ion, mPulse, Image & Video Manager, media delivery.
- [ ] Offload computed byte-weighted, and effort ranked by weight.
- [ ] The RUM steering loop run: segment → rank → edge fix → re-measure.
- [ ] Web and media workloads judged by their own metrics, on separate dashboards.
