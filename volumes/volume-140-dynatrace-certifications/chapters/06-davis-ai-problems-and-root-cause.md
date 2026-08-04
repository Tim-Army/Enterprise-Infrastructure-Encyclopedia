# Chapter 06: Davis AI, Problems, and Root Cause

## Learning Objectives

- Explain deterministic, causation-based analysis and how it differs from correlation.
- Read a problem: what it groups, what it names as root cause, and why.
- Tune baselining and alerting profiles so problems mean something.
- State the conditions under which causal root cause can be trusted.

*Exam relevance: **Problems And Resolution** is one of the six Associate domains and carries into every Professional and Specialist track.*

## Deterministic, causation-based analysis

Dynatrace's documentation describes Davis AI as performing **"deterministic, causation-based analysis"**, identifying **"root cause with topology and dependency context"**, and correlating **"code changes, deployments, configuration, and policy updates to show what changed and why a problem occurred."**

The contrast with the usual approach is worth stating precisely, because the marketing word "AI" obscures it:

| Approach | Method | Produces |
|:---|:---|:---|
| **Statistical anomaly detection** | Each signal compared against its own history | A list of things that look unusual |
| **Correlation** | Signals that moved together | Things that changed at the same time |
| **Causation over topology** | Anomalies mapped onto the dependency graph, following call direction | A claim about *which* anomaly caused the others |

"Deterministic" is the load-bearing word. Given the same telemetry and the same topology, Davis produces the same answer — it is not sampling a probability distribution. That makes its output auditable and reproducible, which matters when the answer is going to reassign an incident to a different team.

## Problems

A **problem** is a grouping of related anomalies with a claimed root cause, an affected-entity set, and an impact assessment. Its defining feature is consolidation: fifty services degrading because one database is slow produce **one problem**, not fifty alerts.

That is the single largest practical difference from threshold-based alerting, and it is the reason the platform is bought. The equivalent burn in a threshold system is fifty pages, five responders, and thirty minutes spent establishing that they are all the same incident.

Problems have a **lifecycle** — open, updated as the blast radius changes, closed when the condition clears — and an **impact level** distinguishing infrastructure, service, and application (user-facing) effects.

## Baselining

Davis learns normal behavior per entity rather than applying global thresholds, which is what allows "slow" to mean something different for a batch job and a checkout API.

Three consequences follow, and all three show up in practice:

1. **A learning period exists.** Immediately after deployment, baselines are unreliable — they have nothing to compare against.
2. **A consistently bad baseline becomes "normal."** If a service has always been slow, its baseline encodes that, and degradation is measured from a bad starting point. Baselines describe what *is*, not what *should be* — that is what SLOs are for (Chapter 08).
3. **Legitimate change requires relearning.** A deliberate architectural improvement will read as an anomaly until the baseline catches up.

## Alerting profiles

An **alerting profile** decides which problems reach whom, filtered by severity, impact, management zone, and tags. The discipline is the same as anywhere else: if everything pages, nothing does. Problems already consolidate the noise; alerting profiles decide which consolidated problems are worth a human at night.

## Hands-On Lab

Python models causal analysis. **Cost:** none.

### Lab 6.1 — Correlation versus causation over topology

**Objective:** Show what the dependency graph adds.

