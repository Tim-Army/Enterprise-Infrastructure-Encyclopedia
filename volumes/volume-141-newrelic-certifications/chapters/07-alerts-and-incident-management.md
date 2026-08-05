# Chapter 07: Alerts and Incident Management

## Learning Objectives

- Build the alert hierarchy: policies, conditions, incidents, and workflows.
- Route notifications by destination and urgency, and mute deliberately.
- Practice alert quality management — measuring and reducing noise.
- Run post-incident analysis that feeds back into the alert configuration.

*Exam relevance: REP Section 1 in full — "New Relic alert concepts (policies, conditions, incidents), custom alert policies, conditions, notification channels and incident workflows, alert quality management (noise reduction), incident post-mortem and root cause analysis (RCA)" — plus the alerting items in NVF Sections 2 and 5.*

## The hierarchy

| Object | Is | Example |
|:---|:---|:---|
| **Condition** | A NRQL query plus thresholds — the thing that detects | "error rate > 3% for 5 minutes" |
| **Policy** | A container grouping related conditions | "checkout-prod alerts" |
| **Incident** | A condition's threshold violated — the thing that opens | "error rate condition breached at 10:04" |
| **Issue** | One or more incidents grouped for notification | What a human actually receives |
| **Workflow** | Routing: which issues go where, enriched how | "tier-1 app issues → PagerDuty; rest → Slack" |

Because a **condition is a NRQL query**, everything Chapter 03 established applies with teeth: the `WHERE` clause that under-counts errors on a dashboard under-counts them in the condition, and Lab 3.3's three-way agreement problem is most dangerous here, where the failure is a page that never fires.

