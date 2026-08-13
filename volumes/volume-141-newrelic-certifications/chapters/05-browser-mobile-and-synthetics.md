# Chapter 05: Browser, Mobile, and Synthetics

## Learning Objectives

- Monitor client-side performance with the browser and mobile agents.
- Read Core Web Vitals and connect them to what users experience.
- Script synthetic monitors that cover journeys, not just uptime.
- Combine real-user and synthetic data for their complementary blind spots.

*Exam relevance: PEP Section 3 (Client-side Performance — "evaluating and improving frontend application performance using browser and mobile monitoring tools as well as synthetic testing") and NVF Section 3 ("configure synthetics in New Relic").*

## Why client-side is its own section

Everything in Chapter 04 measured the server's half of the request. The user's half — DNS, connection, download, render, script execution on a mid-range phone over hotel Wi-Fi — routinely dwarfs it. A service returning in 180 ms can still deliver a five-second experience, and no backend dashboard will show it.

The **browser agent** (injected JavaScript) records page views, timing phases, JavaScript errors, and AJAX calls from real sessions, as events NRQL can query (`PageView` and friends). The **mobile agent** does the analogous job inside native apps, with crash reporting. Both are the RUM half of the RUM/synthetic pairing this shelf has met twice already — the blind-spot analysis from [Volume CXL's DEM chapter](../../volume-140-dynatrace-certifications/chapters/05-digital-experience-monitoring.md) applies verbatim, so this chapter spends its labs on what is new: **vitals and journey scripting**.

## Core Web Vitals

The industry-standard trio, all visible in browser monitoring:

| Vital | Measures | Good | Poor |
|:---|:---|:---|:---|
| **LCP** (Largest Contentful Paint) | When the main content became visible | ≤ 2.5 s | > 4.0 s |
| **INP** (Interaction to Next Paint) | How responsive interactions feel | ≤ 200 ms | > 500 ms |
| **CLS** (Cumulative Layout Shift) | How much the page jumped around | ≤ 0.1 | > 0.25 |

Two properties matter for reading them honestly:

- **They are field metrics with thresholds at the 75th percentile.** The convention is to assess a page by whether the *75th percentile* of real users meets "good" — an average hides exactly the slow tail the thresholds exist for.
- **They measure different failures.** A page can paint fast (good LCP) and still infuriate — buttons that do nothing for 600 ms (poor INP), content that leaps as ads load (poor CLS). One green vital is not a verdict.

## Synthetics

Synthetic monitors run scripted checks from chosen locations on a schedule: ping/simple browser checks for availability, **scripted browser** monitors for multi-step journeys, and API tests for endpoints. Private locations run the same checks from inside your network.

The design question is coverage: an uptime ping on the home page proves almost nothing about whether a customer can *check out*. The journey script — search, add to cart, pay with a test card, confirm — is more work to write and maintain, and it is the one that catches the failures that cost money. The lab quantifies that gap.

## Hands-On Lab

Python models client-side monitoring. **Cost:** none.

### Lab 5.1 — Backend fast, experience terrible

**Objective:** Decompose page experience beyond server time.

```bash
python3 - <<'EOF'
PHASES = [
  # phase,                     ms,   controlled by
  ("DNS + TCP + TLS",          210, "network/CDN"),
  ("Backend (TTFB - conn)",    180, "your APM chapter"),
  ("HTML download",             90, "payload size"),
  ("Render-blocking CSS/JS",  1340, "frontend build"),
  ("Hero image fetch+decode", 1650, "asset pipeline"),
  ("Hydration / JS execution",1120, "frontend code"),
]
total = sum(ms for _, ms, _ in PHASES)
lcp_at = sum(ms for p, ms, _ in PHASES[:5])
print(f"{'phase':28}{'ms':>7}   owner")
for p, ms, owner in PHASES:
    bar = "#" * (ms // 150)
    print(f"{p:28}{ms:>7}   {owner:18} {bar}")
print(f"\ntotal to interactive : {total:,} ms")
print(f"LCP (hero visible)   : {lcp_at:,} ms  -> POOR (threshold: good <= 2500 ms)")
print(f"backend share        : {180/total*100:.0f}% of the user's wait\n")
print("The APM dashboard for this page shows 180 ms and is completely green.")
print(f"The user waited {total/1000:.1f} seconds. {100-180/total*100:.0f}% of that is client-side —")
print("invisible to every backend tool, visible to the browser agent on the first day.")
print("\nThis is why PEP separates 'Backend Application Performance' (Section 2) from")
print("'Client-side Performance' (Section 3): they are different problems, owned by")
print("different teams, measured by different agents.")
EOF
```

**Expected result:** A 4.6-second experience of which the backend contributed 4%, with LCP at ~3.5 s rated POOR while APM shows green. The ownership column is as important as the numbers — each slow phase belongs to a different team, and without client-side telemetry the whole 4.6 seconds gets filed against the one team whose 180 ms was fine.

**Negative test:** Investigating "the site is slow" complaints by tuning the backend because that is where the dashboards are. You can halve 180 ms and the user saves 90 ms of a 4,590 ms wait.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.2 — Read vitals at the 75th percentile

**Objective:** Score a page the way the thresholds intend.

```bash
python3 - <<'EOF'
import random
random.seed(12)
# LCP samples: most users on fast connections, a real slow tail
lcp = [random.lognormvariate(0.62, 0.55) for _ in range(4000)]
def pct(vals, p): return sorted(vals)[int(len(vals)*p/100)]

mean = sum(lcp)/len(lcp)
p50, p75, p95 = pct(lcp,50), pct(lcp,75), pct(lcp,95)
def rate(v): return "GOOD" if v <= 2.5 else ("needs improvement" if v <= 4.0 else "POOR")
print("LCP distribution across 4,000 real page views:")
print(f"   mean : {mean:.2f}s  -> {rate(mean)}")
print(f"   p50  : {p50:.2f}s  -> {rate(p50)}")
print(f"   p75  : {p75:.2f}s  -> {rate(p75)}   <- THE assessment point")
print(f"   p95  : {p95:.2f}s  -> {rate(p95)}")
share_poor = sum(1 for v in lcp if v > 4.0)/len(lcp)*100
print(f"   users with POOR LCP: {share_poor:.1f}%\n")
print("The mean and median both say GOOD. The convention assesses at p75, which")
print(f"here says {rate(p75)} — and {share_poor:.0f}% of users are having a POOR experience the")
print("averages never mention. The 75th-percentile convention exists precisely to")
print("stop 'good on average' from closing the conversation.\n")
print("Three vitals, three different failures — check all of them:")
for name, val, good, poor in (("LCP", p75, 2.5, 4.0), ("INP (p75, ms)", 340, 200, 500), ("CLS (p75)", 0.06, 0.1, 0.25)):
    r = "GOOD" if val <= good else ("needs improvement" if val <= poor else "POOR")
    print(f"   {name:14} {val:>7.2f}  {r}")
print("\nCLS is the only green vital: the page is visually stable while being slow to")
print("paint AND sluggish to touch. One green vital is not a verdict.")
EOF
```

**Expected result:** Mean (2.17 s) and median (1.85 s) both rate GOOD while p75 lands at about 2.7 s — "needs improvement" — with roughly 8% of users in POOR territory, and the three-vital check ends mixed. Both halves push the same discipline: assess at the conventional percentile, and read the vitals as three separate failure modes rather than one score.

**Negative test:** Reporting the mean LCP to stakeholders. It is the one number in the list guaranteed to be dragged toward the fast majority and away from the users who complain.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.3 — Uptime pings versus journey scripts

**Objective:** Measure what each synthetic style would have caught.

```bash
python3 - <<'EOF'
INCIDENTS = [
  ("web server down entirely",                     True,  True),
  ("payment provider rejecting all cards",         False, True),
  ("add-to-cart button broken by JS regression",   False, True),
  ("checkout redirect loop after login",           False, True),
  ("search returning empty results",               False, True),
  ("home page slow but up",                        True,  True),
]
ping_catches    = sum(1 for _, p, _ in INCIDENTS if p)
journey_catches = sum(1 for _, _, j in INCIDENTS if j)
print(f"{'incident':46}{'ping':>6}{'journey':>9}")
for name, p, j in INCIDENTS:
    print(f"{name:46}{'YES' if p else '--':>6}{'YES' if j else '--':>9}")
print(f"\nping monitor catches    : {ping_catches}/{len(INCIDENTS)}")
print(f"journey script catches  : {journey_catches}/{len(INCIDENTS)}")
print("\nEvery incident the ping missed shares a shape: the site is UP and a")
print("specific step is BROKEN. Those are also the expensive ones — a dead")
print("add-to-cart button costs revenue per minute while the uptime board glows green.")
print("\nThe trade is maintenance: journey scripts break when the UI changes, so")
print("script the journeys that make money (checkout, signup, login) and let pings")
print("cover the rest. A failing synthetic that nobody trusts because 'the script is")
print("probably stale again' is worse than no synthetic — treat scripts as code,")
print("updated in the same PR that changes the flow they walk.")
EOF
```

**Expected result:** The ping catches 2 of 6 incidents; the journey script catches all 6, and the four misses are all "up but broken" failures. The maintenance paragraph is the honest half — journey scripts are the highest-value and highest-upkeep synthetic, which is why they belong on the money paths and in the same review cycle as the UI they exercise.

**Negative test:** Scripting every flow in the product. Twenty stale scripts produce daily false alarms, the channel gets muted, and the checkout failure arrives into the muted channel.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Client-side experience decomposed, with backend share put in proportion.
- [ ] Core Web Vitals read at p75, as three separate failure modes.
- [ ] Journey synthetics scripted for revenue paths, maintained as code.
- [ ] RUM and synthetics run together for their complementary blind spots.