```bash
python3 - <<'EOF'
GRAPH = {                                  # service -> what it calls
  "frontend": ["checkout"], "checkout": ["payments","inventory"],
  "payments": ["postgres"], "inventory": ["postgres","redis"],
  "postgres": [], "redis": [],
}
callers = {}
for s, deps in GRAPH.items():
    for d in deps: callers.setdefault(d, []).append(s)

# all six anomalous within the same minute
anomalies = {
  "frontend": {"t":"10:04:10","metric":"latency +340%"},
  "checkout": {"t":"10:04:08","metric":"latency +310%"},
  "payments": {"t":"10:04:06","metric":"latency +290%"},
  "inventory":{"t":"10:04:06","metric":"latency +280%"},
  "postgres": {"t":"10:04:02","metric":"connection pool exhausted"},
  "redis":    {"t":"10:04:55","metric":"latency +15%"},
}
print("--- CORRELATION: 'these all moved together' ---")
for s, a in sorted(anomalies.items(), key=lambda kv: kv[1]["t"]):
    print(f"   {a['t']}  {s:10} {a['metric']}")
print("   => 6 anomalies, 6 alerts, no ranking. Someone must now work out the order.\n")

print("--- CAUSATION over topology: follow the call direction downward ---")
def deepest_anomalous(node, depth=0, seen=None):
    seen = seen or set()
    if node in seen: return []
    seen.add(node)
    out = [(node, depth)] if node in anomalies else []
    for d in GRAPH.get(node, []):
        out += deepest_anomalous(d, depth+1, seen)
    return out
chain = deepest_anomalous("frontend")
root = max(chain, key=lambda x: x[1])
for n, d in sorted(chain, key=lambda x: x[1]):
    mark = "   <-- ROOT CAUSE" if n == root[0] else ""
    print(f"   {'  '*d}{n:10} depth {d}  {anomalies[n]['metric']}{mark}")

print(f"\n   => ONE problem. Root cause: {root[0]}. Affected: {len(chain)-1} downstream services.")
print(f"   redis moved too (+15% at 10:04:55) but is NOT in the causal chain to the")
print( "   symptom — it is later, milder, and downstream of a different caller.")
print( "   Correlation would have included it. Causation excludes it.\n")
print("Two things the topology supplied that timestamps alone could not:")
print("   1. DIRECTION — postgres is called BY payments, so it can cause payments' latency,")
print("      not the other way round. Timestamps alone cannot establish that.")
print("   2. EXCLUSION — a coincidental anomaly is rejected because no causal path")
print("      connects it to the symptom.")
EOF
```

**Expected result:** Six correlated anomalies collapse into one problem rooted at `postgres`, with `redis` explicitly excluded despite being anomalous in the same window. The two closing points are what topology buys: call **direction** establishes which anomaly can cause which — something timestamps cannot do, since near-simultaneous events have no inherent order — and the absence of a causal path is what lets a coincidence be rejected rather than reported.

**Negative test:** Ranking causes by earliest timestamp. Under clock skew or coarse sampling the ordering inverts, and the "earliest" anomaly may simply be the one whose metric was scraped first.

**Cleanup:** None.

### Lab 6.2 — Baselines describe what is, not what should be

**Objective:** Show why a bad baseline hides a bad service.

```bash
python3 - <<'EOF'
import statistics
SERVICES = {
  "checkout-api":  {"history":[210,205,215,208,212,209,211], "now": 640, "slo_ms": 300},
  "legacy-report": {"history":[8200,8100,8400,8250,8300,8150,8220], "now": 8600, "slo_ms": 2000},
  "search":        {"history":[95,102,88,97,91,99,94],        "now": 130, "slo_ms": 250},
}
print(f"{'service':16}{'baseline':>10}{'now':>8}{'vs baseline':>13}{'SLO':>8}{'vs SLO':>9}   verdict")
for name, d in SERVICES.items():
    base = statistics.mean(d["history"])
    dev  = (d["now"]/base - 1) * 100
    anomaly = dev > 50
    breach  = d["now"] > d["slo_ms"]
    chronic = base > d["slo_ms"]
    if anomaly and breach:  v = "problem raised AND SLO breached"
    elif anomaly:           v = "problem raised, still within SLO"
    elif breach and chronic:v = "*** NO PROBLEM RAISED — chronically bad is 'normal'"
    else:                   v = "healthy"
    print(f"{name:16}{base:>10.0f}{d['now']:>8}{dev:>12.0f}%{d['slo_ms']:>8}{'BREACH' if breach else 'ok':>9}   {v}")

print("\nlegacy-report has ALWAYS taken ~8.2 seconds against a 2-second SLO.")
print("Its 8600ms today is only 4% off baseline, so Davis correctly reports no anomaly:")
print("nothing changed. The service is nonetheless failing its objective, permanently.")
print("\nThat is not a defect in baselining — it is baselining working as designed.")
print("A baseline answers 'is this DIFFERENT?'. It cannot answer 'is this GOOD ENOUGH?'")
print("Only an SLO encodes intent (Chapter 08). You need both:")
print("   baseline -> catches sudden regressions against actual behavior")
print("   SLO      -> catches chronic underperformance a baseline has normalized")
EOF
```