Threshold types matter operationally: **static** thresholds ("above 3%") for signals with known meaning, **baseline** conditions ("deviates from its recent normal") for signals whose absolute level varies. Baselines inherit the caution from [Volume CXL's Davis chapter](../../volume-140-dynatrace-certifications/chapters/06-davis-ai-problems-and-root-cause.md): they answer "is this different?", never "is this acceptable?" — a chronically bad signal baselines as normal.

## Alert quality management

REP names **"alert quality management (noise reduction)"** as syllabus material, which makes New Relic unusual: the vendor is examining you on whether your alerts are *good*, not just whether you can create them.

Quality is measurable. For each condition over a trailing window:

- **Action rate** — of the times it fired, how often did a human do something?
- **Sleep cost** — how many of its pages arrived outside business hours?
- **Coverage** — did real incidents occur that it should have caught and did not?

A condition with a 2% action rate is not an alert; it is a subscription to being interrupted. The lab builds the audit, because the numbers usually surprise the team that owns them.

## Muting and maintenance

Muting rules suppress notifications for a scope and duration. The discipline is identical to the silence discipline in [Volume CXXXIX](../../volume-139-grafana-observability/chapters/08-recording-rules-alerting-and-slos.md): **every mute has an expiry and a reason**, or six months later a critical condition is discovered to have been quietly muted since a forgotten maintenance window.

## Post-incident analysis

REP's last Section 1 item — "incident post-mortem and root cause analysis" — closes the loop. The part teams skip is the **alert retrospective** inside the postmortem: for this incident, which conditions fired, which fired late, which should have fired and did not, and which fired and were ignored because they always fire? Each answer is a configuration change. An alerting estate that never absorbs post-incident findings converges on noise; one that does converges on signal.

## Hands-On Lab

Python models alert management. **Cost:** none.

### Lab 7.1 — From condition to notified human

**Objective:** Trace the object hierarchy end to end.

```bash
python3 - <<'EOF'
CONDITIONS = [
  # policy,            condition,                          fires?, tier
  ("checkout-prod",   "error rate > 3% / 5min",            True,  1),
  ("checkout-prod",   "p95 latency > 1.5s / 10min",        True,  1),
  ("checkout-prod",   "throughput drop > 40%",             False, 1),
  ("search-prod",     "error rate > 5% / 5min",            False, 2),
  ("batch-jobs",      "job duration > 2x baseline",        True,  3),
]
WORKFLOWS = [
  ("page on-call",  lambda tier, n: tier == 1),
  ("slack channel", lambda tier, n: tier in (1, 2)),
  ("ticket queue",  lambda tier, n: tier == 3),
]
incidents = [(p, c, t) for p, c, f, t in CONDITIONS if f]
print(f"{len(CONDITIONS)} conditions evaluated -> {len(incidents)} incidents open\n")

# incidents in the same policy group into one issue
from collections import defaultdict
issues = defaultdict(list)
for p, c, t in incidents: issues[p].append((c, t))
print(f"grouped into {len(issues)} issue(s):")
for pol, members in issues.items():
    tier = min(t for _, t in members)
    routes = [name for name, rule in WORKFLOWS if rule(tier, len(members))]
    print(f"   issue '{pol}' ({len(members)} incident(s), tier {tier}) -> {', '.join(routes)}")
    for c, _ in members: print(f"      - {c}")

print("\nThe grouping did real work: checkout-prod's two simultaneous incidents")
print("(errors AND latency) arrive as ONE page with both facts attached — the")
print("on-call reads a story, not two competing interruptions.")
print("The batch job opened an incident and paged NOBODY: tier-3 routes to tickets.")
print("Detection and notification are separate decisions, made by separate objects.")
EOF
```

**Expected result:** Three incidents collapse into two issues; checkout's pair arrives as one enriched page while the batch job becomes a ticket. The last line is the model to retain — conditions decide *what is true*, workflows decide *who cares* — and keeping those decisions in separate objects is what makes each independently reviewable.

**Negative test:** Wiring every condition straight to the paging channel "so nothing is missed." Nothing is missed and everything is ignored, at roughly equal rates.

**Cleanup:** None.

### Lab 7.2 — Audit alert quality

**Objective:** Score conditions by action rate and sleep cost.

```bash
python3 - <<'EOF'
CONDITIONS = [
  # condition,                        fires/90d, acted_on, night_pages
  ("checkout error rate",                   11,       10,        3),
  ("checkout p95 latency",                  19,       14,        5),
  ("host CPU > 90%",                       210,        4,       61),
  ("disk > 80% (any host)",                340,        9,       88),
  ("payment-svc heartbeat",                  6,        6,        2),
  ("JVM old-gen > 70%",                    124,        2,       40),
]
print(f"{'condition':28}{'fires':>7}{'acted':>7}{'action%':>9}{'night':>7}   verdict")
for name, fires, acted, night in sorted(CONDITIONS, key=lambda c: c[2]/c[1]):
    rate = acted/fires*100
    if rate < 5:      v = "DELETE or rebuild — this is noise wearing an alert's name"
    elif rate < 30:   v = "raise threshold / add duration / route to tickets"
    elif rate < 70:   v = "tune: split by tier, review threshold"
    else:             v = "healthy — keep"
    print(f"{name:28}{fires:>7}{acted:>7}{rate:>8.0f}%{night:>7}   {v}")

total_night = sum(c[3] for c in CONDITIONS)
wasted_night = sum(c[3] for c in CONDITIONS if c[2]/c[1] < .1)
print(f"\nnight pages in 90 days: {total_night}, of which {wasted_night} ({wasted_night/total_night*100:.0f}%) came from")
print("conditions nobody acts on. That is the on-call rotation's sleep, spent on")
print("conditions with a measured action rate under 10%.")
print("\nThe audit itself is REP material: 'alert quality management (noise")
print("reduction)' is a syllabus item, and this table — fires, action rate, night")
print("cost — is the minimum viable version. Run it quarterly; the numbers drift.")
EOF
```

**Expected result:** The infrastructure conditions fire hundreds of times with single-digit action rates, contributing 95% of night pages, while the heartbeat and error-rate conditions score healthy. The proportion is the wake-up call — most of the rotation's lost sleep traces to conditions the audit says to delete or reroute.

**Negative test:** Judging alert quality by incident count ("we caught 340 disk events!"). Fires are cost, not value; the value column is *acted on*.

**Cleanup:** None.

### Lab 7.3 — The alert retrospective

**Objective:** Turn one incident into configuration changes.

```bash
python3 - <<'EOF'
INCIDENT = "payment provider degradation, 42 min, revenue impact"
ALERT_REVIEW = [
  # condition,                     behavior during incident,            finding
  ("checkout error rate",         "fired at t+9m",                     "LATE — 5min window + 3% threshold; consider 2%/3min for tier-1"),
  ("payment-svc external calls",  "did not exist",                     "GAP — the failing dependency had no condition at all"),
  ("checkout p95 latency",        "fired at t+11m",                    "redundant confirmation; fine"),
  ("host CPU > 90%",              "fired 6x, unrelated hosts",         "NOISE — actively distracted the responder mid-incident"),
  ("synthetic checkout journey",  "failed at t+3m, went to muted channel","MISROUTED — earliest true signal, nobody saw it"),
]
print(f"POST-MORTEM: {INCIDENT}\n")
print(f"{'condition':28}{'during the incident':38}finding")
for c, b, f in ALERT_REVIEW:
    print(f"{c:28}{b:38}{f}")

print("\nResulting configuration changes (each finding becomes one):")
print("  1. NEW condition: payment-svc external error rate (the gap)")
print("  2. checkout error rate: 3%/5min -> 2%/3min for tier-1 (the latency)")
print("  3. synthetic journey failures -> tier-1 workflow, no longer muted (the misroute)")
print("  4. host CPU condition -> Lab 7.2's audit queue (the noise)")
print("\nEarliest available signal was the synthetic at t+3m; first signal a human")
print("SAW was t+9m. Six minutes of revenue impact were spent on a routing choice.")
print("An alert estate that absorbs one such retrospective per incident converges")
print("on signal; one that never does converges on noise. The postmortem section")
print("REP examines is this table, not the apology paragraph.")
EOF
```

**Expected result:** Five behaviors become four concrete configuration changes, with the sharpest finding being that the earliest true signal existed at t+3m and was muted. That six-minute routing gap is the shape of most real alerting failures — the detection existed, the notification path failed — which is why the retrospective reviews both halves.

**Negative test:** A postmortem that assigns action items to the *service* and none to the *alerting*. The next incident replays the same nine silent minutes.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Conditions, policies, incidents, issues, and workflows built as separate, reviewable decisions.
- [ ] Static versus baseline thresholds chosen per signal, with baseline limits understood.
- [ ] Alert quality audited by action rate and night cost, quarterly.
- [ ] Every mute given an expiry and a reason.
- [ ] Postmortems producing alert-configuration changes, not only service fixes.