**Expected result:** `legacy-report` triggers no problem while sitting four times over its SLO, because 8600 ms is normal *for it*. This is the chapter's most transferable idea: anomaly detection and objectives answer different questions, and a team running only baselines will never be told about a service that has been quietly failing since the day it launched.

**Negative test:** Treating "no open problems" as "everything is meeting its commitments." It means nothing changed recently.

**Cleanup:** None.

### Lab 6.3 — Alerting profiles

**Objective:** Route consolidated problems without recreating alert fatigue.

```bash
python3 - <<'EOF'
PROBLEMS = [
  # id, impact,        severity,      zone,       entities, user_facing
  ("P-1","APPLICATION","availability","payments",  42, True),
  ("P-2","SERVICE",    "slowdown",    "payments",   3, False),
  ("P-3","INFRA",      "resource",    "general",    1, False),
  ("P-4","APPLICATION","slowdown",    "general",  180, True),
  ("P-5","INFRA",      "resource",    "staging",   12, False),
  ("P-6","SERVICE",    "errors",      "pci",        2, True),
]
PROFILES = [
  ("page-oncall",  lambda p: p[5] and p[1]=="APPLICATION" and p[4] >= 10),
  ("page-pci",     lambda p: p[3]=="pci" and p[5]),
  ("ticket-team",  lambda p: p[1]=="SERVICE" and not p[5]),
  ("dashboard",    lambda p: p[3]=="staging" or p[1]=="INFRA"),
]
print(f"{'problem':8}{'impact':13}{'severity':14}{'zone':10}{'entities':>9}  routed to")
routed = {n: [] for n, _ in PROFILES}
for p in PROBLEMS:
    hits = [n for n, f in PROFILES if f(p)]
    for h in hits: routed[h].append(p[0])
    print(f"{p[0]:8}{p[1]:13}{p[2]:14}{p[3]:10}{p[4]:>9}  {', '.join(hits) or '(none — visible in UI only)'}")

pages = set(routed["page-oncall"]) | set(routed["page-pci"])
print(f"\nof {len(PROBLEMS)} problems: {len(pages)} page a human, the rest ticket or display")
print(f"   paging: {', '.join(sorted(pages))}")
print("\nRemember these are already CONSOLIDATED problems, not raw alerts. P-4 alone")
print("covers 180 affected entities — in a threshold system that is 180 notifications.")
print("Dynatrace does the first noise reduction; the alerting profile does the second.")
print("\nBoth are needed. Consolidation without routing still pages someone for a")
print("staging resource problem at 3 a.m. — one page instead of twelve, but still a page.")
EOF
```

**Expected result:** Three of six problems page, with the rest ticketed or left on a dashboard. The layering is the point — consolidation reduces fifty alerts to one problem, and the alerting profile then decides whether that one problem is worth waking someone; skipping the second layer leaves you with fewer, but still unnecessary, pages.

**Negative test:** Routing every problem to the on-call channel because "Dynatrace already reduces noise." It reduced it; it did not decide your priorities.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Deterministic causation-based analysis distinguished from correlation and statistics.
- [ ] Problems understood as consolidated groupings with a claimed root cause.
- [ ] Baselines understood as descriptive, with SLOs supplying intent.
- [ ] Alerting profiles applied as the second noise-reduction layer.
